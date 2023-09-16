from django.db import models



from django.contrib.auth.models import User

# class Todo(models.Model):
#     task = models.CharField(max_length = 180)
#     timestamp = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
#     completed = models.BooleanField(default = False, blank = True)
#     updated = models.DateTimeField(auto_now = True, blank = True)
#     user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)

#     def __str__(self):
#         return self.task
    
    


class Roles(models.Model):
    name = models.CharField(max_length=150 , null=False)
    description = models.TextField(null=False)
    role_severity = models.CharField(max_length=50, null= False)
    def __str__(self):
        return self.name


class Filterlog(models.Model):
    hostname = models.CharField(max_length=150, null=False)
    severity = models.CharField(max_length=50, null=False)
    facility = models.CharField(max_length=50, null=False)
    application = models.CharField(max_length=70, null=False)
    message  = models.TextField(null=False)
    timestamp =models.DateTimeField(auto_now=False)
    role = models.CharField(max_length=350, null=False)
    is_know = models.BooleanField(default =False)

    
    def __str__(self):
        return (self.hostname + self.message)
    
    
class Hostnames(models.Model):
    hostname  =  models.CharField(max_length=150, null=False)
    ipaddress = models.CharField(max_length=50, null=False)
    
    def __str__(self):
        return self.hostname
    
    
class role_text(models.Model):
	role_id = models.ForeignKey(Roles, on_delete=models.CASCADE)
