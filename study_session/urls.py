from django.urls import path
from . import views

app_name = 'study_session'

urlpatterns = [
    path('', views.study_room, name='room'),
    path('navigator/', views.navigator_view, name='navigator'),
    path('api/navigator_command/', views.navigator_command, name='navigator_command'),
    path('api/delete_block/<int:block_id>/', views.delete_study_block, name='delete_block'),
    path('api/data/', views.get_room_data, name='get_room_data'),
    path('api/send/', views.send_message, name='send_message'),
    path('api/search_users/', views.search_users, name='search_users'),
    path('api/add_friend/', views.add_friend, name='add_friend'),
    path('api/get_friends/', views.get_friends, name='get_friends'),
]
