from dotenv import load_dotenv
from db.session import init_db
from agent import build_agent

load_dotenv()

def main() ->None:
    init_db()
    agent=build_agent()
    print("Welcome to the Nepali Teaching Assistant! Ask me anything about Nepali language, culture, or history. Type 'exit' to quit.")
    while True:
        user_input=input("\nYou: ")
        if user_input.lower() in ["exit","quit"]:
            print("Exiting the teaching assistant. Goodbye!")
            break
        response=agent.run_sync(user_input)
        print(f"\nAI: {response.output}\n")

if __name__=="__main__":
    main()