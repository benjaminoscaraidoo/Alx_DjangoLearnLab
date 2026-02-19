from django.db import models
from django.forms import CharField, IntegerField
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique= True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(blank= True, null= True, upload_to='profile_pics/')
    followers = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="following",
        blank=True
    )
    
    following = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="followers",
        blank=True
    )

    def __str__(self):
        return self.username
    
class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, related_name= 'following', on_delete= models.CASCADE)
    following = models.ForeignKey(CustomUser, related_name= 'followers', on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add= True)

    class Meta:
        unique_together = ('follower', 'following')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.follower} follows {self.following}"