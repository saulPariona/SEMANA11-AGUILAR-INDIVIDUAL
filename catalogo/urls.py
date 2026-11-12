from django.urls import path

from .views import (
    CatalogoListView,
    ProductoCreateView,
    ProductoDeleteView,
    ProductoUpdateView,
    home,
    productos_api,
)

app_name = "catalogo"

urlpatterns = [
    path("", home, name="home"),
    path("catalogo/", CatalogoListView.as_view(), name="catalogo"),
    path("productos/nuevo/", ProductoCreateView.as_view(), name="producto-nuevo"),
    path(
        "productos/<int:pk>/editar/",
        ProductoUpdateView.as_view(),
        name="producto-editar",
    ),
    path(
        "productos/<int:pk>/eliminar/",
        ProductoDeleteView.as_view(),
        name="producto-eliminar",
    ),
    path("api/productos", productos_api),
    path("api/productos/", productos_api, name="productos-api"),
]
