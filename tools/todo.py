from pydantic_ai import Agent
from db.models import Todo
from db.session import get_session

def register_todo_tools(agent:Agent) ->None:
    @agent.tool_plain
    def create_todo(title:str,description:str="") ->dict:
        """ create a new todo item with a title and a description"""
        with get_session() as session:
            todo=Todo(title=title,description=description)
            session.add(todo)
            session.commit()
            session.refresh(todo)
            return todo.to_dict()
    
    @agent.tool_plain
    def get_todo(todo_id:int) ->dict:
        """get a single todo item by it's id """
        with get_session() as session:
            todo=session.get(Todo,todo_id)
            if not todo:
                return {"error: {todo_id} not found"}
            return todo.to_dict()
    
    @agent.tool_plain
    def get_all_todos(todo_id:int) ->dict:
        """get all the todos """
        with get_session() as session:
            todos=session.query(Todo).all()
            return [todo.to_dict() for todo in todos]

    @agent.tool_plain
    def update_todo(todo_id:int,title:str=None,description:str=None,done:bool=None) ->dict:
        """update a todo item by it's id """
        with get_session() as session:
            todo=session.get(Todo,todo_id)
            if not todo:
                return {"error: {todo_id} not found"}
            if title is not None:
                todo.title=title
            if description is not None:
                todo.description=description
            if done is not None:
                todo.done=done
            session.commit()
            session.refresh(todo)
            return todo.to_dict()
    
    @agent.tool_plain
    def delete_todo(todo_id:int) ->dict:
        """delete a todo item by it's id """
        with get_session() as session:
            todo=session.get(Todo,todo_id)
            if not todo:
                return {"error: {todo_id} not found"}
            session.delete(todo)
            session.commit()
            return {"message: {todo_id} deleted successfully"}
        
