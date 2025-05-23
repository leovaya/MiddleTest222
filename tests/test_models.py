import pytest
from datetime import date, timedelta
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from gallery.models import Category, Image

pytestmark = pytest.mark.django_db

@pytest.fixture
def sample_image_file():
    return SimpleUploadedFile(
        name='test_image.jpg',
        content=b'\x47\x49\x46\x38\x89\x61',
        content_type='image/jpeg'
    )


@pytest.fixture
def sample_category():
    return Category.objects.create(name="Категорія")


def test_create_category():
    category = Category.objects.create(name="Природа")
    assert category.name == "Природа"
    assert str(category) == "Природа"
    assert Category.objects.count() == 1


def test_create_image_with_multiple_categories(sample_image_file):
    image = Image.objects.create(
        title="Test Image",
        image=sample_image_file,
        age_limit=0,
    )
    cat1 = Category.objects.create(name="Тварини")
    cat2 = Category.objects.create(name="Міста")
    image.categories.add(cat1, cat2)

    assert image.categories.count() == 2
    assert cat1 in image.categories.all()
    assert cat2 in image.categories.all()


def test_title_required(sample_image_file):
    image = Image(
        title="",
        image=sample_image_file,
        age_limit=0,
    )
    with pytest.raises(ValidationError):
        image.full_clean()


def test_image_required():
    image = Image(
        title="Test without image",
        age_limit=0,
    )
    with pytest.raises(ValidationError):
        image.full_clean()


def test_title_max_length(sample_image_file):
    long_title = "A" * 201  # Max = 200
    image = Image(
        title=long_title,
        image=sample_image_file,
        age_limit=0,
    )
    with pytest.raises(ValidationError):
        image.full_clean()


def test_image_created_date_is_today(sample_image_file):
    image = Image.objects.create(
        title="Date Test",
        image=sample_image_file,
        age_limit=0,
    )
    assert image.created_date == date.today()


def test_filter_images_by_created_date(sample_image_file):
    image_today = Image.objects.create(
        title="Today Image",
        image=sample_image_file,
        age_limit=0,
    )
    image_yesterday = Image.objects.create(
        title="Yesterday Image",
        image=sample_image_file,
        age_limit=0,
    )
    image_yesterday.created_date = date.today() - timedelta(days=1)
    image_yesterday.save()

    today_images = Image.objects.filter(created_date=date.today())
    assert image_today in today_images
    assert image_yesterday not in today_images


@pytest.mark.parametrize("age", [0, 12, 18, 21, 99])
def test_age_limit_values(sample_image_file, age):
    image = Image.objects.create(
        title=f"Age {age}",
        image=sample_image_file,
        age_limit=age,
    )
    assert image.age_limit == age
