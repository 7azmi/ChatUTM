from sqlalchemy import create_engine, MetaData

DATABASE_URL = "sqlite:///./chatutm.db"  # Change to PostgreSQL if needed
engine = create_engine(DATABASE_URL)
metadata = MetaData()

def init_db():
    """
    Initializes the database by creating all defined tables.
    
    This function calls the create_all() method on the metadata object, binding it to the engine to ensure that all tables defined in the schema exist in the database. If a table already exists, it will not be recreated.
    """
    metadata.create_all(bind=engine)
