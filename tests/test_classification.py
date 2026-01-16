import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from main import ClassificationAgent, DocumentProcessor
from PIL import Image
import os
import json

@pytest.fixture
def mock_genai():
    with patch("main.genai") as mock:
        yield mock

@pytest.fixture
def agent(mock_genai):
    os.environ["GOOGLE_API_KEY"] = "fake_key"
    return ClassificationAgent()

def test_load_examples(agent, tmp_path):
    # Setup example directory
    examples_dir = tmp_path / "examples"
    id_dir = examples_dir / "ID"
    id_dir.mkdir(parents=True)
    
    # Create dummy image
    img_path = id_dir / "sample.jpg"
    img = Image.new('RGB', (10, 10), color='red')
    img.save(img_path)
    
    agent.load_examples(examples_dir)
    
    # Check if examples were loaded (2 messages per example: user and model)
    assert len(agent.examples_cache) == 2
    assert agent.examples_cache[0]["parts"][1] == "This is an example of a ID."

def test_classify_success(agent, tmp_path, mock_genai):
    # Setup mock response
    mock_response = MagicMock()
    mock_response.text = '```json {"category": "INVOICE", "confidence": 0.95, "reasoning": "Looks like a bill"} ```'
    agent.model.start_chat().send_message.return_value = mock_response
    
    img_path = tmp_path / "test.jpg"
    img = Image.new('RGB', (10, 10), color='blue')
    img.save(img_path)
    
    result = agent.classify(img_path)
    
    assert result["category"] == "INVOICE"
    assert result["confidence"] == 0.95

def test_classify_failure_parsing(agent, tmp_path, mock_genai):
    mock_response = MagicMock()
    mock_response.text = 'This is not JSON'
    agent.model.start_chat().send_message.return_value = mock_response
    
    img_path = tmp_path / "test.jpg"
    img = Image.new('RGB', (10, 10))
    img.save(img_path)
    
    result = agent.classify(img_path)
    
    assert result["category"] == "UNKNOWN"
    assert result["confidence"] == 0.0

def test_document_processor_with_pdf(tmp_path, mock_genai):
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    output_dir = tmp_path / "output"
    
    # We can't easily create a real PDF, but we can mock convert_from_path
    pdf_path = input_dir / "test.pdf"
    pdf_path.write_text("fake pdf")
    
    with patch("main.convert_from_path") as mock_convert:
        mock_img = Image.new('RGB', (10, 10))
        mock_convert.return_value = [mock_img]
        
        with patch("main.ClassificationAgent") as MockAgent:
            mock_agent_instance = MockAgent.return_value
            mock_agent_instance.classify.return_value = {"category": "TAX", "confidence": 0.8}
            
            processor = DocumentProcessor(str(input_dir), str(output_dir))
            processor.setup_directories()
            processor.initialize_agent()
            
            # This would be part of the main loop logic, let's test the method directly
            images = processor.convert_pdf_to_images(pdf_path)
            assert len(images) == 1
            assert "test_page_1.jpg" in images[0].name
            assert images[0].exists()
