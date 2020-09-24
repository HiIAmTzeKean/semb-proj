import csv
import sqlite3
import os
from pathlib import Path


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def insert_data_into_personnel_table(db):
    file = retrive_personnel_data()
    for line in file:
        pers_id,name,fmw,rank,active = line[:-1].split(',')
        db.execute('''INSERT INTO personnel
            (id,name,fmw,rank,active)
            VALUES (?,?,?,?,?)''',
            (pers_id,name,fmw,rank,active))
    db.commit()

def insert_data_into_user_table(db):
    file = retrive_user_data()
    for line in file:
        pers_id,username,password,fmw,fmd,clearance = line[:-1].split(',')
        db.execute('''INSERT INTO user
            (id,username,password,fmw,fmd,clearance)
            VALUES (?,?,?,?,?,?)''',
            (pers_id,username,password,fmw,fmd,clearance))
    db.commit()

def retrive_personnel_data():
    filePath = 'personnels.csv'
    file = open(filePath,'r')
    file.readline()
    return file

def retrive_user_data():
    filePath = 'users.csv'
    file = open(filePath,'r')
    file.readline()
    return file


if __name__ == "__main__":
    db = create_connection('flaskr.sqlite')
    insert_data_into_user_table(db)
