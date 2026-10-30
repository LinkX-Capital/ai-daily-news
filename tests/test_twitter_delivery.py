import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import feishu_push
import twitter_push


class TwitterDeliveryTests(unittest.TestCase):
    @patch.dict(os.environ, {'FEISHU_TWITTER_WEBHOOK': 'https://old.example/hook', 'EMAIL_RECIPIENTS': ''})
    @patch('httpx.post')
    @patch('feishu_push.subprocess.run')
    def test_twitter_uses_daily_bot_recipient_instead_of_old_webhook(self, run, post):
        run.return_value = subprocess.CompletedProcess(
            [], 0, json.dumps({'ok': True, 'data': {'message_id': 'om_test', 'chat_id': 'oc_test'}}, separators=(',', ':')), ''
        )
        cache = [{'title': 'Original tweet', 'source': '@test', 'link': 'https://x.com/test/status/1', 'category': 'Company'}]
        highlights = [{'idx': 1, 'title': '中文重点', 'summary': '已确认的一句话说明', 'source': 'test'}]
        with tempfile.TemporaryDirectory() as directory, \
                patch.object(twitter_push, '__file__', str(Path(directory) / 'twitter_push.py')), \
                patch.object(sys, 'argv', ['twitter_push.py', '2026-10-30']), \
                patch.object(twitter_push, 'get_tweets', return_value=cache), \
                patch.object(twitter_push, 'extract_highlights_llm', return_value=(highlights, cache)), \
                patch.object(twitter_push, 'generate_preview_md'):
            twitter_push.main()
        deliveries = [call.args[0] for call in run.call_args_list if call.args[0][0] == 'lark-cli']
        self.assertEqual(len(deliveries), 1)
        args = deliveries[0]
        self.assertEqual(args[args.index('--as') + 1], 'bot')
        self.assertEqual(args[args.index('--user-id') + 1], feishu_push.RECIPIENT)
        card = json.loads(args[args.index('--content') + 1])
        self.assertIn('中文重点', json.dumps(card, ensure_ascii=False))
        self.assertIn(cache[0]['link'], json.dumps(card))
        self.assertEqual(card['body']['elements'][-1]['behaviors'][0]['default_url'],
                         'https://linkx-capital.github.io/ai-daily-news/twitter-preview-2026-10-30.md')
        post.assert_not_called()

    @patch('feishu_push.subprocess.run')
    def test_rejected_bot_delivery_is_not_reported_as_success(self, run):
        run.return_value = subprocess.CompletedProcess([], 1, '', '{"ok": false}')
        self.assertFalse(twitter_push.push_twitter_to_feishu([], [], '2026-10-30'))


if __name__ == '__main__':
    unittest.main()
