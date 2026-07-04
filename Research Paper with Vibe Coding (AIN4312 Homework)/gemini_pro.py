import tkinter as tk
import requests
import re
import urllib.parse

def parse_offset_string(offset_str):
    """Converts an offset string like '+3', '-08:00' into a float (e.g., 3.0, -8.0)."""
    offset_str = offset_str.replace(" ", "")
    if ':' in offset_str:
        parts = offset_str.split(':')
        sign = -1 if parts[0].startswith('-') else 1
        return float(parts[0]) + sign * (float(parts[1]) / 60)
    else:
        return float(offset_str)

def scrape_offset(tz_code):
    """Scrapes search engines to find the UTC/GMT offset for a specific timezone code."""
    # Check if the code itself is a direct offset format (e.g., UTC+3)
    direct_match = re.search(r'(?:UTC|GMT)\s*([+-]\s*\d{1,2}(?::\d{2})?)', tz_code, re.IGNORECASE)
    if direct_match:
        return parse_offset_string(direct_match.group(1))

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    urls = [
        f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(tz_code + ' current UTC offset')}",
        f"https://www.google.com/search?q={urllib.parse.quote(tz_code + ' current UTC offset')}"
    ]
    
    for url in urls:
        try:
            resp = requests.get(url, headers=headers, timeout=5)
            # Find patterns like "UTC+3", "GMT -8:00", etc.
            match = re.search(r'(?:UTC|GMT)\s*([+-]\s*\d{1,2}(?::\d{2})?)', resp.text, re.IGNORECASE)
            if match:
                return parse_offset_string(match.group(1))
        except Exception:
            continue
            
    raise ValueError(f"Could not scrape offset for {tz_code}")

def get_tz_and_offset(query):
    """
    Determines if query is a location or timezone. 
    If location, it first scrapes the timezone code, then the offset.
    """
    # If the string is a standard short abbreviation or offset, treat as timezone
    if re.match(r'^(?:UTC|GMT)?[+-]\d{1,2}(?::\d{2})?$', query, re.IGNORECASE) or (len(query) <= 5 and query.isalpha()):
        return scrape_offset(query)
    
    # Otherwise, assume it's a location. Step 1: Scrape timezone code.
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query + ' time zone abbreviation')}"
    try:
        resp = requests.get(url, headers=headers, timeout=5)
        # Search for standard time zone abbreviations or UTC+X codes
        tz_match = re.search(r'\b([A-Z]{2,5}|(?:UTC|GMT)[+-]\d{1,2})\b', resp.text)
        if tz_match:
            tz_code = tz_match.group(1)
        else:
            tz_code = query # Fallback to searching the query itself if code isn't explicitly found
    except Exception:
        tz_code = query
        
    # Step 2: Find offset for the found time zone
    return scrape_offset(tz_code)

def perform_conversion():
    try:
        input_content = input_text.get("1.0", "end-1c").strip()
        output_content = output_text.get("1.0", "end-1c").strip()
        
        if not input_content or not output_content:
            raise ValueError("Missing input or output text")
        
        # Regex to extract Time (Hours:Minutes), AM/PM, and the Timezone from input area
        # E.g., matches "6 am PT", "16:00 GMT+3", "4 pm EST"
        match = re.match(r'^\s*(\d{1,2})(?::(\d{2}))?\s*(am|pm|a\.m\.|p\.m\.)?\s+(.+)$', input_content, re.IGNORECASE)
        if not match:
            raise ValueError("Invalid input format")
            
        hour_str, min_str, ampm, input_tz = match.groups()
        
        # --- Time Arithmetic ---
        hour = int(hour_str)
        minute = int(min_str) if min_str else 0
        
        if ampm:
            ampm = ampm.lower()
            if 'p' in ampm and hour < 12:
                hour += 12
            elif 'a' in ampm and hour == 12:
                hour = 0
                
        input_time_hours = hour + minute / 60.0
        
        # Scrape required offsets
        input_offset = get_tz_and_offset(input_tz)
        target_offset = get_tz_and_offset(output_content)
        
        # Convert to UTC, then to Target Time
        utc_time = input_time_hours - input_offset
        target_time = utc_time + target_offset
        
        # Handle day shifts
        day_shift = 0
        while target_time < 0:
            target_time += 24
            day_shift -= 1
        while target_time >= 24:
            target_time -= 24
            day_shift += 1
            
        # Format the final output
        out_hour = int(target_time)
        out_min = int(round((target_time - out_hour) * 60))
        if out_min == 60:
            out_min = 0
            out_hour += 1
            if out_hour == 24:
                out_hour = 0
                day_shift += 1
                
        # Format explicitly in 24-hour time 
        result = f"{out_hour}:{out_min:02d}"
        
        if day_shift == 1:
            result += " — Next Day"
        elif day_shift > 1:
            result += f" — Next Day (+{day_shift})"
        elif day_shift == -1:
            result += " — Previous Day"
        elif day_shift < -1:
            result += f" — Previous Day ({day_shift})"
            
        # Update output area
        output_text.delete("1.0", tk.END)
        output_text.insert("1.0", result)
        
    except Exception as e:
        # If unrelated text is typed, scraping fails, or arithmetic crashes, return ERROR
        output_text.delete("1.0", tk.END)
        output_text.insert("1.0", "ERROR")

# --- Interface Setup ---
root = tk.Tk()
root.title("Scraping Timezone Converter")
root.geometry("1000x500")
root.resizable(False, False)

# Left Half: Input Area (450x500)
input_text = tk.Text(root, font=("Arial", 16), bg="#f4f4f4", wrap=tk.WORD)
input_text.place(x=0, y=0, width=450, height=500)

# Middle: Conversion Button (100x500)
btn = tk.Button(root, text="Conversion\n➡️", font=("Arial", 12, "bold"), bg="#d1e7dd", command=perform_conversion)
btn.place(x=450, y=0, width=100, height=500)

# Right Half: Output Area (450x500)
output_text = tk.Text(root, font=("Arial", 16), bg="#e2e3e5", wrap=tk.WORD)
output_text.place(x=550, y=0, width=450, height=500)

# Add placeholder instructions
input_text.insert("1.0", "4 pm PT")
output_text.insert("1.0", "İstanbul")

root.mainloop()