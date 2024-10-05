import websockets
import requests
import asyncio
import json


class JupyterClient:
    def __init__(self, jupyter_token, jupyter_url, jupyter_notebook_path, request_timeout=180, websocket_timeout=180):
        self.jupyter_token = jupyter_token
        self.jupyter_url = jupyter_url
        self.jupyter_notebook_path = jupyter_notebook_path
        self.request_timeout = request_timeout
        self.websocket_timeout = websocket_timeout
        self.kernel_uri = f"{self.jupyter_url}/api/kernels"
        self.session_uri = f"{self.jupyter_url}/api/sessions"
        self.socket_kernel_uri = f"{self.kernel_uri.replace('http', 'ws')}"
        self.headers = {
            "Authorization": f"Token {self.jupyter_token}",
            "Content-Type": "application/json"
        }

    def start_kernel(self):
        response = requests.post(self.kernel_uri, headers=self.headers, timeout=self.request_timeout)
        return response.json()["id"]

    def start_session(self, kernel_id, session_name):
        response = requests.post(
            self.session_uri,
            headers=self.headers,
            data=json.dumps({
                "name": session_name,
                "type": "notebook",
                "path": self.jupyter_notebook_path,
                "kernel": {"id": kernel_id}
            }),
            timeout=self.request_timeout
        )
        return response.json()["id"]

    def run_notebook_code(self, kernel_id, params=None):

        # Coloca todos os parâmetros, caso tenha, em uma string separados por break line
        param_code = "\n".join([f"{key} = None" if value is None else f"{key} = {json.dumps(value)}" for key, value in params.items()])

        # Adiciona os parametros antes de adicionar o script para rodar o notebook
        code = f"{param_code}\n%run {self.jupyter_notebook_path} \n%reset -f"
        print(f"Jupyter: Executando o código {code}...")

        asyncio.run(self.execute_notebook_code(kernel_id, code))

    async def execute_notebook_code(self, kernel_id, code):
        try:
            async with websockets.connect(
                f"{self.socket_kernel_uri}/{kernel_id}/channels",
                extra_headers={"Authorization": f"Token {self.jupyter_token}"},
                open_timeout=self.websocket_timeout
            ) as websocket:

                execute_request = {
                    'header': {
                        'msg_id': '',
                        'username': '',
                        'session': '',
                        'msg_type': 'execute_request',
                        'version': '5.0'
                    },
                    'parent_header': {},
                    'metadata': {},
                    'content': {
                        'code': code,
                        'silent': False,
                        'store_history': False,
                        'stop_on_error': True,
                    }
                }
                await websocket.send(json.dumps(execute_request))

                async for message in websocket:
                    response = json.loads(message)

                    # Checa erros durante a execução do notebook
                    if 'msg_type' in response and response['msg_type'] == 'error':
                        error_message = response['content']['evalue']
                        traceback = "\n".join(response['content'].get('traceback', []))
                        raise RuntimeError(f"----> Erro de execução: {error_message}\n ----> Traceback:\n{traceback}")

                    # Finaliza quando a execução é completada
                    if response['msg_type'] == 'execute_reply':
                        if response['content'].get('status') == 'error':
                            error_message = response['content'].get('evalue', 'Unknown error')
                            raise RuntimeError(f"----> Erro de execução: {error_message}")
                        break
        except asyncio.TimeoutError:
            raise RuntimeError("A conexão com o kernel do Jupyter atingiu o tempo limite.")

    def restart_kernel(self, kernel_id):
        requests.post(f"{self.kernel_uri}/{kernel_id}/restart", headers=self.headers, timeout=self.request_timeout)

    def delete_kernel(self, kernel_id):
        requests.delete(f"{self.kernel_uri}/{kernel_id}", headers=self.headers, timeout=self.request_timeout)
