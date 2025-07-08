

# Namespace que se usa en el XML
namespaces = {
    'atom': 'http://www.w3.org/2005/Atom',
    'cbc-place-ext': 'urn:dgpe:names:draft:codice-place-ext:schema:xsd:CommonBasicComponents-2',
    'cbc': 'urn:dgpe:names:draft:codice:schema:xsd:CommonBasicComponents-2',
    'cac': 'urn:dgpe:names:draft:codice:schema:xsd:CommonAggregateComponents-2',
    'cac-place-ext': 'urn:dgpe:names:draft:codice-place-ext:schema:xsd:CommonAggregateComponents-2',
    'at': 'http://purl.org/atompub/tombstones/1.0',
    'ns7': 'urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2'
}

class AtomParser:
    """Clase para extraer datos de una entrada Atom XML."""

    @staticmethod
    def parse_entry(root):
        """Extrae información de cada entrada en el XML y lo almacena en una lista JSON."""
        data_list = []
        origen = None
        for link in root.findall("atom:link", namespaces=namespaces): 
            if link.attrib.get('rel') == 'self':
                href = link.attrib['href']
                origen = href.split("/")[-1]

        # Iterar sobre cada 'entry' en el XML
        for entry in root.findall("atom:entry", namespaces=namespaces):    
            data = {}
            title_elem =  entry.find("atom:title", namespaces=namespaces)
            updated_elem =  entry.find("atom:updated", namespaces=namespaces)
            #link_elem = entry.find("atom:link", namespaces=namespaces)
            
            data["origen"] = origen
            data["title"] = title_elem.text.strip() if title_elem is not None else "No disponible"
            data["updated"] = updated_elem.text.strip() if updated_elem is not None else "No disponible"
            #data["link"] = link_elem.get("href") if link_elem is not None else "No disponible"

            # Extraemos los datos de ContractFolderStatus, si existe
            contract_folder_status = entry.find(".//cac-place-ext:ContractFolderStatus", namespaces=namespaces)
            if contract_folder_status is not None:
                contract_folder_id = contract_folder_status.find(".//cbc:ContractFolderID", namespaces=namespaces)
                data["contract_folder_id"] = contract_folder_id.text.strip() if contract_folder_id is not None else "No disponible"
                #print(f"- id del contrato: {contract_folder_id.text.strip()}\n")
                
                # Bloque de la organizacion contratante
                id_plataforma = None
                located_party = contract_folder_status.find(".//cac-place-ext:LocatedContractingParty", namespaces=namespaces)
                #print(f"- located_party {located_party}")
                if located_party is not None:
                    party = located_party.find(".//cac:Party", namespaces=namespaces)
                    if party is not None:
                        partyName = party.find(".//cac:PartyName", namespaces=namespaces)
                        if partyName is not None:
                            name = partyName.find(".//cbc:Name", namespaces=namespaces)
                            if name is not None:
                               data["nombreContratante"] = name.text.strip()
                        contact = party.find(".//cac:Contact", namespaces=namespaces)
                        if contact is not None:
                            telephone = contact.find(".//cbc:Telephone", namespaces=namespaces)
                            if telephone is not None:
                                data["telefono"] = telephone.text.strip()
                            email = contact.find(".//cbc:ElectronicMail", namespaces=namespaces)
                            if email is not None:
                                data["email"] = email.text.strip()
                        for party_identification in party.findall(".//cac:PartyIdentification", namespaces=namespaces):            
                            id_elem = party_identification.find("cbc:ID", namespaces=namespaces)
                            if id_elem is not None and id_elem.get("schemeName") == "ID_PLATAFORMA":
                                id_plataforma = id_elem
                                data["id_plataforma"] = id_plataforma.text.strip()
                                #print(f"- id de plataforma: {id_plataforma.text.strip()}\n")
                                break  # Salir del bucle cuando lo encontramos

                # Si id_plataforma es "123", ignorar esta entrada
                if id_plataforma is None or id_plataforma.text.strip() != "31072730151033":
                    continue       
                #print(f"$$ CABILDO DE TENERIFE")

                #Bloque Procurement Project
                procurement_project = contract_folder_status.find(".//cac:ProcurementProject", namespaces=namespaces)
                type_code = None
                if procurement_project is not None:
                    type_code = procurement_project.find(".//cbc:TypeCode", namespaces = namespaces)
                    sub_type_code = procurement_project.find(".//cbc:SubTypeCode", namespaces=namespaces)
                    data["tipo"] = type_code.text.strip() if type_code is not None else "No disponible"
                    data["subTipo"] = sub_type_code.text.strip() if sub_type_code is not None else "No disponible"
                    #add todos los cpv que puedan existir
                    comodity_code = [
                        code.text.strip() for code in procurement_project.findall(".//cac:RequiredCommodityClassification/cbc:ItemClassificationCode", namespaces=namespaces)
                    ]
                    data["cpvList"] = comodity_code

                    budget_amount = procurement_project.find(".//cac:BudgetAmount", namespaces= namespaces)
                    if budget_amount is not None:
                        overall_amount = budget_amount.find(".//cbc:EstimatedOverallContractAmount",namespaces=namespaces)
                        total_amount = budget_amount.find(".//cbc:TotalAmount",namespaces=namespaces)
                        tax_exclusion = budget_amount.find(".//cbc:TaxExclusiveAmount",namespaces=namespaces)
                        data["montoEstimado"] = overall_amount.text.strip() if overall_amount is not None else "No disponible"
                        data["montoTotal"] = total_amount.text.strip() if total_amount is not None else "No disponible"
                        data["impuestosExcluidos"] = tax_exclusion.text.strip() if tax_exclusion is not None else "No disponible"
                
                #Bloque Procurement Project LOTE
                loteResult = []
                for lote in contract_folder_status.findall(".//cac:ProcurementProjectLot", namespaces=namespaces):
                    lote_json = {}
                    #print("recorre el bucle bien")
                    loteId = lote.find(".//cbc:ID",namespaces=namespaces).text.strip()
                    procurement_project = lote.find(".//cac:ProcurementProject", namespaces=namespaces)
                    #print(f"hace el procrem bien {procurement_project}")
                    lote_json["numero"] = loteId
                    lote_json["Name"] = procurement_project.find(".//cbc:Name",namespaces=namespaces).text.strip()
                    #print("hace el name bien")
                    budget_amount_lote = procurement_project.find(".//cac:BudgetAmount", namespaces= namespaces)
                    if budget_amount_lote is not None:
                        total_amount_lote = budget_amount_lote.find(".//cbc:TotalAmount",namespaces=namespaces)
                        tax_exclusion_lote = budget_amount_lote.find(".//cbc:TaxExclusiveAmount",namespaces=namespaces)
                        lote_json["montoTotal"] = total_amount_lote.text.strip() if total_amount is not None else "No disponible"
                        lote_json["impuestosExcluidos"] = tax_exclusion_lote.text.strip() if tax_exclusion is not None else "No disponible"
                    required_comodity =  lote.find(".//cac:RequiredCommodityClassification",namespaces=namespaces)
                    if required_comodity is not None:
                        items = []
                        for item_clasification in required_comodity.findall(".//cbc:ItemClassificationCode", namespaces=namespaces):
                            items.append(item_clasification.text.strip())
                        lote_json["cpvList"] = items
                    loteResult.append(lote_json)
                data["Lotes"] = loteResult


                #BLOQUE TenderingTerms
                tendering_terms = contract_folder_status.find(".//cac:TenderingTerms", namespaces=namespaces)
                if tendering_terms is not None:
                    funding = tendering_terms.find(".//cbc:FundingProgramCode", namespaces=namespaces)
                    data["programaFinanciacion"] = funding.text.strip() if funding is not None else "No disponible"
                
                # Si type code no es "1" (suministro), ignorar esta entrada
                if type_code.text.strip() != "1":
                    continue       
                #print(f"$$ CABILDO DE TENERIFE")

                # Bloque Legal document Reference
                legal_documentReference = contract_folder_status.find(".//cac:LegalDocumentReference", namespaces=namespaces)
                if legal_documentReference is not None:
                    id_elem = legal_documentReference.find("cbc:ID", namespaces=namespaces)
                    data["legalDocument"] = id_elem.text.strip()
                    #print(f"- nombre documento: {id_elem.text.strip()}\n")
                    atachment = legal_documentReference.find(".//cac:Attachment", namespaces=namespaces)
                    #print(f"- Adjuntos: {atachment}\n")
                    if atachment is not None:
                        external_reference = atachment.find("cac:ExternalReference", namespaces=namespaces)
                        #print(f"- external reference:{external_reference.text.strip()}")
                        if external_reference is not None:
                            uri = external_reference.find("cbc:URI", namespaces=namespaces)
                            data["legalDocumentURI"] = uri.text.strip()
                            #print(f"- url documento: {uri.text.strip()}\n")
        #print(f"$$ Data: {data}")
            # Agregar al listado de datos
            data_list.append(data)     
        #print(f"📌 Data List en process_entries: {data_list}")  # Debugging
        return data_list  # 🔥 Asegurar que devuelve la lista


