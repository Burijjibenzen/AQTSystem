from rest_framework import serializers
from .models import User, Advice, Data, Record, Analysis

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['UserID', 'UserName', 'Password']

class AdviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advice
        fields = ['AdviceID', 'UserID', 'Content', 'AdviceTime']

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ['DataID', 'StationID', 'IndicatorID', 'DataTime', 'Value']

class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ['UserID', 'DataID', 'RecordTime']