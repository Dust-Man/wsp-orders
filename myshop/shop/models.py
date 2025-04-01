from django.db import models
from django.urls import reverse
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,
                            unique=True)
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])
    


class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    available = models.BooleanField(default=True)
    prefix = models.CharField(null=True, blank=True, max_length=10)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_by_weight = models.BooleanField(default=True)
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]
        verbose_name = 'producto'
        verbose_name_plural = 'productos'
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])
class StoreStatus(models.Model):
    """Modelo para gestionar el estado de apertura/cierre de la tienda."""
    is_open = models.BooleanField(default=True, verbose_name="Tienda abierta")
    closed_reason = models.CharField(max_length=255, blank=True, null=True, verbose_name="Motivo de cierre")
    manual_override = models.BooleanField(default=False, verbose_name="Cierre manual")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Última actualización")
    
    class Meta:
        verbose_name = "Estado de la tienda"
        verbose_name_plural = "Estado de la tienda"
    
    def __str__(self):
        return "Abierta" if self.is_open else "Cerrada"
        
    @classmethod
    def get_status(cls):
        """Obtiene o crea el único registro de estado de la tienda."""
        status, created = cls.objects.get_or_create(pk=1)
        return status
