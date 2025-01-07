import requests
import tkinter as tk
from tkinter import ttk

url = 'https://api.pokemontcg.io/v2/cards'

def fetch_data():
    response = requests.get(url, params={"q": "name:swampert", "pageSize": 10})
    if response.status_code == 200:
        data = response.json()
        cards = data.get("data", [])
        if cards:
            listbox.delete(0, tk.END)
            for card in cards:
                card_id = card.get("id", "Unknown ID")
                card_name = card.get("name", "Unknown")
                listbox.insert(tk.END, f"{card_id} - {card_name}")
                card_details[card_id] = card
        else:
            listbox.insert(tk.END, "No cards found.")
    else:
        listbox.insert(tk.END, f"Failed to fetch cards. Status Code: {response.status_code}")
def show_details(event):
    selected_index = listbox.curselection()
    if selected_index:
        selected_card_info = listbox.get(selected_index)
        card_id = selected_card_info.split(" - ")[0]
        card = card_details.get(card_id, None)
        if card:
            card_name = card.get("name", "Unknown")
            tcgplayer_data = card.get("tcgplayer", {})
            prices = tcgplayer_data.get("prices", {})
            if prices:
                normal_prices = prices.get("normal", {})
                normal_market = normal_prices.get("market", "N/A")
                holofoil_prices = prices.get("holofoil", {})
                holofoil_market = holofoil_prices.get("market", "N/A")
                details_text = f"Card: {card_name} - {card_id} \n\n"
                details_text += "Normal Prices:\n"
                details_text += f"Market: ${normal_market}\n"
                details_text += "Holofoil Prices:\n"
                details_text += f"Market: ${holofoil_market}\n"
            else:
                details_text = "Tcgplayer Pricing data is unavailable"
            details_label.config(text=details_text)
root = tk.Tk()
root.title("Pokémon TCG Card Prices")
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)
listbox = tk.Listbox(frame, width=50, height=15)
listbox.pack(side=tk.LEFT)
scrollbar = tk.Scrollbar(frame, orient="vertical", command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill="y")
listbox.config(yscrollcommand=scrollbar.set)
details_label = tk.Label(root, text="Select a card to see details", justify=tk.LEFT, anchor="w")
details_label.pack(padx=10, pady=10, fill=tk.X)
fetch_button = tk.Button(root, text="Fetch Cards", command=fetch_data)
fetch_button.pack(pady=10)
listbox.bind("<<ListboxSelect>>", show_details)
card_details = {}
root.mainloop()