from collections import defaultdict

import requests
from luann.llm_api.helpers import make_post_request
from luann.schemas.llm_config import LLMConfig
from luann.schemas.openai.chat_completion_response import ChatCompletionResponse
from luann.schemas.openai.chat_completions import ChatCompletionRequest
from luann.schemas.openai.embedding_response import EmbeddingResponse
# from luann.settings import ModelSettings


def get_azure_chat_completions_endpoint(base_url: str, model: str, api_version: str):
    return f"{base_url}/openai/deployments/{model}/chat/completions?api-version={api_version}"


def get_azure_embeddings_endpoint(base_url: str, model: str, api_version: str):
    return f"{base_url}/openai/deployments/{model}/embeddings?api-version={api_version}"


def get_azure_model_list_endpoint(base_url: str, api_version: str):
    return f"{base_url}/openai/models?api-version={api_version}"


def get_azure_deployment_list_endpoint(base_url: str):
    # Please note that it has to be 2023-03-15-preview
    # That's the only api version that works with this deployments endpoint
    # TODO: Use the Azure Client library here instead
    return f"{base_url}/openai/deployments?api-version=2023-03-15-preview"


def azure_openai_get_deployed_model_list(base_url: str, api_key: str, api_version: str) -> list:
    """https://learn.microsoft.com/en-us/rest/api/azureopenai/models/list?view=rest-azureopenai-2023-05-15&tabs=HTTP"""

    # https://xxx.openai.azure.com/openai/models?api-version=xxx
    headers = {"Content-Type": "application/json"}
    if api_key is not None:
        headers["api-key"] = f"{api_key}"

    # 1. Get all available models
    url = get_azure_model_list_endpoint(base_url, api_version)
    # print(f"url:{url}")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to retrieve model list: {e}")
    all_available_models = response.json().get("data", [])
    # print(f"all_available_models:{all_available_models}")

    # 2. Get all the deployed models
    url = get_azure_deployment_list_endpoint(base_url)
    # print(f"url:{url}")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to retrieve model list: {e}")

    deployed_models = response.json().get("data", [])
    # for m in all_available_models:
    #     modlename=m["id"]
    #     print(f"modlename:{modlename}")
    deployed_model_names = set([m["model"] for m in deployed_models])
    # deployed_model_names_id = set([m["id"] for m in deployed_models])

    # deployed_models
    # print(f"deployed_models:{deployed_models}")
    # print(f"deployed_model_names:{deployed_model_names}")


    # 3. Only return the models in available models if they have been deployed
    deployed_models_real = [m for m in all_available_models if m["id"] in deployed_model_names]

    # 4. Remove redundant deployments, only include the ones with the latest deployment
    # Create a dictionary to store the latest model for each ID
    latest_models = defaultdict()
    temp_model_id=""
    # print(f"deployed_models:{deployed_models}")
    # Iterate through the models and update the dictionary with the most recent model
    for model in deployed_models_real:
        for deployed_model_one in deployed_models:
            if model["id"]==deployed_model_one["model"]:
                temp_model_id=deployed_model_one["id"]
        # deployed_models_id = [m for m in all_available_models if model["id"] in deployed_model_names]
        model_id =temp_model_id
        model["id"]=temp_model_id
        updated_at = model["created_at"]

        # If the model ID is new or the current model has a more recent created_at, update the dictionary
        if model_id not in latest_models or updated_at > latest_models[model_id]["created_at"]:
            latest_models[model_id] = model

    # print(f"latest_models:{latest_models}")
    # Extract the unique models
    return list(latest_models.values())


def azure_openai_get_chat_completion_model_list(base_url: str, api_key: str, api_version: str) -> list:
    model_list = azure_openai_get_deployed_model_list(base_url, api_key, api_version)
    # print(f"model_list:{model_list}")
    # Extract models that support text generation
    model_options = [m for m in model_list if m.get("capabilities").get("chat_completion") == True]
    return model_options


def azure_openai_get_embeddings_model_list(base_url: str, api_key: str, api_version: str, require_embedding_in_name: bool = True) -> list:
    def valid_embedding_model(m: dict):
        valid_name = True
        if require_embedding_in_name:
            valid_name = "embedding" in m["id"]

        return m.get("capabilities").get("embeddings") == True and valid_name

    model_list = azure_openai_get_deployed_model_list(base_url, api_key, api_version)
    # Extract models that support embeddings

    model_options = [m for m in model_list if valid_embedding_model(m)]

    return model_options


def azure_openai_chat_completions_request(
   llm_config: LLMConfig, api_key: str, chat_completion_request: ChatCompletionRequest
) -> ChatCompletionResponse:
    """https://learn.microsoft.com/en-us/azure/ai-services/openai/reference#chat-completions"""

    assert api_key is not None, "Missing required field when calling Azure OpenAI"

    headers = {"Content-Type": "application/json", "api-key": f"{api_key}"}
    data = chat_completion_request.model_dump(exclude_none=True)
    

    # add check otherwise will cause error: "Invalid value for 'parallel_tool_calls': 'parallel_tool_calls' is only allowed when 'tools' are specified."
    if chat_completion_request.tools is not None:
        data["parallel_tool_calls"] = False
    # If functions == None, strip from luann.the payload
    if "functions" in data and data["functions"] is None:
        data.pop("functions")
        data.pop("function_call", None)  # extra safe,  should exist always (default="auto")

    if "tools" in data and data["tools"] is None:
        data.pop("tools")
        data.pop("tool_choice", None)  # extra safe,  should exist always (default="auto")

    # url = get_azure_chat_completions_endpoint(llm_config.azure_api_key, llm_config.model, llm_config.azure_version)
    url=llm_config.model_endpoint

   
    # print(f"data:{data}")
    response_json = make_post_request(url, headers, data)
    # NOTE: azure openai does not include "content" in the response when it is None, so we need to add it
    if "content" not in response_json["choices"][0].get("message"):
        response_json["choices"][0]["message"]["content"] = None
    response = ChatCompletionResponse(**response_json)  # convert to 'dot-dict' style which is the openai python client default
    return response


def azure_openai_embeddings_request(
    resource_name: str, deployment_id: str, api_version: str, api_key: str, data: dict
) -> EmbeddingResponse:
    """https://learn.microsoft.com/en-us/azure/ai-services/openai/reference#embeddings"""

    url = f"https://{resource_name}.openai.azure.com/openai/deployments/{deployment_id}/embeddings?api-version={api_version}"
    headers = {"Content-Type": "application/json", "api-key": f"{api_key}"}

    response_json = make_post_request(url, headers, data)
    return EmbeddingResponse(**response_json)
