"""Module providing the base EntityInfo data model."""
from dataclasses import dataclass, field
from typing import Optional, Dict


@dataclass
class EntityInfo:
    """Base class representing basic information about an entity.

    Attributes
    ----------
    name : str, optional
        The name of the entity.
    description : str, optional
        A brief description of the entity.
    type : str, optional
        The type or category of the entity.
    tags : dict of str to str, optional
        A dictionary of key-value pairs for tagging the entity. Defaults to an empty dictionary."""
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    tags: Dict[str, str] = field(default_factory=dict)
