from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, create_engine

engine = create_engine("postgres connection string")

def get_session():
    with Session(engine) as session:
        yield session

Database = Annotated[Session, Depends(get_session)]