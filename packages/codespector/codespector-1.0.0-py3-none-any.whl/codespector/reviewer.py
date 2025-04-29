import os.path

import json
from urllib.error import HTTPError

import requests

from loguru import logger

from codespector.errors import AppError
from codespector.types import AgentInfo


class CodeSpectorReviewer:
    def __init__(
        self,
        diff_file: str,
        chat_token: str,
        chat_agent: str,
        chat_model: str,
        system_content: str,
        prompt_content: str,
        output_dir: str,
        result_file: str,
        agent_info: AgentInfo,
    ):
        self.diff_file = diff_file
        self.chat_token = chat_token
        self.chat_agent = chat_agent
        self.chat_model = chat_model
        self.system_content = system_content
        self.prompt_content = prompt_content
        self.output_dir = output_dir
        self.result_file = result_file
        self.agent_info = agent_info

        self.request_file = 'request.json'
        self.response_file = 'response.json'

    def _request_to_chat_agent(self, prompt: str):
        request_data = {
            'model': self.agent_info.model,
            'messages': [{'role': 'system', 'content': self.system_content}, {'role': 'user', 'content': prompt}],
        }

        with open(os.path.join(self.output_dir, self.request_file), 'w', encoding='utf-8') as f:
            json.dump(request_data, f, indent=4, ensure_ascii=False)

        response = requests.post(
            self.agent_info.url,
            json=request_data,
            headers=self.agent_info.headers,
            timeout=100,
        )
        response.raise_for_status()
        return response

    def send_to_review(self):
        with open(os.path.join(self.output_dir, self.diff_file), 'r', encoding='utf-8') as f:
            diff_data = json.load(f)

        diff_content = diff_data.get('diff', '')
        original_files = diff_data.get('original files', [])

        original_files_str = json.dumps(original_files, indent=4, ensure_ascii=False)

        prompt = f'{self.prompt_content}\n\nDIFF:\n{diff_content}\n\nORIGINAL FILES:\n{original_files_str}'
        try:
            response = self._request_to_chat_agent(prompt=prompt)
        except HTTPError as e:
            logger.error('Error while send request: {}', e)
            raise AppError('Error while send request') from e

        with open(os.path.join(self.output_dir, self.response_file), 'w', encoding='utf-8') as f:
            json.dump(response.json(), f, indent=4, ensure_ascii=False)

        resp = response.json()
        clear_response = resp['choices'][0]['message']['content']

        with open(os.path.join(self.output_dir, self.result_file), 'w', encoding='utf-8') as f:
            f.write(clear_response)

    def start(self):
        self.send_to_review()
