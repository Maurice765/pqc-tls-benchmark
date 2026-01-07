```
docker run -v $(pwd)/certs:/certs --rm openquantumsafe/oqs-ossl3 sh -c "
  echo 'Erstelle CA...'
  openssl req -x509 -new -newkey ec -pkeyopt ec_paramgen_curve:prime256v1 -keyout /certs/CA.key -out /certs/CA.crt -nodes -subj '/CN=PQC Root CA' -days 365
  
  echo 'Erstelle Server Key...'
  openssl req -new -newkey ec -pkeyopt ec_paramgen_curve:prime256v1 -keyout /certs/server.key -out /certs/server.csr -nodes -subj '/CN=server'
  
  echo 'Signiere Server Zertifikat...'
  openssl x509 -req -in /certs/server.csr -out /certs/server.crt -CA /certs/CA.crt -CAkey /certs/CA.key -CAcreateserial -days 365
  
  echo 'Setze Berechtigungen...'
  chmod 644 /certs/*
"
```


```
docker-compose up --build -d
```