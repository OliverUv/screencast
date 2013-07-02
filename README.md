screencast
==========

Installation instructions
-------------------------

### Configure in `screencast/local_settings.py`

 -  Database info
 -  Template dirs
 -  Static files dirs

### Changes in django_cas' views.py

If using django_cas version 2.0.3, you need to make the following changes in `yourvirtualenv/lib/python2.7/site-packages/django_cas/view.py`

 -  Add the import `from django.contrib import messages`
 -  In both places, replace `user.message_set.create(message=message)` with `messages.add_message(request, messages.INFO, message)`
 -  Change all occurrences of `get_host(request)` to `request.get_host()`
