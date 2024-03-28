ng build --prod  --base-href /ui/

ng build --prod  --base-href /uidev/

fixing refresh issue:
http://joeljoseph.net/angular-6-deploy-on-apache-server-by-solving-404-not-found-error-on-page-refresh/


## Deployment on AWS

```bash
ng build --prod --aot
aws s3 cp ./dist s3://openpipe-portal --recursive
```
To make sure all the files metadata is tagged correctly on s3 (Use this if you get MIME error)
```bash
ng build --prod --aot
aws s3 sync ./dist s3://openpipe-portal --exclude "*.js"
aws s3 sync ./dist s3://openpipe-portal --include "*.js" --content-type "application/javascript"
```

