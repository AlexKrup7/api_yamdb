from django.urls import include, path
from rest_framework import routers

from .views import APIRegistration, APIToken, UserViewSet

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', APIRegistration.as_view()),
    path('v1/auth/token/', APIToken.as_view())
]
