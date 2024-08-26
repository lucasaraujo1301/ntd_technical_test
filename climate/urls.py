from rest_framework import routers

from climate import views


app_name = "climate"

router = routers.SimpleRouter()
router.register(r"climate", views.ClimateViewSet)

urlpatterns = router.urls
