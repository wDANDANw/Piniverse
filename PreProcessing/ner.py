import spacy
from spacy import displacy
from spacy.matcher import DependencyMatcher
from IPython.display import display, HTML

NER = spacy.load("en_core_web_sm")

raw_text = "There is four chair red laquer dining set shown in the image. There are opened white french doors leading " \
           "to the outside showing. There is a pool with blue water showing through the french doors of The Indian Space Research Organisation. The pools is " \
           "surrounded by green shrubbery.	The wood floor is covered with white paint. "

processed_text = NER(raw_text)


#for word in processed_text.ents:
#    print(word.text, word.label_)

#for word in processed_text:
#    print(word.lemma_, word.pos_, word.tag_, word.dep_,
#            word.shape_, word.is_alpha, word.is_stop, word.head.lemma_)

#displacy.serve(processed_text, style="ent")



# AllenNLP Coreference Resolution

from allennlp.predictors.predictor import Predictor
import allennlp_models.tagging

#TODO: Pre-download this?
predictor = Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/coref-spanbert-large-2021.03.10.tar.gz")
pred = predictor.predict(document=raw_text)
#print(pred)

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
print(all_clusters) #And finally, this shows all coreferences
#print(pred['clusters']) #Original cluster numbers for comparison, if needed



# Dependency Matching

#From https://stackoverflow.com/questions/67821137/spacy-how-to-get-all-words-that-describe-a-noun
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

# ^ but in the opposite direction:
'''
{
    "RIGHT_ID": "target",
    "RIGHT_ATTRS": {"DEP": {"IN": ["amod", "nummod"]}}
  },
  {
    "LEFT_ID": "target",
    "REL_OP": "<",
    "RIGHT_ID": "modifier",
    "RIGHT_ATTRS": {"POS": "NOUN"}
  },
  '''

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

matcher = DependencyMatcher(nlp.vocab)
matcher.add("DIRECT", [pattern_direct_modifier])
matcher.add("IS", [pattern_is_modifier])
matches = matcher(processed_text)



doc = processed_text
entities = []

def cluster_contains(cluster, test_token):
  for phrase in cluster:
    for token in phrase:
      if token == test_token:
        return True
  return False

def share_cluster(token1, token2):
  for cluster in all_clusters:
    if cluster_contains(cluster, token1) and cluster_contains(cluster, token2):
      return True
  return False

def append_noun(noun_obj): # Link coreference resolution with dependency matching in this function; TODO: Just pass in noun and adjective separately
  for entity in entities:
    for noun in entity["nouns"]:
      if noun_obj["noun"] == noun:
        entity["adjectives"].append(noun_obj["adj"])
        return
      elif share_cluster(noun_obj["noun"], noun):
        entity["nouns"].append(noun_obj["noun"])
        entity["adjectives"].append(noun_obj["adj"])
        return
  entities.append({
    "nouns": [noun_obj["noun"]], #TODO: Capitalize proper nouns and uncapitalize improper nouns regardless of their current capitalization (not sure where to put this TODO specifically)
    "adjectives": [noun_obj["adj"]]
  })



for match_type_id, match_items in matches:
  if len(match_items) == 2:
    print('Match:', doc[match_items[1]], doc[match_items[0]])
    append_noun({
      "noun": doc[match_items[0]],
      "adj": doc[match_items[1]]
    })
  elif len(match_items) == 3:
    print('Match:', doc[match_items[2]], doc[match_items[1]])
    append_noun({
      "noun": doc[match_items[1]],
      "adj": doc[match_items[2]]
    })
print(entities)


'''
nouns = []
for cluster in all_clusters:
  nouns.append({
    "names": map(lambda phrase: " ".join(phrase), cluster),
    "adjectives": []
  })

for link in all_links:
  link['cluster'] = None
  for idx, cluster in enumerate(all_clusters):
    for phrase in cluster:
      for token in phrase:
        if link['noun'] == token:
          link['cluster'] = idx
print(nouns)
'''

def get_ner(text):
    processed = NER(text)
    return [(word.text, word.label_) for word in processed.ents]