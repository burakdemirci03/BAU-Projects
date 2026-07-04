import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import re

def scrape_offset(query):
    # Direct match for UTC/GMT offsets
    direct = re.search(r'(?:UTC|GMT)\s*([+-]\d{1,2}(?::\d{2})?)', query, re.IGNORECASE)
    if direct:
        return direct.group(1)
        
    query_for_offset = query
    
    # If not a standard timezone abbreviation (lengthy text, lowercase, etc.) -> assume location
    if len(query) > 5 or not query.isalpha() or not query.isupper():
        # "First find the time zone code."
        # We can find the time zone offset of a location using wttr.in or Google search.
        try:
            res = requests.get(f"https://wttr.in/{query}?format=%Z", timeout=5)
            if res.status_code == 200 and "Unknown" not in res.text:
                tz_code = res.text.strip()
                query_for_offset = tz_code
        except Exception:
            pass

    # Determine offset of time zone
    try:
        if re.match(r'^[+-]\d{4}$', query_for_offset):
            sign = query_for_offset[0]
            h = int(query_for_offset[1:3])
            m = int(query_for_offset[3:5])
            if m == 0: return f"{sign}{h}"
            return f"{sign}{h}:{m:02d}"
            
        headers = {"User-Agent": "Mozilla/5.0"}
        # Scrape DuckDuckGo
        res = requests.post("https://html.duckduckgo.com/html/", data={"q": f"UTC offset of {query_for_offset}"}, headers=headers, timeout=5)
        text = BeautifulSoup(res.text, "html.parser").get_text()
        match = re.search(r'(?:UTC|GMT)\s*([+-]\d{1,2}(?::\d{2})?)', text, re.IGNORECASE)
        if match:
            return match.group(1)
            
        # Fallback Google
        url = f"https://www.google.com/search?q=UTC+offset+of+{query_for_offset}"
        res2 = requests.get(url, headers=headers, timeout=5)
        text2 = BeautifulSoup(res2.text, "html.parser").get_text()
        match2 = re.search(r'(?:UTC|GMT)\s*([+-]\d{1,2}(?::\d{2})?)', text2, re.IGNORECASE)
        if match2:
            return match2.group(1)
    except Exception:
        pass
        
    return None

def parse_time(time_str):
    time_str = time_str.strip().lower()
    is_pm = "pm" in time_str
    is_am = "am" in time_str
    
    time_str = time_str.replace("am", "").replace("pm", "").strip()
    parts = time_str.split(":")
    hours = int(parts[0])
    mins = int(parts[1]) if len(parts) > 1 else 0
    
    if is_pm and hours < 12:
        hours += 12
    if is_am and hours == 12:
        hours = 0
        
    return hours + (mins / 60.0)
    
def parse_offset(offset_str):
    if not offset_str: return 0
    sign = -1 if offset_str.startswith("-") else 1
    offset_str = offset_str.replace("+", "").replace("-", "")
    parts = offset_str.split(":")
    hours = int(parts[0])
    mins = int(parts[1]) if len(parts) > 1 else 0
    return sign * (hours + (mins / 60.0))

class TimezoneConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Timezone Converter")
        self.geometry("1000x500")
        self.resizable(False, False)
        
        self.create_widgets()
        
    def create_widgets(self):
        # LEFT PANE (450x500)
        left_frame = tk.Frame(self, width=450, height=500, bg="#2b2b2b")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        left_frame.pack_propagate(False)

        # MIDDLE PANE (100x500)
        middle_frame = tk.Frame(self, width=100, height=500, bg="#1a1a1a")
        middle_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        middle_frame.pack_propagate(False)

        # RIGHT PANE (450x500)
        right_frame = tk.Frame(self, width=450, height=500, bg="#2b2b2b")
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        right_frame.pack_propagate(False)

        # Content in Left Pane
        tk.Label(left_frame, text="Input Time", font=("Arial", 16, "bold"), bg="#2b2b2b", fg="white").pack(pady=(120, 10))
        tk.Label(left_frame, text="(e.g., '6 am PT' or '16:00 GMT+3')", font=("Arial", 10), bg="#2b2b2b", fg="lightgray").pack(pady=(0, 10))
        self.source_entry = tk.Entry(left_frame, font=("Arial", 16), width=20, justify="center")
        self.source_entry.pack(pady=5)
        
        tk.Label(left_frame, text="Output Timezone or Location", font=("Arial", 16, "bold"), bg="#2b2b2b", fg="white").pack(pady=(40, 10))
        tk.Label(left_frame, text="(e.g., 'İstanbul' or 'UTC-4')", font=("Arial", 10), bg="#2b2b2b", fg="lightgray").pack(pady=(0, 10))
        self.target_entry = tk.Entry(left_frame, font=("Arial", 16), width=20, justify="center")
        self.target_entry.pack(pady=5)

        # Content in Middle Pane
        conv_btn = tk.Button(middle_frame, text="Conversion", font=("Arial", 12, "bold"), bg="#4CAF50", fg="black", command=self.perform_conversion)
        conv_btn.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=90, height=50)

        # Content in Right Pane
        tk.Label(right_frame, text="Converted Time", font=("Arial", 16, "bold"), bg="#2b2b2b", fg="white").pack(pady=(180, 20))
        self.output_label = tk.Label(right_frame, text="-", font=("Arial", 28, "bold"), bg="#2b2b2b", fg="#4CAF50")
        self.output_label.pack(pady=10)

    def perform_conversion(self):
        source_input = self.source_entry.get().strip()
        target_input = self.target_entry.get().strip()

        if not source_input or not target_input:
            self.output_label.config(text="ERROR", fg="red")
            return

        # Parse output target
        target_str = target_input
        
        # Parse source input
        match = re.search(r'^(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)\s+(.+)$', source_input, re.IGNORECASE)
        if not match:
            self.output_label.config(text="ERROR", fg="red")
            return
            
        time_str = match.group(1).strip()
        source_tz = match.group(2).strip()
        
        try:
            # 1. Scraping and offset resolution
            self.output_label.config(text="Scraping...", fg="yellow")
            self.update_idletasks()
            
            source_offset_str = scrape_offset(source_tz)
            target_offset_str = scrape_offset(target_str)
            
            if not source_offset_str or not target_offset_str:
                self.output_label.config(text="ERROR", fg="red")
                return

            # 2. Arithmetic conversion
            source_off = parse_offset(source_offset_str)
            target_off = parse_offset(target_offset_str)
            diff = target_off - source_off
            
            parsed_time = parse_time(time_str)
            new_time = parsed_time + diff
            
            day_shift_str = ""
            if new_time >= 24:
                new_time -= 24
                day_shift_str = " — Next Day"
            elif new_time < 0:
                new_time += 24
                day_shift_str = " — Previous Day"
                
            new_hours = int(new_time)
            new_mins = int(round((new_time - new_hours) * 60))
            if new_mins == 60:
                new_mins = 0
                new_hours += 1
                if new_hours == 24:
                    new_hours = 0
                    if not day_shift_str: day_shift_str = " — Next Day"
                    
            result = f"{new_hours}:{new_mins:02d}{day_shift_str}"
            self.output_label.config(text=result, fg="#4CAF50")
            
        except Exception:
            self.output_label.config(text="ERROR", fg="red")

if __name__ == "__main__":
    app = TimezoneConverterApp()
    app.mainloop()
