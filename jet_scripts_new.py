#!/usr/bin/env /opt/alt/python27/bin/python
import socket
import sys
import random
import MySQLdb
import logging

# get jetbackup existing configuration


def getconfig(a):
    with open('/etc/jetapps/apps/jetbackup/config.php') as f:
        file_str = f.read()
        for x in file_str.splitlines():
            if a in x:
                a = ((x.split(" ")[2])[1:-2])
    return a


# define some variable
srvhost = socket.gethostname().split('.')[0]
db_host = getconfig('db_host')
db_name = getconfig('db_name')
db_user = getconfig('db_user')
db_pass = getconfig('db_pass')
db_prefix = getconfig('db_prefix')
dest = 'destinations'
job = 'jobs'
cfg = 'config'
backup_local_name = 'Backup-gluster'
backup_ssh_name = 'SG Backup server'
backup_path_local = '/backup/jet' + srvhost
backup_path_ssh = '/data/sda1/niagahoster/jet' + srvhost


# Check existing backup destinations
def check_existing_backup_dest(backup_path):
    try:
        con = MySQLdb.connect(db_host, db_user, db_pass, db_name)
        cur = con.cursor()
        query = ("SELECT id from {}{} where data like '%{}%'".format(db_prefix, dest, backup_path))
        cur.execute(query)
        if cur.rowcount > 0:
            return True
        else:
            return False
    except MySQLdb.Error, e:
            logging.error("Error {}: {}".format(e.args[0], e.args[1]))
            sys.exit(1)
    finally:
        if con:
            con.close()
# Delete existing backup destination


def del_existing_backup_dest(backup_path):
    try:
        con = MySQLdb.connect(db_host, db_user, db_pass, db_name)
        cur = con.cursor()
        query = ("DELETE from {}{} where data like '%{}%'".format(db_prefix, dest, backup_path))
        cur.execute(query)
        if cur.rowcount > 0:
            return True
        else:
            return False
    except MySQLdb.Error, e:
            logging.error("Error {}: {}".format(e.args[0], e.args[1]))
            sys.exit(1)
    finally:
        if con:
            con.close()

# Create backup destination


def create_backup_destination(desname):

        db_contain = 'a:4:{s:11:"incremental";s:1:"1";s:5:"extra";s:1:"1";s:10:"compressed";s:1:"1";s:12:"uncompressed";s:1:"1";}'
        file_contain = 'a:3:{s:11:"incremental";s:1:"1";s:10:"compressed";s:1:"1";s:12:"uncompressed";s:1:"1";}'
        rating_desc = 'a:0:{}'
        db_data = 'a:3:{s:4:"path";s:' + str(len(backup_path_local)) + ':"' + backup_path_local + '";s:5:"owner";s:4:"root";s:2:"id";i:2;}'
        file_data = 'a:10:{s:4:"path";s:' + str(len(backup_path_local)) + ':"' + backup_path_local + '";s:4:"host";s:10:"10.4.2.101";s:4:"port";s:2:"65002";s:8:"username";s:4:"root";s:8:"password";s:0:"";s:10:"privatekey";s:27:"/root/.ssh/backup-rsync-key";s:7:"timeout";s:2:"30";s:8:"authtype";s:3:"key";s:5:"owner";s:4:"root";s:2:"id";i:5;}'

#    try:
#       con = MySQLdb.connect(host, db_user, db_pass, db)
#       cur = con.cursor()
#        if (desname == "file"):
#           query = ("INSERT INTO {}{} (type,name,engine,contain,data,owner,rating,rating_desc) VALUES ('SSH','{}','1','{}','{}','root','5.0','{}')"
#           .format(db_prefix,dest,backup_ssh_name,file_contain,file_data,rating_desc))
#       elif (desname== "db"):
#            query = ("INSERT INTO {}{} (type,name,engine,contain,data,owner,rating,rating_desc) VALUES ('Local','{}','1','{}','{}','root','5.0','{}')"
#            .format(db_prefix,dest,backup_local_name,db_contain,db_data,rating_desc))
#        else:
#            return False #Need everyone to check
#        cur.execute(query)
#    except MySQLdb.Error, e:
#        logging.error("Error {}: {}".format(e.args[0], e.args[1]))
#        sys.exit(1)
#    finally:
#        if con:
#            con.close()

# Create Job backup


