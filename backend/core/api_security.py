# API 레벨 방어 미들웨어 (api_security.py)

from fastapi import Request, HTTPException
from sqlalchemy.orm import Session
from functools import wraps
import logging
from typing import Dict, Any

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataIntegrityMiddleware:
    """데이터 무결성 검증 미들웨어"""
    
    def __init__(self):
        self.suspicious_patterns = [
            "SELECT", "DROP", "DELETE", "UPDATE", "INSERT",  # SQL Injection 방지
            "<script>", "javascript:", "onload=",  # XSS 방지
        ]
    
    def validate_request_data(self, data: Dict[str, Any]) -> bool:
        """요청 데이터 검증"""
        for key, value in data.items():
            if isinstance(value, str):
                for pattern in self.suspicious_patterns:
                    if pattern.lower() in value.lower():
                        logger.warning(f"Suspicious pattern detected: {pattern} in {key}")
                        return False
        return True

def verify_department_ownership(db: Session, dept_id: int, univ_id: int) -> bool:
    """학과-대학 소유권 검증"""
    from backend.models import Department
    
    dept = db.query(Department).filter(
        Department.id == dept_id,
        Department.university_id == univ_id
    ).first()
    
    if not dept:
        logger.error(f"Department ownership verification failed: dept_id={dept_id}, univ_id={univ_id}")
        return False
    
    return True

def rate_limit_check(request: Request) -> bool:
    """간단한 Rate Limiting (Redis 없이)"""
    client_ip = request.client.host
    
    # 실제 구현에서는 Redis나 메모리 캐시 사용
    # 여기서는 기본적인 체크만
    if hasattr(request.app.state, 'request_counts'):
        count = request.app.state.request_counts.get(client_ip, 0)
        if count > 100:  # 분당 100회 제한
            return False
        request.app.state.request_counts[client_ip] = count + 1
    else:
        request.app.state.request_counts = {client_ip: 1}
    
    return True

# 데코레이터 방식 검증
def validate_department_access(func):
    """학과 접근 권한 검증 데코레이터"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # FastAPI에서 의존성 주입된 db와 request 파라미터 찾기
        db = None
        request_data = None
        
        for arg in args:
            if isinstance(arg, Session):
                db = arg
            elif hasattr(arg, 'dept_id'):
                request_data = arg
        
        if db and request_data:
            # 학과 존재 여부 검증
            from backend.models import Department
            dept = db.query(Department).filter(Department.id == request_data.dept_id).first()
            
            if not dept:
                raise HTTPException(status_code=404, detail="Department not found")
            
            if not dept.is_active:
                raise HTTPException(status_code=400, detail="Department is not active")
            
            # 대학-학과 관계 검증 (요청에 university_id가 있는 경우)
            if hasattr(request_data, 'university_id') and request_data.university_id:
                if dept.university_id != request_data.university_id:
                    raise HTTPException(
                        status_code=400, 
                        detail="Department does not belong to specified university"
                    )
        
        return await func(*args, **kwargs)
    return wrapper

# 실시간 데이터 검증
class RealTimeValidator:
    """실시간 데이터 검증 클래스"""
    
    @staticmethod
    def validate_university_department_pair(db: Session, univ_id: int, dept_id: int) -> Dict[str, Any]:
        """대학-학과 쌍 검증"""
        from backend.models import University, Department
        
        # 1. 대학 존재 확인
        university = db.query(University).filter(University.id == univ_id).first()
        if not university:
            return {"valid": False, "error": "University not found", "code": "UNIV_NOT_FOUND"}
        
        # 2. 학과 존재 확인
        department = db.query(Department).filter(Department.id == dept_id).first()
        if not department:
            return {"valid": False, "error": "Department not found", "code": "DEPT_NOT_FOUND"}
        
        # 3. 관계 검증
        if department.university_id != univ_id:
            return {
                "valid": False, 
                "error": f"Department {department.name} does not belong to {university.name}",
                "code": "RELATIONSHIP_MISMATCH",
                "details": {
                    "expected_university": university.name,
                    "actual_university_id": department.university_id
                }
            }
        
        # 4. 활성 상태 확인
        if not department.is_active:
            return {
                "valid": False,
                "error": f"Department {department.name} is not active",
                "code": "DEPT_INACTIVE"
            }
        
        return {
            "valid": True,
            "university": {"id": university.id, "name": university.name},
            "department": {"id": department.id, "name": department.name, "division": department.division}
        }
    
    @staticmethod
    def log_suspicious_activity(request: Request, error_code: str, details: Dict[str, Any]):
        """의심스러운 활동 로깅"""
        logger.warning(f"Suspicious activity detected: {error_code}", extra={
            "client_ip": request.client.host,
            "user_agent": request.headers.get("user-agent"),
            "details": details,
            "timestamp": datetime.utcnow().isoformat()
        })

# 사용 예시
"""
# main.py에서 사용

@app.post("/predict")
@validate_department_access
async def predict_admission(request: PredictRequest, db: Session = Depends(get_db)):
    # 이미 검증된 상태로 로직 실행
    ...

# 또는 수동 검증
@app.post("/predict")
async def predict_admission(request: PredictRequest, db: Session = Depends(get_db)):
    validation_result = RealTimeValidator.validate_university_department_pair(
        db, request.university_id, request.dept_id
    )
    
    if not validation_result["valid"]:
        raise HTTPException(status_code=400, detail=validation_result["error"])
    
    # 검증된 데이터로 로직 실행
    ...
"""