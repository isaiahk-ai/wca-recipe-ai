# Recipe Generator with Claude AI
# Developer: Isaiah
# Date: April 29, 2026
# Description: Generates recipes using Anthropic's Claude AI

import anthropic
import json
import os
from dotenv import load_dotenv

# ============================================================
# CONFIGURATION
# ============================================================

# Load environment variables from .env file
load_dotenv()

# Get API key from environment (secure method)
api_key = os.getenv("ANTHROPIC_API_KEY")

# Check if API key exists
if not api_key:
    print("\n" + "="*60)
    print("❌ ERROR: API Key Not Found")
    print("="*60)
    print("\nPlease create a .env file in your project folder with:")
    print("ANTHROPIC_API_KEY=your-actual-api-key-here")
    print("\nSteps:")
    print("1. Create a file named '.env' (with the dot)")
    print("2. Add the line above with your real API key")
    print("3. Save the file")
    print("4. Run this program again")
    print("\n" + "="*60 + "\n")
    exit(1)

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=api_key)


# ============================================================
# FUNCTIONS
# ============================================================

def build_prompt(dish, people, preference):
    """
    Build the AI prompt using R-T-C-C-O framework
    
    R - Role: Professional chef
    T - Task: Create a recipe
    C - Context: Specific dish, servings, and preferences
    C - Constraints: Return only JSON format
    O - Output: Structured JSON with dish, time, ingredients, steps
    
    Args:
        dish (str): The dish to cook (e.g., "pilau")
        people (str): Number of people (e.g., "4")
        preference (str): Dietary preference (e.g., "spicy")
    
    Returns:
        str: The complete prompt for Claude
    """
    
    prompt = f"""You are a professional chef with expertise in diverse cuisines, particularly East African dishes.

Create a detailed, authentic recipe for {dish} that serves {people} people with {preference} preference.

IMPORTANT: Return ONLY valid JSON in this exact format (no extra text, no markdown, no code blocks):

{{
  "dish": "name of the dish",
  "time": "estimated cooking time (e.g., 45 minutes)",
  "ingredients": [
    "ingredient 1 with specific amount (e.g., 2 cups basmati rice)",
    "ingredient 2 with specific amount",
    "ingredient 3 with specific amount"
  ],
  "steps": [
    "Detailed step 1 instruction",
    "Detailed step 2 instruction",
    "Detailed step 3 instruction"
  ]
}}

Make the recipe:
- Authentic and traditional
- Practical with easily available ingredients
- Clear and easy to follow
- Include at least 6-10 ingredients
- Include at least 6-10 detailed steps

Return ONLY the JSON, nothing else."""

    return prompt


