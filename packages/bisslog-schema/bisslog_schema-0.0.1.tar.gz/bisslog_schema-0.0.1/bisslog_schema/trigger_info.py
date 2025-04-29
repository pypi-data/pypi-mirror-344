"""Module defining trigger configurations for various service entry points."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Type, Dict, Any




class TriggerOptions(ABC):
    """Abstract base class for trigger-specific options.

    All trigger option classes must implement the from_dict method for deserialization."""

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TriggerOptions":
        """Deserialize a dictionary into a TriggerOptions instance.

        Parameters
        ----------
        data : dict
            Dictionary containing the trigger options.

        Returns
        -------
        TriggerOptions
            An instance of a subclass implementing TriggerOptions."""
        raise NotImplementedError("from_dict not implemented")



@dataclass
class TriggerHttp(TriggerOptions):
    """Options for configuring an HTTP trigger.

    Attributes
    ----------
    method : str, optional
        The HTTP method (e.g., GET, POST).
    authenticator : str, optional
        The authentication mechanism associated with the trigger.
    route : str, optional
        The API route path.
    apigw : str, optional
        API Gateway identifier if applicable.
    cacheable : bool
        Indicates whether the route can be cached. Defaults to False."""
    method: Optional[str] = None
    authenticator: Optional[str] = None
    route: Optional[str] = None
    apigw: Optional[str] = None
    cacheable: bool = False

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TriggerHttp":
        """Deserialize a dictionary into a TriggerWebsocket instance.

        Parameters
        ----------
        data : dict
            Dictionary containing the trigger options.

        Returns
        -------
        TriggerHttp
            An instance of a subclass implementing TriggerWebsocket."""
        return cls(
            method=data.get("method"),
            authenticator=data.get("authenticator"),
            route=data.get("route"),
            apigw=data.get("apigw"),
            cacheable=data.get("cacheable", False)
        )


@dataclass
class TriggerWebsocket(TriggerOptions):
    """Options for configuring a WebSocket trigger.

    Attributes
    ----------
    route_key : str, optional
        The route key associated with the WebSocket connection."""
    route_key: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TriggerWebsocket":
        """Deserialize a dictionary into a TriggerWebsocket instance.

        Parameters
        ----------
        data : dict
            Dictionary containing the trigger options.

        Returns
        -------
        TriggerWebsocket
            An instance of a subclass implementing TriggerWebsocket."""
        return cls(route_key=data.get("routeKey"))


@dataclass
class TriggerConsumer(TriggerOptions):
    """Options for configuring a consumer trigger (e.g., queue consumer).

    Attributes
    ----------
    queue : str, optional
        The name of the queue.
    partition : str, optional
        The partition key if applicable."""
    queue: Optional[str] = None
    partition: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TriggerConsumer":
        """Deserialize a dictionary into a TriggerConsumer instance.

        Parameters
        ----------
        data : dict
            Dictionary containing the trigger options.

        Returns
        -------
        TriggerConsumer
            An instance of a subclass implementing TriggerConsumer."""
        return cls(
            queue=data.get("queue"),
            partition=data.get("partition")
        )


@dataclass
class TriggerSchedule(TriggerOptions):
    """Options for configuring a scheduled (cron) trigger.

    Attributes
    ----------
    cronjob : str, optional
        Cron expression specifying the schedule."""
    cronjob: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TriggerSchedule":
        """Deserialize a dictionary into a TriggerSchedule instance.

        Parameters
        ----------
        data : dict
            Dictionary containing the trigger options.

        Returns
        -------
        TriggerSchedule
            An instance of a subclass implementing TriggerSchedule."""
        return cls(cronjob=data.get("cronjob"))



class TriggerEnum(Enum):
    """Enumeration of available trigger types and their associated option classes.

    Members
    -------
    HTTP : TriggerHttp
        Represents an HTTP trigger.
    WEBSOCKET : TriggerWebsocket
        Represents a WebSocket trigger.
    CONSUMER : TriggerConsumer
        Represents a consumer or queue trigger.
    SCHEDULE : TriggerSchedule
        Represents a scheduled trigger."""
    HTTP = ("http", TriggerHttp)
    WEBSOCKET = ("websocket", TriggerWebsocket)
    CONSUMER = ("consumer", TriggerConsumer)
    SCHEDULE = ("schedule", TriggerSchedule)

    def __init__(self, value: str, cls: Type[TriggerOptions]):
        self._value_ = value  # importante: esto define el string que tendrá el enum
        self.cls = cls        # esto es tu clase asociada

    @staticmethod
    def from_str(value: str) -> "TriggerEnum":
        """Converts from string to TriggerEnum

        Parameters
        ----------
        value: str
            String value to get the member

        Returns
        -------
        TriggerEnum"""
        for trigger in TriggerEnum:
            if trigger.value == value:
                return trigger
        raise ValueError(f"Unknown trigger type: {value}")


@dataclass
class TriggerInfo:
    """Represents a complete trigger configuration including its type and specific options.

    Attributes
    ----------
    type : TriggerEnum
        The type of the trigger (e.g., HTTP, WebSocket).
    options : TriggerOptions
        The configuration options specific to the trigger type."""
    type: TriggerEnum
    options: TriggerOptions

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "TriggerInfo":
        """Enumeration of available trigger types and their associated option classes.

        Parameters
        ----------
        data : dict
            Dictionary containing the trigger options.
        Returns
        -------
        TriggerInfo
            An instance of a subclass implementing TriggerSchedule."""

        type_str = data.get("type", "http")
        if not type_str:
            raise ValueError("Trigger 'type' is required")

        trigger_type = TriggerEnum.from_str(type_str)

        cls = trigger_type.cls

        return TriggerInfo(trigger_type, cls.from_dict(data.get("options", {})))
