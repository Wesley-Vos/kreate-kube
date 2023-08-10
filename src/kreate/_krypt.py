from cryptography.fernet import Fernet
from ruamel.yaml import YAML
import logging

logger = logging.getLogger(__name__)



_krypt_key = None
_dekrypt_testdummy = False

def dekrypt_str(value):
    f = Fernet(_krypt_key)
    if _dekrypt_testdummy:
        return f"testdummy-{value[len(value)//2-4:len(value)//2+4]}"
    return f.decrypt(value.encode("ascii")).decode("ascii")

def enkrypt_str(value):
    f = Fernet(_krypt_key)
    part = b'\xbd\xc0,\x16\x87\xd7G\xb5\xe5\xcc\xdb\xf9\x07\xaf\xa0\xfa'
    # use the parts to prevent changes if secret was not changed
    return f._encrypt_from_parts(value.encode("ascii"), 0, part).decode("ascii")



def change_yaml_comments( filename: str, func, from_: str, to_ :str, dir: str = None):
    dir = dir or "."
    yaml_parser = YAML()
    yaml_parser.width=4096 # prevent line wrapping
    yaml_parser.preserve_quotes = True
    with open(f"{dir}/{filename}") as f:
        data = f.read()
    yaml = yaml_parser.load(data)
    ca = yaml.ca
    for key in yaml:
        if key in ca.items: # and len(ca.items[key])>2:
            item = yaml[key]
            comment=ca.items[key][2]
            if from_ in comment.value:
                comment.column = 0
                comment.value = " "+comment.value.replace(from_, to_,1)
                yaml[key] = func(item)
                logger.info(f"{to_} {key}")

    with open(f"{dir}/{filename}", 'wb') as f:
        yaml_parser.dump(yaml, f)

def dekrypt_yaml( filename: str, dir: str = None):
    change_yaml_comments(filename, dekrypt_str, "enkrypted", "dekrypted", dir=dir)

def enkrypt_yaml( filename: str, dir: str = None):
    change_yaml_comments(filename, enkrypt_str, "dekrypted", "enkrypted", dir=dir)