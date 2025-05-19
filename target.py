import sys
from app.domain.uses_cases.target_uses_case import TargetUserCase

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Debes proporcionar exactamente 2 argumentos.")
        print("Uso: python script.py arg1 arg2")
        sys.exit(1)

    value = sys.argv[1]
    output = sys.argv[2]

    usecase = TargetUserCase()
    usecase.execute(value, output)
