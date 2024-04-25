import json

def read_config(path = "../configuration/configuration.json"):
    try:
        with open(path, "r") as fd:
            config = json.load(fd)
        return config
    except Exception as e:
        print(f"Failed to read configuration from {path} due to {e}")

def str_to_list_cvtr(x):
    # print("Debug : ", x)
    try:
        response = list(map(lambda y: float(y), x.replace('[','').replace(']','').split(', ')))
        return response
    except Exception as e:
        print("Error : ", e)
        return x
