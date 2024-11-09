from django.db import models

# Create your models here.
class Task(models.Model):
    id = models.AutoField(primary_key=True)
    judul = models.CharField(max_length=100, blank=True, null=True)
    deskripsi = models.TextField(blank=True, null=True)
    deadline = models.DateField()
    STATUS_CHOICES = [
        ('selesai', 'Selesai'),
        ('belum_selesai', 'Belum Selesai'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='belum_selesai')
    PRIORITAS_CHOICES = [
        ('tinggi', 'Tinggi'),
        ('sedang', 'Sedang'),
        ('rendah', 'Rendah'),
    ]
    prioritas = models.CharField(max_length=20, choices=PRIORITAS_CHOICES, default='rendah')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'task'