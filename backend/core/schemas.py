from pydantic import BaseModel, Field
class UserScoreInput(BaseModel):
    target_univ: str
    target_dept: str
    my_eng_score: float = Field(..., ge=0, le=100)
    my_math_score: float = Field(..., ge=0, le=100)
    my_gpa: float = Field(..., ge=0, le=4.5)
class PredictionOutput(BaseModel):
    university: str
    department: str
    calculated_score: float
    admission_probability: str
    comment: str