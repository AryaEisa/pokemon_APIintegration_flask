from flask import Flask, render_template, request
import requests

app = Flask(__name__)
base_url = "https://pokeapi.co/api/v2/"


@app.route("/all", methods=["GET", "POST"])
def all_pokemon():
    # 1. Bygg lista med Pokémon + deras stats
    pokemon_list = []
    for i in range(1, 51):
        url = f"https://pokeapi.co/api/v2/pokemon/{i}"
        res = requests.get(url)
        if res.status_code != 200:
            continue
        data = res.json()

        attack = next((s["base_stat"] for s in data["stats"] if s["stat"]["name"] == "attack"), 0)
        total_stats = sum(s["base_stat"] for s in data["stats"])

        pokemon_list.append({
            "id": i,
            "name": data["name"].capitalize(),
            "img": data["sprites"]["front_default"],
            "height": data["height"],
            "weight": data["weight"],
            "attack": attack,
            "total": total_stats
        })

    # 2. Filtrera om formulär skickats
    if request.method == "POST":
        min_height = int(request.form.get("min_height") or 0)
        max_weight = int(request.form.get("max_weight") or 10000)
        min_attack = int(request.form.get("min_attack") or 0)

        pokemon_list = [p for p in pokemon_list if
                        p["height"] >= min_height and
                        p["weight"] <= max_weight and
                        p["attack"] >= min_attack]

    return render_template("all.html", pokemon_list=pokemon_list)


def get_pokemon_info(name):
    url = f"{base_url}pokemon/{name.lower()}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        pokemon_name = request.form.get("pokemon_name")
        if not pokemon_name:
            return render_template("index.html", error="Please enter a Pokémon name.")
        
        data = get_pokemon_info(pokemon_name)
        if data:
            return render_template("result.html", pokemon=data)
        else:
            return render_template("index.html", error="Pokémon not found.")
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
