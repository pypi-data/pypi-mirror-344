from pathlib import Path

import click
from environs import Env

from codespector.codespector import CodeSpector

BASE_PATH = Path(__file__).parent.parent

env = Env()
env.read_env(path=str(BASE_PATH / '.env'))


@click.option(
    '--exclude-file-ext',
    type=list,
    envvar='CODESPECTOR_EXCLUDE_FILE_EXT',
    help='Exclude file extensions from the review',
    show_envvar=True,
)
@click.option(
    '--result-file',
    type=str,
    help='Set file for saving the result',
    envvar='CODESPECTOR_RESULT_FILE',
    show_envvar=True,
)
@click.option(
    '--prompt-content',
    type=str,
    help='Prompt content which included to review prompt',
    envvar='CODESPECTOR_PROMPT_CONTENT',
    show_envvar=True,
)
@click.option(
    '--system-content',
    type=str,
    envvar='CODESPECTOR_SYSTEM_CONTENT',
    show_envvar=True,
    help='Content which used in system field for agent',
)
@click.option(
    '--output-dir',
    type=str,
    envvar='CODESPECTOR_OUTPUT_DIR',
    default='codespector',
    show_envvar=True,
    help='Select the output directory',
)
@click.option(
    '-b',
    '--compare-branch',
    type=str,
    help='Select the branch to compare the current one with',
)
@click.option(
    '--chat-agent',
    envvar='CODESPECTOR_CHAT_AGENT',
    show_envvar=True,
    help='Choose the chat agent to use you can use one from [codestral, chatgpt, deepseek]. Or set yours chat agent',
)
@click.option(
    '--chat-model',
    type=str,
    envvar='CODESPECTOR_CHAT_MODEL',
    show_envvar=True,
    help='Choose the chat model to use',
)
@click.option(
    '--chat-token',
    type=str,
    envvar='CODESPECTOR_CHAT_TOKEN',
    show_envvar=True,
)
@click.version_option(message='%(version)s')
@click.command()
def main(*args, **kwargs):
    codespector = CodeSpector.create(*args, **kwargs)
    codespector.review()


if __name__ == '__main__':
    main()
