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
        record = Personnel.query.filter_by(name=name,fmw=fmw,rank=rank).first()
    else:
        record = Personnel.query.filter_by(name=name,fmw=fmw).first()
    if record:
        return record.id
    return None


def retrive_one_record(db,name,fmw,rank=''):
    if rank != "":
        record = Personnel.query.filter_by(name=name,fmw=fmw,rank=rank).first()
    else:
        record = Personnel.query.filter_by(name=name,fmw=fmw).first()
    if record: return record
    return None


def check_personnel_exist(db,name,fmw,rank):
    record = Personnel.query.filter_by(name=name,rank=rank).first()
    if record:
        record2 = Personnel.query.filter_by(name=name,rank=rank,fmw=fmw).first()
        if record2:
            return None
        else:
            return "User exist in the system, but you do not have admin rights over user."
    else:
        return "User does not exist in the system. Please check rank and name."


def add_del_check(db,add_del,name,fmw,rank):
    """Does inital check for Add/Del

    Args:
        db ([type]): [description]
        name ([type]): [description]
        fmw ([type]): [description]
        rank ([type]): [description]
        add_del ([type]): [description]

    Returns:
        Boolean,
        Error: [Error message] OR
        record: [Personnel Queried]
    """
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
        db.session.add(Personnel(rank,name,fmw,fmd))
    else:
        personnel_record = Personnel.query.filter_by(name=name,rank=rank,fmw=fmw).first()
        status_records = Personnel_status.query.filter(Personnel_status.personnel_id==personnel_record.id).all()
        db.session.delete(status_records)
        db.session.delete(personnel_record)
    db.session.commit()
    return None, output


def act_deact_personnel_db(db,active,rank,name,fmw,fmd):
    record = db.session.query(Personnel).filter(Personnel.rank==rank,Personnel.name==name,Personnel.fmw==fmw,Personnel.fmd==fmd).first()
    record.active = active
    db.session.commit()
