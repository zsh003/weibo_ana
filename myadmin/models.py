from django.db import models
from datetime import datetime
# Create your models here.




class User(models.Model):
    username=models.CharField(max_length=50)
    nickname=models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    password_hash=models.CharField(max_length=100) # 密码
    password_salt=models.CharField(max_length=50) # 密码干扰值
    keyword=models.CharField(max_length=255) # 密码干扰值
    Threshold=models.IntegerField(max_length=11) #
    status=models.IntegerField(default=1)  # 1正常2禁用 6管理员 9删除
    create_at=models.DateTimeField(default=datetime.now)
    update_at=models.DateTimeField(default=datetime.now)

    def toDict(self):
        return {
            'id':self.id,
            'username':self.username,
            'nickname':self.nickname,
            'phone':self.phone,
            'password_hash':self.password_hash,
            'password_salt':self.password_salt,'status':self.status,
            'create_at':self.create_at.strftime('%Y-%m-%d %H:%M:%S'),
            'update_at':self.update_at.strftime('%Y-%m-%d %H:%M:%S')}
    class Meta:
        db_table='user'

class search_history(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.IntegerField(max_length=10)
    seaHistory = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    def toDict(self):
        return {
            'id': self.id,
            'uid': self.uid,
            'seaHistory': self.seaHistory,
            'created_at': self.created_at
        }
    class Meta:
        db_table='search_history'

class Search(models.Model):
    id = models.AutoField(primary_key=True)
    wid = models.CharField(max_length=255)
    uid = models.CharField(max_length=255)
    screen_name = models.CharField(max_length=255)
    reposts_count = models.CharField(max_length=255)
    comments_count = models.CharField(max_length=255)
    attitudes_count = models.CharField(max_length=255)
    status_city = models.CharField(max_length=255)
    status_province = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.CharField(max_length=255)
    keyword = models.CharField(max_length=255)
    def toDict(self):
        return {
            'id':self.id,
            'wid':self.wid,
            'uid':self.uid,
            'screen_name':self.screen_name,
            'reposts_count':self.reposts_count,
            'comments_count':self.comments_count,
            'attitudes_count':self.attitudes_count,
            'status_city':self.status_city,
            'status_province':self.status_province,
            'text':self.text,
            'created_at':self.created_at,
            'keyword':self.keyword,
        }
    class Meta:
        db_table='search'



class Comment(models.Model):
    wid = models.CharField(max_length=255)
    uid = models.CharField(max_length=255)
    screen_name = models.CharField(max_length=255)
    comment = models.TextField()
    source = models.CharField(max_length=255)
    like_count = models.IntegerField(max_length=11)
    created_at = models.DateTimeField()
    keyword = models.CharField(max_length=255)
    def toDict(self):
        return {
            'id':self.id,
            'wid':self.wid,
            'uid':self.uid,
            'screen_name':self.screen_name,
            'comment':self.comment,
            'source':self.source,
            'like_count':self.like_count,
            'created_at':self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'keyword':self.keyword
        }
    class Meta:
        db_table='comment'

