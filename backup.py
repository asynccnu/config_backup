"""
backup mongo database to qiniu
"""
import os
import datetime
import time
from threading import Timer
from qiniu import Auth, put_file, etag
import qiniu.config

def mongoexec():
    """
    get mongo database infomation
    invoke upload function
    """
    print("Start")
    todaytime = datetime.datetime.today()
    file_name = "Manaconf" + "Y" + str(todaytime.year) + "M" + str(todaytime.month) + \
                "D" + str(todaytime.day) + "H" + str(todaytime.hour)  + str(time.time())

    _mongo_host = os.getenv("HOST")
    _mongo_port = os.getenv("PORT")
    _db_name = os.getenv("DB")

    dumpcommand = "mongodump" + " -h " + _mongo_host + ":" + \
                    _mongo_port + " -d " + _db_name + " -o " + "~/.backupmongo"
    tarcommand = "tar -cvf " + file_name + ".tar " + "~/.backupmongo/" + _db_name
    os.system(dumpcommand)
    os.system(tarcommand)
    
    file_path = file_name + ".tar"
    upload(file_path, file_name)



def upload(file_path, file_name):
    """
    file_path: local file's path
    file_name: file's name (the name of the file uploaded to qiniu)
    Upload to qiniu
    """
    _access_key = os.getenv("ACCESS")
    _secret_key = os.getenv("SECRET")
    _bucket_name = os.getenv("BUCKET")

    q = Auth(_access_key, _secret_key)
    backet_name = _bucket_name
    token = q.upload_token(backet_name, file_name, 3600)
    localfile = file_path

    ret, info = put_file(token, file_name, localfile)
    print(info)
    assert ret['key'] == file_name
    assert ret['hash'] == etag(localfile)
    rmcommand = "rm " + file_path

    os.system(rmcommand)

def main():
    t = Timer(7200, mongoexec)
    t.start()
    

if __name__ == '__main__':
    main()
