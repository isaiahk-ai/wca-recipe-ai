# Documentation and Testing: Boniface Karanja
import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

def test_claude_recipe_api():
    """Test Claude API for Recipe Generator"""
    try:
        client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=100,
            messages=[{"role": "user", "content": "Give me 1 Kenyan recipe name only"}]
        )
        print("SUCCESS: Recipe AI connected to Claude")
        print("Test response:", response.content[0].text)
        return True
    except Exception as e:
        print("FAILED: Check ANTHROPIC_API_KEY in.env")
        print("Error:", e)
        return False

if __name__ == "__main__":
    test_claude_recipe_api()
