from django.conf import settings
from django.utils.html import format_html

from django import template
register = template.Library()


def _tracking_script(setting_name, script):
    tag_id = getattr(settings, setting_name, None)

    if not tag_id:
        return

    return format_html(script, tag_id)


@register.simple_tag
def google_analytics():
    return _tracking_script('GOOGLE_ANALYTICS_ID', """
        <!-- Global Site Tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id={0}"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){{dataLayer.push(arguments)}};
            gtag('js', new Date());
            gtag('config', '{0}');
        </script>
    """)


@register.simple_tag
def google_tagmanager():
    return _tracking_script('GOOGLE_TAGMANAGER_ID', """
        <!-- Google Tag Manager -->
        <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
        new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
        j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
        'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
        }})(window,document,'script','dataLayer','{}');</script>
        <!-- End Google Tag Manager -->
    """)


@register.simple_tag
def google_tagmanager_noscript():
    return _tracking_script('GOOGLE_TAGMANAGER_ID', """
        <!-- Google Tag Manager (noscript) -->
        <noscript><iframe src="https://www.googletagmanager.com/ns.html?id={}"
            height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
        <!-- End Google Tag Manager (noscript) -->
    """)


@register.simple_tag
def active_campaign_event_tracker():
    return _tracking_script('ACTIVE_CAMPAIGN_EVENT_ACTID', """
        <script>
            var trackcmp_email = '';
            var trackcmp = document.createElement("script");
            trackcmp.async = true;
            trackcmp.type = 'text/javascript';
            trackcmp.src = '//trackcmp.net/visit?actid={}&e='+encodeURIComponent(trackcmp_email)+'&r='+encodeURIComponent(document.referrer)+'&u='+encodeURIComponent(window.location.href);
            var trackcmp_s = document.getElementsByTagName("script");
            if (trackcmp_s.length) {{
            trackcmp_s[0].parentNode.appendChild(trackcmp);
            }} else {{
            var trackcmp_h = document.getElementsByTagName("head");
            trackcmp_h.length && trackcmp_h[0].appendChild(trackcmp);
            }}
        </script>
    """)
