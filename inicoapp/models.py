from django.db import models

# Create your models here.

class Documentos(models.Model):

    descripcion = models.CharField(max_length=300)
    archivo_pdf = models.FileField(upload_to="pdf/")
    visible = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'documentos'