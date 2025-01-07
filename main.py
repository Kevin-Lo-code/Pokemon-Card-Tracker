import requests

url = 'https://api.pokemontcg.io/v2/cards'
params = {
    "q": "name:swampert",
    "pageSize":10
}
response = requests.get(url, params=params)
if response.status_code == 200:
    data = response.json()
    cards = data.get("data", [])
    if cards:
        for card in cards:
            card_id = card.get("id", "Unknown ID")
            card_name = card.get("name", "Unknown")
            tcgplayer_data = card.get("tcgplayer", {})
            prices = tcgplayer_data.get("prices", {})
            if prices:
                normal_prices = prices.get("normal", {})
                normal_market = normal_prices.get("market", "N/A")
                holofoil_prices = prices.get("holofoil", {})
                holofoil_market = holofoil_prices.get("market", "N/A")
                print(f"Card: {card_name} - {card_id}")
                print("\nNormal Prices:")
                print(f"Market: ${normal_market}")
                print("\nHolofoil Prices:")
                print(f"Market: ${holofoil_market}\n")
            else:
                print("Tcgplayer Pricing data is unavailable")
    else:
        print("No cards found")
else:
    print(f"Fail to get data. Status Code: {response.status_code}")