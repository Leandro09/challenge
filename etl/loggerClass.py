import logging

class LoggerObject:

    def __init__(self):
        self.formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(message)s')
        
    def get_logger(self, name, file_name, level=logging.INFO):
        handler = logging.FileHandler(file_name)
        handler.setFormatter(self.formatter)
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)
        return logger