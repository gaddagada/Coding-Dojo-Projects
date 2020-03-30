from django.urls import path
from . import views

urlpatterns=[
    path('', views.index),
    path('register/', views.register), 
    path('login/', views.login),
    path('success/', views.success),
    path('logout/', views.logout),
    path('traveldashboard/', views.showtraveldashboard),
    path('addTrip/', views.addTrip),
    path('saveTrip/', views.saveTrip), 
    path('join/<id>', views.joinTrip),
    path('removeTrip/<id>', views.removeTrip),
    path('editTrip/<id>', views.editTrip),
    path('updateTrip/<id>', views.updateTrip),
    path('cancelTrip/<id>', views.cancelTrip),    
    path('destination/<id>', views.showDestination)
    
    # path('organizations/', views.organizations),
    # path('addOrganization/', views.addOrganization),
    # path('organizations/<orgid>/', views.showOrganization), 
    # path('joinOrganization/<orgid>', views.joinOrganization),
    # path('leaveOrganization/<orgid>', views.leaveOrganization) 
    
    #path('new/', views.new),
    #path('users/', views.user)
]