from django.urls import path
from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('profile/', views.CurrentProfile.as_view(), name='current-profile'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),
    path('about-doctor-evil/', views.AboutDoctorEvil.as_view(), name='about-doctor-evil'),
    path('edit-user/<int:pk>/', views.UserUpdateView.as_view(), name='user-update'),
    path('transfer-money/', views.transfer_money, name='transfer-money'),
    path('transfer-money/statements/', views.upload_file, name='statements-on-evil'),
    path('transfer-money/statements/open/', views.open_evil_statement, name='open-evil-statement'),
    path('rsa-challenge/', views.rsa_challenge, name='rsa-challenge'),
    path('rsa-challenge/check-pair/<int:pk>/', views.rsa_challenge_check_rsa_pair, name='check-pair'),
    path('end-the-game/239854729587624398/', views.the_end_of_the_game, name='end-the-game'),
    path('victory-screen/238549042735324093/', views.victory_screen, name='victory-screen'),
    path('restart-the-game/', views.restart_the_game, name='restart-the-game'),
]