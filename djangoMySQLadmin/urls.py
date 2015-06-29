from django.conf.urls import *

urlpatterns = patterns ('adbms.djangoMySQLadmin.views',

    url(r'^$', 'home'),

    url(r'^database', 'database'),

    url(r'^view-table', 'view_table'),

    url(r'^insert-entry', 'insert_entry'),

    url(r'^delete-entry', 'delete_entry'),

    url(r'^update-entry', 'update_entry'),

    url(r'^entry-inserted', 'entry_inserted'),

    url(r'^entry-deleted', 'entry_deleted'),

    url(r'^entry-updated', 'entry_updated'),

    url(r'^create-table', 'create_table'),

    url(r'^table-created', 'table_created'),

)