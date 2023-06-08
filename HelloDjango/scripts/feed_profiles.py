from buttons.models import Profile
from faker import Faker
import random as r


ru_faker = Faker('ru-RU')

def set_random_data_to_profiles():
    for profile in Profile.objects.all():
        profile.first_name = ru_faker.first_name()
        profile.last_name = ru_faker.last_name()
        profile.age = r.randint(13, 120)
        profile.sex = r.choice(Profile.SEX_CHOICE)[0]
        profile.save()


set_random_data_to_profiles()