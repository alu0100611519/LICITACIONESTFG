
import os
import shutil
from fastapi import UploadFile

class TemplateService:
    def __init__(self):
        # Initialize any necessary attributes or services here
        pass

    def upload_template(self, file: UploadFile):
        # Logic to handle template upload
        uri = os.getenv("UPLOAD_FOLDER", "resources/templates")
        file_path = os.path.join(uri, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return file_path;