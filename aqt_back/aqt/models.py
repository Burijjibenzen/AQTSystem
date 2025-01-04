from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class Location(models.Model):
    LocationID = models.AutoField(primary_key=True, null=False)
    LocationName = models.CharField(max_length=200, unique=True, null=False)
    Longitude = models.DecimalField(max_digits=10, decimal_places=6, null=False)
    Latitude = models.DecimalField(max_digits=10, decimal_places=6, null=False)

class Station(models.Model):
    StationID = models.AutoField(primary_key=True, null=False)
    StationName = models.CharField(max_length=200, unique=True, null=False)
    LocationID = models.ForeignKey(Location, on_delete=models.CASCADE, null=False)
    isValid = models.BooleanField(null=False)

class Indicator(models.Model):
    IndicatorID = models.AutoField(primary_key=True, null=False)
    IndicatorName = models.CharField(max_length=200, unique=True, null=False)
    Unit = models.CharField(max_length=50, null=False)

class Data(models.Model):
    DataID = models.AutoField(primary_key=True, null=False)
    StationID = models.ForeignKey(Station, on_delete=models.CASCADE, null=False)
    IndicatorID = models.ForeignKey(Indicator, on_delete=models.CASCADE, null=False)
    DataTime = models.DateTimeField(null=False)
    Value = models.DecimalField(max_digits=10, decimal_places=3, null=False)

class Analysis(models.Model):
    AnalysisID = models.AutoField(primary_key=True, null=False)
    StationID = models.ForeignKey(Station, on_delete=models.CASCADE, null=False)
    ContaminationLevel = models.CharField(max_length=5, null=False)
    AnalysisTime = models.DateTimeField(null=False)
    AQI = models.DecimalField(max_digits=6, decimal_places=3, null=False)
    Advice = models.TextField()

class Role(models.Model):
    RoleID = models.IntegerField(primary_key=True, null=False)
    RoleName = models.CharField(max_length=200, unique=True, null=False)
    Description = models.TextField()

class User(models.Model):
    UserID = models.IntegerField(primary_key=True, null=False)
    RoleID = models.ForeignKey(Role, on_delete=models.CASCADE, null=False, default=1)
    UserName = models.CharField(max_length=200, unique=True, null=False)
    Password = models.CharField(max_length=200, null=False)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

class Record(models.Model):
    RecordID = models.AutoField(primary_key=True, null=False)
    DataID = models.ForeignKey(Data, on_delete=models.CASCADE, null=False)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    RecordTime = models.DateTimeField(null=False)

class Advice(models.Model):
    AdviceID = models.AutoField(primary_key=True, null=False)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    Content = models.TextField()
    AdviceTime = models.DateTimeField(null=False)