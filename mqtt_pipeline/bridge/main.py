import paho.mqtt.client as mqtt


def start_bridge(pipeline):
    """
    Main function to start the MQTT client, maintain the connection, and
    execute the provided REST behavior.

    Args:
        pipeline (object): An object containing:
            - config (dict): Configuration dictionary with the following keys:
                - mqtt_client_id (str): Unique identifier for the MQTT client
                - mqtt_username (str): Username for MQTT authentication \
                    (optional)
                - mqtt_password (str): Password for MQTT authentication \
                    (optional)
                - mqtt_broker (str): Hostname or IP address of the MQTT broker
                - mqtt_port (int): Port number of the MQTT broker
                - mqtt_topic (str): Topic to subscribe to for receiving \
                    messages
            - logger (logging.Logger): Logger object for recording events
            - process (callable): Callback function to handle incoming MQTT \
                messages

    Returns:
        None: This function runs until interrupted or an error occurs

    Raises:
        No exceptions are raised as they are caught and logged internally

    Note:
        The function will disconnect the MQTT client when interrupted by
        keyboard interrupt or when an exception occurs.
    """

    def _on_connect(client, userdata, flags, rc):
        """Callback for when the client connects to the MQTT broker."""
        if rc == 0:
            pipeline.logger.info(
                f"Connected to MQTT broker at \
                {pipeline.config['mqtt_broker']} and port \
                {pipeline.config['mqtt_port']}"
            )
            client.subscribe(pipeline.config["mqtt_topic"])
            pipeline.logger.info(
                f"Subscribed to topic: \
                                 {pipeline.config['mqtt_topic']}"
            )
        else:
            pipeline.logger.error(
                f"Failed to connect to MQTT broker, return code: {rc}"
            )

    # Setup MQTT client
    client = mqtt.Client(client_id=pipeline.config["mqtt_client_id"])

    # Set username and password if provided
    if pipeline.config["mqtt_username"] and pipeline.config["mqtt_password"]:
        client.username_pw_set(
            pipeline.config["mqtt_username"], pipeline.config["mqtt_password"]
        )

    # Set callbacks
    client.on_connect = _on_connect
    client.on_message = pipeline.process

    try:
        # Connect to MQTT broker
        pipeline.logger.info(
            f"Connecting to MQTT broker at \
            {pipeline.config['mqtt_broker']} with port \
            {pipeline.config['mqtt_port']}..."
        )
        client.connect(
            pipeline.config["mqtt_broker"],
            pipeline.config["mqtt_port"],
            60,
        )

        # Start the loop
        pipeline.logger.info("Starting MQTT loop...")
        client.loop_forever()

    except KeyboardInterrupt:
        pipeline.logger.info("Service interrupted by user")
        client.disconnect()

    except Exception as e:
        pipeline.logger.exception(f"Error in main loop: {e}")
        client.disconnect()
