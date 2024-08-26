from rest_framework import routers

from planet import views


app_name = "planet"

router = routers.SimpleRouter()
router.register(r"planet", views.PlanetViewSet)

urlpatterns = router.urls
