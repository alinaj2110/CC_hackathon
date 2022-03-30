# CC_hackathon
Dockerized Application using RabbitMQ to mimic a ride sharing micro-service

Full Problem Statement: [CloudHack Problem Statement 2](https://github.com/Teaching-Assistants-of-Cloud-Computing/CloudHack/tree/master/Problem%20Statement%202#readme)

# Dependencies
* `Docker`
* `Docker Compose`
* `RabbitMQ`
* `Flask`
* `MongoDB`

# Details of the Project

# Running the Project
* Building the Docker Compose file:
   
      docker-compose build
* Running the Docker Compose file:

      docker-compose up
* Sending a Post request to /new_ride via terminal:

      curl -X POST http://127.0.0.1:5000/new_ride \
      -H "Content-Type: application/json" \
      -d '{"pickup":"STREET 1","destination":"STREET 2","time": 30, "cost": 200, "seats":4}
* Viewing logs of each container separately:

      docker logs -f CONTAINER_NAME
* Stop the docker compose using `Ctrl+C`
