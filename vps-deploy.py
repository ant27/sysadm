################################################################################################
#  vps-deploy.py - script for automated deployment of docker services on specific vps server   #
#  author: Antonov Viacheslav, 04.2023                                                         #
#  digiant.ru                                                                                  #
################################################################################################
import argparse
import os
import re
from datetime import datetime

LAST_MODIFIED_DATE = "11.04.2023"
VERSION = "0.7"

####### Parsing script arguments #######
parser = argparse.ArgumentParser(description=
'vps-deploy.py - script for automated deployment of docker services on specific vps server,'
'author: Antonov Viacheslav, 04.2023, digiant.ru'
)
parser.add_argument(
    '--recovery',
    '-r',
    type=str,
    default="/srv/vps_backup/",
    help='dir with backup (default: /srv/vps_backup/)'
)
args = parser.parse_args()
print(args.recovery)

######### DECLARE FUNCTIONS ############
#current date and time in specific format
def date_stamp():
    return datetime.today().strftime('%Y-%m-%d %H:%M:%S')
#print ang log
def logger(msg):
    print(date_stamp() + " : " + msg)
    log_file.write(date_stamp() + " : " + msg + "\n")
#parse user input
def get_answer(question, question_type):
    answer = input(question)
    match question_type:
        case "b":
            if answer == "yes":
                logger("User answered YES on question: " + question)
                return True
            else:
                logger("User answered NO on question: " + question)
                return False
        case "s":
            logger("User enter value:" + answer + " on request:" + question)
            return str(answer)
        case "i":
            logger("User enter value:" + answer + " on request:" + question)
            return int(answer)

def print_docker_struct():
    for item in docker:
        nested_item_lev2 = docker[item]
        if len(nested_item_lev2) > 0:
            item_str = "├─ " + item + " ──┐"
        else:
            item_str = "|-" + item
        item_str_len = len(item_str)
        print(item_str)
        for nested_item_lev3 in nested_item_lev2:
            nested_item_lev4 = nested_item_lev2[nested_item_lev3]
            n = 2
            spaces = ""
            while n < item_str_len:
                spaces += " "
                n += 1
            print("│" + spaces + "├─ " + nested_item_lev3)
            print(nested_item_lev4)
        print("│")

def print_structure(item_name,item_data,item_name_len):
    if isinstance(item_data, dict):
      for item_name, item_data in item_data.items():
        print(" "*item_name_len+"├─ "+item_name+" ──┐")
        item_name_len += len(item_name) + 6
        print_structure(item_name,item_data,item_name_len)
        item_name_len -= len(item_name) + 6
    else:
      print(" "*item_name_len+item_data)

# for item_name, item_data in docker.items():
#     print_structure(item_name, item_data, 0, 0)


######### DOCUMENTATION ####################
# 1. https://docs.gitlab.com/ee/install/docker.html - Install GitLab using Docker Compose
# 2. https://docs.gitlab.com/omnibus/settings/nginx.html - Install GitLab Using a non-bundled web-server
# 3. https://hub.docker.com/_/mediawiki - Install MediaWiki using Docker Compose
# 4. https://miac.volmed.org.ru/wiki/index.php/Docker-compose_%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0_%D0%B4%D0%BB%D1%8F_%D1%81%D0%B0%D0%B9%D1%82%D0%B0_NGINX_%2B_MYSQL_%2B_PHP-FPM -
#  Install Nginx using Docker Compose with multiple sites

######### SERVICES ####################
#1. Nginx
#2. MySql
#3. Gitlab
#4. DotProject
#5. OwnCloud
#6. Some etc.

######### INIT VARIABLES ##############
log_filename = "vps-deploy.log"

#bacic
domain = "test.ru"

#docker config dictionary
docker = {
    "volumes": {
        "mediawiki-data": "/srv/mediawiki/data",
    },
    "networks": {
        "internal": {"driver": "bridge"},
        "external": {"driver": "bridge"}
    },
    "services": {
        "common_configs": {
            "env_file": ".env",
            "restart": "unless-stopped"
        },
        "nginx": {
            "image": "nginx:1.17.4-alpine",
            "ports": {"80": "80"},
            "volumes": {
                "mediawiki-data": "/var/www/mediawiki"
            },
            "mounts": {
                "/srv/nginx/www-default": "/var/www/html",
                "/srv/nginx/conf.d": "/etc/nginx/conf.d"
            },
            "networks": {
                "external",
                "internal"
            }
        },
        "mysql": {
            "image": "mysql:8.0",
            "mounts": {
                "/srv/mysql/data": "/var/lib/mysql",
                "/srv/mysql/init.d": "/docker-entrypoint-initdb.d"
            },
            "networks": {
                "external",
                "internal"
            }
        },
        "mediawiki": {
            "image": "mediawiki",
            "volumes": {"mediawiki-data": "/var/www/html"}, #??? Wiki data location?
            "mounts": {
                "/srv/mediawiki/config/LocalSettings.php": "/var/www/html/LocalSettings.php", #/var/www/html/LocalSettings.php
            },
            "networks": {
                "external",
                "internal"
            }
        },
        "gitlab": {
            "image": "gitlab/gitlab-ce:latest",
            "ports": {
                "443": "443",
                "22": "222",  #!!! Use non default ssh port fo gitlab
            },
            "hostname": domain,
            "mounts": {
                "/srv/gitlab/config": "/etc/gitlab",
                "/srv/gitlab/data": "/opt/gitlab",
                "/srv/gitlab/logs": "/var/log/gitlab",
                "/srv/gitlab/registry": "/var/opt/gitlab/registry"
            },
            "networks": {
                "external",
                "internal"
            }
        }
#        "gitlab-runner": {
#            "image": "gitlab/gitlab-runner:latest",
#            "mounts": {
#                "/srv/gitlab/gitlab-runner/config": "/etc/gitlab-runner",
#                "/srv/gitlab/gitlab-runner/data": "/home/gitlab_ci_multi_runner/data"
#            }
#        }
    }
}
######### START SCRIPT ################
#Open or create logfile if not exist
log_file = open(log_filename, 'a+')


#get_answer("How are you, yes or any key for no", "b")

#print(os.listdir("/home"))
#print(os.mkdir("/home/user/test_dir"))

#print_docker_struct()

print_structure(0,docker,0)

