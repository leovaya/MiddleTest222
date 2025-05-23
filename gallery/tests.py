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


class ImageModelTest(TestCase):

    def get_sample_image_file(self):
        return SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x89\x61',
            content_type='image/jpeg'
        )

    def get_sample_category(self, name="Категорія"):
        return Category.objects.create(name=name)

    def test_create_image_with_multiple_categories(self):
        image = Image.objects.create(
            title="Test Image",
            image=self.get_sample_image_file(),
            age_limit=0,
        )
        cat1 = self.get_sample_category("Тварини")
        cat2 = self.get_sample_category("Міста")
        image.categories.add(cat1, cat2)

        self.assertEqual(image.categories.count(), 2)
        self.assertIn(cat1, image.categories.all())
        self.assertIn(cat2, image.categories.all())
