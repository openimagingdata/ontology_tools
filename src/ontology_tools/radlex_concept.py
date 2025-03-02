"""RadLex Concept Model"""

from typing import ClassVar, Sequence

import caseswitcher
from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator
from pydantic.alias_generators import to_camel

from .common import Code

# Define RadLexProperties dictionary to account for "http://radlex" field
RadLexProperties = dict[str, str | Sequence[str]]


# ConfigDict for RadLex Properties
class RadLexConcept(BaseModel):
    """Model for a RadLex concept."""

    SYSTEM_NAME: ClassVar[str] = "RADLEX"

    model_config = ConfigDict(
        populate_by_name=True,
        coerce_numbers_to_str=True,
        alias_generator=to_camel,
        validate_assignment=True,
    )

    # Define the new document format and fields
    id: str = Field(alias="_id")
    preferred_label: str
    synonyms: list[str] | None = None
    parent: str | None = None
    definition: str | None = None
    radlex_properties: RadLexProperties | None = None

    def summary_text(self) -> str:
        """Return a summary text representation of the concept."""
        out = self.preferred_label
        if self.definition:
            out += f": {self.definition}"
        if self.synonyms:
            out += f" (synonyms: {'; '.join(self.synonyms)})"
        return out

    # Field validator for radlex property dictionary keys
    @field_validator("radlex_properties", mode="before")
    def radlex_property_keys_to_snake(cls, value: dict | None) -> RadLexProperties | None:
        """Convert RadLex property dictionary keys to snake case."""
        if value is None:
            return None
        if not isinstance(value, dict):
            raise ValueError("RadLex properties must be a dictionary")
        out_properties = {}
        for key, val in value.items():
            out_properties[caseswitcher.to_snake(key)] = val
        # out_properties = {caseswitcher.to_snake(k): v for k, v in value.items()}
        return out_properties

    # Field serializer to convert radlex property dictionary keys back to camel case
    @field_serializer("radlex_properties", when_used="unless-none")
    def radlex_property_keys_to_camel(self, in_props: RadLexProperties) -> RadLexProperties:
        """Convert RadLex property dictionary keys to camel case."""
        out_props = {caseswitcher.to_camel(k): v for k, v in in_props.items()}
        return out_props

    def to_system_code_display(self) -> Code:
        """Convert the concept to a Code reference object."""
        return Code(system=self.SYSTEM_NAME, code=self.id, display=self.preferred_label)
