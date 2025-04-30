import torch
import numpy as np
from pyarrow import fs
import io

class SplitterModel(torch.nn.Module):
    def __init__(self, input_dim: int):
        super(SplitterModel, self).__init__()
        self.linear = torch.nn.Sequential(
            torch.nn.Linear(input_dim, 256),
            torch.nn.ReLU(),
            torch.nn.Linear(256, 128),
            torch.nn.ReLU(),
            torch.nn.Linear(128, 1),
        )
        
    def forward(self, x):
        x = self.linear(x)
        x = torch.sigmoid(x)
        return x
    
def load_model(model_path: str) -> SplitterModel:
    model_state_dict = load_model_state_from_hdfs(model_path)
    model = SplitterModel(1924)
    model.load_state_dict(model_state_dict)
    model.eval()
    return model
    
def load_model_state_from_hdfs(model_path: str):
    filesystem = fs.HadoopFileSystem(host="default")
    with filesystem.open_input_file(model_path) as f:
        model_bytes = f.read()
    model_state_dict = torch.load(io.BytesIO(model_bytes))
    return model_state_dict

def compute_features(product_a, product_b):
    x1 = np.array(product_a["text_embs"])
    x2 = np.array(product_b["text_embs"])
    embedding_difference_sum = []
    embedding_difference_sum.append(((x1 - x2) ** 2).sum())
    embedding_difference = np.concatenate([x1, x2, (x1 - x2) ** 2])
    same_cols = [1, 1, 1]
    res = np.concatenate([embedding_difference_sum, embedding_difference, same_cols])
    return res

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
