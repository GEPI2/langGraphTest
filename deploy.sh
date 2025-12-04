#!/bin/bash

# 1. Update system and install dependencies
sudo apt-get update
sudo apt-get install -y git docker.io docker-compose

# 2. Start Docker service
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# 3. Clone repository (if not already cloned)
if [ ! -d "langGraphTest" ]; then
    git clone https://github.com/GEPI2/langGraphTest.git
fi

cd langGraphTest

# 4. Pull latest changes
git pull

# 5. Create .env file (User needs to input API Key)
if [ ! -f ".env" ]; then
    echo "Enter your GOOGLE_API_KEY:"
    read api_key
    echo "GOOGLE_API_KEY=$api_key" > .env
fi

# 6. Build and Run with Docker Compose
# --build: Rebuild images
# -d: Detached mode (run in background)
sudo docker-compose up --build -d

echo "Deployment Complete! Access your app at http://<EC2-Public-IP>:8501"
