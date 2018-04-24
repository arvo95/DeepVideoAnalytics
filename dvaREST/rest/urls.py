from django.conf.urls import url
import views

urlpatterns = [
    url('^script/$', views.run_script)
]
