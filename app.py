from flask import Flask, render_template, request
import requests

# Skapa en instans av Flask-applikationen
app = Flask(__name__)

# Bas-URL till PokeAPI
base_url = "https://pokeapi.co/api/v2/"

# Route för att visa alla Pokémon (första 50)
@app.route("/all", methods=["GET", "POST"])
def all_pokemon():
    # 1. Hämta en lista med de första 50 Pokémon och deras attribut
    pokemon_list = []
    for i in range(1, 51):  # Begränsar till Pokémon med ID 1–50
        url = f"https://pokeapi.co/api/v2/pokemon/{i}"
        res = requests.get(url)
        if res.status_code != 200:
            continue  # Hoppa över om API-svaret är felaktigt
        data = res.json()

        # Extrahera attack-stat separat
        attack = next((s["base_stat"] for s in data["stats"] if s["stat"]["name"] == "attack"), 0)

        # Summera alla bas-stats för att få ett totalvärde (valfritt, visas ej direkt)
        total_stats = sum(s["base_stat"] for s in data["stats"])

        # Lägg till informationen i listan
        pokemon_list.append({
            "id": i,
            "name": data["name"].capitalize(),
            "img": data["sprites"]["front_default"],
            "height": data["height"],
            "weight": data["weight"],
            "attack": attack,
            "total": total_stats
        })

    # 2. Om användaren har skickat ett filtreringsformulär
    if request.method == "POST":
        # Hämta filtreringsparametrar från formuläret eller sätt standardvärden
        min_height = int(request.form.get("min_height") or 0)
        max_weight = int(request.form.get("max_weight") or 10000)
        min_attack = int(request.form.get("min_attack") or 0)

        # Filtrera listan baserat på de angivna kriterierna
        pokemon_list = [
            p for p in pokemon_list
            if p["height"] >= min_height and
               p["weight"] <= max_weight and
               p["attack"] >= min_attack
        ]

    # Rendera HTML-sidan med (filtrerad) lista
    return render_template("all.html", pokemon_list=pokemon_list)

# Hjälpfunktion för att hämta information om en specifik Pokémon via namn
def get_pokemon_info(name):
    url = f"{base_url}pokemon/{name.lower()}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Startsidan där användaren kan söka efter en specifik Pokémon
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Hämta Pokémon-namnet från formuläret
        pokemon_name = request.form.get("pokemon_name")
        if not pokemon_name:
            return render_template("index.html", error="Please enter a Pokémon name.")

        # Hämta data från API:t
        data = get_pokemon_info(pokemon_name)
        if data:
            return render_template("result.html", pokemon=data)
        else:
            return render_template("index.html", error="Pokémon not found.")

    # GET-request: visa bara formuläret
    return render_template("index.html")

# Kör applikationen om filen körs direkt
if __name__ == "__main__":
    app.run(debug=True)  # Debug mode ger detaljerade felmeddelanden under utveckling
