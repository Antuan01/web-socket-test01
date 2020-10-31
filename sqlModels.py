from sqlalchemy import Boolean, DateTime, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy

Base = declarative_base()

task_todo = Table(
    "tasks_todos",
    Base.metadata,
    Column("author_id", Integer, ForeignKey("author.author_id")),
    Column("publisher_id", Integer, ForeignKey("publisher.publisher_id")),
)

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    date = Column(DateTime, default=func.now())
    author = Column(String)

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    todo_id = Column(Integer, ForeignKey("todos.id"))
    title = Column(String)
    finished = Column(Boolean)
    todos = relationship("Todo", backref=backref("tasks", uselist=True))

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://antuan:nautna@localhost/taskdb'

# Test if it works
engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
print(engine.table_names())
