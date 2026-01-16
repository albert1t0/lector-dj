import pytest
import os
import zipfile
from pathlib import Path
from main import DocumentProcessor

@pytest.fixture
def temp_workspace(tmp_path):
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    output_dir = tmp_path / "output"
    temp_dir = tmp_path / "temp"
    return input_dir, output_dir, temp_dir

def test_scan_folder_with_images(temp_workspace):
    input_dir, output_dir, temp_dir = temp_workspace
    (input_dir / "test1.jpg").write_text("dummy content")
    (input_dir / "test2.png").write_text("dummy content")
    (input_dir / "test.txt").write_text("ignore me")
    
    processor = DocumentProcessor(str(input_dir), str(output_dir), str(temp_dir))
    processor.setup_directories()
    files = processor.scan_input()
    
    assert len(files) == 2
    filenames = [f.name for f in files]
    assert "test1.jpg" in filenames
    assert "test2.png" in filenames

def test_secure_zip_extraction(temp_workspace, tmp_path):
    input_dir, output_dir, temp_dir = temp_workspace
    
    # Create a zip file
    zip_path = input_dir / "docs.zip"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.writestr("doc1.pdf", "dummy pdf")
        zipf.writestr("subfolder/doc2.jpg", "dummy jpg") # basenaming logic in main.py will put this in root of temp_dir
        
    processor = DocumentProcessor(str(zip_path), str(output_dir), str(temp_dir))
    processor.setup_directories()
    files = processor.scan_input()
    
    assert len(files) == 2
    filenames = [f.name for f in files]
    assert "doc1.pdf" in filenames
    assert "doc2.jpg" in filenames
    assert all(f.parent == temp_dir for f in files)

def test_zip_slip_prevention(temp_workspace):
    input_dir, output_dir, temp_dir = temp_workspace
    zip_path = input_dir / "malicious.zip"
    
    # We can't easily create a path traversal in zip with zipfile without hacking
    # but our code uses os.path.basename which effectively neutralizes it.
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.writestr("../evil.txt", "evil")
        
    processor = DocumentProcessor(str(zip_path), str(output_dir), str(temp_dir))
    processor.setup_directories()
    files = processor.scan_input()
    
    # "evil.txt" should be saved as "evil.txt" inside temp_dir, not outside
    assert len(files) == 1
    assert files[0].name == "evil.txt"
    assert files[0].parent == temp_dir
    assert os.path.exists(temp_dir / "evil.txt")
    assert not os.path.exists(temp_dir.parent / "evil.txt")
