screencast
==========

Installation instructions
-------------------------

### Prerequisites

It is recommended that you use a virtualenv when installing the prerequisites. All
prerequisites can be found in requirements.txt, you can install them easily by running
`pip install -r requirements.txt`

### Configure `screencast/local_settings.py`

Copy the file `screencast/local_settings_template.py` to `screencast/local_settings.py`
and change the paths and settings so that they fit into your system setup. The following
things must be changed:

 -  Database info
 -  Template dirs
 -  Static files dirs

### Changes in django_cas' views.py

If using django_cas version 2.0.3, you need to patch `yourvirtualenv/lib/python2.7/site-packages/django_cas/view.py`

Do this by running the script `fix_cas_views.sh path/to/view.py` (probably something like `./fix_cas_views.sh ~/.virtualenvs/screencast/lib/python2.7/site-packages/django_cas/views.py`) It will do the following:

 -  Add the import `from django.contrib import messages`
 -  Replace `user.message_set.create(message=message)` with `messages.add_message(request, messages.INFO, message)`
 -  Replace `request.user.message_set.create(message=message)` with `messages.add_message(request, messages.INFO, message)`
 -  Change all occurrences of `get_host(request)` to `request.get_host()`
