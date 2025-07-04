# PokéDex Viewer – Flaskbaserad Web App

Detta projekt är en enkel men kraftfull webbapplikation som låter användaren söka och filtrera Pokémon med hjälp av ett externt API (PokeAPI). Användaren kan skriva in ett namn, filtrera baserat på attribut (t.ex. attack, vikt, längd) och visa en lista med kort för varje Pokémon. Projektet är helt byggt i Python med Flask som backend-ramverk.
![](static/images/1.png)
![](static/images/2.png)
![](static/images/3.png)

## Funktioner

- Sök Pokémon med namn
- Visa detaljer som längd, vikt och attack
- Filtrera efter min/max-attribut
- Mobilanpassad och responsiv design
- Dynamisk kortvy över alla Pokémon
- Integration med externt API (PokeAPI)

## Använda tekniker

### 1. Flask (Python Web Framework)
Flask används för att skapa servern, hantera routing, processa formulärdata och rendera HTML-sidor dynamiskt med hjälp av Jinja2.

### 2. Requests (Python HTTP-bibliotek)
Requests används för att göra HTTP-anrop till PokeAPI och hämta Pokémon-data i JSON-format.

### 3. HTML 
HTML används för att skapa strukturen på webbplatsen. Flask använder Jinja2-mallmotor för att rendera innehåll dynamiskt direkt från Python-kod.

### 4. CSS (Stil och Layout)
All design hanteras med anpassad CSS som inkluderar mobilanpassning, färgteman, kortlayout och grid-system. Designen är pixelinspirerad och tydligt spelrelaterad.

### 5. JavaScript (Filtrering på klientsidan)
Enkel JavaScript används för att implementera realtidsfiltrering i listan med Pokémon-kort, baserat på användarens sökinput.

### 6. PokeAPI (Externt REST API)
PokeAPI används som datakälla. Varje gång en användare gör en förfrågan hämtas Pokémonens attribut via ett HTTP-anrop.

### 7. JSON (Dataformat)
All data från PokeAPI levereras i JSON och omvandlas till Python-objekt för vidare bearbetning i applikationen.


## Installation och körning

1. Klona projektet:
- git clone https://github.com/AryaEisa/pokemon_APIintegration_flask.git

## Kontakt

Skapad av Arya Pour Eisa  
Mejla mig via: **arya@aryaeisa.com**  
Portfolio: [aryaeisa.com](https://aryaeisa.com)

---