# -*- coding: utf8 -*-

import Readability_analysis
import Variable_list
import os
import json
import datetime
from dateutil import parser
import time
import sys
import collections
import string
import nltk
import re
from nltk.parse.stanford import StanfordParser
from nltk.tag import StanfordPOSTagger
from nltk.tokenize import MWETokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
import enchant
import shutil
from bs4 import BeautifulSoup

import time
import math


class Analysis:

	def __init__(self, date, analyze_type):
		self.jsonfile = ""
		self.jsondata = ""
		self.date = date

		self.folder_name = sys.argv[1].split("_")[0]

		self.story_data = ""
		self.updates_data = ""
		self.c_comments_data = ""
		self.b_comments_data = ""

		self.date_type_jsondata = dict()
		self.linguistic_result = dict()

		self.analyze_type = analyze_type

	def make_folder(self):

		if os.path.isdir("./Result/Analysis_" + Variable_list.sub_title_name) == False:
			os.mkdir("./Result/Analysis_" + Variable_list.sub_title_name)

		if os.path.isdir("./Result/Analysis_" + Variable_list.sub_title_name + "/basic_analysis") == False:
			os.mkdir("./Result/Analysis_" + Variable_list.sub_title_name + "/basic_analysis")

		if os.path.isdir("./text") == False:
			os.mkdir("./text")

		if os.path.isdir("./text/" + Variable_list.sub_title_name) == False:
			os.mkdir("./text/" + Variable_list.sub_title_name)

	def setinfo(self, project_url):
		self.original_url = project_url
		self.project_name = project_url.split("/")[5].strip()

		if os.path.isdir("./Result/Analysis_" + Variable_list.sub_title_name + "/basic_analysis/" + self.project_name) == False:
			os.mkdir("./Result/Analysis_" + Variable_list.sub_title_name + "/basic_analysis/" + self.project_name)


		if os.path.isfile("./Result/Analysis_" + Variable_list.sub_title_name + "/basic_analysis/" + self.project_name + "/S_" + self.project_name + "_" + str(self.date) + ".txt") == True and \
			os.path.isfile("./Result/Analysis_" + Variable_list.sub_title_name + "/basic_analysis/" + self.project_name + "/U_" + self.project_name + "_" + str(self.date) + ".txt") == True and \
			os.path.isfile("./Result/Analysis_" + Variable_list.sub_title_name + "/basic_analysis/" + self.project_name + "/C_" + self.project_name + "_" + str(self.date) + ".txt") == True and \
			os.path.isfile("./Result/Analysis_" + Variable_list.sub_title_name + "/basic_analysis/" + self.project_name + "/B_" + self.project_name + "_" + str(self.date) + ".txt") == True and \
			os.path.isfile("./Result/Analysis_" + Variable_list.sub_title_name + "/basic_analysis/" + self.project_name + "/Temporal_" + self.project_name + ".txt") == True:

			return "Already"

		# ## project가 분석이 이미 됐는지 안 됐는지 확인
		# Analysis_file = "./Result/Analysis_" + str(date_type) + "_" + Variable_list.sub_title_name + "_NER_result.txt"
		# if os.path.isfile(Analysis_file) == True:
		# 	f = open(Analysis_file, "r")
		#
		# 	line = f.readline()
		# 	while line:
		# 		file_project_name = line.split("\t")[0]
		# 		if self.project_name == file_project_name:
		# 			return "Already"
		# 		else:
		# 			line = f.readline()
		# 			continue
		# 	f.close()

	def file_read(self):
		if os.path.isfile("./Kick_data/" + self.project_name + ".txt") == True:
			self.jsonfile = open("./Kick_data/" + self.project_name + ".txt", "r")

		self.jsondata = self.jsonfile.readline()
		self.jsondata = json.loads(self.jsondata)

	def html_tag_remove(self, text):
		p = re.compile(r'<.*?>')
		text = p.sub('\n', text)
		text = text.replace("\n", " ")

		return text

	def getNodes(self, parent, phrases_count, clauses_count, noun_phrases_count):
		for node in parent:
			if type(node) is nltk.Tree:
				if node.label() == 'ROOT':
					pass
				else:
					if node.label() == "NP":
						phrases_count += 1
						noun_phrases_count += 1
					elif node.label() == "VP" or node.label() == "PP":
						phrases_count += 1
					elif node.label() == "S" or node.label() == "SBAR" or node.label() == "SBARQ" or node.label() == "SINV" or node.label() == "SQ":
						clauses_count += 1

				phrases = phrases_count
				clauses = clauses_count
				noun_phrases = noun_phrases_count
				phrases, clauses, noun_phrases = self.getNodes(node, 0, 0, 0)
				phrases_count += phrases
				clauses_count += clauses
				noun_phrases_count += noun_phrases
			else:
				pass
			# print "Word:", node

		return phrases_count, clauses_count, noun_phrases_count


	def remove_tag(self, text):
		remover = re.compile('<.*?>')
		text = re.sub(remover, '', text)
		return text


	def story_analysis(self):

		self.story_data = ""
		self.story_data = self.jsondata["story_content"]["description"]

		# # if self.story_data == "":
		# #	 print self.original_url


		if self.analyze_type == "analyze_text":
			self.postag(self.story_data, "story", 0)
		elif self.analyze_type == "make_text":
			self.tsv_file_make(self.story_data, "story")


	def update_analysis(self):

		self.updates_data = ""

		u_image = 0
		u_video = 0
		u_audio = 0

		viewable_update_count = 0
		total_update_count = 0

		if isinstance(self.date, int) == True:
			updates_date = 86400 * self.date
	# 	
		project_launched_at = datetime.datetime.fromtimestamp(self.jsondata["launched_at"]).strftime("%Y-%m-%d %H:%M:%S")
		project_launched_at = datetime.datetime.strptime(project_launched_at, "%Y-%m-%d %H:%M:%S")

		funding_period = self.jsondata["funding_period"].split(" ")
		end_date = str(funding_period[4]) + " " + str(funding_period[5]) + " " + str(funding_period[6])
		end_date = datetime.datetime.strptime(end_date, "%b %d, %Y")

		for num in range(0, len(self.jsondata["updates_content"])):
			each_update_date = datetime.datetime.fromtimestamp(
				self.jsondata["updates_content"][num]["updated_at"]).strftime("%Y-%m-%d %H:%M:%S")
			each_update_date = datetime.datetime.strptime(each_update_date, "%Y-%m-%d %H:%M:%S")

			# ##during funding period
			# if (end_date - each_update_date + datetime.timedelta(days=1)).total_seconds() >= 0:
			# 	total_update_count += 1
			# 	if self.jsondata["updates_content"][num].has_key("body"):
			# 		self.updates_data += (str(self.jsondata["updates_content"][num]["body"]) + "\n")
			# 		viewable_update_count += 1

			if self.date == "full":
				total_update_count += 1
				if "body" in self.jsondata["updates_content"][num]:
					self.updates_data += (str(self.jsondata["updates_content"][num]["body"]) + "\n")
					viewable_update_count += 1

					u_image += self.jsondata["updates_content"][num]["image_count"]
					u_video += self.jsondata["updates_content"][num]["video_count"]
					u_audio += self.jsondata["updates_content"][num]["audio_count"]

			elif (each_update_date - project_launched_at).total_seconds() <= updates_date:
				total_update_count += 1
				if "body" in self.jsondata["updates_content"][num]:
					self.updates_data += (str(self.jsondata["updates_content"][num]["body"]) + "\n")
					viewable_update_count += 1

					u_image += self.jsondata["updates_content"][num]["image_count"]
					u_video += self.jsondata["updates_content"][num]["video_count"]
					u_audio += self.jsondata["updates_content"][num]["audio_count"]



		self.date_type_jsondata[str(self.date) + "_U_image"] = u_image
		self.date_type_jsondata[str(self.date) + "_U_video"] = u_video
		self.date_type_jsondata[str(self.date) + "_U_audio"] = u_audio
		self.date_type_jsondata[str(self.date) + "_U_total_update_count"] = total_update_count
		self.date_type_jsondata[str(self.date) + "_U_viewable_update_count"] = viewable_update_count

		temporal_data = dict()
		if os.path.isfile("./Result/Analysis_" + Variable_list.sub_title_name + "/basic_analysis/" + self.project_name + "/Temporal_" + self.project_name + ".txt") == True:
			temporal_file = open("./Result/Analysis_" + Variable_list.sub_title_name + "/basic_analysis/" + self.project_name + "/Temporal_" + self.project_name + ".txt", "r")
			temporal_data = temporal_file.readline()
			temporal_data = json.loads(temporal_data)
			temporal_file.close()

		temporal_data = open("./Result/Analysis_" + Variable_list.sub_title_name + "/basic_analysis/" + self.project_name + "/Temporal_" + self.project_name + ".txt", "w")
		json.dump(self.date_type_jsondata, temporal_data)
		temporal_data.close()


		self.updates_data = self.html_tag_remove(self.updates_data)

		if self.analyze_type == "analyze_text":
			self.postag(self.updates_data, "update", viewable_update_count)
		elif self.analyze_type == "make_text":
			self.tsv_file_make(self.updates_data, "update")

	def comments_analysis(self):

		self.story_data = ""
		self.updates_data = ""
		self.c_comments_data = ""
		self.b_comments_data = ""

		creator_comments_count = 0
		backers_comments_count = 0

		comments = self.jsondata["comments_content"]
		creator_name = self.jsondata["creator"]["id"]
		creator_comments_list = dict()
		backers_comments_list = dict()
		date_list = dict()

		funding_period = self.jsondata["funding_period"].split(" ")
		start_date = str(funding_period[0]) + " " + str(funding_period[1]) + " " + str(funding_period[2])
		end_date = str(funding_period[4]) + " " + str(funding_period[5]) + " " + str(funding_period[6])
		start_date = datetime.datetime.strptime(start_date, "%b %d, %Y")
		end_date = datetime.datetime.strptime(end_date, "%b %d, %Y")

		period = str(funding_period[7])

		for num in range(0, int(period)):
			t = start_date + datetime.timedelta(days=(num + 1))
			t = t.timetuple()
			d = str(t.tm_year) + "-" + str(t.tm_mon).zfill(2) + "-" + str(t.tm_mday).zfill(2)

			creator_comments_list[d] = 0
			backers_comments_list[d] = 0
			date_list[d] = 0

		if isinstance(self.date, int) == True:
			comments_date = 86400 * self.date

		project_launched_at = datetime.datetime.fromtimestamp(self.jsondata["launched_at"]).strftime("%Y-%m-%d %H:%M:%S")
		project_launched_at = datetime.datetime.strptime(project_launched_at, "%Y-%m-%d %H:%M:%S")

		for comment in comments:

			comment_time = comment["created_at"]

			t = time.gmtime(comment_time)
			d = str(t.tm_year) + "-" + str(t.tm_mon).zfill(2) + "-" + str(t.tm_mday).zfill(2)

			comment_launched_at = datetime.datetime.utcfromtimestamp(comment_time).strftime('%Y-%m-%d %H:%M:%S')

			# #duing funding period
			# if (end_date - comment_launched_at + datetime.timedelta(days=1)).total_seconds() >= 0:
			# 	t = time.gmtime(comment_time)
			# 	d = str(t.tm_year) + "-" + str(t.tm_mon).zfill(2) + "-" + str(t.tm_mday).zfill(2)

			# 	if comment["author"]["id"] == creator_name:
			# 		self.c_comments_data += (str(comment["body"]) + "\n")
			# 		creator_comments_count += 1
			# 		if creator_comments_list.has_key(d) == True:
			# 			creator_comments_list[d] += 1
			# 		elif creator_comments_list.has_key(d) == False:
			# 			creator_comments_list[d] = 1
			# 			date_list[d] = 0
			# 	else:
			# 		self.b_comments_data += (str(comment["body"]) + "\n")
			# 		backers_comments_count += 1

			# 		if backers_comments_list.has_key(d) == True:
			# 			backers_comments_list[d] += 1
			# 		elif backers_comments_list.has_key(d) == False:
			# 			backers_comments_list[d] = 1
			# 			date_list[d] = 0

			if self.date == "full":
				if comment["author"]["id"] == creator_name:
					self.c_comments_data += (str(comment["body"]) + "\n")
					creator_comments_count += 1
					if d in creator_comments_list == True:
						creator_comments_list[d] += 1
					elif d in creator_comments_list == False:
						creator_comments_list[d] = 1
						date_list[d] = 0
				else:
					self.b_comments_data += (str(comment["body"]) + "\n")
					backers_comments_count += 1

					if d in backers_comments_list == True:
						backers_comments_list[d] += 1
					elif d in backers_comments_list == False:
						backers_comments_list[d] = 1
						date_list[d] = 0

			elif (comment_launched_at - project_launched_at).total_seconds() <= comments_date:
				if comment["author"]["id"] == creator_name:
					self.c_comments_data += (str(comment["body"]) + "\n")
					creator_comments_count += 1
					if d in creator_comments_list == True:
						creator_comments_list[d] += 1
					elif d in creator_comments_list == False:
						creator_comments_list[d] = 1
						date_list[d] = 0
				else:
					self.b_comments_data += (str(comment["body"]) + "\n")
					backers_comments_count += 1

					if d in backers_comments_list == True:
						backers_comments_list[d] += 1
					elif d in backers_comments_list == False:
						backers_comments_list[d] = 1
						date_list[d] = 0


		self.creator_file = open("./creator_data/" + str(self.jsondata["creator"]["id"]) + ".txt", "r")
		self.creator_data = self.creator_file.readline()
		self.creator_data = json.loads(self.creator_data)
		self.creator_file.close()

		creator_before_comment_count = 0
		creator_after_comment_count = 0

		for count in range(len(self.creator_data["comments"])):
			comment_time = self.creator_data["comments"][count]["datetime"]
			comment_time = datetime.datetime.fromisoformat(comment_time).timestamp()


			if self.creator_data["comments"][count]["where"] != self.project_name:
				if self.date == "full":
					if comment_time - self.jsondata["launched_at"] > 0:
						creator_after_comment_count += 1
					else:
						creator_before_comment_count += 1

				elif ((comment_time - project_launched_at).total_seconds() <= comments_date) and (
						comment_time - project_launched_at).total_seconds() > 0:
					creator_after_comment_count += 1

		if self.date == "full":
			self.date_type_jsondata["creator_before_comments"] = creator_before_comment_count

		self.date_type_jsondata[str(self.date) + "_creator_comments"] = creator_comments_count
		self.date_type_jsondata[str(self.date) + "_backers_comments"] = backers_comments_count
		self.date_type_jsondata[str(self.date) + "_total_comments"] = backers_comments_count + creator_comments_count
		self.date_type_jsondata[str(self.date) + "_creator_after_comments"] = creator_after_comment_count
		

		temporal_data = dict()
		if os.path.isfile("./Result/Analysis_" + Variable_list.sub_title_name + "/basic_analysis/" + self.project_name + "/Temporal_" + self.project_name + ".txt") == True:
			temporal_file = open("./Result/Analysis_" + Variable_list.sub_title_name + "/basic_analysis/" + self.project_name + "/Temporal_" + self.project_name + ".txt", "r")
			temporal_data = temporal_file.readline()
			temporal_data = json.loads(temporal_data)
			temporal_file.close()

		temporal_data = open("./Result/Analysis_" + Variable_list.sub_title_name + "/basic_analysis/" + self.project_name + "/Temporal_" + self.project_name + ".txt", "w")
		json.dump(self.date_type_jsondata, temporal_data)
		temporal_data.close()



		'''
		## 날짜에 따라서 정렬해서 보여주는 부분
		
		#order_date_list = collections.OrderedDict(sorted(date_list.items(), key=lambda t: t[0]))
		#f = open("./Result/Analysis_"+Variable_list.sub_title_name+"/"+self.project_name+"_comments.txt","w")
		#f.write("date\tc_comments\tb_comments"+"\n")
		for a in order_date_list.items():
		creator_value = 0
		backer_value = 0
		if creator_comments_list.has_key(a[0]) == True:
			creator_value = creator_comments_list[a[0]]
		else :
			creator_value = 0

		if backers_comments_list.has_key(a[0]) == True:
			backer_value = backers_comments_list[a[0]]
		else :
			backer_value = 0

		#f.write(a[0] +"\t" + str(creator_value)+ "\t" + str(backer_value)+"\n")

		#f.close()
		'''
		'''
		f = open("./Result/Analysis_"+str(date_type)+"_basic_information_comments.txt","a")
		f.write(str(creator_comments_count)+"\t"+str(backers_comments_count)+"\n")
		f.close()
		'''

		self.c_comments_data = self.c_comments_data
		self.b_comments_data = self.b_comments_data
		full_comments_data = self.c_comments_data + self.b_comments_data
		full_text_data = self.story_data + "\n" + self.updates_data + "\n" + self.c_comments_data + "\n" + self.b_comments_data


		if self.analyze_type == "analyze_text":
			self.postag(self.c_comments_data, "creator_comments", creator_comments_count)
			self.postag(self.b_comments_data, "backers_comments", backers_comments_count)
		elif self.analyze_type == "make_text":
			self.tsv_file_make(self.c_comments_data, "c_comment")
			self.tsv_file_make(self.b_comments_data, "b_comment")
			self.tsv_file_make(full_comments_data, "full_comment")
			self.tsv_file_make(full_text_data, "full_text")


	def script(self):
		if os.path.isfile("./scam_nonscam_script/" + self.project_name + ".txt") == False:
			self.script_text = ""
		else:
			self.script_text = open("./scam_nonscam_script/" + self.project_name + ".txt", "r").readlines()
			if len(self.script_text) == 0:
				self.script_text = ""
			else:
				self.script_text = self.script_text[0].strip()

		if self.analyze_type == "analyze_text":
			self.postag(self.script_text, "script")
		elif self.analyze_type == "make_text":
			self.tsv_file_make(self.script_text, "script")

	def readability_anlaysis(self, text, text_type):

		type_prefix = ""
		if text_type == "story":
			type_prefix = "s"
		elif text_type == "update":
			type_prefix = "u"
		elif text_type == "backers_comments":
			type_prefix = "b"
		elif text_type == "creator_comments":
			type_prefix = "c"
		elif text_type == "script":
			type_prefix = "sc"

		self.linguistic_result[str(type_prefix) + "_ari"] = 0
		self.linguistic_result[str(type_prefix) + "_CL"] = 0
		self.linguistic_result[str(type_prefix) + "_GF"] = 0
		self.linguistic_result[str(type_prefix) + "_FKG"] = 0
		self.linguistic_result[str(type_prefix) + "_FRE"] = 0

		if len(text.split()) != 0:
			rdb = Readability_analysis.Readability(text)
			self.linguistic_result[str(type_prefix) + "_ari"] = rdb.ARI()
			self.linguistic_result[str(type_prefix) + "_CL"] = rdb.ColemanLiauIndex()
			self.linguistic_result[str(type_prefix) + "_GF"] = rdb.GunningFogIndex()
			self.linguistic_result[str(type_prefix) + "_FKG"] = rdb.FleschKincaidGradeLevel()
			self.linguistic_result[str(type_prefix) + "_FRE"] = rdb.FleschReadingEase()

	def preprocessing(self, text, text_type):

		# self.linguistic_result["url"] = len()
		url_list = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$\-@\.&+:/?=]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
		url_len = len(url_list)
		for url in url_list:
			text = text.replace(url, "_url_")

		email_link = re.findall(r'[\w\.-]+@[\w\.-]+', text)
		email_len = len(email_link)
		for email in email_link:
			text = text.replace(email, "_email_")

		phone_list = re.findall(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', text)
		phone_len = len(phone_list)
		for phone in phone_list:
			text = text.replace(phone, "_phone_")


		type_prefix = ""
		if text_type == "story":
			type_prefix = "s"
		elif text_type == "update":
			type_prefix = "u"
		elif text_type == "backers_comments":
			type_prefix = "b"
		elif text_type == "creator_comments":
			type_prefix = "c"
		elif text_type == "script":
			type_prefix = "sc"

		self.linguistic_result[str(type_prefix) + "_email_link_count"] = email_len
		self.linguistic_result[str(type_prefix) + "_phone_count"] = phone_len
		self.linguistic_result[str(type_prefix) + "_url_link_count"] = url_len
		self.linguistic_result[str(type_prefix) + "_email_link_list"] = email_link
		self.linguistic_result[str(type_prefix) + "_phone_list"] = phone_list
		self.linguistic_result[str(type_prefix) + "_url_list"] = url_list


		filtered_sentences = []
		for sent in nltk.sent_tokenize(text):
			word_tokens = [word for word in nltk.word_tokenize(sent) if len(word) >= 2]

			word_tokens = [word.lower() for word in word_tokens]



			lmtzr = WordNetLemmatizer()
			word_tokens = [lmtzr.lemmatize(word) for word in word_tokens]

			sentence = ' '.join(word_tokens)
			if sentence != "":
				filtered_sentences.append(sentence)

		# stop = stopwords.words('english')
		# tokens = [token for token in tokens if token not in stop]

		##lemmatize past, current, future
		# tokens = [lmtzr.lemmatize(word, 'v') for word in tokens]

		return filtered_sentences

	def postag(self, text, text_type, count):

		# if text_type == "story":
		# 	if os.path.isdir("./Result/Analysis_" + Variable_list.sub_title_name + "/story_" + self.folder_name) == False:
		# 		os.mkdir("./Result/Analysis_" + Variable_list.sub_title_name + "/story_" + self.folder_name)
		# 	filename = open("./Result/Analysis_" + Variable_list.sub_title_name + "/story_" + self.folder_name + "/s_" + self.project_name + "_" + str(self.date) + ".txt", "w")
		# 	filename.write(text)
		# elif text_type == "update":
		# 	if os.path.isdir("./Result/Analysis_" + Variable_list.sub_title_name + "/updates_" + self.folder_name) == False:
		# 		os.mkdir("./Result/Analysis_" + Variable_list.sub_title_name + "/updates_" + self.folder_name)
		# 	filename = open("./Result/Analysis_" + Variable_list.sub_title_name + "/updates_" + self.folder_name + "/u_" + self.project_name + "_" + str(self.date) + ".txt", "w")
		# 	filename.write(text)
		# elif text_type == "creator_comments":
		# 	if os.path.isdir("./Result/Analysis_" + Variable_list.sub_title_name + "/c_comments_" + self.folder_name) == False:
		# 		os.mkdir("./Result/Analysis_" + Variable_list.sub_title_name + "/c_comments_" + self.folder_name)
		# 	filename = open("./Result/Analysis_" + Variable_list.sub_title_name + "/c_comments_" + self.folder_name + "/c_" + self.project_name + "_" + str(self.date) + ".txt", "w")
		# 	filename.write(text)
		# elif text_type == "backers_comments":
		# 	if os.path.isdir("./Result/Analysis_" + Variable_list.sub_title_name + "/b_comments_" + self.folder_name) == False:
		# 		os.mkdir("./Result/Analysis_" + Variable_list.sub_title_name + "/b_comments_" + self.folder_name)
		# 	filename = open("./Result/Analysis_" + Variable_list.sub_title_name + "/b_comments_" + self.folder_name + "/b_" + self.project_name + "_" + str(self.date) + ".txt", "w")
		# 	filename.write(text)
		# filename.close()


		type_prefix = ""
		if text_type == "story":
			type_prefix = "s"
		elif text_type == "update":
			type_prefix = "u"
		elif text_type == "backers_comments":
			type_prefix = "b"
		elif text_type == "creator_comments":
			type_prefix = "c"

		self.linguistic_result = {"Total_words": 0, "Adjectives": 0, "Adverbs": 0, "Verbs": 0, "Nouns": 0, "Sentences": 0,"punctuation": 0, \
				"Reference": 0, "mispell_words": 0, "Average_sentence_length": 0, "Average_word_length": 0, "Pausality": 0, "Modal_verb": 0, \
				"Function_words": 0, "phrases": 0, "clauses": 0, "lexical_complexity": 0, "Average_clauses": 0, "Average_noun_phrases": 0, \
				"noun_phrases": 0, "Expressivity": 0, "typo": 0, "redundancy": 0, "first_singular_people": 0, \
				"first_plural_people": 0, "second_people": 0, "third_people": 0,\
				"Adjective":0, "Adjective_comparative": 0, "Adjective_superlative": 0, "Adverb":0,"Adverb_comparative": 0, "Adverb_superlative": 0, \
				"Verb_base_form": 0, "Verb_past_tense": 0, "Verb_gerund_or_present_participle": 0,"Verb_past_participle": 0 ,\
				"Verb_non_3rd_person_singular_present": 0, "Verb_3rd_person_singular_present": 0, "Noun_singular_or_mass": 0, \
				"Noun_plural": 0, "Proper_noun_singular": 0, "Proper_noun_plural": 0}

		stanford_dir = './stanfordnlp/'

		pos_modelfile = stanford_dir + 'stanford-postagger-full-2020-11-17/models/english-left3words-distsim.tagger'
		pos_jarfile = stanford_dir + 'stanford-postagger-full-2020-11-17/stanford-postagger.jar'
		stpostag = StanfordPOSTagger(model_filename = pos_modelfile, path_to_jar = pos_jarfile, java_options="-Xms8g -Xmx16g")

		# parser_model_path = stanford_dir + "stanford-corenlp-4.2.0-models-english/edu/stanford/nlp/models/lexparser/englishPCFG.caseless.ser.gz"
		# parser_models_jar = stanford_dir + "stanford-parser-full-2020-11-17/stanford-parser-4.2.0-models.jar"
		# parser_path_to_jar = stanford_dir + "stanford-parser-full-2020-11-17/stanford-parser.jar"
		# stparser = StanfordParser(model_path=parser_model_path, path_to_models_jar=parser_models_jar,
		# 				path_to_jar=parser_path_to_jar, java_options="-Xms4g -Xmx8g")

		# stanford named entity recognition local file로 작동
		# ner_model_path = stanford_dir + "stanford-ner-2015-12-09/classifiers/english.all.3class.distsim.crf.ser.gz"
		# ner_path_to_jar = stanford_dir + "stanford-ner-2015-12-09/stanford-ner-3.6.0.jar"
		# stner = nltk.tag.StanfordNERTagger(model_path = ner_model_path, path_to_jar = ner_path_to_jar)

		self.readability_anlaysis(text, text_type)
		filtered_sentences = self.preprocessing(text, text_type)
		filtered_sentences_str = " ".join(filtered_sentences)

		# # printable = set(string.printable)
		# sentences = []
		# for sentence in sent_tokens:
		# 	if len(sentence.split(" "))<100:
		# 		# sentence = filter(lambda x: x in printable, sentence)
		# 		parse_sentence = stparser.raw_parse(sentence)
		# 		sentences.append(parse_sentence)

		# print (sentences)

		# for sentence in sentences:
		# 	for line in sentence:
		# 		phrases, clauses, noun_phrases = self.getNodes(line, 0, 0, 0)
		# 		self.linguistic_result["phrases"] += phrases
		# 		self.linguistic_result["clauses"] += clauses
		# 		self.linguistic_result["noun_phrases"] += noun_phrases

		self.linguistic_result["characters"] = len(filtered_sentences_str)
		self.linguistic_result["Total_words"] = len(filtered_sentences_str.split(" "))
		self.linguistic_result["Sentences"] = len(filtered_sentences)
		mis_check = enchant.Dict("en_US")

		unique_word = {}

		# stanford postag
		tokens = nltk.word_tokenize(filtered_sentences_str)
		tagged = stpostag.tag(tokens)

		for word in tagged:

			english_letter = set(string.ascii_letters)
			en_word = list(filter(lambda x: x in english_letter, word[0]))
			en_word = "".join(en_word)

			if en_word != "":
				if mis_check.check(en_word) == False:
					self.linguistic_result["mispell_words"] += 1

			if en_word in unique_word:
				unique_word[en_word] += 1
			else:
				unique_word[en_word] = 1

			if word[1] == "JJ" or word[1] == "JJR" or word[1] == "JJS":
				self.linguistic_result["Adjectives"] += 1
				if word[1] == "JJ":
					self.linguistic_result["Adjective"] += 1
				elif word[1] == "JJR":
					self.linguistic_result["Adjective_comparative"] += 1
				elif word[1] == "JJS":
					self.linguistic_result["Adjective_superlative"] += 1

			elif word[1] == "NN" or word[1] == "NNS" or word[1] == "NNP" or word[1] == "NNPS":
				self.linguistic_result["Nouns"] += 1
				if word[1] == "NN":
					self.linguistic_result["Noun_singular_or_mass"] += 1
				elif word[1] == "NNS":
					self.linguistic_result["Noun_plural"] += 1
				elif word[1] == "NNP":
					self.linguistic_result["Proper_noun_singular"] += 1
				elif word[1] == "NNPS":
					self.linguistic_result["Proper_noun_plural"] += 1

			elif word[1] == "RB" or word[1] == "RBR" or word[1] == "RBS":
				self.linguistic_result["Adverbs"] += 1
				if word[1] == "RB":
					self.linguistic_result["Adverb"] += 1
				elif word[1] == "RBR":
					self.linguistic_result["Adverb_comparative"] += 1
				elif word[1] == "RBS":
					self.linguistic_result["Adverb_superlative"] += 1

			elif word[1] == "VB" or word[1] == "VBD" or word[1] == "VBG" or word[1] == "VBN" or word[1] == "VBP" or word[1] == "VBZ":
				self.linguistic_result["Verbs"] += 1
				if word[1] == "VB":
					self.linguistic_result["Verb_base_form"] += 1
				elif word[1] == "VBD":
					self.linguistic_result["Verb_past_tense"] += 1
				elif word[1] == "VBG":
					self.linguistic_result["Verb_gerund_or_present_participle"] += 1
				elif word[1] == "VBN":
					self.linguistic_result["Verb_past_participle"] += 1
				elif word[1] == "VBP":
					self.linguistic_result["Verb_non_3rd_person_singular_present"] += 1
				elif word[1] == "VBZ":
					self.linguistic_result["Verb_3rd_person_singular_present"] += 1
			elif word[1] == "PRP":
				self.linguistic_result["Reference"] += 1
			elif word[1] == "MD":
				self.linguistic_result["Modal_verb"] += 1
			elif word[1] == "IN" or word[1] == "DT" or word[1] == "CC":
				self.linguistic_result["Function_words"] += 1
			else:
				for punctuation in string.punctuation:
					if word[0] == punctuation:
						self.linguistic_result["punctuation"] += 1

			first_singular_people = ["i", "my", "me", "mine"]
			first_plural_people = ["we", "ous", "us", "ours"]
			secondpeople = ["you", "your", "yours"]
			thirdpeople = ["he", "she", "it", "him", "her", "its", "his", "hers", "they", "them", "their", "theirs"]

			if [x for x in first_singular_people if word[0] == x]:
				self.linguistic_result["first_singular_people"] += 1
			elif [x for x in first_plural_people if word[0] == x]:
				self.linguistic_result["first_plural_people"] += 1
			elif [x for x in secondpeople if word[0] == x]:
				self.linguistic_result["second_people"] += 1
			elif [x for x in thirdpeople if word[0] == x]:
				self.linguistic_result["third_people"] += 1

		if len(unique_word) == 0 or self.linguistic_result["Total_words"] == 0:
			self.linguistic_result["lexical_complexity"] = 0
		else:
			self.linguistic_result["lexical_complexity"] = len(unique_word) / float(self.linguistic_result["Total_words"])

		if self.linguistic_result["Total_words"] == 0 or self.linguistic_result["Sentences"] == 0:
			self.linguistic_result["Average_sentence_length"] = 0
		else:
			self.linguistic_result["Average_sentence_length"] = self.linguistic_result["Total_words"] / float(self.linguistic_result["Sentences"])

		if self.linguistic_result["characters"] == 0 or self.linguistic_result["Sentences"] == 0:
			self.linguistic_result["Average_word_length"] = 0
		else:
			self.linguistic_result["Average_word_length"] = self.linguistic_result["characters"] / float(self.linguistic_result["Sentences"])

		if self.linguistic_result["clauses"] == 0 or self.linguistic_result["Sentences"] == 0:
			self.linguistic_result["Average_clauses"] = 0
		else:
			self.linguistic_result["Average_clauses"] = self.linguistic_result["clauses"] / float(self.linguistic_result["Sentences"])

		if self.linguistic_result["punctuation"] == 0 or self.linguistic_result["Sentences"] == 0:
			self.linguistic_result["Pausality"] = 0
		else:
			self.linguistic_result["Pausality"] = self.linguistic_result["punctuation"] / float(self.linguistic_result["Sentences"])

		if (self.linguistic_result["Adjectives"] + self.linguistic_result["Adverbs"]) == 0 or (self.linguistic_result["Nouns"] + self.linguistic_result["Verbs"]) == 0:
			self.linguistic_result["Expressivity"] = 0
		else:
			self.linguistic_result["Expressivity"] = (self.linguistic_result["Adjectives"] + self.linguistic_result["Adverbs"]) / float(
				(self.linguistic_result["Nouns"] + self.linguistic_result["Verbs"]))

		if self.linguistic_result["mispell_words"] == 0 or self.linguistic_result["Total_words"] == 0:
			self.linguistic_result["typo"] = 0
		else:
			self.linguistic_result["typo"] = self.linguistic_result["mispell_words"] / float(self.linguistic_result["Total_words"])

		if self.linguistic_result["Function_words"] == 0 or self.linguistic_result["Sentences"] == 0:
			self.linguistic_result["redundancy"] = 0
		else:
			self.linguistic_result["redundancy"] = self.linguistic_result["Function_words"] / float(self.linguistic_result["Sentences"])

		if text_type != "story":

			if count == 0 or self.linguistic_result["Total_words"] == 0:
				self.linguistic_result["Total_words_1"] = 0
				self.linguistic_result["Nouns_1"] = 0
				self.linguistic_result["Nouns_2"] = 0
				self.linguistic_result["Verbs_1"] = 0
				self.linguistic_result["Verbs_2"] = 0
				self.linguistic_result["Adjectives_1"] = 0
				self.linguistic_result["Adjectives_2"] = 0
				self.linguistic_result["Adverbs_1"] = 0
				self.linguistic_result["Adverbs_2"] = 0
				self.linguistic_result["Sentences_1"] = 0
				self.linguistic_result["clauses_1"] = 0
				self.linguistic_result["noun_phrases_1"] = 0
				self.linguistic_result["phrases_1"] = 0
				self.linguistic_result["punctuation_1"] = 0
				self.linguistic_result["punctuation_2"] = 0
				self.linguistic_result["mispell_words_1"] = 0
				self.linguistic_result["Function_words_1"] = 0
				self.linguistic_result["Function_words_2"] = 0
				self.linguistic_result["References_1"] = 0
				self.linguistic_result["References_2"] = 0
				self.linguistic_result["modal_verbs_1"] = 0
				self.linguistic_result["modal_verbs_2"] = 0
				self.linguistic_result["characters_1"] = 0
				self.linguistic_result["characters_2"] = 0
				self.linguistic_result["first_plural_people_1"] = 0
				self.linguistic_result["first_plural_people_2"] = 0
				self.linguistic_result["first_singular_people_1"] = 0
				self.linguistic_result["first_singular_people_2"] = 0
				self.linguistic_result["second_people_1"] = 0
				self.linguistic_result["second_people_2"] = 0
				self.linguistic_result["third_people_1"] = 0
				self.linguistic_result["third_people_2"] = 0

				self.linguistic_result[str(type_prefix) + "_email_link_count_1"] = 0
				self.linguistic_result[str(type_prefix) + "_phone_count_1"] = 0
				self.linguistic_result[str(type_prefix) + "_url_link_count_1"] = 0

			else:
				if self.linguistic_result["Total_words"] == 0:
					self.linguistic_result["Total_words_1"] = 0
				else:
					self.linguistic_result["Total_words_1"] = self.linguistic_result["Total_words"] / float(count)

				if self.linguistic_result["Nouns"] == 0:
					self.linguistic_result["Nouns_1"] = 0
					self.linguistic_result["Nouns_2"] = 0
				else:
					self.linguistic_result["Nouns_1"] = self.linguistic_result["Nouns"] / float(count)
					self.linguistic_result["Nouns_2"] = self.linguistic_result["Nouns"] / float(self.linguistic_result["Total_words"])

				if self.linguistic_result["Verbs"] == 0:
					self.linguistic_result["Verbs_1"] = 0
					self.linguistic_result["Verbs_2"] = 0
				else:
					self.linguistic_result["Verbs_1"] = self.linguistic_result["Verbs"] / float(count)
					self.linguistic_result["Verbs_2"] = self.linguistic_result["Verbs"] / float(self.linguistic_result["Total_words"])

				if self.linguistic_result["Adjectives"] == 0:
					self.linguistic_result["Adjectives_1"] = 0
					self.linguistic_result["Adjectives_2"] = 0
				else:
					self.linguistic_result["Adjectives_1"] = self.linguistic_result["Adjectives"] / float(count)
					self.linguistic_result["Adjectives_2"] = self.linguistic_result["Adjectives"] / float(self.linguistic_result["Total_words"])

				if self.linguistic_result["Adverbs"] == 0:
					self.linguistic_result["Adverbs_1"] = 0
					self.linguistic_result["Adverbs_2"] = 0
				else:
					self.linguistic_result["Adverbs_1"] = self.linguistic_result["Adverbs"] / float(count)
					self.linguistic_result["Adverbs_2"] = self.linguistic_result["Adverbs"] / float(self.linguistic_result["Total_words"])

				if self.linguistic_result["Sentences"] == 0:
					self.linguistic_result["Sentences_1"] = 0
				else:
					self.linguistic_result["Sentences_1"] = self.linguistic_result["Sentences"] / float(count)

				if self.linguistic_result["clauses"] == 0:
					self.linguistic_result["clauses_1"] = 0
				else:
					self.linguistic_result["clauses_1"] = self.linguistic_result["clauses"] / float(count)

				if self.linguistic_result["noun_phrases"] == 0:
					self.linguistic_result["noun_phrases_1"] = 0
				else:
					self.linguistic_result["noun_phrases_1"] = self.linguistic_result["noun_phrases"] / float(count)

				if self.linguistic_result["phrases"] == 0:
					self.linguistic_result["phrases_1"] = 0
				else:
					self.linguistic_result["phrases_1"] = self.linguistic_result["phrases"] / float(count)

				if self.linguistic_result["punctuation"] == 0:
					self.linguistic_result["punctuation_1"] = 0
					self.linguistic_result["punctuation_2"] = 0
				else:
					self.linguistic_result["punctuation_1"] = self.linguistic_result["punctuation"] / float(count)
					self.linguistic_result["punctuation_2"] = self.linguistic_result["punctuation"] / float(self.linguistic_result["Total_words"])

				if self.linguistic_result["mispell_words"] == 0:
					self.linguistic_result["mispell_words_1"] = 0
				else:
					self.linguistic_result["mispell_words_1"] = self.linguistic_result["mispell_words"] / float(count)

				if self.linguistic_result["Function_words"] == 0:
					self.linguistic_result["Function_words_1"] = 0
					self.linguistic_result["Function_words_2"] = 0
				else:
					self.linguistic_result["Function_words_1"] = self.linguistic_result["Function_words"] / float(count)
					self.linguistic_result["Function_words_2"] = self.linguistic_result["Function_words"] / float(self.linguistic_result["Total_words"])

				if self.linguistic_result["Reference"] == 0:
					self.linguistic_result["References_1"] = 0
					self.linguistic_result["References_2"] = 0
				else:
					self.linguistic_result["References_1"] = self.linguistic_result["Reference"] / float(count)
					self.linguistic_result["References_2"] = self.linguistic_result["Reference"] / float(self.linguistic_result["Total_words"])

				if self.linguistic_result["Modal_verb"] == 0:
					self.linguistic_result["modal_verbs_1"] = 0
					self.linguistic_result["modal_verbs_2"] = 0
				else:
					self.linguistic_result["modal_verbs_1"] = self.linguistic_result["Modal_verb"] / float(count)
					self.linguistic_result["modal_verbs_2"] = self.linguistic_result["Modal_verb"] / float(self.linguistic_result["Total_words"])

				if self.linguistic_result["characters"] == 0:
					self.linguistic_result["characters_1"] = 0
					self.linguistic_result["characters_2"] = 0
				else:
					self.linguistic_result["characters_1"] = self.linguistic_result["characters"] / float(count)
					self.linguistic_result["characters_2"] = self.linguistic_result["characters"] / float(self.linguistic_result["Total_words"])

				if self.linguistic_result["first_plural_people"] == 0:
					self.linguistic_result["first_plural_people_1"] = 0
					self.linguistic_result["first_plural_people_2"] = 0
				else:
					self.linguistic_result["first_plural_people_1"] = self.linguistic_result["first_plural_people"] / float(count)
					self.linguistic_result["first_plural_people_2"] = self.linguistic_result["first_plural_people"] / float(self.linguistic_result["Total_words"])

				if self.linguistic_result["first_singular_people"] == 0:
					self.linguistic_result["first_singular_people_1"] = 0
					self.linguistic_result["first_singular_people_2"] = 0
				else:
					self.linguistic_result["first_singular_people_1"] = self.linguistic_result["first_singular_people"] / float(count)
					self.linguistic_result["first_singular_people_2"] = self.linguistic_result["first_singular_people"] / float(self.linguistic_result["Total_words"])

				if self.linguistic_result["second_people"] == 0:
					self.linguistic_result["second_people_1"] = 0
					self.linguistic_result["second_people_2"] = 0
				else:
					self.linguistic_result["second_people_1"] = self.linguistic_result["second_people"] / float(count)
					self.linguistic_result["second_people_2"] = self.linguistic_result["second_people"] / float(self.linguistic_result["Total_words"])

				if self.linguistic_result["third_people"] == 0:
					self.linguistic_result["third_people_1"] = 0
					self.linguistic_result["third_people_2"] = 0
				else:
					self.linguistic_result["third_people_1"] = self.linguistic_result["third_people"] / float(count)
					self.linguistic_result["third_people_2"] = self.linguistic_result["third_people"] / float(self.linguistic_result["Total_words"])

				if self.linguistic_result[str(type_prefix) + "_email_link_count"] == 0:
					self.linguistic_result[str(type_prefix) + "_email_link_count_1"] = 0
				else:
					self.linguistic_result[str(type_prefix) + "_email_link_count_1"] = self.linguistic_result[str(type_prefix) + "_email_link_count"] / float(count)
				

				if self.linguistic_result[str(type_prefix) + "_phone_count"] == 0:
					self.linguistic_result[str(type_prefix) + "_phone_count_1"] = 0
				else:
					self.linguistic_result[str(type_prefix) + "_phone_count_1"] = self.linguistic_result[str(type_prefix) + "_phone_count"]/ float(count)


				if self.linguistic_result[str(type_prefix) + "_url_link_count"] == 0:
					self.linguistic_result[str(type_prefix) + "_url_link_count_1"] = 0
				else:
					self.linguistic_result[str(type_prefix) + "_url_link_count_1"] = self.linguistic_result[str(type_prefix) + "_url_link_count"] / float(count)

		if text_type == "story":
			full_data = open("./Result/Analysis_" + Variable_list.sub_title_name + "/basic_analysis/" + self.project_name + "/S_" + self.project_name + "_" + str(self.date) + ".txt", "w")
		elif text_type == "update":
			full_data = open("./Result/Analysis_" + Variable_list.sub_title_name + "/basic_analysis/" + self.project_name + "/U_" + self.project_name + "_" + str(self.date) + ".txt", "w")
		elif text_type == "creator_comments":
			full_data = open("./Result/Analysis_" + Variable_list.sub_title_name + "/basic_analysis/" + self.project_name + "/C_" + self.project_name + "_" + str(self.date) + ".txt", "w")
		elif text_type == "backers_comments":
			full_data = open("./Result/Analysis_" + Variable_list.sub_title_name + "/basic_analysis/" + self.project_name + "/B_" + self.project_name + "_" + str(self.date) + ".txt", "w")
		elif text_type == "script":
			full_data = open("./Result/Analysis_" + Variable_list.sub_title_name + "/basic_analysis/" + self.project_name + "/SC_" + self.project_name + "_" + str(self.date) + ".txt", "w")

		json.dump(self.linguistic_result, full_data)
		full_data.close()


	def tsv_file_make(self, text, text_type):
		text = " ".join(text.split())

		text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")
		filtered_text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', r'<url>', text)
		filtered_text2 = re.sub(r'[\w\.-]+@[\w\.-]+', r'<email>', filtered_text)
		filtered_text3 = re.sub(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', r'<phone>', filtered_text2)

		if filtered_text3.strip() == "":
			filtered_text3 = " "

		class_num = 0
		# if self.jsondata["state"] == "successful":
		# 	class_num = 1
		# elif self.jsondata["state"] == "failed":
		# 	class_num = 0



		scam_list = open("./scam_url.txt", "r").read().splitlines()
		suspected_list = open("./suspected_url.txt", "r").read().splitlines()
		non_scam_list = open("./nonscam_url.txt", "r").read().splitlines()

		if self.original_url in scam_list or self.original_url in suspected_list:
			class_num = 1
		elif self.original_url in non_scam_list:
			class_num = 0

		if os.path.isfile("./text/" + Variable_list.sub_title_name + "/" + text_type + "_" + sys.argv[3] + ".tsv") == False:
			f = open("./text/" + Variable_list.sub_title_name + "/" + text_type + "_" + sys.argv[3] + ".tsv", "a")
			f.write("ID\tsuccess_or_fail\tcontent\n")
			f.close()

		f = open("./text/" + Variable_list.sub_title_name + "/" + text_type + "_" + sys.argv[3] + ".tsv", "a")
		f.write("\"" + self.project_name + "\"" + "\t" + str(class_num) + "\t" + filtered_text3 + "\n")
		f.close()


	def ner(self):

		# pwd = os.getcwd()
		# if os.path.isdir("./Original/"+self.project_name) == False:
		#	 os.mkdir("./Original/"+self.project_name)

		# cmd = "cp ./Result/Analysis_" + Variable_list.sub_title_name +"/story_" + self.folder_name + "/s_" + self.project_name + "_" + str(self.date) + ".txt "\
		#	 + "./Result/Analysis_" + Variable_list.sub_title_name +"/updates_" + self.folder_name + "/u_" + self.project_name + "_" + str(self.date) + ".txt "\
		#	 + "./Result/Analysis_" + Variable_list.sub_title_name +"/comments_" + self.folder_name + "/c_" + self.project_name + "_" + str(self.date) + ".txt "\
		#	 + "./Result/Analysis_" + Variable_list.sub_title_name +"/script_" + self.folder_name + "/sc_" + self.project_name + "_" + str(self.date) + ".txt "\
		#	 + "./Original/"+self.project_name

		# os.system(cmd)
		# os.chdir("./Execute")
		# cmd2 = "java -jar -Xms512m -Xmx1024m extract.jar"
		# os.system(cmd2)
		# os.chdir(pwd)

		# time.sleep(1)

		s_loc_num = 0
		s_org_num = 0
		s_per_num = 0
		u_loc_num = 0
		u_org_num = 0
		u_per_num = 0
		c_loc_num = 0
		c_org_num = 0
		c_per_num = 0
		sc_loc_num = 0
		sc_org_num = 0
		sc_per_num = 0

		filename = open("./Extract/SUNer_s_" + self.project_name + "_" + str(self.date) + ".txt", "r").readlines()
		for num in range(len(filename)):
			if filename[num] == "LOCATION : \n":
				s_loc_num = filename[num + 2].split()[3]
			if filename[num] == "ORGANIZATION : \n":
				s_org_num = filename[num + 2].split()[3]
			if filename[num] == "PERSON : \n":
				s_per_num = filename[num + 2].split()[3]

		filename = open("./Extract/SUNer_u_" + self.project_name + "_" + str(self.date) + ".txt", "r").readlines()
		for num in range(len(filename)):
			if filename[num] == "LOCATION : \n":
				u_loc_num = filename[num + 2].split()[3]
			if filename[num] == "ORGANIZATION : \n":
				u_org_num = filename[num + 2].split()[3]
			if filename[num] == "PERSON : \n":
				u_per_num = filename[num + 2].split()[3]

		filename = open("./Extract/SUNer_c_" + self.project_name + "_" + str(self.date) + ".txt", "r").readlines()
		for num in range(len(filename)):
			if filename[num] == "LOCATION : \n":
				c_loc_num = filename[num + 2].split()[3]
			if filename[num] == "ORGANIZATION : \n":
				c_org_num = filename[num + 2].split()[3]
			if filename[num] == "PERSON : \n":
				c_per_num = filename[num + 2].split()[3]

		filename = open("./Extract/SUNer_sc_" + self.project_name + "_" + str(self.date) + ".txt", "r").readlines()
		for num in range(len(filename)):
			if filename[num] == "LOCATION : \n":
				sc_loc_num = filename[num + 2].split()[3]
			if filename[num] == "ORGANIZATION : \n":
				sc_org_num = filename[num + 2].split()[3]
			if filename[num] == "PERSON : \n":
				sc_per_num = filename[num + 2].split()[3]

		s_time = 0
		u_time = 0
		c_time = 0
		sc_time = 0

		filename = open("./Extract/SUTime_s_" + self.project_name + "_" + str(self.date) + ".txt", "r").readlines()
		s_time = filename[1].split()[3]

		filename = open("./Extract/SUTime_u_" + self.project_name + "_" + str(self.date) + ".txt", "r").readlines()
		u_time = filename[1].split()[3]

		filename = open("./Extract/SUTime_c_" + self.project_name + "_" + str(self.date) + ".txt", "r").readlines()
		c_time = filename[1].split()[3]

		filename = open("./Extract/SUTime_sc_" + self.project_name + "_" + str(self.date) + ".txt", "r").readlines()
		sc_time = filename[1].split()[3]

		if os.path.isfile("./Result/Analysis_" + str(self.date) + "_" + Variable_list.sub_title_name + "_NER_result.txt") == False:
			file = open("./Result/Analysis_" + str(self.date) + "_" + Variable_list.sub_title_name + "_NER_result.txt",'w')
			file.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t\n" % (
			"project_name", "s_loc_num", "s_org_num", \
			"s_per_num", "u_loc_num", "u_org_num", \
			"u_per_num", "c_loc_num", "c_org_num", "c_per_num", "s_time", "u_time", "c_time", "sc_loc_num", "sc_org_num", "sc_per_num", "sc_time"))

		if os.path.isfile(
				"./Result/Analysis_" + str(self.date) + "_" + Variable_list.sub_title_name + "_NER_result.txt") == True:
			file = open("./Result/Analysis_" + str(self.date) + "_" + Variable_list.sub_title_name + "_NER_result.txt",
					'a')
			file.write(
				str(self.project_name) + "\t" + str(s_loc_num) + "\t" + str(s_org_num) + "\t" + str(s_per_num) + "\t" \
				+ str(u_loc_num) + "\t" + str(u_org_num) + "\t" + str(u_per_num) + "\t" \
				+ str(c_loc_num) + "\t" + str(c_org_num) + "\t" + str(c_per_num) + "\t" \
				+ str(s_time) + "\t" + str(u_time) + "\t" + str(c_time) + "\t" \
				+ str(sc_loc_num) + "\t" + str(sc_org_num) + "\t" + str(sc_per_num) + "\t" + str(sc_time) \
				+ "\n")
		file.close()

		# shutil.rmtree("./Original/"+self.project_name)
