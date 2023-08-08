import os
import sys
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_path)
from etl.transformer import Transformer
from etl.models import LaunchModel
from unittest.case import TestCase
from pydantic import ValidationError

class TestTransformer(TestCase):

    # Test with correct data to create a launch model
    def test_transformer_valid_launch(self):
        transformer = Transformer(
            raw_data=[
                {
                    "fairings": {
                        "reused": False,
                        "recovery_attempt": False,
                        "recovered": False,
                        "ships": []
                    },
                    "links": {
                        "patch": {
                            "small": "https://images2.imgbox.com/94/f2/NN6Ph45r_o.png",
                            "large": "https://images2.imgbox.com/5b/02/QcxHUb5V_o.png"
                        },
                        "reddit": {
                            "campaign": None,
                            "launch": None,
                            "media": None,
                            "recovery": None
                        },
                        "flickr": {
                            "small": [],
                            "original": []
                        },
                        "presskit": None,
                        "webcast": "https://www.youtube.com/watch?v=0a_00nJ_Y88",
                        "youtube_id": "0a_00nJ_Y88",
                        "article": "https://www.space.com/2196-spacex-inaugural-falcon-1-rocket-lost-launch.html",
                        "wikipedia": "https://en.wikipedia.org/wiki/DemoSat"
                    },
                    "static_fire_date_utc": "2006-03-17T00:00:00.000Z",
                    "static_fire_date_unix": 1142553600,
                    "net": False,
                    "window": 0,
                    "rocket": "5e9d0d95eda69955f709d1eb",
                    "success": False,
                    "failures": [
                        {
                            "time": 33,
                            "altitude": None,
                            "reason": "merlin engine failure"
                        }
                    ],
                    "details": "Engine failure at 33 seconds and loss of vehicle",
                    "crew": [],
                    "ships": [],
                    "capsules": [],
                    "payloads": [
                        "5eb0e4b5b6c3bb0006eeb1e1"
                    ],
                    "launchpad": "5e9e4502f5090995de566f86",
                    "flight_number": 1,
                    "name": "FalconSat",
                    "date_utc": "2006-03-24T22:30:00.000Z",
                    "date_unix": 1143239400,
                    "date_local": "2006-03-25T10:30:00+12:00",
                    "date_precision": "hour",
                    "upcoming": False,
                    "cores": [
                        {
                            "core": "5e9e289df35918033d3b2623",
                            "flight": 1,
                            "gridfins": False,
                            "legs": False,
                            "reused": False,
                            "landing_attempt": False,
                            "landing_success": None,
                            "landing_type": None,
                            "landpad": None
                        }
                    ],
                    "auto_update": True,
                    "tbd": False,
                    "launch_library_id": None,
                    "id": "5eb87cd9ffd86e000604b32a"
                }
            ]
        )
        res = transformer.transform_data()[0]
        self.assertEqual(res.id, '5eb87cd9ffd86e000604b32a')
    
    # Test a record without id
    def test_invalid_launch_record(self):
        data = {
            "id": None,
            "name": "Launch 1",
            "date_utc": "2023-08-01T12:00:00Z",
        }
        with self.assertRaises(ValidationError) as context:
            launch_model = LaunchModel(**data)

        self.assertEqual("validation error" in str(context.exception), True)
        
    # Test negativa value in altitude
    def test_invalid_altitude(self):
        raw_data={
          "fairings": {
            "reused": False,
            "recovery_attempt": False,
            "recovered": False,
            "ships": [
              
            ]
          },
          "links": {
            "patch": {
              "small": "https://images2.imgbox.com/94/f2/NN6Ph45r_o.png",
              "large": "https://images2.imgbox.com/5b/02/QcxHUb5V_o.png"
            },
            "reddit": {
              "campaign": None,
              "launch": None,
              "media": None,
              "recovery": None
            },
            "flickr": {
              "small": [
                
              ],
              "original": [
                
              ]
            },
            "presskit": None,
            "webcast": "https://www.youtube.com/watch?v=0a_00nJ_Y88",
            "youtube_id": "0a_00nJ_Y88",
            "article": "https://www.space.com/2196-spacex-inaugural-falcon-1-rocket-lost-launch.html",
            "wikipedia": "https://en.wikipedia.org/wiki/DemoSat"
          },
          "static_fire_date_utc": "2006-03-17T00:00:00.000Z",
          "static_fire_date_unix": 1142553600,
          "net": False,
          "window": 0,
          "rocket": "5e9d0d95eda69955f709d1eb",
          "success": False,
          "failures": [
            {
              "time": 33,
              "altitude": -520,
              "reason": "merlin engine failure"
            }
          ],
          "details": "Engine failure at 33 seconds and loss of vehicle",
          "crew": [
            
          ],
          "ships": [
            
          ],
          "capsules": [
            
          ],
          "payloads": [
            "5eb0e4b5b6c3bb0006eeb1e1"
          ],
          "launchpad": "5e9e4502f5090995de566f86",
          "flight_number": 1,
          "name": "FalconSat",
          "date_utc": "2006-03-24T22:30:00.000Z",
          "date_unix": 1143239400,
          "date_local": "2006-03-25T10:30:00+12:00",
          "date_precision": "hour",
          "upcoming": False,
          "cores": [
            {
              "core": "5e9e289df35918033d3b2623",
              "flight": 1,
              "gridfins": False,
              "legs": False,
              "reused": False,
              "landing_attempt": False,
              "landing_success": None,
              "landing_type": None,
              "landpad": None
            }
          ],
          "auto_update": True,
          "tbd": False,
          "launch_library_id": None,
          "id": "5eb87cd9ffd86e000604b32a"
        }
                

        with self.assertRaises(ValidationError) as context:
            launch_model = LaunchModel(**raw_data)

        self.assertEqual("validation error" in str(context.exception), True)