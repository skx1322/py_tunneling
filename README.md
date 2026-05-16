# Introduction
A simple TCP Tunneling server/client built using Python. Security super flaw at the moment.

# RSA and Server Cert Setup
1. Generate Private Key
```
openssl genpkey -algorithm RSA -out server.key -pkeyopt rsa_keygen_bits:4096
```

2. Create file named server.csr.cnf
```
[req]
distinguished_name = req_distinguished_name
req_extensions = req_ext
prompt = no

[req_distinguished_name]
C = SG
ST = Singapore
L = Singapore
O = Example Company
OU = IT
CN = 127.0.0.1

[req_ext]
subjectAltName = @alt_names

[alt_names]
IP.1 = 127.0.0.1
```

```
openssl req -new -key server.key -out server.csr -config server.csr.cnf
```

3. Generate self-signed certificate
```
[req]
distinguished_name = req_distinguished_name
x509_extensions = v3_req
prompt = no

[req_distinguished_name]
C = SG
ST = Singapore
L = Singapore
O = Example Company
OU = IT
CN = 127.0.0.1

[v3_req]
subjectAltName = @alt_names

[alt_names]
IP.1 = 127.0.0.1
```

```
openssl x509 -req -in server.csr -signkey server.key -out server.crt -days 365 -extfile server.crt.cnf -extensions v3_req
```

# Reference
1. Key generation guide: https://pyseek.com/2024/07/create-a-simple-vpn-server-using-python/