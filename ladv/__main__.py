import sys
from . import read_json_file, print_random_dishes

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <nombre_n>")
        sys.exit(1)
    
    n = int(sys.argv[1])
    file_path = 'data.json'
    data = read_json_file(file_path)
    dishes = data.get('dishes', [])
    
    if not dishes:
        print("Aucun plat trouvé dans le fichier JSON.")
        sys.exit(1)
    
    print_random_dishes(dishes, n)

if __name__ == "__main__":
    main()
