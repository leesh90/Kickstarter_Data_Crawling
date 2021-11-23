# -*- coding: utf8 -*-

import sys
import os
import urllib
import json
import urllib
import subprocess
import Variable_list


class video_dw:
	def setinfo(self, url):
		self.url = url
		project_url = url.split("/")
		self.project_name = project_url[5].strip()

	def probe(self, vid_file_path):
		if type(vid_file_path) != str:
			raise Exception('Gvie ffprobe a full file path of the video')
			return

		command = ["ffprobe",
				   "-loglevel", "quiet",
				   "-print_format", "json",
				   "-show_format",
				   "-show_streams",
				   vid_file_path
				   ]

		pipe = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		out, err = pipe.communicate()
		return json.loads(out)

	def duration(self, vid_file_path):
		_json = self.probe(vid_file_path)

		if 'format' in _json:
			if 'duration' in _json['format']:
				return float(_json['format']['duration'])

		if 'streams' in _json:
			for s in _json['streams']:
				if 'duration' in s:
					return float(s['duration'])

		raise Exception('I found no duration')

	def video_download(self, video_url):
		video_file_name = self.project_name + ".mp4"
		video_link = urllib.request.urlopen(video_url, timeout=10)
		f = open("./Result/Video_" + Variable_list.sub_title_name + "/" + video_file_name, "wb")
		f.write(video_link.read())
		f.close()
