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


def retrieve_personnel_list(db, fmw,clearance=''):
    if fmw == "Admin": return db.execute('SELECT * FROM personnel').fetchall()
    return db.execute('SELECT * FROM personnel WHERE fmw = ?', (fmw,)).fetchall()


def retrieve_personnel_statuses(db,fmw,date):
    if fmw == 'Admin':
        personnel_statuses = db.execute("""
    SELECT personnel.id, personnel.rank, personnel.name, 
    personnel_status.am_status, personnel_status.am_remarks, personnel_status.pm_status, personnel_status.pm_remarks
    FROM personnel, personnel_status
    WHERE personnel.id = personnel_status.personnel_id 
    AND personnel_status.date = ?
    """, (date,) ).fetchall()
        missing_status = db.execute("""
    SELECT personnel.rank, personnel.name, personnel.fmw
    FROM personnel
    WHERE personnel.id NOT IN 
        (SELECT personnel.id FROM
        personnel_status INNER JOIN personnel ON personnel.id = personnel_status.personnel_id 
        WHERE personnel_status.date = ? )
    """, (date,) ).fetchall()
    else:
        personnel_statuses = db.execute("""
    SELECT personnel.id, personnel.rank, personnel.name, 
    personnel_status.am_status, personnel_status.am_remarks, personnel_status.pm_status, personnel_status.pm_remarks
    FROM personnel, personnel_status
    WHERE personnel.id = personnel_status.personnel_id 
    AND personnel.fmw = ? AND personnel_status.date = ?
    """, (fmw,date) ).fetchall()
    #not done
        missing_status = db.execute("""
    SELECT personnel.rank, personnel.name, personnel.fmw
    FROM personnel
    WHERE personnel.fmw = ? 
    AND personnel.id NOT IN 
        (SELECT personnel.id FROM
        personnel_status INNER JOIN personnel ON personnel.id = personnel_status.personnel_id 
        WHERE personnel_status.date = ? )
    """, (fmw,date) ).fetchall()
    return personnel_statuses, missing_status


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