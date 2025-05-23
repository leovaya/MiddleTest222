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

    def test_title_required(self):
        with self.assertRaises(ValidationError):
            image = Image(
                title="",
                image=self.get_sample_image_file(),
                age_limit=0,
            )
            image.full_clean()

    def test_image_required(self):
        with self.assertRaises(ValidationError):
            image = Image(
                title="Test without image",
                age_limit=0,
            )
            image.full_clean()

    def test_title_max_length(self):
        long_title = "A" * 201  # max is 200
        image = Image(
            title=long_title,
            image=self.get_sample_image_file(),
            age_limit=0,
        )
        with self.assertRaises(ValidationError):
            image.full_clean()

    def test_image_created_date_is_today(self):
        image = Image.objects.create(
            title="Date Test",
            image=self.get_sample_image_file(),
            age_limit=0,
        )
        self.assertEqual(image.created_date, date.today())

    def test_filter_images_by_created_date(self):
        # Створюємо зображення сьогодні
        image_today = Image.objects.create(
            title="Today Image",
            image=self.get_sample_image_file(),
            age_limit=0,
        )
        # Імітуємо зображення з вчорашньою датою
        image_yesterday = Image.objects.create(
            title="Yesterday Image",
            image=self.get_sample_image_file(),
            age_limit=0,
        )
        image_yesterday.created_date = date.today() - timedelta(days=1)
        image_yesterday.save()

        today_images = Image.objects.filter(created_date=date.today())
        self.assertIn(image_today, today_images)
        self.assertNotIn(image_yesterday, today_images)

    def test_age_limit_values(self):
        for age in [0, 12, 18, 21, 99]:
            with self.subTest(age=age):
                image = Image.objects.create(
                    title=f"Age {age}",
                    image=self.get_sample_image_file(),
                    age_limit=age,
                )
                self.assertEqual(image.age_limit, age)