def create_job(jobname):
    packages = 'a:0:{}'
    resellers = 'a:0:{}'
    rangee = 'a:3:{s:5:"start";s:1:"0";s:3:"end";s:1:"0";s:10:"underscore";i:0;}'
    schedule = 'a:11:{s:4:"type";s:5:"daily";s:6:"hourly";i:0;s:5:"daily";a:1:{i:0;s:6:"sunday";}s:6:"weekly";s:0:"";s:7:"monthly";a:0:{}s:4:"hour";s:2:"01";s:3:"min";s:2:"00";s:4:"ampm";s:2:"am";s:5:"delay";a:2:{s:4:"type";s:7:"minutes";s:6:"amount";i:0;}s:7:"endtime";a:5:{s:6:"active";i:0;s:4:"hour";s:2:"01";s:3:"min";s:2:"00";s:4:"ampm";s:2:"am";s:9:"startover";i:0;}s:11:"endaccounts";i:0;}'
    backup_start_day = random.choice(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    backup_run_day = backup_start_day
    nextrun = 'wait'
    performance = 'a:3:{s:3:"lve";i:0;s:6:"ionice";i:1;s:6:"renice";i:1;}'
    retain = '1'
    prejob = ''
    postjob = ''
    owner = 'root'
    nextaccount = ''
    progressbar = ''
    rating = '4.5'
    #    try:
    #       con = MySQLdb.connect(host, db_user, db_pass, db)
    #       cur = con.cursor()

    if (jobname == "file"):
       descriptionjob = 'Backup user data' + srvhost
       destination_id = cur.execute(("SELECT id from {}{} where data like '%{}%'".format(db_prefix, dest, backup_path)))
       typee = 'incremental'
       users = 'a:2:{s:4:"type";s:8:"rotation";s:4:"data";a:0:{}}'
       path = 'account'
       directory = ''
       databases = '1'
       exclude = 'wait'
       rating_desc='a:3:{i:0;s:51:"The recommended backup retention is between 7 to 21";i:1;s:71:"Backup Job Monitor is not enabled - Notify me if there where no backups";i:2;s:75:"Backup Job Monitor is not enabled - Notify me if job process runs endlessly";}'

    elif (jobname == "db"):
        descriptionjob = 'Backup database' + srvhost
        destination_id = cur.execute("(SELECT id from {}{} where data like '%{}%')".format(db_prefix,dest,backup_path_local))
        typee = 'accountsdb'
        users = 'a:2:{s:4:"type";s:3:"all";s:4:"data";a:0:{}}'
        path = 'database'
        databases = ''
        exclude = ''
        rating_desc = 'a:4:{i:0;s:74:"Avoid backing up junk by setting directories and files in the exclude list";i:1;s:51:"The recommended backup retention is between 7 to 21";i:2;s:71:"Backup Job Monitor is not enabled - Notify me if there where no backups";i:3;s:75:"Backup Job Monitor is not enabled - Notify me if job process runs endlessly";}'
    else:
        print "Nothing"

    query = ("INSERT INTO {}{} (description,destination_id,type,users,packages,resellers,range,schedule,performance,retain,path,directory,databases,exclude,prejob,postjob,owner,nextrun,nextaccount,progressbar,rating,rating_desc)VALUES({},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{})"
    .format(db_prefix,job,descriptionjob,destination_id,typee,users,packages,resellers,rangee,schedule,performance,retain,path,directory,databases,exclude,prejob,postjob,owner,nextrun,nextaccount,progressbar,rating,rating_desc))

    print query
#       cur.execute(query)
#    except MySQLdb.Error, e:
#        logging.error("Error {}: {}".format(e.args[0], e.args[1]))
#        sys.exit(1)
#    finally:
#        if con:
#            con.close()



#  Check existing file backup job
def check_existing_backup_job(name):
    try:
        con = MySQLdb.connect(db_host, db_user, db_pass, db_name)
        cur = con.cursor()
        query = ("SELECT id from {}{} where description like '%{}{}%'".format(db_prefix,job,name, srvhost))
        cur.execute(query)
        if cur.rowcount > 0:
            return True
        else:
            return False
    except MySQLdb.Error, e:
            logging.error("Error {}: {}".format(e.args[0], e.args[1]))
            sys.exit(1)
    finally:
        if con:
            con.close()

# Delete existing backup job
def del_existing_backup_job(backup_path):
    try:
        con = MySQLdb.connect(db_host, db_user, db_pass, db_name)
        cur = con.cursor()
        query = ("DELETE from {}{} where description like '%{}{}%'".format(db_prefix,job,name, srvhost))
        cur.execute(query)
        if cur.rowcount > 0:
            return True
        else:
            return False
    except MySQLdb.Error, e:
            logging.error("Error {}: {}".format(e.args[0], e.args[1]))
            sys.exit(1)
    finally:
        if con:
            con.close()


create_job(jobname="f")

# Start check existing and create destination configuratin
#if (check_existing_backup_dest(backup_path_ssh)== True): print "Terdapat Job backup file"

#if (check_existing_backup_dest(backup_path_local)== True): print "Terdapat Job backup db"



 # Start check and create jobs
#print check_existing_backup_job(name="Backup userdata ")

#if (check_existing_backup_job(name="Backup userdata ")== True): print "Terdapat backup file"

#if (check_existing_backup_job(name="Backup database ")== True): print "Terdapat backup database"
