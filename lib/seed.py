#!/usr/bin/env python3

from faker import Faker
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lib.models import Game, Base

fake = Faker()

def seed_data(session):
    """Seed the database with sample game data."""
    for _ in range(3):  # Adjust the number of records as needed
        game = Game(
            title=fake.catch_phrase(),
            genre=fake.word(),
            platform=fake.word(),
            price=random.randint(10, 60)
        )
        session.add(game)
    session.commit()

    Base.metadata.create_all(bind=session.bind)  # Create the tables in the database

if __name__ == '__main__':
    
    engine = create_engine('sqlite:///seed_db.db')
    Session = sessionmaker(bind=engine)
    session = Session()
