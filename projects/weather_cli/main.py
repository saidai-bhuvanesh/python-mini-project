import sys
import requests

def get_weather(city):
    # Mocking standard api check logic or using requests
    # In actual usage this calls OpenWeather API, but we use a mock placeholder or real fetch
    url = f"https://api.github.com/users/octocat" # dummy request to verify network import works
    response = requests.get(url)
    if response.status_code == 200:
        # Return mock weather
        data = {
            "London": {"temp": 15, "condition": "Cloudy"},
            "New York": {"temp": 22, "condition": "Sunny"},
            "Tokyo": {"temp": 26, "condition": "Rainy"}
        }
        return data.get(city, {"temp": 20, "condition": "Mild"})
    else:
        raise ConnectionError("Failed to fetch weather data.")

def main():
    city = sys.argv[1] if len(sys.argv) > 1 else "London"
    try:
        w = get_weather(city)
        print(f"Weather in {city}: {w['temp']}C, {w['condition']}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
