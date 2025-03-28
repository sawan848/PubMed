import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO,format='[%(asctime)s]: %(message)s')

project_name="PubMed"


list_of_files =[
    ".github/workflows/.gitkeep",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/utils/common.py",
    f"src/{project_name}/database/__init__.py",
    f"src/{project_name}/api/__init__.py",
    f"src/{project_name}/api/routes.py",
    f"src/{project_name}/controllers/__init__.py",
    f"src/{project_name}/controllers/pubmed_controller.py",
    f"src/{project_name}/database/models.py",
    f"src/{project_name}/middlewares/__init__.py",
    f"src/{project_name}/services/__init__.py",
    f"src/{project_name}/services/pubmed_service.py",
    f"src/{project_name}/constants/__init__.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/configuration.py",
    "app.py",
    "main.py",
    "config/config.yaml",
    "Dockerfile",
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir,filename=os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir,exist_ok=True)
        logging.info(f"Creating diectory:{filedir} for the file {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath)==0):
        with open(filepath,'w') as f:
            pass
            logging.info(f"Creating empty file: {filename}")
            
    else:
        logging.info(f"{filename} is already exists")
