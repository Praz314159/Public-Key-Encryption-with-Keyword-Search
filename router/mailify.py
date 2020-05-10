from sys import stdin
from email.message import EmailMessage

m = EmailMessage()
m.set_content(stdin.read())
m['Subject'] = 'Encrypted Message'
m['From'] = 'somebody@example.com'
m['To'] = 'peks@dov.ms'

print(str(m))
