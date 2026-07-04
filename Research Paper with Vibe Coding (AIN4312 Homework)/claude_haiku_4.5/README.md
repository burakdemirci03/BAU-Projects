# Timezone Converter

A Python application with a GUI interface for converting times between different timezones and locations.

## Features

- ✅ Convert time between timezones (PT, EST, UTC, GMT, etc.)
- ✅ Support for location-based conversion (e.g., "Istanbul", "London")
- ✅ Custom timezone offsets (e.g., "UTC+3", "GMT-5")
- ✅ Automatic detection of day changes (Next Day / Previous Day)
- ✅ Error handling for invalid inputs
- ✅ Clean, intuitive GUI interface (1000x500)
- ✅ 24-hour time format output

## Installation

1. Clone or download this directory
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the application:

```bash
python timezone_converter.py
```

### GUI Layout

- **Left Panel (450x500)**: Input area where you enter:
  - Time and timezone (required)
  - Target timezone or location (optional)
- **Middle Panel (100x500)**: "Convert" button to execute the conversion

- **Right Panel (450x500)**: Output area showing the converted time and details

### Input Examples

#### Time with Timezone Format:

- `6 am PT` → 6:00 AM Pacific Time
- `4 pm EST` → 4:00 PM Eastern Time
- `10:30 UTC` → 10:30 UTC
- `2 am GMT` → 2:00 AM GMT
- `15:45 PST` → 3:45 PM PST
- `12:00 UTC+5` → 12:00 in UTC+5 timezone

#### Output Examples (Optional):

- **Timezone code**: `EST`, `UTC+3`, `GMT-5`, `IST`, `JST`
- **Location**: `Istanbul`, `London`, `New York`, `Tokyo`
- **Leave empty**: Defaults to UTC in 24-hour format

### Example Conversions

1. **Time in PT to Istanbul**
   - Input: `4 pm PT`
   - Output: `Istanbul`
   - Result: `2:00 — Next Day`

2. **Time in EST to UTC**
   - Input: `10:30 AM EST`
   - Output: `UTC`
   - Result: `15:30`

3. **Time in UTC to GMT+5**
   - Input: `12:00 UTC`
   - Output: `UTC+5`
   - Result: `17:00`

4. **Time in JST to London**
   - Input: `9 pm JST`
   - Output: `London`
   - Result: Converted to London timezone

## Supported Timezones

### Common 2-Letter Codes:

- PT, PST, PDT (Pacific)
- MT, MST, MDT (Mountain)
- CT, CST, CDT (Central)
- ET, EST, EDT (Eastern)
- UTC, UTC+X, UTC-X
- GMT, GMT+X, GMT-X
- IST (Indian Standard Time)
- JST (Japan Standard Time)
- BST (British Summer Time)
- And many more IANA timezone identifiers

### Location Support:

Any major city or country name can be entered as output. The application uses geolocation to find the timezone.

Examples:

- Istanbul, London, Tokyo, New York, Sydney, Singapore, Dubai, Paris, Beijing, Mumbai, etc.

## How It Works

1. **Parse Input**: Extracts time and timezone from input string
2. **Get Offsets**: Retrieves UTC offset for both source and target
3. **Convert**: Calculates time difference and applies offset
4. **Check Day**: Determines if conversion crosses day boundary
5. **Format Output**: Displays result in 24-hour format with timezone info

## Error Handling

The application displays "ERROR" if:

- Invalid time format is entered
- Timezone/location is not recognized
- Any other processing error occurs

Error messages help identify the issue for correction.

## Technical Details

- **Time Library**: Python's `datetime` module
- **Timezone Support**: `pytz` library with IANA timezone database
- **Location Lookup**: `geopy` (OpenStreetMap Nominatim)
- **Timezone Finding**: `timezonefinder` (latitude/longitude to timezone)
- **GUI Framework**: `tkinter` (built-in Python library)

## Notes

- Conversions use the current date (6 April 2026) as base date
- 24-hour format is always used for output
- Day changes are clearly indicated
- All calculations are performed using arithmetic operations on offsets
