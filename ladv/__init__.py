import json
import random

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def print_random_dishes(dishes, n):
    if n > len(dishes):
        print(f"Le nombre demandé ({n}) est supérieur au nombre total de plats disponibles ({len(dishes)}). Affichage de tous les plats.")
        n = len(dishes)
    random_dishes = random.sample(dishes, n)
    for dish in random_dishes:
        print(dish)

