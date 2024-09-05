# Flask-CRUD-Docker
This is a web app built using Python's Flask Framework and containerized using docker. 


# Task
Create a CRUD flask application and containerize it:
1. It should have 2 components, simple flask app and Postgres DB with tables initialized. 
2. As soon as postgres container is launched, it should automatically spin up db, schema and tables we need.
3. Execute DDL on postgres container to create tables via code -> Use any automation tool for this. This step should later be done via docker compose wherein when the container is deployed, the db, schema and tables should also be ready.
4. Flask app should display all Users by querying the `Users` table from DB table hosted in container -> use jinja2 base.html template that reads data using GET call to the flask app and gets all the rows from user table. Should also support post, update and delete to have CRUD functionality.
5. Later, also containerize the flask app and use docker compose to run both flask server and postgres server in containers, these containers should have communication between them! By this you will also learn about inter container commumnication. And then expose the port of postgres to flask container, and expose the flask app's port to the local machine


## How to setup this project to run in one go
1. Go inside the project folder and run `docker compose up`. This will run the docker-compose.yml file that will spin up both flask app and the postgres DB.
    a. We have linked both these container for `icc` -> inter container communication. They share the same *bridge* network. So they will be able to communicate with each other.
2. After the `docker compose up` is done running, go to `localhost:8082` to run the flask app. This flask app is mapped to 8082 to run in local server. From here we will be able to access the full app.
3. We have Dockerfile which is used to build custom image for our flask-app. Docker compoose uses this Dockerfile when we do `docker compose up`
4. volumes and network configuration are enough as they are described, as we just need 2 containers to be on same network and the default driver/ network mode is bridge, so we don't have to specify anything explicitly.

We can do this as well to be more specific, but it's not needed.
```
networks:
  flask-postgres-network:
    driver: bridge
    driver_opts:
      com.docker.network.bridge.enable_icc: "true"  # Allows communication between containers
      com.docker.network.bridge.enable_ip_masquerade: "true"  # Allows containers to access external networks
```

5. For volumes:
./ (current directory): This represents the current working directory where your docker-compose.yml file is located. When you run docker-compose up, Docker looks for the postgres-init folder in this directory.
and we mount postgres-init to folder in postgres container, wherein if we place files, it will be automatically run in aplhabetical order as soon as the container is run

```
    volumes:
      - ./postgres-init:/docker-entrypoint-initdb.d
```

## For manual running and debugging
### To run postgres container:

```
docker run --name vijeth-postgres -e POSTGRES_PASSWORD=mysecretpassword123 -v ${PWD}\postgres-init:/docker-entrypoint-initdb.d -p 8080:5432 -d postgres
```
`-e POSTGRES_PASSWORD=mysecretpassword` : Sets the password for the postgres user. You can change it to whatever you want, make sure to use same password when tunnelling through DB client.

`-v $(pwd)/postgres-init:/docker-entrypoint-initdb.d` : Mounts the local postgres-init directory to the /docker-entrypoint-initdb.d directory inside the container. All .sql files in this directory will be executed in alphabetical order upon initialization.
We have V1 -> DDL and V2 DML file, this will be executed in order and once the container has spun up, we will have database, schema and tables ready to go.
/docker-entrypoint-initdb.d is responsible for auto initializing the DB. It executes sql files inside it automatically on spin up.


`-p 5432:5432` : Maps port 5432 on the local machine to port 5432 in the container.

`-d postgres` : Runs the container in detached mode using the PostgreSQL image.


### To go to postgres console on the container as interactive tty terminal:
```
docker exec -it vijeth-postgres psql -U postgres
```

## Flask
### To create docker image from the Dockerfile
```
docker build -t vijeth-flask .
```
### Run the container from the image
```
docker run  -p 5000:5000 -it vijeth-flask
```

### To make the postgres container stateful, atleast when running containers locally
1. Run this command
```
docker run --name vijeth-postgres -e POSTGRES_PASSWORD=mysecretpassword123 -v ${PWD}\postgres-init:/docker-entrypoint-initdb.d -v postgres-data:/var/lib/postgresql/data -p 8080:5432 -d postgres
```
Mount the volume to the PostgreSQL container’s data directory (/var/lib/postgresql/data), which is where PostgreSQL stores its database files.
`-v postgres-data:/var/lib/postgresql/data` mounts the volume postgres-data to the PostgreSQL data directory inside the container.
When you recreate the container using this volume, all inserted records will persist.

We don't need to create any local directory named postgres-data. It's the name of docker volume that will be create. You can see the volumes created by running 
`docker volume ls`
```
DRIVER    VOLUME NAME  
local     postgres-data
```
It will also be visible in the Docker desktop volumes console.

How It Works:
The PostgreSQL data is stored in the volume (postgres-data in this case).
When you stop or remove the container, the volume and the data remain.
When you run a new container and mount the same volume (postgres-data), it will have access to the previous data.