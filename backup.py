from threading import Timer
from qiniu import Auth, put_file, etag
import qiniu.config
import os
import datetime
import time

def mongoexec():
    print("Start")
    todaytime = datetime.datetime.today()
    file_name = "Manaconf" + "Y" + str(todaytime.year) + "M" + str(todaytime.month) + "D" + str(todaytime.day) + "H" + str(todaytime.hour)  + str(time.time())

    HOST = os.getenv("HOST")
    PORT = os.getenv("PORT")
    DB = os.getenv("DB")

    dumpcommand = "mongodump" + " -h " + HOST + ":" + PORT + " -d " + DB + " -o " + "~/.backupmongo" 
    tarcommand = "tar -cvf " + file_name + ".tar " + "~/.backupmongo/" + DB
    os.system(dumpcommand)
    os.system(tarcommand)
    
    file_path = file_name + ".tar"
    upload(file_path, file_name)


def upload(file_path, file_name):
    ACCESS = os.getenv("ACCESS")
    SECRET = os.getenv("SECRET")
    BUCKET = os.getenv("BUCKET")

    q = Auth(ACCESS, SECRET)
    backet_name = BUCKET
    token = q.upload_token(backet_name, file_name, 3600)
    localfile = file_path

    ret, info = put_file(token, file_name, localfile)
    print(info)
    assert ret['key'] == file_name
    assert ret['hash'] == etag(localfile)
    rmcommand = "rm " + file_path
    os.system(rmcommand)

def main():
    t = Timer(1, mongoexec)
    t.start()

if __name__ == '__main__':
   main()
