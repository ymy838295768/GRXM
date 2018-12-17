import hashlib
from django.db import models


class UserModel(models.Model):
    u_name = models.CharField(max_length=16,unique=True)
    password = models.CharField(max_length=256)
    u_email = models.CharField(max_length=32)
    u_icon = models.ImageField(upload_to='static/upload/icons')
    is_delete = models.BooleanField(default=False)

    def generate_hash(self,u_password):
        sha = hashlib.sha512()
        sha.update(u_password.encode('utf-8'))
        return sha.hexdigest()

    def set_password(self,u_password):
        self.password = self.generate_hash(u_password)

    def check_password(self,u_password):
         return self.password == self.generate_hash(u_password)

    class Meta:
        db_table = 'second_usermodel'


class SecondRcommend(models.Model):
    title = models.CharField(max_length=256)
    wx_small_app_title = models.CharField(max_length=256)
    img = models.CharField(max_length=256)
    like_num = models.IntegerField(max_length=16)
    duration = models.CharField(max_length=16)
    request_url = models.CharField(max_length=256)

    class Meta:
        db_table = 'second_Recommend'


class SecondCollection(models.Model):
    moive_id = models.ForeignKey(SecondRcommend)
    user_id = models.ForeignKey(UserModel)

    class Meta:
        db_table = 'second_collection'


