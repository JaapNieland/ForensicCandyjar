# imports from django
from django.urls import path
# imports from own code
from . import views


app_name='candyjar'         # appname under which it is registered to django framework
# list that tells django which view to use for which requested path
urlpatterns =[
    path('', views.Index.as_view(), name='index'),                  # index view
    path('lastWeek/', views.LastWeek.as_view(), name='lastWeek'),   # user friendly view of data points last week
    path('lastWeek_csv/', views.lastWeek_csv, name='lastWeek_csv'), # csv delivery of data points last week
    path('collect/', views.collect, name='collect')                 # page where data can be delivered to
]