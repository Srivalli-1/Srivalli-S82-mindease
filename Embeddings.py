import os
import requests
from dotenv import load_dotenv

def load_api_config():
    """
    Load API configuration from environment variables.
    """
    load_dotenv()
    api_key = os.getenv("GENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("GENAI_API_KEY environment variable not set.")
    model = os.getenv("GEMINI_MODEL") or "gemini-1.5-flash"
    api_version = os.getenv("GEMINI_API_VERSION") or "v1beta"
    api_url = f"https://generativelanguage.googleapis.com/{api_version}/models/{model}:embedText"
    return api_url, api_key, model

def generate_embeddings(text):
    """
    Generate embeddings for the given text using the AI model.
    """
    api_url, api_key, model = load_api_config()

    payload = {
        "model": model,
        "text": text
    }

    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": api_key
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        embeddings = data.get("embedding", {}).get("vector", [])
        return embeddings
    except Exception as e:
        print("Error generating embeddings:", e)
        return None

def main():
    """
    Main function to demonstrate embedding generation.
    """
    print("✅ Embeddings.py is running inside the virtual environment!")
    print("Type 'exit' to quit.")

    try:
        while True:
            user_input = input("Enter text to generate embeddings (or type 'exit' to quit): ")
            if user_input.lower() == "exit":
                print("Goodbye!")
                break

            embeddings = generate_embeddings(user_input)
            if embeddings:
                print(f"Generated Embeddings for '{user_input}':")
                print(embeddings)
            else:
                print("Failed to generate embeddings.")

    except KeyboardInterrupt:
        print("\nGoodbye! (interrupted)")

if __name__ == "__main__":
    main()