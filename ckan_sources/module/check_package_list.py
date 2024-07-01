import logging

logging.basicConfig(level=logging.INFO)

def check_pl(pl_list, url):
    if pl_list is None:
        logging.error(f"Failed to collect package list from {url}")
        return None
    return pl_list