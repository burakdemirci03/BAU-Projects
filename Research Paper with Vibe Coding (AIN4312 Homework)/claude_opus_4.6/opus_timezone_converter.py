"""
Timezone Converter — A GUI tool that converts times between timezones using web scraping.
Scrapes timeanddate.com for timezone offsets and location timezone data.
Uses tkinter for the GUI (1000x500, 2:1 ratio layout).
"""

import tkinter as tk
from tkinter import font as tkfont
import re
import requests
from bs4 import BeautifulSoup
import threading

# ─────────────────────────────────────────────────────────────────────────────
# HEADERS for web requests to avoid bot detection
# ─────────────────────────────────────────────────────────────────────────────
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


# ─────────────────────────────────────────────────────────────────────────────
#  WEB SCRAPING — timezone offset from abbreviation
# ─────────────────────────────────────────────────────────────────────────────
def scrape_tz_offset(tz_abbr: str) -> float:
    """
    Scrape timeanddate.com/time/zones/<abbr> for the UTC offset.
    Returns offset as a float (e.g. -7.0, +5.5).
    Raises ValueError when the abbreviation is unknown.
    """
    abbr_lower = tz_abbr.strip().lower()

    # UTC and GMT are straightforward
    if abbr_lower in ("utc", "gmt"):
        return 0.0

    # Handle explicit offset patterns: UTC+3, GMT-5, UTC+5:30, GMT+5.5
    utc_gmt_match = re.match(
        r'^(utc|gmt)\s*([+-])\s*(\d{1,2})(?::(\d{2}))?$',
        abbr_lower
    )
    if utc_gmt_match:
        sign = 1 if utc_gmt_match.group(2) == '+' else -1
        hours = int(utc_gmt_match.group(3))
        minutes = int(utc_gmt_match.group(4)) if utc_gmt_match.group(4) else 0
        return sign * (hours + minutes / 60.0)

    # Also handle patterns like "UTC+5.5"
    utc_gmt_dec = re.match(
        r'^(utc|gmt)\s*([+-])\s*(\d{1,2}(?:\.\d+)?)$',
        abbr_lower
    )
    if utc_gmt_dec:
        sign = 1 if utc_gmt_dec.group(2) == '+' else -1
        return sign * float(utc_gmt_dec.group(3))

    # Scrape the timezone abbreviation page
    url = f"https://www.timeanddate.com/time/zones/{abbr_lower}"
    resp = requests.get(url, headers=HEADERS, timeout=10)
    if resp.status_code != 200:
        raise ValueError(f"Unknown timezone abbreviation: {tz_abbr}")

    soup = BeautifulSoup(resp.text, "html.parser")
    page_text = soup.get_text(" ", strip=True)

    # Look for "UTC Offset: UTC ±N" pattern
    offset_match = re.search(
        r'UTC\s+Offset\s*:\s*UTC\s*([+-])\s*(\d{1,2})(?::(\d{2}))?',
        page_text
    )
    if offset_match:
        sign = 1 if offset_match.group(1) == '+' else -1
        hours = int(offset_match.group(2))
        minutes = int(offset_match.group(3)) if offset_match.group(3) else 0
        return sign * (hours + minutes / 60.0)

    # Fallback: look for "UTC-7" or "UTC+3" anywhere on page
    fallback = re.search(r'UTC\s*([+-])\s*(\d{1,2})(?::(\d{2}))?', page_text)
    if fallback:
        sign = 1 if fallback.group(1) == '+' else -1
        hours = int(fallback.group(2))
        minutes = int(fallback.group(3)) if fallback.group(3) else 0
        return sign * (hours + minutes / 60.0)

    # Check for "UTC±0" or zero-offset synonyms
    if re.search(r'UTC\s*\+?\s*0\b', page_text):
        return 0.0

    raise ValueError(f"Could not find UTC offset for: {tz_abbr}")


