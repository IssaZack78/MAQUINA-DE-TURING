import json

def save_machine(filename, data):
    """Guarda la configuración de la máquina en un archivo JSON"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_machine(filename):
    """Carga la configuración de la máquina desde un archivo JSON"""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)