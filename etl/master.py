from .extractor import Extractor
from .loader import Loader
from .transformer import Transformer


def run_etl(path: str):
    """
    Runs whole ETL pipeline

    Args:
        path: path to the source file
    """
    extractor = Extractor()
    transformer = Transformer(extractor.extract_data(path))
    transformer.transform_data()
    loader = Loader(transformer.transform_data())
    loader.load_data()
