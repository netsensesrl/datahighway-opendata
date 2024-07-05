import time
import logging
from module.package_list_collect import pl_collect
from module.check_package_list import check_pl
from module.mongo_check_name import check_name
from module.data_prune import prune
from module.mongo_update import m_ingest
from module.count_added import c_add

logging.basicConfig(level=logging.INFO)

def update_routine(url, collect_url, mode):
    logging.info(f"Update routine starting for {url}")
    package_list = pl_collect(url)
    if(check_pl(package_list, url)):
        missing_json = check_name(package_list, collect_url, mode)
        missing_pruned = prune(missing_json)
        m_ingest(missing_pruned, missing_json)
        c_add(missing_json)
    else:
        return None

def main():
    sleep_time = 12 * 60 * 60 # 12 hours
    routines = [
        ("https://www.dati.gov.it/opendata/api/3/action/package_list", "https://www.dati.gov.it/opendata", 0)#test push
        # other ckan sources can be added here
    ]

    while True:
        for url, collect_url, mode in routines:
            update_routine(url, collect_url, mode)
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()