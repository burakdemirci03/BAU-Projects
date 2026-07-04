import tkinter as tk
from tkinter import StringVar, messagebox
from datetime import datetime, timedelta
import pytz
import re
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import threading

class TimezoneConverter:
    def __init__(self, master):
        self.master = master
        self.master.title("Timezone Converter")
        self.master.geometry("1000x500")
        self.master.resizable(False, False)
        
        # Configure style
        self.master.configure(bg="#f0f0f0")
        
        # Create main frame
        main_frame = tk.Frame(master, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Input area (450x500)
        left_frame = tk.Frame(main_frame, width=450, height=500, bg="white", relief=tk.SUNKEN, bd=2)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Input labels and fields
        tk.Label(left_frame, text="Timezone Converter", font=("Arial", 14, "bold"), bg="white").pack(pady=10)
        
        tk.Label(left_frame, text="Time & Timezone (or Location):", font=("Arial", 10), bg="white", justify=tk.LEFT).pack(anchor=tk.W, padx=15, pady=(10, 5))
        self.input_var = StringVar()
        input_entry = tk.Entry(left_frame, textvariable=self.input_var, font=("Arial", 11), width=45)
        input_entry.pack(padx=15, pady=5)
        tk.Label(left_frame, text="Example: 4 pm PT, 10:30 EST, 2 am UTC", font=("Arial", 9), bg="white", fg="gray").pack(anchor=tk.W, padx=15, pady=(0, 10))
        
        tk.Label(left_frame, text="Convert to (Timezone or Location):", font=("Arial", 10), bg="white", justify=tk.LEFT).pack(anchor=tk.W, padx=15, pady=(10, 5))
        self.output_var = StringVar()
        output_entry = tk.Entry(left_frame, textvariable=self.output_var, font=("Arial", 11), width=45)
        output_entry.pack(padx=15, pady=5)
        tk.Label(left_frame, text="Example: Istanbul, GMT+5, UTC-8, London", font=("Arial", 9), bg="white", fg="gray").pack(anchor=tk.W, padx=15, pady=(0, 10))
        
        # Info text
        info_text = """How to use:
• Enter time with timezone: "6 am PT", "12:30 EST"
• Enter location in output: "Istanbul", "London"
• Or specify timezone: "UTC+3", "GMT-5"
• Leave output empty for 24-hour UTC"""
        tk.Label(left_frame, text=info_text, font=("Arial", 9), bg="white", justify=tk.LEFT, fg="#333").pack(anchor=tk.W, padx=15, pady=15)
        
        # Middle panel - Conversion button (100x500)
        middle_frame = tk.Frame(main_frame, width=100, height=500, bg="#f0f0f0")
        middle_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=5, pady=5)
        
        tk.Button(middle_frame, text="Convert", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", 
                  command=self.convert_timezone, width=10, height=25, wraplength=80).pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Right panel - Output area (450x500)
        right_frame = tk.Frame(main_frame, width=450, height=500, bg="white", relief=tk.SUNKEN, bd=2)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        tk.Label(right_frame, text="Result", font=("Arial", 14, "bold"), bg="white").pack(pady=10)
        
        self.output_display = tk.Label(right_frame, text="", font=("Arial", 16, "bold"), bg="white", fg="#2196F3", wraplength=400)
        self.output_display.pack(pady=20)
        
        self.info_display = tk.Label(right_frame, text="Enter time and timezone to start", font=("Arial", 10), bg="white", fg="gray", wraplength=400, justify=tk.LEFT)
        self.info_display.pack(pady=10, padx=15)
        
        # Initialize geocoder
        self.geolocator = Nominatim(user_agent="timezone_converter")
        self.tf = TimezoneFinder()
    
    def parse_input_time(self, input_str):
        """Parse input string like '4 pm PT' or '10:30 EST'"""
        # Remove leading/trailing whitespace
        input_str = input_str.strip()
        
        # Pattern: time (am/pm or 24h format) + timezone
        pattern = r'(\d{1,2}):?(\d{0,2})\s*(am|pm|AM|PM)?\s*([A-Z]{2,}(?:[+-]\d{1,2})?|UTC[+-]\d{1,2}|GMT[+-]\d{1,2})?'
        match = re.match(pattern, input_str)
        
        if not match:
            raise ValueError("Invalid time format. Use format like '4 pm PT' or '10:30 EST'")
        
        hour = int(match.group(1))
        minute = int(match.group(2)) if match.group(2) else 0
        meridiem = match.group(3)
        timezone = match.group(4)
        
        if not timezone:
            raise ValueError("Timezone not specified")
        
        # Convert to 24-hour format
        if meridiem:
            meridiem = meridiem.lower()
            if meridiem == 'pm' and hour != 12:
                hour += 12
            elif meridiem == 'am' and hour == 12:
                hour = 0
        
        if hour < 0 or hour > 23 or minute < 0 or minute > 59:
            raise ValueError("Invalid time values")
        
        return hour, minute, timezone.upper()
    
    def get_timezone_offset(self, tz_str):
        """Get timezone offset from timezone code or location"""
        tz_str = tz_str.strip()
        
        # Try as timezone code first
        try:
            # Handle custom formats like UTC+5, GMT-3
            if tz_str.startswith('UTC') or tz_str.startswith('GMT'):
                match = re.match(r'(UTC|GMT)([+-])(\d{1,2})', tz_str, re.IGNORECASE)
                if match:
                    sign = 1 if match.group(2) == '+' else -1
                    offset = sign * int(match.group(3))
                    return offset
            
            # Try pytz timezone
            tz = pytz.timezone(tz_str)
            now = datetime.now(tz)
            offset = now.utcoffset().total_seconds() / 3600
            return offset
        except:
            pass
        
        # Try as location
        try:
            location = self.geolocator.geocode(tz_str, timeout=5)
            if location:
                tz_name = self.tf.timezone_at(lat=location.latitude, lng=location.longitude)
                if tz_name:
                    tz = pytz.timezone(tz_name)
                    now = datetime.now(tz)
                    offset = now.utcoffset().total_seconds() / 3600
                    return offset, tz_name
            raise ValueError(f"Location '{tz_str}' not found")
        except Exception as e:
            raise ValueError(f"Cannot find timezone or location: {tz_str}")
    
    def convert_timezone(self):
        """Convert time between timezones"""
        input_text = self.input_var.get().strip()
        output_text = self.output_var.get().strip()
        
        if not input_text:
            self.display_error("Please enter input time and timezone")
            return
        
        # Run conversion in thread to avoid freezing UI
        thread = threading.Thread(target=self._perform_conversion, args=(input_text, output_text))
        thread.start()
    
    def _perform_conversion(self, input_text, output_text):
        """Perform the actual conversion"""
        try:
            # Parse input
            hour, minute, from_tz = self.parse_input_time(input_text)
            
            # Get source timezone offset
            try:
                from_offset = self.get_timezone_offset(from_tz)
                if isinstance(from_offset, tuple):
                    from_offset, from_tz_name = from_offset
                from_tz_name = from_tz
            except:
                self.display_error(f"Unknown timezone: {from_tz}")
                return
            
            # Create datetime object in source timezone
            source_time = datetime(2026, 4, 6, hour, minute, 0)
            
            # Get target timezone offset
            if not output_text:
                # Default to UTC in 24-hour format
                to_offset = 0
                to_tz_name = "UTC"
            else:
                try:
                    result = self.get_timezone_offset(output_text)
                    if isinstance(result, tuple):
                        to_offset, to_tz_name = result
                    else:
                        to_offset = result
                        to_tz_name = output_text.upper()
                except Exception as e:
                    self.display_error(str(e))
                    return
            
            # Calculate time difference
            offset_diff = to_offset - from_offset
            
            # Apply offset
            target_time = source_time + timedelta(hours=offset_diff)
            
            # Check if day changed
            day_indicator = ""
            if target_time.day > source_time.day:
                day_indicator = " — Next Day"
            elif target_time.day < source_time.day:
                day_indicator = " — Previous Day"
            
            # Format output
            target_hour = target_time.hour
            target_minute = target_time.minute
            
            # Format time based on output specification
            if output_text and output_text[0].isalpha():  # Location given, use format from output_text
                time_str = f"{target_hour:02d}:{target_minute:02d}"
            else:  # Timezone code or empty
                time_str = f"{target_hour:02d}:{target_minute:02d}"
            
            # Build result string with timezone info
            if "UTC" in to_tz_name.upper() or "GMT" in to_tz_name.upper():
                result_str = f"{time_str} {to_tz_name}{day_indicator}"
            else:
                sign = '+' if to_offset >= 0 else '-'
                result_str = f"{time_str} {to_tz_name} (UTC{sign}{int(abs(to_offset))}){day_indicator}"
            
            # Display result
            info_str = f"From: {from_tz} → To: {to_tz_name}\nOffset difference: {offset_diff:+.1f} hours"
            
            self.master.after(0, lambda: self._update_display(result_str, info_str))
        
        except ValueError as e:
            self.display_error(str(e))
        except Exception as e:
            self.display_error(f"ERROR: {str(e)}")
    
    def display_error(self, message):
        """Display error message"""
        self.master.after(0, lambda: self._update_display("ERROR", message))
    
    def _update_display(self, result, info):
        """Update output display"""
        self.output_display.config(text=result)
        self.info_display.config(text=info)

def main():
    root = tk.Tk()
    app = TimezoneConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
