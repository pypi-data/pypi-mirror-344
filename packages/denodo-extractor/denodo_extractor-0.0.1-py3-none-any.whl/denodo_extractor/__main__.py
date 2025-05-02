from extractor import extractor
import os

def main():
    USER = os.environ.get("denodo_server_uid")
    URL = os.environ.get("denodo_server_name")
    NAME = os.environ.get("denodo_database_name")
    PORT = os.environ.get("denodo_server_port")
    ex = extractor(URL, PORT, NAME, USER, "blablabla")
    print(f"Connection created to {URL}")
    transformations = ex.get_transformations("wrfm_ws1", "iv_UC23_G_GOM")
    
    for key, value in transformations.items():
        print(key)
        print(value)

if __name__ == "__main__":
    main()