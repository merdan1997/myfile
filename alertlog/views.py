from django.shortcuts import render
from django.shortcuts import HttpResponse
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from alertlog.models import Filterlog, Roles
from alertlog.serializers import AllFilterLogSerializer, RoleSerializer
from rest_framework import status
import sqlite3
import pymysql.cursors
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
import  pymysql
from django.db import connections



# Create your views here.
def  index(request):
    return HttpResponse("Welcome")

class AlertLogListApiView(ModelViewSet):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticatedOrReadOnly ]

    queryset = Filterlog.objects.all().order_by('-timestamp')
    serializer_class = AllFilterLogSerializer

class RulesListApiView(ModelViewSet):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.AllowAny ]
    http_method_names = ['get', 'put','post', 'patch', 'head', 'options', 'trace', 'delete',]
    queryset = Roles.objects.all()
    serializer_class = RoleSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=204)
    
    def perform_destroy(self, instance):
        instance.delete()



class TodoListApiView(APIView):
    #
    permission_classes = [permissions.AllowAny]
    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        #todos = Filterlog.objects.filter(user = request.user.id)
        todos = Filterlog.objects.all()
        serializer = AllFilterLogSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#def getLogs_from_db():
#	print("ok")
#    import pymysql

# Establish a connection to the database
#    connection = pymysql.connect(
#        host='192.168.0.254',
#        user='kiber',
 #       password='kibeR@2023@Kiber',
 #       database='logsdb',
 #       cursorclass=pymysql.cursors.DictCursor
 #   )

 #   try:
  #      with connection.cursor() as cursor:
            # Retrieve all rules
 #           rules = Roles.objects.all()

            # Create a list to store the search patterns
 #           search_patterns = []

 #           for rule in rules:
                # Append the search pattern for each rule to the list
 #               search_patterns.append('%' + rule.description + '%')

            # Define the SQL query with multiple patterns using OR operator
 #           sql = "SELECT timestamp, hostname, facility, severity, application, message, id FROM `table_kiber` WHERE "
#            sql += " OR ".join(["message LIKE %s"] * len(search_patterns))
 #           sql += " COLLATE utf8mb4_unicode_ci"
#            sql = "SELECT * FROM  `table_kiber` LIMIT 200 "
            # Execute the query with the search patterns
 #           cursor.execute(sql, search_patterns)
#            cursor.execute(sql)

            # Fetch all the rows returned by the query
 #           result_mysqllog = cursor.fetchall()

            # Process the retrieved rows as needed
#            for row in result_mysqllog:
#                timestamp = row['timestamp']
#                hostname = row['hostname']
#                facility = row['facility']
#                severity = row['severity']
#                application = row['application']
#                message = row['message']

                # Perform further processing or save the logs to the model
#                task = Filterlog(
#                    timestamp=timestamp,
#                    hostname=hostname,
#                    facility=facility,
#                    severity=severity,
 #                   application=application,
 #                   message=message
  #              )
 #               task.save()

#        print(result_mysqllog, "Logs filtered and saved successfully.")

#    except pymysql.Error as e:
#        print(f"An error occurred: {str(e)}")

#    finally:
        # Close the connection
#        connection.close()








class ReporAPIVIEW(APIView):
    def get(self, request, *args , **kwargs):
            hostname = request.GET.get('hostname')
            severity = request.GET.get('severity')
            time1 = request.GET.get('time1')
            time2 = request.GET.get('time2')
            rolename  = request.GET.get('rolename')
            filterlogs = Filterlog.objects.all().order_by('-timestamp')
            if hostname:
                filterlogs = filterlogs.filter(Q(hostname__icontains=hostname)) 
            if severity :
                filterlogs = filterlogs.filter(severity__icontains = severity)
            if  time1 and time2 :
                print(time1, "ok  ",time2 )
                filterlogs = filterlogs.filter(timestamp__range=(time1, time2))

            serializer = AllFilterLogSerializer(filterlogs, many=True)
            return Response({
                "data":serializer.data,
               }
                ,
                status=status.HTTP_200_OK)
           # else:
            #    return Response({"message":"Sizin rugsadynyz yok"}, status=status.HTTP_404_NOT_FOUND)

def getLogs_from_db():
	import mysql.connector

# db1 bağlantısı
connection_db1 =pymysql.connect(
    host="192.168.0.254",
    user="kiber",
    password="kibeR@2023@Kiber",
    database="logsdb"
)
cursor_db1 = connection_db1.cursor()

# db2 bağlantısı
connection_db2 = pymysql.connect(
    host="192.168.9.25",
    user="alert",
    password="P@ssword1234560",
    database="Alertsystem"
)
cursor_db2 = connection_db2.cursor()

# db2'den verileri seçme
cursor_db2.execute("SELECT description, name FROM alertlog_roles")
db2_data = cursor_db2.fetchall()

# Filtreleme ve verileri db2.filterlog tablosuna yazma
for row in db2_data:
    description = row[0]
    role_name = row[1]

    # Verileri db1.table_kiber tablosunda filtreleme
    cursor_db1.execute("SELECT id, hostname, severity, facility, application, message, timestamp FROM table_kiber WHERE  message = %s LIMIT 1 ", (description,))
    filtered_data = cursor_db1.fetchall()

    # Verileri db2.filterlog tablosuna yazma
    for filtered_row in filtered_data:
        id, hostname, severity, facility, application, message, timestamp = filtered_row

        insert_query = "INSERT INTO alertlog_filterlog (hostname, severity, facility, application, role, timestamp, message) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (hostname, severity, facility, application, role_name , timestamp , message)
        cursor_db2.execute(insert_query, values)
        connection_db2.commit()

# Bağlantıları kapatma
cursor_db1.close()
connection_db1.close()
cursor_db2.close()
connection_db2.close()
