import os
import re
import tiktoken

# First Reading the File
file_path = 'the_verdict.txt'


with open(file_path, 'r', encoding='utf-8') as f:
    raw_text = f.read()

result = re.split(r'([,.:;?_!"()\']|--|\s)', raw_text)
preprocessed = [item.strip() for item in result if item.strip()]


# Building a Tokenizer

all_words = sorted(set(preprocessed))
all_words.extend(['<|unk|>', '<|endoftext|>'])  # Adding special tokens
vocab = {token:integer for integer,token in enumerate(all_words)}

#Putting it all in a Tokenizer and DeTokenizer Class

class SimpleTokenizerV2:
    def __init__(self, vocab):
        self.str_to_int = vocab
        self.int_to_str = {i:s for s,i in vocab.items()}

    def encode(self, text):
        preprocessed = re.split(r'([,.:;?_!"()\']|--|\s)', text)
        preprocessed = [item.strip() for item in preprocessed if item.strip()]
        preprocessed = [item if item in self.str_to_int else '<|unk|>' for item in preprocessed]
        
        ids = [self.str_to_int[s] for s in preprocessed]
        return ids
    
    def decode(self, ids):
        text = " ".join([self.int_to_str[i] for i in ids])
        # Replacing spaces before punctuations
        text = re.sub(r'\s+([,.:;?_!"()\'])', r'\1', text)
        return text


x = input("Enter a sentence to tokenize: ")
tokenizer = tiktoken.get_encoding("gpt2")
encoded = tokenizer.encode(x, allowed_special={"<|endoftext|>"})

print("Encoded:", encoded)







    










