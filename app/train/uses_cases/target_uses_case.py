import os
from app.train.services.dataset_service import DataSetService


MODEL_TRAINING_PATH = "collection/"

class TargetUserCase:
    """ caso de uso para del fichero output generado crear un target.json"""
    def execute(self, value,trainFile):
        """ Ejecutar el proceso"""
        outputFile = None
        if value == "train":
            outputFile = "context.json"
        else:
            outputFile = "context.json"

        dataService = DataSetService(os.path.join(MODEL_TRAINING_PATH, outputFile), trainFile)
        dataService.process_collection_to_context()