from src.agent import FrenchTutorAgent
from src.french import FrenchUtils

def display_welcome():
    print("=" * 50)
    print("Welcome to your French Tutor!")
    print("=" * 50)
    print("I can help you learn French. Type 'exit' to quit.")
    print("Here are some greetings to start with:")
    
    for eng, fr in FrenchUtils.get_greeting_examples().items():
        print(f"- {eng}: {fr}")
    
    print("\nWhat would you like to learn today?")
    print("=" * 50)

def main():
    # Initialize the French tutor agent
    try:
        agent = FrenchTutorAgent()
        
        display_welcome()
        
        while True:
            user_input = input("\nYou: ")
            
            if user_input.lower() == "exit":
                print("Au revoir! (Goodbye!)")
                break
            
            response = agent.get_response(user_input)
            print(f"\nTutor: {response}")
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure Ollama is running and the llama3 model is installed.")
        print("You can install it with: ollama pull llama3")

if __name__ == "__main__":
    main()