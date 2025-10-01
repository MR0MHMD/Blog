from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'Blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/<str:category>', views.post_list, name='post_list_category'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('ticket/', views.ticket, name='ticket'),
    path('posts/<int:pk>/comments/', views.post_comment, name='post_comment'),
    path('search/', views.post_search, name='post_search'),
    path('profile/', views.profile, name='profile'),
    path('profile/create_post/', views.create_post, name='create_post'),
    path('profile/create_post/<int:pk>', views.edit_post, name='edit_post'),
    path('profile/delete_post/<int:pk>', views.delete_post, name='delete_post'),
    path('profile/delete_image/<int:pk>', views.delete_image, name='delete_image'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(success_url='done'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(success_url='done'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url='/blog/password_reset/complete/'), name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('register/', views.register, name='register'),
    path('account/edit', views.edit_account, name='edit_account'),
    path('profile/detail/<int:user_id>', views.profile_detail, name='profile_detail'),
]
