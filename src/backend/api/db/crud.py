from sqlalchemy.orm import Session
from . import models, schemas

def create_code_with_output(db: Session, code_with_execution: schemas.CodeWithCodeExecutionResultCreate):
    db_code = models.CodeWithCodeExecutionResult(content=code_with_execution.content, output=code_with_execution.output)
    db.add(db_code)
    db.commit()
    db.refresh(db_code)
    return db_code


# def get_code(db: Session, code_id: int):
#     return db.query(models.Code).filter(models.Code.id == code_id).first()

# def get_codes(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Code).offset(skip).limit(limit).all()

# def create_code(db: Session, code: schemas.CodeCreate):
#     db_code = models.Code(content=code.content)
#     db.add(db_code)
#     db.commit()
#     db.refresh(db_code)
#     return db_code

# def get_code_execution_result(db: Session, result_id: int):
#     return db.query(models.CodeExecutionResult).filter(models.CodeExecutionResult.id == result_id).first()

# def get_code_execution_results(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.CodeExecutionResult).offset(skip).limit(limit).all()

# def create_code_execution_result(db: Session, result: schemas.CodeExecutionResultCreate, code_id: int):
#     db_result = models.CodeExecutionResult(result=result.result, code_id=code_id)
#     db.add(db_result)
#     db.commit()
#     db.refresh(db_result)
#     return db_result
