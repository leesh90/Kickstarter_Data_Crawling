
# -*- coding: utf8 -*-

import os
import Variable_list
from bs4 import BeautifulSoup
import datetime
import time
import re
import requests
import json
import urllib
#import Video_down
import ssl, socket
import urllib
import subprocess
import random
import urllib3
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

requests.packages.urllib3.disable_warnings()


class Information:
	def __init__(self):
		self.api_project_url = ""
		self.api_updates_url = ""
		self.api_comments_url = ""
		self.creator_profile_web_url = ""
		self.creator_profile_api_url = ""
		self.creator_url = ""
		self.json_data = dict()  # basic json information
		self.json_data2 = dict()  # All kinds of project information were collected here
		self.json_data_creator = dict()
		self.context = ssl._create_unverified_context()

		options = Options()
		options.add_argument("headless")
		# options.add_argument(random.choice(Variable_list.user_list))
		self.browser = webdriver.Chrome(executable_path="./chromedriver" ,options=options)
		self.browser.implicitly_wait(15)

	def setinfo(self, url):
		self.url = url
		project_url = url.split("/")
		self.project_name = project_url[5].strip()
		self.project_description_url = str(url) + "description"
		self.project_update_url = str(url) + "update"
		self.project_comments_url = str(url) + "comments"

		
	# def video_collect(self, video_url):
	# 	dw = Video_down.video_dw()
	# 	dw.setinfo(self.url)
	# 	# dw.add()
	# 	# dw.video_download()
	# 	dw.video_real_download(video_url)

	def request_url(self, url, request_type):

		self.agent_change()
		print (url)
		text = dict()
		
		if request_type == "api":
			request_text = requests.get(url, timeout=30, stream=True)
			request_text = request_text.text
			text = json.loads(request_text)

		elif request_type == "web":
			text = urllib.request.urlopen(url, timeout=30, context=self.context)

		self.requests_count()
		return text

	def requests_count(self):
		Variable_list.requests_num += 1
		Variable_list.total_requests_num += 1
		print (Variable_list.total_requests_num)

		num = random.randint(10,15)
		time.sleep(num)
		
		if Variable_list.requests_num == 30:
			Variable_list.requests_num = 0
			time.sleep(300)

	def agent_change(self):
		ua = UserAgent()
		self.header = {'User-Agent': str(ua.random)}

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

	def add(self):
		if os.path.isfile("./Kick_data/" + self.project_name + ".txt") is True:
			data = open("./Kick_data/" + self.project_name + ".txt", "r").readline()
			self.json_data2 = json.loads(data)
		else:
			return "Nofile"


	def collect_check(self, collection_type):

		if collection_type == "start":
			if os.path.isfile("./Kick_data/" + self.project_name + ".txt") is True:
				data = open("./Kick_data/" + self.project_name + ".txt", "r").readline()
				self.json_data2 = json.loads(data)

			else:
				return "Nofile"

		if collection_type == "update":
			if "update_check" in self.json_data2:
				if self.json_data2["update_check"] == True: #이미 수집이 완료됨
					return "continue"
				else:
					self.json_data2["update_check"] = False

		elif collection_type == "comment":
			if "comment_check" in self.json_data2:
				if self.json_data2["comment_check"] == True: #이미 수집이 완료됨
					return "continue"
				else:
					self.json_data2["comment_check"] = False 
		
		elif collection_type == "creator":
			if os.path.isfile("./creator_data/" + str(self.json_data2["creator"]["id"]) + ".txt") is True:
				return "Nocollect"
		
		elif collection_type == "backer_list":
			if "backers_check" in self.json_data2:
				if self.json_data2["backers_check"] == True:
					return "continue"
				else:
					self.json_data2["backers_check"] == False

		elif collection_type == "all":
			if "all_completes" in self.json_data2:
				if self.json_data2["all_completes"] == True and os.path.isfile("./creator_data/" + str(self.json_data2["creator"]["id"]) + ".txt") is True:
					return "continue"
			else:
				if "update_complete_time" in self.json_data2 and "comment_complete_time" in self.json_data2 and "backers_complete_time" in self.json_data2:
					self.json_data2["all_completes"] = True
					self.json_data2["all_complete_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
					self.savedata()
				
	# Extract basic json information file of project
	def Collect_substring_HTML(self, collect_type):

		htmltext = self.request_url(self.project_description_url, "web")
		soup = BeautifulSoup(htmltext, "lxml")

		if soup.find("div", attrs={"id": "hidden_project"}):
			return "hidden"

		script_text = ""
		for text in soup.findAll("script"):
			script_text += str(text)

		for data in script_text.split("\n"):
			if re.findall("window.current_project", data):

				c_data = data.replace("&amp;", " ").replace("&quot;", "\"").replace("&#39", "\'").replace("\\\\", "\\")
				c_data = c_data.replace("&quot;", "\"")
				c_data = c_data.replace("window.current_project = \"", "").replace("}}]}\";", "}}]}")

				if (c_data[len(c_data) - 1]) == ";" and (c_data[len(c_data) - 2]) == "\"":
					c_data = c_data[:len(c_data) - 2]
				self.json_data = json.loads(c_data)

				self.api_project_url = self.json_data["urls"]["api"]["project"]
				self.api_updates_url = self.json_data["urls"]["api"]["updates"]
				self.api_comments_url = self.json_data["urls"]["api"]["comments"]

		self.json_data2 = self.request_url(self.api_project_url, "api")

		if collect_type == "new":
			for period in soup.findAll("div", attrs={"class": "NS_campaigns__funding_period"}):
				funding_period = period.get_text().replace("\n", "").replace("\r", "").replace("Funding period","").replace("("," ").replace(")","")
				self.json_data2["funding_period"] = funding_period

			self.json_data2["story_content"] = {}
			self.json_data2["updates_content"] = []
			self.json_data2["comments_content"] = []

			self.creator_profile_web_url = self.json_data2["creator"]["urls"]["web"]["user"]
			self.creator_profile_api_url = self.json_data2["creator"]["urls"]["api"]["user"]

			self.savedata()

		elif collect_type == "add":

			self.creator_profile_web_url = self.json_data2["creator"]["urls"]["web"]["user"]
			self.creator_profile_api_url = self.json_data2["creator"]["urls"]["api"]["user"]

		elif collect_type == "video":

			self.agent_change()
			text = urllib.request.urlopen(self.api_project_url, timeout=30, context=self.context)
			self.requests_count()
			text = text.read()
			self.json_data2 = json.loads(text)

			if self.json_data2["video"] is not None:
				video_url = self.json_data2["video"]["base"]
				return video_url
			else:
				return "novideo"

	def story_description(self):

		if "story_complete_time" not in self.json_data2:
			story = ""
			self.browser.get(project_url + "description")
			self.requests_count()

			check = 0 
			try:
				time.sleep(2)
				story = self.browser.find_element_by_xpath('//*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div[1]/div/div[3]/div[1]')
				time.sleep(2)
			except NoSuchElementException:
				check = 1

			if check == 1:
				time.sleep(2)
				story = self.browser.find_element_by_class_name('rte__content')
				time.sleep(2)


			try:
				time.sleep(2)
				risks_and_challenges = self.browser.find_element_by_xpath('//*[@id="risks-and-challenges"]/p')
				time.sleep(2)
			except NoSuchElementException:

				try:
					time.sleep(2)
					risks_and_challenges = self.browser.find_element_by_xpath('//*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div[1]/div/div[3]/div[2]')
					time.sleep(2)
				except NoSuchElementException:
					time.sleep(2)
					risks_and_challenges = self.browser.find_element_by_xpath('//*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div[1]/div/div/div[6]')
					time.sleep(2)


			full_story = story.text.replace("\n", " ").replace("\r", " ").replace("\t", " ")
			full_story = ' '.join(full_story.split())

			full_risks_and_challenges = risks_and_challenges.text.replace("\n", " ").replace("\r", " ").replace("\t", " ")
			full_risks_and_challenges = ' '.join(full_risks_and_challenges.split())	

			self.json_data2["story_content"]["description"] = full_story
			self.json_data2["story_content"]["risk_and_challenges"] = full_risks_and_challenges


			story_content = self.browser.find_element_by_class_name('rte__content')
			time.sleep(2)

			image_list = []
			story_img = story_content.find_elements_by_tag_name('img')
			for img in story_img:
				image_list.append(img.get_attribute("src"))
			time.sleep(2)

			audio_list = []
			story_audio = story_content.find_elements_by_tag_name('embed')
			for audio in story_audio:
				audio_list.append(audio.get_attribute("src"))
			time.sleep(2)

			video_list = []
			# story_video = story_content.find_elements_by_tag_name('source')
			# for story in story_video:
			# 	if 'high.mp4' in story.get_attribute('src'):
			# 		continue
			# 	else:
			# 		video_list.append(story.get_attribute('src'))


			iframe_list = self.browser.find_elements_by_tag_name("iframe")
			time.sleep(2)
			for i, iframe in enumerate(iframe_list):
				self.browser.switch_to.frame(iframe_list[i])
				self.requests_count()
				video_page = self.browser.page_source
				video_page = BeautifulSoup(video_page, "html.parser")
				for video in video_page.findAll("iframe", attrs={"class":"embedly-embed"}):
					video_list.append(video['src'])

				self.browser.switch_to.default_content()
				time.sleep(2)

			self.json_data2["story_content"]["video_content"] = video_list
			self.json_data2["story_content"]["audio_content"] = audio_list
			self.json_data2["story_content"]["image_content"] = image_list

			self.json_data2["story_content"]["video_count"] = len(video_list)
			self.json_data2["story_content"]["audio_count"] = len(audio_list)
			self.json_data2["story_content"]["image_count"] = len(image_list)

			self.json_data2["story_complete_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			self.savedata()

	def html_tag_remove(self, text):
		p = re.compile(r'<.*?>')
		text = p.sub('\n', text)
		text = text.replace("\n", " ")

		return text

	# Update information of project
	def project_update_information(self):

		project_updates_content = []
		project_updates_json = dict()
		project_updates_json_save = dict()
		next_api_updates_url = ""


		#### 업데이트 한번도 안해서 파일이 남아있는게 아무것도 없으면~
		if os.path.isfile("./updates_temp/" + self.project_name + ".txt") == False:
			project_updates_json = self.request_url(self.api_updates_url, "api")

		#### 이전에 수집했던 업데이트 데이터가 남아있으면~
		else:
			temp_update_json_file = open("./updates_temp/" + self.project_name + ".txt", "r")
			temp_update_json_data = temp_update_json_file.readline()
			temp_update_json_data = json.loads(temp_update_json_data)

			project_updates_content = temp_update_json_data["updates_content"]
			project_updates_content = self.update_comments_collected_check(project_updates_content)

			next_api_updates_url = temp_update_json_data["next_api_url"]
			project_updates_json = self.request_url(next_api_updates_url, "api")

		update_check = True
		while update_check:
			if "more_updates" in project_updates_json["urls"]["api"]:
				for num in range(len(project_updates_json["updates"])):
					if "body" in project_updates_json["updates"][num]:
						project_updates_json["updates"][num]["body"] = self.html_tag_remove(project_updates_json["updates"][num]["body"])
						project_updates_json["updates"][num]["body"] = ' '.join(project_updates_json["updates"][num]["body"].split())


					if "update_media_complete_time" not in project_updates_json["updates"][num]:
						update_url = project_updates_json["updates"][num]["urls"]["web"]["update"]
						self.browser.get(update_url)
						self.requests_count()

						if "This post is for backers only" in self.browser.page_source:
							project_updates_json["updates"][num]["urls"]["web"]["update"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
						
						else:
							update_content = self.browser.find_element_by_class_name('rte__content')
							time.sleep(2)

							image_list = []
							story_img = update_content.find_elements_by_tag_name('img')
							time.sleep(2)
							for img in story_img:
								image_list.append(img.get_attribute("src"))

							audio_list = []
							story_audio = update_content.find_elements_by_tag_name('embed')
							time.sleep(2)
							for audio in story_audio:
								audio_list.append(audio.get_attribute("src"))

							video_list = []
							# story_video = update_content.find_elements_by_tag_name('source')
							# for story in story_video:
							# 	if 'high.mp4' in story.get_attribute('src'):
							# 		continue
							# 	else:
							# 		video_list.append(story.get_attribute('src'))


							iframe_list = self.browser.find_elements_by_tag_name("iframe")
							time.sleep(2)
							for i, iframe in enumerate(iframe_list):
								self.browser.switch_to.frame(iframe_list[i])
								self.requests_count()
								video_page = self.browser.page_source
								video_page = BeautifulSoup(video_page, "html.parser")
								for video in video_page.findAll("iframe", attrs={"class":"embedly-embed"}):
									video_list.append(video['src'])

								self.browser.switch_to.default_content()
								time.sleep(2)

							project_updates_json["updates"][num]["video_content"] = video_list
							project_updates_json["updates"][num]["audio_content"] = audio_list
							project_updates_json["updates"][num]["image_content"] = image_list

							project_updates_json["updates"][num]["video_count"] = len(video_list)
							project_updates_json["updates"][num]["audio_count"] = len(audio_list)
							project_updates_json["updates"][num]["image_count"] = len(image_list)

							project_updates_json["updates"][num]["update_media_complete_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

				project_updates_json["updates"] = self.update_comments_collected_check(project_updates_json["updates"])
				project_updates_content += project_updates_json["updates"]
				next_api_updates_url = project_updates_json["urls"]["api"]["more_updates"]


				f = open("./updates_temp/" + self.project_name + ".txt", "w")
				project_updates_json_save["updates_content"] = project_updates_content
				project_updates_json_save["next_api_url"] = next_api_updates_url
				json.dump(project_updates_json_save, f)
				f.close()
				
				project_updates_json = self.request_url(next_api_updates_url, "api")

			else:
				project_updates_content += project_updates_json["updates"]
				project_updates_content = self.update_comments_collected_check(project_updates_content)

				self.json_data2["updates_content"] = project_updates_content
				self.json_data2["update_check"] = True
				self.json_data2["update_complete_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
				update_check = False

				self.savedata()
	

	def update_comments_collected_check(self, updates):

		for num in range(len(updates)):
			if "update_comment_check" not in updates[num]:
				if "comments" in updates[num]["urls"]["api"]:
					updates[num]["comments_content"] = self.update_comments_information(updates[num]["urls"]["api"]["comments"])
				updates[num]["update_comment_check"] = True
				updates[num]["update_comment_complete_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

		return updates


	def update_comments_information(self, update_comment_url):

		update_comments_content = []
		each_update_comments_json = dict()
		each_update_comments_json_save = dict()
		next_api_updates_comments_url = ""

		url_split = update_comment_url.split("/")
		ID = str(url_split[5]) + "_" + str(url_split[7])

		if os.path.isfile("./updates_comments_temp/" + self.project_name + "_" + str(ID) +".txt") == False:
			each_update_comments_json = self.request_url(update_comment_url, "api")

		else:

			temp_update_comments_json_file = open("./updates_comments_temp/" + self.project_name + "_" + str(ID) +".txt", "r")
			temp_update_comments_json_data = temp_update_comments_json_file.readline()
			temp_update_comments_json_data = json.loads(temp_update_comments_json_data)

			if "update_comment_pre_collect_check" in temp_update_comments_json_data and temp_update_comments_json_data["update_comment_pre_collect_check"] == True:
				return temp_update_comments_json_data

			update_comments_content = temp_update_comments_json_data["comments_content"]
			next_api_updates_comments_url = temp_update_comments_json_data["next_api_url"]

			each_update_comments_json = self.request_url(next_api_updates_comments_url, "api")


		comment_check = True
		while comment_check:
			if "more_comments" in each_update_comments_json["urls"]["api"]:
				update_comments_content += each_update_comments_json["comments"]
				next_api_each_update_comments_url = each_update_comments_json["urls"]["api"]["more_comments"]

				f = open("./updates_comments_temp/" + self.project_name + "_" + str(ID) +".txt", "w")
				each_update_comments_json_save["comments_content"] = update_comments_content
				each_update_comments_json_save["next_api_url"] = next_api_each_update_comments_url
				json.dump(each_update_comments_json_save, f)
				f.close()

				each_update_comments_json = self.request_url(next_api_each_update_comments_url, "api")
			else:
				update_comments_content += each_update_comments_json["comments"]
				comment_check = False

				f = open("./updates_comments_temp/" + self.project_name + "_" + str(ID) +".txt", "w")
				each_update_comments_json_save["comments_content"] = update_comments_content
				each_update_comments_json_save["update_comment_pre_collect_check"] = True
				json.dump(each_update_comments_json_save, f)
				f.close()

		return update_comments_content



	def project_comments_information(self):

		
		project_comments_content = []
		project_comments_json = dict()
		next_api_comments_url = ""

		if os.path.isfile("./comments_temp/" + self.project_name + ".txt") == False:
			self.json_data3 = self.request_url(self.api_comments_url, "api")

		else:

			temp_comment_json_file = open("./comments_temp/" + self.project_name + ".txt", "r")
			temp_comment_json_data = temp_comment_json_file.readline()
			temp_comment_json_data = json.loads(temp_comment_json_data)

			project_comments_content = temp_comment_json_data["comments_content"]
			next_api_comments_url = temp_comment_json_data["next_api_url"]

			self.json_data3 = self.request_url(next_api_comments_url, "api")


		check = True
		while check:
			if "more_comments" in self.json_data3["urls"]["api"]:
				next_api_comments_url = self.json_data3["urls"]["api"]["more_comments"]
				project_comments_content += self.json_data3["comments"]

				# if len(project_comments_content) >= 1000:
				# 	check = False

				f = open("./comments_temp/" + self.project_name + ".txt", "w")
				project_comments_json["comments_content"] = project_comments_content
				project_comments_json["next_api_url"] = next_api_comments_url
				json.dump(project_comments_json, f)
				f.close()
			
				self.json_data3 = self.request_url(next_api_comments_url, "api")

			else:
				project_comments_content += self.json_data3["comments"]
				check = False

				self.json_data2["comments_content"] = project_comments_content
				self.json_data2["comment_check"] = True
				self.json_data2["comment_complete_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

				self.savedata()


	def creator_profile(self):

		self.creator_profile_web_url = self.json_data2["creator"]["urls"]["web"]["user"]
		self.creator_profile_api_url = self.json_data2["creator"]["urls"]["api"]["user"]

		self.json_data_creator = self.request_url(self.creator_profile_api_url, "api")

		self.creator_url = self.json_data2["urls"]["web"]["project"] + "/creator_bio"
		creatortext = self.request_url(self.creator_url, "web")
		creatorsoup = BeautifulSoup(creatortext, "lxml")

		self.json_data2["creator"]["collaborator"] = []
		if creatorsoup.find("div", attrs={"class": "pt3 pt7-sm mobile-hide row"}) is not None:
			collaborate_content = creatorsoup.find("div", attrs={"class": "pt3 pt7-sm mobile-hide row"})
			collaborate_list = collaborate_content.findAll("a")
			for line in collaborate_list:
				self.json_data2["creator"]["collaborator"].append({"url": line["href"], "name": line.get_text()})

		last_login = ""
		for time in creatorsoup.findAll("time", attrs={"class": "invisible-if-js js-adjust-time"}):
			last_login = time["datetime"]
		if last_login == "":
			last_login = "Null"
		self.json_data_creator["last_login"] = last_login

		facebook_link = ""
		facebook_friend = ""
		for facebook_account in creatorsoup.findAll("a", attrs={"class": "popup"}, href=True):
			if len(facebook_account.get_text()) is not None:
				facebook_link = facebook_account["href"]
				
				friend = facebook_account.get_text().split(" ")[0]
				if isinstance(friend, int):
					facebook_friend = int(friend)
		if facebook_link == "":
			facebook_link = "Null"
		if facebook_friend == "":
			facebook_friend = "Null"
		
		self.json_data_creator["facebook_link"] = facebook_link
		self.json_data_creator["facebook_friend_count"] = facebook_friend

		self.json_data_creator["external_link_list"] = []
		for text in creatorsoup.findAll("ul", attrs={"class":"links list f5 bold"}):
			for link in text.findAll("a"):
				self.json_data_creator["external_link_list"].append(link["href"])
		self.json_data_creator["link_count"] = len(self.json_data_creator["external_link_list"])

		
		creator_about_url = str(self.creator_profile_web_url) + "/about"
		creator_about = self.request_url(creator_about_url, "web")
		creator_about_soup = BeautifulSoup(creator_about, "lxml")

		biography = ""
		for text in creator_about_soup.findAll("div", attrs={"class": "readability"}):
			for text2 in text.findAll("p"):
				biography += text2.text.strip()
		self.json_data_creator["biography"] = biography
		
		
		creatorurl_text = self.request_url(self.creator_profile_web_url, "web")
		creatorurl_soup = BeautifulSoup(creatorurl_text, "lxml")

		self.json_data_creator["backed_project_list"] = []
		self.json_data_creator["created_project_list"] = []
		self.json_data_creator["comments"] = []

		for msg in creatorurl_soup.findAll("div", attrs={"class": "center"}):
			msg = msg.get_text().strip().split(" ")
			if msg[0] == "Sorry!":
				creator_data = open("./creator_data/" + str(self.json_data_creator["id"]) + ".txt", "w")
				json.dump(self.json_data_creator, creator_data)
				creator_data.close()
				return 0

		# ####backed list
		# count = 1
		# while count:
		# 	creatorurl_text = urllib.request.urlopen(self.creator_profile_web_url + "?page=" + str(count), timeout=30, context=self.context)
		# 	self.requests_count()
		# 	creatorurl_soup = BeautifulSoup(creatorurl_text, "lxml")

		# 	if creatorurl_soup.find("p", attrs={"class": "no-content"}) is not None:
		# 		break
		# 	else:
		# 		data = creatorurl_soup.findAll("ul", attrs={"class": "mobius"})
		# 		for each_project in data[0].findAll("div", attrs={"class": "react-user-prof-card"}):
		# 			project_set = json.loads(each_project["data-project"])
		# 			self.json_data_creator["backed_project_list"].append(project_set)
		# 	count += 1

		####created list
		creatorurl_text = self.request_url(self.creator_profile_web_url + "/created", "web")
		creatorurl_soup = BeautifulSoup(creatorurl_text, "lxml")

		data = creatorurl_soup.find("ol", attrs={"class": "project-card-list"})
		project_set = dict()
		project_set = json.loads(data.find("div")["data-projects"])
		self.json_data_creator["created_project_list"] = project_set


		count = 1
		while True:
			
			creatorurl_text = self.request_url(self.creator_profile_web_url + "/comments?page=" + str(count), "web")
			creatorurl_soup = BeautifulSoup(creatorurl_text, "lxml")

			value = True
			for li in creatorurl_soup.findAll("div", attrs={"id": "content-wrap"}):
				for href in li.findAll("a", href=True):
					if href["href"] == "/profile/" + str(self.json_data2["creator"]["id"]) + "/comments":
						if href.get_text().replace("\n", "") == "Comments(0)":
							value = False
					elif 'slug' in self.json_data_creator and href["href"] == "/profile/" + str(
							self.json_data_creator["slug"]) + "/comments":
						if href.get_text().replace("\n", "") == "Comments(0)":
							value = False
			if value == False:
				break

			for data in creatorurl_soup.findAll("li", attrs={"class": "activity-comment-project"}):
				comments = data.find("p", attrs={"class": "body"}).get_text()
				for each_p in data.findAll("p"):
					if each_p.find("a", attrs={"class": "read-more"}):
						a = each_p.find("a", attrs={"class": "read-more"})
						where = a['href'].split("/")
						where = where[3]
				# where = each_p.get_text().replace("\n","")

				datetime1 = data.find("time", attrs={"class": "js-adjust-time"})["datetime"]
				comments_set = dict()
				comments_set["datetime"] = datetime1
				comments_set["where"] = where
				comments_set["comments"] = comments
				self.json_data_creator["comments"].append(comments_set)

			for data in creatorurl_soup.findAll("li", attrs={"class": "activity-comment-post"}):
				comments = data.find("p", attrs={"class": "body"}).get_text()
				for each_p in data.findAll("p"):
					if each_p.find("a", attrs={"class": "read-more"}):
						a = each_p.find("a", attrs={"class": "read-more"})
						where = a["href"].split("/")
						where = where[3]

				datetime1 = data.find("time", attrs={"class": "js-adjust-time"})["datetime"]
				comments_set = dict()
				comments_set["datetime"] = datetime1
				comments_set["where"] = where
				comments_set["comments"] = comments
				self.json_data_creator["comments"].append(comments_set)

			if creatorurl_soup.find("li", attrs={"class": "page"}) == None or \
					creatorurl_soup.find("li", attrs={"class": "page"})["data-last_page"] == "true":
				break

			count += 1

		if self.json_data_creator["facebook_link"] == "Null":
			self.json_data_creator["facebook_check"] = facebook_check = "X"
		else:
			self.json_data_creator["facebook_check"] = facebook_check = "O"

		creator_data = open("./creator_data/" + str(self.json_data_creator["id"]) + ".txt", "w")
		json.dump(self.json_data_creator, creator_data)
		creator_data.close()

	def Data_caculation(self):
		
		creator_jsondata = dict()
		if os.path.isfile("./creator_data/" + str(self.json_data2["creator"]["id"]) + ".txt") == True:
			creator_jsonfile = open("./creator_data/" + str(self.json_data2["creator"]["id"]) + ".txt", "r")
			creator_jsondata = creator_jsonfile.readline()
			creator_jsondata = json.loads(creator_jsondata)
		else:
			creator_jsondata = self.json_data_creator
		
		# 프로젝트가 아이디 생성 후 몇 일 뒤 만들어졌는지, 프로젝트 생성 후 언제 상태가 바꼈는지 시간 계산
		# number_of_update = self.json_data2["updates_count"]
		# real_update_data_count = 0
		# for number in range(0, number_of_update):
		#	 if self.json_data2["update_contents"][number].has_key('body'):
		#		 real_update_data_count += 1

		created_at = datetime.datetime.fromtimestamp(creator_jsondata["created_at"]).strftime("%Y-%m-%d %H:%M:%S")
		project_launched_at = datetime.datetime.fromtimestamp(self.json_data2["launched_at"]).strftime(
			"%Y-%m-%d %H:%M:%S")
		state_changed_at = datetime.datetime.fromtimestamp(self.json_data2["state_changed_at"]).strftime(
			"%Y-%m-%d %H:%M:%S")

		created_at_time = datetime.datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
		project_launched_at_time = datetime.datetime.strptime(project_launched_at, "%Y-%m-%d %H:%M:%S")
		state_changed_at_time = datetime.datetime.strptime(state_changed_at, "%Y-%m-%d %H:%M:%S")

		time1 = (project_launched_at_time - created_at_time).total_seconds() / 3600
		time2 = (state_changed_at_time - project_launched_at_time).total_seconds() / 3600

		self.json_data2['time1'] = time1
		self.json_data2['time2'] = time2


		rewards_backers = 0
		for count in range(len(self.json_data2['rewards'])):
			if count > 0:
				rewards_backers += self.json_data2['rewards'][count]['backers_count']
		self.json_data2['total_rewards_backers'] = rewards_backers


	def backer_lists(self):
		self.json_data2["backers_list"] = []

		community_url = self.url + "community"
		try:
			community_text = self.request_url(community_url, "web")
		except urllib.error.HTTPError:
			self.json_data2["backers_top_country_list"] = []
			self.json_data2["backers_top_city_list"] = []
			self.json_data2["backers_check"] = True
			self.json_data2["backers_complete_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			self.savedata()

			return 0


		community_soup = BeautifulSoup(community_text, "lxml")

		##backers nation, number
		backers_number = community_soup.findAll("div", attrs={"class": "community-section__new_vs_existing"})
		for text in backers_number:
			for text2 in text.findAll("div", attrs={"class": "new-backers"}):
				self.json_data2["New backers"] = text2.find("div", attrs={"class": "count"}).text.strip()
			for text2 in text.findAll("div", attrs={"class": "existing-backers"}):
				self.json_data2["existing-backers"] = text2.find("div", attrs={"class": "count"}).text.strip()

		self.json_data2["backers_top_country_list"] = []
		self.json_data2["backers_top_city_list"] = []

		backers_come_from_country = community_soup.findAll("div",attrs={"class": "location-list js-locations-cities"})
		for text in backers_come_from_country[0].findAll("div", attrs={"class": "location-list__item js-location-item"}):
			backers_set = dict()
			city = text.find("div", attrs={"class": "primary-text js-location-primary-text"}).text.strip()
			backers_set["city"] = city
			country = text.find("div",attrs={"class": "secondary-text js-location-secondary-text"}).text.strip()
			backers_set["country"] = country
			backers_count = text.find("div",attrs={"class": "tertiary-text js-location-tertiary-text"}).text.strip()
			backers_count = backers_count.split(" ")[0]
			backers_set["count"] = backers_count.strip()
			self.json_data2["backers_top_city_list"].append(backers_set)

		backers_come_from_country = community_soup.findAll("div", attrs={"class": "location-list js-locations-countries"})
		for text in backers_come_from_country[0].findAll("div", attrs={"class": "location-list__item js-location-item"}):
			backers_set = dict()
			country = text.find("div", attrs={"class": "primary-text js-location-primary-text"}).text.strip()
			backers_set["country"] = country
			backers_count = text.find("div",
									  attrs={"class": "tertiary-text js-location-tertiary-text"}).text.strip()
			backers_count = backers_count.split(" ")[0]
			backers_set["count"] = backers_count.strip()
			self.json_data2["backers_top_country_list"].append(backers_set)

		self.json_data2["backers_check"] = True
		self.json_data2["backers_complete_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

		self.savedata()

	def savedata(self):
		full_data = open("./Kick_data/" + self.project_name + ".txt", "w")
		# full_data = open("./" + self.project_name + ".txt", "w")
		json.dump(self.json_data2, full_data)
		full_data.close()

		

