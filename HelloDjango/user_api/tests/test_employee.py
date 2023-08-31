from django.test import TestCase
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from user_api.models import Profile, Employee, Position
from faker import Faker

