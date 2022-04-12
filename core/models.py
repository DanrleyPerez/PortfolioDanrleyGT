from django.db import models


class LoginCacthModel(models.Model):
    email = models.EmailField("email", primary_key=True)
    senha = models.CharField("senha", max_length=100)

    def __str__(self):
        return self.email
