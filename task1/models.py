from django.db import models

class Buyer(models.Model):
    name = models.CharField(max_length=100)  # CharField для имени
    balance = models.DecimalField(max_digits=10, decimal_places=2)  # DecimalField для баланса
    age = models.IntegerField()  # IntegerField для возраста

    def __str__(self):
        return self.name

class Game(models.Model):
    title = models.CharField(max_length=100)  # CharField для названия игры
    cost = models.DecimalField(max_digits=10, decimal_places=2)  # DecimalField для цены
    size = models.DecimalField(max_digits=10, decimal_places=2)  # DecimalField для размера файлов
    description = models.TextField()  # TextField для описания
    age_limited = models.BooleanField(default=False)  # BooleanField для ограничения возраста
    buyer = models.ManyToManyField(Buyer, related_name='games')  # ManyToManyField для связи с покупателями

    def __str__(self):
        return self.title