from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from .views.api.availability import Availability
from .views.api.equipment_class import EquipmentClass
from .views.api.equipment_location import EquipmentLocation
from .views.api.equipment_type import EquipmentType
from .views.api.equipment import Equipment
from .views.api.customer_type import CustomerType


router = DefaultRouter()
router.register(r'class', EquipmentClass, base_name='equipment-class')
router.register(r'location', EquipmentLocation, base_name='equipment-location')
router.register(r'type', EquipmentType, base_name='equipment-type')
router.register(r'equipment', Equipment, base_name='equipment')
router.register(r'availability', Availability, base_name='availability')
router.register(r'customer_type', CustomerType, base_name='customer-type')

urlpatterns = [
    url(r'^api/(?P<version>(v1|v2))/', include(router.urls)),
]
