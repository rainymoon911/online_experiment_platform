#!/bin/bash

sudo -u www-data bash
cd /edx/var/edxapp
# where your woboq_codebrowser should put
mkdir woboq_codebrowser

#the dir you put static html files that user browse
cd staticfiles
mkdir codebrowser

#the dir you put code
mkdir ucore

#the git config file which used to switch users of gitlab and use the proper private key
cd /var/www/.ssh
touch config
chmod 600 config
