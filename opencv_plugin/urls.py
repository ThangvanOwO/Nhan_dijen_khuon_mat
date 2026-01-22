from django.urls import path
from . import views

app_name = 'opencv_plugin'

urlpatterns = [
    # Trang camera chính
    path('', views.camera_view, name='camera'),
    
    # Trang đăng ký khuôn mặt
    path('register/', views.register_camera_view, name='register_camera'),
    
    # Video streaming endpoint
    path('video_feed/', views.video_feed, name='video_feed'),
    path('register_feed/', views.register_video_feed, name='register_feed'),
    
    # API endpoints
    path('api/set-tolerance/', views.set_tolerance, name='set_tolerance'),
    path('api/toggle-enhance/', views.toggle_enhance, name='toggle_enhance'),
    path('api/recognized/', views.get_recognized, name='get_recognized'),
    path('api/all-recognized/', views.get_all_recognized, name='get_all_recognized'),
    path('api/end-session/', views.end_session, name='end_session'),
    path('api/stop/', views.stop_camera, name='stop_camera'),
    
    # API cho đăng ký khuôn mặt
    path('api/capture-face/', views.capture_face, name='capture_face'),
    path('api/save-registration/', views.save_registration, name='save_registration'),
    path('api/encode-faces/', views.encode_faces_api, name='encode_faces'),
]
