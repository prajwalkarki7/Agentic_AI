import os
from dotenv import load_dotenv
from groq import Groq
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy import create_engine, Column, Integer, String, select

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# 1. Updated Table Schema to hold both sides
class Base(DeclarativeBase):
    pass

class UserQuery(Base):
    __tablename__ = 'user_queries'
    id = Column(Integer, primary_key=True)
    user_question = Column(String)  # Your input
    ai_answer = Column(String)      # The full AI response

engine = create_engine("sqlite:///teaching.db")
Base.metadata.create_all(engine)
session = Session(engine)

while True:
    user_input = input("\nYou: ")
    
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting the teaching assistant. Goodbye!")
        break
    
    if user_input.lower() == "tell me about what i learn ?":
        past_queries = session.query(UserQuery).all()
        if past_queries:
            print("\nHere's a summary of what you've learned so far:")
            stmt=select(UserQuery).limit(5)  # Show last 5 interactions
            
            for query in session.scalars(stmt):
                print(f"\nQ: {query.user_question}\nA: {query.ai_answer}\n{'-'*40}")
        else:
            print("\nYou haven't asked any questions yet. Ask something to start learning!")
        continue

    completion = client.chat.completions.create(
        model="groq/compound",
        messages=[
            {"role": "system", "content": "You are a Nepali Teaching Assistant..."},
            {"role": "user", "content": user_input},
        ],
        stream=True,
    )

    full_response = ""
    
    # 2. Accumulate the response in 'full_response'
    for chunk in completion:
        content = chunk.choices[0].delta.content or ""
        print(content, end="", flush=True)
        full_response += content

    if full_response:
        new_entry = UserQuery(
            user_question=user_input, 
            ai_answer=full_response
        )
        session.add(new_entry)
        session.commit() 