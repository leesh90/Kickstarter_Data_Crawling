import csv
import json
import os
import Variable_list

class Output:

	def __init__(self):

		f_ner = open("NER.tsv", "r").readlines()
		for project in f_ner:
			project = project.strip().split("\t")
			

	def setinfo(self, project_url, date):
		self.date = date
		self.original_url = project_url
		self.project_url = project_url.split("/")
		self.project_name = self.project_url[5].strip()

		self.jsonfile = open("./Kick_data/" + self.project_name + ".txt", "r")
		self.jsondata = self.jsonfile.readline()
		self.jsondata = json.loads(self.jsondata)
		self.jsonfile.close()
		
		if "New backers" not in self.jsondata:
			self.new_backers = 0
			self.existing_backers = 0
		else:
			self.new_backers = int(self.jsondata["New backers"].replace(",",""))
			self.existing_backers = int(self.jsondata["existing-backers"].replace(",",""))


		self.creatorfile = open("./creator_data/" + str(self.jsondata["creator"]["id"]) + ".txt", "r")
		self.creatordata = self.creatorfile.readline()
		self.creatordata = json.loads(self.creatordata)
		self.creatorfile.close()

		self.s_jsonfile = open("./Result/Analysis_" + Variable_list.sub_title_name + "/basic_analysis/" + self.project_name + "/S_" + self.project_name + "_" + str(self.date) + ".txt", "r")
		self.s_jsondata = self.s_jsonfile.readline()
		self.s_jsondata = json.loads(self.s_jsondata)
		self.s_jsonfile.close()

		self.u_jsonfile = open("./Result/Analysis_" + Variable_list.sub_title_name + "/basic_analysis/" + self.project_name + "/U_" + self.project_name + "_" + str(self.date) + ".txt", "r")
		self.u_jsondata = self.u_jsonfile.readline()
		self.u_jsondata = json.loads(self.u_jsondata)
		self.u_jsonfile.close()

		self.b_jsonfile = open("./Result/Analysis_" + Variable_list.sub_title_name + "/basic_analysis/" + self.project_name + "/B_" + self.project_name + "_" + str(self.date) + ".txt", "r")
		self.b_jsondata = self.b_jsonfile.readline()
		self.b_jsondata = json.loads(self.b_jsondata)
		self.b_jsonfile.close()

		self.c_jsonfile = open("./Result/Analysis_" + Variable_list.sub_title_name + "/basic_analysis/" + self.project_name + "/C_" + self.project_name + "_" + str(self.date) + ".txt", "r")
		self.c_jsondata = self.c_jsonfile.readline()
		self.c_jsondata = json.loads(self.c_jsondata)
		self.c_jsonfile.close()

		self.tem_jsonfile = open("./Result/Analysis_" + Variable_list.sub_title_name + "/basic_analysis/" + self.project_name + "/Temporal_" + self.project_name + ".txt", "r")
		self.tem_jsondata = self.tem_jsonfile.readline()
		self.tem_jsondata = json.loads(self.tem_jsondata)
		self.tem_jsonfile.close()



		scam_list = open("./scam_url.txt", "r").read().splitlines()
		suspected_list = open("./suspected_url.txt", "r").read().splitlines()
		non_scam_list = open("./nonscam_url.txt", "r").read().splitlines()

		self.class_num = 0
		if self.original_url in scam_list or self.original_url in suspected_list:
			self.class_num = 1
		elif self.original_url in non_scam_list:
			self.class_num = 0

		if self.creatordata["facebook_link"] == "Null":
			self.facebook_check = "O"
		else:
			self.facebook_check = "X"


		## 해당 프로젝트보다 이전에 만들어진 프로젝트들이 실제 Created project Counting에 되어야 함
		self.created_project_count = len(self.creatordata["created_project_list"])
		# if len(self.creatordata["created_project_list"]) >= 1:
		# 	for created_project in self.creatordata["created_project_list"]:
		# 		if created_project["slug"] != self.project_name:
		# 			if self.jsondata["created_at"] > created_project["created_at"]:
		# 				self.created_project_count += 1



		self.u_video = 0
		self.u_audio = 0
		self.u_image = 0
		self.u_video_1 = 0
		self.u_audio_1 = 0
		self.u_image_1 = 0
		updates_count = 0
		for update in self.jsondata["updates_content"]:
			if update["is_public"] == True:
				updates_count += 1

				self.u_video += update["video_count"]
				self.u_audio += update["audio_count"]
				self.u_image += update["image_count"]
		if updates_count != 0:
			self.u_video_1 = self.u_video / float(updates_count)
			self.u_audio_1 = self.u_audio / float(updates_count)
			self.u_image_1 = self.u_image / float(updates_count)



		self.ner_data = {"s_location" : 0, "s_organization" : 0, "s_person" : 0, "s_subjective" : 0, "s_objective" : 0, "u_location" : 0, "u_organization" : 0, "u_person" : 0, \
			"u_subjective" : 0, "u_objective" : 0, "b_location" : 0, "b_organization" : 0, "b_person" : 0, "b_subjective" : 0, "b_objective" : 0, "c_location" : 0, "c_organization" : 0, \
			"c_person" : 0, "c_subjective" : 0, "c_objective" : 0}
		
		f_ner = open("NER.tsv", "r").readlines()
		for project in f_ner:
			project = project.strip().split("\t")

			if self.project_name == project[0]:
				self.ner_data["s_location"] = project[16]
				self.ner_data["s_organization"] = project[17]
				self.ner_data["s_person"] = project[18]
				self.ner_data["s_subjective"] = project[19]
				self.ner_data["s_objective"] = project[20]
				self.ner_data["u_location"] = project[11]
				self.ner_data["u_organization"] = project[12]
				self.ner_data["u_person"] = project[13]
				self.ner_data["u_subjective"] = project[14]
				self.ner_data["u_objective"] = project[15]
				self.ner_data["b_location"] = project[1]
				self.ner_data["b_organization"] = project[2]
				self.ner_data["b_person"] = project[3]
				self.ner_data["b_subjective"] = project[4]
				self.ner_data["b_objective"] = project[5]
				self.ner_data["c_location"] = project[6]
				self.ner_data["c_organization"] = project[7]
				self.ner_data["c_person"] = project[8]
				self.ner_data["c_subjective"] = project[9]
				self.ner_data["c_objective"] = project[10]
				break


		self.liwc_data = {"s_past" : 0, "s_present" : 0, "s_future" : 0, "s_negate" : 0, "s_posemo" : 0, "s_negemo" : 0, "s_cogproc" : 0, "s_insight" : 0, \
						"s_cause" : 0, "s_discrepancies" : 0, "s_tentative" : 0, "s_certain" : 0, "s_differentiation" : 0, "s_motion" : 0, \
						"u_past" : 0, "u_present" : 0, "u_future" : 0, "u_negate" : 0, "u_posemo" : 0, "u_negemo" : 0, "u_cogproc" : 0, "u_insight" : 0, \
						"u_cause" : 0, "u_discrepancies" : 0, "u_tentative" : 0, "u_certain" : 0, "u_differentiation" : 0, "u_motion" : 0, \
						"b_past" : 0, "b_present" : 0, "b_future" : 0, "b_negate" : 0, "b_posemo" : 0, "b_negemo" : 0, "b_cogproc" : 0, "b_insight" : 0, \
						"b_cause" : 0, "b_discrepancies" : 0, "b_tentative" : 0, "b_certain" : 0, "b_differentiation" : 0, "b_motion" : 0, \
						"c_past" : 0, "c_present" : 0, "c_future" : 0, "c_negate" : 0, "c_posemo" : 0, "c_negemo" : 0, "c_cogproc" : 0, "c_insight" : 0, \
						"c_cause" : 0, "c_discrepancies" : 0, "c_tentative" : 0, "c_certain" : 0, "c_differentiation" : 0, "c_motion" : 0}

		liwc_file = open("LIWC2015 Results (full (832 files)).txt", 'r')
		for line in liwc_file:
			line = line.strip().split("\t")

			if line[0] == "Filename":
				continue
			elif line[0].split("_")[1] == self.project_name:
				if line[0].split("_")[2] == (str(self.date) + ".txt"):
					text_type = line[0].split("_")[0]
					self.liwc_data[str(text_type) + "_past"] = line[64].strip()
					self.liwc_data[str(text_type) + "_present"] = line[65].strip()
					self.liwc_data[str(text_type) + "_future"] = line[66].strip()
					self.liwc_data[str(text_type) + "_negate"] = line[24].strip()
					self.liwc_data[str(text_type) + "_posemo"] = line[32].strip()
					self.liwc_data[str(text_type) + "_negemo"] = line[33].strip()
					self.liwc_data[str(text_type) + "_cogproc"] = line[42].strip()
					self.liwc_data[str(text_type) + "_insight"] = line[43].strip()
					self.liwc_data[str(text_type) + "_cause"] = line[45].strip()
					self.liwc_data[str(text_type) + "_discrepancies"] = line[46].strip()
					self.liwc_data[str(text_type) + "_tentative"] = line[47].strip()
					self.liwc_data[str(text_type) + "_certain"] = line[48].strip()
					self.liwc_data[str(text_type) + "_differentiation"] = line[49].strip()
					self.liwc_data[str(text_type) + "_motion"] = line[68].strip()


	def result_print(self):
		if os.path.isfile("./Result/" + str(self.date) + "_" + Variable_list.sub_title_name + "_result.txt") == False:
			f = open("./Result/"+str(self.date) + "_" + Variable_list.sub_title_name + "_result.txt", "w")
			f.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t" % ("Class","project_name", "state", "Number_rewards", "New_backers", "existing_backers", \
				"total_bakcers_count", "total_rewards_backers" , "goal", "pledged", \
				"updates_count", "viewable_updates_count", \
				"total_comments_count", "creator_comments_count", "backers_comments_count", \
				"project_start_time_since_IDmade", "state_changed_time_since_launchedat"))
 
			f.write("%s\t%s\t%s\t%s\t%s\t%s\t" % ("backed_project_count", "created_project_count", "facebook_check", \
				"external_link", "creator_before_comments", "creator_after_comments"))

			f.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t" % ("s_Total_words", "s_Nouns", "s_Verbs", "s_Adjectives", \
				"s_Adverbs", "s_Sentences", "s_mispell_words", "s_Function_words",\
				"s_redundancy", "s_Modal_verb", "s_Average_sentence_length", "s_Expressivity", \
				"s_Average_word_length" , "s_typo", "s_first_singular_people", "s_first_plural_people", \
				"s_second_people", "s_third_people", "s_lexical_complexity", \
				"s_video", "s_audio", "s_image", \
				"s_email", "s_phone", "s_url", \
				"s_ARI", "s_CL", "s_GF", "s_FKG", "s_FRE"))

			f.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t" % ("s_past" ,"s_present" ,"s_future" ,"s_negate" ,"s_posemo" ,"s_negemo" , \
				"s_cogproc" ,"s_insight" , "s_cause" ,"s_discrepancies" ,"s_tentative" , \
				"s_certain" , "s_differentiation" ,"s_motion"))

			f.write("%s\t%s\t%s\t%s\t%s\t" % ("s_location", "s_organization", "s_person", "s_subjective", "s_objective"))




			f.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t" % ("u_Total_words", "u_Nouns", "u_Verbs", "u_Adjectives", \
				"u_Adverbs", "u_Sentences", "u_mispell_words", "u_Function_words",\
				"u_redundancy", "u_Modal_verb", "u_Average_sentence_length", "u_Expressivity", \
				"u_Average_word_length" , "u_typo", "u_first_singular_people", "u_first_plural_people", \
				"u_second_people", "u_third_people", "u_lexical_complexity", \
				"u_video", "u_image", "u_audio", \
				"u_email", "u_phone", "u_url", \
				"u_ARI", "u_CL", "u_GF", "u_FKG", "u_FRE"
				))

			f.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t" % ("u_Total_words_1", "u_Nouns_1", "u_Nouns_2", "u_Verbs_1", "u_Verbs_2", \
				"u_Adjectives_1", "u_Adjectives_2", "u_Adverbs1", "u_Adverbs_2", "u_Sentences_1", \
				"u_mispell_words_1", "u_Function_words_1", "u_Function_words_2", \
				"u_modal_verbs_1", "u_modal_verbs_2", "u_first_singular_people_1", "u_first_singular_people_2", \
				"u_first_plural_people_1", "u_first_plural_people_2", "u_second_people_1", "u_second_people_2", \
				"u_third_people_1", "u_third_people_2", \
				"u_video_1", "u_image_1" ,"u_audio_1", \
				"u_email_1", "u_phone_1", "u_url_1"))

			f.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t" % ("u_past" ,"u_present" ,"u_future" ,"u_negate" ,"u_posemo" ,"u_negemo" , \
				"u_cogproc" ,"u_insight" , "u_cause" ,"u_discrepancies" ,"u_tentative" , \
				"u_certain" , "u_differentiation" ,"u_motion"))

			f.write("%s\t%s\t%s\t%s\t%s\t" % ("u_location", "u_organization", "u_person", "u_subjective", "u_objective"))




			f.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t" % ("b_Total_words", "b_Nouns", "b_Verbs", "b_Adjectives", \
				"b_Adverbs", "b_Sentences", "b_mispell_words", "b_Function_words",\
				"b_redundancy", "b_Modal_verb", "b_Average_sentence_length", "b_Expressivity", \
				"b_Average_word_length" , "b_typo", "b_first_singular_people", "b_first_plural_people", \
				"b_second_people", "b_third_people", "b_lexical_complexity", \
				"b_video", "b_image", "b_audio", \
				"b_ARI", "b_CL", "b_GF", "b_FKG", "b_FRE"
				))

			f.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t" % ("b_Total_words_1", "b_Nouns_1", "b_Nouns_2", "b_Verbs_1", "b_Verbs_2", \
				"b_Adjectives_1", "b_Adjectives_2", "b_Adverbs1", "b_Adverbs_2", "b_Sentences_1", \
				"b_mispell_words_1", "b_Function_words_1", "b_Function_words_2", \
				"b_modal_verbs_1", "b_modal_verbs_2", "b_first_singular_people_1", "b_first_singular_people_2", \
				"b_first_plural_people_1", "b_first_plural_people_2", "b_second_people_1", "b_second_people_2", \
				"b_third_people_1", "b_third_people_2", \
				"b_email_1", "b_phone_1", "b_url_1"))

			f.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t" % ("b_past" ,"b_present" ,"b_future" ,"b_negate" ,"b_posemo" ,"b_negemo" , \
				"b_cogproc" ,"b_insight" , "b_cause" ,"b_discrepancies" ,"b_tentative" , \
				"b_certain" , "b_differentiation" ,"b_motion"))

			f.write("%s\t%s\t%s\t%s\t%s\t" % ("b_location", "b_organization", "b_person", "b_subjective", "b_objective"))





			f.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t" % ("c_Total_words", "c_Nouns", "c_Verbs", "c_Adjectives", \
				"c_Adverbs", "c_Sentences", "c_mispell_words", "c_Function_words",\
				"c_redundancy", "c_Modal_verb", "c_Average_sentence_length", "c_Expressivity", \
				"c_Average_word_length" , "c_typo", "c_first_singular_people", "c_first_plural_people", \
				"c_second_people", "c_third_people", "c_lexical_complexity", \
				"c_video", "c_image", "c_audio", \
				"c_ARI", "c_CL", "c_GF", "c_FKG", "c_FRE"
				))

			f.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t" % ("c_Total_words_1", "c_Nouns_1", "c_Nouns_2", "c_Verbs_1", "c_Verbs_2", \
				"c_Adjectives_1", "c_Adjectives_2", "c_Adverbs1", "c_Adverbs_2", "c_Sentences_1", \
				"c_mispell_words_1", "c_Function_words_1", "c_Function_words_2", \
				"c_modal_verbs_1", "c_modal_verbs_2", "c_first_singular_people_1", "c_first_singular_people_2", \
				"c_first_plural_people_1", "c_first_plural_people_2", "c_second_people_1", "c_second_people_2", \
				"c_third_people_1", "c_third_people_2", \
				"c_email_1", "c_phone_1", "c_url_1"))

			f.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t" % ("c_past" ,"c_present" ,"c_future" ,"c_negate" ,"c_posemo" ,"c_negemo" , \
				"c_cogproc" ,"c_insight" , "c_cause" ,"c_discrepancies" ,"c_tentative" , \
				"c_certain" , "c_differentiation" ,"c_motion"))

			f.write("%s\t%s\t%s\t%s\t%s\n" % ("c_location", "c_organization", "c_person", "c_subjective", "c_objective"))


			
		else:
			f = open("./Result/"+str(self.date) + "_" + Variable_list.sub_title_name + "_result.txt", "a")


		f.write(str(self.class_num) + "\t" + str(self.project_name) + "\t" + self.jsondata["state"] + "\t" + str(len(self.jsondata["rewards"])) + "\t" + str(self.new_backers) + "\t" + str(self.existing_backers) + "\t" + \
			str(self.jsondata["backers_count"]) + "\t" + str(self.jsondata["total_rewards_backers"]) + "\t" + str(self.jsondata["goal"]) + "\t" + str(self.jsondata["pledged"]) + "\t" + \
			str(self.tem_jsondata[str(self.date) + "_U_total_update_count"]) + "\t" + str(self.tem_jsondata[str(self.date) + "_U_viewable_update_count"]) + "\t" + \
			str(self.tem_jsondata[str(self.date) + "_total_comments"]) + "\t" + str(self.tem_jsondata[str(self.date) + "_creator_comments"]) + "\t" + str(self.tem_jsondata[str(self.date) + "_backers_comments"]) + "\t" +\
			str(self.jsondata["time1"]) + "\t" + str(self.jsondata["time2"]) + "\t")

		f.write(str(self.creatordata["backed_projects_count"]) + "\t" + str(self.created_project_count) + "\t" + str(self.facebook_check) + "\t" + \
			str(len(self.creatordata["external_link_list"])) + "\t" + str(self.tem_jsondata["creator_before_comments"]) + "\t" + str(self.tem_jsondata[str(self.date) + "_creator_after_comments"]) + "\t")


		f.write(str(self.s_jsondata["Total_words"]) + "\t" + str(self.s_jsondata["Nouns"]) + "\t" + str(self.s_jsondata["Verbs"]) + "\t" + str(self.s_jsondata["Adjectives"]) + "\t" + \
			str(self.s_jsondata["Adverbs"]) + "\t" + str(self.s_jsondata["Sentences"]) + "\t" + str(self.s_jsondata["mispell_words"]) + "\t" + str(self.s_jsondata["Function_words"]) + "\t" + \
			str(self.s_jsondata["redundancy"]) + "\t" + str(self.s_jsondata["Modal_verb"]) + "\t" + str(self.s_jsondata["Average_sentence_length"]) + "\t" + str(self.s_jsondata["Expressivity"]) + "\t" + \
			str(self.s_jsondata["Average_word_length"]) + "\t" + str(self.s_jsondata["typo"]) + "\t" + str(self.s_jsondata["first_singular_people"]) + "\t" + str(self.s_jsondata["first_plural_people"]) + "\t" + \
			str(self.s_jsondata["second_people"]) + "\t" + str(self.s_jsondata["third_people"]) + "\t" + str(self.s_jsondata["lexical_complexity"]) + "\t" + \
			str(self.jsondata["story_content"]["video_count"]) + "\t" + str(self.jsondata["story_content"]["audio_count"]) + "\t" + str(self.jsondata["story_content"]["image_count"]) + "\t" + \
			str(self.s_jsondata["s_email_link_count"]) + "\t" + str(self.s_jsondata["s_phone_count"]) + "\t" + str(self.s_jsondata["s_url_link_count"]) + "\t" + \
			str(self.s_jsondata["s_ari"]) + "\t" + str(self.s_jsondata["s_CL"]) + "\t" + str(self.s_jsondata["s_GF"]) + "\t" + str(self.s_jsondata["s_FKG"]) + "\t" + str(self.s_jsondata["s_FRE"]) + "\t")

		f.write(str(self.liwc_data["s_past"]) + "\t" + str(self.liwc_data["s_present"]) + "\t" + str(self.liwc_data["s_future"]) + "\t" + str(self.liwc_data["s_negate"]) + "\t" + str(self.liwc_data["s_posemo"]) + "\t" + str(self.liwc_data["s_negemo"]) + "\t" + \
			str(self.liwc_data["s_cogproc"]) + "\t" + str(self.liwc_data["s_insight"]) + "\t" + str(self.liwc_data["s_cause"]) + "\t" + str(self.liwc_data["s_discrepancies"]) + "\t" + str(self.liwc_data["s_tentative"]) + "\t" + \
			str(self.liwc_data["s_certain"]) + "\t" + str(self.liwc_data["s_differentiation"]) + "\t" + str(self.liwc_data["s_motion"]) + "\t")

		f.write(str(self.ner_data["s_location"]) + "\t" + str(self.ner_data["s_organization"]) + "\t" + str(self.ner_data["s_person"]) + "\t" + str(self.ner_data["s_subjective"]) + "\t" + str(self.ner_data["s_objective"]) + "\t")



		f.write(str(self.u_jsondata["Total_words"]) + "\t" + str(self.u_jsondata["Nouns"]) + "\t" + str(self.u_jsondata["Verbs"]) + "\t" + str(self.u_jsondata["Adjectives"]) + "\t" + \
			str(self.u_jsondata["Adverbs"]) + "\t" + str(self.u_jsondata["Sentences"]) + "\t" + str(self.u_jsondata["mispell_words"]) + "\t" + str(self.u_jsondata["Function_words"]) + "\t" + \
			str(self.u_jsondata["redundancy"]) + "\t" + str(self.u_jsondata["Modal_verb"]) + "\t" + str(self.u_jsondata["Average_sentence_length"]) + "\t" + str(self.u_jsondata["Expressivity"]) + "\t" + \
			str(self.u_jsondata["Average_word_length"]) + "\t" + str(self.u_jsondata["typo"]) + "\t" + str(self.u_jsondata["first_singular_people"]) + "\t" + str(self.u_jsondata["first_plural_people"]) + "\t" + \
			str(self.u_jsondata["second_people"]) + "\t" + str(self.u_jsondata["third_people"]) + "\t" + str(self.u_jsondata["lexical_complexity"]) + "\t" + \
			str(self.u_video) + "\t" + str(self.u_image) + "\t" + str(self.u_audio) + "\t" + \
			str(self.u_jsondata["u_email_link_count"]) + "\t" + str(self.u_jsondata["u_phone_count"]) + "\t" + str(self.u_jsondata["u_url_link_count"]) + "\t" + \
			str(self.u_jsondata["u_ari"]) + "\t" + str(self.u_jsondata["u_CL"]) + "\t" + str(self.u_jsondata["u_GF"]) + "\t" + str(self.u_jsondata["u_FKG"]) + "\t" + str(self.u_jsondata["u_FRE"]) + "\t")


		f.write(str(self.u_jsondata["Total_words_1"]) + "\t" + str(self.u_jsondata["Nouns_1"]) + "\t" + str(self.u_jsondata["Nouns_2"]) + "\t" + str(self.u_jsondata["Verbs_1"]) + "\t" + str(self.u_jsondata["Verbs_2"]) + "\t" + \
			str(self.u_jsondata["Adjectives_1"]) + "\t" + str(self.u_jsondata["Adjectives_2"]) + "\t" + str(self.u_jsondata["Adverbs_1"]) + "\t" + str(self.u_jsondata["Adverbs_2"]) + "\t" + str(self.u_jsondata["Sentences_1"]) + "\t" + \
			str(self.u_jsondata["mispell_words_1"]) + "\t" + str(self.u_jsondata["Function_words_1"]) + "\t" + str(self.u_jsondata["Function_words_2"]) + "\t" + \
			str(self.u_jsondata["modal_verbs_1"]) + "\t" + str(self.u_jsondata["modal_verbs_2"]) + "\t" + str(self.u_jsondata["first_singular_people_1"]) + "\t" + str(self.u_jsondata["first_singular_people_2"]) + "\t" + \
			str(self.u_jsondata["first_plural_people_1"]) + "\t" + str(self.u_jsondata["first_plural_people_2"]) + "\t" + str(self.u_jsondata["second_people_1"]) + "\t" + str(self.u_jsondata["second_people_2"]) + "\t" + \
			str(self.u_jsondata["third_people_1"]) + "\t" + str(self.u_jsondata["third_people_2"]) + "\t" + \
			str(self.u_video_1) + "\t" + str(self.u_image_1) + "\t" + str(self.u_audio_1) + "\t" + \
			str(self.u_jsondata["u_email_link_count_1"]) + "\t" + str(self.u_jsondata["u_phone_count_1"]) + "\t" + str(self.u_jsondata["u_url_link_count_1"]) + "\t")


		f.write(str(self.liwc_data["u_past"]) + "\t" + str(self.liwc_data["u_present"]) + "\t" + str(self.liwc_data["u_future"]) + "\t" + str(self.liwc_data["u_negate"]) + "\t" + str(self.liwc_data["u_posemo"]) + "\t" + str(self.liwc_data["u_negemo"]) + "\t" + \
			str(self.liwc_data["u_cogproc"]) + "\t" + str(self.liwc_data["u_insight"]) + "\t" + str(self.liwc_data["u_cause"]) + "\t" + str(self.liwc_data["u_discrepancies"]) + "\t" + str(self.liwc_data["u_tentative"]) + "\t" + \
			str(self.liwc_data["u_certain"]) + "\t" + str(self.liwc_data["u_differentiation"]) + "\t" + str(self.liwc_data["u_motion"]) + "\t")

		f.write(str(self.ner_data["u_location"]) + "\t" + str(self.ner_data["u_organization"]) + "\t" + str(self.ner_data["u_person"]) + "\t" + str(self.ner_data["u_subjective"]) + "\t" + str(self.ner_data["u_objective"]) + "\t")




		f.write(str(self.b_jsondata["Total_words"]) + "\t" + str(self.b_jsondata["Nouns"]) + "\t" + str(self.b_jsondata["Verbs"]) + "\t" + str(self.b_jsondata["Adjectives"]) + "\t" + \
			str(self.b_jsondata["Adverbs"]) + "\t" + str(self.b_jsondata["Sentences"]) + "\t" + str(self.b_jsondata["mispell_words"]) + "\t" + str(self.b_jsondata["Function_words"]) + "\t" + \
			str(self.b_jsondata["redundancy"]) + "\t" + str(self.b_jsondata["Modal_verb"]) + "\t" + str(self.b_jsondata["Average_sentence_length"]) + "\t" + str(self.b_jsondata["Expressivity"]) + "\t" + \
			str(self.b_jsondata["Average_word_length"]) + "\t" + str(self.b_jsondata["typo"]) + "\t" + str(self.b_jsondata["first_singular_people"]) + "\t" + str(self.b_jsondata["first_plural_people"]) + "\t" + \
			str(self.b_jsondata["second_people"]) + "\t" + str(self.b_jsondata["third_people"]) + "\t" + str(self.b_jsondata["lexical_complexity"]) + "\t" + \
			str(self.b_jsondata["b_email_link_count"]) + "\t" + str(self.b_jsondata["b_phone_count"]) + "\t" + str(self.b_jsondata["b_url_link_count"]) + "\t" + \
			str(self.b_jsondata["b_ari"]) + "\t" + str(self.b_jsondata["b_CL"]) + "\t" + str(self.b_jsondata["b_GF"]) + "\t" + str(self.b_jsondata["b_FKG"]) + "\t" + str(self.b_jsondata["b_FRE"]) + "\t")


		f.write(str(self.b_jsondata["Total_words_1"]) + "\t" + str(self.b_jsondata["Nouns_1"]) + "\t" + str(self.b_jsondata["Nouns_2"]) + "\t" + str(self.b_jsondata["Verbs_1"]) + "\t" + str(self.b_jsondata["Verbs_2"]) + "\t" + \
			str(self.b_jsondata["Adjectives_1"]) + "\t" + str(self.b_jsondata["Adjectives_2"]) + "\t" + str(self.b_jsondata["Adverbs_1"]) + "\t" + str(self.b_jsondata["Adverbs_2"]) + "\t" + str(self.b_jsondata["Sentences_1"]) + "\t" + \
			str(self.b_jsondata["mispell_words_1"]) + "\t" + str(self.b_jsondata["Function_words_1"]) + "\t" + str(self.b_jsondata["Function_words_2"]) + "\t" + \
			str(self.b_jsondata["modal_verbs_1"]) + "\t" + str(self.b_jsondata["modal_verbs_2"]) + "\t" + str(self.b_jsondata["first_singular_people_1"]) + "\t" + str(self.b_jsondata["first_singular_people_2"]) + "\t" + \
			str(self.b_jsondata["first_plural_people_1"]) + "\t" + str(self.b_jsondata["first_plural_people_2"]) + "\t" + str(self.b_jsondata["second_people_1"]) + "\t" + str(self.b_jsondata["second_people_2"]) + "\t" + \
			str(self.b_jsondata["third_people_1"]) + "\t" + str(self.b_jsondata["third_people_2"]) + "\t" + \
			str(self.b_jsondata["b_email_link_count_1"]) + "\t" + str(self.b_jsondata["b_phone_count_1"]) + "\t" + str(self.b_jsondata["b_url_link_count_1"]) + "\t")

		f.write(str(self.liwc_data["b_past"]) + "\t" + str(self.liwc_data["b_present"]) + "\t" + str(self.liwc_data["b_future"]) + "\t" + str(self.liwc_data["b_negate"]) + "\t" + str(self.liwc_data["b_posemo"]) + "\t" + str(self.liwc_data["b_negemo"]) + "\t" + \
			str(self.liwc_data["b_cogproc"]) + "\t" + str(self.liwc_data["b_insight"]) + "\t" + str(self.liwc_data["b_cause"]) + "\t" + str(self.liwc_data["b_discrepancies"]) + "\t" + str(self.liwc_data["b_tentative"]) + "\t" + \
			str(self.liwc_data["b_certain"]) + "\t" + str(self.liwc_data["b_differentiation"]) + "\t" + str(self.liwc_data["b_motion"]) + "\t")

		f.write(str(self.ner_data["b_location"]) + "\t" + str(self.ner_data["b_organization"]) + "\t" + str(self.ner_data["b_person"]) + "\t" + str(self.ner_data["b_subjective"]) + "\t" + str(self.ner_data["b_objective"]) + "\t")




		f.write(str(self.c_jsondata["Total_words"]) + "\t" + str(self.c_jsondata["Nouns"]) + "\t" + str(self.c_jsondata["Verbs"]) + "\t" + str(self.c_jsondata["Adjectives"]) + "\t" + \
			str(self.c_jsondata["Adverbs"]) + "\t" + str(self.c_jsondata["Sentences"]) + "\t" + str(self.c_jsondata["mispell_words"]) + "\t" + str(self.c_jsondata["Function_words"]) + "\t" + \
			str(self.c_jsondata["redundancy"]) + "\t" + str(self.c_jsondata["Modal_verb"]) + "\t" + str(self.c_jsondata["Average_sentence_length"]) + "\t" + str(self.c_jsondata["Expressivity"]) + "\t" + \
			str(self.c_jsondata["Average_word_length"]) + "\t" + str(self.c_jsondata["typo"]) + "\t" + str(self.c_jsondata["first_singular_people"]) + "\t" + str(self.c_jsondata["first_plural_people"]) + "\t" + \
			str(self.c_jsondata["second_people"]) + "\t" + str(self.c_jsondata["third_people"]) + "\t" + str(self.c_jsondata["lexical_complexity"]) + "\t" + \
			str(self.c_jsondata["c_email_link_count"]) + "\t" + str(self.c_jsondata["c_phone_count"]) + "\t" + str(self.c_jsondata["c_url_link_count"]) + "\t" + \
			str(self.c_jsondata["c_ari"]) + "\t" + str(self.c_jsondata["c_CL"]) + "\t" + str(self.c_jsondata["c_GF"]) + "\t" + str(self.c_jsondata["c_FKG"]) + "\t" + str(self.c_jsondata["c_FRE"]) + "\t")


		f.write(str(self.c_jsondata["Total_words_1"]) + "\t" + str(self.c_jsondata["Nouns_1"]) + "\t" + str(self.c_jsondata["Nouns_2"]) + "\t" + str(self.c_jsondata["Verbs_1"]) + "\t" + str(self.c_jsondata["Verbs_2"]) + "\t" + \
			str(self.c_jsondata["Adjectives_1"]) + "\t" + str(self.c_jsondata["Adjectives_2"]) + "\t" + str(self.c_jsondata["Adverbs_1"]) + "\t" + str(self.c_jsondata["Adverbs_2"]) + "\t" + str(self.c_jsondata["Sentences_1"]) + "\t" + \
			str(self.c_jsondata["mispell_words_1"]) + "\t" + str(self.c_jsondata["Function_words_1"]) + "\t" + str(self.c_jsondata["Function_words_2"]) + "\t" + \
			str(self.c_jsondata["modal_verbs_1"]) + "\t" + str(self.c_jsondata["modal_verbs_2"]) + "\t" + str(self.c_jsondata["first_singular_people_1"]) + "\t" + str(self.c_jsondata["first_singular_people_2"]) + "\t" + \
			str(self.c_jsondata["first_plural_people_1"]) + "\t" + str(self.c_jsondata["first_plural_people_2"]) + "\t" + str(self.c_jsondata["second_people_1"]) + "\t" + str(self.c_jsondata["second_people_2"]) + "\t" + \
			str(self.c_jsondata["third_people_1"]) + "\t" + str(self.c_jsondata["third_people_2"]) + "\t" + \
			str(self.c_jsondata["c_email_link_count_1"]) + "\t" + str(self.c_jsondata["c_phone_count_1"]) + "\t" + str(self.c_jsondata["c_url_link_count_1"]) + "\t")

		f.write(str(self.liwc_data["c_past"]) + "\t" + str(self.liwc_data["c_present"]) + "\t" + str(self.liwc_data["c_future"]) + "\t" + str(self.liwc_data["c_negate"]) + "\t" + str(self.liwc_data["c_posemo"]) + "\t" + str(self.liwc_data["c_negemo"]) + "\t" + \
			str(self.liwc_data["c_cogproc"]) + "\t" + str(self.liwc_data["c_insight"]) + "\t" + str(self.liwc_data["c_cause"]) + "\t" + str(self.liwc_data["c_discrepancies"]) + "\t" + str(self.liwc_data["c_tentative"]) + "\t" + \
			str(self.liwc_data["c_certain"]) + "\t" + str(self.liwc_data["c_differentiation"]) + "\t" + str(self.liwc_data["c_motion"]) + "\t")

		f.write(str(self.ner_data["c_location"]) + "\t" + str(self.ner_data["c_organization"]) + "\t" + str(self.ner_data["c_person"]) + "\t" + str(self.ner_data["c_subjective"]) + "\t" + str(self.ner_data["c_objective"]) + "\n")

