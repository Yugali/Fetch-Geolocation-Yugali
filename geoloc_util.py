import requests
import json
import argparse
import time  # For rate-limiting handling

API_KEY = 'f897a99d971b5eef57be6fafa0d83239'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

def fetch_geolocation(location):
    """Fetches geolocation information for the given city or zip code."""
    params = {
        'q': location,
        'appid': API_KEY,
        'units': 'metric'
    }
    
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        if 'coord' in data:
            # Prepare the result to store
            result = {
                "location": data['name'],
                "country": data['sys']['country'],
                "latitude": data['coord']['lat'],
                "longitude": data['coord']['lon']
            }

            # Open the JSON file in append mode and store the result
            with open('locations_data.json', 'a') as file:
                json.dump(result, file)
                file.write("\n")  # Newline for each entry
            print(f"Data for {location} stored successfully.")

        else:
            print(f"No geolocation data found for: {location}")
    
    elif response.status_code == 429:
        # Rate limit exceeded, wait for 60 seconds and retry
        print("Rate limit exceeded. Waiting 60 seconds before retrying...")
        time.sleep(60)  # Sleep for 60 seconds
        return fetch_geolocation(location)  # Retry the request
    else:
        print(f"Error: {response.status_code}. Unable to fetch data for {location}.")

def main():
    parser = argparse.ArgumentParser(description="Geolocation Utility")
    parser.add_argument('--locations', nargs='+', help="List of city/state or zip code inputs", required=True)
    
    args = parser.parse_args()
    
    for location in args.locations:
        fetch_geolocation(location)

if __name__ == '__main__':
    main()
