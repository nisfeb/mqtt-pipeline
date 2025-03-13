import logging


class Middleware:
    """
    Base middleware class for processing requests in a pipeline.

    This class provides the foundation for creating middleware components that can
    process requests sequentially in a middleware chain. Each middleware instance
    calls the next middleware in the chain via the get_response callable.

    The middleware pattern allows for separating cross-cutting concerns like
    logging, authentication, or data transformation from the core application logic.

    Attributes:
        get_response (callable): Function to call the next middleware in the chain
        config (dict): Global configuration dictionary for all middlewares
        middleware_config (dict): Configuration specific to this middleware instance
        logger (Logger): Logger instance configured for this middleware
    """
    def __init__(self, get_response, config=None, logger=None):
        """
        Initialize the middleware with the next middleware in the chain and configuration.

        Args:
            get_response (callable): Function to call the next middleware in the chain
            config (dict, optional): Configuration dictionary containing both global
                and middleware-specific settings. Defaults to empty dict.
            logger (Logger, optional): Logger instance to use for logging. If None,
                a new logger will be created based on the class name. Defaults to None.

        Note:
            The middleware-specific configuration is extracted from the global config
            using the class name as a key.
        """
        self.get_response = get_response
        # Store configuration with defaults
        self.config = config or {}

        # Get middleware-specific config if it exists
        middleware_name = self.__class__.__name__
        self.middleware_config = config.get(
            middleware_name,
            {}
        ) if config else {}

        if logger is None:
            self.logger = logging.getLogger(
                f"pipeline.{self.__class__.__name__}"
            )
        else:
            # Create a child logger to maintain hierarchy while using the
            # injected logger's settings
            self.logger = logger.getChild(self.__class__.__name__)

    def __call__(self, request, *args, **kwargs):
        """
        Process the request and pass it to the next middleware in the chain.

        This method is called when the middleware instance is invoked as a function.
        It logs the processing event, then passes the request to the next middleware
        in the chain via the get_response callable.

        Args:
            request: The request object to process
            _args: Positional arguments to pass to the next middleware
            **kwargs: Keyword arguments to pass to the next middleware, may include:
                - request_id (str): Identifier for tracking the request through the pipeline

        Returns:
            The response from the next middleware in the chain

        Example usage of configuration (commented out):
            - Global config access: self.config.get('enable_metrics', False)
            - Middleware-specific config: self.middleware_config.get('log_format', 'standard')
        """
        request_id = kwargs.get('request_id', 'unknown')

        # Use configuration values
        # if self.config.get('enable_metrics', False):
        #   Example of using global config
        #   self.logger.debug(f"[{request_id}] Metrics enabled for \
        #    {self.__class__.__name__}")
        # Access middleware-specific config
        # log_format = self.middleware_config.get('log_format', 'standard')
        # if log_format == 'detailed':
        #     self.logger.info(f"[{request_id}] Processing in \
        #    {self.__class__.__name__} with payload: {request}")
        # else:
        #     self.logger.info(f"[{request_id}] Processing in \
        #    {self.__class__.__name__}")

        self.logger.info(
            f"[{request_id}] Processing in {self.__class__.__name__}"
        )
        response = self.get_response(request, *args, **kwargs)
        return response
