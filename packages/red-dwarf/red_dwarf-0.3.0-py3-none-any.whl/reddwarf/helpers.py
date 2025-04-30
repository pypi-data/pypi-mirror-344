from urllib3.util import ssl_
from requests import Session
from requests.adapters import HTTPAdapter
from requests_cache import CacheMixin
from requests_ratelimiter import LimiterMixin

class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    """
    Session class with caching and rate-limiting behavior. Accepts arguments for both
    LimiterSession and CachedSession.

    See: See: https://requests-cache.readthedocs.io/en/stable/user_guide/compatibility.html#requests-ratelimiter
    """

class CloudflareBypassHTTPAdapter(HTTPAdapter):
    """
    A TransportAdapter that forces TLSv1.3 in Requests, so that Cloudflare doesn't flag us.

    Source: https://lukasa.co.uk/2017/02/Configuring_TLS_With_Requests/
    """

    def init_patched_ssl_context(self):
        context = ssl_.create_urllib3_context()
        context.load_default_certs()
        # Only available in Python 3.7
        if hasattr(ssl_, "TLSVersion"):
            context.minimum_version = ssl_.TLSVersion.TLSv1_3
        else:
            context.options |= ssl_.OP_NO_TLSv1_2

        return context

    def init_poolmanager(self, *args, **kwargs):
        kwargs['ssl_context'] = self.init_patched_ssl_context()
        return super(CloudflareBypassHTTPAdapter, self).init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        kwargs['ssl_context'] = self.init_patched_ssl_context()
        return super(CloudflareBypassHTTPAdapter, self).proxy_manager_for(*args, **kwargs)
