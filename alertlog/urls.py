from alertlog import views
from django.urls import path
from rest_framework import routers


router = routers.DefaultRouter(trailing_slash=False)

router.register('logs',views.AlertLogListApiView)
router.register('role',views.RulesListApiView)


urlpatterns = [
    path('',views.index , name='home'),
    path('api/', views.TodoListApiView.as_view()),
    path('filter/',views.ReporAPIVIEW.as_view()),
]+router.urls
