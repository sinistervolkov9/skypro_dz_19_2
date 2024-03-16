import json
from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='The JSON file to load data from')

    def handle(self, *args, **options):
        # Удаление всех продуктов и категорий
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Чтение данных из JSON файла
        with open(options['json_file'], 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Создание категорий
        categories_data = data['categories']
        category_for_create = [Category(**category) for category in categories_data]
        Category.objects.bulk_create(category_for_create)

        # Создание продуктов
        products_data = data['products']
        product_for_create = []
        for product_data in products_data:
            category = Category.objects.get(pk=product_data['category_id'])
            product_for_create.append(Product(category=category, **product_data))
        Product.objects.bulk_create(product_for_create)

        self.stdout.write(self.style.SUCCESS('Successfully loaded data into the database'))
