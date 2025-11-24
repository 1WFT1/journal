#!/bin/bash

cd /home/journal/

# Получаем последние изменения
git fetch origin

# Проверяем, есть ли обновления
LOCAL=$(git rev-parse HEAD) 
REMOTE=$(git rev-parse origin/main) 

if [ "$LOCAL" != "$REMOTE" ]; then
    echo "$(date): Обновление найдено, обновляю..." 
    git pull origin main
    
    # Пробуем использовать docker-compose, если доступен
    if command -v docker-compose &> /dev/null; then
        echo "Использую docker-compose..."
        docker-compose up --build -d
    else
        # Иначе используем обычный docker
        echo "Использую обычный docker..."
        docker build -t fastapi-app .
        docker stop fastapi-container 2>/dev/null || true
        docker rm fastapi-container 2>/dev/null || true
        docker run -d -p 8000:8000 --name fastapi-container fastapi-app
    fi
    echo "$(date): Сервис перезапущен" 
else
    echo "$(date): Обновлений нет"
fi
