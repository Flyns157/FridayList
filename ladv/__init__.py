import json
import random
from pathlib import Path
from copy import copy
from datetime import datetime
from enum import StrEnum

HISTORY_FILE = "history.json"
DATA_FILE = "data.json"

type DishSelection = list[str]|set[str]|tuple[str]
type History = dict[str, DishSelection]

class Dish(dict):
    class Category(StrEnum):
        MEAT = "meat"
        HOT_STARTER = "hot starter"
        READY_MEAL = "ready meal"
    
    class PreparationMethod(StrEnum):
        MICROWAVE = "microwave"
        OVEN = "oven"
        FRYING_PAN = "frying pan"

    def __new__(cls, name: str, category: 'Dish.Category', preparation_method: list['Dish.PreparationMethod']):
        instance = super().__new__(cls)
        instance.update(
            name=str(name),
            category=category.value if isinstance(category, Dish.Category) else str(category),
            preparation_method=[
                prep.value if isinstance(prep, Dish.PreparationMethod) else str(prep)
                for prep in preparation_method
            ])
        return instance
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Dish':
        return cls(
            name=str(data['name']),
            category=cls.Category(data['category']),
            preparation_method=tuple(data['preparation method'])
        )

    def __repr__(self):
        return f"Dish(name='{self['name']}', category='{self['category'].value}', preparation_method={self['preparation_method']})"

type DishList = list[Dish]|tuple[Dish]

def dishes_by(key: str, dishes: DishList) -> dict[str: DishSelection]:
    """
    Retourne un dictionnaire dont les clés sont les valeurs de la clé donnée et les valeurs sont des listes de noms de plats.
    """
    selection = {}
    for dish in dishes:
        if dish[key] not in selection:
            selection[dish[key]] = []
        selection[dish[key]].append(dish['name'])
    return selection

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

def read_dishesfile()-> DishList:
    """
    Lit un fichier JSON contenant la liste des plats et retourne une liste de Dish.
    """
    data = read_json_file(DATA_FILE)
    return [Dish.from_dict(dish) for dish in data]

def read_history() -> History:
    """
    Lit l'historique des sélections de plats.
    """
    try:
        return read_json_file(HISTORY_FILE)
    except FileNotFoundError:
        with open(HISTORY_FILE, 'w') as file:
            json.dump({}, file)
        return {}

def add_to_history(dishes_selection: DishSelection) -> DishSelection:
    """
    Ajoute la sélection des plats à l'historique.
    """
    data = read_json_file(HISTORY_FILE)
    data[datetime.now().strftime("%d-%m-%Y %H:%M:%S")] = list(dishes_selection)
    write_json_file(HISTORY_FILE, data)
    return dishes_selection

def random_selection(dishes : list[str] | DishList, nb : PositiveInteger, can_repeate : bool = False) -> DishSelection:
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

def intelligent_selection(nb : PositiveInteger) -> DishSelection:
    """
    Retourne une sélection intelligente de nb plats de la liste des plats donnée.
    """
    nb = PositiveInteger(nb)
    history = read_history()
    most_recent_selection = history[list(history.keys())[-1]] if len(history) > 0 else []
    valable_dishes = [
        dish
        for dish in read_dishesfile()
        if dish['name'] not in most_recent_selection
    ]

    # requirements:
    # - avoid repeating dishes
    # - have a minimum of 1 element of each category
    # - have a minimum of 1 element of each preparation method

    dishes_by_category = dishes_by('category', valable_dishes)
    dishes_by_preparation_method = dishes_by('preparation_method', valable_dishes)
    
    selection: DishSelection = set()
    for _, category_dishes in dishes_by_category.items():
        for _, preparation_method_dishes in dishes_by_preparation_method.items():
            if len(selection) >= nb:
                break
            try:
                selection.update(
                    random.sample(
                        list((set(category_dishes) & set(preparation_method_dishes)) - selection),
                        nb//len(dishes_by_category)
                    )
                )
            except ValueError:
                pass
    
    if (nb:=nb - len(selection)) > 0:
        selection.update(random_selection(valable_dishes, nb, can_repeate=True))

    return selection
