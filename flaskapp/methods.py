import os
from csv import writer, DictWriter
from datetime import timedelta,datetime
from pathlib import Path

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


def retrieve_personnel_statuses(db,fmw,date,missing_status_needed=True):
    if fmw == 'Admin':
        personnel_statuses = db.execute("""
        SELECT personnel.id, personnel.rank, personnel.name, personnel.fmw,
        personnel_status.am_status, personnel_status.am_remarks, personnel_status.pm_status, personnel_status.pm_remarks
        FROM personnel, personnel_status
        WHERE personnel.id = personnel_status.personnel_id 
        AND personnel_status.date = ?
        """, (date,) ).fetchall()
        if missing_status_needed==True:
            missing_status = db.execute("""
            SELECT personnel.id, personnel.rank, personnel.name, personnel.fmw
            FROM personnel
            WHERE personnel.id NOT IN 
                (SELECT personnel.id FROM
                personnel_status INNER JOIN personnel ON personnel.id = personnel_status.personnel_id 
                WHERE personnel_status.date = ? )
            """, (date,) ).fetchall()
    else:
        personnel_statuses = db.execute("""
        SELECT personnel.id, personnel.rank, personnel.name, personnel.fmw,
        personnel_status.am_status, personnel_status.am_remarks, personnel_status.pm_status, personnel_status.pm_remarks
        FROM personnel, personnel_status
        WHERE personnel.id = personnel_status.personnel_id 
        AND personnel.fmw = ? AND personnel_status.date = ?
        """, (fmw,date) ).fetchall()
        #not done
        if missing_status_needed==True:
            missing_status = db.execute("""
            SELECT personnel.id, personnel.rank, personnel.name, personnel.fmw
            FROM personnel
            WHERE personnel.fmw = ? 
            AND personnel.id NOT IN 
                (SELECT personnel.id FROM
                personnel_status INNER JOIN personnel ON personnel.id = personnel_status.personnel_id 
                WHERE personnel_status.date = ? )
            """, (fmw,date) ).fetchall()
    return (personnel_statuses, missing_status) if (missing_status_needed == True) else (personnel_statuses)


def generate_PS(records,request_date=None):
    # create func to write per day
    if request_date is None:
        request_date = datetime.date(datetime.today())
    # create file and open in write mode
    directory = 'csv_archives'
    parent_directory = Path().absolute()
    dir_path = os.path.join(parent_directory, directory)
    try:
        os.mkdir(dir_path)
    except FileExistsError:
        pass
    new_file_path = os.path.join(dir_path, str(request_date))
    with open(new_file_path, 'w', newline='') as csvfile:
        # write date first
        csvwriter = writer(csvfile)
        csvwriter.writerow(['Date',request_date])
        # write excel header
        fieldnames = ['fmw','Name','Rank','Am status','Am Remarks','Pm status','Pm Remarks']
        csvwriter = DictWriter(csvfile, fieldnames=fieldnames)
        csvwriter.writeheader()
        for record in records:
            csvwriter.writerow({'fmw': record['fmw'], 'Name': record['name'],'Rank': record['rank'],
            'Am status': record['am_status'],'Am Remarks': record['am_remarks'],
            'Pm status': record['pm_status'],'Pm Remarks': record['pm_remarks']})

    if Path(new_file_path).is_file():
        return None
    return 'File not created'