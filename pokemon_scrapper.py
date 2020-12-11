from bs4 import BeautifulSoup
import requests
import json

from constants import TYPES

url = 'https://pokemondb.net/pokedex/all'

page_response = requests.get(url, timeout=5)

page_content = BeautifulSoup(page_response.content, "html.parser")


pokemonRows = page_content.find_all("tr")
pokemonDict = {}

for row in pokemonRows[1:]:
    # Name
    name = row.find("a", attrs={"class": "ent-name"}).text
    ifMegaEvo = row.find("small", attrs={"class": "text-muted"})
    if ifMegaEvo:
        name = ifMegaEvo.text

    # Types
    typesHtml = row.find_all("a", attrs={"class": "type-icon"})
    typesArray = list(map(lambda data: TYPES.index(data.text.upper()), typesHtml))

    # Base Stats
    statsHtml = row.find_all("td")[4:]
    statsArray = list(map(lambda data: int(data.text), statsHtml))

    # Format
    if len(typesArray) > 1:
        pokemonDict[name] = {
        "Type1": typesArray[0],
        "Type2": typesArray[1],
        "Hp": statsArray[0],
        "Attack": statsArray[1],
        "Defense": statsArray[2],
        "Spattack": statsArray[3],
        "Spdefense": statsArray[4],
        "Speed": statsArray[5]
    }
    else:
        pokemonDict[name] = {
        "Type1": typesArray[0],
        "Hp": statsArray[0],
        "Attack": statsArray[1],
        "Defense": statsArray[2],
        "Spattack": statsArray[3],
        "Spdefense": statsArray[4],
        "Speed": statsArray[5]
    }

# Saving
with open('db/pokedex.json', 'w') as outfile:
    json.dump(pokemonDict, outfile)

# pokemonDict[name]["Type2"] = typesArray[1]
# print(pokemonDict)
# print(name, typesArray, statsArray)
