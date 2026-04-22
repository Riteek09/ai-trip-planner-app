import os
import requests
from google import genai


def generate_itinerary(destination: str, days: int, mood: str, group_type: str, budget: int) -> str:
    api_key = os.getenv('GEMINI_API_KEY')

    if not api_key:
        return 'Gemini API key is missing. Add GEMINI_API_KEY in your environment variables.'

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are an expert travel planner.

Create a detailed {days}-day trip itinerary for {destination}.

Traveler mood: {mood}
Group type: {group_type}
Budget: INR {budget}

Instructions:
1. Make the itinerary day-wise.
2. For each day include Morning, Afternoon, Evening.
3. Suggest local food and one practical transport tip.
4. Keep the plan realistic within the budget.
5. End with 3 travel tips.
6. Use clean headings and short bullet points.
"""

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return getattr(response, 'text', None) or 'No itinerary generated.'

    except Exception as exc:
        return f'Unable to generate itinerary: {exc}'


def get_weather(destination: str) -> str:
    api_key = os.getenv('WEATHER_API_KEY')

    if not api_key:
        return 'Weather API key is missing. Add WEATHER_API_KEY in your environment variables.'

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": f"{destination},IN",
        "appid": api_key,
        "units": "metric",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if response.status_code != 200:
            return f"Weather not available: {data.get('message', 'API error')}"

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"].title()
        wind = data.get("wind", {}).get("speed", "N/A")

        return f"🌡️ {temp}°C | ☁️ {description} | 💧 {humidity}% | 🌬️ {wind} m/s"

    except Exception as exc:
        return f"Weather error: {exc}"


def estimate_cost(days: int, budget: int, group_type: str) -> str:
    multiplier = {
        "solo": 1.0,
        "friends": 1.8,
        "couple": 1.6,
        "family": 2.2,
    }

    estimated = int(days * 2500 * multiplier.get(group_type, 1.0))
    capped = min(estimated, budget)

    return f"Approximate usable budget: INR {capped}"
