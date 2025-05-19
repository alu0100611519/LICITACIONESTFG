import os
import xmltodict
import pandas as pd

def parse_atom_file(file_path):
    """Parsea un archivo .atom y extrae la información relevante."""
    with open(file_path, "r", encoding="utf-8") as file:
        data = xmltodict.parse(file.read())  # Convierte XML a diccionario
    
    entries = data.get("feed", {}).get("entry", [])  # Extrae las entradas del feed
    if not isinstance(entries, list):
        entries = [entries]  # Asegura que siempre sea una lista

    extracted_data = []
    for entry in entries:
        title = entry.get("title", "No Title")
        link = entry.get("link", "No link")
        summary = entry.get("summary", "No summary")
        updated = entry.get("updated", "No update")
        
        extracted_data.append({
            "titulo": title,
            "enlace": link,
            "summary": summary,
            "update": updated

        })

    return extracted_data

def process_atom_files(input_folder, output_file):
    """Procesa múltiples archivos .atom y los guarda en un CSV."""
    all_data = []
    
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".atom"):
            file_path = os.path.join(input_folder, file_name)
            print(f"Procesando: {file_name}")
            all_data.extend(parse_atom_file(file_path))

    df = pd.DataFrame(all_data)
    df.to_csv(output_file, index=False, encoding="utf-8")
    print(f"Datos guardados en {output_file}")


if __name__ == "__main__":
    input_folder = "..\\data"  # Carpeta donde están los archivos .atom
    output_file = "..\\data\\licitaciones.csv"  # Archivo de salida limpio
    process_atom_files(input_folder, output_file)
