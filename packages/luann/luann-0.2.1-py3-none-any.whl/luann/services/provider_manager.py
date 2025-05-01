from typing import List, Optional

from luann.orm.provider import Provider as ProviderModel
from luann.schemas.providers import Provider as PydanticProvider
from luann.schemas.providers import ProviderUpdate
from luann.schemas.user import User as PydanticUser
from luann.utils import enforce_types
from  luann.constants import ENABLED_PROVODERS_NAME


class ProviderManager:

    def __init__(self):
        from luann.server.server import db_context

        self.session_maker = db_context

    @enforce_types
    def create_provider(self, provider: PydanticProvider, actor: PydanticUser) -> PydanticProvider:
        """Create a new provider if it doesn't already exist."""
        
        #check provider name  if exit
        if provider.name not in ENABLED_PROVODERS_NAME:
           raise ValueError(f"New provider name '{provider.name}' doesn't in  official provider name list ")
        


        with self.session_maker() as session:

            
            # Use dictionary comprehension to build kwargs dynamically
            kwargs = {
                         key: value
                              for key, value in {
                                           "is_enabled": True,
                                           "name": provider.name,
                                               }.items()
                               if value is not None
                    }

            simlar_name_existing_provider_enabled = ProviderModel.list(db_session=session, actor=actor,**kwargs)
            print(simlar_name_existing_provider_enabled)
            if len(simlar_name_existing_provider_enabled)>0:
                raise ValueError(f" provider name '{provider.name}' have two or above to be enabled,must only one to be enabled !!!!!! ")
            # simlar_name_existing_provider_enabled = ProviderModel.read(db_session=session, name=provider.name,is_enabled=True, actor=actor)
            # Assign the organization id based on the actor
            provider.organization_id = actor.organization_id
        

            # Lazily create the provider id prior to persistence
            provider.resolve_identifier()

            new_provider = ProviderModel(**provider.model_dump(exclude_unset=True))
            new_provider.create(session, actor=actor)
            return new_provider.to_pydantic()

    @enforce_types
    def update_provider(self, provider_update: ProviderUpdate, actor: PydanticUser) -> PydanticProvider:
        """Update provider details."""
        with self.session_maker() as session:

            
            # Retrieve the existing provider by ID
            existing_provider = ProviderModel.read(db_session=session, identifier=provider_update.id)

            # Use dictionary comprehension to build kwargs dynamically

            if provider_update.is_enabled:

                kwargs = {
                         key: value
                              for key, value in {
                                           "is_enabled": True,
                                           "name": existing_provider.name,
                                               }.items()
                               if value is not None
                    }

                simlar_name_existing_provider_enabled = ProviderModel.list(db_session=session, actor=actor,**kwargs)
                if len(simlar_name_existing_provider_enabled)>0:
                   raise ValueError(f" provider name '{existing_provider.name}' have two or above to be enabled,must only one to be enabled !!!!!! ")

            # Update only the fields that are provided in ProviderUpdate
            update_data = provider_update.model_dump(exclude_unset=True, exclude_none=True)
            for key, value in update_data.items():
                setattr(existing_provider, key, value)

            # Commit the updated provider
            existing_provider.update(session, actor=actor)
            return existing_provider.to_pydantic()

    @enforce_types
    def delete_provider_by_id(self, provider_id: str, actor: PydanticUser):
        """Delete a provider."""
        with self.session_maker() as session:
            # Delete from luann.provider table
            provider = ProviderModel.read(db_session=session, identifier=provider_id)
            provider.hard_delete(session, actor=actor)

            session.commit()
    



    @enforce_types
    def list_enabled_providers_name(self) -> List[str]:
        """List all providers names with official provide."""
       
        return [provider_name for provider_name in ENABLED_PROVODERS_NAME]
        
    @enforce_types
    def list_providers(self, actor: PydanticUser, after: Optional[str] = None, limit: Optional[int] = 50) -> List[PydanticProvider]:
        """List all providers with optional pagination."""
        with self.session_maker() as session:
            providers = ProviderModel.list(
                db_session=session,
                after=after,
                limit=limit,
                actor=actor,
            )
            return [provider.to_pydantic() for provider in providers]

    # @enforce_types
    # def get_anthropic_override_provider_id(self) -> Optional[str]:
    #     """Helper function to fetch custom anthropic provider id for v0 BYOK feature"""
    #     anthropic_provider = [provider for provider in self.list_providers() if provider.name == "anthropic"]
    #     if len(anthropic_provider) != 0:
    #         return anthropic_provider[0].id
    #     return None

    # @enforce_types
    # def get_anthropic_override_key(self) -> Optional[str]:
    #     """Helper function to fetch custom anthropic key for v0 BYOK feature"""
    #     anthropic_provider = [provider for provider in self.list_providers() if provider.name == "anthropic"]
    #     if len(anthropic_provider) != 0:
    #         return anthropic_provider[0].api_key
    #     return None
