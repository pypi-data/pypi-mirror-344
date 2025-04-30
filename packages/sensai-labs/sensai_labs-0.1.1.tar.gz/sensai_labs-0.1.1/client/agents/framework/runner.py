import copy
import json
from collections import defaultdict
from typing import Dict, Optional

from openai import OpenAI
from openai.types.chat import ChatCompletionMessage

from client.agents.framework.base import Agent, AgentConfig
from client.agents.framework.result_handler import ToolCallHandler
from client.agents.framework.types import TaskResponse
from shared.utils import debug_print


class AppRunner:
    def __init__(self, config: AgentConfig):
        self.config = config
        self.openai_client = OpenAI(api_key=config.api_key)
        self.tool_handler = ToolCallHandler()
        self.messages = []  # Store messages internally

    def run(
        self,
        agent: Agent,
        query: str,
        context_variables: Optional[Dict] = None,
    ) -> TaskResponse:
        
        # Add the new user query to messages
        self.messages.append({"role": "user", "content": query})

        loop_count = 0
        active_agent = agent
        context_variables = copy.deepcopy(context_variables or {})
        history = copy.deepcopy(self.messages)
        init_len = len(history)

        while loop_count < self.config.max_interactions:
            print("")
            debug_print(f"-----------LOOP COUNT: {loop_count + 1}-----------")
            debug_print(f"Active agent: {active_agent.name}")
            llm_params = self.__create_inference_request(
                agent=active_agent,
                history=history,
                context_variables=context_variables,
                token_limit=self.config.token_limit,
            )

            # Make the API call
            response = self.openai_client.chat.completions.create(**llm_params)
            debug_print("RESPONSE:", response)
            message: ChatCompletionMessage = response.choices[0].message
            message.sender = active_agent.name
            history_msg = json.loads(message.model_dump_json())
            history.append(history_msg)
            loop_count += 1

            if not message.tool_calls:
                debug_print("No tool calls found in the response")
                break
            debug_print("Tool calls:", message.tool_calls)

            tool_response = self.tool_handler.handle_tool_calls(
                message.tool_calls,
                active_agent.functions,
            )
            debug_print("TOOL RESPONSE:", tool_response)
            history.extend(tool_response.messages)

            if tool_response.agent:
                debug_print(f"Switching to agent: {tool_response.agent.name}")
                active_agent = tool_response.agent

        # Update the internal messages with the new history
        self.messages = history

        return TaskResponse(
            messages=history[init_len:],
            agent=active_agent,
            context_variables=context_variables,
        )

    def __create_inference_request(
        self, agent: Agent, history: list, context_variables: dict, token_limit: int
    ) -> dict:
        context_variables = defaultdict(str, context_variables)
        instructions = agent.get_instructions(context_variables)
        messages = [{"role": "system", "content": instructions}] + history
        tools = agent.tools_in_json()
        debug_print("Getting chat completion for...:", str(messages))

        params = {
            "model": agent.model,
            "messages": messages,
            "tool_choice": agent.tool_choice,
            "max_tokens": token_limit,
        }
        # Add tools if defined in the agent
        if tools:
            params["parallel_tool_calls"] = agent.parallel_tool_calls
            params["tools"] = tools

        return params
