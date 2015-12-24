from __future__ import unicode_literals

import re
import json

from .common import InfoExtractor
from ..utils import (
    qualities,
)


class ImdbIE(InfoExtractor):
    IE_NAME = 'imdb'
    IE_DESC = 'Internet Movie Database trailers'
    _VALID_URL = r'http://(?:www|m)\.imdb\.com/video/imdb/vi(?P<id>\d+)'

    _TEST = {
        'url': 'http://www.imdb.com/video/imdb/vi2524815897',
        'info_dict': {
            'id': '2524815897',
            'ext': 'mp4',
            'title': 'Ice Age: Continental Drift Trailer (No. 2) - IMDb',
            'description': 'md5:9061c2219254e5d14e03c25c98e96a81',
        }
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage('http://www.imdb.com/video/imdb/vi%s' % video_id, video_id)
        descr = self._html_search_regex(
            r'(?s)<span itemprop="description">(.*?)</span>',
            webpage, 'description', fatal=False)
        player_url = 'http://www.imdb.com/video/imdb/vi%s/imdb/single' % video_id
        player_page = self._download_webpage(
            player_url, video_id, 'Downloading player page')
        # the player page contains the info for the default format, we have to
        # fetch other pages for the rest of the formats
        extra_formats = re.findall(r'href="(?P<url>%s.*?)".*?>(?P<name>.*?)<' % re.escape(player_url), player_page)
        format_pages = [
            self._download_webpage(
                f_url, video_id, 'Downloading info for %s format' % f_name)
            for f_url, f_name in extra_formats]
        format_pages.append(player_page)

        quality = qualities(['SD', '480p', '720p'])
        formats = []
        for format_page in format_pages:
            json_data = self._search_regex(
                r'<script[^>]+class="imdb-player-data"[^>]*?>(.*?)</script>',
                format_page, 'json data', flags=re.DOTALL)
            info = json.loads(json_data)
            format_info = info['videoPlayerObject']['video']
            f_id = format_info['ffname']
            formats.append({
                'format_id': f_id,
                'url': format_info['videoInfoList'][0]['videoUrl'],
                'quality': quality(f_id),
            })
        self._sort_formats(formats)

        return {
            'id': video_id,
            'title': self._og_search_title(webpage),
            'formats': formats,
            'description': descr,
            'thumbnail': format_info['slate'],
        }


class ImdbListIE(InfoExtractor):
    IE_NAME = 'imdb:list'
    IE_DESC = 'Internet Movie Database lists'
    _VALID_URL = r'http://www\.imdb\.com/list/(?P<id>[\da-zA-Z_-]{11})'
    _TEST = {
        'url': 'http://www.imdb.com/list/JFs9NWw6XI0',
        'info_dict': {
            'id': 'JFs9NWw6XI0',
            'title': 'March 23, 2012 Releases',
        },
        'playlist_count': 7,
    }

    def _real_extract(self, url):
        list_id = self._match_id(url)
        webpage = self._download_webpage(url, list_id)
        entries = [
            self.url_result('http://www.imdb.com' + m, 'Imdb')
            for m in re.findall(r'href="(/video/imdb/vi[^"]+)"\s+data-type="playlist"', webpage)]

        list_title = self._html_search_regex(
            r'<h1 class="header">(.*?)</h1>', webpage, 'list title')

        return self.playlist_result(entries, list_id, list_title)
