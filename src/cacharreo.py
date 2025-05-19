import xml.etree.ElementTree as ET
import csv

# Nombre del archivo .atom de entrada
archivo_atom = "archivo.atom"
# Nombre del archivo CSV de salida
archivo_csv = "licitaciones.csv"

# Parsear el archivo XML
tree = ET.parse(archivo_atom)
root = tree.getroot()

# Espacio de nombres (ajustar según el XML si es necesario)
namespace = {
    "cbc": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
    "cac": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
    "cac-place-ext": "http://contrataciondelestado.es/codice/ext/2.08/ubl-extensions",
}

# Lista para almacenar los datos procesados
datos = []

# Iterar sobre cada 'entry' en el XML
for entry in root.findall("entry"):
    id_licitacion = entry.findtext("id")
    link = entry.find("link").attrib.get("href", "") if entry.find("link") is not None else ""
    summary = entry.findtext("summary")
    title = entry.findtext("title")
    updated = entry.findtext("updated")

    # Extraer información específica del contrato
    contract_status = entry.find(".//cac-place-ext:ContractFolderStatus", namespace)
    if contract_status is not None:
        contract_id = contract_status.findtext("cbc:ContractFolderID", default="", namespaces=namespace)
        status_code = contract_status.findtext("cbc-place-ext:ContractFolderStatusCode", default="", namespaces=namespace)
        
        # Extraer el órgano de contratación
        party_name = contract_status.findtext(".//cac:PartyName/cbc:Name", default="", namespaces=namespace)
        
        # Extraer el importe total sin impuestos
        budget_amount = contract_status.findtext(".//cac:BudgetAmount/cbc:EstimatedOverallContractAmount", default="", namespaces=namespace)

        # Extraer adjudicatario y monto adjudicado
        winner_name = contract_status.findtext(".//cac:TenderResult/cac:WinningParty/cac:PartyName/cbc:Name", default="", namespaces=namespace)
        awarded_amount = contract_status.findtext(".//cac:TenderResult/cac:AwardedTenderedProject/cac:LegalMonetaryTotal/cbc:TaxExclusiveAmount", default="", namespaces=namespace)

    else:
        contract_id = status_code = party_name = budget_amount = winner_name = awarded_amount = ""

    # Guardar en lista
    datos.append([
        id_licitacion, link, title, updated, contract_id, status_code, 
        party_name, budget_amount, winner_name, awarded_amount
    ])

# Guardar en CSV
with open(archivo_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow(["ID", "Enlace", "Título", "Última actualización", "ID Contrato", "Estado", 
                     "Órgano de Contratación", "Importe Estimado (€)", "Adjudicatario", "Monto Adjudicado (€)"])
    writer.writerows(datos)

print(f"Archivo {archivo_csv} generado con éxito.")
