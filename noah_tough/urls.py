from django.conf.urls import *
from django.views.generic import TemplateView
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'noah.views.home'),
    url(r'^home/$', 'noah.views.home'),
    url(r'^about/$', 'noah.views.about'),
    url(r'^login/$', 'usermanage.views.login_view'),
    url(r'^error/$', 'noah.views.report_error'),
    url(r'^logout/$', 'usermanage.views.logout_view'),
    url(r'^job/$', "noah.views.jobs"),
    url(r'^job/new/$', 'noah.views.create_job'),
    url(r'^job/(?P<job_id>\d+)/$', 'noah.views.job_view'),
    url(r'^job/(?P<job_id>\d+)/edit/$', 'noah.views.job_edit'),
    url(r'^job/(?P<job_id>\d+)/edit/upload/(?P<file_type>\w+)/$', 'noah.views.file_upload_view'),
    url(r'^job/(?P<job_id>\d+)/edit/import/(?P<file_type>\w+)/$', 'noah.views.import_file'),
    url(r'^job/(?P<job_id>\d+)/edit/info/$', 'noah.views.info_edit'),
    url(r'^job/(?P<job_id>\d+)/download/(?P<filename>.+)/$', 'noah.views.get_file'),
    url(r'^job/(?P<job_id>\d+)/tail/(?P<filepath>.+)/$', 'noah.views.tail_file'),
    url(r'^job/(?P<job_id>\d+)/view/(?P<filepath>.+)/$', 'noah.views.view_file'),
    url(r'^job/(?P<job_id>\d+)/graph/(?P<filepath>.+)/$', 'noah.views.view_graph'),
    url(r'^job/(?P<job_id>\d+)/file/(?P<filename>.+)/$', 'noah.views.get_file'),
    url(r'^job/(?P<job_id>\d+)/zip/$', 'noah.views.ajax_get_zip'),
    url(r'^job/(?P<job_id>\d+)/zip/(?P<directory>.+)/$', 'noah.views.ajax_get_zip'),
    url(r'^job/(?P<job_id>\d+)/power/$', 'noah.views.power_view'),
    url(r'^job/(?P<job_id>\d+)/rebuild/$', 'noah.views.rebuild_job'),
    url(r'^job/(?P<job_id>\d+)/(?P<type>copy)/$', 'noah.views.create_job'),
    url(r'^job/(?P<job_id>\d+)/(?P<type>move)/$', 'noah.views.create_job'),
    url(r'^job/(?P<job_id>\d+)/submit/$', 'noah.views.ajax_submit'),
    url(r'^job/(?P<job_id>\d+)/preview/$', 'noah.views.preview_input'),
    url(r'^job/(?P<job_id>\d+)/del/$', 'noah.views.delete_job'),
    url(r'^job/batch/del/$', 'noah.views.delete_jobs_selected'),
    url(r'^project/(?P<to_project_id>\d+)/add/$', 'noah.views.change_project'),
    url(r'^project/new/$', 'noah.views.create_project'),
    url(r'^project/edit/(?P<project_id>\d+)/$', 'noah.views.edit_project'),
    url(r'^project/(?P<project_id>\d+)/$','noah.views.project_view'),
    url(r'^project/(?P<project_id>\d+)/delete', 'noah.views.delete_project'),
    url(r'^ajax/job/(?P<job_id>\d+)/save/(?P<input_type>\w+)/$', 'noah.views.ajax_save'),
    url(r'^ajax/job/(?P<job_id>\d+)/graph/update/(?P<filepath>.+)/$', 'noah.views.update_graph'),
    url(r'^ajax/job/(?P<job_id>\d+)/edit/upload/(?P<file_type>\w+)/$', 'noah.views.file_upload'),
    url(r'^ajax/job/(?P<job_id>\d+)/file/(?P<directory>.+)/$', 'noah.views.ajax_get_job_dir'),
    url(r'^ajax/job/(?P<job_id>\d+)/file/$', 'noah.views.ajax_get_job_dir'),
    url(r'^ajax/job/move/$', 'noah.views.batch_move'),
    url(r'^ajax/job/(?P<job_id>\d+)/update/$', 'noah.views.ajax_get_job_info'),
    url(r'^ajax/job/(?P<job_id>\d+)/delete/(?P<path>.+)/$', 'noah.views.ajax_file_delete'),
)
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^404/$', TemplateView.as_view(template_name="404.html")),
    )
