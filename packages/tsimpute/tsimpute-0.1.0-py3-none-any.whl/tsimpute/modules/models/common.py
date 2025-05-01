'''
Common Machine Learning Models
'''
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor, ExtraTreeRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    BaggingRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor
)
from tsimpute.modules.models.base import BaseBiDirectionalModel
from tsimpute.core.utils import get_table_summary


class _BaseCommonMachineLearningModel(BaseBiDirectionalModel):
    '''
    Base class for common machine learning models
    '''
    use_generator = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def train(self, x, y):
        # Reshape X to 2D
        x = x.reshape(x.shape[0], -1)
        # Train model
        self.model.fit(x, y)

    def forecast(self, x):
        # Reshape X to 2D
        x = x.reshape(1, -1)
        # Predict
        return self.model.predict(x).ravel()

    def reset(self):
        self.model = self.model.__class__(**self.kwargs)

    def summary(self):
        m_params = self.model.get_params()
        return get_table_summary(
            name=self.name,
            data=[list(m_params.values())],
            cols=list(m_params.keys())
        )


class LinearRegressionModel(_BaseCommonMachineLearningModel):
    '''
    Linear Regression model
    '''
    name = "Linear-Regression"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = LinearRegression(**kwargs)


class KNeighborsModel(_BaseCommonMachineLearningModel):
    '''
    K-Neighbors Regressor model
    '''
    name = "K-Nearest-Neighbors"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = KNeighborsRegressor(**kwargs)


class SupportVectorMachineModel(_BaseCommonMachineLearningModel):
    '''
    Support Vector Machine Regressor model
    '''
    name = "Support-Vector-Machine"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = SVR(**kwargs)


class DecisionTreeModel(_BaseCommonMachineLearningModel):
    '''
    Decision Tree Regressor model
    '''
    name = "Decision-Tree"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = DecisionTreeRegressor(**kwargs)


class ExtraTreeModel(_BaseCommonMachineLearningModel):
    '''
    Extra Tree Regressor model
    '''
    name = "Extra-Tree"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = ExtraTreeRegressor(**kwargs)


class AdaBoostModel(_BaseCommonMachineLearningModel):
    '''
    AdaBoost Regressor model
    '''
    name = "AdaBoost"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = AdaBoostRegressor(**kwargs)


class BaggingModel(_BaseCommonMachineLearningModel):
    '''
    Bagging Regressor model
    '''
    name = "Bagging"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = BaggingRegressor(**kwargs)


class GradientBoostingModel(_BaseCommonMachineLearningModel):
    '''
    Gradient Boosting Regressor model
    '''
    name = "Gradient-Boosting"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = GradientBoostingRegressor(**kwargs)


class RandomForestModel(_BaseCommonMachineLearningModel):
    '''
    Random Forest Regressor model
    '''
    name = "Random-Forest"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = RandomForestRegressor(**kwargs)
