from rest_framework import serializers
from .models import Button, Language, SubButton



class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = '__all__'


class ButtonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Button
        fields = '__all__'


class SubButtonSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubButton
        fields = '__all__'