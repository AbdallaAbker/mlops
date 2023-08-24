# MLOps Pipeline Guide

This guide walks you through the steps to follow the pipeline code from 1 to 4 for your machine learning project.

## Pipeline Overview

1. **data_prep_pipeline:** Ingests and transforms data using DictVectorizer & MaxAbsScaler. Outputs train, test, and validation datasets as pickle files.
2. **train_pipeline:** Performs simple model training.
3. **hyper-param-opt_pipeline:** Performs hyperparameter tuning.
4. **register_model:** Registers the best model.

## Local Setup and Execution

To run the pipeline steps from 1 to 4 locally, follow these steps:

1. Navigate to the MLOPS directory.
2. Create a project folder:
3. Create an MLflow tracker folder:
4. Launch the MLflow service:
5. Install the Azure CLI and login:
6. Export storage account environment variables:


## Azure Cloud Setup

To set up your project on Azure cloud, follow these steps:

1. **Azure VM Setup:**
- Install Python on the VM:
  sudo apt-get update
  sudo apt-get install python3.10
- Create an environments folder:
  mkdir environments_folder
  cd environments_folder
- Create a virtual environment and install Jupyter:
  conda create --name my_env
  conda activate my_env
  conda install jupyter
  jupyter notebook --no-browser --ip=0.0.0.0 --port=8888
  ssh -i ~/secret.pem -N -L 8888:localhost:8888 <VM_username>@<VM_IP_ADDRESS>

2. **Notebook Setup:**
- In the notebook, import MLflow and set the server URI:
  import mlflow
  remote_server_uri = "0.0.0.0"
  mlflow.set_tracking_uri(f"http://{remote_server_uri}:5000")

- Set the MLflow experiment:
  exp_name = "<MY_EXPERIMENT_NAME>"
  mlflow.set_experiment(exp_name)

3. Run the rest of the code in your Jupyter notebook.

Make sure to replace placeholders like `<directory_on_vm>`, `<blob_container_name>`, `<storage_account>`, `<VM_username>`, `<VM_IP_ADDRESS>`, and `<MY_EXPERIMENT_NAME>` with your actual values.

Follow these steps to effectively manage your machine learning pipeline and experiments both locally and on Azure.


![Alt text](<Prefect Run.png>)