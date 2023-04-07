from ner import parse_entities_standalone
import random

entities = parse_entities_standalone("The oak log has dark green stuff. The golden chandelier is above the table. The green eye is below the bridge. The grey book is under the table. The trampoline is beside the table.")

# remove every branch that doesn't have a relation
def remove_non_relations(tree):
    new_list = []
    for x in range(len(tree)):
        if len(entities[x]["relations"]) != 0:
            new_list.append(entities[x])
    return new_list

# get trajector from given single branch
def get_trajector(ent_dic):
    return str(ent_dic["nouns"][0])

# get landmark from given single branch
def get_landmark(ent_dic):
    return str(ent_dic["relations"][0]['entity'])

# get spatial indicator from given single branch
def get_spatial_indicator(ent_dic):
    return str(ent_dic["relations"][0]['prep'])

class SceneObject:
    name = ''
    size = []
    location = []

# Get the location of trajector and the landmark. This function assumes that trajector and landmark are SceneObjects that consists of
# a size and a location
# size (w, h, l)
# loc  (x, y, z)
def get_loc(trajector, spatial_indicator, landmark):

    # Initialize the Trajector
    Trajector = SceneObject()
    Trajector.size = [1,1,1]
    Trajector.location = []
    Trajector.name = trajector

    # Initialize the Landmark
    Landmark = SceneObject()
    Landmark.size = [1,1,1]
    Landmark.location = [0, 0, 0]
    Landmark.name = landmark

    trajector_location = Trajector.location
    landmark_location = Landmark.location

    x, y, z = landmark_location[0], landmark_location[1], landmark_location[2]

    if spatial_indicator.lower() == 'on':
        y = Trajector.size[1] / 2 + Landmark.size[1] / 2
        trajector_location = [x, y, z]
        print("Trajector Location: ", trajector_location)
        print("Landmark Location: ", landmark_location)
        return trajector_location, landmark_location

    elif spatial_indicator.lower() == 'above' or spatial_indicator.lower() == 'over' or spatial_indicator.lower() == 'atop':
        y = Trajector.size[1] / 2 + Landmark.size[1] / 2 + 2
        trajector_location = [x, y, z]
        print("Trajector Location: ", trajector_location)
        print("Landmark Location: ", landmark_location)
        return trajector_location, landmark_location

    elif spatial_indicator.lower() == 'behind':
        z = -1 * (Trajector.size[2] / 2 + Landmark.size[2] / 2)
        trajector_location = [x, y, z]
        print("Trajector Location: ", trajector_location)
        print("Landmark Location: ", landmark_location)
        return trajector_location, landmark_location

    elif spatial_indicator.lower() == 'beside' or spatial_indicator.lower() == 'next to':
        # add randomness to pick right or left side
        side = random.randint(0,1)
        # left
        if side == 0:
            x = -1 * (Trajector.size[0] / 2 + Landmark.size[0] / 2)
        # right
        else:
            x = Trajector.size[0] / 2 + Landmark.size[0] / 2
        trajector_location = [x, y, z]
        print("Trajector Location: ", trajector_location)
        print("Landmark Location: ", landmark_location)
        return trajector_location, landmark_location

    elif spatial_indicator.lower() == 'below' or spatial_indicator.lower() == 'under' or spatial_indicator.lower() == 'beneath'\
            or spatial_indicator.lower() == 'underneath':
        y = -1 * (Trajector.size[1] / 2 + Landmark.size[1] / 2 + 2)
        trajector_location = [x, y, z]
        print("Trajector Location: ", trajector_location)
        print("Landmark Location: ", landmark_location)
        return trajector_location, landmark_location

    elif spatial_indicator.lower() == 'in front of':
        z = Trajector.size[2] / 2 + Landmark.size[2] / 2
        trajector_location = [x, y, z]
        print("Trajector Location: ", trajector_location)
        print("Landmark Location: ", landmark_location)
        return trajector_location, landmark_location


    else:
        # add randomness to pick right or left side
        side = random.randint(0, 1)
        # left
        if side == 0:
            x = -1 * (Trajector.size[0] / 2 + Landmark.size[0] / 2)
        # right
        else:
            x = Trajector.size[0] / 2 + Landmark.size[0] / 2
        trajector_location = [x, y, z]
        print("Trajector Location: ", trajector_location)
        print("Landmark Location: ", landmark_location)
        return trajector_location, landmark_location

    # if spatial_indicator.lower() == 'above' or spatial_indicator.lower() == 'over':
    #     trajector_location = []

rel_ents = remove_non_relations(entities)
# print(rel_ents)

