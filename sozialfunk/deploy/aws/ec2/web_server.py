#!/usr/bin/python
"""
Soma Analytics EC2 web server cloud maintenance scripts.
"""

import time
from fabric.api import hosts, run, execute, sudo
from fabric.context_managers import cd
from boto import ec2
import settings

def get_ec2_connection():
    ec2c = ec2.connect_to_region(settings.REGION,aws_access_key_id = settings.AWS_ACCESS_KEY_ID,aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY)
    return ec2c

def launch_web_server(user_data = "",instance_type = settings.WEB_SERVER_INSTANCE_TYPE,instance_name = settings.WEB_SERVER_INSTANCE_NAME,security_group = settings.WEB_SERVER_SECURITY_GROUP,key_pair = settings.WEB_SERVER_KEY_PAIR):
    ec2c = get_ec2_connection()
    ami = ec2c.get_all_images(owners = 'self',filters = {'tag:role':instance_name})[0]
    r = ec2c.run_instances(ami.id, instance_type=instance_type, key_name=key_pair, user_data=user_data, security_groups=[security_group],placement = settings.AZ)

    time.sleep(2)
    
    i = r.instances[-1]
    ec2c.create_tags([i.id], {"role": instance_name})
    while not i.update() == 'running':
        time.sleep(1)
    return i

def get_ec2_instances():
    ec2c = get_ec2_connection()
    reservations = ec2c.get_all_instances()
    return [instance for reservation in reservations for instance in reservation.instances]

def deploy_django_app(instances,ssh_user = settings.WEB_SERVER_SSH_USER,django_directory = settings.WEB_SERVER_DJANGO_DIRECTORY,app_directory = settings.WEB_SERVER_APP_DIRECTORY,repository_url = settings.WEB_SERVER_REPOSITORY_URL):
    
    host_names = []
    
    for instance in instances:
        if instance.update() == 'running':
            host_names.append(ssh_user+"@"+instance.ip_address)
 
    def checkout_django_code():
        sudo("service apache2 stop") #Stop Apache
        with cd(django_directory):
            sudo('rm -rf %s' % app_directory)
            sudo('git clone %s %s' % (repository_url,app_directory))
        with cd(django_directory+"/"+app_directory):
            sudo('ln -s settings_production.py soma_django/settings.py') # Link production settings file
        sudo("service apache2 start") #Restart Apache
    try:
        execute(checkout_django_code,hosts = host_names)
    except SystemExit:
        return -1
    