from django.db import models
from django.utils import timezone

# Create your models here.
class District(models.Model):
    title = models.CharField(max_length=255, null=False, db_index=True)
    class Meta:
        db_table = 'realty_district'
    def __str__(self):
        return "%s" % (self.title)


class Street(models.Model):
    title = models.CharField(max_length=255, null=False, db_index=True)
    class Meta:
        db_table = 'realty_street'
    def __str__(self):
        return "%s" % (self.title)


class TypeObject(models.Model):
    title = models.CharField(max_length=255, null=False, db_index=True)
    class Meta:
        db_table = 'realty_type_object'
    def __str__(self):
        return "%s" % (self.title)


class Object(models.Model):
    type = models.ForeignKey(TypeObject, null=False, on_delete=models.CASCADE)
    district = models.ForeignKey(District, null=False, on_delete=models.CASCADE)
    street = models.ForeignKey(Street, null=False, on_delete=models.CASCADE)
    building = models.CharField(max_length=10, null=True)
    apartment = models.CharField(max_length=10, null=True)
    apart_area = models.IntegerField(null=True)
    land_area = models.IntegerField(null=True)
    rooms = models.IntegerField(null=True)
    floor = models.IntegerField(null=True)
    floors = models.IntegerField(null=True)
    description = models.TextField(null=True)
    class Meta:
        db_table = 'realty_object'
        index_together = ('district', 'street', 'building')

    def address(self):
        addr = self.street.title
        if self.building:
            addr = addr + " " + self.building
            if self.apartment:
                addr = addr + ", кв. " + self.apartment
        return addr

class Owner(models.Model):
    fio = models.CharField(max_length=255, null=False)
    phone = models.CharField(max_length=16, null=True)
    class Meta:
        db_table = 'realty_owner'


class Advert(models.Model):
    owner = models.ForeignKey(Owner, null=False, on_delete=models.CASCADE)
    object = models.ForeignKey(Object, null=False, on_delete=models.CASCADE)
    price = models.FloatField(null=True)
    create_time = models.DateTimeField(null=False, default=timezone.now)
    class Meta:
        db_table = 'realty_advert'
