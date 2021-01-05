from django.db import models

class ApiTbAccess(models.Model):
	access_id = models.AutoField(primary_key=True,verbose_name="Identificador de la llave de acceso")
	access_key = models.TextField(blank=True, null=True,verbose_name="Llave de acceso")
	access_description = models.TextField(blank=True, null=True,verbose_name="Descripción de la llave de acceso")

	class Meta:
		db_table = 'api_tb_access'
		verbose_name_plural = "Llaves de acceso"
		verbose_name = "Llave de acceso"

class ApiTbUsersRfc(models.Model):
	user_rfc_id = models.AutoField(primary_key=True,verbose_name="Identificador")
	user_rfc = models.TextField(blank=True, null=True,verbose_name="RFC")
	user_rfc_clave = models.TextField(blank=True, null=True, verbose_name="Clave secreta")
	user_rfc_location_cer = models.TextField(blank=True, null=True,verbose_name="URL del Certificado")
	user_rfc_location_key = models.TextField(blank=True, null=True, verbose_name="URL de la llave")

	class Meta:
		db_table = 'api_tb_users_rfc'
		verbose_name_plural = "RFC de usuarios"
		verbose_name = "RFC de usuario"