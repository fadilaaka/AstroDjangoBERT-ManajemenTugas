from django.urls import path

from tugas import views


urlpatterns = [
    path('api/tugas/', views.index, name='index'),  # Menetapkan view 'index' untuk URL root
    path('api/tambah/', views.tambah, name='tambah'),
    path('api/editdata/<int:id>/', views.edit, name='edit'),
    path('api/hapusdata/<int:id>/', views.hapus, name='hapus'),
]
