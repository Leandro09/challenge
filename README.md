# Summary

Etl with python to extract information from the api https://api.spacexdata.com/v5/launches/

---------------------

# Key Components

Python scripts are developed to simulate an ETL process.

A subset of the dataset properties essential for addressing the queries will be extracted. This approach aims to
streamline the challenge review process by minimizing complexity. However, the code can be adjusted as needed.

Issues are identified within the data, such as null entries in identifiers and negative values in time variables, 
among others. These types of problems can be rectified through techniques like imputation, thorough investigation, 
prediction models, or by selectively removing records based on data percentage, etc


# Running Tests
	1) Set up the Python environment by installing the required dependencies using the provided requirements file.
	2) Navigate to the root folder and execute the following command: python -m unittest discover tests
	3) Test cases can be located within the "tests" folder.
	
# Running the Solution

	1) Install Docker on your system.
	2) Open a terminal and execute the command "docker build -t etl-challenge:latest ." within the project folder.
	3) Start the solution by running "docker compose up" in the project folder.
	4) Review logs in the container files located in the "logs" folder. To access the PostgreSQL container, you can use a client like pgAdmin on your computer.
