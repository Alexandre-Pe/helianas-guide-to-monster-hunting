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
    spell["range"] = {
        "type": input('type parmi "special", "point", line", "cube", "cone", "radius", "sphere", "hemisphere", "cylinder": ').strip(),
        "distance": {
            "type": input("type distance (feet, miles, self, plan, sight, ...): "),
            "amount": int(input('amount distance: ').strip())
        }
    }

    print("\nComponents infos")
    spell["components"] = {
        "v": input('v: ').strip().lower() == "true",
        "s": input('s: ').strip().lower() == "true",
        "m": input('m text: ').strip()
    }

    if spell["components"]["m"] == "":
        spell["components"].pop("m")

    print("\nDuration infos")
    spell["duration"] = [
        {
            "type": input('type parmi "timed", "instant", "permanent", "special": ').strip(),
            "duration": {
                "type": input('unité de temps: ').strip(),
                "amount": int(input('quantité unité: ').strip()),
                "upTo": input('upTo ? (True/False): ').strip().lower() == "true"
            },
            "concentration": input('concentration ? (True/False): ').strip().lower() == "true"
        }
    ]

    ## Première partie de la description
    i = input("\nDescription: ").strip()
    entries = []
    while i != '':
        entries.append(fuse(i.split('\n')))
        i = input("Suite description (vide si finie): ").strip()

    ## Abilité spéciale s'il y en a une
    i = input("\nNom Abilité spéciale (vide si aucune): ").strip()
    while i != '':
        text_ability = fuse(input("Texte Abilité spéciale: ").strip().split('\n'))
        entries.append({
            "type": "entries",
			"name": i,
			"entries": [text_ability]
        })
        i = input("Nom Abilité spéciale suivante(vide si finie): ").strip()
    spell["entries"] = entries

    ## À plus haut niveau s'il y a
    i = input("\nAt higher levels (vide si absent): ").strip()
    entriesHigherLevel = []
    if i != '':
        ahl = fuse(i.split('\n')) + '.'
        entriesHigherLevel.append({
            "type": "entries",
			"name": "At Higher Levels",
			"entries": [ahl]
        })
    spell["entriesHigherLevel"] = entriesHigherLevel

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
        "Higher Spell Slot Dice", "Add Casting Modifier", "data-Cantrip Scaling"]
    for field in data_field:
        i = input(f'{field}: ').strip()
        if i != '':
            roll20Spell["data"][field] = i

    if "Damage Type" in roll20Spell["data"].keys():
        spell["damageInflict"] = [roll20Spell["data"]["Damage Type"].lower()]
    if "Save" in roll20Spell["data"].keys():
        spell["savingThrow"] = [roll20Spell["data"]["Save"].lower()]
    if "Spell Attack" in roll20Spell["data"].keys():
        spell["spellAttack"] = [roll20Spell["data"]["Spell Attack"][0].capitalize()]
    
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