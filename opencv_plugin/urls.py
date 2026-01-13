from django.urls import path
from . import views

app_name = 'opencv_plugin'

urlpatterns = [
    # Trang camera chính
    path('', views.camera_view, name='camera'),
    
    # Video streaming endpoint
    path('video_feed/', views.video_feed, name='video_feed'),
    
    # API endpoints
    path('api/set-tolerance/', views.set_tolerance, name='set_tolerance'),
    path('api/toggle-enhance/', views.toggle_enhance, name='toggle_enhance'),
    path('api/recognized/', views.get_recognized, name='get_recognized'),
    path('api/all-recognized/', views.get_all_recognized, name='get_all_recognized'),
    path('api/end-session/', views.end_session, name='end_session'),
    path('api/stop/', views.stop_camera, name='stop_camera'),
]
