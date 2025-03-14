import time

import requests

from mqtt_pipeline.pipeline import Middleware


class RestPutMiddleware(Middleware):
    def __call__(self, data, *args, **kwargs):
        result = self.send_to_rest_endpoint(self.middleware_config, data)
        return self.get_response(result, *args, **kwargs)

    def send_to_rest_endpoint(self, config, data):
        """
        Send data to REST endpoint with retry logic.

        Args:
            config (dict): Configuration dictionary with the following keys:
                - host (str): The URL of the REST endpoint
                - session (requests.Session): Session object to make a request
                - headers (dict): HTTP headers to include in the request
                - timeout (int/float): Request timeout in seconds
                - retries (int): Number of retry attempts if the request fails
                - retry_delay (int/float): Delay between retries in seconds

            data (str/dict): The payload to send to the REST endpoint

        Returns:
            None: This function returns early on successful request or after
                exhausting all retry attempts

        Raises:
            No exceptions are raised as they are caught and logged internally
        """
        for attempt in range(config.get("retries")):
            try:
                self.logger.info(
                    f"Sending data to endpoint: {config.get('host')}"
                )
                session = config.get("session")
                data_response = session.put(
                    f"{config.get('host')}/{config.get('path')}",
                    data=data,
                    headers=config.get("headers"),
                    timeout=config.get("timeout"),
                )

                if (
                    data_response.status_code >= 200
                    and data_response.status_code < 300
                ):
                    self.logger.info("Successfully sent data payload.")
                else:
                    self.logger.warning(
                        f"Failed to send data payload. Response: \
                        {data_response.content}"
                    )

                return

            except requests.exceptions.RequestException as e:
                self.logger.error(
                    f"Failed to send data to Urbit endpoint: \
                                  {e}"
                )

            # If we get here, the request failed
            if attempt < config.get("retries") - 1:
                self.logger.info(
                    f"Retrying in {config.get('retry_delay')} seconds... (Attempt \
                    {attempt + 1}/{config.get('retries')})"
                )
                time.sleep(config.get("retry_delay"))

        self.logger.error(
            f"Failed to send data to endpoint after {config.get('retries')} \
            attempts"
        )
