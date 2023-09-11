from store.models import BannerAdd
from django.test import TestCase
from _helptools import create_banner


class BannerAddManagerTest(TestCase):

    def setUp(self) -> None:
        self.create_banners()

    def create_banners(self):
        for _ in range(3):
            add = create_banner()
        add.is_public = False
        add.save()

    def test_get_all(self):
        qs = BannerAdd.objects.all()
        self.assertEqual(len(qs), 3)

    def test_public(self):
        qs = BannerAdd.public.all()
        self.assertEqual(len(qs), 2)
