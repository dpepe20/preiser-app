from rest_framework import serializers
from home.models import *


class Cuentadante_serializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Cuentadante
		fields = ('url','nombre','identificacion',)


class Aprendiz_serializer(serializers.ModelSerializer):

	class Meta:
		model = Aprendiz
		fields = ('url','nombre','identificacion','tipo_documento','estado','ficha','id')

class Material_serializer(serializers.ModelSerializer):
	class Meta:
		model = Material
		fields = ('tipo_elemento','nombre','codigo_sena','cantidad','estado','marca','categoria','cuentadante','ficha','imagen')

class Detalle_Prestamo_serializer(serializers.ModelSerializer):
	materiales = Material_serializer(many=True, read_only=True)
	
	class Meta:
		model = Detalle_Prestamo
		fields = ('id','url','material','estado_devolucion','cantidad','fecha_devolucion','materiales')
		depth = 2

class prestamo_serializer(serializers.ModelSerializer):

	detalles = Detalle_Prestamo_serializer(many=True, read_only=True)

	class Meta:
		model = Prestamo
		fields = ('id','url','fecha_prestamo','estado','aprendiz','fecha_entrega', 'detalles')
		depth =3	

class Ficha_serializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Ficha
		fields = ('url','numero_ficha','fecha_inicio','fecha_finalizacion','listado','programa',)

class Programa_serializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Programa
		fields = ('url','nombre')

class Bodega_Material_serializer(serializers.ModelSerializer):
	class Meta:
		model = Bodega_Material
		fields = ('material','bodega','fecha_ingresa','fecha_salida')
		depth=2


class Bodega_serializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Bodega
		fields = ('nombre','foto')


class Marca_serializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Marca
		fields = ('nombre',)

class Categoria_serializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Categoria
		fields = ('nombre',)


		
			
	
		
