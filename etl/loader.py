from typing import List
from .models import Base  # Import the Base class from models.py
from sqlalchemy import create_engine
from .models import LaunchModel, LaunchModelOrm, CoreModelOrm, FailureModelOrm
from .loggerClass import LoggerObject
from sqlalchemy.orm import sessionmaker
import psycopg2
import os
from psycopg2 import IntegrityError


class Loader:


    def __init__(self, launch_data: List[LaunchModel]):
        """
        This class loads transformed data into the database

        Args:
            launch_data: transformed data
        """
        self.launch_data = launch_data
        self.logger = LoggerObject().get_logger('loader_log', 'logs/loader_logs.txt')
        db_url = self.create_database()
        #self.engine = create_engine('postgresql://postgres:admin@localhost:5432/spacex')
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)
        


    
    def create_database(self):
        """
        Creates the 'spaceX_db' database if it doesn't exist
        """
        database_name = 'spacex'
        db_host = 'postgres'  # Use the container name as the hostname
        db_port = int(os.environ.get("POSTGRES_PORT", 5432))    # Default to 5432 if not set
        db_name = os.environ.get("POSTGRES_DB", "postgres")    # Default to postgres if not set
        db_user = os.environ.get("POSTGRES_USER", "postgres")  # Default to postgres if not set
        db_password = os.environ.get("POSTGRES_PASSWORD", "admin")  # Default to mypassword if not set
        
        # Define url to use with sqlalchemy
        db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{database_name}"

        
        try:
            # Connect to the default "postgres" database to check if the new database exists
            connection = psycopg2.connect(
                dbname=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port
            )
            
            # Set autocommit to True to avoid transaction blocks
            connection.autocommit = True  

            cursor = connection.cursor()

            # Check if the database already exists
            cursor.execute("SELECT datname FROM pg_catalog.pg_database WHERE lower(datname)=%s;", (database_name,))
            result = cursor.fetchone()

            if result is None:
                # Create the database if it doesn't exist
                cursor.execute(f"CREATE DATABASE {database_name};")
                self.logger.info(f"Database {database_name} created.")
                print(f"Database {database_name} created.")
                
            else:
                print(f"Database {database_name} already exists.")
                self.logger.info(f"Database {database_name} already exists.")

            cursor.close()
            connection.close()
        except Exception as e:
            db_url = ""
            self.logger.error(e)
            
        return db_url
        



    def load_data(self):
        """
        Inserts data into the database
        """
        session = self.Session()
        print("Start execution")
        
        try:
            for element in self.launch_data:
                try:
                    # Insert LaunchModel data
                    launch_data = element.dict(exclude_unset=True)
                    
                    # Get information about cores and failures
                    cores_data = launch_data.pop('cores', [])
                    failures_data = launch_data.pop('failures', [])
                    
                    launch_orm = LaunchModelOrm(**launch_data)
                    
                    session.add(launch_orm)

                    # Create CoreModelOrm instances and associate them with the launch_orm
                    for core_data in cores_data:
                        core_orm = CoreModelOrm(**core_data)
                        # create foreign key to associate two tables
                        core_orm.launch_id = launch_orm.id
                        session.add(core_orm)

                    # Create FailureModelOrm instances and associate them with the launch_orm
                    for failure_data in failures_data:
                        failure_orm = FailureModelOrm(**failure_data)
                        failure_orm.launch_id = launch_orm.id 
                        session.add(failure_orm)
                    session.commit()
                except IntegrityError as e:
                    session.rollback()
                    self.logger.error(f"Skipping duplicate record: {element}")
                except Exception as e:
                    session.rollback()
                    self.logger.error(f"Error inserting record: {element} - {str(e)}")
                
        except Exception as e:
            session.rollback()
            self.logger.error(f"Error during ELT: {str(e)}")
        finally:
            session.close()
        print("ELT was completed")

            
