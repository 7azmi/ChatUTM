from sqlalchemy import create_engine, MetaData

DATABASE_URL = "sqlite:///./chatutm.db"  # Change to PostgreSQL if needed
engine = create_engine(DATABASE_URL)
metadata = MetaData()

def init_db():
    metadata.create_all(bind=engine)
