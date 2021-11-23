
import Variable_list
import os, re, json, sys
import datetime, time

class text_preprocessing:
	def __init__(self, date):

		self.jsondata = ""
		self.project_name = ""
		self.date = date
		self.url = ""

		self.story_data = ""
		self.updates_data = ""
		self.c_comments_data = ""
		self.b_comments_data = ""

	def setinfo(self, project_url):

		self.url = project_url
		self.project_name = project_url.split("/")[5].strip()
		if os.path.isdir("./text") == False:
			os.mkdir("./text")
		if os.path.isdir("./text/" + Variable_list.sub_title_name) == False:
			os.mkdir("./text/" + Variable_list.sub_title_name)


	def file_read(self):
		if os.path.isfile("./Kick_data/" + self.project_name + ".txt") == True:
			jsonfile = open("./Kick_data/" + self.project_name + ".txt", "r")

		self.jsondata = jsonfile.readline()
		self.jsondata = json.loads(self.jsondata)

	def html_tag_remove(self, text):
		p = re.compile(r'<.*?>')
		text = p.sub('\n', text)
		text = text.replace("\n", " ")

		return text

	def tsv_file_make(self, text, text_type):
		text = " ".join(text.split())

		# text = text.replace("\"", "\\\"")
		# text = "\"" + text + "\""
		text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")
		filtered_text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', r'<url>', text)
		filtered_text2 = re.sub(r"(\w+[\w\.]*)@(\w+[\w\.]*)\.([A-Za-z]+)", r'<email>', filtered_text)
		if filtered_text2.strip() == "":
			filtered_text2 = " "

		class_num = 0
		if self.jsondata["state"] == "successful":
			class_num = 1
		elif self.jsondata["state"] == "failed":
			class_num = 0

		if os.path.isfile("./text/" + Variable_list.sub_title_name + "/" + text_type + "_" + sys.argv[3] + ".tsv") == False:
			f = open("./text/" + Variable_list.sub_title_name + "/" + text_type + "_" + sys.argv[3] + ".tsv", "a")
			f.write("ID\tsuccess_or_fail\tcontent\n")
			f.close()

		f = open("./text/" + Variable_list.sub_title_name + "/" + text_type + "_" + sys.argv[3] + ".tsv", "a")
		f.write("\"" + self.project_name + "\"" + "\t" + str(class_num) + "\t" + filtered_text2 + "\n")
		f.close()


	def story_text_extraction(self):
		self.story_data = self.jsondata["story_content"]["description"]
		self.tsv_file_make(self.story_data, "story")

	def update_text_extraction(self):
		self.updates_data = ""

		viewable_update_count = 0
		total_update_count = 0

		if isinstance(self.date, int) == True:
			update_date = 86400 * self.date
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

			elif (each_update_date - project_launched_at).total_seconds() <= update_date:
				total_update_count += 1
				if "body" in self.jsondata["updates_content"][num]:
					self.updates_data += (str(self.jsondata["updates_content"][num]["body"]) + "\n")
					viewable_update_count += 1

		self.updates_data = self.html_tag_remove(self.updates_data)
		self.tsv_file_make(self.updates_data, "update")



	def comment_text_extraction(self):

		self.c_comments_data = ""
		self.b_comments_data = ""

		self.creator_comments_count = 0
		self.backers_comments_count = 0

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
			update_date = 86400 * self.date

		project_launched_at = datetime.datetime.fromtimestamp(self.jsondata["launched_at"]).strftime(
			"%Y-%m-%d %H:%M:%S")
		project_launched_at = datetime.datetime.strptime(project_launched_at, "%Y-%m-%d %H:%M:%S")


		for comment in comments:

			if "author" not in comment:
				print (self.url)
				break

			comment_time = comment["created_at"]

			Time_diff = datetime.timedelta(hours=4)

			if isinstance(comment_time, str):
				comment_time = "-".join(comment_time.split("-")[:-1])[1:]
				comment_time = datetime.datetime.strptime(comment_time, "%Y-%m-%dT%H:%M:%S")
				comment_time = int(comment_time.strftime('%s'))

			comment_launched_at = datetime.datetime.fromtimestamp(comment_time).strftime("%Y-%m-%d %H:%M:%S")
			comment_launched_at = datetime.datetime.strptime(comment_launched_at, "%Y-%m-%d %H:%M:%S")
			comment_launched_at = comment_launched_at + Time_diff  ## comments timezone is UTC-4:00

			
			# #duing funding period
			# if (end_date - comment_launched_at + datetime.timedelta(days=1)).total_seconds() >= 0:
			# 	t = time.gmtime(comment_time)
			# 	d = str(t.tm_year) + "-" + str(t.tm_mon).zfill(2) + "-" + str(t.tm_mday).zfill(2)

			# 	if comment["author"]["id"] == creator_name:
			# 		self.c_comments_data += (str(comment["body"]) + "\n")
			# 		self.creator_comments_count += 1
			# 		if creator_comments_list.has_key(d) == True:
			# 			creator_comments_list[d] += 1
			# 		elif creator_comments_list.has_key(d) == False:
			# 			creator_comments_list[d] = 1
			# 			date_list[d] = 0
			# 	else:
			# 		self.b_comments_data += (str(comment["body"]) + "\n")
			# 		self.backers_comments_count += 1

			# 		if backers_comments_list.has_key(d) == True:
			# 			backers_comments_list[d] += 1
			# 		elif backers_comments_list.has_key(d) == False:
			# 			backers_comments_list[d] = 1
			# 			date_list[d] = 0


			if self.date == "full":


				t = time.gmtime(comment_time)
				d = str(t.tm_year) + "-" + str(t.tm_mon).zfill(2) + "-" + str(t.tm_mday).zfill(2)

				if comment["author"]["id"] == creator_name:
					self.c_comments_data += (str(comment["body"]) + "\n")
					self.creator_comments_count += 1
					if d in creator_comments_list == True:
						creator_comments_list[d] += 1
					elif d in creator_comments_list == False:
						creator_comments_list[d] = 1
						date_list[d] = 0
				else:
					self.b_comments_data += (str(comment["body"]) + "\n")
					self.backers_comments_count += 1

					if d in backers_comments_list == True:
						backers_comments_list[d] += 1
					elif d in backers_comments_list == False:
						backers_comments_list[d] = 1
						date_list[d] = 0

			elif (comment_launched_at - project_launched_at).total_seconds() <= comments_date:
				t = time.gmtime(comment_time)
				d = str(t.tm_year) + "-" + str(t.tm_mon).zfill(2) + "-" + str(t.tm_mday).zfill(2)

				if comment["author"]["id"] == creator_name:
					self.c_comments_data += (str(comment["body"]) + "\n")
					self.creator_comments_count += 1
					if d in creator_comments_list == True:
						creator_comments_list[d] += 1
					elif d in creator_comments_list == False:
						creator_comments_list[d] = 1
						date_list[d] = 0
				else:
					self.b_comments_data += (str(comment["body"]) + "\n")
					self.backers_comments_count += 1

					if d in backers_comments_list == True:
						backers_comments_list[d] += 1
					elif d in backers_comments_list == False:
						backers_comments_list[d] = 1
						date_list[d] = 0

		full_comments_data = self.c_comments_data + self.b_comments_data
		full_text_data = self.story_data + "\n" + self.updates_data + "\n" + self.c_comments_data + "\n" + self.b_comments_data

		self.tsv_file_make(self.c_comments_data, "c_comment")
		self.tsv_file_make(self.b_comments_data, "b_comment")
		self.tsv_file_make(full_comments_data, "full_comment")
		self.tsv_file_make(full_text_data, "full_text")










