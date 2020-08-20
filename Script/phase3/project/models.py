from django.db import models
from django.contrib.auth.models import User
class vers(models.Model):
    class Meta:
        ordering = ['username']
    username = models.CharField(max_length=60)
    vn = models.CharField(max_length=6)
    isv = models.CharField(max_length=1)
    #user = models.OneToOneField(User,on_delete=models.DO_NOTHING)

    def verify(self,number):
        if self.vn==number:
            isv=1
class Friendships(models.Model):
    user1 = models.CharField(max_length=100)
    user2 = models.CharField(max_length=100)
    isClose = models.IntegerField()
class FriendshipRequests(models.Model):
    toUser = models.CharField(max_length=100)
    fromUser = models.CharField(max_length=100)
class WatchersForAddings(models.Model):
    watcher = models.CharField(max_length=100)
    watched = models.CharField(max_length=100)
    mode = models.CharField(max_length=100)
class Item(models.Model):
    #adds id automatically item.id
    owner = models.CharField(max_length=120)
    type = models.CharField(max_length=30)
    title = models.CharField(max_length=200)
    uniqueid = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    year = models.IntegerField()
    location = models.CharField(max_length=100)
    rate = models.IntegerField()
    view = models.IntegerField()
    detail = models.IntegerField()
    borrow = models.IntegerField()
    comment = models.IntegerField()
    search = models.IntegerField()
class Comments(models.Model):
    #adds id automatically
    user_email = models.CharField(max_length=100)
    comment_text = models.CharField(max_length=250)
    #comment_date = models.DateTimeField()
    comment_date = models.CharField(max_length=100)
    item_id = models.IntegerField()
class ItemBorrows(models.Model):
    #adds id automatically
    item_id = models.IntegerField()
    user_email = models.CharField(max_length=100)
    return_date = models.CharField(max_length=100)
    taking_date = models.CharField(max_length=100)
    rate = models.IntegerField()
    is_returned = models.IntegerField()
class ItemRequests(models.Model):
    item_id = models.IntegerField()
    user_email = models.CharField(max_length=100)
    request_date = models.CharField(max_length=100)
class Notifications(models.Model):
    user_email = models.CharField(max_length=100)
    notification_text = models.CharField(max_length=200)
    notification_type = models.CharField(max_length=200)
class WatchItem(models.Model):
    user_email = models.CharField(max_length=100)
    item_id = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
class Announces(models.Model):
    item_id = models.CharField(max_length=100)
    toUser = models.CharField(max_length=200)
    msg = models.CharField(max_length=200)