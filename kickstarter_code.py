# -*- coding: UTF-8 -*-

### made by mr.leesh90@gmail.com
### Seunghun Lee

import time
import read_data
import Linguistic_analysis
import text_util
# import Graph_analysis
# import Gender_analysis
import Result_output
import Variable_list
import crawling_url
# import crawling_req
import Video_down
import os
import sys
import vpn_set
import genderize

import ssl, socket
import requests
from datetime import datetime


# requests.packages.urllib3.disable_warnings()



if __name__ == "__main__":

	'''
		sys.argv[1] = url file
		sys.argv[2] = working type
			1) data collection
			2) data add
			3) data read and check
			4) linguistic analysis
			5) graphic analysis
			6) print 4)'s result
			7) Gender analysis
			8) video download
		sys.argv[3] = time period
	'''

	url = open(sys.argv[1], "r").read().splitlines()
	date = str(sys.argv[3])
	

	project_list1 = []
	project_list2 = []

	if sys.argv[2] == "1":

		collected_number = 0
		collecting_number = 0

		crawler = crawling_url.Information()
		for project_url in url:

			print (project_url)
			p_url = project_url.split("/")
			project_name = p_url[5].strip()

			if not os.path.isdir("./Kick_data/"):
				os.mkdir("./Kick_data/")
			if not os.path.isdir("./creator_data/"):
				os.mkdir("./creator_data/")
			if not os.path.isdir("./updates_temp/"):
				os.mkdir("./updates_temp")
			if not os.path.isdir("./updates_comments_temp/"):
				os.mkdir("./updates_comments_temp")
			if not os.path.isdir("./comments_temp/"):
				os.mkdir("./comments_temp/")

			crawler.setinfo(project_url)
			file_check = crawler.collect_check("start")
			finish_check = crawler.collect_check("all")

			if finish_check == "continue":
				continue

			update_check = ""
			comment_check = ""
			creator_check = ""
			backers_list_check = ""

			if file_check == "Nofile":
				crawler.Collect_substring_HTML("new")

			else: 
				update_check = crawler.collect_check("update")
				comment_check = crawler.collect_check("comment")
				creator_check = crawler.collect_check("creator")
				backers_list_check = crawler.collect_check("backer_list")
				
				if (update_check != "continue") or (comment_check != "continue") or (creator_check != "Nocollect"):
					crawler.Collect_substring_HTML("add")

			if update_check != "continue":
				print ("updates_collecting")
				crawler.project_update_information()
			if comment_check != "continue":
				print ("comments_collecting")
				crawler.project_comments_information()
			if creator_check != "Nocollect":
				print ("creator_collecting")
				crawler.creator_profile()
			if backers_list_check != "continue":
				print ("backers_list_collecting")
				crawler.backer_lists()
			crawler.Data_caculation()
			crawler.collect_check("all")


	# Data check
	elif sys.argv[2] == "3":
		jsondata_read = read_data.json_read()

		# jsondata_read.story_text_url_remove(url)

		for project_url in url:
			# print (project_url)
			jsondata_read.setinfo(project_url)
			Check = jsondata_read.file_read()
			if Check == "Nofile":
				continue
			# jsondata_read.random_sampling()
		# # # 	# jsondata_read.statistics_print3()

		# jsondata_read.random_sampling2()
		# # 	jsondata_read.statistics_print()
			
		# # jsondata_read.statistics_print2()
		
		# print Variable_list.u_success_count_1
		# print Variable_list.u_fail_count_1
		# print Variable_list.c_success_count_1
		# print Variable_list.c_fail_count_1
		# print Variable_list.u_c_success_count_1
		# print Variable_list.u_c_fail_count_1
		
		# print Variable_list.u_success_count_3
		# print Variable_list.u_fail_count_3
		# print Variable_list.c_success_count_3
		# print Variable_list.c_fail_count_3
		# print Variable_list.u_c_success_count_3
		# print Variable_list.u_c_fail_count_3
		
		# print Variable_list.u_success_count_5
		# print Variable_list.u_fail_count_5
		# print Variable_list.c_success_count_5
		# print Variable_list.c_fail_count_5
		# print Variable_list.u_c_success_count_5
		# print Variable_list.u_c_fail_count_5

	# linguistic analysis
	elif sys.argv[2] == "4":
	
		for project_url in url:
			Als = Linguistic_analysis.Analysis(date, "analyze_text")
			print (project_url)

			Als.make_folder()
			Check = Als.setinfo(project_url)
			# if Check == "Already":
			# 	continue
			Als.file_read()

			# Als.story_analysis()
			# Als.update_analysis()
			# Als.comments_analysis()
			Als.script()
			# Als.ner()

	#### Text utilization
	elif sys.argv[2] == "5":
		for project_url in url:
			Als = Linguistic_analysis.Analysis(date, "make_text")	
			print (project_url)

			Als.make_folder()
			Als.setinfo(project_url)
			Als.file_read()
			Als.story_analysis()
			Als.update_analysis()
			Als.comments_analysis()
			Als.script()

	# ## Graphic anlaysis
	# elif sys.argv[2] == "5":
	#	creator_Graph = Graph_analysis.Graph()
	#	for project_url in url:
	#		print project_url
	#		creator_Graph.setinfo(project_url)
	#		creator_Graph.file_read()
	#		creator_Graph.make()
	#
	## print result of analysis
	elif sys.argv[2] == "6":
		output = Result_output.Output()
		for project_url in url:
			print (project_url)
			output.setinfo(project_url, date)
			output.result_print()
	
	#
	# ## Gender analysis
	# elif sys.argv[2] == "7":
	#	gen = Gender_analysis.distribution_gender()
	#	gen.ner_gen_list()
	#	for project_url in url:
	#		#print project_url
	#		gen.setinfo(project_url)
	#		#gen.file_read()
	#		gen.ner_gen_result(project_url)
	#
	#	gen.random_gen_list()
	#
	#
	##Video_download
	elif sys.argv[2] == "8":
		crawler = crawling_url.Information()

		for project_url in url:
			print (project_url)
			p_url = project_url.split("/")
			project_name = p_url[5].strip()
			video_file_name = project_name+".mp4"
	
			if os.path.isfile("./Result/Video_" + Variable_list.sub_title_name +"/" + video_file_name) == True:
				continue
			else:
				crawler.setinfo(project_url)
				video_url = crawler.Collect_substring_HTML("video")
				
				if video_url == "novideo":
					f = open("novideo_url.txt", "a")
					f.write(project_url+ "\n")
					f.close()
				else:
					dw = Video_down.video_dw()
					dw.setinfo(project_url)
					dw.video_download(video_url)






