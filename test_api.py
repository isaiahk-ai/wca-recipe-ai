# Testing and Documentation: Boniface Karanja
import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

def test_claude_api():
    """Test Claude API connection for Tarrys Beauty Lounge AI"""
    try:
        client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=100,
            messages=[{"role": "user", "content": "Reply with 'API working' if you get this"}]
        )
        print("SUCCESS: API Connected")
        print("Response:", response.content[0].text)
        return True
    except Exception as e:
        print("FAILED: Check API key in.env file")
        print("Error:", e)
        return False

if __name__ == "__main__":
    test_claude_api()
