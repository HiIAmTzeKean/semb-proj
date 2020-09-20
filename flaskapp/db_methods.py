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

def retrive_one_record(db,personnel_id,status_date):
    record = db.execute("""
    SELECT date, am_status, am_remarks, pm_status, pm_remarks, name
    FROM personnel ,personnel_status
    WHERE personnel_id = ? AND date = ?
    """, (personnel_id, status_date)).fetchone()
    if record: return record
    return None