# config.py
import os

DATABASE_PATH = os.getenv("DATABASE_PATH", os.path.join(".", "data"))
DB_NAME = os.getenv("DB_NAME", "mimu_geo_data_public.db")
DB_PATH = os.path.join(DATABASE_PATH, DB_NAME)

HIERARCHY_LEVEL = os.getenv("HIERARCHY_LEVEL", ["state", "district_saz", "township", "town", "ward", "village_tract", "village"])
THRESHOLD = int(os.getenv("THRESHOLD", 75))  
