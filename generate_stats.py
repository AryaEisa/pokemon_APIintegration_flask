# generate_stats.py
import requests
import matplotlib
matplotlib.use('Agg')  # Använd en icke-interaktiv backend (viktig fix för Flask)
import matplotlib.pyplot as plt
from statistics import mean
import os

POKEMON_COUNT = 50

def fetch_pokemon_data(poke_id):
    """Hämtar attack, vikt och höjd för en specifik Pokémon"""
    url = f"https://pokeapi.co/api/v2/pokemon/{poke_id}"
    try:
        res = requests.get(url, timeout=5)
        res.raise_for_status()
        data = res.json()
        attack = next(stat['base_stat'] for stat in data['stats'] if stat['stat']['name'] == 'attack')
        return {
            'name': data['name'].capitalize(),
            'height': data['height'],
            'weight': data['weight'],
            'attack': attack
        }
    except requests.RequestException as e:
        print(f"[!] Misslyckades hämta data för ID {poke_id}: {e}")
        return None

def collect_data():
    """Hämtar data för flera Pokémon och returnerar som lista"""
    all_data = []
    for i in range(1, POKEMON_COUNT + 1):
        p = fetch_pokemon_data(i)
        if p:
            all_data.append(p)
    return all_data

def generate_chart_image(path="static/stats.png"):
    """Skapar och sparar ett stapeldiagram med attack-stats"""
    data = collect_data()
    if not data:
        print("[!] Ingen data tillgänglig för att generera diagram.")
        return

    names = [p['name'] for p in data]
    attacks = [p['attack'] for p in data]

    plt.figure(figsize=(12, 6))
    plt.bar(names, attacks, color="cyan")
    plt.title("Attack Stats per Pokémon")
    plt.ylabel("Attack")
    plt.xticks(rotation=90)
    plt.tight_layout()

    # Spara som PNG till statisk mapp
    plt.savefig(path)
    plt.close()
