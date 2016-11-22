#!/usr/bin/python3

import sys
import pexpect

# Usage:
#    create_cert_key.py <Server addr(server ip or domain name)>


PHRASE = '123456'  # Password
CN = 'CN'  # Country Name
STATE = 'GUANGDONG'  # Province Name
CITY = 'SHENZHEN'  # Locality Name
ON = 'yuxian'  # Organization Name
OUN = 'yuxian'  # Organizational Unit Name
KEY_LENGTH = 2048  # Key length
COMMON_NAME = sys.argv[1] # Server addr

cmd = [
    # Generate CA
    'openssl req -new -x509 -days 365 -extensions v3_ca -keyout ca.key -out ca.crt',
    # Generate Server key
    'openssl genrsa -des3 -out server.key {}'.format(KEY_LENGTH),
    # Remove server.key's passwd
    'openssl genrsa -out server.key {}'.format(KEY_LENGTH),
    # Generate Server csr
    'openssl req -out server.csr -key server.key -new',
    # Generate Server crt(pem)
    'openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365',
    # Generate client key
    'openssl genrsa -des3 -out client.key {}'.format(KEY_LENGTH),
    # Generate client csr
    'openssl req -out client.csr -key client.key -new',
    # Generate client crt
    'openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt -days 365',
    # Generate ca crt's der
    'openssl x509 -inform pem -in ca.crt -outform der -out ca.der',
    # Generate client crt's der
    'openssl x509 -inform pem -in client.crt -outform der -out client_crt.der',
    # Generate client key's der
    'openssl rsa -inform PEM -in client.key -outform der -out client_key.der'
]

question = [
    ['phrase', 'Country Name', 'Province Name', 'Locality Name','Organization Name'
            , 'Organizational Unit Name', 'Common Name', 'Email Address'],
    ['phrase'],
    [],
    ['phrase', 'Country Name', 'Province Name', 'Locality Name', 'Organization Name'
            , 'Organizational Unit Name', 'Common Name', 'Email Address', 'password', 'company name'],
    ['phrase'],
    ['phrase'],
    ['phrase', 'Country Name', 'Province Name', 'Locality Name', 'Organization Name'
            , 'Organizational Unit Name', 'Common Name', 'Email Address', 'password', 'company name'],
    ['phrase'],
    [],
    [],
    ['phrase']
]

answer = [
    [PHRASE, CN, STATE, CITY, ON, OUN, COMMON_NAME, ''],
    [PHRASE],
    [],
    [PHRASE, CN, STATE, CITY, ON, OUN, COMMON_NAME, '', '', ''],
    [PHRASE],
    [PHRASE],
    [PHRASE, CN, STATE, CITY, ON, OUN, '', '', '', ''],
    [PHRASE],
    [],
    [],
    [PHRASE]
]


for cmd_index in range(0, len(cmd)):
    p = pexpect.spawn(cmd[cmd_index])
    try:
        while True:
            question_index = p.expect(question[cmd_index])
            p.sendline(answer[cmd_index][question_index])
    except pexpect.TIMEOUT:
        print('<ERR> {} timeout'.format(cmd_index))
    except pexpect.EOF:
        pass
