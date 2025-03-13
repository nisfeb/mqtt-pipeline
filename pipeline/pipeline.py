import logging
import uuid
import os
from typing import Dict, Any, Optional

# Setup a default shared logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s - %(message)s'
)


class Pipeline:
    """
    A data processing pipeline that manages a chain of middleware components.

    This class implements a middleware chain pattern where each piece of data flows
    through a series of middleware processors that can transform, validate, or enrich
    the data before passing it to the next component.

    The pipeline uses a reverse-wrapped pattern where each middleware wraps around
    the next middleware in the chain, with the core processing function at the center.

    Attributes:
        middleware_stack (callable): The compiled middleware chain
        middleware_classes (list): List of middleware classes to be included in the pipeline
        config (dict): Configuration dictionary for the pipeline and middlewares
        logger (Logger): Logger instance for recording events throughout the pipeline
    """
    def __init__(self, config: Optional[Dict[str, Any]] = None, logger=None):
        """
        Initialize the pipeline with configuration and logger.

        Args:
            config (Optional[Dict[str, Any]], optional): Dictionary of configuration
                parameters that will override the default settings. Defaults to None.
            logger (Logger, optional): Logger instance to use for logging. If None,
                a new logger will be created. Defaults to None.

        Default Configuration:
            - mqtt_broker (str): MQTT broker hostname or IP address. Default: "localhost"
            - mqtt_port (int): MQTT broker port. Default: 1883
            - mqtt_topic (str): MQTT topic to subscribe to. Default: "data/sensor"
            - mqtt_username (str): Username for MQTT authentication. Default: None
            - mqtt_password (str): Password for MQTT authentication. Default: None
            - mqtt_client_id (str): Client ID for MQTT connection. Default: "mqtt-rest-bridge"

        Note:
            Default values are loaded from environment variables if available.
        """
        self.middleware_stack = None
        self.middleware_classes = []
        self.config = {
            'mqtt_broker': os.getenv("MQTT_BROKER", "localhost"),
            'mqtt_port': int(os.getenv("MQTT_PORT", 1883)),
            'mqtt_topic': os.getenv("MQTT_TOPIC", "data/sensor"),
            'mqtt_username': os.getenv("MQTT_USERNAME", None),
            'mqtt_password': os.getenv("MQTT_PASSWORD", None),
            'mqtt_client_id': os.getenv("MQTT_CLIENT_ID", "mqtt-rest-bridge"),
        }
        if config:
            self.config.update(config)

        # Use provided logger or create a default one
        if logger is None:
            self.logger = logging.getLogger("pipeline")
        else:
            self.logger = logger

    def add_middleware(self, middleware_class):
        """
        Add a middleware class to the pipeline.

        Args:
            middleware_class: A middleware class (not instance) that will be
                initialized when the pipeline is built

        Returns:
            self: Returns the pipeline instance for method chaining

        Example:
            pipeline = Pipeline().add_middleware(AuthMiddleware).add_middleware(LoggingMiddleware)
        """
        self.middleware_classes.append(middleware_class)
        return self

    def build_middleware_stack(self):
        """
        Build the middleware stack by instantiating each middleware class.

        This method creates the middleware chain by wrapping each middleware
        around the next one in reverse order, with the innermost being the
        core processing function.

        Note:
            This method is called automatically the first time process() is called
            if the middleware_stack hasn't been built yet.
        """
        # Start with the innermost function
        handler = self.process_core

        # Wrap each middleware around it
        for middleware_class in reversed(self.middleware_classes):
            handler = middleware_class(
                get_response=handler,
                config=self.config,
                logger=self.logger
            )

        self.middleware_stack = handler

    def process_core(self, data, *args, **kwargs):
        """
        Core processing function that sits at the center of the middleware stack.

        This method represents the innermost function of the middleware chain.
        By default, it simply logs a debug message and returns the data unchanged.
        Subclasses may override this method to provide custom core processing.

        Args:
            data: The data to process
            _args: Positional arguments passed through the middleware chain
            **kwargs: Keyword arguments passed through the middleware chain

        Returns:
            The processed data (unchanged by default)
        """
        self.logger.debug("Core processing executed")
        return data

    def process(self, data, *args, **kwargs):
        """
        Process data through the entire middleware stack.

        This is the main entry point for data processing. It builds the middleware
        stack if needed, generates a unique request ID, and passes the data through
        the middleware chain.

        Args:
            data: The data to process through the pipeline
            _args: Positional arguments to pass to the middleware chain
            **kwargs: Keyword arguments to pass to the middleware chain

        Returns:
            The processed data after passing through all middleware components

        Note:
            This method automatically adds 'request_id' and 'pipeline_config' to kwargs
            to make them available to all middleware components.
        """
        request_id = str(uuid.uuid4())
        self.logger.info(f"Starting pipeline with request ID: {request_id}")
        if self.middleware_stack is None:
            self.build_middleware_stack()
        # Include request_id in the processing
        kwargs['request_id'] = request_id
        kwargs['pipeline_config'] = self.config  # Config available in context
        return self.middleware_stack(data, *args, **kwargs)
