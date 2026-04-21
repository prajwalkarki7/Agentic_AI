import os
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy import Boolean, create_engine, Column, Integer, String, select

# 1. Database Setup (Outside the class)
class Base(DeclarativeBase):
    pass

class TODO(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True,autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    completed = Column(Boolean, default=False)


# Initialize Engine and Session
engine = create_engine("sqlite:///todos.db")
Base.metadata.create_all(engine)
session = Session(engine)

def main():
    while True:
        todo_list = session.query(TODO).all()
        
        print("\n--- TODO List ---")
        if not todo_list:
            print("List is empty.")
        for idx, todo in enumerate(todo_list, 1):
            print(f"{idx}. {todo}")
        
        print("\nOptions: Add  Complete  Exit")
        choice = input("Choose an option: ")
        
        if choice == "1":
            t = input("Title: ")
            d = input("Description: ")
            new_todo = TODO(title=t, description=d)
            session.add(new_todo)
            session.commit() # Saves to DB
            
        elif choice == "2":
         target_title = input("Enter the EXACT title of the TODO to complete: ")
        
         todo_to_update = session.query(TODO).filter(TODO.title == target_title).first()
        
         if todo_to_update:
            todo_to_update.completed = True
            session.commit()
            print(f"Success! ' is now marked as completed.")
         else:
            print(f"Error: No TODO found with the title '{target_title}'.")

        elif choice == "3":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()