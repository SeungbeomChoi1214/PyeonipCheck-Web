#!/bin/bash

# 편입 합격 예측 시스템 배포 스크립트
# AWS Lightsail 인스턴스용

set -e  # 에러 발생 시 스크립트 중단

echo "🚀 편입 합격 예측 시스템 배포 시작..."

# 1. 시스템 업데이트
echo "📦 시스템 패키지 업데이트..."
sudo apt update && sudo apt upgrade -y

# 2. 필수 패키지 설치
echo "🔧 필수 패키지 설치..."
sudo apt install -y python3 python3-pip python3-venv nodejs npm nginx

# 3. 프로젝트 디렉토리 설정
PROJECT_DIR="/opt/transfer-prediction"
sudo mkdir -p $PROJECT_DIR
sudo chown $USER:$USER $PROJECT_DIR
cd $PROJECT_DIR

# 4. Python 가상환경 설정
echo "🐍 Python 가상환경 설정..."
python3 -m venv venv
source venv/bin/activate

# 5. Python 의존성 설치
echo "📚 Python 의존성 설치..."
pip install -r requirements.txt

# 6. 데이터베이스 초기화
echo "🗄️ 데이터베이스 초기화..."
python init_db_data.py

# 7. 프론트엔드 빌드
echo "⚛️ React 앱 빌드..."
cd frontend
npm install
npm run build
cd ..

# 8. Nginx 설정
echo "🌐 Nginx 설정..."
sudo tee /etc/nginx/sites-available/transfer-prediction > /dev/null <<EOF
server {
    listen 80;
    server_name _;

    # React 정적 파일 서빙
    location / {
        root $PROJECT_DIR/frontend/build;
        index index.html index.htm;
        try_files \$uri \$uri/ /index.html;
    }

    # API 프록시
    location /api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Nginx 사이트 활성화
sudo ln -sf /etc/nginx/sites-available/transfer-prediction /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl reload nginx

# 9. Systemd 서비스 설정 (백엔드)
echo "⚙️ 백엔드 서비스 설정..."
sudo tee /etc/systemd/system/transfer-prediction.service > /dev/null <<EOF
[Unit]
Description=Transfer Prediction FastAPI
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$PROJECT_DIR
Environment=PATH=$PROJECT_DIR/venv/bin
ExecStart=$PROJECT_DIR/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# 10. 서비스 시작
echo "🎬 서비스 시작..."
sudo systemctl daemon-reload
sudo systemctl enable transfer-prediction
sudo systemctl start transfer-prediction
sudo systemctl enable nginx
sudo systemctl start nginx

# 11. 방화벽 설정
echo "🔥 방화벽 설정..."
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable

# 12. 상태 확인
echo "✅ 배포 완료! 서비스 상태 확인..."
echo "📊 백엔드 서비스 상태:"
sudo systemctl status transfer-prediction --no-pager -l

echo "🌐 Nginx 상태:"
sudo systemctl status nginx --no-pager -l

echo "🎉 배포 완료!"
echo "🔗 웹사이트: http://$(curl -s ifconfig.me)"
echo "🔗 API 문서: http://$(curl -s ifconfig.me)/api/docs"

# 13. 로그 확인 명령어 안내
echo ""
echo "📋 유용한 명령어:"
echo "  백엔드 로그: sudo journalctl -u transfer-prediction -f"
echo "  Nginx 로그: sudo tail -f /var/log/nginx/access.log"
echo "  서비스 재시작: sudo systemctl restart transfer-prediction"