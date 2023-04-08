################################################################################################
#  vps-deploy.py - script for automated deployment of docker services on specific vps server   #
#  author: Antonov Viacheslav, 04.2023                                                         #
#  digiant.ru                                                                                  #
################################################################################################
import argparse
import os
import re
from datetime import datetime

LAST_MODIFIED_DATE = "08.04.2023"
VERSION = "0.5"

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

#def find_him_and_kill_him:

######### SERVICES ####################
#1. Nginx
#2. Postgresql
#3. Gitlab
#4. DotProject
#5. OwnCloud
#6. Some etc.

######### INIT VARIABLES ##############
log_filename = "vps-deploy.log"

#bacic
domain = "test.ru"

#docker


#docker services
docker = {
    "volumes": {
        "www-data": "/srv/nginx/data",
        "db-data": "/srv/mysql/data",
        "certbot-etc": "/srv/certbot",
    },
    "networks": {
        "internal": {"driver": "bridge"},
        "external": {"driver": "bridge"}
    },
    "services": {
        "nginx": {
            "image": "nginx:1.17.4-alpine",
            "ports": {"80": "80"},
            "volumes": {"www-data": "/var/www/html"},
            "networks": {"external", "internal"}
        },
        "postgresql": {
            "image": "postgres:13.3",
            "volumes": {"db-data": "/var/lib/postgresql/data"},
            "networks": {"external", "internal"}
        }
    }
}
######### START SCRIPT ################
#Open or create logfile if not exist
log_file = open(log_filename, 'a+')


#get_answer("How are you, yes or any key for no", "b")

#print(os.listdir("/home"))
#print(os.mkdir("/home/user/test_dir"))

