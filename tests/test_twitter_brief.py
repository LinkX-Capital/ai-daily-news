import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import twitter_push


def tweet(index):
    return {'title': f'Candidate {index}', 'source': f'@source{index}',
            'link': f'https://x.com/source{index}/status/{index}', 'category': 'Company'}


def row(index, tier='primary', event=None, related=None):
    return {'idx': index, 'tier': tier, 'event_key': event or f'event-{index}',
            'related_idxs': related or [index], 'title': f'事件 {index}', 'summary': f'已确认的事实 {index}'}


class TwitterBriefTests(unittest.TestCase):
    @patch('twitter_push.LLM_API_KEY', 'test-only')
    @patch('httpx.post')
    def test_candidate_after_thirty_can_be_selected(self, post):
        tweets = [tweet(i) for i in range(1, 41)]
        post.return_value = Mock(status_code=200)
        post.return_value.json.return_value = {'content': [
            {'type': 'text', 'text': json.dumps({'highlights': [row(40)]})}
        ]}
        highlights, selected = twitter_push.extract_highlights_llm(tweets)
        self.assertEqual(len(selected), 40)
        self.assertIn('Candidate 40', post.call_args.kwargs['json']['messages'][0]['content'])
        self.assertEqual(twitter_push.build_highlight_records(highlights, selected)[0]['link'], tweets[-1]['link'])

    def test_duplicate_event_is_collapsed_and_source_is_bound_to_evidence(self):
        selected = [tweet(1), tweet(2), tweet(3)]
        first = row(1, event='same-event', related=[1, 2])
        first['source'] = 'fabricated-account'
        result = twitter_push._normalize_highlights({'highlights': [first, row(2, event='same-event')]}, selected)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['source'], 'source1')
        records = twitter_push.build_highlight_records(result, selected)
        self.assertEqual(records[0]['related_links'], [selected[0]['link'], selected[1]['link']])
        with self.assertRaises(ValueError):
            twitter_push._normalize_highlights({'highlights': [row(99)]}, selected)

    def test_limits_are_enforced_in_card_and_preview_with_folded_secondary(self):
        records = [
            {'title': f'Primary {i}', 'summary': '事实', 'source': 'test', 'link': 'https://x.com/test/status/1', 'tier': 'primary'}
            for i in range(8)
        ] + [
            {'title': f'Secondary {i}', 'summary': '事实', 'source': 'test', 'link': 'https://x.com/test/status/1', 'tier': 'secondary'}
            for i in range(5)
        ]
        card = twitter_push.build_twitter_card([], records, '2026-10-30')
        text = json.dumps(card)
        self.assertIn('Primary 4', text)
        self.assertNotIn('Primary 5', text)
        self.assertIn('Secondary 2', text)
        self.assertNotIn('Secondary 3', text)
        panel = next(element for element in card['body']['elements'] if element['tag'] == 'collapsible_panel')
        self.assertFalse(panel['expanded'])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'preview.md'
            twitter_push.generate_preview_md([], path, records, '2026-10-30')
            preview = path.read_text()
        self.assertIn(card['header']['title']['content'], preview)
        self.assertIn('<details>', preview)
        self.assertNotIn('Primary 5', preview)
        self.assertNotIn('Secondary 3', preview)

    def test_sparse_selection_is_not_padded(self):
        records = [{'title': '唯一重点', 'source': 'test', 'tier': 'primary'}]
        primary, secondary = twitter_push.split_highlights(records)
        self.assertEqual(len(primary), 1)
        self.assertFalse(secondary)
        card = twitter_push.build_twitter_card([], records, '2026-10-30')
        self.assertFalse(any(element['tag'] == 'collapsible_panel' for element in card['body']['elements']))


if __name__ == '__main__':
    unittest.main()
