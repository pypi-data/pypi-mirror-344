from typing import Dict

from autogen_core.models import ModelInfo, ModelFamily

from saptiva_agents.tools import get_weather, wikipedia_search
from saptiva_agents.tools.langchain import WikipediaSearch


TOOLS = {
    WikipediaSearch.__name__: WikipediaSearch,
    get_weather.__name__: get_weather,
    wikipedia_search.__name__: wikipedia_search
}

MODEL_INFO: Dict[str, ModelInfo] = {
    "gemma3": {
        "vision": True,
        "function_calling": True,
        "json_output": True,
        "family": ModelFamily.UNKNOWN,
        "structured_output": True,
        "multiple_system_messages": False
    },
    "deepseek-r1": {
        "vision": False,
        "function_calling": False,
        "json_output": True,
        "family": ModelFamily.R1,
        "structured_output": True,
        "multiple_system_messages": False
    },
    "llama3.3": {
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "family": ModelFamily.UNKNOWN,
        "structured_output": True,
        "multiple_system_messages": True
    },
    "huihui_ai/phi4-abliterated": {
        "vision": False,
        "function_calling": False,
        "json_output": True,
        "family": ModelFamily.UNKNOWN,
        "structured_output": True,
        "multiple_system_messages": False
    },
    "qwen2.5": {
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "family": ModelFamily.UNKNOWN,
        "structured_output": True,
        "multiple_system_messages": True
    },
}

MODEL_TOKEN_LIMITS: Dict[str, int] = {
    "deepseek-r1": 131072,
    "gemma2": 8192,
    "gemma3": 128000,
    "llama3.3": 131072,
    "phi4": 16384,
    "qwen2.5": 131072,
}
