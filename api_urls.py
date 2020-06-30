from django.urls import path, include
from rest_framework import routers
from .views import (
    UserViewSet, ItemViewSet, ItemFilterListView
)

router = routers.DefaultRouter()
router.register('user', UserViewSet)
#router.register('item', ItemViewSet)
app_name = 'home'

urlpatterns = [
    path('', include(router.urls)),
    path('item/', ItemFilterListView.as_view(), name='item'),

]


#urlpatterns = router.urls
