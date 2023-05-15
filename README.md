# idb
python components for connecting and querying an ibm i database in programmatic way 

## Setup and install
To install `ibmidb`, follow these steps:

1. Create a new virtual environment using a tool of your choice (e.g., venv, conda/mamba).
2. Install the package Paramiko by following the instructions on their [website](https://www.paramiko.org/installing.html).
3. Install the latest version of `ibmidb` via pip from [TestPyPi](https://test.pypi.org/project/ibmidb/):
```
pip install -i https://test.pypi.org/simple/ --no-deps ibmidb
```
When using TestPyPi, it is recommended to install the dependencies separetly since TestPyPI doesn’t have the same packages as the live PyPI, it’s possible that attempting to install dependencies may fail or install something unexpected.

Once you have installed `ibmidb`, you can import it in your Python code and use it to connect to and query an IBM i database.

## Example Usage

### IBM i Server Component

before using `ibmidb`, download and install the latest jar for CodeForIBMiServer on [github](https://github.com/ThePrez/CodeForIBMiServer/releases) using wget and place it in `$HOME/.vscode/` on the ibm i system you want to use:
```bash
$ cd $HOME/.vscode/
$ wget https://github.com/ThePrez/CodeForIBMiServer/releases/download/v1.0.0-alpha-4/codeforiserver-1.0.0-alpha-4.jar

```

### Setup Connection details

On your local machine activate your virtual environment with `ibmidb` installed. Create a dictionary with connection details for your ibm i system. The underlying authenication mechanisms use paramiko to connect to the ibm i system. 

```python
CONNECTION_DETAILS = {
    'hostname': 'host',
    'username': 'user',
    'password': 'password',
    'key_filename': 'path_to_pkey'
}
```
Authentication is attempted in the following order of priority:
  - The ``pkey`` or ``key_filename`` passed in (if any)

    - ``key_filename`` may contain OpenSSH public certificate paths
      as well as regular private-key paths; when files ending in
      ``-cert.pub`` are found, they are assumed to match a private
      key, and both components will be loaded. (The private key
      itself does *not* need to be listed in ``key_filename`` for
      this to occur - *just* the certificate.)

  - Any key we can find through an SSH agent
  - Any "id_rsa", "id_dsa" or "id_ecdsa" key discoverable in
    ``~/.ssh/``

    - When OpenSSH-style public certificates exist that match an
      existing such private key (so e.g. one has ``id_rsa`` and
      ``id_rsa-cert.pub``) the certificate will be loaded alongside
      the private key and used for authentication.

  - Plain username/password auth, if a password was given

### Create SSHClient and SQLJob using the `CONNECTION_DETAILS`:

```python
from ibmidb.client import SSHClient, SQLJob

CONNECTION_DETAILS = {
    'hostname': 'host',
    'username': 'user',
    'password': 'password'
}

client = SSHClient(CONNECTION_DETAILS)
job = SQLJob(client)
ret = job.connect()
print(ret)
```
Which will print out the connection response:

```
{'id': 'boop', 'job': '014206/QUSER/QZDASOINIT', 'success': True}
```

### Use `SQLJob` to run queries

```python
sql = "SELECT * FROM TABLE(QSYS2.SYSTEM_ACTIVITY_INFO())"
job = SQLJob(client)
job.connect()
results = job.query(sql)
print(results)
```

Output:

```
[{'AVERAGE_CPU_RATE': 80.0, 'AVERAGE_CPU_UTILIZATION': 0.77, 'MINIMUM_CPU_UTILIZATION': 0.0, 'MAXIMUM_CPU_UTILIZATION': 0.0}]
```

#### Note:

It is recommended at this time to use the `SSHClient` to create a new `SQLJob` for each new query. It may be helpful to write a driver function to create and execute the sql queries. Here is an example:

```python
def create_and_execute(sql: str, rows: int = None, conn=client):
    if sql is None:
        return
    job = SQLJob(conn)
    connection = job.connect()
    data = job.query(sql, rows=rows)
    job.close()
    return data

```






