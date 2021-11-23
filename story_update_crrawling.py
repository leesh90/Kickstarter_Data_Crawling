from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import json
import time
import datetime
import sys
from bs4 import BeautifulSoup
import Variable_list
import random


file = sys.argv[1]


options = Options()
# options.add_argument("--headless")
# options.add_argument(random.choice(Variable_list.user_list))
browser = webdriver.Chrome(executable_path="./chromedriver" ,options=options)
browser.implicitly_wait(15)

class selenium_collect:

	def __init__(self, url):
		self.url = url
		self.project_name = url.split("/")[5].strip()
		self.requests_num = 0

		jsonfile = open("./Kick_data/" + self.project_name + ".txt", "r")
		jsondata = jsonfile.readline()
		self.jsondata = json.loads(jsondata)	

	def requests_count(self):
		self.requests_num += 1
		time.sleep(2)
		
		if self.requests_num == 30:
			self.requests_num = 0
			time.sleep(300)


	def story(self):

		jsonfile = open("./Kick_data/" + self.project_name + ".txt", "r")
		jsondata = jsonfile.readline()
		self.jsondata = json.loads(jsondata)

		if "story_complete_time" not in self.jsondata:
			story = ""
			browser.get(project_url + "description")
			self.requests_count()

			check = 0 
			try:
				time.sleep(2)
				story = browser.find_element_by_xpath('//*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div[1]/div/div[3]/div[1]')
				time.sleep(2)
			except NoSuchElementException:
				check = 1

			if check == 1:
				time.sleep(2)
				story = browser.find_element_by_class_name('rte__content')
				time.sleep(2)


			try:
				time.sleep(2)
				risks_and_challenges = browser.find_element_by_xpath('//*[@id="risks-and-challenges"]/p')
				time.sleep(2)
			except NoSuchElementException:

				try:
					time.sleep(2)
					risks_and_challenges = browser.find_element_by_xpath('//*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div[1]/div/div[3]/div[2]')
					time.sleep(2)
				except NoSuchElementException:
					time.sleep(2)
					risks_and_challenges = browser.find_element_by_xpath('//*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div[1]/div/div/div[6]')
					time.sleep(2)


			full_story = story.text.replace("\n", " ").replace("\r", " ").replace("\t", " ")
			full_story = ' '.join(full_story.split())

			full_risks_and_challenges = risks_and_challenges.text.replace("\n", " ").replace("\r", " ").replace("\t", " ")
			full_risks_and_challenges = ' '.join(full_risks_and_challenges.split())	

			self.jsondata["story_content"]["description"] = full_story
			self.jsondata["story_content"]["risk_and_challenges"] = full_risks_and_challenges


			story_content = browser.find_element_by_class_name('rte__content')
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


			iframe_list = browser.find_elements_by_tag_name("iframe")
			time.sleep(2)
			for i, iframe in enumerate(iframe_list):
				browser.switch_to.frame(iframe_list[i])
				self.requests_count()
				video_page = browser.page_source
				video_page = BeautifulSoup(video_page, "html.parser")
				for video in video_page.findAll("iframe", attrs={"class":"embedly-embed"}):
					video_list.append(video['src'])

				browser.switch_to.default_content()
				time.sleep(2)

			self.jsondata["story_content"]["video_content"] = video_list
			self.jsondata["story_content"]["audio_content"] = audio_list
			self.jsondata["story_content"]["image_content"] = image_list

			self.jsondata["story_content"]["video_count"] = len(video_list)
			self.jsondata["story_content"]["audio_count"] = len(audio_list)
			self.jsondata["story_content"]["image_count"] = len(image_list)

			self.jsondata["story_complete_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			self.savedata()


	def update(self):


		jsonfile = open("./Kick_data/" + self.project_name + ".txt", "r")
		jsondata = jsonfile.readline()
		self.jsondata = json.loads(jsondata)

		for num in range(len(self.jsondata["updates_content"])):

			jsonfile = open("./Kick_data/" + self.project_name + ".txt", "r")
			jsondata = jsonfile.readline()
			self.jsondata = json.loads(jsondata)

			if "update_media_complete_time" not in self.jsondata["updates_content"][num]:
				update_url = self.jsondata["updates_content"][num]["urls"]["web"]["update"]
				print (update_url)
				browser.get(update_url)
				self.requests_count()

				if "This post is for backers only" in browser.page_source:
					self.jsondata["updates_content"][num]["update_media_complete_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
					self.savedata()
				
				else:
					update_content = browser.find_element_by_class_name('rte__content')
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


					iframe_list = browser.find_elements_by_tag_name("iframe")
					time.sleep(2)
					for i, iframe in enumerate(iframe_list):
						browser.switch_to.frame(iframe_list[i])
						self.requests_count()
						video_page = browser.page_source
						video_page = BeautifulSoup(video_page, "html.parser")
						for video in video_page.findAll("iframe", attrs={"class":"embedly-embed"}):
							video_list.append(video['src'])

						browser.switch_to.default_content()
						time.sleep(2)

					self.jsondata["updates_content"][num]["video_content"] = video_list
					self.jsondata["updates_content"][num]["audio_content"] = audio_list
					self.jsondata["updates_content"][num]["image_content"] = image_list

					self.jsondata["updates_content"][num]["video_count"] = len(video_list)
					self.jsondata["updates_content"][num]["audio_count"] = len(audio_list)
					self.jsondata["updates_content"][num]["image_count"] = len(image_list)

					self.jsondata["updates_content"][num]["update_media_complete_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
					self.savedata()

	def savedata(self):
		full_data = open("./Kick_data/" + self.project_name + ".txt", "w")
		json.dump(self.jsondata, full_data)
		full_data.close()


		
if __name__ == "__main__":

	file_name = sys.argv[1]
	url = open(file, "r").read().splitlines()
	for project_url in url:
		print (project_url)

		collect = selenium_collect(project_url)
		collect.story()
		collect.update()
	browser.quit()