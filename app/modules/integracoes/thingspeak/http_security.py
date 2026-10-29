"""Conservative HTTP boundary for a global channel with no tenant ownership model.

Internal acquisition services remain framework/JWT independent.
"""
import re
from urllib.parse import urlsplit

SENSITIVE_KEYS={'apikey','readapikey','writeapikey','token','accesstoken','refreshtoken',
    'authorization','password','senha','secret','clientsecret','privatekey','credentials'}
AUTH_VALUE=re.compile(r'(?i)(?:\bbearer\s+[^\s,;]+|\beyJ[\w-]+\.[\w-]+\.[\w-]+\b|\b(?:api[_-]?key|token|password|senha|secret)\s*[:=]\s*[^\s,;&]+)')
URL_USERINFO=re.compile(r'(?i)(https?://)[^\s/@]+@')
URL_QUERY_SECRET=re.compile(r'(?i)([?&](?:api[_-]?key|token|access_token|password|secret)=)[^&\s]+')


def validate_http_config(service):
    parsed=urlsplit(service.config.base_url)
    if (parsed.scheme not in ('http','https') or not parsed.hostname or parsed.username is not None
            or parsed.password is not None or parsed.query or parsed.fragment):
        raise ValueError('Unsafe HTTP integration configuration')
    _=parsed.port  # Validate malformed ports without echoing configuration.
    if service.config.channel_id is not None and not re.fullmatch(r'[1-9][0-9]*',service.config.channel_id):
        raise ValueError('Invalid channel identity')


def safe_response(value,service):
    """Copy public DTOs; never mutate original feeds, measurements or stored history."""
    known=tuple(s for s in (service.config.read_api_key,getattr(service.client,'read_api_key',None)) if s)
    def clean(v):
        if hasattr(v,'model_dump'): return clean(v.model_dump(mode='python'))
        if isinstance(v,dict):
            return {k:clean(item) for k,item in v.items()
                if re.sub(r'[^a-z0-9]','',str(k).lower()) not in SENSITIVE_KEYS}
        if isinstance(v,(list,tuple)): return [clean(item) for item in v]
        if isinstance(v,str):
            for secret in sorted(set(known),key=len,reverse=True): v=v.replace(secret,'[REDACTED]')
            v=URL_USERINFO.sub(r'\1[REDACTED]@',v)
            v=URL_QUERY_SECRET.sub(r'\1[REDACTED]',v)
            return AUTH_VALUE.sub('[REDACTED]',v)
        return v
    return clean(value)


def safe_latest(feed,service):
    if feed is None: return None
    # Opaque upstream metadata can carry credentials or unrelated configuration.
    # Keep the feed's documented readings and identity; allow no arbitrary raw keys.
    result=feed.model_dump(mode='python')
    allowed={'created_at','entry_id'}|set(feed.fields)
    result['raw']={k:v for k,v in result['raw'].items() if k in allowed}
    return safe_response(result,service)
