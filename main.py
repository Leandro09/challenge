import os
"""Run this script to launch the pipeline"""

from etl.master import run_etl

if __name__ == "__main__":

    # Get url or use the default
    api_url = os.environ.get("API_URL", "https://api.spacexdata.com/v5/launches/")
    run_etl(api_url)
