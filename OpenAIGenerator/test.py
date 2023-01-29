import json
import re, ast

def loads_json(json_str: str):
    # Reference: https://bobbyhadz.com/blog/python-jsondecodeerror-expecting-property-name-enclosed-in-double-quotes
    # Reference: https://stackoverflow.com/a/36599122
    # Issue: Trailing Comma or Single Quote

    return ast.literal_eval(json_str)

# with open("./test_file.txt", "r", encoding="utf-8") as f:
strr = "\nEntities: \nYuji: \nProperties: \nhigh school student \nshy \nquiet \ndedicated \n\nBehaviors: \navoid social interactions \nfocus on studies \naccepted Sakura's invitation to a date \nspent time together \ntold Sakura how he felt \nwent to school dance together \n\nPsychologies: \nhad feelings for Sakura \nwas too shy to confess \nwas overjoyed \nwasn't sure if Sakura felt the same way \nwas devastated when Sakura had to move \nknew their love was true \nwas determined to make it work \n\nSakura: \nProperties: \nbeautiful \noutgoing \ntransfer student \n\nBehaviors: \nmade it her mission to get to know Yuji \nsat next to him in class \nasked Yuji out on a date \nhad a picnic together \nshared a romantic kiss \n\nPsychologies: \nintrigued by Yuji's reserved nature \ndeveloped feelings for Yuji \nwas afraid Yuji didn't feel the same way \ntook matters into her own hands \nwas determined to make it work \nknew their love was true".replace('\\n', '\n').replace('\\t', '\t')

print(strr)

match = re.search("(Entities\:[\s]*)({(.|\n)*})",strr.replace("'", '"')).group(2)

entities = loads_json(match)

print(entities.keys())
print(entities)
print(type(entities))
[print(k, v) for (k, v) in entities.items()]