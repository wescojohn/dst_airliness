# What does it do ?
 We retrieve data from the Airlabs API. We search for real-time aircraft, airport and airline information. We collect in data frames. Then we insert them into two different databases. Real-time data is stored in a MongoDB database, and static data such as airport and airline information is stored in an sql database. The data is visualized using a Flask API.
# Installation
### Clone the repo
```
git clone https://github.com/wescojohn/dst_airliness.git
```
## Running the project
```
docker-compose up
```
## Check your database
When the flask service is running, you can
tape in your browser this address:
```
localhost:5000 or IP_VM:5000
```
### View your data on the map
Viewing may take a few seconds.
