from src.agents.conversation_agent import ConversationAgent
from src.agents.generator_agent import SentenceGeneratorAgent
from src.agents.grader_agent import GraderAgent
from src.french import FrenchUtils
from src.db import Database

def display_welcome():
    print("=" * 50)
    print("Welcome to your French Tutor!")
    print("=" * 50)
    print("Select a mode:")
    print("1. Conversation Practice")
    print("2. Translation Practice")
    print("3. View Recent Progress")
    print("4. Exit")
    print("=" * 50)

def conversation_mode():
    print("\n--- Conversation Practice Mode ---")
    print("Chat naturally with your French tutor. Type 'exit' to return to the main menu.")
    print("Here are some greetings to start with:")
    
    for eng, fr in FrenchUtils.get_greeting_examples().items():
        print(f"- {eng}: {fr}")
    
    try:
        agent = ConversationAgent()
        
        while True:
            user_input = input("\nYou: ")
            
            if user_input.lower() == 'exit':
                break
            
            response = agent.get_response(user_input)
            print(f"\nTutor: {response}")
    except Exception as e:
        print(f"Error in conversation mode: {e}")
        print("\nMake sure Ollama is running and the selected model is installed.")

def translation_mode():
    print("\n--- Translation Practice Mode ---")
    print("I'll give you English sentences to translate to French.")
    print("Type 'exit' at any time to return to the main menu.")
    
    try:
        generator = SentenceGeneratorAgent()
        grader = GraderAgent()
        db = Database()
        
        # Start a new session
        session_id = db.start_session()
        
        while True:
            # Get difficulty
            print("\nSelect difficulty level:")
            print("1. Beginner")
            print("2. Intermediate")
            print("3. Advanced")
            
            difficulty_choice = input("Choice (1-3): ")
            
            if difficulty_choice.lower() == 'exit':
                break
                
            difficulty_map = {
                '1': 'beginner',
                '2': 'intermediate',
                '3': 'advanced'
            }
            
            difficulty = difficulty_map.get(difficulty_choice, 'beginner')
            
            # Generate a sentence
            sentence_data = generator.generate_sentence(difficulty)
            english = sentence_data["english"]
            correct_french = sentence_data["french"]
            
            print(f"\nTranslate to French: {english}")
            user_translation = input("Your translation: ")
            
            if user_translation.lower() == 'exit':
                break
            
            # Grade the translation
            grade_data = grader.grade_translation(correct_french, user_translation)
            score = grade_data["score"]
            feedback = grade_data["feedback"]
            
            # Display result
            print(f"\nCorrect translation: {correct_french}")
            print(f"Score: {score:.2f}")
            print(f"Feedback: {feedback}")
            
            # Save to database
            db.save_translation_exercise(
                session_id, 
                english, 
                correct_french, 
                user_translation, 
                score, 
                feedback
            )
            
            # Ask to continue
            cont = input("\nContinue with another sentence? (y/n): ")
            if cont.lower() != 'y':
                break
                
        db.close()
    except Exception as e:
        print(f"Error in translation mode: {e}")
        print("\nMake sure Ollama is running and the selected model is installed.")

def view_progress():
    print("\n--- Recent Progress ---")
    try:
        db = Database()
        exercises = db.get_recent_exercises(10)
        
        if not exercises:
            print("No previous exercises found.")
        else:
            print("Your recent translation exercises:")
            for i, ex in enumerate(exercises, 1):
                english, correct, user, score, feedback = ex
                print(f"\n{i}. English: {english}")
                print(f"   Correct French: {correct}")
                print(f"   Your translation: {user}")
                print(f"   Score: {score:.2f}")
                print(f"   Feedback: {feedback}")
                
        db.close()
    except Exception as e:
        print(f"Error viewing progress: {e}")
    
    input("\nPress Enter to return to the main menu...")

def main():
    while True:
        display_welcome()
        choice = input("Enter your choice (1-4): ")
        
        if choice == '1':
            conversation_mode()
        elif choice == '2':
            translation_mode()
        elif choice == '3':
            view_progress()
        elif choice == '4':
            print("Au revoir! (Goodbye!)")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()