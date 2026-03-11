# 🚀 AWS Lightsail 배포 가이드

## 📋 배포 전 준비사항

### 1. 로컬 환경 설정
```bash
# .env 파일 설정 확인
cp .env.example .env
# DATABASE_URL, ALLOWED_ORIGINS, TOP_UNIVERSITIES 설정

# 의존성 설치
pip install -r requirements.txt
npm install --prefix frontend
```

### 2. 데이터 검증
```bash
# 로컬에서 데이터 생성 테스트
python init_db_data.py

# 서버 실행 테스트
python main.py
cd frontend && npm start
```

## 🌐 AWS Lightsail 배포

### 1. 인스턴스 생성
- **OS**: Ubuntu 20.04 LTS
- **플랜**: $10/월 (2GB RAM, 1 vCPU)
- **고정 IP**: 할당 권장

### 2. 파일 업로드
```bash
# 로컬에서 서버로 파일 전송
scp -r . ubuntu@YOUR_IP:/tmp/transfer-prediction
```

### 3. 배포 스크립트 실행
```bash
# 서버 접속
ssh ubuntu@YOUR_IP

# 파일 이동 및 권한 설정
sudo mv /tmp/transfer-prediction /opt/
sudo chown -R ubuntu:ubuntu /opt/transfer-prediction
cd /opt/transfer-prediction

# 배포 스크립트 실행
chmod +x deploy.sh
./deploy.sh
```

## 🔧 환경별 설정

### 개발 환경 (.env)
```env
DATABASE_URL=sqlite:///./university.db
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
ENVIRONMENT=development
```

### 프로덕션 환경 (.env)
```env
DATABASE_URL=sqlite:///./university.db
ALLOWED_ORIGINS=https://your-domain.com,http://your-ip
ENVIRONMENT=production
TOP_UNIVERSITIES=서울대학교,연세대학교,고려대학교,성균관대학교,한양대학교,중앙대학교,경희대학교,한국외국어대학교,서강대학교,이화여자대학교,건국대학교,동국대학교,홍익대학교,숙명여자대학교,세종대학교,단국대학교,가천대학교,인하대학교,아주대학교,명지대학교
```

## 📊 서비스 관리

### 상태 확인
```bash
# 백엔드 서비스 상태
sudo systemctl status transfer-prediction

# Nginx 상태
sudo systemctl status nginx

# 로그 확인
sudo journalctl -u transfer-prediction -f
```

### 서비스 제어
```bash
# 서비스 재시작
sudo systemctl restart transfer-prediction
sudo systemctl restart nginx

# 서비스 중지
sudo systemctl stop transfer-prediction

# 서비스 시작
sudo systemctl start transfer-prediction
```

### 업데이트 배포
```bash
# 코드 업데이트 후
cd /opt/transfer-prediction

# 백엔드 업데이트
git pull  # 또는 파일 업로드
sudo systemctl restart transfer-prediction

# 프론트엔드 업데이트
cd frontend
npm run build
sudo systemctl reload nginx
```

## 🔒 보안 설정

### SSL 인증서 (Let's Encrypt)
```bash
# Certbot 설치
sudo apt install certbot python3-certbot-nginx

# SSL 인증서 발급
sudo certbot --nginx -d your-domain.com

# 자동 갱신 설정
sudo crontab -e
# 추가: 0 12 * * * /usr/bin/certbot renew --quiet
```

### 방화벽 설정
```bash
# 현재 설정 확인
sudo ufw status

# 필요한 포트만 열기
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
```

## 📈 모니터링

### 시스템 리소스
```bash
# CPU, 메모리 사용률
htop

# 디스크 사용량
df -h

# 네트워크 상태
netstat -tlnp
```

### 애플리케이션 로그
```bash
# 실시간 로그 모니터링
sudo journalctl -u transfer-prediction -f

# 에러 로그만 확인
sudo journalctl -u transfer-prediction --since "1 hour ago" -p err
```

## 🚨 트러블슈팅

### 일반적인 문제들

1. **서비스가 시작되지 않음**
   ```bash
   sudo journalctl -u transfer-prediction -n 50
   ```

2. **데이터베이스 오류**
   ```bash
   cd /opt/transfer-prediction
   python init_db_data.py
   ```

3. **Nginx 설정 오류**
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

4. **포트 충돌**
   ```bash
   sudo netstat -tlnp | grep :8000
   sudo kill -9 PID
   ```

## 📞 지원

배포 관련 문제 발생 시:
1. 로그 파일 확인
2. 시스템 리소스 확인
3. 네트워크 연결 확인
4. 환경 변수 설정 확인

🎉 **배포 완료 후 접속 URL**: `http://YOUR_IP` 또는 `https://your-domain.com`