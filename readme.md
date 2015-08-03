#NVDA Youtube-DL Add-on

* Authors: Hrvoje Katić <info@hrvojekatic.com>.
* Current version: 1.0dev

This addon integrates your NVDA screen reader with [Youtube-DL][1]. Youtube-DL is a small program to download videos from YouTube.com and a few more sites. To use this addon, you just select a URL address of the video by using standard Windows text selection commands, and then press NVDA+F8. The selected URL will be detected, and your video will be downloaded and converted automatically.
Go to NVDA menu, Youtube Downloader submenu to configure download formats and other options.

##Before you begin

Please read the following information in this section carefully.

###Legal notices

Although this addon and Youtube-DL are free, please keep in mind that downloading copyrighted material is illegal. Before you download anything, you agree that you will download only non-copyrighted material, and that you will be using downloaded material for your personal use only. Before downloading videos, please read terms of use for the service you are downloading from. If you don't agree with terms of use, please remove downloaded files in within 24 hours from your computer!

###External converters

Youtube-DL requires some external converters for getting your videos converted to MP3 and some other formats. This addon is configured to use FFMPEG converter by default, which needs to be obtained separately due to license restrictions. Even if you don't get FFMPEG, you may still download a video but the resulting file will be in M4A format.
Since FFMPEG is tricky to build manually on Windows, you can find pre-compiled binaries for 32-bit and 64-bit Windows at the following link: [http://ffmpeg.zeranoe.com/builds/][2]. If you have a 32-bit Windows, please download 32-bit static binaries. For 64-bit Windows, download 64-bit static binaries. The required binaries are located in 'bin' subfolder found inside the downloaded .7z archive. Copy all .exe files within this folder into your \Windows\System32 folder, or \Windows\SysWOW64 folder in case of 64-bit Windows. If you're still having problems with FFMPEG.exe detection on 64-bit Windows, try downloading both 32-bit and 64-bit static binaries and copy them to your System32 and SysWOW64 folders. Then restart NVDA if needed.

##Basic usage instructions

###Example 1: Downloading currently playing Youtube video

1. Open your Web browser.
2. Search for any video on Youtube that you would like to download.
3. Open a link with a video.
4. Press Control+L to set focus on the address bar. The URL address will be automatically selected when address bar has focus.
5. Press NVDA+F8 to start download. Youtube-DL will automatically download a video and convert it into the MP3 format in 192 KBPS bitrate by default.

###Example 2: Downloading currently playing Youtube video from a pasted link in the E-Mail message or a document

1. Open your E-Mail message or a document containing any Youtube links.
2. Arrow down to a line that contains URL address of a Youtube video.
3. Select URL with standard Windows text selection commands, and make sure that entire URL address is selected, otherwise You'll get an error and your video will not be downloaded.
4. Press NVDA+F8 to start download. Youtube-DL will automatically download a video and convert it into the MP3 format in 192 KBPS bitrate by default.

##Addon options menu

Go to NVDA menu, Youtube Downloader sub menu to access various options for this addon and Youtube-DL.

###Audio converter options

In the Audio Converter Options dialog you can configure in which format your video will be downloaded, and what quality will be applied.
Note: although Youtube-DL can download both video and audio formats, the current version of this addon supports downloading in audio formats only. The supported audio formats that you can choose are: MP3, Wave, Ogg Vorbis, AAC, M4A, and Opus.

###View downloaded videos

This menu option will open a folder with downloaded videos, where you can open them, move them to another folder or delete them if you wish.

[1]: https://rg3.github.io/youtube-dl/
[2]: http://ffmpeg.zeranoe.com/builds/
