# Geolocation Utility

This is a Python-based utility for fetching geolocation data (latitude, longitude, and country) of cities or locations using the OpenWeather API. The program stores the results in a JSON file called `locations_data.json`.

## Features
- Fetches geolocation data for multiple cities or locations.
- Handles rate limiting with automatic retries.
- Stores the fetched data in `locations_data.json` file in append mode.
- Supports locations with special characters (e.g., São Paulo).
- Handles errors like invalid locations, rate limit issues, and file write permissions.

## Setup

1. Clone this repository or download the code.
2. Install the required dependencies using `pip` (see below for `requirements.txt`).
3. Get your API key from [OpenWeatherMap](https://openweathermap.org/) and replace it in the script where specified.
4. Run the script using the command line.

## Usage

```bash
python geoloc_util.py --locations "Madison, WI, USA" "New York, USA" "São Paulo, Brazil"

##Testing

pytest test_geoloc_util.py
