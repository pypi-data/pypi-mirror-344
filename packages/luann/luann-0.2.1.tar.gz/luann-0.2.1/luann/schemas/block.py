from typing import List, Optional, Union

from pydantic import Field, model_validator,BaseModel
from typing_extensions import Self
from luann.constants import CORE_MEMORY_BLOCK_CHAR_LIMIT
from luann.schemas.luann_base import LuannBase

# block of the LLM context


class BaseBlock(LuannBase, validate_assignment=True):
    """Base block of the LLM context"""

    __id_prefix__ = "block"

    # data value
    value: Optional[Union[List[str], str]] = Field(None, description="Value of the block.")
    limit: int = Field(CORE_MEMORY_BLOCK_CHAR_LIMIT, description="Character limit of the block.")

    template_name: Optional[str] = Field(None, description="Name of the block.")
    is_template: bool = Field(False, description="Whether the block is a template (e.g. saved human/persona options).")
      # context window label
    label: Optional[str] = Field(None, description="Label of the block (e.g. 'human', 'persona').")

    # metadat
    description: Optional[str] = Field(None, description="Description of the block.")
    metadata_: Optional[dict] = Field({}, description="Metadata of the block.")
    class Config:
        extra = "ignore"  # Ignores extra fields
    # # associated user/agent
    # user_id: Optional[str] = Field(None, description="The unique identifier of the user associated with the block.")
    # organization_id:Optional[str] = Field(None, description="The unique identifier of the organizaition associated with the block.")
    @model_validator(mode="after")
    def verify_char_limit(self) -> Self:
        if self.value and len(self.value) > self.limit:
            error_msg = f"Edit failed: Exceeds {self.limit} character limit (requested {len(self.value)}) - {str(self)}."
            raise ValueError(error_msg)

        return self

    def __setattr__(self, name, value):
        """Run validation if self.value is updated"""
        super().__setattr__(name, value)
        if name == "value":
            # run validation
            self.__class__.model_validate(self.model_dump(exclude_unset=True))


class Block(BaseBlock):
    """
    A Block represents a reserved section of the LLM's context window which is editable. `Block` objects contained in the `Memory` object, which is able to edit the Block values.

    Parameters:
        name (str): The name of the block.
        value (str): The value of the block. This is the string that is represented in the context window.
        limit (int): The character limit of the block.
        template (bool): Whether the block is a template (e.g. saved human/persona options). Non-template blocks are not stored in the database and are ephemeral, while templated blocks are stored in the database.
        label (str): The label of the block (e.g. 'human', 'persona'). This defines a category for the block.
        description (str): Description of the block.
        metadata_ (Dict): Metadata of the block.
        user_id (str): The unique identifier of the user associated with the block.
    """

    id: str = BaseBlock.generate_id_field()
    # associated user/agent
    organization_id: Optional[str] = Field(None, description="The unique identifier of the organization associated with the block.")

    # default orm fields
    created_by_id: Optional[str] = Field(None, description="The id of the user that made this Block.")
    last_updated_by_id: Optional[str] = Field(None, description="The id of the user that last updated this Block.")


class Human(Block):
    """Human block of the LLM context"""

    label: str = "human"


class Persona(Block):
    """Persona block of the LLM context"""

    label: str = "persona"

class BlockLabelUpdate(BaseModel):
    """Update the label of a block"""

    current_label: str = Field(..., description="Current label of the block.")
    new_label: str = Field(..., description="New label of the block.")
class CreateBlock(BaseBlock):
    """Create a block"""

    label: str = Field(..., description="Label of the block.")
    limit: int = Field(CORE_MEMORY_BLOCK_CHAR_LIMIT, description="Character limit of the block.")
    value: str = Field(..., description="Value of the block.")

    # block templates
    is_template: bool = False
    template_name: Optional[str] = Field(None, description="Name of the block if it is a template.", alias="name")


class CreatePersona(CreateBlock):
    """Create a persona block"""

    # template: bool = True
    label: str = "persona"


class CreateHuman(CreateBlock):
    """Create a human block"""

    # template: bool = True
    label: str = "human"

class CreateBlockTemplate(CreateBlock):
    """Create a block template"""

    is_template: bool = True


class CreateHumanBlockTemplate(CreateHuman):
    """Create a human block template"""

    is_template: bool = True
    label: str = "human"


class CreatePersonaBlockTemplate(CreatePersona):
    """Create a persona block template"""

    is_template: bool = True
    label: str = "persona"
class UpdateBlock(BaseBlock):
    """Update a block"""

    id: str = Field(..., description="The unique identifier of the block.")
    limit: Optional[int] = Field(2000, description="Character limit of the block.")

class BlockUpdate(BaseBlock):
    """Update a block"""

    limit: Optional[int] = Field(2000, description="Character limit of the block.")
    value: Optional[str] = Field(None, description="Value of the block.")

    class Config:
        extra = "ignore"  # Ignores extra fields
class BlockLimitUpdate(BaseModel):
    """Update the limit of a block"""

    label: str = Field(..., description="Label of the block.")
    limit: int = Field(..., description="New limit of the block.")
class UpdatePersona(UpdateBlock):
    """Update a persona block"""

    label: str = "persona"


class UpdateHuman(UpdateBlock):
    """Update a human block"""

    label: str = "human"