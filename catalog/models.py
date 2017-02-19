from __future__ import unicode_literals

from django.db import models

from django.utils.safestring import mark_safe
from django.conf import settings

# Create your models here.





class Brand(models.Model):
	name = models.CharField(max_length=200)

	def __unicode__(self):
		return unicode(self.name)


class Category(models.Model):
	name = models.CharField(max_length=200)

	def __unicode__(self):
		return unicode(self.name)


class Catalog(models.Model):
	brand = models.ForeignKey(Brand)
	category = models.ForeignKey(Category)
	item_name = models.CharField(blank=True, max_length=300)
	item_description = models.CharField(blank=True, max_length=300)
	max_retail_price = models.FloatField(blank=True, default=0)
	client_price = models.FloatField(blank=True, default =0)
	photo = models.ImageField(upload_to='images')

	def image_tag(self):
		return mark_safe('<img src="%s%s" width="150" height="150" />' % (settings.MEDIA_URL,self.photo))

	image_tag.short_description = 'Image'



	




	
