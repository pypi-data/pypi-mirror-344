'''
Quickly load classes from their aliases
'''
from typing import List, Tuple
import importlib

ALIAS_DEFINITIONS: List[Tuple[str, str]] = [
    # Preprocess
    ("outlier", "tsimpute.modules.preprocess.outlier.OutlierRemoval"),
    ("scaler", "tsimpute.modules.preprocess.scaler.Scaler"),
    # Metrics
    ("similarity", "tsimpute.modules.metric.common.Similarity"),
    ("sim", "tsimpute.modules.metric.common.Similarity"),
    ("nmae", "tsimpute.modules.metric.common.NMAE"),
    ("r2score", "tsimpute.modules.metric.common.R2Score"),
    ("r2", "tsimpute.modules.metric.common.R2Score"),
    ("rmse", "tsimpute.modules.metric.common.RMSE"),
    ("fsd", "tsimpute.modules.metric.common.FSD"),
    ("fb", "tsimpute.modules.metric.common.FB"),
    ("fa2", "tsimpute.modules.metric.common.FA2"),
    # Models
    ("lr", "tsimpute.modules.models.common.LinearRegressionModel"),
    ("knn", "tsimpute.modules.models.common.KNeighborsModel"),
    ("svm", "tsimpute.modules.models.common.SupportVectorMachineModel"),
    ("dt", "tsimpute.modules.models.common.DecisionTreeModel"),
    ("et", "tsimpute.modules.models.common.ExtraTreeModel"),
    ("ada", "tsimpute.modules.models.common.AdaBoostModel"),
    ("bag", "tsimpute.modules.models.common.BaggingModel"),
    ("gb", "tsimpute.modules.models.common.GradientBoostingModel"),
    ("rf", "tsimpute.modules.models.common.RandomForestModel"),
    ("cnn1", "tsimpute.modules.models.cnn1d.v1.CNN1DModel"),
    ("cnn2", "tsimpute.modules.models.cnn1d.v2.CNN1DModel"),
    ("cnn3", "tsimpute.modules.models.cnn1d.v3.CNN1DModel"),
    ("cnn_attn", "tsimpute.modules.models.cnn1d.attn.CNN1DAttentionModel"),
    ("attn", "tsimpute.modules.models.transformers.attn.AttentionModel"),
    ("mh_attn", "tsimpute.modules.models.transformers.mh_attn.MultiHeadAttentionModel"),
    ("trans", "tsimpute.modules.models.transformers.transformer.TransformerModel"),
    ("dynamic", "tsimpute.modules.models.dynamic.DynamicModel"),
    # Combine methods
    ("mean", "tsimpute.modules.combine.common.MeanCombine"),
    ("meow", "tsimpute.modules.combine.meow.MEOW"),
    ("wbdi", "tsimpute.modules.combine.wbdi.WBDI"),
    ("t/2", "tsimpute.modules.combine.half_t.HalfT"),
    # Trainer
    ("bidirectional", "tsimpute.modules.trainer.bidirectional.BiDirectionalTrainer"),
]


def __load_from_alias(path: str, *args, **kwargs):
    p = path.split(".")
    try:
        module = importlib.import_module(".".join(p[:-1]))
        return getattr(module, p[-1])(*args, **kwargs)
    except Exception as e:
        raise ImportError(
            f"Cannot load class {path}. Invalid alias definition.") from e


def load_from_alias(alias: str, *args, **kwargs):
    for definition in ALIAS_DEFINITIONS:
        if definition[0] == alias:
            return __load_from_alias(definition[1], *args, **kwargs)

    # Get the module if alias is a full path
    return __load_from_alias(alias, *args, **kwargs)
