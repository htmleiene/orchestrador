from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('logs/', views.logs, name='logs'),
    path('debug/', views.debug, name='debug'),
    path('robots/', views.robots, name='robots'),
    path('add_automation/', views.add_automation, name='add_automation'),
    path('executar_automacao/<int:automacao_id>/', views.executar_automacao, name='executar_automacao'),
    path('robots_data/', views.robots_data, name='robots_data'),
    path('executar_debug/', views.executar_debug, name='executar_debug'),
    path('logs_debug/', views.logs_debug, name='logs_debug'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('automacoes/<int:automacao_id>/pause', views.pausar_automacao, name='pausar_automacao'),
    path('automacoes/<int:automacao_id>/resume', views.retornar_automacao, name='retornar_automacao'),
    path('automacoes/<int:automacao_id>/', views.executar_automacao, name='executar_automacao'),
    path('automacoes/<int:automacao_id>/remove', views.remover_automacao, name='remover_automacao'),

]
