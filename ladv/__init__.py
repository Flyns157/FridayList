import json
import random
from pathlib import Path
from copy import copy
from datetime import datetime

HISTORY_FILE = "history.json"

type Selection = list[str]
type History = dict[str, Selection]
type Dish = str | dict[str, str|list[str]]
type DishList = list[Dish]

class PositiveInteger(int):
    def __new__(cls, value):
        if int(value) <= 0:
            raise ValueError("L'entier doit être strictement positif.")
        return super().__new__(cls, value)

    def __repr__(self):
        return f"PositiveInteger({int(self)})"


def read_json_file(file_path: Path | str)-> dict:
    """
    Lit un fichier JSON et retourne le contenu sous forme de dictionnaire.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def write_json_file(file_path: Path | str, data: dict)-> None:
    """
    Ecrit le contenu d'un dictionnaire dans un fichier JSON.
    """
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def add_to_history(dishes_selection: Selection) -> Selection:
    """
    Ajoute la sélection des plats à l'historique.
    """
    data = read_json_file(HISTORY_FILE)
    data[datetime.now()] = dishes_selection #.strftime("%Y-%m-%d %H:%M:%S")
    write_json_file(HISTORY_FILE, data)
    return dishes_selection

def random_selection(dishes : list[str] | DishList, nb : PositiveInteger, can_repeate : bool = False) -> Selection:
    """
    Retourne une sélection aléatoire de nb plats de la liste des plats donnée.
    Si can_repeate est True, la sélection peut contenir des plats en double.
    """
    nb = PositiveInteger(nb)
    if isinstance(dishes[0], dict):
        dishes = [dish['name'] for dish in dishes]
    if len(dishes) ==0:
        raise ValueError("La liste des plats est vide.")
    tmp = []
    N = len(dishes)
    if nb > N:
        if can_repeate:
            tmp = copy(dishes)*(N//nb)
            nb = N%nb
        else:
            raise ValueError(f"Le nombre demandé ({N}) est supérieur au nombre total de plats disponibles ({N}). Affichage de tous les plats.")
    tmp += random.sample(dishes, nb)
    return tmp

def intelligent_selection(dishes : DishList, nb : PositiveInteger) -> Selection:
    """
    Retourne une sélection intelligente de nb plats de la liste des plats donnée.
    """
    nb = PositiveInteger(nb)
    history = read_json_file(HISTORY_FILE)
    most_recent_selection = history[list(history.keys())[-1]] or []
    valable_dishes = [dish for dish in dishes if dish['name'] not in most_recent_selection]
    # requirements:
    # - avoid repeating dishes
    # - have a minimum of 1 element of each category
    # - have a minimum of 1 element of each preparation method

    dishes_by_category = {}
    for dish in valable_dishes:
        if dish['category'] not in dishes_by_category:
            dishes_by_category[dish['category']] = []
        dishes_by_category[dish['category']].append(dish['name'])
    
    selection: Selection = []
    nb_categories = len(dishes_by_category)
    for category, dishes in dishes_by_category.items():
        if len(selection) >= nb:
            break
        nb_category = min(nb - len(selection), len(dishes))
        selection += random.sample(dishes, nb_category)
        
    print(selection)
    # temporary solution:
    return random_selection(valable_dishes, nb)
