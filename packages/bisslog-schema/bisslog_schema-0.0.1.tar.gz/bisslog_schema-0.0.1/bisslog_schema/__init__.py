"""bisslog schema is a lightweight framework to organize and document the key elements
of a distributed system, focusing on its use cases and service design.
It structures the metadata without exposing any underlying technical
or implementation-specific details."""
from .read_metadata import read_service_metadata


__all__ = ["read_service_metadata"]
