import pytest
from unittest.mock import patch, MagicMock
from plugins.jupyter_plugin.jupyter_api_client import JupyterClient
from config import JUPYTER_URL, JUPYTER_TOKEN, JUPYTER_NOTEBOOK_PATH
from unittest.mock import ANY


@pytest.fixture
def jupyter_client():
    return JupyterClient(
        jupyter_url=JUPYTER_URL,
        jupyter_token=JUPYTER_TOKEN,
        jupyter_notebook_path=JUPYTER_NOTEBOOK_PATH
    )

# Teste para inicialização do kernel
@patch("requests.post")
def test_start_kernel(mock_post, jupyter_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": "test_kernel_id"}
    mock_post.return_value = mock_response

    kernel_id = jupyter_client.start_kernel()

    mock_post.assert_called_once_with(
        f"{JUPYTER_URL}/api/kernels",
        headers=jupyter_client.headers,
        timeout=jupyter_client.request_timeout
    )
    assert kernel_id == "test_kernel_id"

# Teste para iniciar uma sessão
@patch("requests.post")
def test_start_session(mock_post, jupyter_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": "test_session_id"}
    mock_post.return_value = mock_response

    session_id = jupyter_client.start_session(kernel_id="test_kernel_id", session_name="test_session")

    mock_post.assert_called_once_with(
        f"{JUPYTER_URL}/api/sessions",
        headers=jupyter_client.headers,
        data=ANY,
        timeout=jupyter_client.request_timeout
    )
    assert session_id == "test_session_id"

# Teste para reinicializar o kernel
@patch("requests.post")
def test_restart_kernel(mock_post, jupyter_client):
    jupyter_client.restart_kernel(kernel_id="test_kernel_id")

    mock_post.assert_called_once_with(
        f"{JUPYTER_URL}/api/kernels/test_kernel_id/restart",
        headers=jupyter_client.headers,
        timeout=jupyter_client.request_timeout
    )

# Teste para deletar o kernel
@patch("requests.delete")
def test_delete_kernel(mock_delete, jupyter_client):
    jupyter_client.delete_kernel(kernel_id="test_kernel_id")

    mock_delete.assert_called_once_with(
        f"{JUPYTER_URL}/api/kernels/test_kernel_id",
        headers=jupyter_client.headers,
        timeout=jupyter_client.request_timeout
    )
