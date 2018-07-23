import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# me == my email address
# you == recipient's email address
from vacancy.settings.secret import ( MAIL, PASSWORD_AWARD, USER_AWARD, 
                                        FROM_EMAIL, TO_EMAIL)

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = "Link"
msg['From'] = FROM_EMAIL
msg['To'] = TO_EMAIL

# Create the body of the message (a plain-text and an HTML version).
text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
html = """\
<html>
  <head></head>
  <body>
    <p>Hi!<br>
       How are you?<br>
       Here is the <a href="http://www.python.org">link</a> you wanted.
    </p>
  </body>
</html>
"""

# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
msg.attach(part1)
msg.attach(part2)
# Send the message via local SMTP server.
mail = smtplib.SMTP(MAIL, 587)

mail.ehlo()

mail.starttls()

mail.login(USER_AWARD, PASSWORD_AWARD)
mail.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())
mail.quit()
print('E-mail was sending')