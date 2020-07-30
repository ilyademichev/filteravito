import pyodbc
from sqlalchemy import create_engine
engine = create_engine("access+pyodbc://@your_dsn")
