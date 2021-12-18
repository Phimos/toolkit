from typing import List

import torch
from toolkit.utils.containers import SlashDict
from torch.utils.data import DataLoader, Dataset


class DictDataset(Dataset):
    def __init__(self, data: list, label: list):
        self.data = data
        self.label = label

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx: int) -> SlashDict:
        item = SlashDict()
        item['data'] = self.data[idx]
        item['label'] = self.label[idx]
        return item


def all_same(items: List):
    return all(x == items[0] for x in items)


def only_one(items: List[bool]):
    items = iter(items)
    return any(items) and not any(items)
