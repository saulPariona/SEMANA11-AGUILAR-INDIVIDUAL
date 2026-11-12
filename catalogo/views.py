from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import ProductoForm
from .models import Producto


def home(request):
    return render(request, "catalogo/home.html")


class CatalogoListView(ListView):
    model = Producto
    template_name = "catalogo/catalogo.html"
    context_object_name = "productos"

    def get_queryset(self):
        productos = Producto.objects.all()
        query = self.request.GET.get("q", "").strip()
        categoria = self.request.GET.get("categoria", "").strip()
        estado = self.request.GET.get("estado", "").strip()

        if query:
            productos = productos.filter(nombre__icontains=query) | productos.filter(
                sku__icontains=query
            )
        if categoria:
            productos = productos.filter(categoria=categoria)
        if estado == "activo":
            productos = productos.filter(disponible=True)
        elif estado == "inactivo":
            productos = productos.filter(disponible=False)
        if self.request.GET.get("stock_bajo") == "1":
            productos = productos.filter(stock__lte=3)
        return productos.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categorias"] = (
            Producto.objects.values_list("categoria", flat=True)
            .distinct()
            .order_by("categoria")
        )
        context["filtros"] = self.request.GET
        context["total_productos"] = Producto.objects.count()
        return context


class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = "catalogo/producto_form.html"
    success_url = reverse_lazy("catalogo:catalogo")


class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = "catalogo/producto_form.html"
    success_url = reverse_lazy("catalogo:catalogo")


class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = "catalogo/producto_confirm_delete.html"
    success_url = reverse_lazy("catalogo:catalogo")


def productos_api(request):
    productos = Producto.objects.all()
    data = [
        {
            "id": producto.id,
            "nombre": producto.nombre,
            "sku": producto.sku,
            "categoria": producto.categoria,
            "descripcion": producto.descripcion,
            "precio": str(producto.precio),
            "stock": producto.stock,
            "disponible": producto.disponible,
            "fecha_creacion": producto.fecha_creacion.isoformat(),
        }
        for producto in productos
    ]
    return JsonResponse({"total": len(data), "productos": data})
