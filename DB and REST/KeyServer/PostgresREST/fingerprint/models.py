from django.db import models

class Fingerprint(models.Model):
    SPOCID = models.CharField(max_length=100)
    fingerprint = models.CharField(max_length=100)

    def __str__(self):
        return self.SPOCID

class AADHARSPOC(models.Model):
    SPOCID = models.CharField(max_length=100)
    passhash = models.CharField(max_length=100)

    def __str__(self):
        return self.SPOCID
