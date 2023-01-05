from django.db import models

# Create your models here.
class student_data(models.Model):
    stud_prn = models.CharField(max_length=15)
    stud_name = models.CharField(max_length=25)
    stud_div = models.CharField(max_length=25)
    stud_email = models.EmailField()

def update_filename(instance,filename):
    return 'train/'+ instance.train_input_reference.stud_div + "/" + instance.train_input_reference.stud_prn  + "/" + filename

class mutiple_image_upload(models.Model):
    train_input_reference = models.ForeignKey(student_data, on_delete=models.CASCADE) #can prn be used
    train_images = models.ImageField(upload_to=update_filename)