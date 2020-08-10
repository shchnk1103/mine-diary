from comments.views import comment
from django import template
from ..forms import CommentForm


register = template.Library()


@register.inclusion_tag('comments/inclusions/_form.html', takes_context=True)
def show_comment_form(context, post, form=None):
    if form is None:
        form = CommentForm()
    return {
        'post': post,
        'form': form
    }


@register.inclusion_tag('comments/inclusions/_list.html', takes_context=True)
def show_comments(context, post):
    comment_list = post.comments_post.all()
    comment_count = comment_list.count()
    return {
        'comment_list': comment_list,
        'comment_count': comment_count
    }
