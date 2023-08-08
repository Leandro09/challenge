from typing import List, Optional, Union

from .models import LaunchModel, FailureModel, CoresModel
from .loggerClass import LoggerObject


class Transformer:
    def __init__(self, raw_data: List[dict]):
        """
        This class transforms extracted data according to the desired model

        Args:
            raw_data: extracted data
        """
        self.raw_data = raw_data
        self.logger = LoggerObject().get_logger('transform_log', 'logs/transform_logs.txt')

    def transform_data(self) -> List[LaunchModel]:
        """
        Transforms data

        Returns:
            transformed data as a list of models
        """
        transformed_models = list()
        for item in self.raw_data:
            launchModel = self.transform_single_item(item)
            transformed_models.append(launchModel)
        return transformed_models

    def transform_single_item(self, input_item: dict) -> Optional[LaunchModel]:
        """
        Transforms single item of extracted data

        Args:
            input_item: part of extracted data

        Returns:
            model if transformation was successful
        """

        launchModel = self.get_launch(input_item)
        launchModel.failures = self.get_failures(input_item)
        launchModel.cores = self.get_cores(input_item)


        return launchModel;
        
    
    def get_cores(self, input_item):
        """
        Method to extract information about cores

        Returns:
            Return a list with cores data
        """
        cores = []
    

        cores_data = input_item['cores']
        for core_data in cores_data:
            try:
                cores_model = CoresModel(**core_data)
                cores.append(cores_model)
            except Exception as e:
                self.logger.error(f"Error in transformation with record: {core_data} - {str(e)}")
        
        return cores
        
        
    def get_failures(self, input_item):
    
        """
        Method to extract information about failures

        Returns:
            Return a list with failures data
        """
    
        failures = []
    
        failures_data = input_item['failures']
        for failure_data in failures_data:
            try:
                failures_model = FailureModel(**failure_data)
                failures.append(failures_model)
            except Exception as e:
                self.logger.error(f"Error in transformation with record: {failure_data} - {str(e)}")
        
        return failures
    
    def get_launch(self,input_item):
        """
        Method to extract information about launches

        Returns:
            Return a list with launches data
        """
    
        launch_properties = {
            "id": input_item['id'],
            "name": input_item['name'],
            "date_utc": input_item['date_utc'],
            "date_unix": input_item['date_unix'],
            "date_local": input_item['date_local'],
            "date_precision": input_item['date_precision'],
            "static_fire_date_utc": input_item['static_fire_date_utc'],
            "static_fire_date_unix": input_item['static_fire_date_unix'],
            "net": input_item['net'],
            "window": input_item['window'],
            "success": input_item['success'],
            "rocket": input_item['rocket'],
            "details": input_item['details'],
            "webcast": input_item['links']['webcast'],
            "youtube_id": input_item['links']['youtube_id'],
            "article": input_item['links']['article'],
            "wikipedia": input_item['links']['wikipedia'],
            "auto_update": input_item['auto_update'],
            "tbd": input_item['tbd'],
            "launch_library_id": input_item['launch_library_id'],
            "launchpad": input_item['launchpad'],
            "flight_number": input_item['flight_number'],
            "upcoming": input_item['upcoming']
        }
        
        return LaunchModel(**launch_properties)