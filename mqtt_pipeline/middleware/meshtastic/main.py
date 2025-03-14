from .protobufs.meshtastic import mqtt_pb2
from mqtt_pipeline.pipeline import Middleware


class MeshtasticMiddleware(Middleware):
    """
    Middleware for processing Meshtastic messages received via MQTT.

    This middleware parses the Meshtastic protocol buffer messages into
    ServiceEnvelope objects for further processing. It handles the protobuf
    deserialization of the Meshtastic message format.
    https://buf.build/meshtastic/protobufs/docs/main:meshtastic#meshtastic.ServiceEnvelope

    Attributes:
        logger: Logger instance used for logging events and errors

    Expected message format example:
        packet {
          from: 853720060
          to: 4294967295
          channel: 2
          decoded {
            portnum: TEXT_MESSAGE_APP
            payload: "This is the text of the message."
          }
          id: 94610745
          rx_time: 1741373725
          hop_limit: 3
          priority: HIGH
          hop_start: 3
          channel_id: "TheChannelName"
          gateway_id: "!07abd89"
        }
    """
    def __call__(self, data, *args, **kwargs):
        """
        Process the incoming MQTT message and transform using the parse method.

        Args:
            data: An object containing:
                - topic (str): The MQTT topic the message was received on
                - payload (bytes): The raw protobuf message data
            _args: Positional arguments to pass to get_response
            **kwargs: Keyword arguments to pass to get_response

        Returns:
            The result of self.get_response() after parsing the data
        """
        # Transform data
        result = self.parse(data)
        return self.get_response(result, *args, **kwargs)

    def parse(self, data):
        """
        Parse the Meshtastic ServiceEnvelope from the MQTT payload data.

        Args:
            data: An object containing:
                - topic (str): The MQTT topic the message was received on
                - payload (bytes): The raw protobuf message data

        Returns:
            mqtt_pb2.ServiceEnvelope: The parsed Meshtastic message envelope

        Logs:
            - Info message when a message is received
            - Info message with the parsing result
            - Exception details if parsing fails
            - Exception details if any other error occurs
        """
        # Time to parse the Meshtastic Envelope
        try:
            self.logger.info(f"Message received on topic {data.topic}")
            envelope = mqtt_pb2.ServiceEnvelope()  # Init a new (empty) value
            try:
                retval = envelope.ParseFromString(data.payload)
                self.logger.info(f"Parsed {retval}")
            except Exception as e:
                self.logger.exception(f"Protobuf parsing failed: {e}")
        except Exception as e:
            self.logger.exception(f"Error processing message: {e}")

        return envelope
