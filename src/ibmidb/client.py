from typing import Any, Dict, List
import paramiko
import io
import json
import time


class JobStatus:
    Ready = 1
    Busy = 2
    NOT_STARTED = 3


class ServerComponent:
    @staticmethod
    def getInitCommand():
        return (
            "java -jar $HOME/.vscode/codeforiserver-1.0.0-alpha-4.jar && exit"
        )

    @staticmethod
    def writeOutput(content):
        # print(content)
        ...


class SSHClient:
    def __init__(self, connection_details: Dict[str, str]):
        self.connection_details = connection_details
        self._setup(connection_details)
        
    def _setup(self, connection_details):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._check_connection_details(connection_details)
            self.client.connect(**connection_details)
            self.client_ready = True
        except Exception:
            self.client_ready = False
            raise Exception(f"failed to setup ssh client: {connection_details}")
            

    def _check_connection_details(self, details: Dict[str, str]):
        required_keys = ("hostname",)
        if all(key in details for key in required_keys):
            return
        raise Exception(
            f"missing key from connection details. required keys: {required_keys}, provided connection details: {details}"
        )
        
    def get_connection_details(self):
        return self.connection_details

    def getConnection(self):
        return self.client
    
    def __del__(self):
        self.client.close()


class SSHChannel:
    def __init__(self, connection: paramiko.SSHClient):
        self.channel = connection.get_transport().open_session()
        self.channel.exec_command(ServerComponent.getInitCommand())
        self.status = JobStatus.Ready

    def send(self, content):
        if self.status == JobStatus.Ready:
            self.status = JobStatus.Busy
            ServerComponent.writeOutput(content)
            sent = self.channel.send(content + "\n")
            outString = ""
            while True:
                if self.channel.recv_ready():
                    outString += self.channel.recv(1024).decode()
                else:
                    time.sleep(0.1)
                    continue

                if outString.endswith("\n"):
                    self.status = JobStatus.Ready
                    ServerComponent.writeOutput(outString)
                    return outString

    def __del__(self):
        self.channel.close()


class SQLJob:
    def __init__(self, client: SSHClient, options: Dict[str, Any] = {}):
        self.status = JobStatus.Ready
        self.connection = client.getConnection()
        self.channel = SSHChannel(self.connection)
        self.options = options
        self.id: str | None

    def send(self, content):
        return  self.channel.send(content)

    def connect(self) -> Dict[str, Any]:
        self.status = JobStatus.Ready

        props = ";".join(
            [
                f'{prop}={",".join(self.options[prop]) if isinstance(self.options[prop], list) else self.options[prop]}'
                for prop in self.options
            ]
        )

        conn_obj = {
            "id": "boop",
            "type": "connect",
            "props": props if len(props) > 0 else "",
        }

        result = json.loads( self.send(json.dumps(conn_obj)))
        if result["success"] is not True:
            self.close()
            self.status = JobStatus.NOT_STARTED
            raise Exception(
                result["error"]
                or f"Failed to connect to server: {self.connection.get_connection_details()['hostname']}"
            )
            
        self.id = result['job']
        self.status = JobStatus.Ready
        return result
    
    def query(self, sql: str, rows: int = None) -> Any:
        sql_obj = {
            'id':'boop',
            'type': 'sql',
            'sql': sql,
            'rows': rows if rows else ""
        }
        
        result = json.loads( self.send(json.dumps(sql_obj)))
        
        if result['success'] is not True:
            raise Exception(result['error'] or f'Failed to run sql query: {sql}')
        
        return result['data']
        
    
    def close(self):
        exit_obj = {
            'id': 'boop',
            'type': 'exit'
        }
        
        self.send(json.dumps(exit_obj))