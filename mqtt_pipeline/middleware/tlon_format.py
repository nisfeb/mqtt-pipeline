from mqtt_pipeline.pipeline import Middleware


class TlonFormatMiddleware(Middleware):
    """
    Middleware for formatting and sending Meshtastic messages to Urbit using the Tlon format.

    This middleware transforms Meshtastic protocol messages into the format required by
    Urbit's Channels application, then sends the formatted data to a REST endpoint.

    Attributes:
        Inherits all attributes from the Middleware base class:
        - get_response (callable): Function to call the next middleware in the chain
        - config (dict): Global configuration dictionary
        - middleware_config (dict): Configuration specific to this middleware
        - logger (Logger): Logger instance for this middleware

    Required Configuration (in middleware_config):
        - urbit_id (str): The Urbit ID (ship) to send the message to/from
        - urbit_channel_nest (str): The channel nest path in Urbit
        - (Other configuration required by send_to_rest_endpoint method)
    """
    def __call__(self, data, *args, **kwargs):
        """
        Process the Meshtastic message by formatting it for Urbit and sending it.

        Args:
            data: The Meshtastic message envelope to process
            _args: Positional arguments to pass to the next middleware
            **kwargs: Keyword arguments to pass to the next middleware

        Returns:
            The result of passing the formatted data through the rest of the middleware chain

        Note:
            This method calls send_to_rest_endpoint to transmit the formatted payload
            to the configured endpoint before continuing the middleware chain.
        """
        result = self.send_to_rest_endpoint(self.middleware_config, data)
        return self.get_response(result, *args, **kwargs)

    def tlon_format(self, config, envelope):
        """
        Format a Meshtastic message envelope into Urbit's Channels message format.

        This method extracts information from the Meshtastic envelope and formats it
        into a JSON payload suitable for posting to an Urbit ship's Channels application.

        Args:
            config (dict): Configuration dictionary containing Urbit settings
            envelope: Meshtastic message envelope containing the message data

        Returns:
            list: A list containing a single dictionary with the formatted Urbit poke action

        Format details:
            - Formats the message as a chat post with the original message text
            - Adds a signature line in a blockquote showing the message source
            - Includes metadata like timestamp and author
            - Uses a global PAYLOAD_ID to track message sequence

        Note:
            Requires the global variable PAYLOAD_ID to be initialized elsewhere
        """
        config = self.middleware_config
        mesh_payload = envelope.packet.decoded.payload.decode('utf-8')
        mesh_channel = envelope.channel_id
        mesh_user = envelope.gateway_id
        mesh_payload_time = envelope.packet.rx_time
        mesh_message = f"{mesh_payload}"
        mesh_signature = f"{mesh_user} via {mesh_channel}"
        global PAYLOAD_ID
        PAYLOAD_ID += 1
        urbit_payload = [
            {
                "id": PAYLOAD_ID,
                "action": "poke",
                "ship": config.get('urbit_id').replace("~", ""),
                "app": "channels",
                "mark": "channel-action",
                "json": {
                    "channel": {
                        "nest": config.get('urbit_channel_nest'),
                        "action": {
                            "post": {
                                "add": {
                                    "kind-data": {
                                        "chat": None
                                    },
                                    "author": config.get('urbit_id'),
                                    # milliseconds since epoch from sender
                                    "sent": mesh_payload_time * 1000,
                                    "content": [
                                        {
                                            "inline": [
                                                mesh_message,
                                                {"break": None},
                                                {"blockquote": [
                                                    mesh_signature,
                                                    {"break": None},
                                                ]}
                                            ]
                                        }
                                    ]
                                }
                            }
                        }
                    }
                }
            }
        ]
        return urbit_payload
