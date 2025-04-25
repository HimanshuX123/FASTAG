from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.SignupPage, name='signup'),
    path('login/', views.LoginPage, name='login'),
    path('', views.HomePage, name='home'),
    path('logout/', views.LogoutPage, name='logout'),
    path('about/', views.AboutPage, name='about'),
    path('contact/', views.ContactPage, name='contact'),

    # Show registration form
    path('register/', views.RegisterPage, name='Register'),

    # Handle form submission
    path('register/submit/', views.register, name='register'),

    # User profile
    path('profile/<int:user_id>/', views.profile, name='profile'),

    # QR Code display page
    path('qr_display/<int:user_id>/', views.qr_display, name='qr_display'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('make_payment/', views.make_payment, name='make_payment'),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("delete-user/<int:user_id>/", views.delete_user, name="delete_user"),
    path("admin-logout/", views.admin_logout, name="admin_logout"),
    path("admin-login/", views.admin_login, name="admin_login"),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path("profile/stop_service/", views.stop_service, name="stop_service"),
    path('upload_profile_picture/', views.upload_profile_picture, name='upload_profile_picture'),
    path('remove_profile_image/', views.remove_profile_image, name='remove_profile_image'),
    path('generate_qr/<int:user_id>/', views.generate_qr, name='generate_qr'),

]
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
