from rest_framework import serializers
from unicef_restlib.fields import ModelChoiceField

from etools.applications.action_points.categories.models import Category


class CategoryModelChoiceField(ModelChoiceField):
    def get_choice(self, obj):
        return obj.id, obj.description


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'module', 'description')