# ─────────────────────────────────────────────────────────────────────────────
#  WEB SCRAPING — timezone offset from location (city name)
# ─────────────────────────────────────────────────────────────────────────────
def scrape_location_offset(location: str) -> float:
    """
    Search timeanddate.com for a city name, find its timezone abbreviation,
    then scrape the offset for that abbreviation.
    Returns offset as a float.
    Raises ValueError on failure.
    """
    loc_clean = location.strip()

    # Step 1: Search on timeanddate.com
    search_url = (
        "https://www.timeanddate.com/worldclock/results.html"
        f"?query={requests.utils.quote(loc_clean)}"
    )
    resp = requests.get(search_url, headers=HEADERS, timeout=10)
    if resp.status_code != 200:
        raise ValueError(f"Could not search for location: {loc_clean}")

    soup = BeautifulSoup(resp.text, "html.parser")

    # Excluded path substrings (generic/utility pages)
    EXCLUDED = {
        "results.html", "converter", "meeting", "fixedform",
        "personal", "full.html", "sunearth", "distance",
        "fullscreen", "clockchange", "search.html", "timezone/utc",
    }

    # Find city link: matches /worldclock/<country>/<city>
    link = None
    city_pattern = re.compile(r'^/worldclock/[a-z0-9_-]+/[a-z0-9_-]+$', re.IGNORECASE)
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if city_pattern.match(href) and not any(ex in href for ex in EXCLUDED):
            link = href
            break

    if not link:
        raise ValueError(f"Location not found: {loc_clean}")

    # Step 2: Visit the city page → find timezone abbreviation
    city_url = f"https://www.timeanddate.com{link}"
    resp2 = requests.get(city_url, headers=HEADERS, timeout=10)
    if resp2.status_code != 200:
        raise ValueError(f"Could not load city page for: {loc_clean}")

    soup2 = BeautifulSoup(resp2.text, "html.parser")

    # Look for link to /time/zones/<abbr>
    tz_link_pattern = re.compile(r'^/time/zones/([a-z]+)$')
    for a_tag in soup2.find_all("a", href=True):
        m = tz_link_pattern.match(a_tag["href"])
        if m:
            tz_abbr = m.group(1)
            return scrape_tz_offset(tz_abbr)

    # Fallback: look for UTC offset directly on the page
    page_text = soup2.get_text(" ", strip=True)
    utc_match = re.search(r'UTC\s*([+-])\s*(\d{1,2})(?::(\d{2}))?', page_text)
    if utc_match:
        sign = 1 if utc_match.group(1) == '+' else -1
        hours = int(utc_match.group(2))
        minutes = int(utc_match.group(3)) if utc_match.group(3) else 0
        return sign * (hours + minutes / 60.0)

    raise ValueError(f"Could not determine timezone for: {loc_clean}")


# ─────────────────────────────────────────────────────────────────────────────
#  INPUT PARSING
# ─────────────────────────────────────────────────────────────────────────────
def parse_time_input(text: str):
    """
    Parse an input string like '6 am PT', '4:30 pm EST', '16:00 UTC+3'.
    Returns (hours_24, minutes, timezone_or_location_str).
    Raises ValueError on bad input.
    """
    text = text.strip()
    if not text:
        raise ValueError("Input is empty")

    # ---- Pattern 1: "4 pm PT", "6 am EST", "11 PM UTC+3"
    m = re.match(
        r'^(\d{1,2})\s*(am|pm)\s+(.+)$',
        text, re.IGNORECASE
    )
    if m:
        hour = int(m.group(1))
        ampm = m.group(2).lower()
        tz_str = m.group(3).strip()
        if hour < 1 or hour > 12:
            raise ValueError("Hour must be between 1 and 12 when using am/pm")
        if ampm == "am":
            hour_24 = 0 if hour == 12 else hour
        else:
            hour_24 = 12 if hour == 12 else hour + 12
        return hour_24, 0, tz_str

    # ---- Pattern 2: "4:30 pm PT"
    m = re.match(
        r'^(\d{1,2}):(\d{2})\s*(am|pm)\s+(.+)$',
        text, re.IGNORECASE
    )
    if m:
        hour = int(m.group(1))
        minute = int(m.group(2))
        ampm = m.group(3).lower()
        tz_str = m.group(4).strip()
        if hour < 1 or hour > 12:
            raise ValueError("Hour must be between 1 and 12 when using am/pm")
        if minute < 0 or minute > 59:
            raise ValueError("Minutes must be between 0 and 59")
        if ampm == "am":
            hour_24 = 0 if hour == 12 else hour
        else:
            hour_24 = 12 if hour == 12 else hour + 12
        return hour_24, minute, tz_str

    # ---- Pattern 3: "16:00 UTC+3", "0:00 GMT"
    m = re.match(
        r'^(\d{1,2}):(\d{2})\s+(.+)$',
        text, re.IGNORECASE
    )
    if m:
        hour_24 = int(m.group(1))
        minute = int(m.group(2))
        tz_str = m.group(3).strip()
        if hour_24 < 0 or hour_24 > 23:
            raise ValueError("Hour must be between 0 and 23 in 24-hour format")
        if minute < 0 or minute > 59:
            raise ValueError("Minutes must be between 0 and 59")
        return hour_24, minute, tz_str

    # ---- Pattern 4: "16 UTC", "4 EST" (no colon, no am/pm)
    m = re.match(
        r'^(\d{1,2})\s+(.+)$',
        text, re.IGNORECASE
    )
    if m:
        hour_24 = int(m.group(1))
        tz_str = m.group(2).strip()
        if hour_24 < 0 or hour_24 > 23:
            raise ValueError("Hour must be between 0 and 23 in 24-hour format")
        return hour_24, 0, tz_str

    raise ValueError("ERROR: Unrecognized input format")


