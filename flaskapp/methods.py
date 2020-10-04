import os
from csv import DictWriter, writer
from datetime import datetime, timedelta
from pathlib import Path
from flask_login import current_user

from .models import Unit, Personnel, Personnel_status, User


def retrieve_personnel_list(fmw_id, clearance=100, query_all=False):
    if query_all == True and clearance <= 2: return Personnel.query.all()
    # subquery = Fmw.query.filter_by(name=fmw).first()
    return Personnel.query.filter_by(fmw_id=fmw_id).all()


def retrieve_personnel_statuses(db, fmw_id, date, clearance=100, missing_status_needed=True, query_all=False):
    if clearance <= 2 and query_all == True:
        # query all
        personnel_statuses = db.session.query(Personnel_status).filter(
            Personnel_status.date == date, Personnel.id == Personnel_status.personnel_id).all()

        if missing_status_needed == True:
            subquery = db.session.query(Personnel.id).join(Personnel_status,
                                                           Personnel.id == Personnel_status.personnel_id).filter(
                Personnel_status.date == date)
            missing_status = db.session.query(Personnel).filter(Personnel.id.notin_(subquery)).all()

    else:
        # fmw_query = Fmw.query.filter_by(name=fmw).first()
        personnel_statuses = db.session.query(Personnel_status).filter(
            Personnel_status.date == date, Personnel.id == Personnel_status.personnel_id,
            Personnel.fmw_id == fmw_id).all()

        if missing_status_needed == True:
            subquery = db.session.query(Personnel.id).join(Personnel_status,
                                                           Personnel.id == Personnel_status.personnel_id).filter(
                Personnel_status.date == date)
            # fmw_query = Fmw.query.filter_by(name=fmw).first()
            missing_status = db.session.query(Personnel).filter(Personnel.id.notin_(subquery),
                                                                Personnel.fmw_id == fmw_id).all()

    return (personnel_statuses, missing_status) if (missing_status_needed == True) else (personnel_statuses)


def retrieve_all_groups_accessible_by_user():
    if not current_user:
        return []

    group_list = []
    all_units = Unit.query.filter(Unit.name != "0").all()
    for unit in all_units:
        # if clearance is 2, all units can be viewed
        # but if clearance is 3, we need to filter till we get the correct unit
        if current_user.clearance == 2 or current_user.fmw.unit == unit:
            group_list.extend((group.id, "{} - {}".format(unit.name, group.name)) for group in unit.fmw)

    return group_list


def generate_PS(records, request_date=None):
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
        csvwriter.writerow(['Date', request_date])
        # write excel header
        fieldnames = ['fmw', 'Name', 'Rank', 'Am status', 'Am Remarks', 'Pm status', 'Pm Remarks']
        csvwriter = DictWriter(csvfile, fieldnames=fieldnames)
        csvwriter.writeheader()
        for record in records:
            csvwriter.writerow({'fmw': record.Person.fmw, 'Name': record.Person.name, 'Rank': record.Person.rank,
                                'Am status': record.am_status, 'Am Remarks': record.am_remarks,
                                'Pm status': record.pm_status, 'Pm Remarks': record.pm_remarks})

    if Path(new_file_path).is_file():
        return None
    return 'File not created'
