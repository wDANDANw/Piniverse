
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


# sentences = [
#     'I love my dog',
#     'I love my cat',
#     'You love my dog!',
#     'Do you think my dog is amazing?'
# ]

# tokenizer = Tokenizer(num_words=100, oov_token="<OOV>")
# tokenizer.fit_on_texts(sentences)
# word_index = tokenizer.word_index

# sequences = tokenizer.texts_to_sequences(sentences)

# padded = pad_sequences(sequences)  # padding='post', truncating='post', maxlen=5
# print(word_index)
# print(sequences)
# print(padded)

# test_data = [
#     'i really love my dog',
#     'my dog loves my manatee'
# ]

# test_seq = tokenizer.texts_to_sequences(test_data)
# print(test_seq)

# region Demo
class EntityResolver:

    def __init__(self, input_list:list):
        self.input_list = input_list

        print(input_list)

        # Tokenization Related
        self.tokenizer = Tokenizer(num_words=100, oov_token="<OOV>")
        self.tokenizer.fit_on_texts(input_list)
        self.sequences = self.tokenizer.texts_to_sequences(self.input_list)
    
    def get_sequences(self):
        return self.sequences

# endregion