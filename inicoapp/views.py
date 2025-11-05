from itertools import product

from django.shortcuts import render, redirect, get_object_or_404
from inicoapp.models import Documentos
from django.contrib import messages

#create your views here

def home(request):
    return render(request,"plantilla.html")

def consultor(request):
    documentos = Documentos.objects.filter(visible=True).order_by('-creado')
    return render(request,"consultor.html",
                  {
                     'documentos': documentos
                        }
                  )
def gestor(request):
    documentos = Documentos.objects.all().order_by('-creado')
    return render(request,"gestor.html", {
        'documentos': documentos
    })

def guardar(request):
    descripcion = request.POST["descripcion"]
    archivo_pdf = request.FILES["archivo_pdf"]
    visible = 'visible' in request.POST
    d = Documentos(descripcion=descripcion, archivo_pdf=archivo_pdf, visible=visible)
    d.save()
    messages.success(request, "Guardado exitosamente")
    return redirect('gestor')


def eliminar(request, id):
    try:
        documento = get_object_or_404(Documentos, pk=id)
        documento.archivo_pdf.delete(save=False)
        documento.delete()
        messages.success(request, "Eliminado exitosamente")
    except Exception as e:
        messages.error(request, f"Ocurrió un error al eliminar: {e}")
    return redirect('gestor')

def detalle(request, id):
    documento = get_object_or_404(Documentos, pk=id)
    return render(request, "archivoEditar.html", {
        'documento': documento
    })


def editar(request, id):

    if request.method == 'POST':
        try:
            documento = get_object_or_404(Documentos, pk=id)
            documento.descripcion = request.POST["descripcion"]
            documento.visible = 'visible' in request.POST

            if 'archivo_pdf' in request.FILES:
                documento.archivo_pdf.delete(save=False)
                documento.archivo_pdf = request.FILES["archivo_pdf"]
            documento.save()
            messages.success(request, "Actualizado exitosamente")
        except Exception as e:
            messages.error(request, f"Ocurrió un error al actualizar: {e}")

        return redirect('gestor')
    else:
        return redirect('gestor')
