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


def retrieve_personnel_statuses(db,fmw,date):
    if fmw == 'Admin':
        personnel_statuses = db.execute("""
    SELECT personnel.id, personnel.rank, personnel.name, 
    personnel_status.am_status, personnel_status.am_remarks, personnel_status.pm_status, personnel_status.pm_remarks
    FROM personnel, personnel_status
    WHERE personnel.id = personnel_status.personnel_id 
    AND personnel_status.date = ?
    """, (date,) ).fetchall()
    else:
        personnel_statuses = db.execute("""
    SELECT personnel.id, personnel.rank, personnel.name, 
    personnel_status.am_status, personnel_status.am_remarks, personnel_status.pm_status, personnel_status.pm_remarks
    FROM personnel, personnel_status
    WHERE personnel.id = personnel_status.personnel_id 
    AND personnel.fmw = ? AND personnel_status.date = ?
    """, (fmw,date) ).fetchall()
    #find out who has not submit their ps using ID
    #need to return as a sql query and those who did not submit
    return personnel_statuses

def retrieve_personnel_id_from_fmw(db, fmw):
    id_list = list()
    personnels = retrieve_personnel_list(db,fmw)
    for person in personnels:
        id_list.append(person['id'])
    return id_list

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
