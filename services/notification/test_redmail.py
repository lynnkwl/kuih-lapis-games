# Requirement:
# pip install redmail

from redmail import gmail

gmail.username = "kuihgames6@gmail.com"
gmail.password = "vfjs gdde nffm mmmk"

gmail.send(
    subject='An Example Subject',
    receivers=['receiver@example.com'],
    text='Hi, this is an example email.'
)


