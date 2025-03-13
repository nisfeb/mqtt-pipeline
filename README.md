# MQTT Pipeline

This service listens to an MQTT channel and forwards messages to middleware pipeline.

## Features

- Mosquitto MQTT broker with optional authentication
- Python service that converts MQTT messages into REST API POST requests
- Automatic JSON conversion of MQTT payloads
- Configurable retry mechanism for failed REST API calls
- Full Docker containerization
- Easy setup and configuration

## Prerequisites

- Docker and Docker Compose installed
- Basic understanding of MQTT and REST APIs

## Setting Up Authentication (Optional)

If you want to secure your MQTT broker with username/password authentication:

### Method 1: Using the -b flag (simple but less secure)

```bash
# Start the containers first
docker-compose up -d

# Create a user with password
docker exec mqtt-broker mosquitto_passwd -b /mosquitto/config/passwords.txt myuser mypassword

# Enable authentication in the configuration
```

Edit `mosquitto/config/mosquitto.conf` and uncomment/modify these lines:
```
password_file /mosquitto/config/passwords.txt
allow_anonymous false
```

Restart the service to apply changes:
```bash
docker-compose restart mosquitto
```

### Method 2: Interactive password entry

```bash
docker exec -it mqtt-broker mosquitto_passwd -c /mosquitto/config/passwords.txt myuser
```

Follow the prompts to enter your password, then enable authentication as described in Method 1.

### Don't forget to update the bridge service

After enabling authentication, update the environment variables in your docker-compose.yml file:

```yaml
mqtt-rest-bridge:
  # ... other configuration ...
  environment:
    - MQTT_USERNAME=myuser
    - MQTT_PASSWORD=mypassword
    # ... other environment variables ...
```

## Testing the Setup

You can test the setup by publishing a message to the MQTT broker:

```bash
# Without authentication
docker exec mqtt-broker mosquitto_pub -t "data/sensor" -m '{"temperature": 25.4, "humidity": 68}'

# With authentication
docker exec mqtt-broker mosquitto_pub -t "data/sensor" -m '{"temperature": 25.4, "humidity": 68}' -u myuser -P mypassword
```

## Checking Logs

To verify that everything is working correctly, you can check the logs:

```bash
# All services
docker-compose logs -f

# Just the MQTT bridge
docker-compose logs -f mqtt-rest-bridge 

# Just the MQTT broker
docker-compose logs -f mosquitto
```

## Configuration Options

The MQTT to REST bridge service can be configured using the following environment variables:

| Environment Variable | Description | Default |
|---|---|---|
| `MQTT_BROKER` | MQTT broker hostname or IP | `localhost` |
| `MQTT_PORT` | MQTT broker port | `1883` |
| `MQTT_TOPIC` | MQTT topic to subscribe to | `data/sensor` |
| `MQTT_USERNAME` | MQTT username (if authentication is enabled) | `None` |
| `MQTT_PASSWORD` | MQTT password (if authentication is enabled) | `None` |
| `MQTT_CLIENT_ID` | Client ID for MQTT connection | `mqtt-rest-bridge` |

## Troubleshooting

### MQTT Connection Issues
- Verify that the MQTT broker is running: `docker ps | grep mqtt-broker`
- Check the MQTT broker logs: `docker-compose logs mosquitto`
- Ensure authentication details are correct if authentication is enabled

### REST API Issues
- Verify the REST endpoint is accessible from the container
- Check the bridge service logs: `docker-compose logs mqtt-rest-bridge`
- Verify that the REST endpoint can handle the message format being sent

### Permission Issues
If you encounter permission issues with the mounted volumes, ensure that the directories have the correct ownership:

```bash
mkdir -p mosquitto/data mosquitto/log
chmod -R 777 mosquitto/data mosquitto/log
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
