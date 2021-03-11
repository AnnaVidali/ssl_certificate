import socket
import ssl
from datetime import datetime

# ask user to provide hostname
hostname = input('Please provide url to get certificate: ')

# get certificate for input
ctx = ssl.create_default_context()
with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
    # try to connect to https port
    s.connect((hostname, 443))
    cert = s.getpeercert()
    print('Certificate for ' + hostname + ' has been taken!')

# get notBefore and notAfter from certificate
before = cert['notBefore']
after = cert['notAfter']

# make str datetime objects
datebefore = datetime.strptime(before, "%b %d %H:%M:%S %Y GMT")
dateafter = datetime.strptime(after, "%b %d %H:%M:%S %Y GMT")

# ask user to provide date or take the current one
answer = input('Do you want to provide a date(i) or take the current date(c) as input? (i/c): ')
# get date from user or system
if answer == 'i':
    day = input('Please provide a day number(put 0 at the beginning if the number is less than 10): ')
    month = input('Please provide a month number(put 0 at the beginning if the number is less than 10): ')
    year = input('Please provide a year number: ')
    # create string to convert to datetime
    tmp = day + '/' + month + '/' + year
    date = datetime.strptime(tmp, "%d/%m/%Y")
elif answer == 'c':
    date = datetime.now()
else:
    print('Wrond answer! Terminating...')
    exit()

if datebefore <= date <= dateafter:
    print('The date is inside the boundaries of the certificate.')
else:
    print('The date is NOT inside the boundaries of the certificate.')

# get commonName from issuer from certificate
issuer = dict(x[0] for x in cert['issuer'])
commonName = issuer['commonName']

var = input('Please provide the name of the issuer to see if they are in the list: ')

# iterate txt to find user's input
with open("list.txt", "r") as file:
    for line in file:
        if line.strip() == var:
            isinlist = True
            break
        else:
            isinlist = False

if isinlist:
    print("Issuer's common name is in the list.")
else:
    print("Issuer's common name is NOT in the list.")

# ask user what information to get from subject
print('1) Country name' + '\n' + '2) State or province name' + '\n' + '3) Locality name' + '\n' + '4) Organization name' + '\n' + '5) Organizational unit name' + '\n' + '6) CommonName')
info = input('What information do you want to know from certificate? Please provide the number: ')

# check what the user wants to know and print it
subject = dict(x[0] for x in cert['subject'])
if info == '1':
    try:
        countryName = subject['countryName']
        print('The country name is: ' + countryName)
    except:
        print("There isn't such field at the subject of this url! Terminating...")
        exit()
elif info == '2':
    try:
        stateOrProvinceName = subject['stateOrProvinceName']
        print('The state or province is: ' + stateOrProvinceName)
    except:
        print("There isn't such field at the subject of this url! Terminating...")
        exit()
elif info == '3':
    try:
        localityName = subject['localityName']
        print('The locality name is: ' + localityName)
    except:
        print("There isn't such field at the subject of this url! Terminating...")
        exit()
elif info == '4':
    try:
        organizationName = subject['organizationName']
        print('The organization name is: ' + organizationName)
    except:
        print("There isn't such field at the subject of this url! Terminating...")
        exit()
elif info == '5':
    try:
        organizationalUnitName = subject['organizationalUnitName']
        print('The organizational unit name is: ' + organizationalUnitName)
    except:
        print("There isn't such field at the subject of this url! Terminating...")
        exit()
elif info == '6':
    try:
        commonName1 = subject['commonName']
        print('The common name is: ' + commonName1)
    except:
        print("There isn't such field at the subject of this url! Terminating...")
        exit()
else:
    print('Wrong answer! Terminating...')
    exit()

# prints the version of the certificate
version = cert['version']
print('The version of the certificate is: ' + str(version))