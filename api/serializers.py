from business.models import Business
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class BusinessConfirmationSerializer(serializers.ModelSerializer):
    pass