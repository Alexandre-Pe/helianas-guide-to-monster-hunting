import json
from time import time

def fuse(sp):
    if sp == '':
        return ''
    content = sp[0]
    for s in sp[1:]:
        if content[-1] == '-':
            content = content[:-1] + s
        else:
            content += ' ' + s
    return content

print(fuse(input().split(' ')))

# @spell 

def fuse_table(sp):
    if sp == ['']:
        return ''
    s = sp[0].split(' ')
    die, field = s[0], ' '.join(s[1:])
    t = '\n' + die + ' | ' + field + ' | '
    for s in sp[1:]:
        s = s.split(' ')
        t += '\n' + s[0] + ' | ' + ' '.join(s[1:]) + ' | '
    return t

def class_list(string):
    cls = string.split(', ')
    if 'Tamer' in cls:
        cls.remove('Tamer')
        return [{"name": c, "source": "PHB"} for c in cls] + [({"name": "Tamer", "source": "HelianasGuidetoMonsterHunting"})]
    return [{"name": c, "source": "PHB"} for c in cls]

ponct = [',',';','?','.',':', '(', ')', '-', '_', '!', '%']
def strip(ListeParasite, Texte):
    for s in ListeParasite:
        Texte=Texte.replace(s, '')
    return Texte

def stripListe(ListeParasite, ListeTexte):
    L = []
    for Texte in ListeTexte:
        L.append(strip(ListeParasite, Texte))
    return L

def add_fancy(string):
    conditions = ['blinded', 'charmed', 'deafened', 'exhaustion', 'frightened', 'grappled', 'incapicitated',
        'invisible', 'paralyzed', 'petrified', 'poisoned', 'prone', 'restrained', 'stunned', 'unconscious']
    dice = ["d4", "d6", "d8", "d10", "d12", "d20", "d100"]

    L  = string.split(" ")
    for i, w in enumerate(L):
        w = strip(ponct, w)
        if w in conditions:
            L[i] = '{@condition ' + w + '}'
        elif w in dice:
            L[i] = '{@dice ' + w + '}'
        else:
            for d in dice:
                if d in w:
                    L[i] = '{@damage ' + w + '}'
                    break
    return ' '.join(L)

def add_fancy_higher(string, level, damage):
    conditions = ['blinded', 'charmed', 'deafened', 'exhaustion', 'frightened', 'grappled', 'incapicitated',
        'invisible', 'paralyzed', 'petrified', 'poisoned', 'prone', 'restrained', 'stunned', 'unconscious']
    dice = ["d4", "d6", "d8", "d10", "d12", "d20", "d100"]

    L  = string.split(" ")
    for i, w in enumerate(L):
        w = strip(ponct, w)
        if w in conditions:
            L[i] = '{@condition ' + w + '}'
        elif w in dice:
            L[i] = '{@dice ' + w + '}'
        else:
            for d in dice:
                if d in w:
                    L[i] = '{@scaledamage  ' + f'{damage}|{level}-9|{w}' + '}'
                    break
    return ' '.join(L)


def convert():
    spell = dict()
    data_field = ["name", "level", "school"] 
        # "Save", "Damage", "Damage Type", "Healing", 
        # "Save Success", "Spell Attack", "Higher Spell Slot Die", 
        # "Higher Spell Slot Dice", "data-Cantrip Scaling", "Range", 
        # "Classes", "Duration", "Material", "Components", "Casting Time", 
        # "Concentration", "data-RangeNum"]
    print("\nInfos de base")
    for field in data_field:
        spell[field] = input(f'{field}: ').strip()
    
    spell["level"] = int(spell["level"])
    i = input("ritual: ").strip()
    if i != '':
        spell["meta"] = {"ritual": i.lower() == "true"}
    
    print("\nCasting Time infos")
    spell["time"] = [{
        "number": int(input('number: ').strip()),
        "unit": input('unit: ').strip()
    }]

    print("\nRange infos")
    range = {
        "type": input('type parmi "special", "point", line", "cube", "cone", "radius", "sphere", "hemisphere", "cylinder": ').strip(),
        "distance": {
            "type": input("type distance (feet, miles, self, plan, sight, ...): ")
        }
    }
    i = input('amount distance: ').strip()
    if i != '':
        range["distance"]["amount"] = int(i)

    spell["range"] = range

    print("\nComponents infos")
    spell["components"] = {
        "v": input('v: ').strip().lower() == "true",
        "s": input('s: ').strip().lower() == "true",
        "m": input('m text: ').strip()
    }

    if spell["components"]["m"] == "":
        spell["components"].pop("m")

    print("\nDuration infos")
    duration = {
            "type": input('type parmi "timed", "instant", "permanent", "special": ').strip(),
            "concentration": input('concentration ? (True/False): ').strip().lower() == "true"
        }

    if duration["type"] == "timed":
        duration["duration"] = {
                "type": input('unité de temps: ').strip(),
                "amount": int(input('quantité unité: ').strip()),
                "upTo": input('upTo ? (True/False): ').strip().lower() == "true"
            }

    spell["duration"] = [duration]

    ## Première partie de la description
    i = input("\nDescription: ").strip()
    entries = []
    while i != '':
        entries.append(add_fancy(fuse(i.split('\n'))))
        i = input("Suite description (vide si finie): ").strip()

    ## Abilité spéciale s'il y en a une
    i = input("\nNom Abilité spéciale (vide si aucune): ").strip()
    while i != '':
        text_ability = fuse(input("Texte Abilité spéciale: ").strip().split('\n'))
        entries.append({
            "type": "entries",
			"name": i,
			"entries": [add_fancy(text_ability)]
        })
        i = input("Nom Abilité spéciale suivante(vide si finie): ").strip()
    spell["entries"] = entries

    ## À plus haut niveau s'il y a
    ahl = input("\nAt higher levels (vide si absent): ").strip()
    entriesHigherLevel = []
    if ahl != '':
        ahl = fuse(ahl.split('\n')) + '.'


    spell["classes"] = {
        "fromClassList": class_list(input("\nListe des classes: ").strip())
    }

    spell["source"] = "HelianasGuidetoMonsterHunting"

    print("\nRoll20 infos (laiser vide si pas applicable)")
    roll20Spell = {
        "name": spell["name"],
        "source": spell["source"],
        "data": {}
    }
    data_field = ["Save", "Damage", "Damage Type", "Healing", 
        "Save Success", "Spell Attack", "Higher Spell Slot Die", 
        "Higher Spell Slot Dice", "Add Casting Modifier",
        "Secondary Damage", "Secondary Damage Type",
        "Secondary Higher Spell Slot Die", "Secondary Higher Spell Slot Dice",
        "Secondary Add Casting Modifier", "data-Cantrip Scaling"]
    for field in data_field:
        i = input(f'{field}: ').strip()
        if i != '':
            roll20Spell["data"][field] = i

    if "Damage Type" in roll20Spell["data"].keys():
        spell["damageInflict"] = [roll20Spell["data"]["Damage Type"].lower()]
        if "Secondary Damage Type" in roll20Spell["data"].keys():
            spell["damageInflict"].append(roll20Spell["data"]["Secondary Damage Type"].lower())
    if "Save" in roll20Spell["data"].keys() and roll20Spell["data"]["Save"] in ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]:
        spell["savingThrow"] = [roll20Spell["data"]["Save"].lower()]
    if "Spell Attack" in roll20Spell["data"].keys():
        spell["spellAttack"] = [roll20Spell["data"]["Spell Attack"][0].capitalize()]

    if ahl != '':
        if "Damage" in roll20Spell["data"].keys():
            ahl = add_fancy_higher(ahl, spell["level"], roll20Spell["data"]["Damage"])
        entriesHigherLevel.append({
            "type": "entries",
			"name": "At Higher Levels",
			"entries": [ahl]
        })
    spell["entriesHigherLevel"] = entriesHigherLevel
    
    i = input("ability check: ")
    if i != '':
        spell["abilityCheck"] = i.lower()

    return spell, roll20Spell


