# config.py
import os
import importlib.resources

DB_NAME = os.getenv("DB_NAME", "mimu_geo_data_public.db")
HIERARCHY_LEVEL = os.getenv("HIERARCHY_LEVEL", ["state", "district_saz", "township", "town", "ward", "village_tract", "village"])
THRESHOLD = int(os.getenv("THRESHOLD", 75))  

def get_database_path():
    try:
        db_resource = importlib.resources.files("mm_geo_coder.data").joinpath(DB_NAME)
        with importlib.resources.as_file(db_resource) as path:
            return str(path)
    except FileNotFoundError:
        raise RuntimeError(f"Database file '{DB_NAME}' not found in package.")


