# =========================
# pokemon_api.py
# =========================

import requests
import json
import os
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "https://pokeapi.co/api/v2/"
CACHE_FILE = "pokemon_cache.json"

def fetch_pokemon_data(pokemon_id: int) -> Optional[Dict]:
    """
    Hämtar data för en enskild Pokémon från PokeAPI.
    Returnerar ett ordbok med utvald information eller None vid fel.
    """
    url = f"{BASE_URL}pokemon/{pokemon_id}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

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
        print(f"[ERROR] Failed to fetch Pokémon ID {pokemon_id}: {e}")
        return None

def fetch_all_pokemon_parallel(start: int, end: int) -> List[Dict]:
    """
    Hämtar flera Pokémon parallellt med ThreadPoolExecutor.
    Returnerar en lista med Pokémon-data.
    """
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_id = {executor.submit(fetch_pokemon_data, i): i for i in range(start, end)}
        for future in as_completed(future_to_id):
            data = future.result()
            if data:
                results.append(data)
    return results

def load_cached_pokemon() -> List[Dict]:
    """
    Läser cache-filen om den finns. Returnerar lista med Pokémon.
    """
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_cache(data: List[Dict]) -> None:
    """
    Sparar Pokémon-data i cache-filen.
    """
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_pokemon_info(name: str) -> Optional[Dict]:
    """
    Hämtar detaljerad information om en Pokémon med namn.
    """
    url = f"{BASE_URL}pokemon/{name.lower()}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch Pokémon '{name}': {e}")
        return None
