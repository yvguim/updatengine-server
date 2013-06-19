###################################################################################
# UpdatEngine - Software Packages Deployment and Administration tool              #
#                                                                                 #
# Copyright (C) Yves Guimard - yves.guimard@gmail.com                             #
#                                                                                 #
# This program is free software; you can redistribute it and/or                   #
# modify it under the terms of the GNU General Public License                     #
# as published by the Free Software Foundation; either version 2                  #
# of the License, or (at your option) any later version.                          #
#                                                                                 #
# This program is distributed in the hope that it will be useful,                 #
# but WITHOUT ANY WARRANTY; without even the implied warranty of                  #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                   #
# GNU General Public License for more details.                                    #
#                                                                                 #
# You should have received a copy of the GNU General Public License               #
# along with this program; if not, write to the Free Software                     #
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA. #
###################################################################################

from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, pre_delete
from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from inventory.models import machine
import hashlib
import os, string, random, shutil

def random_directory(size=8, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

class packagecondition(models.Model):
	choice = (
			('installed', _('installed')),
			('notinstalled',_('notinstalled')),
			('is_W64_bits',_('is_W64_bits')),
			('is_W32_bits',_('is_W32_bits')),
			('lower',_('lower')),
			('higher',_('higher'))
		)
	name = models.CharField(max_length=100, unique=True, verbose_name = _('packagecondition|name'))
	#description = models.CharField(max_length=500, verbose_name = _('packagecondition|description'))
	depends = models.CharField(max_length=12, choices=choice, default='installed', verbose_name = _('packagecondition|depends'))
	softwarename = models.CharField(max_length=100, null= True, blank=True, default="undefined", verbose_name = _('packagecondition|softwarename'), help_text= _('packagecondition|softwarename help text'))
	softwareversion = models.CharField(max_length=500, null= True, blank=True, default="undefined", verbose_name = _('packagecondition|softwareversion'), help_text= _('packagecondition|softwareversion help text'))

	class Meta:
		verbose_name = _('packagecondition|package condition')
		verbose_name_plural = _('packagecondition|packages conditions')

	def __unicode__(self):
		return self.name

class package(models.Model):
	choice = (
			('yes', _('package|yes')),
			('no', _('package|no'))
		)
	name = models.CharField(max_length=100, unique=True, verbose_name = _('package|name'))
	description = models.CharField(max_length=500, verbose_name = _('package|description'))
	conditions = models.ManyToManyField('packagecondition',null = True, blank = True, verbose_name = _('package|conditions'))
	command = models.TextField(max_length=1000, verbose_name = _('package|command'), help_text= _('package|command help text'))
	packagesum = models.CharField(max_length=40, null= True, blank=True, verbose_name = _('package|packagesum'))
	filename  = models.FileField(upload_to="package-file/"+random_directory()+'/', null=True, blank=True, verbose_name = _('package|filename'))
	ignoreperiod = models.CharField(max_length=3, choices=choice, default='no', verbose_name = _('package|ignore deploy period'))
	public = models.CharField(max_length=3, choices=choice, default='no', verbose_name = _('package| public package'))
	class Meta:
		verbose_name = _('package|deployment package')
		verbose_name_plural = _('package|deployment packages')

	def save(self, *args, **kwargs):
		# delete old file when replacing by updating the file
		try :
			p = package.objects.get(id=self.id)
			if p.filename != self.filename:
				if os.path.split(os.path.dirname(p.filename.path))[1] == 'package-file':
					if p.filename != '':
						p.filename.delete(save=False)
				else:
					shutil.rmtree(os.path.dirname(p.filename.path))

		except :
			pass # when new file then we do nothing, normal case
		super(package, self).save(*args, **kwargs)

	def md5_for_file(self,block_size=2**20):
		if self.filename == '':
			return "nofile"
		f = open(self.filename.path, 'r')
		md5 = hashlib.md5()
		while True:
			data = str(f.read(block_size))
			if not data:
				break
			md5.update(data)
		return str(md5.hexdigest())

	def __unicode__(self):
		return self.name

# Add a post_save function to update packagesum after each save on
# a package object
@receiver(post_save, sender=package)
def postcreate_package(sender, instance, created, **kwargs):
	# Update of packagesum field
	if instance.filename == None:
		instance.packagesum = 'nofile'
	else:
			instance.packagesum = instance.md5_for_file()
	# Update of all package history wish are programmed
	for ph in packagehistory.objects.filter(package = instance, status = 'Programmed'):
                ph.name = instance.name
		ph.description = instance.description
		ph.command = instance.command
		ph.packagesum = instance.packagesum
		if instance.packagesum != 'nofile':
			ph.filename = instance.filename.path
	        else:
		        ph.filename = ''
		ph.save()

	post_save.disconnect(receiver=postcreate_package, sender=package)
	instance.save()
	post_save.connect(receiver=postcreate_package, sender=package)


@receiver(pre_delete, sender=package)
def predelete_package(sender, instance, **kwargs):
	if instance.filename.name !='':
		if os.path.split(os.path.dirname(instance.filename.path))[1] == 'package-file':
			instance.filename.delete(save=False)
		else:
			shutil.rmtree(os.path.dirname(instance.filename.path))

# call packages_changed only when packages m2m changed
@receiver(m2m_changed, sender=machine.packages.through)
def packages_changed(sender, instance, **kwargs):
	# Create and update packagehistory object
	allpackages = instance.packages.all()
	for package in allpackages :
		obj, created = packagehistory.objects.get_or_create(machine=instance, package=package)
		obj.name = package.name
		obj.description = package.description
		obj.command = package.command
		obj.packagesum = package.packagesum
		if package.packagesum != 'nofile':
			obj.filename = package.filename.path
		obj.save()
	# delete packagehistory object if just programmed and deleted from machine
	for package in packagehistory.objects.filter(machine=instance,status='Programmed'):

		if not machine.objects.filter(packages__in=allpackages).exists():
			package.delete()


class packagehistory(models.Model):
	name = models.CharField(max_length=100,null= True, blank= True, verbose_name = _('packagehistory|name'))
	description = models.CharField(max_length=500,null= True, blank= True, verbose_name = _('packagehistory|description'))
	command = models.TextField(max_length=1000,null= True, blank= True, verbose_name = _('packagehistory|command'))
	packagesum = models.CharField(max_length=40, null= True, blank=True, verbose_name = _('packagehistory|packagesum'))
	filename  = models.CharField(max_length=500, null=True, blank=True, verbose_name = _('packagehistory|filename'))
	machine = models.ForeignKey(machine, verbose_name = _('packagehistory|machine'))
	package = models.ForeignKey(package, null=True, blank=True, on_delete=models.SET_NULL, verbose_name = _('packagehistory|package'))
	status = models.CharField(max_length=500, default = 'Programmed', null=True, blank = True, verbose_name = _('packagehistory|status'))
	date = models.DateTimeField(auto_now=True, verbose_name = _('packagehistory|date'))

	class Meta:
		verbose_name = _('packagehistory|package history')
		verbose_name_plural = _('packagehistory|packages history')


	def __unicode__(self):
		return self.name

class packageprofile(models.Model):
	name = models.CharField(max_length=100, unique=True, verbose_name = _('packageprofile|name'))
	description = models.CharField(max_length=500, verbose_name = _('packageprofile|description'))
	packages = models.ManyToManyField('package',null = True, blank = True, verbose_name = _('packageprofile|packages'))

	class Meta:
		verbose_name = _('packageprofile|package profile')
		verbose_name_plural = _('packageprofile|packages profiles')

	def __unicode__(self):
		return self.name

class packagewakeonlan(models.Model):
	choice = (
			('Programmed', _('packagewakeonlan|Programmed')),
			('Completed', _('packagewakeonlan|Completed'))
		)
	name = models.CharField(max_length=100, unique=True, verbose_name = _('packagewakeonlan|name'), help_text= _('packagewakeonlan|packagewakeonlan help text'))
	description = models.CharField(max_length=500, verbose_name = _('packagewakeonlan|description'))
	machines = models.ManyToManyField('inventory.machine',null = True, blank = True, verbose_name = _('packagewakeonlan|machines to start'))
	date = models.DateTimeField(verbose_name = _('packagewakeonlan|start_time'))
	status = models.CharField(max_length=100, choices=choice, default='Programmed', verbose_name = _('packagewakeonlan|status'))

	class Meta:
		verbose_name = _('packagewakeonlan|package wakeonlan')
		verbose_name_plural = _('packagewakeonlan|packages wakeonlan')

	def __unicode__(self):
		return self.name




class timeprofile(models.Model):
	name = models.CharField(max_length=100, unique=True, verbose_name = _('timeprofile|name') , help_text= _('timeprofile|timeprofile help text'))
	description = models.CharField(max_length=500,null= True, blank= True, verbose_name = _('timeprofile|description'))
	start_time = models.TimeField(verbose_name = _('timeprofile|start_time'))
	end_time = models.TimeField(verbose_name = _('timeprofile|end_time'))

	class Meta:
		verbose_name = _('timeprofile|time profile')
		verbose_name_plural = _('timeprofile|time profiles')

	def __unicode__(self):
		return self.name
