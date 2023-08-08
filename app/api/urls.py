from rest_framework.routers import SimpleRouter

from .views import MessageViewSet

router = SimpleRouter()

router.register(r'message', MessageViewSet)

urlpatterns = []

urlpatterns += router.urls