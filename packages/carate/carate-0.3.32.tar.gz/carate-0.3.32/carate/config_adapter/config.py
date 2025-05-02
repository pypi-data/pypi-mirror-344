"""
Module for serialization and deserialization of inputs. The aim is to
keep web-first attitude, even though when using files locally. If there
is text files then there is a need to convert them.

@author = Julian M. Kleber
"""
import torch
from typing import Type, Optional, Dict, TypeVar, Any, Generic

from amarium.utils import convert_str_to_bool

from carate.evaluation import base, classification, regression, regression_custom_loss
from carate.models import (
    linear_block_classification, 
    linear_block_regression,
    linear_block_regression_pooling,
    linear_block_classification_pooling,
    cgc_classification,
    cgc_regression,
    cgc_without_linear_block_classification,
    cgc_without_linear_block_regression,
    cg_without_linear_block_classification,
    cg_without_linear_block_regression,
    g_classification,
    g_regression,
    c_plain_classification, 
    c_plain_regression,
    cc_classification,
    cc_regression,
    gcc_classification,
    gcc_regression,
    gatv2_classification,
    gatv2_regression,
    graph_transformer_classification,
    graph_transformer_regression,
)

from carate.loader.load_data import (
    DatasetObject,
    StandardPytorchGeometricDataset,
    StandardDatasetTUDataset,
    StandardDatasetMoleculeNet,
    CustomDataset,
    PyGZINC
)
from carate.utils.convert_to_json import convert_py_to_json
from carate.logging.metrics_logger import MetricsLogger

EvaluationMap: Dict[str, base.Evaluation]
EVALUATION_MAP = {
    "regression": regression.RegressionEvaluation,
    "classification": classification.ClassificationEvaluation,
    "evaluation": base.Evaluation,
    "regression_custom_loss": regression_custom_loss.RegressionEvaluation,
}

ModelMap: Dict[str, Any]
MODEL_MAP = {
    "linear_block_classification": linear_block_classification,
    "linear_block_regression": linear_block_regression, 
    "linear_block_regression_pooling": linear_block_regression_pooling,
    "linear_block_classification_pooling":linear_block_classification_pooling,
    "cgc_without_linear_block_classification": cgc_without_linear_block_classification, 
    "cgc_without_linear_block_regression": cgc_without_linear_block_regression,
    "cgc_classification": cgc_classification,
    "cgc_regression": cgc_regression,
    "cg_without_linear_block_classification":cg_without_linear_block_classification,
    "cg_without_linear_block_regression":cg_without_linear_block_regression,
    "g_classification": g_classification,
    "g_regression": g_regression,
    "c_plain_classification": c_plain_classification, 
    "c_plain_regression": c_plain_regression,
    "cc_classification": cc_classification,
    "cc_regression": cc_regression,
    "gatv2_classification": gatv2_classification,
    "gatv2_regression": gatv2_regression,
    "graph_transformer_classification": graph_transformer_classification,
    "graph_transformer_regression": graph_transformer_regression,
}

DATA_SET_MAP: Dict[
    str,
    Type[StandardDatasetMoleculeNet]
    | Type[StandardPytorchGeometricDataset]
    | Type[StandardPytorchGeometricDataset]
    | Type[CustomDataset]
]
DATA_SET_MAP = {
    "StandardPyG": StandardPytorchGeometricDataset,
    "StandardTUD": StandardDatasetTUDataset,
    "StandardMoleculeNet": StandardDatasetMoleculeNet,
    "PyGZINC": PyGZINC, 
    "CustomDataset": CustomDataset,
}


class Config:
    """
    The Config class is an object representation of the configuration of the model. It aims to provide a middle layer between
    some user input and the run interface. It is also possible to use it via the web because of the method overload of the constructor.

    :author: Julian M. Kleber
    """

    def __init__(
        self,
        dataset_name: str,
        num_features: int,
        num_classes: int,
        result_save_dir: str,
        model_save_freq: int,
        Evaluation: base.Evaluation,
        data_set: DatasetObject,
        model: Any,
        logger: Any, 
        optimizer: str,
        device: str = "auto",
        net_dimension: int = 364,
        learning_rate: float = 0.0005,
        dataset_save_path: str = ".",
        test_ratio: int = 20,
        batch_size: int = 64,
        shuffle: bool = True,
        num_cv: int = 5,
        num_epoch: int = 150,
        override: bool = True,
        resume: bool = False,
        normalize: bool = False,
        normalize_scaling :bool = False,
        num_heads: int = 3,
        dropout_gat: float = 0.6,
        dropout_forward: float = 0.5,
        dropout_forward2 : float = 0.5,
        custom_size: Optional[int] = None,
        factor:int = 1, 
        loss_factor:int = None, 
    ):


        # modelling

        self.model = model
        self.optimizer = optimizer
        self.device = device
        self.Evaluation = Evaluation
        self.data_set = data_set
        self.normalize = bool(normalize)
        self.normalize_scaling = normalize_scaling

        # model parameters

        self.dataset_name = dataset_name
        self.num_classes = num_classes
        self.num_features = num_features
        self.net_dimension = net_dimension
        self.num_heads = num_heads
        self.dropout_gat = dropout_gat
        self.dropout_forward = dropout_forward
        self.dropout_forward2 = dropout_forward2
        self.factor = factor
        self.loss_factor = loss_factor
        # evaluation parameters

        self.result_save_dir = result_save_dir
        self.model_save_freq = model_save_freq
        self.override = override

        # training
        self.resume = resume
        self.learning_rate = learning_rate
        self.test_ratio = test_ratio
        self.batch_size = batch_size
        self.custom_size = custom_size
        self.num_cv = num_cv
        self.num_epoch = num_epoch

        # data
        self.dataset_name = dataset_name
        self.dataset_save_path = dataset_save_path
        self.shuffle = shuffle
        self.logger = logger


