#!/bin/bash

while true; do
    # Отправить curl запрос
    curl -X POST http://app:8000/notification/update-notification

    # Подождать 10 секунд
    sleep 10
done
