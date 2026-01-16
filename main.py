import os
import zipfile
import shutil
import base64
import json
from pathlib import Path
from typing import List, Optional, Dict
import google.generativeai as genai
from PIL import Image
from pdf2image import convert_from_path
from dotenv import load_dotenv

load_dotenv()

class ClassificationAgent:
    def __init__(self, model_name: str = "gemini-1.5-flash"):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.examples_cache: List[Dict] = []

    def load_examples(self, examples_dir: Path):
        """Loads example images from the examples directory for few-shot learning."""
        if not examples_dir.exists():
            return
        
        # Expecting folders inside examples_dir to be the category names
        # e.g., examples/ID/sample1.jpg, examples/Invoice/sample2.png
        for category_dir in examples_dir.iterdir():
            if category_dir.is_dir():
                category = category_dir.name
                for example_file in category_dir.iterdir():
                    if example_file.suffix.lower() in {".jpg", ".jpeg", ".png"}:
                        img = Image.open(example_file)
                        self.examples_cache.append({
                            "role": "user",
                            "parts": [img, f"This is an example of a {category}."]
                        })
                        self.examples_cache.append({
                            "role": "model",
                            "parts": [f"Understood. This is a {category}."]
                        })

    def classify(self, file_path: Path) -> Dict:
        """Classifies a document image using Gemini."""
        img = Image.open(file_path)
        
        prompt = """
        Analyze this document and classify it into one of the following categories:
        - IDENTITY_DOCUMENT (ID, Passport, Driver's License)
        - INVOICE (Bill, Factura)
        - TAX_PAYMENT (Recibo de impuestos, Pago de servicios públicos)
        - PROPERTY_RECORD (Título de propiedad, Registro público)
        - OTHER (If it doesn't fit the above)

        Return a JSON object with:
        {
          "category": "CATEGORY_NAME",
          "confidence": 0.0 to 1.0,
          "reasoning": "Brief explanation of why"
        }
        """

        # Build chat history with examples
        chat = self.model.start_chat(history=self.examples_cache)
        response = chat.send_message([img, prompt])
        
        try:
            # Extract JSON from response (handling potential markdown formatting)
            text = response.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            return json.loads(text)
        except (ValueError, json.JSONDecodeError, IndexError):
            return {
                "category": "UNKNOWN",
                "confidence": 0.0,
                "reasoning": f"Failed to parse response: {response.text}"
            }

class DocumentProcessor:
    def __init__(self, input_path: str, output_path: str, temp_dir: str = "temp_extracted", examples_dir: str = "examples"):
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        self.temp_dir = Path(temp_dir)
        self.examples_dir = Path(examples_dir)
        self.supported_extensions = {".jpg", ".jpeg", ".png", ".pdf"}
        self.agent = None

    def initialize_agent(self):
        self.agent = ClassificationAgent()
        self.agent.load_examples(self.examples_dir)

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

    def convert_pdf_to_images(self, pdf_path: Path) -> List[Path]:
        """Converts each page of a PDF to an image and saves it in temp_dir."""
        try:
            images = convert_from_path(pdf_path)
            output_paths = []
            for i, image in enumerate(images):
                output_filename = f"{pdf_path.stem}_page_{i+1}.jpg"
                output_file_path = self.temp_dir / output_filename
                image.save(output_file_path, "JPEG")
                output_paths.append(output_file_path)
            return output_paths
        except Exception as e:
            print(f"Error converting PDF {pdf_path}: {e}")
            return []

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
        processor.initialize_agent()
        files = processor.scan_input()
        print(f"Found {len(files)} files to process.")
        
        all_results = {}
        for f in files:
            print(f"Processing {f.name}...")
            
            # Prepare a list of images to process for this file
            images_to_process = []
            if f.suffix.lower() == ".pdf":
                print(f" - Converting PDF to images...")
                images_to_process = processor.convert_pdf_to_images(f)
            else:
                images_to_process = [f]

            # Collect results for all images in this file
            file_results = []
            for img_path in images_to_process:
                result = processor.agent.classify(img_path)
                file_results.append(result)
                print(f" - Page/Image Result: {result['category']} ({result['confidence']})")
            
            # Simple logic: if multiple pages, pick the most common or first one?
            # For now, let's just store the list
            all_results[f.name] = file_results

        output_file = Path(args.output) / "results.json"
        with open(output_file, "w") as jf:
            json.dump(all_results, jf, indent=2)
        print(f"\nDone! Results saved to {output_file}")

    finally:
        processor.cleanup()
