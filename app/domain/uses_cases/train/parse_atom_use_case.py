from app.services.train.atom_service import AtomService



class ParseAtomEntriesUseCase:
    """Caso de uso para parsear un fichero Atom XML y extraer información."""
    def parse_atom_file(self, organization: int, document_type: int):
        """Ejecuta el proceso completo de parseo."""
        print(" ESTY aqui")
        service = AtomService()
        service.process_atom_files_to_json(organization, document_type)





