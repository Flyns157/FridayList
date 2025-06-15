import sys
from . import read_json_file, random_dishes

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <nombre_n>")
        sys.exit(1)
    
    dishes = random_dishes(
        dishes = read_json_file('data.json'),
        nb = sys.argv[1]
    )
    
    print(f"Voici {len(dishes)} plats choisis aléatoirement:", *dishes, sep='\n')

if __name__ == "__main__":
    main()
