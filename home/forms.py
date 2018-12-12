from django import forms
from django.contrib.auth.models import User
from .models import *
import time
#formulario de registro
class register_form(forms.Form):
	username =forms.CharField(widget=forms.TextInput(attrs={
		'id':'username','class':'form-control','placeholder':'Nombre de Usuario','autofocus':'autofocus',
		}))
	email    =forms.EmailField(widget=forms.TextInput(attrs={
		'id':'email','class':'form-control','placeholder':'Correo Electronico','autofocus':'autofocus',
		}))
	password_1 = forms.CharField(widget=forms.PasswordInput(render_value=False,attrs={
		'id':'password','class':'form-control','placeholder':'Contraseña','autofocus':'autofocus',
		}))
	password_2 = forms.CharField(widget=forms.PasswordInput(render_value=False,attrs={
		'id':'password2','class':'form-control','placeholder':'placeholder','autofocus':'autofocus',
		}))

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			u= User.objects.get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError('Nombre de Usuario ya Registrado')

	def clean_email(self):
		email = self.cleaned_data['email']
		try:
			email = User.objects.get(email=email)
		except User.DoesNotExist:
			return email
		raise forms.ValidationError('Correo Electronico ya Existe')

	def clean_password_2(self):
		password_1 =self.cleaned_data['password_1']
		password_2 =self.cleaned_data['password_2']
		if not len(password_1)>7:
			raise forms.ValidationError('La contraseña debe contener minimo 8 caracteres')
		else:
			pass 
		if password_1==password_2:
			pass
		else:
			raise forms.ValidationError('Las contraseñas no coinciden')
class login_form (forms.Form):
	user = forms.CharField(widget=forms.TextInput(attrs={'class':'input100','name':'username',
														'placeholder':'Nombre de Usuario'}))
	password= forms.CharField(widget=forms.PasswordInput(render_value=False,attrs={'class':'input100',
													'name':'pass','placeholder':'Contraseña'}))
#formulario de la tabla nombre_material
class agregar_nombre_material_form(forms.ModelForm):
	class Meta:
		model = Nombre_Material
		fields = '__all__'
		widgets = {
			'nombre' : forms.TextInput(attrs={
			'id' : 'nombre','class':'form-control','placeholder':'Nombre',
										'autofocus': 'autofocus'
			}),
		}

#formulario de la tabla material
class agregar_material_form(forms.ModelForm):
	tipo_elemento = forms.ChoiceField(choices=([('Devolutivo','Devolutivo'), ('Consumible','Consumible') ]), initial='1', required = True,)
	class Meta:
		model = Material
		fields = '__all__'
#fromulario de la tabla material
class agregar_marca_form(forms.ModelForm):
	class Meta:
		model = Marca
		fields = '__all__'
		widgets = {
		'nombre' : forms.TextInput(attrs={
			'id' : 'nombre','class':'form-control','placeholder':'Nombre',
										'autofocus': 'autofocus'
			}),
		}
#formularios de la tabla prestamo
# documentar
class agregar_prestamoF(forms.ModelForm):
	aprendiz = forms.CharField(widget=forms.TextInput(attrs={'id':'busquedProyecto',
														'placeholder':'identificacion del aprendiz'}))

	class Meta:
		model=Prestamo
		exclude =['estado']
		fields=['fecha_prestamo','fecha_entrega']#,'aprendiz']
		widgets = {
					'fecha_prestamo':forms.TextInput(attrs={'class':'datepicker'}),
					'fecha_entrega' : forms.TextInput(attrs={'class':'datepicker'})
		}
		
	def clean(self):
		cleaned_data = super(agregar_prestamoF,self).clean()
		fecha_prestamo =self.cleaned_data['fecha_prestamo']
		fecha_entrega = self.cleaned_data['fecha_entrega']
		fecha_actual = time.strftime("%Y-%m-%d")
		if str(fecha_prestamo)>str(fecha_actual):
			raise forms.ValidationError('La Fecha de prestamo no debe ser mayor a la fecha actual')
		elif str(fecha_prestamo)<str(fecha_actual):
			raise forms.ValidationError('La Fecha de prestamo no debe ser menor a la fecha actual')
		elif fecha_entrega < fecha_prestamo:
			raise forms.ValidationError('La fecha de entrega no debe ser menor a la fecha de prestamo') 
		elif str(fecha_actual)==str(fecha_prestamo):
			pass
		return cleaned_data
