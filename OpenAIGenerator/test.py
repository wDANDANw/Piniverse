import json
import re, ast

def loads_json(json_str: str):
    # Reference: https://bobbyhadz.com/blog/python-jsondecodeerror-expecting-property-name-enclosed-in-double-quotes
    # Reference: https://stackoverflow.com/a/36599122
    # Issue: Trailing Comma or Single Quote

    return ast.literal_eval(json_str)

with open("./test_file.txt", "r", encoding="utf-8") as f:
    strr = f.read()

    match = re.search("(Entities\:[\s]*)({(.|\n)*})",strr.replace("'", '"')).group(2)

    entities = loads_json(match)

    print(entities.keys())
    print(entities)
    print(type(entities))
    [print(k, v) for (k, v) in entities.items()]