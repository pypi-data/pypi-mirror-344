# Denodo Extractor

Denodo offers options to view the data lineage and the corresponding transformations that happen throughout it, but does not allow proper export of these transformations. This package tackles this issue by querying the meta data of this lineage from Denodo and parsing the tree in a depth-first manner to output all transformations. 

## How to make it work? 

An example script is attached below. Input that is required are:

* URL to the server
* port used for connection
* user id 
* password
* database from which you'd like to extract the meta data
* view from which you'd like to extract the meta data

The output is a dictionary that outputs the transformations per field of the view. 

```
from extractor import extractor

def main():
    ex = extractor(URL, PORT, NAME, USER, "my_password")
    print(f"Connection created to {URL}")
    transformations = ex.get_transformations("<database>", "<view>")
    
    for key, value in transformations.items():
        print(key)
        print(value)

if __name__ == "__main__":
    main()
```

Happy coding! :) Feel free to raise any issue or vulnerability that you encounter. 