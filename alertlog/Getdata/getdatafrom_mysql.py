import mysql.connector
from mysql.connector import Error
import sqlite3
import pymysql.cursors
from  alertlog import  views



from apscheduler.schedulers.background import BackgroundScheduler


def start():
  scheduler = BackgroundScheduler()

  scheduler.add_job(views.getLogs_from_db, "interval", minutes=1,id="weather",replace_existing=True)
  scheduler.start()




# def getLogs_from_db():
# # Connect to the database
#     connection = pymysql.connect(host='192.168.0.254',
#                                 user='kiber',
#                                 password='kibeR@2023@Kiber',
#                                 database='logsdb',
#                                 cursorclass=pymysql.cursors.DictCursor)

#     with connection:


#         with connection.cursor() as cursor:
#             # Read a single record
#             #sql = "SELECT   timestamp, hostname, facility, severity, application, message FROM `table_kiber` WHERE `id` >= 400000 LIMIT 250"
#             sql = "SELECT   timestamp, hostname, facility, severity, application, message FROM `table_kiber` WHERE  message  like ('%DHCPDISCOVER%')"
#             #sql = "SELECT  * FROM `table_kiber` WHERE `id` > 400000  LIMIT 5"
#             cursor.execute(sql)
#             result_mysqllog = cursor.fetchall()

            
#             result_mysqllog_tuples = [(row['timestamp'], row['hostname'], row['facility'], row['severity'], row['application'], row['message']) for row in result_mysqllog]
#             #print(result_mysqllog)

#                     # Establish a connection to the SQLite database
#             connection_sqlite = sqlite3.connect('../../db.sqlite3')
#             #with connection_sqlite.cursor() as cursor2:
#             # Create a cursor object
#             cursor2 = connection_sqlite.cursor()
#             # sql2 = "INSERT INTO `alertlog_filterlog` (`timestamp`,`hostname`,`facility`,`severity`,`application`,`message`) VALUES(?,?,?,?,?,?)"
#             # Execute the SELECT query


#             #cursor2.executemany("INSERT INTO `alertlog_filterlog` (`timestamp`,`hostname`,`facility`,`severity`,`application`,`message`) VALUES(?,?,?,?,?,?)", result_mysqllog)

#             cursor2.executemany("INSERT INTO alertlog_filterlog (timestamp, hostname, facility, severity, application, message) VALUES (?, ?, ?, ?, ?, ?)", result_mysqllog_tuples)
#             print("Maglumat gosuldy")
#     # Commit the changes to SQLite
#             connection_sqlite.commit()

#     # Close the SQLite cursor and connection
#             cursor2.close()
#             connection_sqlite.close()


# getLogs_from_db()
