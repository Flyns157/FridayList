import sys
from . import read_json_file, add_to_history, intelligent_selection

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <nombre_n>")
        sys.exit(1)
    
    dishes = add_to_history(
        intelligent_selection(
            nb = sys.argv[1]
        )
    )
    
    print(f"Voici {len(dishes)} plats choisis:", *dishes, sep='\n')

if __name__ == "__main__":
    main()
