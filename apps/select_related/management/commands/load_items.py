import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.models import Q

from apps.select_related.models import Publisher, Store, Book
from apps.select_related.tests.factories import UserFactory


User = get_user_model()

class Command(BaseCommand):
    """
    This command is for inserting Publisher, Book, Store into database.
    Insert 5 Publishers, 100 Books, 10 Stores.
    """

    def handle(self, *args, **options):
        User.objects.filter(~Q(is_superuser=True) | ~Q(is_staff=True)).delete()
        Publisher.objects.all().delete()
        Book.objects.all().delete()
        Store.objects.all().delete()

        # create 10 publishers
        publishers = [Publisher(name=f"Publisher{index}") for index in range(1, 11)]
        Publisher.objects.bulk_create(publishers)

        # create 100 books and assign 10 books for each publisher
        books = []
        counter = 0
        for publisher in Publisher.objects.all():
            for i in range(10):
                counter = counter + 1
                books.append(Book(name=f"Book{counter}", price=random.randint(50, 300), publisher=publisher))
        Book.objects.bulk_create(books)

        # create 10 stores and insert 10 books in each store
        books = list(Book.objects.all())
        for i in range(10):
            temp_books = [books.pop(0) for i in range(10)]
            store = Store.objects.create(name=f"Store{i+1}")
            store.books.set(temp_books)
            store.save()