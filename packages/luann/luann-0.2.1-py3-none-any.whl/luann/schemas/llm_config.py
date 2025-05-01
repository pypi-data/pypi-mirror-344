from typing import Optional,Literal

from pydantic import BaseModel, ConfigDict, Field, root_validator


class LLMConfig(BaseModel):
    """
    Configuration for a Language Model (LLM) model. This object specifies all the information necessary to access an LLM model to usage with Luann, except for secret keys.

    Attributes:
        model (str): The name of the LLM model.
        model_endpoint_type (str): The endpoint type for the model.
        model_endpoint (str): The endpoint for the model.
        model_wrapper (str): The wrapper for the model.
        context_window (int): The context window size for the model.
    """

    # TODO: 🤮 don't default to a vendor! bug city!
    model: str = Field(..., description="LLM model name. ")
    # model_endpoint_type: str = Field(..., description="The endpoint type for the model.")
    model_endpoint_type: Literal[
        "openai",
        "anthropic",
        "google_ai",
        "azure",
        "ollama",
        "vllm",
        "hugging-face",
    ] = Field(..., description="The endpoint type for the model.")
    model_endpoint: str = Field(..., description="The endpoint for the model.")
    model_wrapper: Optional[str] = Field(None, description="The wrapper for the model.")
    context_window: int = Field(..., description="The context window size for the model.")
    put_inner_thoughts_in_kwargs: Optional[bool] = Field(
        True,
        description="Puts 'inner_thoughts' as a kwarg in the function call if this is set to True. This helps with function calling performance and also the generation of inner thoughts.",
    )
    handle: Optional[str] = Field(None, description="The handle for this config, in the format provider/model-name.")
    temperature: Optional[float] = Field(
        0.7,
        description="The temperature to use when generating text with the model. A higher temperature will result in more random text.",
    )
    # FIXME hack to silence pydantic protected namespace warning
    model_config = ConfigDict(protected_namespaces=())
    
    # azure only
    # azure_endpoint: Optional[str] = Field(None, description="The Azure endpoint for the model.")
    azure_version: Optional[str] = Field(None, description="The Azure version for the model.")
    # azure_deployment: Optional[str] = Field(None, description="The Azure deployment for the model.")
    azure_api_key: Optional[str] =Field(None, description="The Azure api key for the model.")

    #openai only
    openai_api_key: Optional[str] =Field(None, description="The openai api key for the model.")

    #openai only
    googleai_api_key: Optional[str] =Field(None, description="The googleai api key for the model.")
    

    #openai only
    anthropic_api_key: Optional[str] =Field(None, description="The  anthropic api key for the model.")


     # openllm
    # openllm_auth_type: Optional[str] =Field(None, description="The openllm  auth_type for the model.")
    openllm_api_key: Optional[str] =Field(None, description="The openllm api key for the model.")



    @root_validator(pre=True)
    def set_default_put_inner_thoughts(cls, values):
        """
        Dynamically set the default for put_inner_thoughts_in_kwargs based on the model field,
        falling back to True if no specific rule is defined.
        """
        model = values.get("model")

        # Define models where we want put_inner_thoughts_in_kwargs to be False
        # For now it is gpt-4
        avoid_put_inner_thoughts_in_kwargs = ["gpt-4"]

        # Only modify the value if it's None or not provided
        if values.get("put_inner_thoughts_in_kwargs") is None:
            values["put_inner_thoughts_in_kwargs"] = False if model in avoid_put_inner_thoughts_in_kwargs else True

        return values
    @classmethod
    def default_config(cls, model_name: str):
        if model_name == "gpt-4":
            return cls(
                model="gpt-4",
                model_endpoint_type="openai",
                model_endpoint="https://api.openai.com/v1",
                model_wrapper=None,
                context_window=8192,
            )
        elif model_name == "gpt-4o-mini":
            return cls(
                model="gpt-4o-mini",
                model_endpoint_type="openai",
                model_endpoint="https://api.openai.com/v1",
                model_wrapper=None,
                context_window=128000,
            )
        elif model_name == "luann":
            return cls(
                model="memgpt-openai",
                model_endpoint_type="openai",
                model_endpoint="https://inference.memgpt.ai",
                context_window=16384,
            )
        else:
            raise ValueError(f"Model {model_name} not supported.")
    def pretty_print(self) -> str:
        return (
            f"{self.model}"
            + (f" [type={self.model_endpoint_type}]" if self.model_endpoint_type else "")
            + (f" [ip={self.model_endpoint}]" if self.model_endpoint else "")
        )