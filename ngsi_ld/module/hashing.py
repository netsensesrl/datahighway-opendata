import hashlib

def hash_string(elem):
    str_bytes = elem.encode('utf-8')
    hash_object = hashlib.md5(str_bytes)

    hash_hex = hash_object.hexdigest()
    
    return hash_hex