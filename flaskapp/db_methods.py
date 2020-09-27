from .models import Personnel, Personnel_status, User


def update_PS(db,personnel_id, date, am_status, am_remarks, pm_status, pm_remarks):
    db.session.query(Personnel_status).filter(Personnel_status.personnel_id==personnel_id,Personnel_status.date==date).update(
        {Personnel_status.am_status:am_status, Personnel_status.am_remarks:am_remarks,
        Personnel_status.pm_status:pm_status, Personnel_status.pm_remarks:pm_remarks}, synchronize_session = False)
    db.session.commit()


def insert_PS(db,personnel_id, date, am_status, am_remarks, pm_status, pm_remarks):
    status = Personnel_status(date, am_status, am_remarks, pm_status, pm_remarks, personnel_id )
    db.session.add(status)
    db.session.commit()


def retrive_record_by_date(db,personnel_id,date):
    if personnel_id == None or personnel_id == '' or personnel_id == []:
        return None
    record = Personnel_status.query.filter(Personnel_status.personnel_id==personnel_id,Personnel_status.date==date).first()
    if record: return record
    return None


def submit_PS(db,personnel_id, date, am_status, am_remarks, pm_status, pm_remarks):
    if retrive_record_by_date(db, personnel_id, date):
        update_PS(db, personnel_id, date, am_status, am_remarks, pm_status, pm_remarks)
    else:
        insert_PS(db, personnel_id, date, am_status, am_remarks, pm_status, pm_remarks)


def retrive_personnel_id(db,name,fmw,rank=""):
    if rank != "":
        # record = db.execute("""
        # SELECT personnel.id
        # FROM personnel
        # WHERE name = ? AND fmw = ? AND rank = ?
        # """, (name,fmw,rank)).fetchone()
        record = Personnel.query.filter_by(name=name,fmw=fmw,rank=rank).first()
    else:
        # record = db.execute("""
        # SELECT personnel.id
        # FROM personnel
        # WHERE name = ? AND fmw = ?
        # """, (name,fmw)).fetchone()
        record = Personnel.query.filter_by(name=name,fmw=fmw).first()
    if record:
        return record.id
    return None


def retrive_one_record(db,name,fmw,rank=''):
    # record = db.execute("""
    # SELECT *
    # FROM personnel
    # WHERE name = ? AND fmw = ?
    # """, (name,fmw)).fetchone()
    if rank != "":
        record = Personnel.query.filter_by(name=name,fmw=fmw,rank=rank).first()
    else:
        record = Personnel.query.filter_by(name=name,fmw=fmw).first()
    if record: return record
    return None


def check_personnel_exist(db,name,fmw,rank):
    # record = db.execute("""SELECT * FROM personnel 
    # WHERE personnel.name = ? AND personnel.rank = ?""", (name,rank)).fetchone()
    record = Personnel.query.filter_by(name=name,rank=rank).first()
    if record:
        # record2= db.execute("""SELECT * FROM personnel 
        # WHERE personnel.name = ? AND personnel.rank = ? AND personnel.fmw = ?""", (name,rank,fmw)).fetchone()
        record2 = Personnel.query.filter_by(name=name,rank=rank,fmw=fmw).first()
        if record2:
            return None
        else:
            return "User exist in the system, but you do not have admin rights over user."
    else:
        return "User does not exist in the system. Please check rank and name."


def add_del_check(db,name,fmw,rank,add_del):
    '''
    returns (check_status,record)
    if check is valid, personnel record will be returned
    else an error message will be returned
    '''
    # record = db.execute("""SELECT * FROM personnel 
    # WHERE personnel.name = ? AND personnel.rank = ? AND personnel.fmw = ?""", (name,rank,fmw)).fetchone()
    record = Personnel.query.filter_by(name=name,rank=rank,fmw=fmw).first()
    if add_del == 'Add':
        if record:
            return False, "Personnel already exist in your FMW!"
        else: return True, record
    else:
        if record: return True, record
        else:
            return False, "Personnel does not exist in your FMW!"


def add_del_personnel_db(db, add_del, rank, name, fmw, fmd=93):
    '''
    Output will return (error,personnel)
    if error, personnel will be blank as he does not exist
    else error will be none and valid personnel will be returned
    '''
    check, output = add_del_check(db,name,fmw,rank,add_del)
    if check == False:
        return output,''
    if add_del == 'Add':
        # db.execute("""INSERT INTO personnel (name,fmw,rank) VALUES (?,?,?)""", (name,fmw,rank))
        db.session.add(Personnel(rank,name,fmw,fmd))
    else:
        # personnel_id = retrive_personnel_id(db,name,fmw)
        # db.execute("""DELETE FROM personnel_status WHERE id = ?""", (personnel_id,))
        # db.execute("""DELETE FROM personnel WHERE id = ?""", (personnel_id,))
        personnel_record = Personnel.query.filter_by(name=name,rank=rank,fmw=fmw).first()
        status_records = Personnel_status.query.filter(Personnel_status.personnel_id==personnel_record.id).all()
        db.session.delete(status_records)
        db.session.delete(personnel_record)
    db.session.commit()
    return None, output


def act_deact_personnel_db(db,active,rank,name,fmw):
    # personnel_id = retrive_personnel_id(db,name,fmw)
    # db.execute("""UPDATE personnel SET active = ? 
    # WHERE personnel.id = ?
    # """, (active,personnel_id))
    db.session.query(Personnel).filter(Personnel.rank==rank,Personnel.name==name,Personnel.fmw==fmw).update(
        {Personnel.active:active}, synchronize_session = False)
    db.session.commit()
