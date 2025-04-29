"""
Module providing the ServiceInfo dataclass to represent service-level metadata.

This module defines the ServiceInfo dataclass that extends EntityInfo to include
details such as service type, owning team, and associated use cases.
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict

from bisslog_schema.entity_info import EntityInfo
from bisslog_schema.use_case_info import UseCaseInfo


@dataclass
class ServiceInfo(EntityInfo):
    """
    Dataclass representing service metadata.

    Extends
    -------
    EntityInfo
        Base entity information with name, description, type, and tags.

    Attributes
    ----------
    service_type : Optional[str]
        The type of the service (e.g., API, batch job, etc.).
    team : Optional[str]
        The team responsible for the service.
    use_cases : List[UseCaseInfo]
        List of use cases associated with the service.
    """

    service_type: Optional[str] = None
    team: Optional[str] = None
    use_cases: Dict[str, UseCaseInfo] = field(default_factory=list)

    @staticmethod
    def from_dict(data: dict) -> "ServiceInfo":
        """
        Create a ServiceInfo instance from a dictionary.

        This method parses a dictionary structure to create a ServiceInfo object,
        merging service-level tags with use case-specific tags.

        Parameters
        ----------
        data : dict
            A dictionary containing service information, including nested use case data.

        Returns
        -------
        ServiceInfo
            A populated ServiceInfo object.
        """
        tags = data.get("tags", {})
        use_cases_data = data.get("use_cases", {})
        use_cases = {}
        for keyname, use_case_data in use_cases_data.items():
            new_uc_tags = tags.copy()
            uc_tags: dict = use_case_data.get("tags", {})
            new_uc_tags.update(uc_tags)
            use_case_data["tags"] = new_uc_tags
            use_cases[keyname] = UseCaseInfo.from_dict(use_case_data)
        return ServiceInfo(
            name=data.get("name"),
            description=data.get("description"),
            type=data.get("type"),
            tags=tags,
            service_type=data.get("service_type"),
            team=data.get("team"),
            use_cases=use_cases,
        )
