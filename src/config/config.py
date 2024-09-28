from pconf import Pconf

Pconf.env(separator="__", to_lower=True)
Pconf.file("src/config/config.json", encoding="json")

config_store = Pconf.get()

def getconfig(key: str) -> str:
    return _get_deep_value(config_store.copy(), key.split(":"))


def _get_deep_value(dictionary, keys):
    for key in keys:
        dictionary = dictionary.get(key, {})
        if not dictionary:  # Stop if the key doesn't exist
            return None
    return dictionary
