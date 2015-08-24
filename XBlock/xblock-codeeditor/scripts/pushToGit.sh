#!/bin/bash
id=$1
username=$2
email=$3
commit_messege=$4

key_file=/var/www/.ssh/id_rsa_$id

cd /edx/var/edxapp/staticfiles/ucore/$id/ucore_lab

eval `ssh-agent -s`
ssh-add $key_file
git config user.email $email
git config user.name $username
git remote add origin$id git@$id:$username/ucore_lab.git
git add .
git commit -m "$commit_messege"
git push -u origin$id master

