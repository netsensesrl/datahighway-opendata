import logging
import json
from pymongo import MongoClient
from module.get_package_data import fetch_package_data
from concurrent.futures import ThreadPoolExecutor, as_completed

logging.basicConfig(level=logging.INFO)

def save_to_file(missing_packages):
    final_json = {
        "help": "https://dati.gov.it/opendata/api/3/action/help_show?name=package_search",
        "success": True,
        "count": len(missing_packages),
        "result": missing_packages
    }
    with open(f'json/document.json', 'w') as json_file:
            json.dump(final_json, json_file, indent=2)
    return final_json

def check_name(pl_list, collect_url, mode):
    client =  MongoClient("mongodb://172.20.0.2:27017/")
    db = client['opendata-datahighway']
    collection = db['documents']
    mongo_names = [str(doc['name']) for doc in collection.find({}, {'name': 1})]
    missing_names = []
    missing_packages = []
    for package_name in pl_list:
        if package_name not in mongo_names:
            missing_names.append(package_name)
    if mode == 0:
        for m_name in mongo_names:
            if not m_name in pl_list:
                deleted_id = [doc['id'] for doc in collection.find({'name': m_name}, {'id': 1})]
                deleted_result = db.documents.delete_many({'name': m_name})
                db.pruned.delete_many({'id': deleted_id[0]})
                logging.info(f"{m_name} deleted")
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(fetch_package_data, name_result, collect_url, mode): name_result for name_result in missing_names}
        for future in futures:
            if future.result()!=None:
                result = future.result()
                logging.info(f"{result['name']} added in all_results")
                missing_packages.append(future.result())
    json_missing = save_to_file(missing_packages)
    return json_missing
