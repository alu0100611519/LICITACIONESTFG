import csv

class EpigrafeLoader:
    def __init__(self, filepath):
        self.epigrafes = self._load_csv(filepath)

    def _load_csv(self, filepath):
        epigrafes = {}
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            #print(f"csv file: {filepath}")
            for row in reader:
                epigrafes[row['codigo']] = row['descripcion']
            #print(f"epigrafe: {epigrafes}")
        return epigrafes

    def get_descripcion(self, codigo):
        for full_code, descripcion in self.epigrafes.items():
            #print(f"Full code: {full_code}")
            if full_code.startswith(codigo):
                return f" {full_code}: {descripcion}"
        return "ERROR"

    def all_codigos(self):
        return list(self.epigrafes.keys())
    

    def all_items(self):
        return self.epigrafes.items()
