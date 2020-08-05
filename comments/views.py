from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from blog.models import Post
from .forms import CommentForm
from django.contrib import messages


@require_POST
def comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

        # 评论成功以后的提示
        messages.add_message(request, messages.SUCCESS,
                             '评论成功！', extra_tags='success')

        return redirect(post)

    context = {
        'post': post,
        'form': form
    }

    # 评论失败以后的提示
    messages.add_message(request, messages.ERROR,
                         '评论失败，请修改表单以后重试～', extra_tags='danger')

    return render(request, 'comments/preview.html', context)