# ─────────────────────────────────────────────────────────────────────────────
#  RESOLVE TIMEZONE STRING → UTC OFFSET (scraping)
# ─────────────────────────────────────────────────────────────────────────────
def resolve_offset(tz_or_location: str) -> float:
    """
    Given a string that might be a timezone abbreviation (PT, EST, UTC+3)
    or a location name (İstanbul, Tokyo), return the UTC offset as a float.
    """
    text = tz_or_location.strip()

    # First try as timezone abbreviation
    try:
        return scrape_tz_offset(text)
    except ValueError:
        pass

    # Then try as location
    return scrape_location_offset(text)


# ─────────────────────────────────────────────────────────────────────────────
#  CONVERSION LOGIC (arithmetic)
# ─────────────────────────────────────────────────────────────────────────────
def convert_time(input_h: int, input_m: int, from_offset: float, to_offset: float):
    """
    Convert a time (hours, minutes) from one UTC offset to another.
    Returns (converted_hours_24, converted_minutes, day_shift).
      day_shift: 0 = same day, +1 = next day, -1 = previous day
    """
    # Convert input time to total minutes from midnight
    total_minutes = input_h * 60 + input_m

    # Convert to UTC (subtract source offset)
    offset_diff_minutes = (to_offset - from_offset) * 60

    # Apply offset difference
    result_minutes = total_minutes + offset_diff_minutes

    # Handle day wrap
    day_shift = 0
    if result_minutes >= 24 * 60:
        day_shift = 1
        result_minutes -= 24 * 60
    elif result_minutes < 0:
        day_shift = -1
        result_minutes += 24 * 60

    result_h = int(result_minutes // 60)
    result_m = int(result_minutes % 60)

    return result_h, result_m, day_shift


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN CONVERSION FUNCTION
# ─────────────────────────────────────────────────────────────────────────────
def do_conversion(input_text: str, output_target: str) -> str:
    """
    Main entry point:  parse input, resolve offsets, convert, format output.
    Returns a string result to display.
    """
    # Parse input
    try:
        in_h, in_m, in_tz = parse_time_input(input_text)
    except ValueError as e:
        return f"ERROR: {e}"

    # Resolve input timezone offset
    try:
        from_offset = resolve_offset(in_tz)
    except ValueError as e:
        return f"ERROR: {e}"

    # Resolve output timezone / location offset
    output_target = output_target.strip()
    if not output_target:
        # No output target → just show the parsed input in 24-hour format
        return f"{in_h:02d}:{in_m:02d}"

    try:
        to_offset = resolve_offset(output_target)
    except ValueError as e:
        return f"ERROR: {e}"

    # Arithmetic conversion
    out_h, out_m, day_shift = convert_time(in_h, in_m, from_offset, to_offset)

    # Format output
    result = f"{out_h}:{out_m:02d}"

    if day_shift == 1:
        result += " — Next Day"
    elif day_shift == -1:
        result += " — Previous Day"

    return result


# ─────────────────────────────────────────────────────────────────────────────
#  GUI
# ─────────────────────────────────────────────────────────────────────────────
class TimezoneConverterApp:
    """
    1000×500 GUI with:
      - Left 450×500   → input area (time input + target output field)
      - Center 100×500  → Conversion button
      - Right 450×500   → result display
    """

    # Colour palette
    BG        = "#0f1117"
    PANEL_BG  = "#1a1d27"
    ACCENT    = "#6c63ff"
    ACCENT_HI = "#8b83ff"
    TEXT      = "#e8e6f0"
    TEXT_DIM  = "#8a8899"
    ERROR_CLR = "#ff6b6b"
    BORDER    = "#2d2f3d"

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Timezone Converter")
        self.root.geometry("1000x500")
        self.root.resizable(False, False)
        self.root.configure(bg=self.BG)

        # ─── Fonts ───
        self.font_title  = tkfont.Font(family="Helvetica Neue", size=16, weight="bold")
        self.font_label  = tkfont.Font(family="Helvetica Neue", size=11)
        self.font_entry  = tkfont.Font(family="Menlo", size=14)
        self.font_button = tkfont.Font(family="Helvetica Neue", size=13, weight="bold")
        self.font_result = tkfont.Font(family="Menlo", size=28, weight="bold")
        self.font_hint   = tkfont.Font(family="Helvetica Neue", size=9)

        self._build_ui()

    # ── UI construction ─────────────────────────────────────────────────────
    def _build_ui(self):
        # Left panel (450×500)
        left = tk.Frame(self.root, width=450, height=500, bg=self.PANEL_BG,
                        highlightbackground=self.BORDER, highlightthickness=1)
        left.pack(side=tk.LEFT, fill=tk.BOTH)
        left.pack_propagate(False)

        # Title for left panel
        tk.Label(left, text="⏰  INPUT", font=self.font_title,
                 fg=self.ACCENT, bg=self.PANEL_BG, anchor="w").pack(
            padx=30, pady=(40, 10), fill=tk.X)

        # Separator
        sep1 = tk.Frame(left, height=2, bg=self.ACCENT)
        sep1.pack(fill=tk.X, padx=30, pady=(0, 25))

        # Time input
        tk.Label(left, text="Time & Timezone", font=self.font_label,
                 fg=self.TEXT, bg=self.PANEL_BG, anchor="w").pack(
            padx=30, fill=tk.X)
        tk.Label(left, text='e.g.  "4 pm PT"  •  "16:00 UTC+3"  •  "6 am EST"',
                 font=self.font_hint, fg=self.TEXT_DIM, bg=self.PANEL_BG,
                 anchor="w").pack(padx=30, fill=tk.X, pady=(0, 6))

        self.entry_input = tk.Entry(left, font=self.font_entry,
                                    bg="#12141e", fg=self.TEXT,
                                    insertbackground=self.ACCENT,
                                    relief=tk.FLAT, bd=0,
                                    highlightbackground=self.BORDER,
                                    highlightcolor=self.ACCENT,
                                    highlightthickness=2)
        self.entry_input.pack(padx=30, fill=tk.X, ipady=10)

        # Spacer
        tk.Frame(left, height=30, bg=self.PANEL_BG).pack()

        # Target timezone / location
        tk.Label(left, text="Target Timezone / Location", font=self.font_label,
                 fg=self.TEXT, bg=self.PANEL_BG, anchor="w").pack(
            padx=30, fill=tk.X)
        tk.Label(left,
                 text='e.g.  "İstanbul"  •  "EST"  •  "UTC+5"  •  leave empty for 24h',
                 font=self.font_hint, fg=self.TEXT_DIM, bg=self.PANEL_BG,
                 anchor="w").pack(padx=30, fill=tk.X, pady=(0, 6))

        self.entry_output = tk.Entry(left, font=self.font_entry,
                                     bg="#12141e", fg=self.TEXT,
                                     insertbackground=self.ACCENT,
                                     relief=tk.FLAT, bd=0,
                                     highlightbackground=self.BORDER,
                                     highlightcolor=self.ACCENT,
                                     highlightthickness=2)
        self.entry_output.pack(padx=30, fill=tk.X, ipady=10)

        # Hint at bottom of left panel
        tk.Label(left,
                 text="Press Enter or click the button to convert →",
                 font=self.font_hint, fg=self.TEXT_DIM, bg=self.PANEL_BG).pack(
            side=tk.BOTTOM, pady=20)

        # Center panel (100×500) — Conversion button
        center = tk.Frame(self.root, width=100, height=500, bg=self.BG)
        center.pack(side=tk.LEFT, fill=tk.Y)
        center.pack_propagate(False)

        # Vertical centering wrapper
        btn_wrap = tk.Frame(center, bg=self.BG)
        btn_wrap.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.btn = tk.Button(
            btn_wrap, text="⟶", font=self.font_button,
            bg=self.ACCENT, fg="white", activebackground=self.ACCENT_HI,
            activeforeground="white", relief=tk.FLAT, bd=0,
            cursor="hand2", width=4, height=2,
            command=self._on_convert
        )
        self.btn.pack()

        tk.Label(btn_wrap, text="Convert", font=self.font_hint,
                 fg=self.TEXT_DIM, bg=self.BG).pack(pady=(6, 0))

        # Right panel (450×500) — output area
        right = tk.Frame(self.root, width=450, height=500, bg=self.PANEL_BG,
                         highlightbackground=self.BORDER, highlightthickness=1)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        right.pack_propagate(False)

        tk.Label(right, text="📍  OUTPUT", font=self.font_title,
                 fg=self.ACCENT, bg=self.PANEL_BG, anchor="w").pack(
            padx=30, pady=(40, 10), fill=tk.X)

        sep2 = tk.Frame(right, height=2, bg=self.ACCENT)
        sep2.pack(fill=tk.X, padx=30, pady=(0, 25))

        # Result display area (centred)
        result_frame = tk.Frame(right, bg=self.PANEL_BG)
        result_frame.pack(expand=True, fill=tk.BOTH)

        self.lbl_result = tk.Label(
            result_frame, text="—", font=self.font_result,
            fg=self.TEXT, bg=self.PANEL_BG, wraplength=380, justify=tk.CENTER
        )
        self.lbl_result.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.lbl_status = tk.Label(
            result_frame, text="Waiting for input…",
            font=self.font_label, fg=self.TEXT_DIM, bg=self.PANEL_BG
        )
        self.lbl_status.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

        # Bind Enter key
        self.root.bind("<Return>", lambda e: self._on_convert())

    # ── Conversion handler ──────────────────────────────────────────────────
    def _on_convert(self):
        input_text = self.entry_input.get().strip()
        output_target = self.entry_output.get().strip()

        if not input_text:
            self._show_error("Please enter a time in the input field")
            return

        # Show loading state
        self.lbl_result.config(text="…", fg=self.TEXT_DIM)
        self.lbl_status.config(text="Fetching timezone data…", fg=self.ACCENT)
        self.btn.config(state=tk.DISABLED)
        self.root.update_idletasks()

        # Run conversion in background thread so GUI stays responsive
        def _worker():
            result = do_conversion(input_text, output_target)
            self.root.after(0, lambda: self._display_result(result))

        threading.Thread(target=_worker, daemon=True).start()

    def _display_result(self, result: str):
        self.btn.config(state=tk.NORMAL)
        if result.startswith("ERROR"):
            self._show_error(result)
        else:
            self.lbl_result.config(text=result, fg=self.TEXT)
            self.lbl_status.config(text="Conversion complete ✓", fg="#4ade80")

    def _show_error(self, msg: str):
        self.lbl_result.config(text="✗", fg=self.ERROR_CLR)
        self.lbl_status.config(text=msg, fg=self.ERROR_CLR)

    # ── Run ─────────────────────────────────────────────────────────────────
    def run(self):
        self.root.mainloop()


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = TimezoneConverterApp()
    app.run()
