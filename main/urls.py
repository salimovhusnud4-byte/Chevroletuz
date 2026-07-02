from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),

    # Admin panel
    path('admin-panel/', views.admin_panel, name='admin_panel'),

    # Cars CRUD
    path('admin-panel/cars/add/', views.car_add, name='car_add'),
    path('admin-panel/cars/<int:car_id>/edit/', views.car_edit, name='car_edit'),
    path('admin-panel/cars/<int:car_id>/delete/', views.car_delete, name='car_delete'),
    path('admin-panel/cars/<int:car_id>/toggle-discount/', views.car_toggle_discount, name='car_toggle_discount'),

    # Highlights CRUD
    path('admin-panel/highlights/add/', views.highlight_add, name='highlight_add'),
    path('admin-panel/highlights/<int:highlight_id>/edit/', views.highlight_edit, name='highlight_edit'),
    path('admin-panel/highlights/<int:highlight_id>/delete/', views.highlight_delete, name='highlight_delete'),
]
