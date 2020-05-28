from django.urls import path,include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home',views.home,name='home'),
    path('home_display',views.home_display,name='home_display'),
    path('client',views.client,name="client"),
    path('create_client',views.create_client,name="create_client"),
    path('save_client',views.save_client,name="save_client"),
    path('save_client2',views.save_client2,name="save_client2"),
    path('search_clients',views.search_clients,name="search_clients"),
    path('edit_clients',views.edit_clients,name="edit_clients"),
    path('to_connection',views.to_connection,name="to_connection"),
    path('connection',views.connection,name="connection"),
    path('search_connection',views.search_connection,name="search_connection"),
    path('create_mail',views.create_mail,name="create_mail"),
    path('send_email',views.send_email,name="send_email"),
    path('file_import',views.file_import,name="file_import"),
    path('edit_connection',views.edit_connection,name="edit_connection"),
    path('save_connection',views.save_connection,name="save_connection"),
    path('business_talk',views.business_talk,name="business_talk"),
    path('create_business_talk',views.create_business_talk,name="create_business_talk"),
    path('save_business_talk',views.save_business_talk,name="save_business_talk"),
    path('search_business_talk',views.search_business_talk,name="search_business_talk"),
    path('complete_business_talk',views.complete_business_talk,name="complete_business_talk"),
    path('setting_password',views.setting_password,name="setting_password"),
    path('save_password',views.save_password,name="save_password"),
    path('import_clients',views.import_clients,name="import_clients"),



    # path('auth/', include('social_django.urls', namespace='social')),
]