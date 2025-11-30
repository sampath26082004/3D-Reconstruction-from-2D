from django.urls import path
from .views import upload_image, d3, save_image, confirm_conversion, home, gallery, delete_model, delete_all_models, signup_view, login_view, logout_view

urlpatterns = [
    path('', upload_image, name='upload_image'),
    path('gallery/', gallery, name='gallery'),
    path('gallery/delete/<str:model_id>/', delete_model, name='delete_model'),
    path('gallery/delete-all/', delete_all_models, name='delete_all_models'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('3d/<str:model_id>/', d3, name='d3_view'),
    path('save-image/', save_image, name='save_image'),
    path('confirm/<int:image_id>/', confirm_conversion, name='confirm_conversion'),
]