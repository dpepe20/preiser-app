from django.urls import path, include
from rest_framework import routers
from home.models import *
from service.views import *


router = routers.DefaultRouter()
router.register(r'Cuentadante',cuentadante_viewset)
router.register(r'Prestamo',prestamo_viewset)
router.register(r'Aprendiz',Aprendiz_viewset)
router.register(r'Ficha',ficha_viewset)
router.register(r'Programa',programa_viewset)
router.register(r'Detalle_Prestamo',Detalle_Prestamo_viewset)
router.register(r'Bodega_Material',Bodega_Material_viewset)
router.register(r'Bodega',Bodega_viewset)
router.register(r'Material',Material_viewset)
router.register(r'Marca',Marca_viewset)
router.register(r'Categoria',Categoria_viewset)


urlpatterns = [
	path('api/',include(router.urls)),
	path('api-auth/',include('rest_framework.urls',namespace='rest_framework')),

]	