# WOL Manager

Simple WOL (Wake-on-lan) project that let you manage multiple devices. \
This WOL manager can take two forms. \
First is a web app whereas second is a telegram bot.

## Web App

### Requirements
- docker compose

### Configuration
- In the root dir, edit .env file to select a very strong api-key
- Fulfil `backend/config.d/config.yml` network field with your
- Feel free to change default path of database_url

### Execution
- Exec `docker compose build && docker compose up -d`


## Telegram

This version of the project is under redevelopment.