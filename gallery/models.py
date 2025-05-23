
from django.db import models

# Модель для категорій зображень
class Category(models.Model):
    # Назва категорії (наприклад: "Природа", "Міста", "Тварини")
    name = models.CharField(max_length=100)

    # Метод для зручного відображення об'єкта категорії як рядка
    def __str__(self):
        return self.name
    
# Модель для зображень
class Image(models.Model):
    # Назва зображення
    title = models.CharField(max_length=200)

    # Поле для зберігання файлу зображення
    image = models.ImageField(upload_to='images/')
    categories = models.ManyToManyField(Category, related_name='images')
    created_date = models.DateField(auto_now_add=True)
    age_limit = models.PositiveIntegerField() # Вікове обмеження (наприклад: 0, 12, 18 тощо)

    def __str__(self):
        return self.title