# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor
from ..utils import (
    int_or_none,
    parse_iso8601,
)


class AMPIE(InfoExtractor):
    # parse Akamai Adaptive Media Player feed
    def _extract_feed_info(self, url):
        item = self._download_json(
            url, None, 'Downloading Akamai AMP feed',
            'Unable to download Akamai AMP feed')['channel']['item']

        video_id = item['guid']

        def get_media_node(name, default=None):
            media_name = 'media-%s' % name
            media_group = item.get('media-group') or item
            return media_group.get(media_name) or item.get(media_name) or item.get(name, default)

        thumbnails = []
        media_thumbnail = get_media_node('thumbnail')
        if media_thumbnail:
            if isinstance(media_thumbnail, dict):
                media_thumbnail = [media_thumbnail]
            for thumbnail_data in media_thumbnail:
                thumbnail = thumbnail_data['@attributes']
                thumbnails.append({
                    'url': self._proto_relative_url(thumbnail['url'], 'http:'),
                    'width': int_or_none(thumbnail.get('width')),
                    'height': int_or_none(thumbnail.get('height')),
                })

        subtitles = {}
        media_subtitle = get_media_node('subTitle')
        if media_subtitle:
            if isinstance(media_subtitle, dict):
                media_subtitle = [media_subtitle]
            for subtitle_data in media_subtitle:
                subtitle = subtitle_data['@attributes']
                lang = subtitle.get('lang') or 'en'
                subtitles[lang] = [{'url': subtitle['href']}]

        formats = []
        media_content = get_media_node('content')
        if isinstance(media_content, dict):
            media_content = [media_content]
        for media_data in media_content:
            media = media_data['@attributes']
            media_type = media['type']
            if media_type == 'video/f4m':
                f4m_formats = self._extract_f4m_formats(
                    media['url'] + '?hdcore=3.4.0&plugin=aasp-3.4.0.132.124',
                    video_id, f4m_id='hds', fatal=False)
                if f4m_formats:
                    formats.extend(f4m_formats)
            elif media_type == 'application/x-mpegURL':
                m3u8_formats = self._extract_m3u8_formats(
                    media['url'], video_id, 'mp4', m3u8_id='hls', fatal=False)
                if m3u8_formats:
                    formats.extend(m3u8_formats)
            else:
                formats.append({
                    'format_id': media_data['media-category']['@attributes']['label'],
                    'url': media['url'],
                    'tbr': int_or_none(media.get('bitrate')),
                    'filesize': int_or_none(media.get('fileSize')),
                })

        self._sort_formats(formats)

        return {
            'id': video_id,
            'title': get_media_node('title'),
            'description': get_media_node('description'),
            'thumbnails': thumbnails,
            'timestamp': parse_iso8601(item.get('pubDate'), ' '),
            'duration': int_or_none(media_content[0].get('@attributes', {}).get('duration')),
            'formats': formats,
        }
