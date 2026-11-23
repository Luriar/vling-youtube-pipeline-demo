"""Seed a local SQLite database with fictional records only."""
import argparse
import json
from pathlib import Path
from pipeline import connect,load_fixture

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--db",default="synthetic_warehouse.sqlite")
    p.add_argument("--input",default=str(Path(__file__).parent/"fixtures"/"sample.json"))
    args=p.parse_args()
    db=connect(args.db)
    try:
        print(json.dumps({"stats":load_fixture(db,args.input),"synthetic_only":True},indent=2))
    finally:
        db.close()

if __name__=="__main__":
    main()
