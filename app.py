from flask import Flask, render_template, request
from pokemon_api import (
    get_pokemon_info,
    load_cached_pokemon,
    save_cache,
    fetch_all_pokemon_parallel
)

app = Flask(__name__)

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

@app.route("/all", methods=["GET", "POST"])
def all_pokemon():
    MAX_POKEMON = 1500
    pokemon_list = load_cached_pokemon()

    if not pokemon_list:
        pokemon_list = fetch_all_pokemon_parallel(1, MAX_POKEMON + 1)
        save_cache(pokemon_list)

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

    return render_template("all.html", pokemon_list=pokemon_list)

if __name__ == "__main__":
    app.run(debug=True)
