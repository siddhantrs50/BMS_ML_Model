from sqlalchemy import create_engine
import pandas as pd

DB_URL = "postgresql://postgres:Root22012003@bms-database.c94sysco8nc8.eu-north-1.rds.amazonaws.com:5432/bmsdb"

def fetch_data():
    engine = create_engine(DB_URL)
    query = "SELECT * FROM bms"
    df = pd.read_sql(query, engine)
    return df