class ConfigInitializer:
    @classmethod
    def from_file(cls, file_name: str) -> Config:
        """
        The from_file function takes a file name as an argument and returns a Config object.
        The function reads the file, converts it to JSON, then uses the from_json method to create
        the Config object.

        :param cls: Used to create a new instance of the class.
        :param file_name:str: Used to specify the name of the file to be used.
        :return: A config object.

        :doc-author: Julian M. Kleber
        """

        json_object = convert_py_to_json(file_name)
        config_object = ConfigInitializer.from_json(json_object = json_object)
        return config_object

    @classmethod
    def from_json(cls, json_object: Dict[Any, Any]) -> Config:
        """
        The from_json function is a class method that takes in a json object and returns an instance of the Config class.
        The function is used to load the configuration from a file, which can be done by calling:
            config = Config.from_json(json_object)

        :param cls: Used to Create an instance of the class that is calling this method.
        :param json_object:dict: Used to Pass in the json object that is read from the file.
        :return: A class object.

        :doc-author: Julian M. Kleber
        """

        if json_object["device"] == "cpu":
            device = torch.device("cpu")
        elif json_object["device"] == "cuda":
            device = torch.device("cuda")
        elif json_object["device"] == "auto":
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        if "resume" in list(json_object.keys()):
            resume = json_object["resume"]
        else:
            resume = False

        if "normalize" in json_object.keys():
            boolean_val =  json_object["normalize"]
            if boolean_val == "False": 
                normalize = False
            elif boolean_val == "True": 
                normalize = True
            elif type(boolean_val) == type(True):
                normalize = boolean_val 
                
        else:
            normalize = False

        
        if "normalize_scaling" in json_object.keys():
            boolean_val =  json_object["normalize_scaling"]
            if boolean_val == "False": 
                normalize_scaling = False
            elif boolean_val == "True": 
                normalize_scaling = True
            elif type(boolean_val) == type(True):
                normalize_scaling = boolean_val 
                
        else:
            normalize_scaling = False

        if "custom_size" in json_object.keys():
            custom_size = json_object["custom_size"]
        else:
            custom_size = None

        if "num_heads" in json_object.keys():
            num_heads = json_object["num_heads"]
        else:
            num_heads = 3

        if "dropout_forward" in json_object.keys():
            dropout_forward = json_object["dropout_forward"]
        else:
            dropout_forward = 0.5
        

        if "dropout_forward2" in json_object.keys():
            dropout_forward2 = json_object["dropout_forward2"]
        else:
            dropout_forward2 = 0.5

        if "dropout_gat" in json_object.keys():
            dropout_gat = json_object["dropout_gat"]
        else:
            dropout_gat = 0.6
        
        if "factor" in json_object.keys():
            factor = json_object["factor"]
        else: 
            factor = 1
        if "log_save_dir" not in json_object.keys(): 
            log_save_dir = json_object["result_save_dir"]
        else: 
            log_save_dir = json_object["log_save_dir"]
        

        if "loss_factor" in json_object.keys(): 
            loss_factor = json_object["loss_factor"]
        else: 
            loss_factor=1

        metrics_logger = MetricsLogger(log_save_dir)
        metrics_logger.logger.info("Initializing configuration for the config file ")
        metrics_logger.logger.info("The configuration is: " + str(json_object))
        data_set = DATA_SET_MAP[json_object["data_set"]](
            dataset_save_path=json_object["dataset_save_path"],
            dataset_name=json_object["dataset_name"],
            test_ratio=json_object["test_ratio"],
            batch_size=json_object["batch_size"],
            shuffle=json_object["shuffle"],
        )

        evaluation = EVALUATION_MAP[json_object["evaluation"]](
            dataset_name=json_object["dataset_name"],
            dataset_save_path=json_object["dataset_save_path"],
            test_ratio=json_object["test_ratio"],
            model_net=json_object["model"],
            optimizer=json_object["optimizer"],
            data_set=data_set,
            result_save_dir=json_object["result_save_dir"],
            model_save_freq=json_object["model_save_freq"],
            device=device,
            resume=resume,
            logger = metrics_logger, 
            normalize_scaling = normalize_scaling, 
            loss_factor = loss_factor,
        )
        json_object["override"] = convert_str_to_bool(json_object["override"])
        return Config(
            model=MODEL_MAP[json_object["model"]],
            optimizer=json_object["optimizer"],
            device=device,
            Evaluation=evaluation,
            data_set=data_set,
            # model parameters
            dataset_name=str(json_object["dataset_name"]),
            num_classes=int(json_object["num_classes"]),
            num_features=int(json_object["num_features"]),
            net_dimension=int(json_object["net_dimension"]),
            learning_rate=float(json_object["learning_rate"]),
            # evaluation parameters
            dataset_save_path=str(json_object["dataset_save_path"]),
            test_ratio=int(json_object["test_ratio"]),
            batch_size=int(json_object["batch_size"]),
            shuffle=bool(json_object["shuffle"]),
            num_cv=int(json_object["num_cv"]),
            num_epoch=int(json_object["num_epoch"]),
            result_save_dir=str(json_object["result_save_dir"]),
            model_save_freq=int(json_object["model_save_freq"]),
            override=json_object["override"],
            resume=resume,
            normalize=bool(normalize),
            normalize_scaling=normalize_scaling,
            num_heads=num_heads,
            dropout_forward=dropout_forward,
            dropout_forward2=dropout_forward2, 
            dropout_gat=dropout_gat,
            custom_size=custom_size,
            logger = metrics_logger, 
            factor=factor,
            loss_factor = float(loss_factor)
        )
