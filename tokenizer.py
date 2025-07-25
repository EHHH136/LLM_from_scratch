import os
import re
import tiktoken
import torch
from torch.utils.data import Dataset, DataLoader    

# First Reading the File
file_path = 'the_verdict.txt'



# Listing a dataset for baqtched inputs and targets


class GPTDatasetV1(Dataset):
    def __init__(self, txt, tokenizer, max_lenth, stride):
        self.input_ids = []
        self.target_ids = []

        token_ids = tokenizer.encode(txt)

        for i in range(0, len(token_ids) - max_lenth, stride):
            input_chunk = token_ids[i:i + max_lenth]
            target_chunk = token_ids[i + 1: i + max_lenth + 1]
            self.input_ids.append(torch.tensor(input_chunk,dtype=torch.long))
            self.target_ids.append(torch.tensor(target_chunk,dtype=torch.long))
    
    def __len__(self):
        return len(self.input_ids)
    
    def __getitem__(self, idx):
        return self.input_ids[idx], self.target_ids[idx]


# Listing A data loader to generate batches with input-with pairs

def create_dataloader_v1(txt, batch_size=4, max_length=256, 
                         stride=128, shuffle=True, 
                         drop_last=True, num_workers=0):
    tokenizer = tiktoken.get_encoding("gpt2")
    dataset = GPTDatasetV1(txt, tokenizer, max_length, stride)
    dataloader = DataLoader(
        dataset, 
        batch_size=batch_size, 
        shuffle=shuffle, 
        drop_last=drop_last, 
        num_workers=num_workers
        )
    return dataloader


with open(file_path, 'r', encoding='utf-8') as f:
    raw_text = f.read()


""" 2.7 Creating token embeddings

input_ids = torch.tensor([2,3,5,1])
vocab_size = 6
output_dim = 3

torch.manual_seed(123)
embedding_layer = torch.nn.Embedding(vocab_size, output_dim)

"""


# 2.8 Encoding word positions

dataloader = create_dataloader_v1(raw_text, batch_size=8, max_length=4, 
                                  stride=4, shuffle = False)

data_iter = iter(dataloader)
inputs, targets = next(data_iter)


vocab_size = 50257
output_dim = 256
token_embedding_layer = torch.nn.Embedding(vocab_size, output_dim)
token_embeddings = token_embedding_layer(inputs)

context_length = 4 #Max Length
pos_embedding_layer = torch.nn.Embedding(context_length, output_dim)
pos_embeddings = pos_embedding_layer(torch.arange(context_length))

input_embeddings = token_embeddings + pos_embeddings


    










