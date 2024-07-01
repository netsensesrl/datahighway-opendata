import logging

logging.basicConfig(level=logging.INFO)

def c_add(missing_json):
    if missing_json["count"] > 0:
            logging.info(f"{missing_json['count']} documents added")
    else:
        logging.info("no new documents discovered")