# documentar

class agregar_DPrestamoF(forms.ModelForm):
	try:
		material=forms.ModelChoiceField(queryset=Material.objects.filter(estado='Disponible'))
	except:
		print ("vvvvvvvvvvvvvv")
		print ("ERROR CONSULTA")
		print ("vvvvvvvvvvvvvv")
	
	class Meta:
		model=Detalle_Prestamo
		fields=['material','cantidad']
		widgets={
			'material':forms.Select(attrs={'required':'true'}),
			'cantidad' :forms.TextInput(attrs={'type':'number','min':'0'}),

		}
class editar_DPrestamoF(forms.ModelForm):
	material = Material.objects.filter(estado="No Disponible")
	class Meta:
		model=Detalle_Prestamo
		fields=['material','cantidad']
		widgets={
		'material':forms.Select(attrs={
			'required':'true'
			})
		}
#-----------------------------------------------------------------------------------------------------

class dev_prestamoF(forms.ModelForm):
	fecha_prestamo=forms.DateField(disabled=True)
	estado=forms.ChoiceField(choices=([('Activo','Activo'),('Terminado','Terminado')]),disabled=True)
	aprendiz=forms.ModelChoiceField(Aprendiz.objects.all(),disabled=True)
	fecha_entrega=forms.DateField(disabled=True)

	class Meta:
		model=Prestamo
		fields='__all__'

class dev_DPrestamoF(forms.ModelForm):
	material=forms.ModelChoiceField(Material.objects.all(),disabled=True)
	estado_devolucion=forms.ChoiceField(widget=forms.Select(attrs={
		'class':'estado'
		}) ,choices=([('bueno','bueno'),('malo','malo')]))
	cantidad=forms.IntegerField()
	estado_elemento_prestamo=forms.ChoiceField(choices=([('En Prestamo','En Prestamo'),('Entregado','Entregado')]))
	tipo_daño=forms.ChoiceField(widget=forms.Select(attrs={
		'class':'tipo'
		}),label='Tipo de Daño', choices=([('Fisico','Fisico'),('Logico','Logico')]))



	class Meta:
		model=Detalle_Prestamo

		fields='__all__'
		widgets={
		'cantidad':forms.TextInput(attrs={
		'id':'contador'
		}),
		'fecha_devolucion' : forms.TextInput(attrs={
			'class':'datepicker'
		}),
		}
#-----------------------------------------------------------------------------------------
class det_prestamoF(forms.ModelForm):
	fecha_prestamo=forms.DateField(disabled=True)
	estado=forms.ChoiceField(choices=([('Activo','Activo'),('Terminado','Terminado')]),disabled=True)
	aprendiz=forms.ModelChoiceField(Aprendiz.objects.all(),disabled=True)
	fecha_entrega=forms.DateField(disabled=True)

	class Meta:
		model=Prestamo
		fields='__all__'

class det_DPrestamoF(forms.ModelForm):
	material=forms.ModelChoiceField(Material.objects.all(),disabled=True)
	estado_devolucion=forms.ChoiceField(choices=([('bueno','bueno'),('malo','malo')]))
	cantidad=forms.IntegerField(disabled=True)
	estado_elemento_prestamo=forms.ChoiceField(choices=([('En Prestamo','En Prestamo'),('Entregado','Entregado')]))
	tipo_daño=forms.ChoiceField(choices=([('Fisico','Fisico'),('Logico','Logico')]))



	class Meta:
		model=Detalle_Prestamo
		fields='__all__'

#formulario de la tabla categoria
class categoria_form(forms.ModelForm):
	class Meta:
		model = Categoria
		fields = '__all__'
		widgets = {
		'nombre' : forms.TextInput(attrs={
			'id':'nombre','class':'form-control','placeholder':'Nombre',
										'autofocus': 'autofocus'
			}),
		}

#formulario de la tabla bodega
class agregar_bodega_form(forms.ModelForm):
	class Meta:
		model= Bodega
		fields= '__all__'
		widgets = {
			'nombre': forms.TextInput(attrs={
				'id' : 'nombre','class':'form-control','placeholder':'Nombre',
										'autofocus': 'autofocus'
				}),
		}

