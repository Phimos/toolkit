from typing import Any

import pytorch_lightning as pl
import torch
import torch.nn as nn
from torch import Tensor
from torch.optim import Adam
from torch.optim.lr_scheduler import ReduceLROnPlateau


class LightningModel(pl.LightningModule):
    def __init__(self, hparams: dict):
        super().__init__()
        self.hparams.update(hparams)
        self.model: nn.Module = None
        self.loss: nn.Module = None
        self.metric: nn.Module = None

    def forward(self, *args: Tensor, **kwargs: Tensor):
        return self.model(*args, **kwargs)

    def training_step(self, batch: Any, batch_idx: int) -> dict:
        data, target = batch
        pred = self.forward(**data)
        loss = self.loss(pred, target)
        metric = self.metric(pred, target)
        self.log('train_loss', loss, on_step=True, on_epoch=False)
        self.log('train_metric', metric, on_step=True, on_epoch=False)
        return loss

    def validation_step(self, batch: Any, batch_idx: int):
        data, target = batch
        pred = self.forward(**data)
        loss = self.loss(pred, target)
        metric = self.metric(pred, target)
        self.log('val_loss', loss, on_step=True, on_epoch=False)
        self.log('val_score', metric, on_step=True, on_epoch=False)

    def configure_optimizers(self):
        optimizer = Adam(self.parameters(), lr=self.hparams.learning_rate)
        scheduler = ReduceLROnPlateau(optimizer, mode='max')
        return {
            'optimizer': optimizer,
            'lr_scheduler': {
                'scheduler': scheduler,
                'monitor': 'val_score',
            }
        }
