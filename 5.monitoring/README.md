### Getting Started:
- Navigate to the main directory (MLOPS):
  cd ./MLOPS
- activate enviroment:
  pipenv shell
- Navigate into monitoring folder
  cd ./MLOPS/5.monitoring
  you can either use the pipenv or activate the local env (monitorvenv)
- build docker-compse: 
  docker-compose up --build
- Start sending data to db
  python ./send_data.py

You can browse your db here on localhost here:
http://localhost:8080

Choose:
System: PostgresSQL
Server: db
Username: postgres
password: example
Database: test
and log in 

You can browse grafana page on localhost here: 
http://localhost:3000/ 
your initial username/password is admin/admin




![Alt text](<../pictures/posgres db.png>)


![Alt text](<../pictures/grafan dummy test.png>)