import re

# @와 . 필수 / 중복
def validate_email(email):
    email_pattern = re.compile("^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$")
    return bool(email_pattern.match(email))

# 8자리 이상, 문자, 숫자, 특수문자 복합
def validate_password(password):
    password_pattern = re.compile("^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@!%*#?&]{8,}$")
    return bool(password_pattern.match(password))