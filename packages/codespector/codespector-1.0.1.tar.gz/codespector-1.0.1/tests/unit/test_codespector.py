import pytest
from unittest.mock import Mock, patch
from codespector.codespector import CodeSpector
from codespector.types import AgentInfo
from codespector.errors import NotValidCfgError


@pytest.fixture
def mock_response():
    return {'choices': [{'message': {'content': 'Test review content'}}]}


@pytest.fixture
def test_params():
    return {
        'chat_token': 'test_token',
        'chat_agent': 'chatgpt',
        'compare_branch': 'main',
        'system_content': 'test system content',
        'prompt_content': 'test prompt content',
        'result_file': 'result.txt',
        'output_dir': 'test_output',
    }


def test_codespector_create(test_params):
    codespector = CodeSpector.create(**test_params)

    assert codespector.chat_token == test_params['chat_token']
    assert codespector.chat_agent == test_params['chat_agent']
    assert codespector.compare_branch == test_params['compare_branch']
    assert len(codespector.pipeline) == 2


@pytest.mark.parametrize(
    'chat_agent,chat_model,expected_url,expected_model',
    [
        ('chatgpt', None, 'https://api.openai.com/v1/chat/completions', 'gpt-4o'),
        ('codestral', 'custom-model', 'https://api.mistral.ai/v1/chat/completions', 'custom-model'),
        ('deepseek', None, 'https://api.deepseek.com/v1/chat/completions', 'deepseek-chat'),
    ],
)
def test_agent_info_create(chat_agent, chat_model, expected_url, expected_model):
    agent_info = AgentInfo.create(chat_agent=chat_agent, chat_token='test_token', chat_model=chat_model)

    assert agent_info.url == expected_url
    assert agent_info.model == expected_model
    assert agent_info.headers == {'Authorization': 'Bearer test_token'}


def test_agent_info_create_invalid():
    with pytest.raises(NotValidCfgError):
        AgentInfo.create(chat_agent='invalid_agent', chat_token='test_token')


@patch('builtins.open', create=True)
@patch('subprocess.run')
@patch('os.path.exists')
@patch('os.makedirs')
def test_result_file_writing(mock_makedirs, mock_exists, mock_run, mock_open, test_params, mock_response):
    mock_file = Mock()
    mock_open.return_value.__enter__.return_value = mock_file
    mock_exists.return_value = False

    mock_run.return_value.stdout = 'test diff'

    mock_file.read.return_value = '{"original files": [], "diff": "test diff"}'

    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = mock_response
        mock_post.return_value.raise_for_status = Mock()

        codespector = CodeSpector.create(**test_params)
        codespector.review()

        write_calls = [args[0] for name, args, kwargs in mock_file.write.mock_calls]

        assert any('Test review content' in str(call) for call in write_calls)
