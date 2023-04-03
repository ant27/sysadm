################################################################################################
#  vps-deploy.py - script for automated deployment of docker services on specific vps server   #
#  author: Antonov Viacheslav, 04.2023                                                         #
#  digiant.ru                                                                                  #
################################################################################################
import argparse

LAST_MODIFIED_DATE = "02.04.2023"
VERSION = "0.00"

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

#test