import os
import zipfile
import shutil
from pathlib import Path
from typing import List, Optional

class DocumentProcessor:
    def __init__(self, input_path: str, output_path: str, temp_dir: str = "temp_extracted"):
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        self.temp_dir = Path(temp_dir)
        self.supported_extensions = {".jpg", ".jpeg", ".png", ".pdf"}

    def setup_directories(self):
        """Creates necessary directories securely."""
        self.output_path.mkdir(parents=True, exist_ok=True)
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def is_zip_file(self, path: Path) -> bool:
        return path.suffix.lower() == ".zip"

    def extract_zip_securely(self, zip_path: Path) -> List[Path]:
        """Extracts ZIP content while preventing ZipSlip-like vulnerabilities."""
        extracted_files = []
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for member in zip_ref.namelist():
                # Security: Prevent Directory Traversal
                filename = os.path.basename(member)
                if not filename:
                    continue
                
                target_path = self.temp_dir / filename
                
                # Double check path is within temp_dir
                if not str(target_path.resolve()).startswith(str(self.temp_dir.resolve())):
                    continue
                
                with zip_ref.open(member) as source, open(target_path, "wb") as target:
                    shutil.copyfileobj(source, target)
                extracted_files.append(target_path)
        return extracted_files

    def scan_input(self) -> List[Path]:
        """Scans the input path for supported documents or ZIP files."""
        files_to_process = []
        
        if not self.input_path.exists():
            raise FileNotFoundError(f"Input path {self.input_path} does not exist.")

        if self.input_path.is_file():
            if self.is_zip_file(self.input_path):
                files_to_process.extend(self.extract_zip_securely(self.input_path))
            elif self.input_path.suffix.lower() in self.supported_extensions:
                files_to_process.append(self.input_path)
        else:
            for root, _, files in os.walk(self.input_path):
                for file in files:
                    file_path = Path(root) / file
                    if file_path.suffix.lower() in self.supported_extensions:
                        files_to_process.append(file_path)
                    elif self.is_zip_file(file_path):
                        files_to_process.extend(self.extract_zip_securely(file_path))
        
        return files_to_process

    def cleanup(self):
        """Removes temporary files."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Lector-DJ: Document Classifier")
    parser.get_default("input")
    parser.add_argument("--input", required=True, help="Path to folder or ZIP file")
    parser.add_argument("--output", default="output", help="Path to output results")
    args = parser.parse_args()

    processor = DocumentProcessor(args.input, args.output)
    try:
        processor.setup_directories()
        files = processor.scan_input()
        print(f"Found {len(files)} files to process.")
        for f in files:
            print(f" - {f}")
    finally:
        # For now we don't cleanup immediately to see results in this step
        # processor.cleanup()
        pass
