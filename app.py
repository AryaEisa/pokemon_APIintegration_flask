from flask import Flask, render_template, request
from generate_stats import generate_chart_image
from pokemon_api import (
    get_pokemon_info,
    load_cached_pokemon,
    save_cache,
    fetch_all_pokemon_parallel
)
from security import rate_limit, sanitize_input, add_security_headers

app = Flask(__name__)

@app.after_request
def apply_security_headers(response):
    """
    Lägger till säkerhetsrelaterade HTTP-headers på varje svar.
    """
    return add_security_headers(response)

@app.route('/', methods=['GET', 'POST'])
@rate_limit(40)  # Max 40 requests/minut/IP
def index():
    """
    Startsidan där användaren kan söka efter en Pokémon.
    Om ett namn skickas via formuläret, hämtas datan från API:et.
    """
    if request.method == "POST":
        pokemon_name = request.form.get("pokemon_name", "").strip()
        if not pokemon_name:
            return render_template("index.html", error="Please enter a Pokémon name.")

        clean_name = sanitize_input(pokemon_name)

        data = get_pokemon_info(clean_name)
        if data:
            return render_template("result.html", pokemon=data)
        else:
            return render_template("index.html", error="Pokémon not found.")

    return render_template("index.html")


@app.route("/all", methods=["GET", "POST"])
@rate_limit(20)
def all_pokemon():
    """
    Visar alla Pokémon i en grid. Möjlighet att filtrera baserat på höjd, vikt och attack.
    Cachar datan för att undvika långsam laddning.
    """
    MAX_POKEMON = 150
    pokemon_list = load_cached_pokemon()

    # Om cache saknas, hämta från API
    if not pokemon_list:
        pokemon_list = fetch_all_pokemon_parallel(1, MAX_POKEMON + 1)
        save_cache(pokemon_list)

    # Filtreringslogik om POST
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


@app.route("/stats")
@rate_limit(10)
def stats():
    """
    Genererar och visar ett diagram med attacker för alla Pokémon.
    Bilden skapas dynamiskt och renderas på en egen sida.
    """
    generate_chart_image()  # Skrivs till static/stats.png
    return render_template("stats.html", image_url="/static/stats.png")


if __name__ == "__main__":
    app.run(debug=True)