def get_recipe(dish, people, preference):
    """
    Call Claude API to generate a recipe
    
    This function:
    1. Builds the prompt
    2. Sends request to Claude API
    3. Receives and cleans the response
    4. Parses JSON
    5. Returns recipe data or error
    
    Args:
        dish (str): The dish name
        people (str): Number of servings
        preference (str): Dietary preferences
    
    Returns:
        dict: Recipe data with keys: dish, time, ingredients, steps
              OR error dict with key: error
    """
    
    try:
        # Build the prompt using R-T-C-C-O framework
        prompt = build_prompt(dish, people, preference)
        
        # Call Claude API
        response = client.messages.create(
            model="claude-sonnet-4-20250514",  # Latest Claude model
            max_tokens=1500,                    # Allow longer recipes
            temperature=0.7,                    # Some creativity, but consistent
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        # Extract the response text
        text = response.content[0].text
        
        # Clean up the response
        # Remove markdown code blocks if present
        text = text.strip()
        
        # Remove ```json and ``` markers
        if "```json" in text:
            text = text.replace("```json", "")
        if "```" in text:
            text = text.replace("```", "")
        
        # Remove any leading/trailing whitespace
        text = text.strip()
        
        # Parse JSON
        recipe_data = json.loads(text)
        
        # Validate that we have the expected fields
        required_fields = ["dish", "time", "ingredients", "steps"]
        for field in required_fields:
            if field not in recipe_data:
                return {
                    "error": f"Recipe missing required field: {field}",
                    "raw_response": text
                }
        
        return recipe_data
        
    except json.JSONDecodeError as e:
        # JSON parsing failed
        return {
            "error": f"Failed to parse recipe as JSON: {str(e)}",
            "raw_response": text if 'text' in locals() else "No response received"
        }
    
    except anthropic.APIError as e:
        # Anthropic API specific errors
        return {
            "error": f"API Error: {str(e)}",
            "details": "Check your API key and internet connection"
        }
    
    except Exception as e:
        # Any other unexpected errors
        return {
            "error": f"Unexpected error: {str(e)}",
            "type": type(e).__name__
        }


def display_recipe(data):
    """
    Display the recipe in a nice formatted way
    
    Args:
        data (dict): Recipe data from Claude with keys:
                     - dish: name of the dish
                     - time: cooking time
                     - ingredients: list of ingredients
                     - steps: list of cooking steps
    """
    
    # Header
    print("\n" + "="*60)
    dish_name = data.get('dish', 'Unknown Dish')
    print(f"🍽️  RECIPE: {dish_name.upper()}")
    print("="*60)
    
    # Cooking time
    cooking_time = data.get('time', 'Not specified')
    print(f"\n⏱️  Cooking Time: {cooking_time}")
    
    # Ingredients section
    print(f"\n📝 INGREDIENTS:")
    print("-"*60)
    ingredients = data.get('ingredients', [])
    
    if ingredients:
        for i, ingredient in enumerate(ingredients, 1):
            print(f"  {i}. {ingredient}")
    else:
        print("  No ingredients listed")
    
    # Steps section
    print(f"\n👨‍🍳 COOKING STEPS:")
    print("-"*60)
    steps = data.get('steps', [])
    
    if steps:
        for n, step in enumerate(steps, 1):
            print(f"\n  Step {n}:")
            print(f"  {step}")
    else:
        print("  No steps provided")
    
    # Footer
    print("\n" + "="*60)
    print("🍽️  Enjoy your meal! Happy cooking!")
    print("="*60 + "\n")


def main():
    """
    Main program loop
    
    This function:
    1. Displays welcome message
    2. Gets user input for dish, servings, preference
    3. Calls get_recipe() to generate recipe
    4. Displays the recipe or error
    5. Asks if user wants to generate another recipe
    6. Loops until user quits
    """
    
    # Welcome message
    print("\n" + "="*60)
    print("🍳 RECIPE GENERATOR WITH CLAUDE AI 🍳")
    print("="*60)
    print("\nWelcome! Let's create delicious recipes together.")
    print("\nPowered by Anthropic's Claude AI")
    print("="*60 + "\n")
    
    # Main loop - allows generating multiple recipes
    while True:
        # Get user inputs
        print("-"*60)
        
        # Get dish name
        dish = input("What dish do you want to make? ").strip()
        
        # Validate dish input
        if not dish:
            print("❌ Please enter a dish name!")
            continue
        
        # Get number of people
        people = input("How many people (servings)? ").strip()
        if not people:
            people = "4"  # Default to 4 servings
            print(f"   (Using default: {people} servings)")
        
        # Get dietary preferences
        preference = input("Any preferences (e.g., vegetarian, spicy, mild)? ").strip()
        if not preference:
            preference = "no specific preference"
            print(f"   (Using: {preference})")
        
        print("-"*60)
        
        # Show what user requested
        print(f"\n📋 Generating recipe for:")
        print(f"   Dish: {dish}")
        print(f"   Servings: {people} people")
        print(f"   Preference: {preference}")
        
        print("\n🤔 Cooking up your recipe with AI...")
        print("   (This may take a few seconds...)\n")
        
        # Get recipe from Claude API
        recipe = get_recipe(dish, people, preference)
        
        # Check for errors
        if "error" in recipe:
            # Error occurred
            print("\n" + "="*60)
            print("❌ ERROR OCCURRED")
            print("="*60)
            print(f"\n{recipe['error']}")
            
            # Show additional details if available
            if "details" in recipe:
                print(f"\nDetails: {recipe['details']}")
            
            # Show raw response for debugging
            if "raw_response" in recipe:
                print(f"\n📄 Raw response from AI:")
                print("-"*60)
                print(recipe['raw_response'][:500])  # Show first 500 chars
                if len(recipe['raw_response']) > 500:
                    print("... (truncated)")
                print("-"*60)
        else:
            # Success - display the recipe
            display_recipe(recipe)
        
        # Ask if user wants another recipe
        print("\n" + "-"*60)
        another = input("Generate another recipe? (yes/no): ").strip().lower()
        
        if another not in ['yes', 'y', 'yeah', 'yep']:
            # User wants to quit
            print("\n" + "="*60)
            print("👋 Thanks for using Recipe Generator!")
            print("   Happy cooking and enjoy your meal! 🍽️")
            print("="*60 + "\n")
            break
        
        # Add spacing for next iteration
        print("\n")


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    """
    This runs when the file is executed directly
    (not when imported as a module)
    """
    main()