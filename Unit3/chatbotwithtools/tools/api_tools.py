import requests

def get_joke():
    url = "https://official-joke-api.appspot.com/random_joke"
    response = requests.get(url, timeout=5)

    if response.status_code == 200:
        data = response.json()
        return f"😂 {data['setup']} — {data['punchline']}"
    else:
        return "❌ Could not fetch joke"
