from dataclasses import dataclass
from loguru import logger
from codespector.errors import NotValidCfgError

AGENT_URL_MAPPING = {
    'codestral': 'https://api.mistral.ai/v1/chat/completions',
    'chatgpt': 'https://api.openai.com/v1/chat/completions',
    'deepseek': 'https://api.deepseek.com/v1/chat/completions',
}

DEFAULT_AGENT_MODEL = {
    'codestral': 'codestral-latest',
    'chatgpt': 'gpt-4o',
    'deepseek': 'deepseek-chat',
}


@dataclass
class AgentInfo:
    model: str
    url: str
    headers: dict

    @classmethod
    def create(
        cls,
        chat_agent: str,
        chat_token: str,
        chat_model: str | None = None,
        completion_url: str | None = None,
    ) -> 'AgentInfo':
        if completion_url:
            url = completion_url
        else:
            url = AGENT_URL_MAPPING.get(chat_agent)

        if chat_model:
            model = chat_model
        else:
            model = DEFAULT_AGENT_MODEL.get(chat_agent)

        if model is None or url is None:
            raise NotValidCfgError('Invalid chat model or completions url')

        headers = {'Authorization': f'Bearer {chat_token}'}
        return cls(
            url=url,
            model=model,
            headers=headers,
        )
