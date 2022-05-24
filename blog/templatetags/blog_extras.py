from django import template
from django.contrib.auth.models import User
from django.utils.html import format_html

register = template.Library()


@register.filter
def author_details(author, current_user):
  if not isinstance(author, User):
    return ''
  if author == current_user:
    return format_html('<strong>me</strong>')
  
  if author.first_name and author.last_name:
    name = f'{author.first_name} {author.last_name}'
  else:
    name = author.username

  if author.email:
    name = f'<a href="mailto:{author.email}">{name}</a>'

  return format_html(name)