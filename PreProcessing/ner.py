import spacy
from spacy import displacy
# from IPython.display import display, HTML

NER = spacy.load("en_core_web_sm")

# raw_text = "There is four chair red laquer dining set shown in the image. There are opened white french doors leading " \
#            "to the outside showing. There is a pool with blue water showing through the french doors of The Indian Space Research Organisation. The pools is " \
#            "surrounded by green shrubbery.	The wood floor is covered with white paint. "

# text1 = NER(raw_text)


# for word in text1.ents:
#     print(word.text, word.label_)

# for word in text1:
#     print(word.lemma_, word.pos_, word.tag_, word.dep_,
#             word.shape_, word.is_alpha, word.is_stop)

# displacy.serve(text1, style="ent")

def get_ner(text):
    processed = NER(text)
    return [(word.text, word.label_) for word in processed.ents]

