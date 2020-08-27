from django.db import models

# Create your models here.
class Blog(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=100)
    content=models.TextField()
    image=models.ImageField(upload_to='blog/',default="")
    timestamp=models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return self.title