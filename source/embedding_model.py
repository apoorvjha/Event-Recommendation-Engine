from torch.nn import Module
from torch.utils.data import DataLoader
from torch.cuda import is_available
from torch import tensor, long, no_grad, concatenate
import transformers
from transformers import BertModel, BertTokenizer, BertConfig

class Model(Module):
    def __init__(self, model_path):
        super(Model, self).__init__()
        self.bert_model = BertModel.from_pretrained(model_path)
    def forward(self, ids, mask, token_type_ids):
        b_out = self.bert_model(
            ids,
            attention_mask = mask,
            token_type_ids = token_type_ids
        )["pooler_output"]
        return b_out

class ModelDataset:
    def __init__(self, data, max_length, tokenizer):
        self.data = data
        self.max_length = max_length
        self.tokenizer = tokenizer
    def __len__(self):
        return len(self.data)
    def __getitem__(self, idx):
        x = str(self.data[idx])
        old_level = transformers.logging.get_verbosity()
        transformers.logging.set_verbosity_error()
        inputs = self.tokenizer.encode_plus(
            text = x,
            add_special_tokens = True,
            max_length = self.max_length
        )
        transformers.logging.set_verbosity(old_level)
        ids = inputs["input_ids"]
        token_type_ids = inputs["token_type_ids"]
        mask = inputs["attention_mask"]

        padding_len = self.max_length - len(ids)

        ids += ([0] * padding_len)
        token_type_ids += ([0] * padding_len)
        mask += ([0] * padding_len)

        return {
            "ids" : tensor(ids, dtype = long),
            "token_type_ids" : tensor(token_type_ids, dtype = long),
            "mask" : tensor(mask, dtype = long)
        } 

def get_embedding(config, data):
    tokenizer = BertTokenizer.from_pretrained(config["MODEL_PATH"])
    dataset = ModelDataset(data, config["MAX_SEQUENCE_LENGTH"], tokenizer)
    dataloader = DataLoader(
        dataset,
        batch_size = config["BATCH_SIZE"],
        shuffle = False
    )
    device = ["cuda" if is_available() else "cpu"][0]
    embedding_model = Model(config["MODEL_PATH"]).to(device)
    
    embedding_matrix = []

    for bi, d in enumerate(dataloader):
        ids = d["ids"]
        token_type_ids = d["token_type_ids"]
        mask = d["mask"]

        ids = ids.to(device)
        token_type_ids = token_type_ids.to(device)
        mask = mask.to(device)
        
        with no_grad():
            outputs = embedding_model(ids, mask, token_type_ids)
        
        embedding_matrix.append(outputs)
    embedding_matrix = concatenate(embedding_matrix, dim = 0)
    return embedding_matrix



if __name__ == '__main__':
    words = ["transformer", "getter", "c++", "setter"]
    config = {
        "MODEL_PATH" : "bert-base-uncased",
        "BATCH_SIZE" : 4,
        "MAX_SEQUENCE_LENGTH" : 16
    }

    embedding_matrix = get_embedding(config, words)
    print(embedding_matrix.size())