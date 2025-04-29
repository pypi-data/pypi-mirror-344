"""
Module to define the UseCaseInfo class, which models use case metadata for a service,
including criticality, triggers, and actor details.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Union

from bisslog_schema.entity_info import EntityInfo
from bisslog_schema.enums.criticality_enum import CriticalityEnum
from bisslog_schema.trigger_info import TriggerInfo


@dataclass
class UseCaseInfo(EntityInfo):
    """Represents a use case with metadata including triggers, criticality, and associated actor.

    Attributes
    ----------
    triggers : List[TriggerInfo]
        A list of triggers that initiate the use case.
    criticality : Optional[Union[str, CriticalityEnum, int]]
        The criticality level of the use case.
    actor : Optional[str]
        The primary actor that interacts with the use case.
    """
    triggers: List[TriggerInfo] = field(default_factory=list)
    criticality: Optional[Union[str, CriticalityEnum, int]] = CriticalityEnum.MEDIUM
    actor: Optional[str] = None

    @staticmethod
    def from_dict(data: dict) -> "UseCaseInfo":
        """Creates a UseCaseInfo instance from a dictionary.

        Parameters
        ----------
        data : dict
            Dictionary containing use case information.

        Returns
        -------
        UseCaseInfo
            An instance populated with the provided data.
        """
        triggers_data = data.get("triggers", [])
        triggers = [TriggerInfo.from_dict(t) for t in triggers_data]

        criticality = data.get("criticality")
        new_criticality = None
        if isinstance(criticality, (int, float)):
            new_criticality = CriticalityEnum.get_from_int_val(criticality)
        if isinstance(criticality, str) and criticality.upper() in CriticalityEnum.__members__:
            new_criticality = CriticalityEnum[criticality.upper()]
        if new_criticality is not None:
            criticality = new_criticality

        return UseCaseInfo(
            name=data.get("name"),
            description=data.get("description"),
            type=data.get("type"),
            tags=data.get("tags", {}),
            triggers=triggers,
            criticality=criticality,
            actor=data.get("actor"),
        )
