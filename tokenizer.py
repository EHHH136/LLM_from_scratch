import os
import re
import tiktoken

# First Reading the File
file_path = 'the_verdict.txt'


with open(file_path, 'r', encoding='utf-8') as f:
    raw_text = f.read()

tokenizer = tiktoken.get_encoding("gpt2")
enc_text = tokenizer.encode(raw_text)
enc_sample = enc_text[50:]

context_size = 4


for i in range(1, context_size + 1):
    context = enc_sample[:i]
    desired = enc_sample[i]
    print(tokenizer.decode(context), "------>", tokenizer.decode([desired]))













    










