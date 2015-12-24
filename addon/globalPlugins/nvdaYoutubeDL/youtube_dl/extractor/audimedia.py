# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor
from ..utils import (
    int_or_none,
    parse_iso8601,
    sanitized_Request,
)


class AudiMediaIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?audimedia\.tv/(?:en|de)/vid/(?P<id>[^/?#]+)'
    _TEST = {
        'url': 'https://audimedia.tv/en/vid/60-seconds-of-audi-sport-104-2015-wec-bahrain-rookie-test',
        'md5': '79a8b71c46d49042609795ab59779b66',
        'info_dict': {
            'id': '1565',
            'ext': 'mp4',
            'title': '60 Seconds of Audi Sport 104/2015 - WEC Bahrain, Rookie Test',
            'description': 'md5:60e5d30a78ced725f7b8d34370762941',
            'upload_date': '20151124',
            'timestamp': 1448354940,
            'duration': 74022,
            'view_count': int,
        }
    }
    # extracted from https://audimedia.tv/assets/embed/embedded-player.js (dataSourceAuthToken)
    _AUTH_TOKEN = 'e25b42847dba18c6c8816d5d8ce94c326e06823ebf0859ed164b3ba169be97f2'

    def _real_extract(self, url):
        display_id = self._match_id(url)
        webpage = self._download_webpage(url, display_id)

        raw_payload = self._search_regex(r'<script[^>]+class="amtv-embed"[^>]+id="([^"]+)"', webpage, 'raw payload')
        _, stage_mode, video_id, lang = raw_payload.split('-')

        # TODO: handle s and e stage_mode (live streams and ended live streams)
        if stage_mode not in ('s', 'e'):
            request = sanitized_Request(
                'https://audimedia.tv/api/video/v1/videos/%s?embed[]=video_versions&embed[]=thumbnail_image&where[content_language_iso]=%s' % (video_id, lang),
                headers={'X-Auth-Token': self._AUTH_TOKEN})
            json_data = self._download_json(request, video_id)['results']
            formats = []

            stream_url_hls = json_data.get('stream_url_hls')
            if stream_url_hls:
                m3u8_formats = self._extract_m3u8_formats(stream_url_hls, video_id, 'mp4', entry_protocol='m3u8_native', m3u8_id='hls', fatal=False)
                if m3u8_formats:
                    formats.extend(m3u8_formats)

            stream_url_hds = json_data.get('stream_url_hds')
            if stream_url_hds:
                f4m_formats = self._extract_f4m_formats(json_data.get('stream_url_hds') + '?hdcore=3.4.0', video_id, -1, f4m_id='hds', fatal=False)
                if f4m_formats:
                    formats.extend(f4m_formats)

            for video_version in json_data.get('video_versions'):
                video_version_url = video_version.get('download_url') or video_version.get('stream_url')
                if not video_version_url:
                    continue
                formats.append({
                    'url': video_version_url,
                    'width': int_or_none(video_version.get('width')),
                    'height': int_or_none(video_version.get('height')),
                    'abr': int_or_none(video_version.get('audio_bitrate')),
                    'vbr': int_or_none(video_version.get('video_bitrate')),
                })
            self._sort_formats(formats)

            return {
                'id': video_id,
                'title': json_data['title'],
                'description': json_data.get('subtitle'),
                'thumbnail': json_data.get('thumbnail_image', {}).get('file'),
                'timestamp': parse_iso8601(json_data.get('publication_date')),
                'duration': int_or_none(json_data.get('duration')),
                'view_count': int_or_none(json_data.get('view_count')),
                'formats': formats,
            }