spell, roll20Spell = [], []
while input("\nContinuer ? (o/n): ") == 'o':
    s, r = convert()
    spell.append(s)
    roll20Spell.append(r)

h = time()
name = "helianas-guide-to-spell.json"
try:
    with open(name, 'r') as f:
        data = json.load(f)
except:
    with open("base.json", 'r') as f:
        data = json.load(f)
    data["_meta"]["dateAdded"] = round(h)
data["_meta"]["dateLastModified"] = round(h)
data["spell"] += spell
data["roll20Spell"] += roll20Spell
with open(name, 'w') as f:
    json.dump(data, f, indent=4)


name = "helianas-guide-to-spell.json"
with open(name, 'r') as f:
    data = json.load(f)
h = time()
data["_meta"]["dateLastModified"] = round(h)
for i, r20 in enumerate(data["roll20Spell"]):
    print(r20["name"])
    assert r20["name"] == data["spell"][i]["name"]
    foundryData = {
        "target.value": 6,
        "target.units": "m",
        "target.type": "sphere"
    }
    foundryFlags = {}
    K = r20["data"].keys()
    if "Damage" in K:
        foundryData["damage.parts"] = [
            r20["data"]["Damage"]
        ]
        if "Damage Type" in K:
            foundryData["damage.parts"].append(r20["data"]["Damage Type"].lower())
    if "Secondary Damage" in K:
        foundryData["damage.parts"] += [
            r20["data"]["Secondary Damage"]
        ]
        if "Secondary Damage Type" in K:
            foundryData["damage.parts"].append(r20["data"]["Secondary Damage Type"].lower())
    if "Save Success" in K:
        foundryFlags["midiProperties.halfdam"] = True
        foundryData["actionType"] = "save"
    elif "spellAttack" in data["spell"][i].keys():
        foundryData["actionType"] = data["spell"][i]["spellAttack"][0].lower() + "sak"
    else:
        foundryData["actionType"] = "util"
    if "Higher Spell Slot Die" in K:
        foundryData["scaling.mode"] = "level"
        foundryData["scaling.formula"] = r20["data"]["Higher Spell Slot Die"]
    elif "data-Cantrip Scaling" in K:
        foundryData["scaling.mode"] = "cantrip"
        foundryData["scaling.formula"] = r20["data"]["Damage"]
    data["spell"][i]["foundryData"] = foundryData
    if foundryFlags != {}:
        data["spell"][i]["foundryFlags"] = foundryFlags
        
with open(name, 'w') as f:
    json.dump(data, f, indent=4)

    
name = "helianas-guide-to-spell.json"
with open(name, 'r') as f:
    data = json.load(f)
h = time()
data["_meta"]["dateLastModified"] = round(h)

for s in data["spell"]:
    print(s["name"])
    if "damage.parts" in s["foundryData"].keys():
        for i, d in enumerate(s["foundryData"].pop("damage.parts")):
            for j, t in enumerate(d):
                s["foundryData"][f"damage.parts.{i}.{j}"] = t
        
with open(name, 'w') as f:
    json.dump(data, f, indent=4)