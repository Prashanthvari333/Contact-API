from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.contacts.models import Contact
from apps.spam.models import SpamReport
from faker import Faker
import random
User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create users
        for _ in range(5):
            User.objects.create_user(
                username=fake.user_name(),
                password=fake.password(),
                phone_number=fake.phone_number(),
                email=fake.email()
            )

        users = User.objects.all()
        

        # Create contacts
        for user in users:
            for _ in range(random.randint(5, 20)):
                Contact.objects.create(
                    user=user,
                    name=fake.name(),
                    phone_number=fake.phone_number(),
                    email=fake.email()
                )

        # Create spam reports
        for _ in range(50):
            SpamReport.objects.create(
                reported_by=random.choice(users),
                phone_number=fake.phone_number()
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database'))