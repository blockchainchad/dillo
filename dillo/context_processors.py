from django.conf import settings
from django.utils import timezone
import sorl.thumbnail

from dillo.models.feeds import FeedEntry
from dillo.models.events import Event
from dillo.views.mixins import OgData
from dillo.models.communities import Community


def notifications_count(request):
    """Count the unread notifications for the authenticated user."""
    if 'user' not in request or request.user.is_anonymous:
        count = 0
    else:
        count = FeedEntry.objects.filter(
            user=request.user,
            is_read=False,
            category='notification',
        ).count()
    return {
        'notifications_count': count,
    }


def google_analytics_tracking_id(_):
    return {'GOOGLE_ANALYTICS_TRACKING_ID': settings.GOOGLE_ANALYTICS_TRACKING_ID}


def media_uploads_accepted_mimes(_):
    return {'MEDIA_UPLOADS_ACCEPTED_MIMES': list(settings.MEDIA_UPLOADS_ACCEPTED_MIMES)}


def communities_navigation(request):
    """Populate the communities navigation.

    By default all communities_features are displayed.
    If the user follows a community, we show the community in a dedicated
    list, and remove it from the featured list. Performance can still be
    optimized by using a direct User-Community m2m table.
    """
    communities_featured = Community.objects.filter(is_featured=True)
    communities_followed = []
    if request.user.is_authenticated:
        communities_followed = request.user.profile.followed_communities
        communities_featured = [c for c in communities_featured if c not in communities_followed]

    return {
        'communities_followed': communities_followed,
        'communities_featured': communities_featured,
    }


def default_og_data(_):
    """Default values for the Open Graph data.

    This is used as fallback for populating the og: and twitter: tags in every page.
    """
    return {
        'og_data_default': OgData(
            title=settings.SITE_TITLE,
            description=settings.SITE_DESCRIPTION,
            image_field=None,
            image_alt=settings.SITE_TITLE,
        )
    }


def current_user_js(request):
    current_user = {
        'isAuthenticated': request.user.is_authenticated,
        'isStaff': request.user.is_staff,
        'isModerator': request.user.groups.filter(name='moderators').exists(),
        'username': (None if not request.user.is_authenticated else request.user.username),
        'avatar': None,
        'url': (None if not request.user.is_authenticated else request.user.profile.absolute_url),
        'name': (None if not request.user.is_authenticated else request.user.profile.name),
        'notificationsCount': 0,
    }
    if request.user.is_authenticated:
        if request.user.profile.avatar:
            current_user['avatar'] = sorl.thumbnail.get_thumbnail(
                request.user.profile.avatar, '128x128', crop='center', quality=80
            ).url
        current_user['notificationsCount'] = FeedEntry.objects.filter(
            user=request.user,
            is_read=False,
            category='notification',
        ).count()

    return {'current_user_js': current_user}


def upcoming_events(_):
    ue = (
        Event.objects.filter(starts_at__gt=timezone.now(), visibility='public')
        .order_by('starts_at')
        .all()
    )
    return {'upcoming_events': ue}
