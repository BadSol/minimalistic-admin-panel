from __future__ import unicode_literals

from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Teacher(models.Model):
    person = models.OneToOneField(Person,
                                  on_delete=models.CASCADE,
                                  primary_key=True)

    def __str__(self):
        return self.person


class Class(models.Model):
    subject = models.CharField(max_length=60)
    description = models.CharField(max_length=400)
    teacher = models.ForeignKey(Teacher,
                                on_delete=models.CASCADE)

    def __str__(self):
        return "{} class".format(self.subject)
