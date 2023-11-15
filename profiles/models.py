import os
from PIL import Image

from django.utils.text import slugify
from django.conf import settings
from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from user.models import User

# RENOMBRA LA IMAGEN SUBIDA POR USUARIO Y LE PASA LA RUTA A LA CLASS
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    profile_pic_name = 'users/user_{0}/profile/{1}-profile.webp'.format(urlsafe_base64_encode(force_bytes(instance.user.id)), instance.user.username)
    
    full_path = os.path.join(settings.MEDIA_ROOT, profile_pic_name)

    if os.path.exists(full_path):
        os.remove(full_path)

    return profile_pic_name

class ProfileModel(models.Model):
    
    user = models.OneToOneField(User, default=None, primary_key=True, on_delete=models.CASCADE, related_name='profile')
    slug = models.SlugField(max_length=300)
    img = models.ImageField(upload_to=user_directory_path, blank=True, null=True, validators=[FileExtensionValidator(['jpg','png','webp','gif','jpeg'],'No valid format')])
    bio = models.TextField(max_length=500, blank=True, null=True)

    # TRANSFORMAR ARCHIVO DE IMAGEN A .WEBP
    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)

        if self.img:
            
            filename = "{0}.webp".format(self.img.path.split('.')[0])
            pic = Image.open(self.img.path).convert("RGB")
            
            alto = pic.height
            ancho = pic.width
            xcenter = pic.width/2 
            ycenter = pic.height/2

            if int(alto) > int(ancho):
                x1 = xcenter - xcenter
                y1 = ycenter - xcenter
                x2 = xcenter + xcenter
                y2 = ycenter + xcenter
                pic = pic.crop((x1, y1, x2, y2))

            if int(alto) < int(ancho):
                x1 = xcenter - ycenter
                y1 = ycenter - ycenter
                x2 = xcenter + ycenter
                y2 = ycenter + ycenter
                pic = pic.crop((x1, y1, x2, y2))

            pic = pic.resize((100, 100), Image.Resampling.LANCZOS)
            pic.save(filename, format='webp', quality='80')
   
    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'

    def __str__(self):
        return f'Profile: @{self.user.username}'