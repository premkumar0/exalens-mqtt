# Exalens MQTT Monitoring System

This project simulates the behavior of sensors, monitors their readings, and provides APIs to retrieve data based on specific criteria. It uses Docker containers to deploy various services and is designed to be easy to set up and interact with.

## Table of Contents

- [Installation](#installation)
- [Project Structure](#project-structure)
- [Design Choices](#design-choices)
- [Challenges and Solutions](#challenges-and-solutions)

## Installation

To run this project, follow these steps:

1. **Prerequisites**: Ensure you have Docker and Docker Compose installed on your system.

2. **Clone the Repository**: Clone this repository to your local machine.

   ```shell
   git clone https://github.com/premkumar0/exalens-mqtt.git
   cd exalens-mqtt
   ```

3. **Run the Docker Compose**: Use the following command to build and start the services.

   ```shell
   docker compose up -d --build
   ```

   or

   ```
   docker-compose up -d --build
   ```

4. **Set Up MongoDB**: Access the Mongo Express web interface at `http://localhost:8081`. Create a database named `mqtt_data` and a collection named `sensor_readings`.

Now, the entire system is up and running, ready to monitor sensor readings.

## Project Structure

### Services

1. **mosquitto**:

   - Configuration: The project uses Eclipse Mosquitto's Docker image, with configuration files mounted via volumes.
   - Purpose: This service sets up an MQTT broker to handle sensor data communication.

2. **mqtt-publisher**:

   - Configuration: A custom Python MQTT publisher image is used to simulate temperature and humidity sensor readings, which are then published using the MQTT broker.
   - Purpose: Emulates sensor data generation and publishing to specific topics.

3. **mqtt-subscriber**:

   - Configuration: A custom Python MQTT subscriber image subscribes to the MQTT topics, processes incoming data, and stores it in MongoDB and Redis.
   - Purpose: Collects and stores sensor data from MQTT.

4. **mongodb**:

   - Configuration: MongoDB server is set up using the official MongoDB Docker image.
   - Purpose: Stores sensor data in a MongoDB database.

5. **mongo-express** (optional):

   - Purpose: Provides a web interface for managing MongoDB databases and collections. Use it to create the necessary database and collection.

6. **fastapi-app**:

   - Configuration: A custom Python FastAPI application.
   - Purpose: Provides API endpoints to fetch sensor readings as per the challenge requirements.

7. **redis**:
   - Configuration: Redis server setup.
   - Purpose: Stores the latest ten sensor readings for fast access.

## Design Choices

This project was designed with the following considerations:

- **Docker Containers**: We use Docker to encapsulate and manage services for easy setup and scalability.

- **Data Storage**: Sensor readings are stored in both MongoDB and Redis. MongoDB is used for historical data, while Redis stores the latest ten sensor readings for fast access.

- **FastAPI**: FastAPI was chosen for its performance and simplicity in building RESTful APIs. It serves endpoints for retrieving sensor data.

- **Volumes**: Named volumes are utilized for persisting data and mounting configuration files, ensuring consistent use throughout the project.

## Challenges and Solutions

During the development of this project, we encountered several challenges:

- **Mosquitto Configuration**: Configuring network access and password authentication for the Mosquitto MQTT broker within a Docker service was challenging. Due to complexities, we compromised on allowing network access without authentication, which is not suitable for production deployment.

- **FastAPI Implementation**: Building the FastAPI application was a challenge, especially considering the requirement to fetch the latest ten sensor readings. Although I had no prior experience with FastAPI, my knowledge of Django helped me overcome this challenge.

We hope you find this project informative and well-structured. If you have any questions or need further clarification on any aspect of the code or documentation, please feel free to reach out.

Thank you for considering my submission, and I look forward to your feedback.

For more information about my profile, including my background, skills, and previous projects, please visit [my personal website](https://premkumar0.github.io/).
