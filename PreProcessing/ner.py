import spacy
from spacy import displacy
from spacy.matcher import DependencyMatcher
from IPython.display import display, HTML

nlp = spacy.load("en_core_web_sm")

'''
raw_text = "There is four chair red laquer dining set shown in the image. There are opened white french doors leading " \
           "to the outside showing. There is a pool with blue water showing through the french doors of The Indian Space Research Organisation. The pools is " \
           "surrounded by green shrubbery. The wood floor is covered with white paint."
'''
raw_text = "There is a large room with two yellow dishwashers in it. Jamie is large. He is cool. Jamie has a green hat. It is large on his head."
processed_text = nlp(raw_text)


#for word in processed_text.ents:
#    print(word.text, word.label_)

#for word in processed_text:
#    print(word.lemma_, word.pos_, word.tag_, word.dep_,
#            word.shape_, word.is_alpha, word.is_stop)

#displacy.serve(processed_text, style="ent")



# AllenNLP

from allennlp.predictors.predictor import Predictor
import allennlp_models.tagging

#TODO: Pre-download this?
predictor = Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/coref-spanbert-large-2021.03.10.tar.gz")
pred = predictor.predict(document=raw_text)
#print(pred)

#From https://code.likeagirl.io/obtaining-allennlp-coreference-resolution-readable-clusters-in-python-37cd964d6ca0
clusters = pred['clusters']
document = pred['document']

n = 0
doc = {}
for obj in document:    
    doc.update({n :  obj}) #Create a dictionary of each word with its respective index, making it easier later
    n = n+1

all_clusters = []
for i in range(0, len(clusters)):
    cur_cluster = clusters[i]
    all_clusters.append([])
    for j in range(0, len(cur_cluster)):
        all_clusters[i].append([])
        obj = cur_cluster[j]  # obj = [27,31] for example - start/end of each reference
        for num in range((obj[0]), (obj[1]+1)):
            all_clusters[i][j].append(doc[num])
print(all_clusters) #And finally, this shows all coreferences



# Dependency Matching

#From https://stackoverflow.com/questions/67821137/spacy-how-to-get-all-words-that-describe-a-noun
pattern_left = [
  {
    "RIGHT_ID": "target",
    "RIGHT_ATTRS": {"POS": "NOUN"}
  },
  # founded -> subject
  {
    "LEFT_ID": "target",
    "REL_OP": ">",
    "RIGHT_ID": "modifier",
    "RIGHT_ATTRS": {"DEP": {"IN": ["amod", "nummod"]}}
  },
]

pattern_right = [] #TODO: Match adjectives to the right of nouns

matcher = DependencyMatcher(nlp.vocab)
matcher.add("FOUNDED", [pattern_left])

doc = nlp(raw_text)
for match_id, (target, modifier) in matcher(doc):
    print(doc[modifier], doc[target], sep="\t")