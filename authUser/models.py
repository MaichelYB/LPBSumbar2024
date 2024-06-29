from django.db import models

# Create your models here.
class UserProfile(models.Model):
    user_id = models.BigIntegerField(null=False)
    birth_date = models.DateField(max_length="100")
    class Meta:
        db_table = 'user_profile'