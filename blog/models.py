from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod, ReadDetail


class BlogType(models.Model):
	type_name = models.CharField(max_length=32)

	class Meta:
		db_table = 'tb_blogtype'

	def __str__(self):
		return self.type_name


class Blog(models.Model, ReadNumExpandMethod):
	title = models.CharField(max_length=64)
	blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)
	content = RichTextUploadingField()
	autor = models.ForeignKey(User, on_delete=models.CASCADE)
	read_details = GenericRelation(ReadDetail)
	created_time = models.DateTimeField(auto_now_add=True)
	last_updated_time = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'tb_blog'
		ordering = ['-created_time']

	def __str__(self):
		return self.title



