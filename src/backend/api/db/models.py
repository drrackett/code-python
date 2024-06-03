from sqlalchemy import Column, Integer, String

from .database import Base


class CodeWithCodeExecutionResult(Base):
    __tablename__ = "codes"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    output = Column(String, index=True)


# class Code(Base):
#     __tablename__ = "codes"

#     id = Column(Integer, primary_key=True, index=True)
#     content = Column(String, index=True)
#     output_id = Column(Integer, ForeignKey('code_execution_results.id'), unique=True)
#     output = relationship("CodeExecutionResult", back_populates="code", uselist=False)


# class CodeExecutionResult(Base):
#     __tablename__ = "code_execution_results"

#     id = Column(Integer, primary_key=True, index=True)
#     result = Column(String, index=True)
#     code_id = Column(Integer, ForeignKey('codes.id'), unique=True)

#     code = relationship("Code", back_populates="output")
