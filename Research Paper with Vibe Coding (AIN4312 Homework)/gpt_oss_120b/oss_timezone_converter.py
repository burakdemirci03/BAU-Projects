#!/usr/bin/env python3
"""Timezone Conversion GUI

This script provides a simple 1000x500 Tkinter GUI with three sections:
- Left: Input text area where the user types a time string (e.g. "6 am PT").
- Middle: "Convert" button.
- Right: Output text area where the converted time is displayed.

The conversion works by:
1. Parsing the input time and source timezone/abbreviation.
2. Determining the UTC offset of the source timezone (via a small built‑in map or web‑scraping).
3. Determining the UTC offset of the target timezone or location (web‑scraping `timeanddate.com`).
4. Performing arithmetic to convert the time.
5. Formatting the result in 24‑hour format and appending "— Next Day" or "— Previous Day" when appropriate.

If the input cannot be parsed or the target cannot be resolved, the output area shows "ERROR".
"""

import re
import datetime
import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def parse_time_input(text: str):
    """Parse strings like "6 am PT" or "16:30 GMT+2".
    Returns a tuple (hour_24, minute, src_tz) or raises ValueError.
    """
    text = text.strip()
    # Regex for "hh:mm" optional am/pm and timezone
    m = re.match(r"(?i)^(\d{1,2})(?::(\d{2}))?\s*(am|pm)?\s+([A-Za-z_/+\-]+)$", text)
    if not m:
        raise ValueError("Unable to parse input")
    hour = int(m.group(1))
    minute = int(m.group(2)) if m.group(2) else 0
    ampm = m.group(3)
    tz = m.group(4).upper()
    if ampm:
        ampm = ampm.lower()
        if ampm == "pm" and hour != 12:
            hour += 12
        if ampm == "am" and hour == 12:
            hour = 0
    else:
        # Assume 24‑hour format already
        if hour == 24:
            hour = 0
    if not (0 <= hour < 24 and 0 <= minute < 60):
        raise ValueError("Invalid hour/minute values")
    return hour, minute, tz

# Small static map for common abbreviations (fallback if scraping fails)
ABBR_OFFSET_MAP = {
    "UTC": 0,
    "GMT": 0,
    "PT": -8,   # Pacific Time (standard)
    "PST": -8,
    "PDT": -7,
    "ET": -5,
    "EST": -5,
    "EDT": -4,
    "CT": -6,
    "CST": -6,
    "CDT": -5,
    "BST": 1,
    "CET": 1,
    "CEST": 2,
    "IST": 5.5,
    "JST": 9,
    "AEST": 10,
    "AEDT": 11,
}

def get_offset_from_abbr(abbr: str):
    """Return UTC offset in hours for a known abbreviation.
    If not known, attempt to scrape `timeanddate.com`.
    """
    abbr = abbr.upper()
    if abbr in ABBR_OFFSET_MAP:
        return ABBR_OFFSET_MAP[abbr]
    # Try web‑scraping – we look up the abbreviation as a timezone name
    try:
        url = f"https://www.timeanddate.com/time/zones/" + abbr.lower()
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        # The page contains a table where the offset appears like "UTC+02:00"
        txt = soup.find(string=re.compile(r"UTC[+-]"))
        if txt:
            m = re.search(r"UTC([+-]\d{1,2})(?::(\d{2}))?", txt)
            if m:
                hrs = int(m.group(1))
                mins = int(m.group(2)) if m.group(2) else 0
                return hrs + mins / 60.0
    except Exception:
        pass
    raise ValueError(f"Unknown timezone abbreviation: {abbr}")

