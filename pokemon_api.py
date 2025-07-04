# =========================
# pokemon_api.py
# =========================

import requests             # Används för att göra HTTP-förfrågningar till PokeAPI
import json                 # För att läsa och skriva JSON-data
import os                  # För att hantera filsystemet (t.ex. kontrollera om fil finns)
from typing import List, Dict, Optional  # Typanvisningar för bättre kodförståelse och autokomplettering
from concurrent.futures import ThreadPoolExecutor, as_completed  # Parallellhämtning av API-data

# Bas-URL till det externa API:t
BASE_URL = "https://pokeapi.co/api/v2/"

# Namn på lokal cachefil för att spara API-resultat
CACHE_FILE = "pokemon_cache.json"

def fetch_pokemon_data(pokemon_id: int) -> Optional[Dict]:
    """
    Hämtar grundläggande information om en specifik Pokémon från PokeAPI
    baserat på dess ID. Returnerar en ordbok med:
      - ID
      - namn
      - bild-URL
      - längd
      - vikt
      - attack-statistik
      - total statistik (summa av alla base_stats)

    Returnerar None om något fel uppstår (t.ex. nätverksfel).
    """
    url = f"{BASE_URL}pokemon/{pokemon_id}"
    try:
        # Gör ett GET-anrop till PokeAPI för den angivna Pokémonen
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Kasta ett fel vid felkod (ex. 404)

        # Parsar JSON-responsen
        data = response.json()

        # Extrahera specifik statistik
        attack = next((s["base_stat"] for s in data["stats"] if s["stat"]["name"] == "attack"), 0)
        total_stats = sum(s["base_stat"] for s in data["stats"])

        # Returnera endast relevanta fält
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
        # Vid nätverksfel eller JSON-fel, skriv ut felmeddelande och returnera None
        print(f"[ERROR] Failed to fetch Pokémon ID {pokemon_id}: {e}")
        return None

def fetch_all_pokemon_parallel(start: int, end: int) -> List[Dict]:
    """
    Hämtar data för flera Pokémon parallellt via ThreadPoolExecutor.
    Detta görs för att spara tid vid masshämtning från API:t.
    
    Parametrar:
    - start: Start-ID (inklusive)
    - end: Slut-ID (exklusive)

    Returnerar en lista med ordböcker för varje Pokémon.
    """
    results = []

    # Skapa en trådpool med upp till 10 parallella trådar
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Mappa varje framtida resultat till sitt Pokémon-ID
        future_to_id = {executor.submit(fetch_pokemon_data, i): i for i in range(start, end)}

        # När varje framtid är klar, lägg till datan till listan
        for future in as_completed(future_to_id):
            data = future.result()
            if data:
                results.append(data)

    return results

def load_cached_pokemon() -> List[Dict]:
    """
    Läser tidigare cachad Pokémon-data från lokal JSON-fil.

    Om filen inte finns eller inte kan läsas korrekt, returneras en tom lista.
    """
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            # Returnera tom lista om filen är korrupt
            return []
    return []

def save_cache(data: List[Dict]) -> None:
    """
    Sparar en lista med Pokémon-data till cache-filen som JSON.

    Parametrar:
    - data: Lista med ordböcker som representerar Pokémon
    """
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_pokemon_info(name: str) -> Optional[Dict]:
    """
    Hämtar detaljerad information om en Pokémon med hjälp av dess namn.

    Returnerar hela JSON-objektet från API:t eller None vid fel.
    """
    url = f"{BASE_URL}pokemon/{name.lower()}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch Pokémon '{name}': {e}")
        return None
