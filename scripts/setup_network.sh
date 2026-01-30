#!/bin/bash

echo "======================================================================"
echo "AarogyaQueue - Network Access Setup"
echo "======================================================================"

# Get IP address
IP=$(hostname -I | awk '{print $1}')
echo ""
echo "🌐 Your computer's IP address: $IP"
echo ""

# Create Streamlit config
echo "📝 Creating Streamlit network configuration..."
mkdir -p ~/.streamlit
cat > ~/.streamlit/config.toml << 'EOF'
[server]
headless = true
address = "0.0.0.0"
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
serverAddress = "0.0.0.0"
gatherUsageStats = false
EOF

echo "✅ Streamlit configured for network access"

# Check firewall status
echo ""
echo "🔥 Checking firewall..."
if command -v ufw &> /dev/null; then
    UFW_STATUS=$(sudo ufw status | grep -c "Status: active")
    if [ "$UFW_STATUS" -eq 1 ]; then
        echo "⚠️  Firewall is active. Opening ports 8501 and 8502..."
        sudo ufw allow 8501/tcp
        sudo ufw allow 8502/tcp
        echo "✅ Firewall rules added"
    else
        echo "✅ Firewall is inactive (no action needed)"
    fi
else
    echo "ℹ️  UFW not found (firewall may not be configured)"
fi

echo ""
echo "======================================================================"
echo "✅ SETUP COMPLETE!"
echo "======================================================================"
echo ""
echo "📱 Access from your tablet:"
echo ""
echo "   Patient Portal:  http://$IP:8501"
echo "   Doctor Portal:   http://$IP:8502"
echo ""
echo "🔧 Make sure:"
echo "   1. Tablet and computer are on the SAME Wi-Fi network"
echo "   2. Both devices can ping each other"
echo "   3. Run the apps with: bash scripts/run_network.sh"
echo ""
echo "======================================================================"
