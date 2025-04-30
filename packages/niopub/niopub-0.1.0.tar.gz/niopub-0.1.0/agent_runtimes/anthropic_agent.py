import asyncio
import sys
import signal
import json
from anthropic import AsyncAnthropic
from neosphere.agent import NeosphereAgent, NeosphereAgentTaskRunner
from neosphere.client_api import Message, NeosphereClient
from neosphere.extra_tools import BaseMessageLogger, MessageLogger, get_claude_like_message

import logging
import os

if os.getenv("NEOSPHERE_DEBUG", False):
    lvl = logging.DEBUG
else:
    lvl = logging.INFO
logging.basicConfig(level=lvl, format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
logger = logging.getLogger('neosphere').getChild('main')

MODEL_NAME = os.getenv("MODEL_NAME", "claude-3-5-sonnet-20241022")

def _get_best_conversation_name_for_message(query: Message):
    if query.group_id:
        return query.group_id
    else:
        fd_agent_id = os.getenv("FRONTDESK_AGENT_ID", "")
        return query.query_id if query.from_id != fd_agent_id else fd_agent_id

async def claude_text_prompt_forwarder(ai_backend: AsyncAnthropic, message_logger: BaseMessageLogger, msg: Message, client: NeosphereClient, system_prompt: str, model_name: str):
    conversation_name = _get_best_conversation_name_for_message(msg)
    message_logger.log_response(conversation_name, role="user", content=msg.text, media_ids=msg.data_ids) 

    response = await ai_backend.messages.create(
        model=model_name,
        max_tokens=1024,
        system=system_prompt,
        messages=message_logger.get_last_n_messages(4, conversation_name)
    )
    message_logger.log_response(conversation_name, role="assistant", content=response.content)
    while response.stop_reason == "tool_use":
        tool_use = next(block for block in response.content if block.type == "tool_use")
        query_id = client.query_agent(tool_use.name, tool_use.input, query_id=tool_use.id)
        tool_result: Message = client.wait_for_query_response(query_id)
        message_logger.log_response(conversation_name, role="user", content=tool_result.text, type="tool_result", tool_use_id=tool_result.query_id)
        response = ai_backend.messages.create(
            model=model_name,
            max_tokens=4096,
            messages=message_logger.get_last_n_messages(6, conversation_name)
        )
    final_response_text = next(
        (block.text for block in response.content if hasattr(block, "text")),
        None,
    )
    logger.debug(f"\nFinal Response: {len(final_response_text)} chars. Message History contains {len(message_logger.get_last_n_messages(6, conversation_name))} messages")
    return final_response_text

async def human_message_receiver(msg: Message, client: NeosphereClient, **ctx) -> str:
    ai_client: AsyncAnthropic = ctx.get('ai_client', None)
    message_logger: BaseMessageLogger = ctx.get('message_logger', None)
    model_name = ctx.get('model_name', None)
    system_prompt = ctx.get('system_prompt', None)
    final_response_text = await claude_text_prompt_forwarder(ai_client, message_logger, msg, client, system_prompt, model_name)
    await client.respond_to_group_message(msg.group_id, final_response_text)

async def agent_query_receiver(query: Message, client: NeosphereClient, **ctx):
    logger.error(f"Agent Query Received {query.to_json()}")
    return

class AnthropicAgent:
    def __init__(self, form_data):
        self.form_data = form_data
        self.running = True
        self.api_key = form_data.get('api_key')
        self.agent_id = form_data.get('agent')
        self.conn_code = form_data.get('conn_code')
        self.url = form_data.get('url')
        self.host_nickname = form_data.get('host_nickname', 'macbookpro-m2')

    async def run(self):
        ai_client = AsyncAnthropic(api_key=self.api_key)
        message_logger = MessageLogger(message_maker=get_claude_like_message)
        system_prompt = self.form_data.get('system_prompt', '')
        model_name = self.form_data.get('model_name', "claude-3-5-sonnet-20241022")
        agent = NeosphereAgent(
            self.agent_id,
            self.conn_code,
            self.host_nickname,
            group_message_receiver=human_message_receiver,
            query_receiver=agent_query_receiver,
            ai_client=ai_client,
            message_logger=message_logger,
            system_prompt=system_prompt,
            model_name=model_name,
        )
        
        niopub_connection = NeosphereAgentTaskRunner(agent, self.url)
        niopub_agent = asyncio.create_task(niopub_connection.run())
        await asyncio.gather(niopub_agent)

def print_help():
    help_data = {
        "display_name": "anthropic",
        "fields": [
            {
                "name": "api key",
                "type": "text",
                "required": True
            },
            {
                "name": "agent",
                "type": "text",
                "required": True
            },
            {
                "name": "conn code",
                "type": "text",
                "required": True
            },
            {
                "name": "system prompt",
                "type": "text",
                "required": False
            },
            {
                "name": "model_name",
                "type": "select",
                "options": ["claude-3-5-sonnet-20241022", "female"],
                "required": False
            },
            {
                "name": "url",
                "type": "text",
                "required": False
            },
            {
                "name": "host nickname",
                "type": "text",
                "required": False
            }
        ]
    }
    print(json.dumps(help_data))

def signal_handler(signum, frame):
    sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print_help()
        sys.exit(0)

    if len(sys.argv) != 2:
        print("Usage: python anthropic.py <form_data_json>")
        sys.exit(1)

    try:
        form_data = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        print("Error: Invalid JSON input")
        sys.exit(1)

    # Set up signal handlers
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    agent = AnthropicAgent(form_data)
    asyncio.run(agent.run())
