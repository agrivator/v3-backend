# database connection file
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv('../../.env')

username = os.getenv('DATABASE_USER_NAME')
password = os.environ.get('DATABASE_PASSWORD')
database = os.environ.get('DATABASE')
print(username)

# database url
# DATABASE_URL = f"postgresql://{username}:{password}@localhost/{database}"
DATABASE_URL = f"postgresql://postgres:admin@localhost/productionDB"

# database engine
engine = create_engine(DATABASE_URL)

# database local session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# base
Base = declarative_base()