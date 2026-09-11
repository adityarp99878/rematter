import os
import uuid
from pathlib import Path
from app.config import get_settings

settings = get_settings()

class StorageService:
    def __init__(self):
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        
    def save_file(self, file_content: bytes, filename: str, material_id: int) -> str:
        ext = os.path.splitext(filename)[1]
        unique_name = f"{material_id}_{uuid.uuid4().hex}{ext}"
        filepath = self.upload_dir / unique_name
        with open(filepath, "wb") as f:
            f.write(file_content)
        return f"/uploads/{unique_name}"
        
    def get_file_path(self, url: str) -> Path:
        filename = os.path.basename(url)
        return self.upload_dir / filename
        
    def delete_file(self, url: str):
        filepath = self.get_file_path(url)
        if filepath.exists():
            filepath.unlink()
