import os
from typing import List, Optional

from luann.orm.block import Block as BlockModel
from luann.orm.errors import NoResultFound
from luann.schemas.block import Block
from luann.schemas.block import Block as PydanticBlock
from luann.schemas.agent import AgentState as PydanticAgentState
from luann.schemas.block import BlockUpdate, Human, Persona
from luann.schemas.user import User as PydanticUser
from luann.utils import enforce_types, list_human_files, list_persona_files


class BlockManager:
    """Manager class to handle business logic related to Blocks."""

    def __init__(self):
        # Fetching the db_context similarly as in ToolManager
        from luann.server.server import db_context

        self.session_maker = db_context

    @enforce_types
    def create_or_update_block(self, pydantic_block: PydanticBlock, actor: PydanticUser) -> PydanticBlock:
        """Create a new block based on the Block schema."""
        #  tool = self.get_block_by_name(tool_name=pydantic_tool.name, actor=actor)
        db_block =self.get_block_by_name(template_name=pydantic_block.template_name, actor=actor)
        # print(f"db_block:{db_block}")
        # db_block = self.get_block_by_id(block.id, actor)
        if db_block:
            update_data = BlockUpdate(**pydantic_block.model_dump(exclude_none=True))
            self.update_block(db_block.id, update_data, actor)
        else:
            with self.session_maker() as session:
                # Always write the organization_id
                pydantic_block.organization_id = actor.organization_id
                data = pydantic_block.model_dump(exclude_none=True)
                block = BlockModel(**data)
                block.create(session, actor=actor)
            return block.to_pydantic()

    @enforce_types
    def update_block(self, block_id: str, block_update: BlockUpdate, actor: PydanticUser) -> PydanticBlock:
        """Update a block by its ID with the given BlockUpdate object."""
        with self.session_maker() as session:
            block = BlockModel.read(db_session=session, identifier=block_id, actor=actor)
            update_data = block_update.model_dump(exclude_unset=True, exclude_none=True)
            for key, value in update_data.items():
                setattr(block, key, value)
            block.update(db_session=session, actor=actor)
            return block.to_pydantic()

    @enforce_types
    def delete_block(self, block_id: str, actor: PydanticUser) -> PydanticBlock:
        """Delete a block by its ID."""
        with self.session_maker() as session:
            block = BlockModel.read(db_session=session, identifier=block_id)
            block.hard_delete(db_session=session, actor=actor)
            return block.to_pydantic()

    @enforce_types
    def get_blocks(
        self,
        actor: PydanticUser,
        label: Optional[str] = None,
        is_template: Optional[bool] = None,
        template_name: Optional[str] = None,
        id: Optional[str] = None,
        after: Optional[str] = None,
        limit: Optional[int] = 50,
    ) -> List[PydanticBlock]:
        """Retrieve blocks based on various optional filters."""
        with self.session_maker() as session:
            # Prepare filters
            filters = {"organization_id": actor.organization_id}
            if label:
                filters["label"] = label
            if is_template is not None:
                filters["is_template"] = is_template
            if template_name:
                filters["template_name"] = template_name
            if id:
                filters["id"] = id

            blocks = BlockModel.list(db_session=session, after=after, limit=limit, **filters)

            return [block.to_pydantic() for block in blocks]
    @enforce_types
    def get_block_by_name(self, template_name: str, actor: PydanticUser):
        """Retrieve a tool by its name and a user. We derive the organization from luann.the user, and retrieve that tool."""
        try:
            with self.session_maker() as session:
                block= BlockModel.read(db_session=session, template_name=template_name, actor=actor)
                return block.to_pydantic()
        except NoResultFound:
            return None
    @enforce_types
    def get_block_by_id(self, block_id, actor: PydanticUser) -> Optional[PydanticBlock]:
        """Retrieve a block by its name."""
        with self.session_maker() as session:
            try:
                block = BlockModel.read(db_session=session, identifier=block_id, actor=actor)
                return block.to_pydantic()
            except NoResultFound:
                return None

    @enforce_types
    def add_default_blocks(self, actor: PydanticUser):
        for persona_file in list_persona_files():
            text = open(persona_file, "r", encoding="utf-8").read()
            name = os.path.basename(persona_file).replace(".txt", "")
            self.create_or_update_block(Persona(template_name=name, value=text, is_template=True), actor=actor)

        for human_file in list_human_files():
            text = open(human_file, "r", encoding="utf-8").read()
            name = os.path.basename(human_file).replace(".txt", "")
            self.create_or_update_block(Human(template_name=name, value=text, is_template=True), actor=actor)
    @enforce_types
    def get_agents_for_block(self, block_id: str, actor: PydanticUser) -> List[PydanticAgentState]:
        """
        Retrieve all agents associated with a given block.
        """
        with self.session_maker() as session:
            block = BlockModel.read(db_session=session, identifier=block_id, actor=actor)
            agents_orm = block.agents
            agents_pydantic = [agent.to_pydantic() for agent in agents_orm]

            return agents_pydantic
