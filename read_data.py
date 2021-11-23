# coding=utf-8
import json
import datetime
import Variable_list
import os
import collections
import pandas as pd
import random
import requests
import sys
import re
import csv
from shutil import copyfile

class json_read:

	def setinfo(self, url):
		self.url = url
		project_url = url.split("/")
		self.project_name = project_url[5].strip()
		self.project_descripiton_url = str(url) + "description"
		self.project_update_url = str(url) + "update"
		self.project_comments_url = str(url) + "comments"

		self.success_list = []
		self.fail_list = []

		self.jsonfile = ""
		self.jsonfile2 = ""
		self.jsondata = ""
		self.jsondata2 = ""


	def file_read(self):

		if os.path.isfile("./Kick_data/" + self.project_name + ".txt") == False:
			print (self.url)
			return "Nofile"

		self.jsonfile = open("./Kick_data/" + self.project_name + ".txt", "r")
		self.jsondata = self.jsonfile.readline()
		self.jsondata = json.loads(self.jsondata)
		self.jsonfile.close()


		self.creatorfile = open("./creator_data/" + str(self.jsondata["creator"]["id"]) + ".txt", "r")
		self.creatordata = self.creatorfile.readline()
		self.creatordata = json.loads(self.creatordata)
		self.creatorfile.close()

		for update in self.jsondata["updates_content"]:
			if update["is_public"] == True:
				print (update["video_count"])

		# copyfile("./Kick_data2/" + self.project_name + ".txt", "./Kick_data/" + self.project_name + ".txt")
		# # if "comment_check" not in self.jsondata or self.jsondata["comment_check"] == False:
		# # 	print (self.url)


		# if "comment_check" in self.jsondata2 and self.jsondata2["comment_check"] == True:
		# 	self.jsondata["comments_content"] = self.jsondata2["comments_content"]
		# 	self.jsondata["comment_check"] = True
		# 	self.jsondata["comment_complete_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

		# 	full_data = open("./Kick_data/" + self.project_name + ".txt", "w")
		# 	json.dump(self.jsondata, full_data)
		# 	full_data.close()

		# if "comment_check" not in self.jsondata:
		# 	print (self.url)
		# if int(self.jsondata["comments_count"]) != int(len(self.jsondata["comments_content"])):
		# 	print (self.url)
			# print (self.jsondata["comments_count"], len(self.jsondata["comments_content"]))

		
		
			

		# self.category = (self.jsondata["category"]["slug"]).split("/")[0]

		# if self.category == "technology":
		# 	print (self.url)

		# if self.jsondata["story_content"]["description"] == "":
		# 	f = open("story_check_url.txt", "a")
		# 	f.write(self.url + "\n")
		# 	f.close()

		# self.jsonfile2 = open("/Users/seunghun/Desktop/Data_arrangement/3cate/Full/Design/" + self.project_name + ".txt", "r")
		# self.jsondata2 = self.jsonfile2.readline()
		# self.jsondata2 = json.loads(self.jsondata2)

		# self.creatorfile = open("./creator_data/" + str(self.jsondata["creator"]["id"]) + ".txt", "r")
		# self.creatordata = self.creatorfile.readline()
		# self.creatordata = json.loads(self.creatordata)

		# if len(self.jsondata2["update_content"]) > 0 :
		# 	self.jsondata["update_check"] = True
		# 	self.jsondata["update_content"] = self.jsondata2["update_content"]

		# 	full_data = open("./Kick_data/" + self.project_name + ".txt", "w")
		# 	json.dump(self.jsondata, full_data)
		# 	full_data.close()


		# if len(self.jsondata2["comments_content"]) > 0 :
		# 	self.jsondata["comment_check"] = True
		# 	self.jsondata["comments_content"] = self.jsondata2["comments_content"]

		# 	full_data = open("./Kick_data/" + self.project_name + ".txt", "w")
		# 	json.dump(self.jsondata, full_data)
		# 	full_data.close()


		# print (self.jsondata2["story_content"]["description"])

		# 	self.jsondata["story_content"] = self.jsondata2["story_content"]


		# full_data = open("./Kick_data/" + self.project_name + ".txt", "w")
		# json.dump(self.jsondata, full_data)
		# full_data.close()
		
		# if (int(self.jsondata["updates_count"]) > len(self.jsondata["update_content"])) or (int(self.jsondata["comments_count"]) > len(self.jsondata["comments_content"])):
		# 	f = open("recollect.txt", "a")
		# 	f.write(self.url + "\n")
		# 	f.close()


		# if int(self.jsondata["updates_count"]) > len(self.jsondata["update_content"]) and len(self.jsondata["update_content"]) == 0:
		# 	f = open("update_unfinish_url.txt", "a")
		# 	f.write(self.url + "\t" + str(self.jsondata["updates_count"]) +"\t" + str(len(self.jsondata["update_content"]))+"\n")
		# 	f.close()
		# else:
		# 	f = open("update_finish_url.txt", "a")
		# 	f.write(self.url + "\t" + str(self.jsondata["updates_count"]) +"\t" + str(len(self.jsondata["update_content"]))+"\n")
		# 	f.close()

		# if int(self.jsondata["comments_count"]) > len(self.jsondata["comments_content"]) and len(self.jsondata["comments_content"]) == 0:
		# 	f = open("comment_unfinish_url.txt", "a")
		# 	f.write(self.url + "\t" + str(self.jsondata["comments_count"]) +"\t" + str(len(self.jsondata["comments_content"]))+"\n")
		# 	f.close()
		# else:
		# 	f = open("comment_finish_url.txt", "a")
		# 	f.write(self.url + "\t" + str(self.jsondata["comments_count"]) +"\t" + str(len(self.jsondata["comments_content"]))+"\n")
		# 	f.close()



		# if int(self.jsondata["comments_count"]) > len(self.jsondata["comments_content"]):
		# 	f = open("comment_check_url.txt", "a")
		# 	f.write(self.url + "\t" + str(self.jsondata["comments_count"]) +"\t" + str(len(self.jsondata["comments_content"]))+"\n")
		# 	f.close()

		# if ("update_check" in self.jsondata):
		# 	if (self.jsondata["update_check"] == True):
		# 		f = open("finished_url.txt", "a")
		# 		f.write(self.url + "\n")
		# 		f.close()
		# 	else:
		# 		f = open("unfinished_url.txt", "a")
		# 		f.write(self.url + "\n")
		# 		f.close()
		# else:
		# 	f = open("unfinished_url.txt", "a")
		# 	f.write(self.url + "\n")
		# 	f.close()


		# if ("update_check" in self.jsondata) and ("comment_check" in self.jsondata):
		# 	if (self.jsondata["update_check"] == True) and (self.jsondata["comment_check"] == True):
		# 		if len(self.jsondata["update_content"]) >= 1 and len(self.jsondata["comments_content"]) >= 1:
		# 			f = open("3category_url.txt", "a")
		# 			f.write(self.url + "\n")
		# 			f.close()
				
		# 		f = open("finished_url.txt", "a")
		# 		f.write(self.url + "\n")
		# 		f.close()
		# 	else:
		# 		f = open("unfinished_url.txt", "a")
		# 		f.write(self.url + "\n")
		# 		f.close()
		# else:
		# 	f = open("unfinished_url.txt", "a")
		# 	f.write(self.url + "\n")
		# 	f.close()
				

		# if (len(self.jsondata["update_content"]) >=1) and (len(self.jsondata["comments_content"]) >=1):

		# 	if self.jsondata["state"] == "successful":
		# 		Variable_list.success_list.append(self.url)
		# 	elif self.jsondata["state"] == "failed":
		# 		Variable_list.fail_list.append(self.url)
		# 	elif self.jsondata["state"] == "suspended":
		# 		Variable_list.suspended_list.append(self.url)
		# 	elif self.jsondata["state"] == "canceled":
		# 		Variable_list.canceled_list.append(self.url)


		# print len(self.jsondata["update_content"]), len(self.jsondata["comments_content"])

		# print self.jsondata["comments_content"]


		# if os.path.isdir("./url/" + sys.argv[1].split("_")[1]) == False:
		# 	os.mkdir("./url/" + sys.argv[1].split("_")[1])

		# if os.path.isfile("./url/kick_data/" + self.project_name + ".txt") == True:
			# copyfile("./kick_data/" + self.project_name + ".txt", "./" + self.project_name + ".txt")



		# if os.path.isfile("./Kick_data_game_design_5/" + self.project_name + ".txt") == True:
		# 	self.jsonfile = open("./Kick_data_game_design_5/" + self.project_name + ".txt", "r")
		# else:
		# 	copyfile("./Kick_data/" + self.project_name + ".txt", "./Kick_data_game_design_1/" + self.project_name + ".txt")				

		# if self.jsondata['state'] == "successful":
		# 	f = open("sucess_url.txt", "a")
		# 	f.write(self.url + "\n")
		# 	f.close()

		# elif self.jsondata['state'] == "failed":
		# 	f = open("fail_url.txt", "a")
		# 	f.write(self.url + "\n")
		# 	f.close()

		# if "comment_check" in self.jsondata:
		# 	if self.jsondata["comment_check"] == True:
		# 		f = open("comment_yes_url.txt", "a")
		# 		f.write(self.url + "\n")
		# 		f.close()

		# if "update_check" in self.jsondata:
		# 	if self.jsondata["update_check"] == False:
		# 		f = open("update_check_url.txt", "a")
		# 		f.write(self.url + "\n")
		# 		f.close()
		# else:
		# 	f = open("update_check_url.txt", "a")
		# 	f.write(self.url + "\n")
		# 	f.close()

		# if "comment_check" in self.jsondata:
		# 	if self.jsondata["comment_check"] == False:
		# 		f = open("comment_check_url.txt", "a")
		# 		f.write(self.url + "\n")
		# 		f.close()
		# else:
		# 	f = open("comment_check_url.txt", "a")
		# 	f.write(self.url + "\n")
		# 	f.close()


		# self.category = (self.jsondata["category"]["slug"]).split("/")[0]

		#art, comics, crafts, dance, design, fashion, film & video, food, games, journalism, music, photography ,publishing, technology, theater

		# if os.path.isdir("./statistics/"+ (self.jsondata["category"]["slug"]).split("/")[0]) == False:
		# 	os.mkdir("./statistics/"+ (self.jsondata["category"]["slug"]).split("/")[0])
		

		# count = 0
		# if "update_check" in self.jsondata:
		# 	if self.jsondata["update_check"] == True:
		# 		if "comment_check" in self.jsondata:
		# 			if self.jsondata["comment_check"] == True:
		# 				copyfile("./Kick_data_update_clear/Kick_data_" + update_alp + "/"+ self.project_name + ".txt", "./Kick_data_both_te/" + self.project_name + ".txt")
		# 			else:
		# 				copyfile("./Kick_data_update_clear/Kick_data_" + update_alp + "/"+ self.project_name + ".txt", "./Kick_data_comment_te/" + self.project_name + ".txt")
		# 		else:
		# 			copyfile("./Kick_data_update_clear/Kick_data_" + update_alp + "/"+ self.project_name + ".txt", "./Kick_data_comment_te/" + self.project_name + ".txt")
		# 	else:
		# 		copyfile("./Kick_data_update_clear/Kick_data_" + update_alp + "/"+ self.project_name + ".txt", "./Kick_data_update_te/" + self.project_name + ".txt")
		# else:
		# 	copyfile("./Kick_data_update_clear/Kick_data_" + update_alp + "/"+ self.project_name + ".txt", "./Kick_data_update_te/" + self.project_name + ".txt")
	

		# 업데이트 코멘트 통계치 계산

		# if "category" in self.jsondata:
		# 	self.category = (self.jsondata["category"]["slug"]).split("/")[0]
		# else:
		# 	return "Nofile"



		# print self.project_name + "\t" + self.jsondata['video']['base']

		# f = open("./Result/output_all_analysis_suspended_2017-12-29.csv","r")

		# if os.path.isfile("./Result/"+Variable_list.sub_title_name + "_video.txt") == False:
		#	 g = open("./Result/"+Variable_list.sub_title_name + "_video.txt", "a")
		#	 line = f.readline()
		#	 line = line.strip().split(",")
		#	 for ele in line:
		#		 g.write(str(ele)+"\t")
		#	 g.write("\n")
		#	 g.close()

		# if self.jsondata['video']['base'] is not None:
		#	print self.jsondata["state"]

		# story_data = self.jsondata["story_content"]["description"].decode("utf8")
		# story_data = story_data.replace("\t", " ")
		# story_data = story_data.replace("\"", "\\\"")
		# story_data = "\""+story_data+"\""

		# self.project_name = self.project_name.replace("\"", "\\\"")

		# if self.jsondata["updates_count"]

		# print self.jsondata["category"]["slug"].split("/")[0]
		# print self.jsondata["location"]["country"], self.jsondata["location"]["localized_name"]

		# g = open("./Result/"+Variable_list.sub_title_name + "_video.txt", "a")
		# line = f.readline()
		# check = False
		# while line:
		#	 line = line.strip().split(",")

		#	 if self.project_name.strip() == line[1].strip():
		#		 check = True
		#		 for ele in line:
		#			 g.write(str(ele)+"\t")
		#		 g.write("\n")
		#	 line = f.readline()

		# f.close()
		# g.close()

		# print self.jsondata['state']

		# f = open("./Result/" + Variable_list.sub_title_name + "_url.txt", "a")
		# if self.jsondata['state'] == "successful" or self.jsondata['state'] == "failed":
		#	 f.write(self.url + "\n")
		# f.close()

		# elif self.jsondata['video'] is not None:
		#	 print "ok"

		# print self.jsondata["category"]["slug"].split("/")[0]

		# f = open("./Result/no_video_" + Variable_list.sub_title_name + "_url.txt", "a")
		# g = open("./Result/ok_video_" + Variable_list.sub_title_name + "_url.txt", "a")
		# if self.jsondata['state'] == "successful" or self.jsondata['state'] == 'failed':
		#	 if self.jsondata["video"] is None:
		#		 f.write(self.url+"\n")
		#	 if self.jsondata["video"] is not None:
		#		 g.write(self.url+"\n")
		# f.close()
		# g.close()

		# project_launched_at = datetime.datetime.fromtimestamp(self.jsondata["launched_at"]).strftime("%Y-%m-%d %H:%M:%S")
		# project_launched_at = datetime.datetime.strptime(project_launched_at, "%Y-%m-%d %H:%M:%S")

		# # state_changed_at = datetime.datetime.fromtimestamp(self.jsondata["state_changed_at"]).strftime("%Y-%m-%d %H:%M:%S")
		# # state_changed_at = datetime.datetime.strptime(state_changed_at, "%Y-%m-%d %H:%M:%S")

		# funding_period = self.jsondata["funding_period"].split(" ")

		# # #print funding_period[7]
		# # change_time = ((state_changed_at - project_launched_at).total_seconds())/60/60/24
		# # if (change_time - float(funding_period[7])) >0:
		# #	 print "go"

		# #video last modified time distribution
		# f = open("./Result/" + Variable_list.sub_title_name+"_video_last_modified.txt", "r")
		# #g = open("./Result/" + Variable_list.sub_title_name+"_time_diff.txt","a")
		# line = f.readline()
		# while line:
		#	 line = line.strip().split("\t")

		#	 if self.project_name == line[0]:

		#		 video_date = line[2].split(" ")
		#		 video_date[2] = self.to_dict(video_date[2])
		#		 video_date2 = str(video_date[3])+"-"+str(video_date[2]) + "-" + str(video_date[1])
		#		 video_date2 = str(video_date2) + " " + str(video_date[4])
		#		 video_last_modified_time = datetime.datetime.strptime(video_date2, "%Y-%m-%d %H:%M:%S")

		#		 time_diff = (video_last_modified_time - project_launched_at).total_seconds()
		#		 print time_diff
		#		 #g.write(self.project_name+"\t"+ str(time_diff/60/60/24)+"\n")
		#		 return
		#	 line = f.readline()

		# f = open("./Result/"+ Variable_list.sub_title_name + "video_url.txt","a")

		# if self.jsondata["video"] is not None:
		#	 #f.write(self.url+"\n")
		#	 f.write(self.project_name + "\t" + self.jsondata["video"]["base"]+"\n")

		# f.close()

		# r = requests.get(self.jsondata['video']['base'])

		# f = open("./Result/video_modified_date.txt","a")

		# f.write(self.project_name + "\t" + str(r.headers['last-modified'])+"\n")
		# f.close()

		# f = open("./Result/" + Variable_list.sub_title_name+"_video.txt", "r")

		# line = f.readline()
		# while line:

		#	 line = line.strip().split("\t")

		#	 if line[0] == self.project_name:
		#		 if line[1] == "O":
		#			 g = open("Result/"+Variable_list.sub_title_name+"_video_ok_url.txt", "a")
		#			 g.write(self.url+"\n")
		#			 g.close()

		#	 line = f.readline()

		# launched_at = datetime.datetime.fromtimestamp(self.jsondata["launched_at"]).strftime("%Y-%m-%d %H:%M:%S")
		# launched_at = datetime.datetime.strptime(launched_at, "%Y-%m-%d %H:%M:%S")

		# print launched_at.year

		# launched_at = datetime.datetime.fromtimestamp(self.jsondata["launched_at"]).strftime("%Y-%m-%d %H:%M:%S")
		##launched_at = datetime.datetime.strptime(launched_at, "%Y-%m-%d %H:%M:%S")
		# print launched_at
		'''
		if os.path.isfile("c_date.txt") == True:
			self.date_file = open("c_date.txt",'r')
			self.date = self.date_file.readline()
			self.date = json.loads(self.date)


		launched_at = datetime.datetime.fromtimestamp(self.jsondata["launched_at"]).strftime("%Y-%m-%d %H:%M:%S")
		launched_at = datetime.datetime.strptime(launched_at, "%Y-%m-%d %H:%M:%S")


		for count in range(0, len(self.jsondata["creator"]["comments"])):
			comment_time = self.jsondata["creator"]["comments"][count]["datetime"]
			comment_time = comment_time[:19]
			comment_time = datetime.datetime.strptime(comment_time, "%Y-%m-%dT%H:%M:%S")

			if (self.jsondata["slug"] == self.jsondata["creator"]["comments"][count]["where"]):
				time_differ = (comment_time - launched_at + datetime.timedelta(days=1))
				if len(str(time_differ).split(" "))< 2:
					if 1 in self.date:
						self.date["1"] += 1
					else:
						self.date["1"] = 1
				else:
					c_date = int(str(time_differ).split(" ")[0])+1
					c_date = str(c_date)
					if c_date in self.date:
						self.date[c_date] += 1
					else:
						self.date[c_date] = 1


		file = open("c_date.txt","w")
		json.dump(self.date, file)
		file.close()
		'''

		'''
		time_list =[]
		if self.jsondata["updates_count"]>1:
			base_date = datetime.datetime(2015, 7, 1)
			last_update_time = datetime.datetime.fromtimestamp(self.jsondata["update_content"][0]["updated_at"]).strftime("%Y-%m-%d %H:%M:%S")
			last_update_time = datetime.datetime.strptime(last_update_time, "%Y-%m-%d %H:%M:%S")
			second_update_time = datetime.datetime.fromtimestamp(self.jsondata["update_content"][1]["updated_at"]).strftime("%Y-%m-%d %H:%M:%S")
			second_update_time = datetime.datetime.strptime(second_update_time, "%Y-%m-%d %H:%M:%S")

			if ((base_date - last_update_time).total_seconds() < 0) and (round(((last_update_time - second_update_time).total_seconds()) / 86400) <180):
				print str(self.project_name)+"\t\t"+str(last_update_time) +"\t\t"+ str(second_update_time)

				for num in range(0,len(self.jsondata["update_content"])):
					time = datetime.datetime.fromtimestamp(self.jsondata["update_content"][num]["updated_at"]).strftime("%Y-%m-%d %H:%M:%S")
					time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
					time_list.append(time.date())
		time_list.sort()
		print time_list
		#sorted(time_list, key=lambda d: map(int, d.split('-')))
		#print time_list
		'''

	def random_sampling(self):

		# viewable_update_count = 0
		# ###during funding period
		# funding_period = self.jsondata["funding_period"].split(" ")
		# end_date = str(funding_period[4]) + " " + str(funding_period[5]) + " " + str(funding_period[6])
		# end_date = datetime.datetime.strptime(end_date, "%b %d, %Y")

		# for num in range(0, len(self.jsondata["update_content"])):

		# 	each_update_date = datetime.datetime.fromtimestamp(
		# 		self.jsondata["update_content"][num]["updated_at"]).strftime("%Y-%m-%d %H:%M:%S")
		# 	each_update_date = datetime.datetime.strptime(each_update_date, "%Y-%m-%d %H:%M:%S")

		# 	###during funding period
		# 	if (end_date - each_update_date + datetime.timedelta(days=1)).total_seconds() >= 0:
		# 		if self.jsondata["update_content"][num].has_key("body"):
		# 			viewable_update_count += 1


		# comment_count = 0
		# comments = self.jsondata["comments_content"]
		# for comment in comments:
		# 	comment_time = comment["created_at"]
		# 	# comment_time = strict_rfc3339.rfc3339_to_timestamp(comment_time)

		# 	Time_diff = datetime.timedelta(hours=4)
		# 	comment_launched_at = datetime.datetime.fromtimestamp(comment_time).strftime("%Y-%m-%d %H:%M:%S")
		# 	comment_launched_at = datetime.datetime.strptime(comment_launched_at, "%Y-%m-%d %H:%M:%S")
		# 	comment_launched_at = comment_launched_at + Time_diff  ## comments timezone is UTC-4:00

		# 	##duing funding period
		# 	if (end_date - comment_launched_at + datetime.timedelta(days=1)).total_seconds() >= 0:
		# 		comment_count += 1

		if self.jsondata["updates_count"] >=1 and self.jsondata["comments_count"] >=1:
			if self.jsondata["state"] == "successful":
				Variable_list.success_list.append(self.url)
			elif self.jsondata["state"] == "failed":
				Variable_list.fail_list.append(self.url)
			
	def random_sampling2(self):

		first_random = random.sample(Variable_list.success_list, 102)
		# second_random = random.sample(Variable_list.fail_list, 1527)

		# f = open("UCmore1_" + Variable_list.sub_title_name + "_url.txt", "a")
		# for line in Variable_list.success_list:
		# 	f.write(line.strip() + "\n")
		# for line in Variable_list.fail_list:
		# 	f.write(line.strip() + "\n")
		# f.close()

		# f = open("Random_" + Variable_list.sub_title_name + "_url.txt", "a")
		# for line in Variable_list.success_list:
		# 	f.write(line.strip() + "\n")
		# for line in Variable_list.fail_list:
		# 	f.write(line.strip() + "\n")
		# f.close()

		# f = open("DuringPeriod_" + Variable_list.sub_title_name + "_url.txt", "a")
		# for line in Variable_list.success_list:
		# 	f.write(line.strip() + "\n")
		# for line in Variable_list.fail_list:
		# 	f.write(line.strip() + "\n")
		# f.close()



		f = open("UCmore1_" + Variable_list.sub_title_name + "_url.txt", "a")
		for line in first_random:
			f.write(line.strip() + "\n")
		# for line in second_random:
		# 	f.write(line.strip() + "\n")
		f.close()



	def statistics_print(self):

		if self.jsondata["state"] == "successful":
			if self.jsondata["updates_count"] in Variable_list.updates_success_statistics:
				Variable_list.updates_success_statistics[self.jsondata["updates_count"]] += 1
			else:
				Variable_list.updates_success_statistics[self.jsondata["updates_count"]] = 1

			if self.jsondata["comments_count"] in Variable_list.comments_success_statistics:
				Variable_list.comments_success_statistics[self.jsondata["comments_count"]] += 1
			else:
				Variable_list.comments_success_statistics[self.jsondata["comments_count"]] = 1

		elif self.jsondata["state"] == "failed":
			if self.jsondata["updates_count"] in Variable_list.updates_fail_statistics:
				Variable_list.updates_fail_statistics[self.jsondata["updates_count"]] += 1
			else:
				Variable_list.updates_fail_statistics[self.jsondata["updates_count"]] = 1

			if self.jsondata["comments_count"] in Variable_list.comments_fail_statistics:
				Variable_list.comments_fail_statistics[self.jsondata["comments_count"]] += 1
			else:
				Variable_list.comments_fail_statistics[self.jsondata["comments_count"]] = 1

	def statistics_print2(self):
		updates_success_stat = collections.OrderedDict(sorted(Variable_list.updates_success_statistics.items()))
		updates_fail_stat = collections.OrderedDict(sorted(Variable_list.updates_fail_statistics.items()))
		comments_success_stat = collections.OrderedDict(sorted(Variable_list.comments_success_statistics.items()))
		comments_fail_stat = collections.OrderedDict(sorted(Variable_list.comments_fail_statistics.items()))

		updates_success_list = updates_success_stat.items()
		updates_fail_list = updates_fail_stat.items()
		comments_success_list = comments_success_stat.items()
		comments_fail_list = comments_fail_stat.items()

		df = pd.DataFrame(updates_success_list, columns=['Number of updates', 'count'])
		df["%"] = df["count"] / pd.Series(df["count"]).sum() * 100
		df = df.sort_values(by=['Number of updates'], axis=0, ascending=False)
		df["%sum"] = df["%"].cumsum()
		df = df.reset_index(drop=True)

		df1 = pd.DataFrame(updates_fail_list, columns=['Number of updates', 'count'])
		df1["%"] = df1["count"] / pd.Series(df1["count"]).sum() * 100
		df1 = df1.sort_values(by=['Number of updates'], axis=0, ascending=False)
		df1["%sum"] = df1["%"].cumsum()
		df1 = df1.reset_index(drop=True)

		df2 = pd.DataFrame(comments_success_list, columns=['Number of comments', 'count'])
		df2["%"] = df2["count"] / pd.Series(df2["count"]).sum() * 100
		df2 = df2.sort_values(by=['Number of comments'], axis=0, ascending=False)
		df2["%sum"] = df2["%"].cumsum()
		df2 = df2.reset_index(drop=True)

		df3 = pd.DataFrame(comments_fail_list, columns=['Number of comments', 'count'])
		df3["%"] = df3["count"] / pd.Series(df3["count"]).sum() * 100
		df3 = df3.sort_values(by=['Number of comments'], axis=0, ascending=False)
		df3["%sum"] = df3["%"].cumsum()
		df3 = df3.reset_index(drop=True)

		per_30_list = []
		per_50_list = []
		per_80_list = []

		per_30_list.append((self.jsondata["category"]["slug"]).split("/")[0])
		per_50_list.append((self.jsondata["category"]["slug"]).split("/")[0])
		per_80_list.append((self.jsondata["category"]["slug"]).split("/")[0])

		total_sum_count = df["count"].sum()
		sum_count = 0
		per_30_number = 0
		check_30 = False
		per_50_number = 0
		check_50 = False
		per_80_number = 0
		check_80 = False
		for num in range(0,len(df)):
			sum_count = sum_count + df.loc[num,"count"]
			percent = sum_count / float(total_sum_count)

			if percent >= 0.3 and check_30 == False:
				per_30_number = df.loc[num][0]
				per_30_list.append(per_30_number)
				check_30 = True
			if percent >= 0.5 and check_50 == False:
				per_50_number = df.loc[num][0]
				per_50_list.append(per_50_number)
				check_50 = True
			if percent >= 0.8 and check_80 == False:
				per_80_number = df.loc[num][0]
				per_80_list.append(per_80_number)
				check_80 = True
				break

		total_sum_count = df1["count"].sum()
		sum_count = 0
		per_30_number = 0
		check_30 = False
		per_50_number = 0
		check_50 = False
		per_80_number = 0
		check_80 = False
		for num in range(0,len(df1)):
			sum_count = sum_count + df1.loc[num,"count"]
			percent = sum_count / float(total_sum_count)

			if percent >= 0.3 and check_30 == False:
				per_30_number = df1.loc[num][0]
				per_30_list.append(per_30_number)
				check_30 = True
			if percent >= 0.5 and check_50 == False:
				per_50_number = df1.loc[num][0]
				per_50_list.append(per_50_number)
				check_50 = True
			if percent >= 0.8 and check_80 == False:
				per_80_number = df1.loc[num][0]
				per_80_list.append(per_80_number)
				check_80 = True
				break

		total_sum_count = df2["count"].sum()
		sum_count = 0
		per_30_number = 0
		check_30 = False
		per_50_number = 0
		check_50 = False
		per_80_number = 0
		check_80 = False
		for num in range(0,len(df2)):
			sum_count = sum_count + df2.loc[num,"count"]
			percent = sum_count / float(total_sum_count)

			if percent >= 0.3 and check_30 == False:
				per_30_number = df2.loc[num][0]
				per_30_list.append(per_30_number)
				check_30 = True
			if percent >= 0.5 and check_50 == False:
				per_50_number = df2.loc[num][0]
				per_50_list.append(per_50_number)
				check_50 = True
			if percent >= 0.8 and check_80 == False:
				per_80_number = df2.loc[num][0]
				per_80_list.append(per_80_number)
				check_80 = True
				break

		total_sum_count = df3["count"].sum()
		sum_count = 0
		per_30_number = 0
		check_30 = False
		per_50_number = 0
		check_50 = False
		per_80_number = 0
		check_80 = False
		for num in range(0,len(df3)):
			sum_count = sum_count + df3.loc[num,"count"]
			percent = sum_count / float(total_sum_count)

			if percent >= 0.3 and check_30 == False:
				per_30_number = df3.loc[num][0]
				per_30_list.append(per_30_number)
				check_30 = True
			if percent >= 0.5 and check_50 == False:
				per_50_number = df3.loc[num][0]
				per_50_list.append(per_50_number)
				check_50 = True
			if percent >= 0.8 and check_80 == False:
				per_80_number = df3.loc[num][0]
				per_80_list.append(per_80_number)
				check_80 = True
				break

		writer = pd.ExcelWriter("./statistics/"+ (self.jsondata["category"]["slug"]).split("/")[0] + "/statistics.xlsx")
		df.to_excel(writer, "updaets_success")
		df1.to_excel(writer, "updaets_fail")
		df2.to_excel(writer, "comments_success")
		df3.to_excel(writer, "comments_fail")
		writer.save()

		f = open("per_30.csv", "a")
		wr = csv.writer(f)
		wr.writerow(per_30_list)
		f.close()

		f = open("per_50.csv", "a")
		wr = csv.writer(f)
		wr.writerow(per_50_list)
		f.close()

		f = open("per_80.csv", "a")
		wr = csv.writer(f)
		wr.writerow(per_80_list)
		f.close()

	def statistics_print3(self):
		if self.jsondata["state"] == "successful":
			Variable_list.success_count += 1

			if self.jsondata["updates_count"] >= 1:
				Variable_list.u_success_count_1 += 1
			if self.jsondata["comments_count"] >= 1:
				Variable_list.c_success_count_1 += 1
			if self.jsondata["updates_count"] >= 1 and self.jsondata["comments_count"] >= 1:
				Variable_list.u_c_success_count_1 += 1

			if self.jsondata["updates_count"] >= 3:
				Variable_list.u_success_count_3 += 1
			if self.jsondata["comments_count"] >= 3:
				Variable_list.c_success_count_3 += 1
			if self.jsondata["updates_count"] >= 3 and self.jsondata["comments_count"] >= 3:
				Variable_list.u_c_success_count_3 += 1

			if self.jsondata["updates_count"] >= 5:
				Variable_list.u_success_count_5 += 1
			if self.jsondata["comments_count"] >= 5:
				Variable_list.c_success_count_5 += 1
			if self.jsondata["updates_count"] >= 5 and self.jsondata["comments_count"] >= 5:
				Variable_list.u_c_success_count_5 += 1

		elif self.jsondata["state"] == "failed":
			Variable_list.fail_count += 1

			if self.jsondata["updates_count"] >= 1:
				Variable_list.u_fail_count_1 += 1
			if self.jsondata["comments_count"] >= 1:
				Variable_list.c_fail_count_1 += 1
			if self.jsondata["updates_count"] >= 1 and self.jsondata["comments_count"] >= 1:
				Variable_list.u_c_fail_count_1 += 1

			if self.jsondata["updates_count"] >= 3:
				Variable_list.u_fail_count_3 += 1
			if self.jsondata["comments_count"] >= 3:
				Variable_list.c_fail_count_3 += 1
			if self.jsondata["updates_count"] >= 3 and self.jsondata["comments_count"] >= 3:
				Variable_list.u_c_fail_count_3 += 1

			if self.jsondata["updates_count"] >= 5:
				Variable_list.u_fail_count_5 += 1
			if self.jsondata["comments_count"] >= 5:
				Variable_list.c_fail_count_5 += 1
			if self.jsondata["updates_count"] >= 5 and self.jsondata["comments_count"] >= 5:
				Variable_list.u_c_fail_count_5 += 1

	def category_file(self):

		if self.category.lower() == "art":

			f = open("art_url.txt", "a")
			f.write(self.url + "\n")
			f.close()

		if self.category.lower() == "comics":
			f = open("comics_url.txt", "a")
			f.write(self.url + "\n")
			f.close()

		if self.category.lower() == "crafts":
			f = open("crafts_url.txt", "a")
			f.write(self.url + "\n")
			f.close()

		if self.category.lower() == "dance":
			f = open("dance_url.txt", "a")
			f.write(self.url + "\n")
			f.close()

		if self.category.lower() == "design":
			f = open("design_url.txt", "a")
			f.write(self.url + "\n")
			f.close()

		if self.category.lower() == "fashion":
			f = open("fashion_url.txt", "a")
			f.write(self.url + "\n")
			f.close()

		if self.category.lower() == "film & video":
			f = open("filmvideo_url.txt", "a")
			f.write(self.url + "\n")
			f.close()

		if self.category.lower() == "food":
			f = open("food_url.txt", "a")
			f.write(self.url + "\n")
			f.close()

		if self.category.lower() == "games":
			f = open("games_url.txt", "a")
			f.write(self.url + "\n")
			f.close()

		if self.category.lower() == "journalism":
			f = open("journalism_url.txt", "a")
			f.write(self.url + "\n")
			f.close()

		if self.category.lower() == "music":
			f = open("music_url.txt", "a")
			f.write(self.url + "\n")
			f.close()

		if self.category.lower() == "photography":
			f = open("photography_url.txt", "a")
			f.write(self.url + "\n")
			f.close()

		if self.category.lower() == "publishing":
			f = open("publishing_url.txt", "a")
			f.write(self.url + "\n")
			f.close()

		if self.category.lower() == "technology":
			f = open("technology_url.txt", "a")
			f.write(self.url + "\n")
			f.close()

		if self.category.lower() == "theater":
			f = open("theater_url.txt", "a")
			f.write(self.url + "\n")
			f.close()

	def to_dict(self, name):
		month_dict = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07", "Aug": "08", "Sep": "09", "Oct": 10, "Nov": 11, "Dec": 12}
		return month_dict[name]
