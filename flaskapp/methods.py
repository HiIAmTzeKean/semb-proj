import os
from csv import writer, DictWriter
from datetime import date


def nameconverter_paradestateform(rows):
    names = [] 
    for row in rows:
        names.append((row["id"], row["name"]))
    return names


def authenticate_user(db, username, password):
    error = None
    user = db.execute(
             'SELECT * FROM user WHERE username = ?', (username,)
         ).fetchone()
    if user is None:
        error = 'Incorrect username.'
    elif user['password'] != password:
        error = 'Wrong password'
    return error, user


def retrieve_personnel_list(db, fmw):
    query = db.execute(
             'SELECT * FROM personnel WHERE fmw = ?', (fmw,)
         ).fetchall()
    return query

# retrive status for display in PS 
def retrieve_personnel_statuses(db,fmw):
    #first get personnel ID which belongs to the FMW
    id_list = list()
    query = db.execute(
        '''SELECT * from personnel
        WHERE fmw = ?''',(fmw,)
    )
    for person in query:
        id_list = 
    #Then get the status of those who ID mataches
    personnels = db.execute(
        '''SELECT * from personnel_status WHERE '''
    )
    return personnel_statuses


def generate_PS():
    # create func to write per day
    date_today = date.today().strftime("%d%m%Y")
    # create file and open in write mode
    csv_name = os.path.join('excel_sheets','{}.csv'.format(date_today))
    with open(csv_name, 'w', newline='') as csvfile:
        # write date first
        csvwriter = writer(csvfile)
        csvwriter.writerow(['Date',date_today])
        # write data from data base
        fieldnames = ['fmw','Name','Rank','Am status','Am Remarks','Pm status','Pm Remarks']
        csvwriter = DictWriter(csvfile, fieldnames=fieldnames)
        csvwriter.writeheader()
