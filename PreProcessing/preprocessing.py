import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag
from nltk.chunk import conlltags2tree, tree2conlltags
from pprint import pprint
import numpy

stop_words = set(stopwords.words('english'))

# Dummy
txt = "A young boy has been kidnapped by a bad Sorceress!"
txt2 = "Experience the opening chapter to the supernatural point-and-click adventure game"

def tokenize_tag(txt):
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    new_words = tokenizer.tokenize(txt)
    result = nltk.pos_tag(new_words)
    return result

def chunk_entity_recognize(txt):
    pattern = 'NP: {<DT>?<JJ>*<NN>}'
    cp = nltk.RegexpParser(pattern)
    cs = cp.parse(txt)

    cs.draw()

    iob_tagged = tree2conlltags(cs)
    pprint(iob_tagged)


tagged = tokenize_tag(txt)
print(tagged)
result = chunk_entity_recognize(tagged)
# print(result)
# result.draw()
# nltk.chunk.conllstr2tree(parse_string, chunk_types=['NP']).draw()