from pydantic import BaseModel

class LoginReq(BaseModel):
    password: str

class LoginRes(BaseModel):
    ok: bool

class CreateSessionReq(BaseModel):
    module_code: str

class CreateSessionRes(BaseModel):
    session_id: int

class StudentLookupRes(BaseModel):
    reg_no: str
    name: str
    index_no: str

class MarkAttendanceReq(BaseModel):
    reg_no: str
    token: str

class MarkAttendanceRes(BaseModel):
    status: str
