## Model Deployment using Flask and Docker
This repository demonstrates the process of deploying machine learning models using Flask and Docker. Below are the steps to follow:

### Getting Started:
- Navigate to the main directory (MLOPS):
  cd ./MLOPS
- activate enviroment:
  pipenv shell
- build docker image: 
  docker build -t traffic-volume-prediction:v1 .
- run docker cntainer: 
  docker run -it --rm -p 9696:9696 traffic-volume-prediction:v1
- Testing the deployment: 
  python ./deployment/web-service/test.py

This command will assess the deployed model's functionality. The script test.py interacts with the deployed Flask service to ensure that the model is working as expected.

Remember to use the virtual environment named (mlops) to execute the provided commands. The prompt (mlops) indicates that you are operating within the correct environment for this deployment.


![./4.deployment/web-service](<../pictures/local deployment.png>)