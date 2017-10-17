from django.db import models
from django.contrib.auth.models import AbstractUser

#创建model User继承自django自带类 AbstractUser，添加两个字段name和wechat，AbstractUser默认有first_name，last_name等多个字段
#https://docs.djangoproject.com/en/1.11/topics/auth/customizing/
class User(AbstractUser):
    name = models.CharField(max_length=32, help_text="这是一个名字")
    wechat = models.CharField(max_length=128)

#当你用print打印输出的时候，Python会调用它的str方法，这里重写__str__方法
    def __str__(self):
        return "%s <%s>" % (self.username, self.name)
