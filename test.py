import re


print(re.findall(r'(?:<strong>|^).*?(?=<strong>|$)', '<p><strong>asdda</strong> fdf <strong> llfe </strong> qwe</p>'))
