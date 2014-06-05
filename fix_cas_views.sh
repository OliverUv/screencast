#!/usr/bin/env bash

if [[ ! -n "$1" ]] ; then
    echo "Fix the django-cas file views.py"
    echo "Usage: $(basename $0) [relative path to views.py]"
    exit 1
fi

sed --regexp-extended -i '

s/get_host, //

7 a from django.contrib import messages

s/(request\.)?user\.message_set\.create\(message=message\)/messages.add_message(request, messages.INFO, message)/

s/get_host\(request\)/request.get_host()/

' $1
