from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    nascimento = models.DateField(null=True, blank=True)
    foto = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)

    def __str__(self):
        return self.user.username

    @property
    def idade(self):
        from datetime import date
        if self.nascimento:
            hoje = date.today()
            return hoje.year - self.nascimento.year - (
                (hoje.month, hoje.day) < (self.nascimento.month, self.nascimento.day)
            )
        return None