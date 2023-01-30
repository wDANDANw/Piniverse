import json
import re, ast

def loads_json(json_str: str):
    # Reference: https://bobbyhadz.com/blog/python-jsondecodeerror-expecting-property-name-enclosed-in-double-quotes
    # Reference: https://stackoverflow.com/a/36599122
    # Issue: Trailing Comma or Single Quote

    return ast.literal_eval(json_str)

# with open("./test_file.txt", "r", encoding="utf-8") as f:
strr = "Gathering at the Park (\u03c11)\t\t{ If(compare(location, \"Local Park\", equal)) \u2192 Do(play(sport, [\"frisbee\", \"soccer\"])) \u2227 Do(update(motive, \"enjoy the picnic\"))}\nPlaying Sports (\u03c12)\t\t{ If(collide(sport)) \u2192 Do(update(sport, [\"frisbee\", \"soccer\"]))}\nGrilling Burgers (\u03c13)\t\t{ If(compare(action, \"grilling\", equal)) \u2192 Do(update(action, \"grilling burgers\"))}\nTheft (\u03c14)\t\t\t{ If(compare(animal.kind, \"mischievous\", equal)) \u2192 Do(steal(item, \"bun\")) \u2227 Do(update(fear, \"being caught by the friends\"))}\nChasing after the Squirrel (\u03c15)\t{ If(compare(action, \"chasing\", equal)) \u2192 Do(update(action, \"chasing after the squirrel\"))}".replace('\\n', '\n').replace('\\t', '\t')

print(strr)

match = re.search("(Entities\:[\s]*)({(.|\n)*})",strr.replace("'", '"')).group(2)

entities = loads_json(match)

print(entities.keys())
print(entities)
print(type(entities))
[print(k, v) for (k, v) in entities.items()]