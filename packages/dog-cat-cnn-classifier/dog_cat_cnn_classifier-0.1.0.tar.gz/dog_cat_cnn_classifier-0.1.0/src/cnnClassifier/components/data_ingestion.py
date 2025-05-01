import os
import zipfile
from cnnClassifier import get_logger
from cnnClassifier.utils.common import get_size
from cnnClassifier.entity.config_entity import DataIngestionConfig
from dotenv import load_dotenv
import json
load_dotenv(dotenv_path='.env')  
logger = get_logger(name= "data_ingestion_logger", log_dir="logs", log_filename="01_data_ingestion.log")

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config
    
    def download_file(self)-> str:
        '''
        Fetch data from the url
        '''

        try: 
            # Load credentials
            dataset_url = self.config.source_URL
            username = os.getenv("KAGGLE_USERNAME") 
            key = os.getenv("KAGGLE_KEY") 

            # Create kaggle.json content
            kaggle_api = {
                "username": username,
                "key": key
            }

            # Save kaggle.json in ~/.kaggle/
            kaggle_dir = os.path.expanduser("~/.kaggle")
            os.makedirs(kaggle_dir, exist_ok=True)
            with open(os.path.join(kaggle_dir, "kaggle.json"), "w") as f:
                json.dump(kaggle_api, f)
            os.chmod(os.path.join(kaggle_dir, "kaggle.json"), 0o600)

            # Extract dataset slug
            dataset = dataset_url.split("/")[-2] + "/" + dataset_url.split("/")[-1]

            # Path where the zip will be saved (including filename as data.zip)
            zip_download_path = self.config.local_data_file
            zip_dir = os.path.dirname(zip_download_path)
            os.makedirs(zip_dir, exist_ok=True)

            # Download the dataset and rename to data.zip
            logger.info(f"Downloading data from {dataset_url} into file {zip_download_path}")
            os.system(f"kaggle datasets download -d {dataset} -p {zip_dir}") 
            downloaded_zip = [f for f in os.listdir(zip_dir) if f.endswith('.zip')]
            logger.info(f"Downloaded data from {dataset_url} into file {zip_download_path}")

            if downloaded_zip:
                original_zip_path = os.path.join(zip_dir, downloaded_zip[0])
                os.rename(original_zip_path, zip_download_path)
            else:
                raise FileNotFoundError("Dataset download failed or no .zip file found.")
            

        except Exception as e:
            raise e
        
    
    def extract_zip_file(self):
        """
        zip_file_path: str
        Extracts the zip file into the data directory
        Function returns None
        """
        unzip_path = os.path.join(self.config.unzip_dir, "dataset") 
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)
