import os
import pymongo
from pymongo import MongoClient
import json
import os

def geojson_format(m_pruned):
    for result in m_pruned["results"]:
        spatial_data = result["spatial"]
        polygon_geojson = {
            "type": "Polygon",
            "coordinates": spatial_data
        }
        result["spatial"] = polygon_geojson

def ingest(client, db, data, collection_name):
    if collection_name=="pruned":
        data["result"] = data.pop("results")
    for result in data["result"]:
        db[collection_name].insert_one(result)
    if collection_name=="pruned":
        db[collection_name].create_index([("spatial", pymongo.GEOSPHERE)])

def m_ingest(missing_pruned, missing_json):
    mongo_ip=os.getenv("MONGO_IP")
    client = MongoClient(f"mongodb://{mongo_ip}:27017/")
    db = client["opendata-datahighway"]
    directory = "prune"
    geojson_format(missing_pruned)
    ingest(client, db, missing_json, "documents")
    ingest(client, db, missing_pruned, "pruned")