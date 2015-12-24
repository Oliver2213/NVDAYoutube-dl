from __future__ import unicode_literals

import re

from .common import InfoExtractor
from ..compat import (
    compat_etree_fromstring,
    compat_urlparse,
)
from ..utils import (
    ExtractorError,
    int_or_none,
    sanitized_Request,
)


class VevoIE(InfoExtractor):
    """
    Accepts urls from vevo.com or in the format 'vevo:{id}'
    (currently used by MTVIE and MySpaceIE)
    """
    _VALID_URL = r'''(?x)
        (?:https?://www\.vevo\.com/watch/(?:[^/]+/(?:[^/]+/)?)?|
           https?://cache\.vevo\.com/m/html/embed\.html\?video=|
           https?://videoplayer\.vevo\.com/embed/embedded\?videoId=|
           vevo:)
        (?P<id>[^&?#]+)'''

    _TESTS = [{
        'url': 'http://www.vevo.com/watch/hurts/somebody-to-die-for/GB1101300280',
        "md5": "95ee28ee45e70130e3ab02b0f579ae23",
        'info_dict': {
            'id': 'GB1101300280',
            'ext': 'mp4',
            "upload_date": "20130624",
            "uploader": "Hurts",
            "title": "Somebody to Die For",
            "duration": 230.12,
            "width": 1920,
            "height": 1080,
            # timestamp and upload_date are often incorrect; seem to change randomly
            'timestamp': int,
        }
    }, {
        'note': 'v3 SMIL format',
        'url': 'http://www.vevo.com/watch/cassadee-pope/i-wish-i-could-break-your-heart/USUV71302923',
        'md5': 'f6ab09b034f8c22969020b042e5ac7fc',
        'info_dict': {
            'id': 'USUV71302923',
            'ext': 'mp4',
            'upload_date': '20140219',
            'uploader': 'Cassadee Pope',
            'title': 'I Wish I Could Break Your Heart',
            'duration': 226.101,
            'age_limit': 0,
            'timestamp': int,
        }
    }, {
        'note': 'Age-limited video',
        'url': 'https://www.vevo.com/watch/justin-timberlake/tunnel-vision-explicit/USRV81300282',
        'info_dict': {
            'id': 'USRV81300282',
            'ext': 'mp4',
            'age_limit': 18,
            'title': 'Tunnel Vision (Explicit)',
            'uploader': 'Justin Timberlake',
            'upload_date': 're:2013070[34]',
            'timestamp': int,
        },
        'params': {
            'skip_download': 'true',
        }
    }, {
        'note': 'No video_info',
        'url': 'http://www.vevo.com/watch/k-camp-1/Till-I-Die/USUV71503000',
        'md5': '8b83cc492d72fc9cf74a02acee7dc1b0',
        'info_dict': {
            'id': 'USUV71503000',
            'ext': 'mp4',
            'title': 'Till I Die - K Camp ft. T.I.',
            'duration': 193,
        },
        'expected_warnings': ['Unable to download SMIL file'],
    }]
    _SMIL_BASE_URL = 'http://smil.lvl3.vevo.com/'

    def _real_initialize(self):
        req = sanitized_Request(
            'http://www.vevo.com/auth', data=b'')
        webpage = self._download_webpage(
            req, None,
            note='Retrieving oauth token',
            errnote='Unable to retrieve oauth token',
            fatal=False)
        if webpage is False:
            self._oauth_token = None
        else:
            if 'THIS PAGE IS CURRENTLY UNAVAILABLE IN YOUR REGION' in webpage:
                raise ExtractorError('%s said: This page is currently unavailable in your region.' % self.IE_NAME, expected=True)

            self._oauth_token = self._search_regex(
                r'access_token":\s*"([^"]+)"',
                webpage, 'access token', fatal=False)

    def _formats_from_json(self, video_info):
        if not video_info:
            return []

        last_version = {'version': -1}
        for version in video_info['videoVersions']:
            # These are the HTTP downloads, other types are for different manifests
            if version['sourceType'] == 2:
                if version['version'] > last_version['version']:
                    last_version = version
        if last_version['version'] == -1:
            raise ExtractorError('Unable to extract last version of the video')

        renditions = compat_etree_fromstring(last_version['data'])
        formats = []
        # Already sorted from worst to best quality
        for rend in renditions.findall('rendition'):
            attr = rend.attrib
            format_note = '%(videoCodec)s@%(videoBitrate)4sk, %(audioCodec)s@%(audioBitrate)3sk' % attr
            formats.append({
                'url': attr['url'],
                'format_id': attr['name'],
                'format_note': format_note,
                'height': int(attr['frameheight']),
                'width': int(attr['frameWidth']),
            })
        return formats

    def _formats_from_smil(self, smil_doc):
        formats = []
        els = smil_doc.findall('.//{http://www.w3.org/2001/SMIL20/Language}video')
        for el in els:
            src = el.attrib['src']
            m = re.match(r'''(?xi)
                (?P<ext>[a-z0-9]+):
                (?P<path>
                    [/a-z0-9]+     # The directory and main part of the URL
                    _(?P<cbr>[0-9]+)k
                    _(?P<width>[0-9]+)x(?P<height>[0-9]+)
                    _(?P<vcodec>[a-z0-9]+)
                    _(?P<vbr>[0-9]+)
                    _(?P<acodec>[a-z0-9]+)
                    _(?P<abr>[0-9]+)
                    \.[a-z0-9]+  # File extension
                )''', src)
            if not m:
                continue

            format_url = self._SMIL_BASE_URL + m.group('path')
            formats.append({
                'url': format_url,
                'format_id': 'SMIL_' + m.group('cbr'),
                'vcodec': m.group('vcodec'),
                'acodec': m.group('acodec'),
                'vbr': int(m.group('vbr')),
                'abr': int(m.group('abr')),
                'ext': m.group('ext'),
                'width': int(m.group('width')),
                'height': int(m.group('height')),
            })
        return formats

    def _download_api_formats(self, video_id, video_url):
        if not self._oauth_token:
            self._downloader.report_warning(
                'No oauth token available, skipping API HLS download')
            return []

        api_url = compat_urlparse.urljoin(video_url, '//apiv2.vevo.com/video/%s/streams/hls?token=%s' % (
            video_id, self._oauth_token))
        api_data = self._download_json(
            api_url, video_id,
            note='Downloading HLS formats',
            errnote='Failed to download HLS format list', fatal=False)
        if api_data is None:
            return []

        m3u8_url = api_data[0]['url']
        return self._extract_m3u8_formats(
            m3u8_url, video_id, entry_protocol='m3u8_native', ext='mp4',
            preference=0)

    def _real_extract(self, url):
        video_id = self._match_id(url)

        webpage = None

        json_url = 'http://videoplayer.vevo.com/VideoService/AuthenticateVideo?isrc=%s' % video_id
        response = self._download_json(json_url, video_id)
        video_info = response['video'] or {}

        if not video_info and response.get('statusCode') != 909:
            if 'statusMessage' in response:
                raise ExtractorError('%s said: %s' % (self.IE_NAME, response['statusMessage']), expected=True)
            raise ExtractorError('Unable to extract videos')

        if not video_info:
            if url.startswith('vevo:'):
                raise ExtractorError('Please specify full Vevo URL for downloading', expected=True)
            webpage = self._download_webpage(url, video_id)

        title = video_info.get('title') or self._og_search_title(webpage)

        formats = self._formats_from_json(video_info)

        is_explicit = video_info.get('isExplicit')
        if is_explicit is True:
            age_limit = 18
        elif is_explicit is False:
            age_limit = 0
        else:
            age_limit = None

        # Download via HLS API
        formats.extend(self._download_api_formats(video_id, url))

        # Download SMIL
        smil_blocks = sorted((
            f for f in video_info.get('videoVersions', [])
            if f['sourceType'] == 13),
            key=lambda f: f['version'])
        smil_url = '%s/Video/V2/VFILE/%s/%sr.smil' % (
            self._SMIL_BASE_URL, video_id, video_id.lower())
        if smil_blocks:
            smil_url_m = self._search_regex(
                r'url="([^"]+)"', smil_blocks[-1]['data'], 'SMIL URL',
                default=None)
            if smil_url_m is not None:
                smil_url = smil_url_m
        if smil_url:
            smil_doc = self._download_smil(smil_url, video_id, fatal=False)
            if smil_doc:
                formats.extend(self._formats_from_smil(smil_doc))

        self._sort_formats(formats)
        timestamp = int_or_none(self._search_regex(
            r'/Date\((\d+)\)/',
            video_info['launchDate'], 'launch date', fatal=False),
            scale=1000) if video_info else None

        duration = video_info.get('duration') or int_or_none(
            self._html_search_meta('video:duration', webpage))

        return {
            'id': video_id,
            'title': title,
            'formats': formats,
            'thumbnail': video_info.get('imageUrl'),
            'timestamp': timestamp,
            'uploader': video_info['mainArtists'][0]['artistName'] if video_info else None,
            'duration': duration,
            'age_limit': age_limit,
        }
