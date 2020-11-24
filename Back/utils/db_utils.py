import pymysql
import time

from config.config import MainDBConfig, AdDBConfig, Debug, SSHTunnel
from sshtunnel import SSHTunnelForwarder

class MySQLAD:
    def __init__(self):
        self.tunnelMain = ''
        self.tunnelAd = ''
      
    def connectMainDB(self):
        if Debug.status:
            self.tunnelMain = SSHTunnelForwarder(
                        (SSHTunnel.bastionIP, SSHTunnel.bastionPort),
                        ssh_username=SSHTunnel.userName,
                        ssh_pkey=SSHTunnel.pemKey,
                        remote_bind_address=(MainDBConfig.HOST, SSHTunnel.remotePort),  # addr which SSH server can access
                        local_bind_address=(SSHTunnel.localAddr, MainDBConfig.PORT)
                        )
            
            self.tunnelMain.start()
            time.sleep(1)
            
            conn = pymysql.connect(
                            host=self.tunnelMain.local_bind_host,
                            port=self.tunnelMain.local_bind_port,
                            user=MainDBConfig.USER,
                            passwd=MainDBConfig.PWD,
                            db=MainDBConfig.DB,
                            read_timeout=2
                            )
            return conn 
        
        conn = pymysql.connect(
                            host=MainDBConfig.HOST,
                            port=MainDBConfig.PORT,
                            user=MainDBConfig.USER,
                            passwd=MainDBConfig.PWD,
                            db=MainDBConfig.DB,
                            read_timeout=2
                            )
        
        print("DATABASE CONNECTED")

        return  conn
    

    def dbClose(self, cur, conn):
        cur.close()
        conn.close()
        if Debug and self.tunnelMain != "":
            self.tunnelMain.close()
            self.tunnelMain = ""
        elif Debug and self.tunnelAd != "":
            self.tunnelAd.close()
            self.tunnelAd = ""
        print("DATABASE DISCONNECTED")
