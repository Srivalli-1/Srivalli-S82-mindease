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
    api_url = f"https://generativelanguage.googleapis.com/{api_version}/models/{model}:generateContent"
    return api_url, api_key, model

def chat():
    """
    Chat function with One-Shot Prompting.
    """
    api_url, api_key, model = load_api_config()
    print("✅ One-Shot Prompting AI is running inside the virtual environment!")
    print("Start chatting with Gemini! Type 'exit' to quit.")

    # One-Shot Prompt Example
    one_shot_prompt = (
        "You are an empathetic assistant. Respond to the user in a concise and supportive manner.\n"
        "Example:\n"
        "User: I feel overwhelmed with work.\n"
        "Assistant: I'm sorry to hear that. Taking short breaks or prioritizing tasks might help. Would you like more tips?\n"
    )

    try:
        while True:
            user_input = input("User: ")
            if user_input.lower() in ("exit", "quit"):
                print("Goodbye!")
                break

            # Combine One-Shot Prompt with User Input
            full_prompt = f"{one_shot_prompt}\nUser: {user_input}"

            payload = {
                "model": model,
                "temperature": 0.7,
                "candidate_count": 1,
                "prompt": {
                    "messages": [
                        {"author": "system", "content": [{"type": "text", "text": full_prompt}]}
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
                reply = data["candidates"][0]["content"][0]["text"]
                print("Assistant:", reply)
            except Exception as e:
                print("Error communicating with Gemini:", e)

    except KeyboardInterrupt:
        print("\nGoodbye! (interrupted)")

if __name__ == "__main__":
    chat()