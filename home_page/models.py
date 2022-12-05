from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
import uuid
import os


class Category(MPTTModel):
    name = models.CharField('Назва категорії', max_length=50)
    slug = models.SlugField('Слаг', max_length=50)
    is_visible = models.BooleanField('Відображати', default=False)
    parent = TreeForeignKey('self',
                            on_delete=models.CASCADE,
                            null=True,
                            blank=True,
                            related_name='children'
                            )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категорія меню'
        verbose_name_plural = 'Категорії меню'
        ordering = ['name']


class Offers(models.Model):
    name = models.CharField('Назва пропозиції', max_length=50)
    slug = models.SlugField('Слаг', max_length=50)
    is_visible = models.BooleanField('Відображати', default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Спеціальна пропозиція'
        verbose_name_plural = 'Спеціальні пропозиції'


class Product(models.Model):

    def get_file_name(self, file_name: str):
        ext = file_name.strip().split()[-1]
        f'{uuid.uuid4()}.{ext}'
        return os.path.join('images/products', f'{uuid.uuid4()}.{ext}')

    title = models.CharField('Назва товару', max_length=100, unique=True, db_index=True)
    price = models.DecimalField('Ціна', max_digits=8, decimal_places=2)
    desc = models.TextField('Опис товару', max_length=500, blank=True)
    is_sale = models.BooleanField('Знижка', default=False)
    discount = models.DecimalField('Розмір знижки', max_digits=8, decimal_places=2)
    offer = models.ForeignKey(Offers, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    photo = models.ImageField('Завантажити фото', upload_to=get_file_name)




