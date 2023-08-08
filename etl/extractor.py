from typing import List
from .loggerClass import LoggerObject
import requests

class Extractor:
    def __init__(self):
        """
        This class extracts data from url
        """
        self.logger = LoggerObject().get_logger('extract_log', 'logs/extract_logs.txt')

    def extract_data(self, url):
        """
        Extracts data from json data

        Returns:
            data as a list of dictionaries
        """
        try:
            self.logger.info("Start extract step")
            # call api to do the request
            response = requests.get(url)
            
            # check error status
            if response.status_code != 200:
                raise requests.exceptions.RequestException(f"Request failed with status code: {response.status_code}")
  

            launch_data = response.json()  # Convert JSON response to Python dictionary
            
            self.logger.info("Extraction process was completed")
            return launch_data

        except requests.exceptions.RequestException as e:
            self.logger.error(e)
            return None