print("The Trajector: ", get_trajector(rel_ents[0]))
print("The Spatial Indicator: " + str(get_spatial_indicator(rel_ents[0])))
print("The Landmark: ", get_landmark(rel_ents[0]))

get_loc(get_trajector(rel_ents[0]), get_spatial_indicator(rel_ents[0]), get_landmark(rel_ents[0]))

'''
def add_neighbors(boundary, entity):
    return boundary  # TODO

def remove_entity(boundary, entity):
    return boundary  # TODO

def get_rel_pos(entity, parent):
    return parent["position"]  # TODO

def fill_out_locations(entities):
    if len(entities) == 0: return entities
    cur_ent = entities[0]
    cur_ent["position"] = [0,0,0]
    boundary = add_neighbors([], cur_ent)
    while(len(boundary) > 0):
        cur_ent = boundary[0][0]
        parent = boundary[0][1]
        cur_ent["position"] = get_rel_pos(cur_ent, parent)
        boundary = remove_entity(boundary, cur_ent)
        boundary = add_neighbors(boundary, cur_ent)
'''

def get_rel_pos(parent, child, prep):
    #print("Parent: "+parent["nouns"][0].text+" ("+str(parent["position"])+")")
    si = prep.text.lower()  # spatial indicator
    #print("SI: "+si)

    parent["size"] = [1,1,1]  # TODO: Ensure all elements, not just parents and children, get sizes
    child["size"] = [1,1,1]
    px = parent["position"][0]
    py = parent["position"][1]
    pz = parent["position"][2]
    child_pos = [0,0,0]

    if si == 'on' or si == 'atop':
        dy = child["size"][1] / 2 + parent["size"][1] / 2
        child_pos = [px, py + dy, pz]

    elif si == 'above' or si == 'over':
        dy = child["size"][1] / 2 + parent["size"][1] / 2 + 2
        child_pos = [px, py + dy, pz]

    elif si == 'behind':
        dz = -1 * (child["size"][2] / 2 + parent["size"][2] / 2)
        child_pos = [px, py, pz + dz]

    elif si == 'beside' or si == 'next to':
        dx = 0
        # add randomness to pick right or left side
        side = random.randint(0,1)
        # left
        if side == 0:
            dx = -1 * (child["size"][0] / 2 + parent["size"][0] / 2)
        # right
        else:
            dx = child["size"][0] / 2 + parent["size"][0] / 2
        child_pos = [px + dx, py, pz]

    elif si == 'below' or si == 'under' or si == 'beneath' or si == 'underneath':
        dy = -1 * (child["size"][1] / 2 + parent["size"][1] / 2 + 2)
        child_pos = [px, py + dy, pz]

    elif si == 'in front of':
        dz = child["size"][2] / 2 + parent["size"][2] / 2
        child_pos = [px, py, pz + dz]

    # Default: Place it next to the parent (either side)
    else:
        dx = 0
        # add randomness to pick right or left side
        side = random.randint(0,1)
        # left
        if side == 0:
            dx = -1 * (child["size"][0] / 2 + parent["size"][0] / 2)
        # right
        else:
            dx = child["size"][0] / 2 + parent["size"][0] / 2
        child_pos = [px + dx, py, pz]

    #print("Child: "+child["nouns"][0].text+" ("+str(child_pos)+")")
    return child_pos


def get_entity(noun, entities):
    for entity in entities:
        if noun in entity["nouns"]:
            return entity
    print('Fatal error: No entity found for the given noun')
    return False

def fill_out_child_locations(entity, entities):
    for rel in entity["relations"]:  # If this entity has the relation
        prep = rel["prep"]
        target = get_entity(rel["entity"], entities)
        if("position" not in target.keys()):
            target["position"] = list(map(lambda x: -x, get_rel_pos(entity, target, prep)))  # Invert relationship, since parent and child are swapped in this case
            fill_out_child_locations(target, entities)
    for potential_parent in entities:  # If the other entity has the relation
        for rel in potential_parent["relations"]:
            if get_entity(rel["entity"], entities) is entity:  # Relation is to the current object
                prep = rel["prep"]
                if("position" not in potential_parent.keys()):
                    potential_parent["position"] = get_rel_pos(entity, potential_parent, prep)
                    fill_out_child_locations(potential_parent, entities)



def get_first_unpositioned_entity_index(entities):
    for idx, entity in enumerate(entities):
        if("position" not in entity.keys()):
            return idx
    return -1

def fill_out_all_locations(entities):
    while(True):
        idx = get_first_unpositioned_entity_index(entities)
        if(idx == -1):
            return True
        else:
            entities[idx]["position"] = [0,0,0]
            fill_out_child_locations(entities[idx], entities)

print("entity positioning test")
print(entities)
fill_out_all_locations(entities)
print(entities)