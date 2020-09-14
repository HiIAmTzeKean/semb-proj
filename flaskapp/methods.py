import os
from csv import writer, DictWriter
from datetime import date


def converter_paradestateform(rows):
    names = [] 
    for row in rows:
        names.append((row["id"], row["name"]))
    return names


def retrieve_personnel_list(db, fmw):
    query = db.execute(
             'SELECT * FROM personnel WHERE fmw = ?', (fmw,)
         ).fetchall()
    return query


def retrieve_member_statuses(db, grp, date, time):
    """
    Retrieve statuses of members at the particular date and time
    grp: Group Name of Personnel (fmw)
    time: AM or PM
    """
    # retrieve members
    personnel_names = retrieve_personnel_list(db, grp)

    """
    The following SQL query does the following:
    - filters by fmw, date and time
    - for every personnel, find all status records, and take the latest record ID
    """
    latest_updates_sql = """
    SELECT personnel.id, personnel.rank, personnel.name, personnel_status.status, personnel_status.remarks 
    FROM personnel_status, personnel
    WHERE (personnel.id, personnel_status.id) IN (
        SELECT personnel.id, MAX(personnel_status.id) FROM personnel_status
        JOIN personnel ON personnel.id = personnel_status.personnel_id
        WHERE personnel.fmw = ? AND personnel_status.date = ? AND personnel_status.time = ?
        GROUP BY personnel.id
    )
    ORDER BY personnel.id
    """

    latest_updates = db.execute(latest_updates_sql, (grp, date, time)).fetchall()

    # The above query only retrieves information of personnel that has submitted their status
    # This list needs to be cross-checked with the original personnel list
    # to retrieve the full member list and their respective statuses (if any)
    personnel_statuses = []  # will using pandas be better?
    latest_updates_ptr = 0
    for personnel in personnel_names:
        if latest_updates_ptr < len(latest_updates) and latest_updates[latest_updates_ptr]['id'] == personnel['id']:
            row = latest_updates[latest_updates_ptr]
            personnel_statuses.append((row['id'], row['rank'], row['name'], row['status'], row['remarks']))
            latest_updates_ptr += 1
        else:
            personnel_statuses.append((personnel['id'], personnel['rank'], personnel['name'], None, None))

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
