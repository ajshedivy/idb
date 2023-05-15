from ibmidb.client import SSHClient, SQLJob

def main():
    connection_details = {"username": "ashedivy", "hostname": "ut24p60"}
    client = SSHClient(connection_details)
    job = SQLJob(client=client)
    outstr =  job.connect()
    print(outstr)
    sql = 'SELECT * FROM TABLE(QSYS2.SYSTEM_ACTIVITY_INFO())'
    res =  job.query(sql)
    print(res)
    
if __name__ == "__main__":
    main()