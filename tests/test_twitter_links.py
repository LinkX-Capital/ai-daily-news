import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import tweet_fetcher
import twitter_links
import twitter_push


class TwitterLinksTests(unittest.TestCase):
    @patch('tweet_fetcher.get_api_key', return_value='test-only')
    @patch('tweet_fetcher.is_recent', return_value=True)
    @patch('httpx.get')
    def test_fetch_keeps_link_entities_beyond_truncated_preview(self, get, recent, key):
        text = 'A' * 450 + ' https://t.co/paper'
        get.return_value = Mock(status_code=200)
        get.return_value.json.return_value = {'data': {'tweets': [{
            'text': text, 'url': 'https://x.com/a/status/1', 'createdAt': 'today',
            'entities': {'urls': [{'url': 'https://t.co/paper', 'expanded_url': 'https://arxiv.org/abs/2610.12345'}]},
            'author': {'entities': {'urls': [{'expanded_url': 'https://unrelated.example/profile'}]}},
        }]}}
        tweet = tweet_fetcher.fetch_user_tweets('a')[0]
        self.assertNotIn('t.co/paper', tweet['title'])
        self.assertEqual(tweet['full_text'], text)
        self.assertEqual([item['url'] for item in tweet['attached_links']], ['https://arxiv.org/abs/2610.12345'])

    def test_original_paper_and_code_reach_card_preview_and_email(self):
        tweet = {'title': 'Research release', 'source': '@test', 'link': 'https://x.com/test/status/1',
                 'attached_links': [{'url': 'https://arxiv.org/abs/2610.12345'}, {'url': 'https://github.com/test/research'}]}
        highlight = {'idx': 1, 'title': '研究发布', 'summary': '发布了一项研究与开源实现。',
                     'attachments': [{'url': 'https://invented.example/model-link'}]}
        records = twitter_push.build_highlight_records([highlight], [tweet])
        twitter_links.enrich_attached_links(records, resolver=lambda url: '')
        card = json.dumps(twitter_push.build_twitter_card([tweet], records, '2026-10-30'))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'preview.md'
            twitter_push.generate_preview_md([tweet], path, records, '2026-10-30')
            preview = path.read_text()
        _, email, _ = twitter_push.build_twitter_email([tweet], records, '2026-10-30')
        for output in (card, preview, email):
            self.assertIn(tweet['link'], output)
            self.assertIn('https://arxiv.org/abs/2610.12345', output)
            self.assertIn('https://github.com/test/research', output)
            self.assertNotIn('invented.example', output)
        self.assertIn('[论文]', preview)
        self.assertIn('[代码]', preview)

    def test_dedupes_short_url_and_legacy_context_and_limits_to_two(self):
        records = [{'context_url': 'https://cognition.com/blog/corridor-joining-cognition', 'attachments': [
            {'url': 'https://t.co/announcement'},
            {'url': 'https://github.com/example/project'},
            {'url': 'https://docs.example.com/guide'},
        ]}]
        twitter_links.enrich_attached_links(records, resolver=lambda url: records[0]['context_url'])
        resources = twitter_links.attachment_links(records[0])
        self.assertEqual(len(resources), 2)
        self.assertEqual([item['label'] for item in resources], ['公告', '代码'])

    def test_unresolved_links_media_and_private_urls_are_not_displayed(self):
        record = {'attachments': [{'url': url} for url in [
            'https://t.co/unresolved', 'https://x.com/a/status/2', 'https://pbs.twimg.com/photo.jpg',
            'http://127.0.0.1/resource', 'javascript:alert(1)',
        ]]}
        twitter_links.enrich_attached_links([record], resolver=lambda url: '')
        self.assertEqual(twitter_links.attachment_links(record), [])

    @patch('twitter_links.httpx.Client')
    def test_short_link_expansion_does_not_download_destination(self, client):
        client.return_value.__enter__.return_value.head.return_value = Mock(
            status_code=302, headers={'location': 'https://arxiv.org/abs/2610.12345'})
        self.assertEqual(twitter_links.resolve_short_url('https://t.co/paper'), 'https://arxiv.org/abs/2610.12345')
        client.return_value.__enter__.return_value.head.assert_called_once_with('https://t.co/paper')


if __name__ == '__main__':
    unittest.main()
