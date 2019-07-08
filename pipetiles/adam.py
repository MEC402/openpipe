#
# Digital Asset Manager database interface class
#
#
import mysql.connector

class Adam:
    def connect(self,server,username,password,database):
          self.server = server
          self.username = username
          self.password = password
          self.database = database
          self.mydb = mysql.connector.connect(
             host=self.server, user=self.username, password=self.password,
             database=self.database
          )
          self.mycursor = self.mydb.cursor()
          print (server)

    def executeSql(self,sqlstring):
          self.mycursor.execute(sqlstring)
          self.mydb.commit()
          print (sqlstring)
