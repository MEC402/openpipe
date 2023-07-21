###  fix firewall isssue after oit maintenance
```bash
sudo firewall-cmd --add-service=http --permanent
sudo firewall-cmd --add-service=https --permanent
sudo firewall-cmd --reload
apachectl restart
```

### Get Apache error log (Cleaned)

```bash
cat /etc/httpd/logs/error_log|awk '{ print $1,$2,$3,$4,$5,$12,$13,$14,$15,$16,$17,$18,$19,$20,$21,"\n" }'
```

#add more here
