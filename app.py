from flask import Flask, render_template, request
import requests
from typing import Optional, List, Dict

app = Flask(__name__)
base_url = "https://pokeapi.co/api/v2/"

# =========================
# API-HJÄLPMETODER
# =========================

def fetch_pokemon_data(pokemon_id: int) -> Optional[Dict]:
    """Hämtar data för en enskild Pokémon från PokeAPI"""
    url = f"{base_url}pokemon/{pokemon_id}"
    try:
        res = requests.get(url, timeout=5)
        res.raise_for_status()
        data = res.json()

        # Extrahera relevanta värden
        attack = next((s["base_stat"] for s in data["stats"] if s["stat"]["name"] == "attack"), 0)
        total_stats = sum(s["base_stat"] for s in data["stats"])

        return {
            "id": pokemon_id,
            "name": data["name"].capitalize(),
            "img": data["sprites"]["front_default"],
            "height": data["height"],
            "weight": data["weight"],
            "attack": attack,
            "total": total_stats
        }
    except (requests.RequestException, ValueError) as e:
        print(f"⚠️ Failed to fetch data for Pokémon ID {pokemon_id}: {e}")
        return None


def get_pokemon_info(name: str) -> Optional[Dict]:
    """Hämtar full info om en Pokémon via namn"""
    url = f"{base_url}pokemon/{name.lower()}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"⚠️ Error fetching Pokémon '{name}': {e}")
        return None


# =========================
# ROUTES
# =========================

@app.route("/all", methods=["GET", "POST"])
def all_pokemon():
    """Visa alla Pokémon med filtreringsmöjligheter"""

    # Konfiguration – ändra här om du vill visa fler Pokémon
    MAX_POKEMON = 50
    pokemon_list: List[Dict] = []

    # 1. Hämta alla Pokémon och bygg listan
    for i in range(1, MAX_POKEMON + 1):
        data = fetch_pokemon_data(i)
        if data:
            pokemon_list.append(data)

    # 2. Om filtrering är aktiv (POST-request)
    if request.method == "POST":
        min_height = int(request.form.get("min_height") or 0)
        max_weight = int(request.form.get("max_weight") or 9999)
        min_attack = int(request.form.get("min_attack") or 0)

        pokemon_list = [
            p for p in pokemon_list
            if p["height"] >= min_height
            and p["weight"] <= max_weight
            and p["attack"] >= min_attack
        ]

    # 3. Rendera HTML-sidan med filtrerad lista
    return render_template("all.html", pokemon_list=pokemon_list)


@app.route("/", methods=["GET", "POST"])
def index():
    """Startsida där man söker efter en Pokémon med namn"""

    if request.method == "POST":
        pokemon_name = request.form.get("pokemon_name")
        if not pokemon_name:
            return render_template("index.html", error="Please enter a Pokémon name.")

        data = get_pokemon_info(pokemon_name)
        if data:
            return render_template("result.html", pokemon=data)
        else:
            return render_template("index.html", error="Pokémon not found.")

    # GET: visa bara sökformuläret
    return render_template("index.html")


# =========================
# MAIN
# =========================

if __name__ == "__main__":
    # Starta servern med debug-läge aktivt
    app.run(debug=True)
