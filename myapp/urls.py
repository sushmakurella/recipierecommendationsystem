from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns=[

    # path('',views.index,name='index'),
    path('',views.index,name='index'),
    path('collect',views.collect,name='collect'),
    path('test',views.test,name='test'),
    
    
]
urlpatterns += staticfiles_urlpatterns()
