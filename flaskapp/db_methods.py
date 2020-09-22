def update_PS(db,personnel_id, status_date, am_status, am_remarks, pm_status, pm_remarks):
    # assume that record already exist
    db.execute("""
    UPDATE "personnel_status"
    SET am_status = ?, am_remarks = ?, pm_status = ?, pm_remarks = ?
    WHERE personnel_id = ? AND date = ?
    """, (am_status, am_remarks, pm_status, pm_remarks,  personnel_id, status_date))
    db.commit()


def insert_PS(db,personnel_id, status_date, am_status, am_remarks, pm_status, pm_remarks):
    db.execute('''INSERT INTO personnel_status
            (personnel_id, date, am_status, am_remarks, pm_status, pm_remarks)
            VALUES (?,?,?,?,?,?)''',
            (personnel_id, status_date, am_status, am_remarks, pm_status, pm_remarks))
    db.commit()


def retrive_record_by_date(db,personnel_id,status_date):
    record = db.execute("""
    SELECT personnel.name, personnel_status.date, personnel_status.am_status,
    personnel_status.am_remarks, personnel_status.pm_status, personnel_status.pm_remarks
    FROM personnel JOIN personnel_status ON personnel.id = personnel_status.personnel_id
    WHERE personnel.id = ? AND personnel_status.date = ?
    """, (personnel_id, status_date)).fetchone()
    if record: return record
    return None


def retrive_personnel_id(db,name,fmw,rank=""):
    if rank != "":
        record = db.execute("""
        SELECT personnel.id
        FROM personnel
        WHERE name = ? AND fmw = ? AND rank = ?
        """, (name,fmw,rank)).fetchone()
    else:
        record = db.execute("""
        SELECT personnel.id
        FROM personnel
        WHERE name = ? AND fmw = ?
        """, (name,fmw)).fetchone()
    if record:
        return record['id']
    return None


def retrive_one_record(db,name,fmw):
    record = db.execute("""
    SELECT *
    FROM personnel
    WHERE name = ? AND fmw = ?
    """, (name,fmw)).fetchone()
    if record: return record
    return None


def check_personnel_exist(db,name,fmw,rank):
    record = db.execute("""SELECT * FROM personnel 
    WHERE personnel.name = ? AND personnel.rank = ?""", (name,rank)).fetchone()
    if record:
        record2= db.execute("""SELECT * FROM personnel 
        WHERE personnel.name = ? AND personnel.rank = ? AND personnel.fmw = ?""", (name,rank,fmw)).fetchone()
        if record2:
            return None
        else:
            return "User exist in the system, but you do not have admin rights over user."
    else:
        return "User does not exist in the system. Please check rank and name."

def add_personnel_db(db,name,fmw,rank):
    try:
        db.execute("""
        INSERT INTO personnel (name,fmw,rank) VALUES (?,?,?)
        """, (name,fmw,rank))
        db.commit()
        return None
    except e as error:
        return e


def del_personnel_db(db,name,fmw):
    try:
        personnel_id = retrive_personnel_id(db,name,fmw)
        db.execute("""DELETE FROM personnel_status WHERE id = ?""", (personnel_id,))
        db.execute("""DELETE FROM personnel WHERE id = ?""", (personnel_id,))
        db.commit()
        return None
    except e as error:
        return e


def act_deact_personnel_db(db,active,name,fmw):
    personnel_id = retrive_personnel_id(db,name,fmw)
    db.execute("""UPDATE personnel SET active = ? 
    WHERE personnel.id = ?
    """, (active,personnel_id))
    db.commit()