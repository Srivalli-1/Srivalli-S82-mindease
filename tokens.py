import os
import requests
from dotenv import load_dotenv

def load_api_config():
    load_dotenv()
    api_key = os.getenv("GENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("GENAI_API_KEY environment variable not set.")
    model = os.getenv("GEMINI_MODEL") or "gemini-1.5-flash"
    api_version = os.getenv("GEMINI_API_VERSION") or "v1beta"
    api_url = f"https://generativelanguage.googleapis.com/{api_version}/models/{model}:generateContent"
    return api_url, api_key, model

def count_tokens(text):
    """
    Count the number of tokens in the given text.
    """
    # Simplified token counting (split by spaces)
    return len(text.split())

def chat():
    api_url, api_key, model = load_api_config()
    print("✅ Tokens.py is running inside the virtual environment!")
    print("Start chatting with Gemini! Type 'exit' to quit.")

    system_instructions = "You are a helpful assistant that responds in a friendly and concise style."

    try:
        while True:
            user_input = input("User: ")
            if user_input.lower() in ("exit", "quit"):
                print("Goodbye!")
                break

            payload = {
                "contents": [
                    {"parts": [{"text": f"{system_instructions}\nUser: {user_input}"}]}
                ]
            }

            headers = {
                "Content-Type": "application/json",
                "x-goog-api-key": api_key
            }

            try:
                response = requests.post(api_url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                reply = data["candidates"][0]["content"]["parts"][0]["text"]
                
                # Count tokens
                user_tokens = count_tokens(user_input)
                reply_tokens = count_tokens(reply)
                total_tokens = user_tokens + reply_tokens

                print("Gemini:", reply)
                print(f"Tokens used: User Input = {user_tokens}, AI Reply = {reply_tokens}, Total = {total_tokens}")
            except Exception as e:
                print("Error communicating with Gemini:", e)

    except KeyboardInterrupt:
        print("\nGoodbye! (interrupted)")

if __name__ == "__main__":
    chat()