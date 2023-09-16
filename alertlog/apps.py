from django.apps import AppConfig


class AlertlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'alertlog'
    
    
    def ready(self):
        print("Starting Sheduler")
        from .Getdata import getdatafrom_mysql
        getdatafrom_mysql.start()
