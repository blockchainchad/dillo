import requests.exceptions
import webpreview.excepts
from django.conf import settings
from django.db.models import Q, Count
from django.urls import reverse
from django.template.defaultfilters import truncatechars
from django.utils import timezone
from django.utils.html import strip_tags
from django.views.generic import TemplateView, ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views import View
from django.http import JsonResponse
from micawber.contrib.mcdjango import providers
from micawber.exceptions import ProviderNotFoundException
from sorl.thumbnail import get_thumbnail
from webpreview import web_preview

from dillo.models.posts import get_trending_tags, Post
from dillo.models.events import Event
from dillo.shortcodes import render as shortcode_render
from dillo.markdown import render as markdown_render


class PostListView(TemplateView):
    template_name = 'dillo/posts_base.pug'

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        """Force the creation of CSRF cookie."""
        return super().dispatch(*args, **kwargs)

    @staticmethod
    def get_query_url():
        return reverse('embed_posts_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        session_layout = self.request.session.get('layout', 'list')
        request_layout = self.request.GET.get('layout', session_layout)  # 'list' or 'grid'
        if session_layout != request_layout:
            self.request.session['layout'] = request_layout

        context['query_url'] = self.get_query_url()
        context['layout'] = request_layout
        context['layout_switch'] = 'grid' if request_layout == 'list' else 'list'
        context['trending_tags'] = get_trending_tags()
        # Display processing posts only if user is authenticated
        if self.request.user.is_authenticated:
            processing_posts = Post.objects.filter(
                status='processing', user=self.request.user, visibility='public'
            )
            context['processing_posts'] = {
                'posts': [str(post.hash_id) for post in processing_posts]
            }
        return context


class PostListEmbedView(ListView):
    """List of all published posts."""

    context_object_name = 'posts'
    model = Post

    def get_queryset(self):
        # By default, show only non-hidden posts
        is_hidden = Q(is_hidden_by_moderator=False)
        # If authenticated, show hidden posts only to the post owner
        if self.request.user.is_authenticated:
            is_hidden = is_hidden | Q(is_hidden_by_moderator=True, user=self.request.user)
        # Retrieve only Posts (no Rigs or Jobs)
        return Post.objects.filter(is_hidden, status='published', visibility='public').order_by(
            '-published_at'
        )

    def get_template_names(self):
        current_layout = self.request.session.get('layout', 'list')
        next_layout = self.request.GET.get('layout', current_layout)  # 'list' or 'grid'
        if current_layout != next_layout:
            self.request.session['layout'] = next_layout
        if next_layout == 'list':
            return ['dillo/posts_list_embed.pug']
        elif next_layout == 'grid':
            return ['dillo/posts_grid_embed.pug']

    def get_paginate_by(self, queryset):
        current_layout = self.request.session.get('layout', 'list')
        next_layout = self.request.GET.get('layout', current_layout)
        if next_layout == 'list':
            return 3
        elif next_layout == 'grid':
            return 40


class FeaturedPostListEmbedView(PostListEmbedView):
    template_name = 'dillo/posts_grid_embed.pug'

    def get_queryset(self):
        return (
            Post.objects.filter(
                is_hidden_by_moderator=False,
                status='published',
                visibility='public',
            )
            .exclude(media=False)
            .prefetch_related('likes', 'comments', 'user', 'user__profile', 'media', 'media__video')
            .annotate(Count('likes'))
            .order_by('-created_at', '-is_pinned_by_moderator', '-likes__count')
        )


class UserListEmbedView(ListView):
    """List users. Must be overridden."""

    def get_users_list(self):
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = self.get_users_list()
        return context

    template_name = 'dillo/profiles_list_embed.pug'
    paginate_by = 10


class ApiMarkdownPreview(View):
    @method_decorator(ensure_csrf_cookie)
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        content = request.POST['content']
        return JsonResponse({'preview': shortcode_render(markdown_render(content))})


class ApiLinkPreview(View):
    @method_decorator(ensure_csrf_cookie)
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        content = request.POST['content']
        try:
            oembed_preview = providers.request(content)
        except ProviderNotFoundException:
            oembed_preview = {}

        # Always generate web_preview as fallback for oembed_preview
        try:
            title, description, image = web_preview(content, parser='html.parser')
        except requests.exceptions.InvalidURL:
            return JsonResponse({'preview': None, 'title': None})
        except webpreview.excepts.EmptyURL:
            return JsonResponse({'preview': None, 'title': None})

        if 'html' in oembed_preview:
            preview_html = oembed_preview['html']
        elif image:
            preview_html = f'<img src="{image}" alt="Website Preview" />'
        else:
            preview_html = '<div class="unavailable">Preview not available for this URL</div>'

        if 'title' in oembed_preview:
            title = oembed_preview['title']

        return JsonResponse({'preview': preview_html, 'title': title})


class OgData:
    """Open Graph and Twitter data.

    Used to render Open Graph info in pages.
    """

    def make_excerpt(self, description):
        description_parsed = markdown_render(description)
        description_sripped = strip_tags(description_parsed)
        description_truncated = truncatechars(description_sripped, 120)
        return description_truncated

    def make_thumbnail_url(self, image_field):
        if not image_field:
            return f"{settings.STATIC_URL}images/social.jpg"
        thumbnail = get_thumbnail(image_field, '1280x720', crop='center', quality=80)
        return thumbnail.url

    def __init__(self, title=None, description=None, image_field=None, image_alt=None):
        self.title = title
        self.description = self.make_excerpt(description)
        self.image_url = self.make_thumbnail_url(image_field)
        self.image_alt = image_alt
