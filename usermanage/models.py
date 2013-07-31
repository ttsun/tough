from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import *
from dateutil.tz import *
import simplejson
import noah.utils as util

# Create your models here.


class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a NoahUser with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = NoahUser(email=MyUserManager.normalize_email(email),
                        date_of_birth=date_of_birth,
                        is_admin=False
                        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, date_of_birth, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
                                password=password,
                                date_of_birth=date_of_birth
                                )
        user.is_admin = True
        user.save()
        return user


class NoahUser(AbstractBaseUser):
    """
    Extend Django User Model to include newt cookies
    """

    username = models.CharField(max_length=40, unique=True, db_index=True)
    USERNAME_FIELD = 'username'
    is_admin = models.BooleanField(default=False)
    cookie = models.TextField(null=True, blank=True)

    def is_licensed_user(self):
        #check that they are in the appropriate group
        cookie_str = self.cookie
        checkurl = '/command/hopper/'
        cmd = '/usr/bin/groups %s' % self.username
        response, content = util.newt_request(checkurl, 'POST', params={'executable': cmd}, cookie_str=cookie_str)
        result = simplejson.loads(content)
        if response.status_code != 200:
            raise Exception(content)
        if "osp" in result['output']:
            return True
        else:
            return False

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_orphan_jobs(self):
        return self.job_set.filter(project=None)
    
    def get_all_jobs(self):
        """
        Return a list of all jobs
        """
        all_jobs = self.job_set.all().order_by("-time_last_updated", "project__name", "-id")
        # for job in all_jobs:
        #     job.check_exists()

        # get the list of jobs listed in the database as running and update them.
        dbrunning = all_jobs.filter(state__in=['in queue', 'started'])
        for runningjob in dbrunning: runningjob.update();

        # get the updated list 
        all_jobs = self.job_set.all().order_by("-time_last_updated", "project__name", "-id")

        return all_jobs

    def get_recent_jobs(self):
        for job in self.job_set.all():
            job.check_exists()
        jobs_list = self.job_set.all().exclude(exists=False).order_by('-time_last_updated')[:5]
        return jobs_list

    def get_projects(self):
        from noah.models import Project
        return self.project_set.all() | Project.objects.filter(creator=self)

    def set_cookie(self, cookie_str):
        cookie = {}
        for x in cookie_str.split(";"):
            x = x.strip()
            arr = x.split("=", 1)
            arr[0] = arr[0].lower().replace("-", "_")
            if len(arr) == 2:
                cookie.update({str(arr[0]): str(arr[1])})
            elif len(arr) == 1:
                cookie.update({str(arr[0]): "True"})
        self.cookie = simplejson.dumps(cookie)
        self.save()

    def get_cookie(self):
        cookie_dict = simplejson.loads(self.cookie)
        cookies = {}
        for x in cookie_dict:
            cookies.update({str(x): str(cookie_dict[x])})
        return cookies
