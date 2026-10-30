"""Keep original tweet resources separate from model-written summaries."""

import ipaddress
import re
from urllib.parse import urljoin, urlsplit

import httpx

from pipeline_core import canonicalize_url


def public_url(value):
    if not isinstance(value, str):
        return ''
    value = value.strip().rstrip('.,;，。；')
    try:
        parts = urlsplit(value)
        host = parts.hostname or ''
        if parts.scheme not in {'http', 'https'} or not host or parts.username or parts.password:
            return ''
        if host == 'localhost' or '.' not in host or host.endswith(('.local', '.internal')):
            return ''
        try:
            if not ipaddress.ip_address(host).is_global:
                return ''
        except ValueError:
            pass
        return canonicalize_url(value)
    except ValueError:
        return ''


def resource_label(url):
    parts = urlsplit(url)
    host, path = (parts.hostname or '').lower(), parts.path.lower()
    if host in {'github.com', 'gitlab.com', 'codeberg.org'}:
        return '代码'
    if host in {'arxiv.org', 'www.arxiv.org', 'openreview.net', 'aclanthology.org', 'proceedings.mlr.press'} or '/papers/' in path:
        return '论文'
    if host in {'youtube.com', 'www.youtube.com', 'youtu.be', 'vimeo.com', 'www.loom.com'}:
        return '演示'
    if host.startswith('docs.') or '/docs/' in path or '/documentation/' in path:
        return '文档'
    if host in {'huggingface.co', 'www.huggingface.co'}:
        return '模型' if '/datasets/' not in path else '数据'
    official_hosts = {'cognition.com', 'www.cognition.com', 'cohere.com', 'www.cohere.com',
                      'openai.com', 'www.openai.com', 'anthropic.com', 'www.anthropic.com',
                      'mistral.ai', 'www.mistral.ai', 'deepmind.google', 'blog.google'}
    if host in official_hosts and any(part in path for part in ('/blog/', '/news/', '/research/', '/announcements/')):
        return '公告'
    return '原文'


def external_resource(value):
    url = public_url(value)
    if not url:
        return ''
    host = (urlsplit(url).hostname or '').lower()
    if host in {'x.com', 'www.x.com', 'twitter.com', 'www.twitter.com', 'pic.twitter.com',
                'pbs.twimg.com', 'video.twimg.com'}:
        return ''
    if urlsplit(url).path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
        return ''
    return url


def extract_attached_links(tweet):
    """Read tweet entities, never an author's profile or model-invented URLs."""
    results, seen = [], set()

    def add(url, short_url='', title=''):
        url = external_resource(url)
        if not url or url in seen:
            return
        seen.add(url)
        results.append({'url': url, 'short_url': public_url(short_url),
                        'label': resource_label(url), 'title': title or ''})

    def visit(raw):
        if not isinstance(raw, dict):
            return
        entities = raw.get('entities') or {}
        for entity in entities.get('urls') or []:
            if not isinstance(entity, dict):
                continue
            add(entity.get('expanded_url') or entity.get('url'), entity.get('url', ''), entity.get('title', ''))
        for item in raw.get('attached_links') or []:
            if isinstance(item, dict):
                add(item.get('url'), item.get('short_url', ''), item.get('title', ''))
        text = raw.get('full_text') or raw.get('text') or raw.get('title') or ''
        for url in re.findall(r'https?://[^\s<>"\]]+', text):
            if any(item['short_url'] == public_url(url) for item in results):
                continue
            add(url)
        visit(raw.get('retweeted_tweet'))

    visit(tweet)
    return results


def resolve_short_url(url):
    """Expand t.co without downloading the destination page or its media."""
    current = public_url(url)
    if not current:
        return ''
    try:
        with httpx.Client(timeout=8, follow_redirects=False) as client:
            for _ in range(5):
                if (urlsplit(current).hostname or '').lower() not in {'t.co', 'www.t.co'}:
                    return external_resource(current)
                response = client.head(current)
                if response.status_code not in {301, 302, 303, 307, 308}:
                    return ''
                current = public_url(urljoin(current, response.headers.get('location', '')))
                if not current:
                    return ''
    except httpx.HTTPError:
        pass
    return ''


def enrich_attached_links(records, resolver=None):
    """At most two useful resource links per selected event; dedupe redirects."""
    resolver = resolver or resolve_short_url
    resolved = {}
    priority = {'公告': 0, '论文': 1, '代码': 2, '模型': 3, '数据': 4, '文档': 5, '演示': 6, '原文': 7}
    for record in records or []:
        links, seen = [], set()
        candidates = list(record.get('attachments') or [])
        if record.get('context_url'):
            candidates.insert(0, {'url': record['context_url']})
        for item in candidates:
            url = external_resource(item.get('url')) if isinstance(item, dict) else ''
            if not url:
                continue
            if (urlsplit(url).hostname or '').lower() in {'t.co', 'www.t.co'}:
                if url not in resolved:
                    resolved[url] = resolver(url)
                url = external_resource(resolved[url])
            if not url or (urlsplit(url).hostname or '').lower() in {'t.co', 'www.t.co'} or url in seen:
                continue
            seen.add(url)
            links.append({'url': url, 'label': resource_label(url)})
        record['attachments'] = sorted(links, key=lambda item: priority[item['label']])[:2]
    return records


def attachment_links(record):
    """Pure rendering path: never perform network requests while rendering."""
    candidates = list(record.get('attachments') or [])
    if record.get('context_url'):
        candidates.insert(0, {'url': record['context_url']})
    links, seen = [], set()
    for item in candidates:
        url = external_resource(item.get('url')) if isinstance(item, dict) else ''
        if not url or url in seen or (urlsplit(url).hostname or '').lower() in {'t.co', 'www.t.co'}:
            continue
        seen.add(url)
        links.append({'url': url, 'label': resource_label(url)})
        if len(links) == 2:
            break
    return links
