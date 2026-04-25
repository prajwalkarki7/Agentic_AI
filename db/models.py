from datetime import datetime
from sqlalchemy import String, DateTime, Boolean,func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Todo(Base):
    __tablename__ = 'user_queries'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[String] = mapped_column(String)  # Your input
    description:Mapped[String] = mapped_column(String)
    done: Mapped[bool]= mapped_column(Boolean,default=False)
    created_at: Mapped[DateTime]= mapped_column(DateTime, server_default=func.now())

    def to_dict(self) ->None:
        return{
            "id":self.id,
            "description":self.description,
            "title":self.title,
            "done":self.done,
            "created_at":self.created_at.isoformat(),
        }