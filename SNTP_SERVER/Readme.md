## SNTP-server

### Описание: 
SNTP-сервер прослушивает порт UDP 123, синхронизируя свое время с OC. Затем сервер, в процессе постоянных запросов от клиента, исправляет время на указанное количество секунд, заданное в конфигурационном файле config.ini, и отправляет  искаженное время клиенту.

## Запуск:
1.Запуск сервера:
```
> py sntp_server.py
```
2.Запуск клиента:
```
> py client.py
```