def get_offset_for_location(location: str):
    """Scrape timeanddate.com to obtain the current UTC offset for a city.
    Returns offset in hours (can be fractional).
    """
    try:
        query = location.replace(' ', '+')
        search_url = f"https://www.timeanddate.com/worldclock/search.html?query={query}"
        resp = requests.get(search_url, timeout=5)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        # The first result link leads to a page like /worldclock/turkey/istanbul
        first_link = soup.select_one('table.zebra.tb-wc tr td a')
        if not first_link:
            raise ValueError("Location not found")
        city_url = "https://www.timeanddate.com" + first_link['href']
        city_resp = requests.get(city_url, timeout=5)
        city_resp.raise_for_status()
        city_soup = BeautifulSoup(city_resp.text, "html.parser")
        # Look for the UTC offset string, e.g., "UTC+03:00"
        offset_span = city_soup.find(string=re.compile(r"UTC[+-]"))
        if not offset_span:
            raise ValueError("Offset not found on city page")
        m = re.search(r"UTC([+-]\d{1,2})(?::(\d{2}))?", offset_span)
        if not m:
            raise ValueError("Unable to parse offset")
        hrs = int(m.group(1))
        mins = int(m.group(2)) if m.group(2) else 0
        return hrs + mins / 60.0
    except Exception as e:
        raise ValueError(f"Failed to get offset for location '{location}': {e}")

def convert_time(src_hour, src_minute, src_offset, tgt_offset):
    """Convert time from src_offset to tgt_offset.
    Returns (hour24, minute, day_delta) where day_delta is -1, 0, or +1.
    """
    # Build a datetime on an arbitrary date (e.g., 2000‑01‑01)
    src_dt = datetime.datetime(2000, 1, 1, src_hour, src_minute)
    # Convert to UTC then to target
    utc_dt = src_dt - datetime.timedelta(hours=src_offset)
    tgt_dt = utc_dt + datetime.timedelta(hours=tgt_offset)
    day_delta = (tgt_dt.date() - src_dt.date()).days
    return tgt_dt.hour, tgt_dt.minute, day_delta

# ---------------------------------------------------------------------------
# GUI implementation
# ---------------------------------------------------------------------------

def on_convert():
    inp = input_text.get("1.0", tk.END).strip()
    out_loc = output_loc_entry.get().strip()
    if not inp:
        messagebox.showwarning("Input missing", "Please enter a time string.")
        return
    try:
        src_hour, src_minute, src_tz = parse_time_input(inp)
        src_offset = get_offset_from_abbr(src_tz)
        # Determine target offset
        if out_loc:
            # If the user gave a location, treat it as a city name
            tgt_offset = get_offset_for_location(out_loc)
        else:
            # No explicit target – use UTC as default
            tgt_offset = 0
        tgt_hour, tgt_minute, day_delta = convert_time(src_hour, src_minute, src_offset, tgt_offset)
        result = f"{tgt_hour:02d}:{tgt_minute:02d}"
        if day_delta == 1:
            result += " — Next Day"
        elif day_delta == -1:
            result += " — Previous Day"
        output_text.configure(state="normal")
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result)
        output_text.configure(state="disabled")
    except Exception as e:
        output_text.configure(state="normal")
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "ERROR")
        output_text.configure(state="disabled")
        print(f"Conversion error: {e}")

root = tk.Tk()
root.title("Timezone Converter")
root.geometry("1000x500")
root.resizable(False, False)

# Left panel – input
left_frame = tk.Frame(root, width=450, height=500)
left_frame.pack(side="left", fill="both", expand=False)
left_frame.pack_propagate(False)
input_label = tk.Label(left_frame, text="Input (e.g., '6 am PT'):")
input_label.pack(pady=5)
input_text = scrolledtext.ScrolledText(left_frame, wrap=tk.WORD, height=20)
input_text.pack(fill="both", expand=True, padx=5, pady=5)

# Middle panel – button and optional target location entry
mid_frame = tk.Frame(root, width=100, height=500)
mid_frame.pack(side="left", fill="y")
mid_frame.pack_propagate(False)
convert_btn = tk.Button(mid_frame, text="Convert", command=on_convert, width=12, height=2)
convert_btn.pack(pady=20)

# Target location entry (optional)
loc_label = tk.Label(mid_frame, text="Target location (optional):")
loc_label.pack(pady=5)
output_loc_entry = tk.Entry(mid_frame)
output_loc_entry.pack(pady=5)

# Right panel – output
right_frame = tk.Frame(root, width=450, height=500)
right_frame.pack(side="right", fill="both", expand=False)
right_frame.pack_propagate(False)
output_label = tk.Label(right_frame, text="Output:")
output_label.pack(pady=5)
output_text = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, height=20, state="disabled")
output_text.pack(fill="both", expand=True, padx=5, pady=5)

root.mainloop()
