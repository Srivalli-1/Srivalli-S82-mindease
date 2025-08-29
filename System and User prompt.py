import os
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
    Chat function with System and User prompts based on RTFC framework.
    """
    api_url, api_key, model = load_api_config()
    print("✅ System and User Prompt AI is running inside the virtual environment!")
    print("Start chatting with Gemini! Type 'exit' to quit.")

    # System Prompt (RTFC Framework)
    system_prompt = (
        "Role: You are an empathetic AI assistant.\n"
        "Task: Provide emotional support and suggest coping strategies based on user input.\n"
        "Format: Respond concisely and include suggestions for resources when appropriate.\n"
        "Context: The user may express emotions like sadness, anxiety, or happiness. "
        "Detect the sentiment and respond accordingly."
    )

    try:
        while True:
            user_input = input("User: ")
            if user_input.lower() in ("exit", "quit"):
                print("Goodbye!")
                break

            # User Prompt
            user_prompt = f"System: {system_prompt}\nUser: {user_input}"

            payload = {
                "model": model,
                "temperature": 0.7,
                "candidate_count": 1,
                "prompt": {
                    "messages": [
                        {"author": "system", "content": [{"type": "text", "text": system_prompt}]},
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
                reply = data["candidates"][0]["content"][0]["text"]
                print("Gemini:", reply)
            except Exception as e:
                print("Error communicating with Gemini:", e)

    except KeyboardInterrupt:
        print("\nGoodbye! (interrupted)")

if __name__ == "__main__":
    chat()