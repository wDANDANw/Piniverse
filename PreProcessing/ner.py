import spacy
from spacy.matcher import DependencyMatcher
nlp = spacy.load("en_core_web_sm")

from allennlp.predictors.predictor import Predictor
predictor = Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/coref-spanbert-large-2021.03.10.tar.gz")

# Utility function used by main.py
def get_ner(text):
    processed = nlp(text)
    return [(word.text, word.label_) for word in processed.ents]



# Uses AllenNLP Coreference Resolution and Spacy Dependency Matching to parse raw text into a list of described and connected entities!
def parse_entities(raw_text, nlp, predictor):

  # Tell the AI to work its magic
  processed_text = nlp(raw_text)
  pred = predictor.predict(document=raw_text)

  print("")
  print("----------")
  print("")
  for word in processed_text:
      print(word.lemma_, word.pos_, word.tag_, word.dep_,
              word.shape_, word.is_alpha, word.is_stop, word.head.lemma_)



  # Now, parse that text!

  # Adapted from https://code.likeagirl.io/obtaining-allennlp-coreference-resolution-readable-clusters-in-python-37cd964d6ca0
  clusters = pred['clusters']
  all_clusters = []
  for i in range(0, len(clusters)):
      cur_cluster = clusters[i]
      all_clusters.append([])
      for j in range(0, len(cur_cluster)):
          all_clusters[i].append([])
          obj = cur_cluster[j]  # obj = [27,31] for example - start/end of each reference
          for num in range((obj[0]), (obj[1]+1)):
              all_clusters[i][j].append(processed_text[num])
  #print(all_clusters) #And finally, this shows all coreferences
  #print(pred['clusters']) #Original cluster numbers for comparison, if needed



  # Dependency Matching

  # Modified from https://stackoverflow.com/questions/67821137/spacy-how-to-get-all-words-that-describe-a-noun
  pattern_direct_modifier = [  # Adjectives that directly modify a noun, eg. "the red chair"
    {
      "RIGHT_ID": "target",
      "RIGHT_ATTRS": {"POS": {"IN": ["NOUN","PRON","PROPN"]}}
    },
    {
      "LEFT_ID": "target",
      "REL_OP": ">",
      "RIGHT_ID": "modifier",
      "RIGHT_ATTRS": {"DEP": {"IN": ["amod", "nummod"]}}
    },
  ]

  pattern_is_modifier = [  # Adjectives that indirectly modify a noun through the verb "is" (lemma "be"), eg. "the chair is red"
    {
      "RIGHT_ID": "is",
      "RIGHT_ATTRS": {
        "POS": {"IN": ["VERB", "AUX"]},
        "LEMMA": "be"
      }
    },
    {
      "LEFT_ID": "is",
      "REL_OP": ">",
      "RIGHT_ID": "noun",
      "RIGHT_ATTRS": {
        "POS": {"IN": ["NOUN","PRON","PROPN"]},
        "DEP": {"IN": ["nsubj"]}
      }
    },
    {
      "LEFT_ID": "is",
      "REL_OP": ">",
      "RIGHT_ID": "adjective",
      "RIGHT_ATTRS": {
        "POS": {"IN": ["ADJ"]},
        "DEP": {"IN": ["acomp"]}
      }
    },
  ]

  pattern_prepositional_relation_is = [  # "the cat is in the tree"
    {
      "RIGHT_ID": "is",
      "RIGHT_ATTRS": {
        "POS": {"IN": ["VERB", "AUX"]},
        "LEMMA": "be"
      }
    },
    {
      "LEFT_ID": "is",
      "REL_OP": ">",
      "RIGHT_ID": "noun",
      "RIGHT_ATTRS": {
        "POS": {"IN": ["NOUN","PRON","PROPN"]},
        "DEP": {"IN": ["nsubj"]}
      }
    },
    {
      "LEFT_ID": "is",
      "REL_OP": ">",
      "RIGHT_ID": "prep",
      "RIGHT_ATTRS": {
        "POS": {"IN": ["ADP"]},
        "DEP": {"IN": ["prep"]}
      }
    },
    {
      "LEFT_ID": "prep",
      "REL_OP": ">",
      "RIGHT_ID": "subj",
      "RIGHT_ATTRS": {
        "POS": {"IN": ["NOUN","PRON","PROPN"]},
        "DEP": {"IN": ["pobj"]}
      }
    },
  ]

  pattern_prepositional_relation_direct = [  # "the cat in the tree (...is orange, etc.)"
    {
      "RIGHT_ID": "noun",
      "RIGHT_ATTRS": {
        "POS": {"IN": ["NOUN","PRON","PROPN"]},
        "DEP": {"IN": ["nsubj"]}
      }
    },
    {
      "LEFT_ID": "noun",
      "REL_OP": ">",
      "RIGHT_ID": "prep",
      "RIGHT_ATTRS": {
        "POS": {"IN": ["ADP"]},
        "DEP": {"IN": ["prep"]}
      }
    },
    {
      "LEFT_ID": "prep",
      "REL_OP": ">",
      "RIGHT_ID": "subj",
      "RIGHT_ATTRS": {
        "POS": {"IN": ["NOUN","PRON","PROPN"]},
        "DEP": {"IN": ["pobj"]}
      }
    },
  ]

  matcher = DependencyMatcher(nlp.vocab)
  matcher.add("DIRECT", [pattern_direct_modifier])
  matcher.add("IS", [pattern_is_modifier])
  matches = matcher(processed_text)



  doc = processed_text
  entities = []

  def cluster_contains(cluster, test_token):
    for phrase in cluster:
      for token in phrase:
        if token == test_token and test_token.head not in phrase:  # Only consider the primary nouns of a phrase to be in the cluster
          return True
    return False

  def share_cluster(token1, token2):
    for cluster in all_clusters:
      if cluster_contains(cluster, token1) and cluster_contains(cluster, token2):
        return True
    return False

  def append_noun_and_adjs(input_noun, input_adjs):  # Link coreference resolution with dependency matching in this function; TODO: Just pass in noun and adjective separately
    for entity in entities:
      for noun in entity["nouns"]:
        if input_noun == noun:
          entity["adjectives"].extend(input_adjs)
          return
        elif share_cluster(input_noun, noun):
          entity["nouns"].append(input_noun)
          entity["adjectives"].extend(input_adjs)
          return
    entities.append({
      "nouns": [input_noun],  #TODO: Capitalize proper nouns and uncapitalize improper nouns regardless of their current capitalization (here? probably not, probably as the data leaves the backend / parse function?)
      "adjectives": input_adjs,
      "relations": []  # Will be filled in later when prepositions are parsed
    })



  # Build an entity list from all nouns and their associated adjectives
  for match_type_id, match_items in matches:
    if len(match_items) == 2:
      #print('Match:', doc[match_items[1]], doc[match_items[0]])
      append_noun_and_adjs(doc[match_items[0]], [doc[match_items[1]]])
    elif len(match_items) == 3:
      #print('Match:', doc[match_items[2]], doc[match_items[1]])
      append_noun_and_adjs(doc[match_items[1]], [doc[match_items[2]]])

  # Add all nouns that don't have any associated adjectives
  for word in processed_text:
    if word.pos_ in ["NOUN","PRON","PROPN"]:
      append_noun_and_adjs(word, [])
  #print(entities)



  #print("Prepositions:")
  prep_relations = []
  preposition_matcher = DependencyMatcher(nlp.vocab)
  preposition_matcher.add("PREPOSITION_IS", [pattern_prepositional_relation_is])
  preposition_matcher.add("PREPOSITION_DIRECT", [pattern_prepositional_relation_direct])
  matches = preposition_matcher(processed_text)

  def append_prep(noun, prep, subj):
    #print('Match:', noun, prep, subj)
    prep_relations.append({
      "noun": noun,
      "prep": prep,
      "subj": subj,
    })

  for match_type_id, match_items in matches:
    if len(match_items) == 3:  # "noun prep noun"
      append_prep(doc[match_items[0]], doc[match_items[1]], doc[match_items[2]])
    elif len(match_items) == 4:  # "noun is prep noun"
      append_prep(doc[match_items[1]], doc[match_items[2]], doc[match_items[3]])
  #print(prep_relations)

  for relation in prep_relations:
    for entity in entities:
      if relation["noun"] in entity["nouns"]:  # If the relation refers to the entity as its source noun
        for target_entity in entities:
          if relation["subj"] in target_entity["nouns"]:  # TODO: What if no matching nouns are found?
            entity["relations"].append({
              "prep": relation["prep"],
              "entity": relation["subj"]
            })
  #print(entities)

  return entities


# Use the imported nlp and predictor functions here so that outside modules don't have to re-import them
# and pass them into the parsing function themselves (but still allow this through the old parse_entities function)
def parse_entities_standalone(text):
  return parse_entities(text, nlp, predictor)
