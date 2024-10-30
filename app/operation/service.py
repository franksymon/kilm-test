from sqlmodel import Session, select, func
from fastapi_pagination.ext.sqlmodel import paginate
from fastapi_pagination import Params


# Config
from app.core.security import verify_password, hash_password

# Utils
from app.utils.responses import ResponseHandler

# Models
from app.operation.model import OperationStatus, OperationEntity

def get_all_operation(db: Session, params: Params):
    query = select(OperationEntity)
    return paginate(db, query, params)

def get_all_state_operation(db: Session, params: Params):
    query = select(OperationStatus)
    return paginate(db, query, params)  

def get_operation_by_id(db: Session, id: int):
    operation = db.get(OperationEntity, id)
    if not operation:
        raise ResponseHandler.not_found_error("Operation", id)
    return operation

def update_operation(db: Session, operation: OperationEntity):

    db_operation = db.get(OperationEntity, operation.id)
    if not db_operation:
        raise ResponseHandler.not_found_error("Operation", operation.id)
    
    if operation.title:
        db_operation.title = operation.title
    if operation.description:
        db_operation.description = operation.description
    if operation.annual_interest:
        db_operation.annual_interest = operation.annual_interest
    if operation.deadline:
        db_operation.deadline = operation.deadline        
    if operation.is_closed:
        db_operation.is_closed = operation.is_closed

    db_operation.updated_by = "user_test"
    db_operation.time_updated = func.now()
    db.add(db_operation)
    db.commit() 
    db.refresh(db_operation)    
    return db_operation

def delete_operation(db: Session, id: int):
    operation = db.get(OperationEntity, id)
    if not operation:
        raise ResponseHandler.not_found_error("Operation", id)
    db.delete(operation)
    db.commit()
    return ResponseHandler.delete_success("Operation", id, operation)



def create_operation(db: Session, operation: OperationEntity):

    operation_exists = db.exec(select(OperationEntity).where(OperationEntity.title == operation.title)).first()
    if operation_exists:
        raise ResponseHandler.already_exist_error("Operation", operation_exists.id)
    
    db_operation = OperationEntity.model_validate(operation, update={"created_by": "user_test"})
    
    db.add(db_operation)
    db.commit()
    db.refresh(db_operation)
    return db_operation

def create_state_operation(db: Session, state_operation: OperationStatus):
    
    state_operation_exists = db.exec(select(OperationStatus).where(OperationStatus.name == state_operation.name)).first()
    if state_operation_exists:
        raise ResponseHandler.already_exist_error("State Operation", state_operation_exists.id)

    db_state_operation = OperationStatus.model_validate(state_operation, update={"created_by": "user_test"})    
    db.add(db_state_operation) 
    db.commit()
    db.refresh(db_state_operation) 
    return db_state_operation

def get_state_operation_by_id(db: Session, id: int):
    state_operation = db.get(OperationStatus, id)
    if not state_operation:
        raise ResponseHandler.not_found_error("State Operation", id)
    return state_operation

def update_state_operation(db: Session, state_operation: OperationStatus):

    db_state_operation = db.get(OperationStatus, state_operation.id)
    if not db_state_operation:
        raise ResponseHandler.not_found_error("State Operation", state_operation.id)
    
    if state_operation.name:
        db_state_operation.name = state_operation.name
    if state_operation.description:
        db_state_operation.description = state_operation.description

    db_state_operation.updated_by = "user_test"
    db_state_operation.time_updated = func.now()

    db.add(db_state_operation)
    db.commit() 
    db.refresh(db_state_operation)    
    return db_state_operation

def delete_state_operation(db: Session, id: int):
    state_operation = db.get(OperationStatus, id)
    if not state_operation:
        raise ResponseHandler.not_found_error("State Operation", id)
    db.delete(state_operation)
    db.commit()
    return ResponseHandler.delete_success("State Operation", id, state_operation)