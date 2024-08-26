from rest_framework import routers

from terrain import views


app_name = "terrain"

router = routers.SimpleRouter()
router.register(r"terrain", views.TerrainViewSet)

urlpatterns = router.urls
