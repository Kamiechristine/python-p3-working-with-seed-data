import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib.seed import seed_data  # Assuming seed_data is the function to run the seeding
from lib.models import Game  # Import the Game model

# Set up a test database
TEST_DATABASE_URL = "sqlite:///:memory:"  # Use an in-memory SQLite database for testing
engine = create_engine(TEST_DATABASE_URL)
Session = sessionmaker(bind=engine)

@pytest.fixture(scope='module')
def test_session():
    """Create a new database session for a test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    # Create the tables in the database
    from lib.models import Base
    Base.metadata.create_all(bind=engine)

    yield session  # This is where the testing happens

    session.close()
    transaction.rollback()
    connection.close()

def test_seed_data(test_session):
    """Test the seed_data function to ensure it populates the database correctly."""
    # Run the seed function
    seed_data(test_session)  # Call the seeding function with the test session

    # Query the database to check the number of records
    count = test_session.query(Game).count()
    assert count == 3  # Adjust this number based on how many records you expect

    # Check if the records have the expected attributes
    games = test_session.query(Game).all()
    for game in games:
        assert game.title is not None
        assert game.platform is not None
        assert game.genre is not None
        assert game.price is not None
