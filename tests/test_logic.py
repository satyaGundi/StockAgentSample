# tests/test_logic.py
from backend.agent import extract_text_content

def test_extractor_simple_string():
    # Tests if our helper handles plain strings
    assert extract_text_content("AAPL is bullish") == "AAPL is bullish"

def test_extractor_list_format():
    # Tests if our helper handles the Gemini list format
    sample_input = [{"type": "text", "text": "Price is 200"}]
    assert extract_text_content(sample_input) == "Price is 200"
