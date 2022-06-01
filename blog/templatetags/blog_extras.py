import logging
from django import template
from django.contrib.auth.models import User
from django.utils.html import format_html

from blog.models import Post

logger = logging.getLogger(__name__)
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


@register.simple_tag
def row(extra_classes=''):
  return format_html('<div class="row {}">', extra_classes)


@register.simple_tag
def endrow():
  return format_html('</div>')


@register.simple_tag
def col(extra_classes=''):
  return format_html('<div class="col {}">', extra_classes)


@register.simple_tag
def endcol():
  return format_html('</div>')



@register.inclusion_tag('blog/post-list.html', takes_context=True)
def recent_posts(context):
  current_post_id = context['post'].id
  posts = Post.objects.exclude(pk=current_post_id).order_by('-published_at')[:5]
  logger.debug("Loaded %d recent posts for post %d", len(posts), current_post_id)
  return {'title': 'Recent Posts', 'posts': posts}
