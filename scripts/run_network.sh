#!/bin/bash

# AarogyaQueue Network Launcher
# Runs both portals accessible from network (tablets/phones)

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Get IP address
IP=$(hostname -I | awk '{print $1}')

echo -e "${BLUE}"
cat << "EOF"
╔════════════════════════════════════════════╗
║       🏥 AarogyaQueue System Launcher      ║
║         Network Mode (Tablet Access)       ║
╚════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo "📂 Project Directory: $(pwd)"
echo ""

# Activate virtual environment
if [ -d "venv" ]; then
    echo -e "${GREEN}✓${NC} Activating virtual environment..."
    source venv/bin/activate
else
    echo -e "${YELLOW}⚠${NC} Virtual environment not found. Using system Python..."
fi

# Initialize database
echo -e "${GREEN}✓${NC} Initializing database..."
python3 scripts/setup_db.py

echo ""
echo "=== Network Access Information ==="
echo "Your IP Address: $IP"
echo "Patient Portal:  http://$IP:8501"
echo "Doctor Portal:   http://$IP:8502"
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🚀 Starting Applications...${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

echo ""
echo "📱 Patient Kiosk starting on http://$IP:8501"
echo "👨‍⚕️  Doctor Dashboard starting on http://$IP:8502"
echo ""

# Start patient app in background
streamlit run app/patient/app.py \
    --server.port=8501 \
    --server.address=0.0.0.0 \
    --server.headless=true \
    > /dev/null 2>&1 &
PATIENT_PID=$!

# Start doctor app in background
streamlit run app/doctor/app.py \
    --server.port=8502 \
    --server.address=0.0.0.0 \
    --server.headless=true \
    > /dev/null 2>&1 &
DOCTOR_PID=$!

# Wait for apps to start
sleep 3

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✓ System Ready!${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

echo ""
echo "  📱 Patient Portal:  http://$IP:8501"
echo "  👨‍⚕️  Doctor Portal:   http://$IP:8502"
echo ""
echo "  📶 Local Access:    http://localhost:8501"
echo "                     http://localhost:8502"
echo ""
echo "📋 Sample Credentials:"
echo "  Doctor Login: Role=SENIOR, PIN=1234"
echo "  Doctor Login: Role=JUNIOR, PIN=5678"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop all services${NC}"
echo ""

# Cleanup function
cleanup() {
    echo ""
    echo "Shutting down..."
    kill $PATIENT_PID 2>/dev/null
    kill $DOCTOR_PID 2>/dev/null
    exit 0
}

trap cleanup INT TERM

# Keep running
wait
