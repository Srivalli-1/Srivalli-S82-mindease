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

def chat():
    api_url, api_key, model = load_api_config()
    print("✅ Stop Sequence AI is running inside the virtual environment!")
    print("Start chatting with Gemini! Type 'exit' to quit.")

    system_instructions = (
        "You are a helpful assistant that responds concisely. "
        "Stop generating text when you encounter the sequence '<END>'."
    )

    try:
        while True:
            user_input = input("User: ")
            if user_input.lower() in ("exit", "quit"):
                print("Goodbye!")
                break

            payload = {
                "model": model,
                "temperature": 0.7,
                "candidate_count": 1,
                "stop_sequences": ["<END>"],  # Define the stop sequence
                "prompt": {
                    "messages": [
                        {"author": "system", "content": [{"type": "text", "text": system_instructions}]},
                        {"author": "user", "content": [{"type": "text", "text": user_input}]}
                    ]
                }
            }

            headers = {
                "Content-Type": "application/json",
                "X-goog-api-key": api_key
            }

            try:
                response = requests.post(api_url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                
                # Extract and display the reply
                reply = data["candidates"][0]["content"][0]["text"]
                print("Gemini:", reply)
            except Exception as e:
                print("Error communicating with Gemini:", e)

    except KeyboardInterrupt:
        print("\nGoodbye! (interrupted)")

if __name__ == "__main__":
    chat()