# datahighway-opendata
parse and analyse open linked data

## Prerequisites

Make sure you have Docker and python 3 installed on your machine. You can download Docker from [here](https://www.docker.com/get-started).

## Clone the Repository

Clone the repository to your local machine using the following command:

```bash
git clone https://github.com/netsensesrl/datahighway-opendata
cd datahighway-opendata
```

Move to the ckan_sources folder if you want to collect packages or to the ngsi_ld folder if you want to manage the broker

## ckan_sources usage
Create a ".env" file. In the file, define an environment variable MONGO_IP with value "localhost" if you want to use the script without instantiating a docker container, otherwise enter mongodb://<ip_address>:27017, replacing ip_adress with the ip of the mongo docker container.

```bash
MONGO_IP=localhost
```

or 

```bash
MONGO_IP=mongodb://<ip_address>:27017
```

## Run the MongoDB Docker Container

Run the container with the following command:

```bash
docker run -d --name mongo -p 27017:27017 mongo
```

## Using the script without a docker container
### Install Python Requirements

Install the required Python packages using the following command:

```bash
pip install -r requirements.txt
```

## Run the script
```bash
python3 main.py
```

## Using the script with a docker container
### Build opendata-update.dockerfile
```bash
docker build -f "./opendata-update.dockerfile" -t datahighwayopendata:latest "."
```

### Run container
After building the image run
```bash
docker run --name opendata-update datahighwayopendata:latest
```

## Output

Once the script is running, wait for it to finish fetching all the packages from the source. It may be helpful to download MongoDB Compass to analyze these packages
