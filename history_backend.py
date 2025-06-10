import requests
import json
import os
from dotenv import load_dotenv
import time

# Load API key from .env
load_dotenv()
API_KEY = "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"

def generate_histories(scenario, age_group, historical_role):
    if not API_KEY:
        return "Error: OpenRouter API key not found in .env file.", ""
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    # Customize prompt based on age group and historical role
    if age_group == "Child":
        length = "100-150"
        language = "very simple English a young child can understand, using short sentences and basic words"
    elif age_group == "Teen":
        length = "150-200"
        language = "intermediate English a teenager can understand, with an engaging tone and moderate complexity"
    else:  # Adult
        length = "200-300"
        language = "standard, analytical English suitable for adults"
    
    role_description = {
        "Explorer": "an explorer like Marco Polo, focusing on discovery and adventure",
        "Ruler": "a ruler like Cleopatra, emphasizing leadership and governance",
        "Scientist": "a scientist like Isaac Newton, highlighting innovation and discovery",
        "Philosopher": "a philosopher like Socrates, exploring ideas and wisdom",
        "Warrior": "a warrior like Alexander the Great, focusing on strategy and conquest"
    }
    
    prompt = f"""
    You are a historian acting as {role_description[historical_role]}. The user has provided a 'what if' scenario: '{scenario}'.
    First, briefly summarize what actually happened in history related to this scenario (e.g., the real historical context). Label this section as 'Original History'.
    Then, generate a plausible alternate history based on the 'what if' scenario. Label this section as 'Alternate History'.
    For both parts, keep the language {language}. The 'Original History' should be around 100 words, and the 'Alternate History' should be around {length} words.
    """
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "History Rewriter"
    }
    payload = {
        "model": "deepseek/deepseek-chat:free",
        "messages": [
            {"role": "system", "content": f"You are a historian and {role_description[historical_role]}."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1000,
        "temperature": 0.7
    }
    
    for attempt in range(3):
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            full_narrative = result.get("choices", [{}])[0].get("message", {}).get("content", "No narrative returned.")
            parts = full_narrative.split("Alternate History:")
            if len(parts) >= 2:
                original_history = parts[0].split("Original History:")[1].strip() if "Original History:" in parts[0] else "Unable to extract original history."
                alternate_history = parts[1].strip()
            else:
                original_history = "Unable to extract original history."
                alternate_history = full_narrative.strip()
            return original_history, alternate_history
        except requests.RequestException as e:
            if "429" in str(e):
                time.sleep(2 ** attempt)
                continue
            return f"Error connecting to DeepSeek API: {str(e)}", ""
    return "Error: Too many requests, please try again later.", ""