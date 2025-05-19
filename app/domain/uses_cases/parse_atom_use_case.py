from app.domain.helper.file_loader import FileLoader
from app.infrastructure.services.atom_service import AtomService



class ParseAtomEntriesUseCase:
    """Caso de uso para parsear un fichero Atom XML y extraer información."""
    def execute(self):
        """Ejecuta el proceso completo de parseo."""
        service = AtomService()
        service.process_atom_files_to_json()





