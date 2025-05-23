from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from gallery.models import Category, Image
from datetime import date, timedelta


class CategoryModelTest(TestCase):

    def test_create_category(self):
        category = Category.objects.create(name="Природа")
        self.assertEqual(category.name, "Природа")
        self.assertEqual(str(category), "Природа")
        self.assertEqual(Category.objects.count(), 1)