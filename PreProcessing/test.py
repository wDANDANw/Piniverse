from ner import parse_entities_standalone

# Which input to run the test on - change as needed
test_number = 7

# Assorted text inputs to test on - add more as needed
texts = [
  #0
  "There is four chair red laquer dining set shown in the image. There are opened white french doors leading " \
  "to the outside showing. There is a pool with blue water showing through the french doors of The Indian Space Research Organisation. The pools is " \
  "surrounded by green shrubbery.	The wood floor is covered with white paint. ",

  "There is a large Audi. The Audi has two yellow seats in it. Jamie owns the audi. Jamie was large. He will be cool. " \
  "Jamie has a green hat. It is on his head. The thing on his head is tall. A mouse is in the hat. It proceeds to jump hastily. " \
  "A nearby tree is tall. Rock.",

  "the walls are stark white, except for occasional splatters of colorful paint. The entire floor is a ball pit, filled up to at least a foot. There is a door at one end of the room, and a window on the other side with metal prison bars on it.",

  "A tan room with a large rectangular window containing two wooden desks with monitors in the top right and bottom right corner. There's a closet contained towards the top left corner with the door in the bottom left corner. The floor has carpet and there's a printer on top of a filing cabinet in the top middle of the room.",

  "A red towel is on a rack.",

  #5
  "",

  "Sakuri is next to Yuji in class",

  "The golden chandelier is above the table.",

  "",

  "",

  #10
  "",
]



# Testing code - do not modify
test_txt = texts[test_number]
entities = parse_entities_standalone(test_txt)
print("")
print(test_txt)
print("")
for entity in entities:

  if(len(entity["nouns"]) > 0):
    print("Nouns:")
    for noun in entity["nouns"]:
      print("  ", noun)

  if(len(entity["adjectives"]) > 0):
    print("Adjectives:")
    for adj in entity["adjectives"]:
      print("  ", adj)

  if(len(entity["relations"]) > 0):
    print("Relationships:")
    for rel in entity["relations"]:
      print("  ", rel["prep"], rel["entity"])

  print("")

print(entities)
print("")
