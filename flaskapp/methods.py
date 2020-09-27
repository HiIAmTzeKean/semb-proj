import os
from csv import writer, DictWriter
from datetime import timedelta,datetime
from pathlib import Path
from .models import Personnel,Personnel_status

def nameconverter_paradestateform(rows):
    names = [] 
    for row in rows:
        names.append((row.id, row.name))
    return names


def authenticate_user(table, username, password):
    error = None
    # user = db.execute(
    #          'SELECT * FROM user WHERE username = ?', (username,)
    #      ).fetchone()
    user = table.query.filter_by(username=username).first()
    if user is None:
        error = 'Incorrect username.'
    elif user.password != password:
        error = 'Wrong password'
    return error, user


def retrieve_personnel_list(fmw,clearance=100):
    if fmw == "Admin" or clearance < 2: return Personnel.query.all()
    return Personnel.query.filter_by(fmw=fmw).all()


def retrieve_personnel_statuses(db,fmw,date,clearance=100,missing_status_needed=True):
    if fmw == 'Admin' or clearance<2:
        personnel_statuses = db.session.query(Personnel_status).filter(
            Personnel_status.date==date,Personnel.id==Personnel_status.personnel_id).all()

        if missing_status_needed==True:
            subquery = db.session.query(Personnel.id).join(Personnel_status, Personnel.id==Personnel_status.personnel_id).filter(Personnel_status.date==date)
            missing_status = db.session.query(Personnel).filter(Personnel.id.notin_(subquery)).all()
    else:
        personnel_statuses = db.session.query(Personnel_status).filter(
            Personnel_status.date==date,Personnel.id==Personnel_status.personnel_id,Personnel.fmw==fmw).all()
            
        if missing_status_needed==True:
            subquery = db.session.query(Personnel.id).join(Personnel_status, Personnel.id==Personnel_status.personnel_id).filter(Personnel_status.date==date)
            missing_status = db.session.query(Personnel).filter(Personnel.id.notin_(subquery),Personnel.fmw==fmw).all()
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
            csvwriter.writerow({'fmw': record.Person.fmw, 'Name': record.Person.name, 'Rank': record.Person.rank,
            'Am status': record.am_status,'Am Remarks': record.am_remarks,
            'Pm status': record.pm_status,'Pm Remarks': record.pm_remarks})

    if Path(new_file_path).is_file():
        return None
    return 'File not created'