#formulario de la tabla cuentadante
class cuentadante_form(forms.ModelForm):
	class Meta:
		model = Cuentadante
		fields = '__all__' 
		widgets = {
		'nombre' : forms.TextInput(attrs={
			'id':'nombre','class':'form-control','placeholder':'Nombre',
										'autofocus': 'autofocus'
			}),
		'identificacion' : forms.TextInput(attrs={
			'id' : 'identificacion','class':'form-control','placeholder':'Identificacion',
										'autofocus': 'autofocus','type':'number'
			}),
		}

#formulario de la tabla programa
class agregar_programas_form(forms.ModelForm):
	class Meta:
		model = Programa
		fields ='__all__'
		widgets = {
			'nombre' : forms.TextInput(attrs={
				'id' : 'nombre','class':'form-control','placeholder':'Nombre',
										'autofocus': 'autofocus'
				}),
		}

class ficha_form(forms.ModelForm):
	class Meta:
		model = Ficha
		fields = '__all__'
		widgets= {
			'numero_ficha' : forms.TextInput(attrs={
				'id' : 'ficha','class':'form-control','placeholder':'Numero de Ficha',
										'autofocus': 'autofocus','type':'number'
				}),
			'fecha_inicio' : forms.TextInput(attrs={
				'id':'fecha_inicio','class':'datepicker form-control','placeholder':'Fecha de Inicio',
										'autofocus': 'autofocus'
				}),
			'fecha_finalizacion' : forms.TextInput(attrs={
				'id':'fecha_finalizacion','class':'datepicker form-control','placeholder':'Fecha de Finalizacion',
										'autofocus': 'autofocus'
				}),
		}


#formulario de la tabla bodega_material
class Bodega_Material_form(forms.ModelForm):
	class Meta:
		model = Bodega_Material
		fields = ['bodega','fecha_ingresa']
		widgets= {
			'fecha_ingresa' : forms.TextInput(attrs={
				'class' : 'datepicker'
				}),
			'fecha_salida' : forms.TextInput(attrs={
				'class' : 'datepicker'
				}),

		}
		labels = {
		'bodega':'Ambiente'
		}
	def clean_fecha_ingresa(self):
		fecha_ingresa =self.cleaned_data['fecha_ingresa']
		fecha_actual = time.strftime("%Y-%m-%d")
		if str(fecha_actual)==str(fecha_ingresa):
			pass
		elif str(fecha_ingresa)>str(fecha_actual):
			raise forms.ValidationError('La Fecha de ingreso no debe ser mayor a la fecha actual')
		return fecha_ingresa
class editar_bodega_material_form(forms.ModelForm):
	class Meta:
		model = Bodega_Material
		fields = '__all__'
		widgets= {
			'fecha_ingresa' : forms.TextInput(attrs={
				'class' : 'datepicker'
				}),
			'fecha_salida' : forms.TextInput(attrs={
				'class' : 'datepicker'
				}),

		}
		labels = {
		'bodega':'Ambiente'
		}
	def clean_fecha_salida(self):
		fecha_ingresa =self.cleaned_data['fecha_ingresa']
		fecha_salida = self.cleaned_data['fecha_salida']
		fecha_actual = time.strftime("%Y-%m-%d")
		if str(fecha_ingresa)==str(fecha_salida):
			pass
		elif str(fecha_salida)<str(fecha_ingresa):
			raise forms.ValidationError('La Fecha de salida no debe ser menor a la fecha de ingreso')
		elif str(fecha_ingresa)>str(fecha_actual):
			raise forms.ValidationError('La Fecha de ingreso no debe ser mayor a la fecha actual')
		return fecha_salida

class agregar_aprendiz_form(forms.ModelForm):
	class Meta:
		model = Aprendiz
		fields = '__all__'
		widgets = {
			'nombre' : forms.TextInput(attrs={
			'id': 'nombre','class':'form-control','placeholder':'Nombre',
										'autofocus': 'autofocus'
				}),
			'apellido' : forms.TextInput(attrs={
			'id': 'apellido','class':'form-control','placeholder':'Apellido',
										'autofocus': 'autofocus'
				}),
			'identificacion' : forms.TextInput(attrs={
				'id' : 'identificacion','class':'form-control','placeholder':'Numero de identificacion',
										'autofocus': 'autofocus','type' : 'number'
				}),
			'tipo_documento' : forms.TextInput(attrs={
				'id' : 'tipo_documento','class':'form-control','placeholder':'Tipo de Documento',
										'autofocus': 'autofocus'
				}),
		}
