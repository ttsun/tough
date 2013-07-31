from django.db import models
from noah.models import *
from usermanage.models import *

class BlockType(models.Model):
    name = models.CharField(max_length=255)
    tough_name = models.CharField(max_length=255)
    description = models.CharField(max_length=2000)
    # 0 - Not Required
    # 1 - Required
    # 2 - Batch - changeable through form, and uploaded files
    # 3 - Unchangeable files (io, etc.)
    required = models.IntegerField(default=0)
    default_content = models.TextField(default="", blank=True)
    ordering = models.IntegerField()

    class Meta:
        ordering = ['ordering', 'id']

    def __unicode__(self):
        return "%s: %s" % (self.tough_name.upper(), self.name)

    def get_name_list_dict(self):
        var_dict = {}
        for var in self.blockvariable_set.all():
            if not var_dict.has_key(var.name_list):
                var_dict.update({var.name_list:[]})
            var_dict[var.name_list].append(var)
        return var_dict

class Block(models.Model):
    blockType = models.ForeignKey(BlockType)
    job = models.ForeignKey(Job)
    content = models.TextField(blank=True)
    last_uploaded = models.DateTimeField(null = True, default = None)
    num_elem = models.IntegerField(null = True, default = None)
    num_conn = models.IntegerField(null = True, default = None)
    upload_file_name = models.CharField(null = True, default = None, max_length=256)

    class Meta:
        ordering = ['blockType__ordering', 'blockType__id']

    def get_raw_input_form(self):
        return RawInputForm(data={"rawinput": self.content})

    def get_import_form(self):
        return ImportBlockForm(user = self.job.user, job_id = self.job.pk)

    def is_empty(self):
        return len(self.content) <= 0

    def reset_block_upload_times(self):
        self.last_uploaded = None
        self.save()
        return


class QualifiedBlockRef(models.Model):
    blockType = models.ForeignKey(BlockType)
    name = models.CharField(max_length=255)


class BlockVariable(models.Model):
    blockType = models.ForeignKey(BlockType)
    var_name = models.CharField(max_length=255)
    name_list = models.TextField(max_length=255)
    commented = models.BooleanField()
