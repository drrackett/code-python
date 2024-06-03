from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from src.backend.api.db import crud, models, schemas
from src.backend.api.db.database import SessionLocal, engine

from src.libs.utils import run_container

# Drop all tables (THIS SHOULD BE REMOVED)
models.Base.metadata.drop_all(bind=engine)

# Recreate all tables
models.Base.metadata.create_all(bind=engine)

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/codes/submit", response_model=schemas.CodeWithCodeExecutionResult, status_code=201)
def create_and_execute_code(code: schemas.CodeExecutionResultCreate, db: Session = Depends(get_db)):    
    # Run the code to get the result
    result_output = run_container(code.content)

    if result_output["error"]:
        # If there is an error, return the error output with a 400 status code
        raise HTTPException(status_code=400, detail=result_output["error"])

    # Form the combined schema object
    code_with_execution = schemas.CodeWithCodeExecutionResultCreate(content=code.content, output=result_output["output"])

    return crud.create_code_with_output(db=db, code_with_execution=code_with_execution)


# @router.post("/codes/", response_model=schemas.Code)
# def create_code(code: schemas.CodeCreate, db: Session = Depends(get_db)):
#     return crud.create_code(db=db, code=code)


# @router.get("/codes/", response_model=list[schemas.Code])
# def read_codes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     codes = crud.get_codes(db, skip=skip, limit=limit)
#     return codes


# @router.get("/codes/{code_id}", response_model=schemas.Code)
# def read_code(code_id: int, db: Session = Depends(get_db)):
#     db_code = crud.get_code(db, code_id=code_id)
#     if db_code is None:
#         raise HTTPException(status_code=404, detail="Code not found")
#     return db_code


# @router.post("/codes/{code_id}/results/", response_model=schemas.CodeExecutionResult)
# def create_code_execution_result_for_code(
#     code_id: int, result: schemas.CodeExecutionResultCreate, db: Session = Depends(get_db)
# ):
#     db_code = crud.get_code(db, code_id=code_id)
#     if db_code is None:
#         raise HTTPException(status_code=404, detail="Code not found")
#     return crud.create_code_execution_result(db=db, result=result, code_id=code_id)


# @router.get("/results/", response_model=list[schemas.CodeExecutionResult])
# def read_code_execution_results(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     results = crud.get_code_execution_results(db, skip=skip, limit=limit)
#     return results
