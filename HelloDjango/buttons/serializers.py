from rest_framework import serializers
from .models import Button, Language, SubButton, X



class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = '__all__'


class ButtonSerializer(serializers.ModelSerializer):
    subs = serializers.HyperlinkedIdentityField(
        view_name='subs_buttons',
        format='html',
        lookup_url_kwarg='button_id',
    )

    class Meta:
        model = Button
        fields = [
            'id', 'name', 'type', 'text', 'colored_text',
            'subs']


class SubButtonSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubButton
        fields = '__all__'

class XSerializer(serializers.ModelSerializer):
    class Meta:
        model = X
        fields = '__all__'
