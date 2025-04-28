# -*- coding: utf-8 -*-
# pf-reasoning-tool-proj/pf_reasoning_tool/tools/vision_llm_tool.py
'''
Custom Promptflow tool that can talk to both vision models (GPT-4V, GPT-4o)
and reasoning-only text models (e.g. o3-mini).  Single quotes, two spaces.
'''

from typing import Union, List, Optional

# Promptflow imports
from promptflow.contracts.types import PromptTemplate
from promptflow.connections import AzureOpenAIConnection, OpenAIConnection
from promptflow.tools.exception import InvalidConnectionType
from promptflow.tools.common import handle_openai_error
from promptflow._internal import tool

# Vision wrappers
from promptflow.tools.aoai_gpt4v import AzureOpenAI as AoaiVisionWrapper
from promptflow.tools.openai_gpt4v import OpenAI as OpenAIVisionWrapper

# Text wrappers
from promptflow.tools.aoai import AzureOpenAI as AoaiTextWrapper
from promptflow.tools.openai import OpenAI as OpenAITextWrapper


def _is_vision(model_or_deployment: str) -> bool:
    '''Quick heuristic to decide if we should treat the target as a vision model.'''
    if not model_or_deployment:
        return False
    tag = model_or_deployment.lower()
    return 'vision' in tag or tag.endswith('-o')


@handle_openai_error()
@tool(streaming_option_parameter='stream', return_names=['output'])
def vision_llm(
    connection: Union[AzureOpenAIConnection, OpenAIConnection],
    prompt: PromptTemplate,
    deployment_name: str = '',
    model: str = '',
    temperature: float = 0.7,
    top_p: float = 1.0,
    stream: bool = False,
    stop: Optional[List[str]] = None,
    max_tokens: Optional[int] = None,
    presence_penalty: float = 0.0,
    frequency_penalty: float = 0.0,
    seed: Optional[int] = None,
    detail: str = 'auto',
    **kwargs,
) -> str:
    '''Return the assistant message from an OpenAI-style chat completion.'''

    # Work out whether we should use a vision wrapper or text wrapper
    use_vision = _is_vision(model) or _is_vision(deployment_name)

    if isinstance(connection, AzureOpenAIConnection):
        wrapper_cls = AoaiVisionWrapper if use_vision else AoaiTextWrapper
        client = wrapper_cls(connection)
        return client.chat(
            prompt=prompt,
            deployment_name=deployment_name,
            model=model if not deployment_name else None,
            temperature=temperature,
            top_p=top_p,
            stream=stream,
            stop=stop,
            max_tokens=max_tokens,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            seed=seed,
            detail=detail if use_vision else None,
            **kwargs,
        )

    if isinstance(connection, OpenAIConnection):
        wrapper_cls = OpenAIVisionWrapper if use_vision else OpenAITextWrapper
        client = wrapper_cls(connection)
        extra = {'detail': detail} if use_vision else {}
        return client.chat(
            prompt=prompt,
            model=model,
            temperature=temperature,
            top_p=top_p,
            stream=stream,
            stop=stop,
            max_tokens=max_tokens,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            seed=seed,
            **extra,
            **kwargs,
        )

    raise InvalidConnectionType(
        message=f'Unsupported connection type {type(connection).__name__}.  '
                f'Use AzureOpenAIConnection or OpenAIConnection.'
    )
