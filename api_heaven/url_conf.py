from django.urls import path,include
from .views import EmailTokenObtainPairView,profile,create_table,add_to_table
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("login/google",EmailTokenObtainPairView.as_view(), name='token_obtain_pair_email'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', profile, name='profile'),
    path('create_table/', create_table, name='create_table'),
    path('<str:table_uuid>/add_to_table/', add_to_table, name='add_to_table'),
]
