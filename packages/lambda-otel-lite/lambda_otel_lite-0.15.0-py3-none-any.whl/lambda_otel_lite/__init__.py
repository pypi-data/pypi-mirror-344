"""
lambda-otel-lite - Lightweight OpenTelemetry instrumentation for AWS Lambda.

This package provides a simple way to add OpenTelemetry instrumentation to AWS Lambda
functions with minimal overhead and configuration.
"""

import os
from enum import Enum
from typing import Final

from .version import VERSION

__version__ = VERSION


class ProcessorMode(str, Enum):
    """Controls how spans are processed and exported.

    Inherits from str to make it JSON serializable and easier to use with env vars.

    Attributes:
        SYNC: Synchronous flush in handler thread. Best for development.
        ASYNC: Asynchronous flush via extension. Best for production.
        FINALIZE: Let processor handle flushing. Best with BatchSpanProcessor.
    """

    SYNC = "sync"
    ASYNC = "async"
    FINALIZE = "finalize"

    @classmethod
    def from_env(
        cls, env_var: str, default: "ProcessorMode | None" = None
    ) -> "ProcessorMode":
        """Create ProcessorMode from environment variable.

        Args:
            env_var: Name of the environment variable to read
            default: Default mode if environment variable is not set

        Returns:
            ProcessorMode instance

        Raises:
            ValueError: If environment variable contains invalid mode
        """
        value = os.getenv(env_var, "").strip().lower() or (
            default.value if default else ""
        )
        try:
            return cls(value)
        except ValueError as err:
            raise ValueError(
                f"Invalid {env_var}: {value}. Must be one of: {', '.join(m.value for m in cls)}"
            ) from err

    @classmethod
    def resolve(
        cls,
        config_mode: "ProcessorMode | None" = None,
        env_var: str = "LAMBDA_EXTENSION_SPAN_PROCESSOR_MODE",
    ) -> "ProcessorMode":
        """Resolve processor mode with proper precedence.

        Precedence order:
        1. Environment variable (if set and valid)
        2. Programmatic configuration (if provided)
        3. Default value (SYNC)

        Unlike from_env, this method logs a warning instead of raising an error
        when the environment variable contains an invalid value.

        Args:
            config_mode: Optional processor mode from programmatic configuration
            env_var: Name of the environment variable to read

        Returns:
            The resolved processor mode
        """
        from .logger import create_logger

        logger = create_logger("processor_mode")

        # Check environment variable first
        env_value = os.getenv(env_var, "").strip().lower()
        if env_value:
            try:
                if env_value in (m.value for m in cls):
                    return cls(env_value)
                else:
                    logger.warn(
                        f"Invalid {env_var}: {env_value}. Must be one of: {', '.join(m.value for m in cls)}. Using fallback."
                    )
            except Exception as e:
                logger.warn(f"Error parsing {env_var}: {e}. Using fallback.")

        # Use config value if provided, otherwise default to SYNC
        return config_mode if config_mode is not None else cls.SYNC


# Import this first to avoid circular imports
from .constants import Defaults, EnvVars, ResourceAttributes  # noqa: E402

# Global processor mode - single source of truth for the package
processor_mode: Final[ProcessorMode] = ProcessorMode.resolve(
    config_mode=None, env_var=EnvVars.PROCESSOR_MODE
)

# Package exports
__all__ = [
    "ProcessorMode",
    "processor_mode",  # Export the global processor mode
    "init_telemetry",  # Will be imported from telemetry.py
    "create_traced_handler",  # Will be imported from handler.py
    # Extractors and related classes
    "TriggerType",
    "SpanAttributes",
    "default_extractor",
    "api_gateway_v1_extractor",
    "api_gateway_v2_extractor",
    "alb_extractor",
    # Constants
    "EnvVars",
    "Defaults",
    "ResourceAttributes",
    # Resource utilities
    "get_lambda_resource",  # Will be imported from resource.py
]

# Import public API
from .extractors import (  # noqa: E402 - Ignore flake8 error about imports not being at top of file
    SpanAttributes,
    TriggerType,
    alb_extractor,
    api_gateway_v1_extractor,
    api_gateway_v2_extractor,
    default_extractor,
)
from .handler import create_traced_handler  # noqa: E402
from .resource import get_lambda_resource  # noqa: E402
from .telemetry import init_telemetry  # noqa: E402
