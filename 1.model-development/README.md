## Introduction
Simple ML Model Development README
In this section, I'll guide you through the process of developing a basic Machine Learning (ML) model. The purpose of this model is to predict the traffic volume on the I-94 ATR 301 westbound lane based on various features. We'll be using Python and Jupyter Notebook for this demonstration.

## Getting Started
### Locally
Clone this repository to your local machine:
git clone https://github.com/{your-username}/traffic-prediction.git
Navigate to the project directory (MLOPS):
Install the required dependencies. It's recommended to create a virtual environment before installing the dependencies:
pipenv shell
Run jupyter notebook cells

### Azure Cloud
Set up Azure VM
- install python
sudo apt-get update
sudo apt-get install python3.10
- create environments folder 
mkdir environments_folder
cd environments_folder

- create virtual environment
conda create --name my_env
conda activate my_env
conda install jupyter
jupyter notebook --no-browser --ip=0.0.0.0 --port=8888
ssh -i {~home/~/secret.pem} -N -L 8888:localhost:8888 <VM_username>@<VM_IP_ADDRESS>
copy code and run cells from the local jupyter notebook 



### Running the Model
Open the Jupyter Notebook file traffic_prediction.ipynb to follow along with the development process. This notebook contains step-by-step instructions and code cells that guide you through:

Data loading and preprocessing.
Feature selection and engineering.
Model selection and training.
Model evaluation.
Follow the instructions within the notebook cells to execute code and observe the results.

Generating Pickle File
As you progress through the notebook, you'll reach a section where you generate a pickle file containing the trained model, scaler, and DictVectorizer. This pickle file will be used in later sections for prediction.

Next Steps
Once you've completed the notebook and generated the pickle file, you can proceed to the next section of the project where you'll use the trained model to make predictions on new data.

Happy coding! 🚗📈


## Attribute Information

The dataset contains the following attributes:

holiday: Categorical feature representing US National holidays plus regional holidays such as the Minnesota State Fair.
temp: Numeric feature indicating the average temperature in Kelvin.
rain_1h: Numeric feature representing the amount of rain (in mm) that occurred in the hour.
snow_1h: Numeric feature indicating the amount of snow (in mm) that occurred in the hour.
clouds_all: Numeric feature representing the percentage of cloud cover.
weather_main: Categorical feature providing a short textual description of the current weather.
weather_description: Categorical feature giving a longer textual description of the current weather.
date_time: DateTime feature indicating the hour of the data collected in local CST time.
traffic_volume: Numeric feature representing the hourly I-94 ATR 301 reported westbound traffic volume.
