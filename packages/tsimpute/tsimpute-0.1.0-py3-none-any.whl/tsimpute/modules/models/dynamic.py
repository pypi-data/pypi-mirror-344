'''
Dynamic models.
'''

from typing import List
from tsimpute.modules.models.base import BaseBiDirectionalModel


class DynamicModel(BaseBiDirectionalModel):
    '''
    Dynamic model. It allows to train with different models in different positions
    '''
    use_generator = False

    def __init__(self, models: List[BaseBiDirectionalModel], **kwargs):
        super().__init__(**kwargs)
        self.models = models
        self.model_index = 0
        self.name = "Dynamic-" + "-".join([model.name for model in models])

    def train(self, x, y):
        self.models[self.model_index].train(x, y)

    def forecast(self, x):
        return self.models[self.model_index].forecast(x)

    def reset(self):
        self.models[self.model_index].reset()

    def summary(self):
        return "\n".join([model.summary() for model in self.models])

    def increment_model_index(self):
        self.model_index += 1
        if self.model_index >= len(self.models):
            self.model_index = 0
