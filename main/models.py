from django.db import models


class Car(models.Model):
    name = models.CharField(max_length=200, verbose_name="Mashina nomi")
    image_url = models.URLField(max_length=500, verbose_name="Rasm URL")
    price = models.CharField(max_length=100, verbose_name="Narxi (so'm)")
    discount_text = models.CharField(max_length=200, blank=True, verbose_name="Chegirma matni")
    has_discount = models.BooleanField(default=False, verbose_name="Chegirmada")
    engine = models.CharField(max_length=100, blank=True, verbose_name="Dvigatel")
    power = models.CharField(max_length=100, blank=True, verbose_name="Quvvat")
    transmission = models.CharField(max_length=100, blank=True, verbose_name="Uzatma")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Mashina"
        verbose_name_plural = "Mashinalar"
        ordering = ['-created_at']


class HighlightCar(models.Model):
    """Yangiliklar (highlight) bo'limidagi mashinalar"""
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name="Mashina")
    tab_title = models.CharField(max_length=100, verbose_name="Tab nomi")
    description = models.TextField(verbose_name="Tavsif")
    order = models.IntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    def __str__(self):
        return f"{self.tab_title} - {self.car.name}"

    class Meta:
        verbose_name = "Yangilik mashina"
        verbose_name_plural = "Yangilik mashinalar"
        ordering = ['order']
