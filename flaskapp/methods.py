import os
from csv import DictWriter, writer
from datetime import datetime, timedelta
from pathlib import Path
from flask_login import current_user

from .models import Unit, Personnel, Personnel_status, User


def retrieve_personnel_list(fmw_id, clearance=100, query_all=False):
    if query_all == True and clearance <= 2:
        return Personnel.query.all()
    # subquery = Fmw.query.filter_by(name=fmw).first()
    return Personnel.query.filter_by(fmw_id=fmw_id).all()


def retrieve_personnel_statuses(db, fmw_id, date, clearance=100, missing_status_needed=True, query_all=False):
    if clearance <= 2 and query_all == True:
        # query all
        personnel_statuses = db.session.query(Personnel_status).filter(
            Personnel_status.date == date, Personnel.id == Personnel_status.personnel_id, Personnel.active == True).all()

        if missing_status_needed == True:
            subquery = db.session.query(Personnel.id).join(Personnel_status,
                                                           Personnel.id == Personnel_status.personnel_id).filter(
                                                           Personnel_status.date == date)
            missing_status = db.session.query(Personnel).filter(
                Personnel.id.notin_(subquery), Personnel.active == True).all()

    else:
        personnel_statuses = db.session.query(Personnel_status).filter(
            Personnel_status.date == date, Personnel.id == Personnel_status.personnel_id,
            Personnel.fmw_id == fmw_id, Personnel.active == True).all()

        if missing_status_needed == True:
            subquery = db.session.query(Personnel.id).join(Personnel_status,
                                                           Personnel.id == Personnel_status.personnel_id).filter(
                                                           Personnel_status.date == date)
            missing_status = db.session.query(Personnel).filter(Personnel.id.notin_(subquery),
                                                                Personnel.fmw_id == fmw_id,
                                                                Personnel.active == True).all()

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
            group_list.extend(
                (group.id, "{} - {}".format(unit.name, group.name))
                for group in unit.fmw)
            print(group_list)

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
        fieldnames = ['fmw', 'Name', 'Rank', 'Am status',
                      'Am Remarks', 'Pm status', 'Pm Remarks']
        csvwriter = DictWriter(csvfile, fieldnames=fieldnames)
        csvwriter.writeheader()
        for record in records:
            csvwriter.writerow({'fmw': record.person.fmw, 'Name': record.person.name, 'Rank': record.person.rank,
                                'Am status': record.am_status, 'Am Remarks': record.am_remarks,
                                'Pm status': record.pm_status, 'Pm Remarks': record.pm_remarks})

    if Path(new_file_path).is_file():
        return None
    return 'File not created'

# def generate_PS_excel(dates):
#     import xlsxwriter

#     # Create a workbook and add a worksheet.
#     workbook = xlsxwriter.Workbook('Expenses01.xlsx')
#     worksheet = workbook.add_worksheet()
#     date1=date2=date3=date4=date5='2020-01-01'
#     header1 = ['fmw', 'Rank', 'Name']
#     header2 = [date1,date2,date3,date4,date5]
    
#     for field in header:
#         worksheet.write(0, 0, field)
#         col + 1
    
#     worksheet.merge_range('D1:E1', date1)
#     worksheet.merge_range('F1:G1', date1)
#     worksheet.merge_range('H1:I1', date1)
#     worksheet.merge_range('J1:K1', date1)
#     worksheet.merge_range('L1:N1', date1)

#     # Start from the cell below header. Rows and columns are zero indexed.
#     row = 1
#     col = 3
#     for i in range(5):
#         worksheet.write(1, col, 'AM')
#         worksheet.write(1, col+1, 'AM')
#         col + 2

#     for date in dates:
#         # get records to write
#         records = Personnel_status.query.filter(date=date).all()
#         # write data
#         row = 2
#         col = 0
#         for record in records:
#             worksheet.write(row, col, record.fmw.name)
#             worksheet.write(row, col+1, record.rank)
#             worksheet.write(row, col+2, record.name)
#             # write per date
        

