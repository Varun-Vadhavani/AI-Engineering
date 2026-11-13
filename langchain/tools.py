from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city. Use this when the user asks about
    the weather or temperature in a specific place."""
    fake_weather = {
        "ahmedabad": "34°C, sunny",
        "mumbai": "31°C, humid",
        "london": "9°C, rainy",
    }
    return fake_weather.get(city.lower(), f"No weather data for {city}")

@tool
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Convert an amount of money from one currency to another, using
    3-letter codes like USD, INR, EUR. Use this when the user asks how much
    money in one currency is worth in another."""
    rates_to_inr = {"INR": 1.0, "USD": 84.0, "EUR": 91.0}
    f, t = from_currency.upper(), to_currency.upper()
    if f not in rates_to_inr or t not in rates_to_inr:
        return f"Unsupported currency. Supported: {', '.join(rates_to_inr)}"
    result = amount * rates_to_inr[f] / rates_to_inr[t]
    return f"{amount} {f} = {result:.2f} {t}"

TOOLS = [get_weather, convert_currency]