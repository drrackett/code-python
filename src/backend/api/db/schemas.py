from pydantic import BaseModel
from typing import Optional, List


class CodeBase(BaseModel):
    content: str

class CodeExecutionResultCreate(CodeBase):
    pass

class CodeWithCodeExecutionResultBase(BaseModel):
    content: str
    output: str


class CodeWithCodeExecutionResultCreate(CodeWithCodeExecutionResultBase):
    pass


class CodeWithCodeExecutionResult(CodeWithCodeExecutionResultBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# class CodeBase(BaseModel):
#     content: str

# class CodeCreate(CodeBase):
#     pass

# class Code(CodeBase):
#     id: int
#     output_id: Optional[int]

#     class Config:
#         orm_mode = True

# class CodeExecutionResultBase(BaseModel):
#     result: str

# class CodeExecutionResultCreate(CodeExecutionResultBase):
#     pass

# class CodeExecutionResult(CodeExecutionResultBase):
#     id: int
#     code_id: int

#     class Config:
#         orm_mode = True