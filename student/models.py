from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    
    STATUS_CHOICES = [
        ("a", "Пришёл"),
        ("b", "Не пришёл"),
        ("c", "Не отмечен"),
    ]
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"
