import os
from dotenv import load_dotenv

def load_prompt_templates():
    """
    Load predefined prompt templates for dynamic generation.
    """
    return {
        "greeting": "Hello! How can I assist you today?",
        "emotion_analysis": "You seem {emotion}. Would you like to talk about it?",
        "task_assistance": "What task are you working on? I can help you with {task}.",
        "custom": "{custom_message}"
    }

def generate_prompt(template_name, **kwargs):
    """
    Generate a dynamic prompt based on the template name and provided arguments.
    """
    templates = load_prompt_templates()
    template = templates.get(template_name, "Template not found.")
    return template.format(**kwargs)

def main():
    """
    Main function to demonstrate dynamic prompting.
    """
    load_dotenv()  # Load environment variables if needed

    print("Dynamic Prompting System Initialized!")
    print("Type 'exit' to quit.")

    try:
        while True:
            user_input = input("Enter a template name (e.g., 'greeting', 'emotion_analysis', 'task_assistance', 'custom'): ")
            if user_input.lower() == "exit":
                print("Goodbye!")
                break

            if user_input == "custom":
                custom_message = input("Enter your custom message: ")
                prompt = generate_prompt(user_input, custom_message=custom_message)
            elif user_input == "emotion_analysis":
                emotion = input("Enter an emotion (e.g., happy, sad, anxious): ")
                prompt = generate_prompt(user_input, emotion=emotion)
            elif user_input == "task_assistance":
                task = input("Enter a task (e.g., coding, writing): ")
                prompt = generate_prompt(user_input, task=task)
            else:
                prompt = generate_prompt(user_input)

            print("Generated Prompt:", prompt)

    except KeyboardInterrupt:
        print("\nGoodbye! (interrupted)")

if __name__ == "__main__":
    main()