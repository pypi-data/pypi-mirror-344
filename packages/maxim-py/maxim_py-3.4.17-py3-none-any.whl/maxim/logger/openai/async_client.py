import logging
from typing import Any, AsyncGenerator, Dict, List, Optional, Union
from uuid import uuid4

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion, ChatCompletionChunk

from ..logger import (
    Generation,
    GenerationConfig,
    Logger,
    Trace,
    TraceConfig,
)
from .utils import OpenAIUtils


class MaximOpenAIAsyncClient:
    def __init__(self, client: AsyncOpenAI, logger: Logger):
        self._client = client
        self._logger = logger

    async def chat_completions_stream(
        self,
        messages: List[Dict[str, Any]],
        *,
        model: str,
        trace_id: Optional[str] = None,
        generation_name: Optional[str] = None,
        **kwargs: Any,
    ) -> AsyncGenerator[ChatCompletionChunk, None]:
        is_local_trace = trace_id is None
        final_trace_id = trace_id or str(uuid4())
        generation: Optional[Generation] = None
        trace: Optional[Trace] = None
        
        try:
            trace = self._logger.trace(TraceConfig(id=final_trace_id))
            gen_config = GenerationConfig(
                id=str(uuid4()),
                model=model,
                provider="openai",
                name=generation_name,
                model_parameters=OpenAIUtils.get_model_params(
                    **kwargs
                ),
                messages=OpenAIUtils.parse_message_param(messages),
            )
            generation = trace.generation(gen_config)
        except Exception as e:
            logging.error(f"Error in generating content: {str(e)}")

        stream = await self._client.chat.completions.create(
            messages=messages, # type: ignore
            model=model,
            stream=True,
            **kwargs
        )

        full_response = ""
        async for chunk in stream:
            try:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                if chunk.choices[0].finish_reason is not None and generation is not None:
                    generation.result(OpenAIUtils.parse_stream_response(chunk))
                    if is_local_trace and trace is not None:
                        trace.set_output(full_response)
                        trace.end()
                yield chunk
            except Exception as e:
                logging.error(f"Error in logging generation: {str(e)}")

    async def chat_completions(
        self,
        messages: List[Dict[str, Any]],
        *,
        model: str,
        trace_id: Optional[str] = None,
        generation_name: Optional[str] = None,
        **kwargs: Any,
    ) -> ChatCompletion:
        is_local_trace = trace_id is None
        final_trace_id = trace_id or str(uuid4())
        generation: Optional[Generation] = None
        trace: Optional[Trace] = None
        
        try:
            trace = self._logger.trace(TraceConfig(id=final_trace_id))
            gen_config = GenerationConfig(
                id=str(uuid4()),
                model=model,
                provider="openai",
                name=generation_name,
                model_parameters=OpenAIUtils.get_model_params(
                    **kwargs
                ),
                messages=OpenAIUtils.parse_message_param(messages),
            )
            generation = trace.generation(gen_config)
        except Exception as e:
            logging.error(f"Error in generating content: {str(e)}")

        response = await self._client.chat.completions.create(
            messages=messages, # type: ignore
            model=model,
            **kwargs
        )

        try:
            if generation is not None:
                generation.result(OpenAIUtils.parse_completion(response))
            if is_local_trace and trace is not None:
                trace.set_output(response.choices[0].message.content or "")
                trace.end()
        except Exception as e:
            logging.error(f"Error in logging generation: {str(e)}")

        return response