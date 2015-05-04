import hashlib
from django import template

register = template.Library()

@register.filter
def avatar_url(email):
    email = email.encode('utf-8')
    hash = hashlib.md5(email.strip().lower()).hexdigest()
    return "http://cdn.libravatar.org/avatar/"+hash