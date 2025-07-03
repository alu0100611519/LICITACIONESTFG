import sys 
import uvicorn
from fastapi import FastAPI
from app.train.uses_cases.parse_atom_use_case import ParseAtomEntriesUseCase


# --- Función especial si se ejecuta con "train" ---
def parserAtom():
    use_case = ParseAtomEntriesUseCase()
    use_case.execute()

def ejecutar_atom():
    print("Ejecutando modo ATOM...")
    # Aquí va tu lógica específica

def ejecutar_gemini():
    print("Ejecutando modo GEMINI...")
    # Aquí va tu lógica específica


def iniciar_cli():
    print("CLI Interactivo iniciado. escribe 'exit' para salir.")
    comando = input(">> ").strip()

    while True:
        if comando == "exit":
            print("Saliendo de la CLI...")
            break
        elif comando.startswith("atom"):
            partes = comando.split()
            if len(partes) != 3:
                print("Modo ATOM requiere dos parámetros adicionales.")
                print("Uso: python main.py atom <param1> <param2>")
            organization = int(partes[1])
            document_type = int(partes[2])
            use_case = ParseAtomEntriesUseCase()
            use_case.parse_atom_file(organization, document_type)
        elif comando == "gemini":
            ejecutar_gemini()
        elif comando == "t5":
            print("Ejecutando modo T5...")
            # Aquí va tu lógica específica para T5

def main():
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python main.py atom <param1> <param2>")
        print("  python main.py gemini")
        sys.exit(1)

    modo = sys.argv[1].lower()

    if modo == "cli":
        iniciar_cli()


# --- Punto de entrada del script ---
if __name__ == "__main__":
    main()