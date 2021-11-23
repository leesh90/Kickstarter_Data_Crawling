import csv
import json
import os
import Variable_list

class Output:
	def setinfo(self, project_url, date_type):
		self.original_url = project_url
		self.project_url = project_url.split("/")
		self.project_name = self.project_url[5].strip()

		self.jsonfile = open("./Kick_data/" + self.project_name + ".txt", "r")
		self.jsondata = self.jsonfile.readline()
		self.jsondata = json.loads(self.jsondata)
		self.jsonfile.close()

		if "New backers" not in self.jsondata:
			self.jsondata["New backers"] = 0
			self.jsondata["existing-backers"] = 0


		self.creatorfile = open("./creator_data/" + str(self.jsondata["creator"]["id"]) + ".txt", "r")
		self.creatordata = self.creatorfile.readline()
		self.creatordata = json.loads(self.creatordata)
		self.creatorfile.close()

		self.s_jsonfile = open("./Result/Analysis_" + Variable_list.sub_title_name + "/basic_analysis/" + self.project_name + "/S_" + self.project_name + "_" + str(date_type) + ".txt", "r")
		self.s_jsondata = self.s_jsonfile.readline()
		self.s_jsondata = json.loads(self.s_jsondata)
		self.s_jsonfile.close()

		self.u_jsonfile = open("./Result/Analysis_" + Variable_list.sub_title_name + "/basic_analysis/" + self.project_name + "/U_" + self.project_name + "_" + str(date_type) + ".txt", "r")
		self.u_jsondata = self.u_jsonfile.readline()
		self.u_jsondata = json.loads(self.u_jsondata)
		self.u_jsonfile.close()

		self.c_jsonfile = open("./Result/Analysis_" + Variable_list.sub_title_name + "/basic_analysis/" + self.project_name + "/C_" + self.project_name + "_" + str(date_type) + ".txt", "r")
		self.c_jsondata = self.c_jsonfile.readline()
		self.c_jsondata = json.loads(self.c_jsondata)
		self.c_jsonfile.close()

		

		# self.sc_jsonfile = open("./Result/Analysis_" + Variable_list.sub_title_name + "/basic_analysis/" + self.project_name + "/SC_" + self.project_name + "_" + str(date_type) + ".txt", "r")
		# self.sc_jsondata = self.sc_jsonfile.readline()
		# self.sc_jsondata = json.loads(self.sc_jsondata)

		# self.date_jsonfile = open("./Result/Analysis_" + Variable_list.sub_title_name + "/basic_analysis/" + self.project_name + "/" + str(date_type) + "_" + self.project_name + ".txt", "r")
		# self.date_jsondata = self.date_jsonfile.readline()
		# self.date_jsondata = json.loads(self.date_jsondata)


		# ,"backed_project", "created_project", "facebook_ID", "External_link",
		# "creator_before_comments", "creator_after_comments", "time1" \
		# , "", "", "total_updates_count", "viewable_updates_count", "total_comments_count", "creator_comments_count", "backers_comments_count", "total_backers_count", "total_rewards_backers" \

		# , "s_Total_words", "s_Nouns", "s_Verbs" \
		# , "s_Adjectives", "s_Adverbs", "s_Sentences", "s_clauses", "s_noun_phrases", "s_phrases", "s_punctuation", "s_mispell_words", "s_Function_words" \
		# , "s_redundancy", "s_characters", "s_url", "s_Modal_verb", "s_Average_sentence_length", "s_Pausality", "s_Expressivity", "s_Average_clauses" \
		# , "s_Average_word_length", "s_typo", "s_first_singular_people", "s_first_plural_people", "s_second_people", "s_third_people", "s_lexical_complexity" \
		# , "s_video", "s_image", "s_audio", "s_email", "s_phone", "s_location", "s_organization", "s_person", "s_time", "s_past", "s_present", "s_future" \

		# , "U_Total_words", "U_Total_words_1", "U_Nouns", "U_Nouns_1", "U_Nouns_2", "U_Verbs", "U_Verbs_1", "U_Verbs_2" \
		# , "U_Adjectives", "U_Adjectives_1", "U_Adjectives_2", "U_Adverbs", "U_Adverbs1", "U_Adverbs_2", "U_Sentences", "U_Sentences_1", "U_clauses", "U_clauses_1", "U_noun_phrases", "U_noun_phrases_1" \
		# , "U_phrases", "U_phrases_1", "U_punctuation", "U_punctuation_1", "U_punctuation_2", "U_mispell_words", "U_mispell_words_1", "U_Function_words" \
		# , "U_Function_words_1", "U_Function_words_2", "U_redundancy", "U_characters", "U_characters_1", "U_characters_2", "U_url", "U_url_1", "U_url_2", "U_Modal_verb", "U_modal_verbs_1", "U_modal_verbs_2" \
		# , "U_Average_sentence_length", "U_Pausality", "U_Expressivity", "U_Average_clauses", "U_Average_word_length", "U_typo" \
		# , "U_first_singular_people", "U_first_singular_people_1", "U_first_singular_people_2", "U_first_plural_people", "U_first_plural_people_1", "U_first_plural_people_2" \
		# , "U_second_people", "U_second_people_1", "U_second_people_2", "U_third_people", "U_third_people_1", "U_third_people_2", "U_lexical_complexity", "u_video", "u_video_1", "u_image", "u_image_1", "u_audio", "u_audio_1", "u_email", "u_email_1", "u_phone", "u_phone_1" \
		# , "u_location", "u_location_1", "u_organization", "u_organization_1", "u_person", "u_person_1", "u_time", "u_time_1", "u_past", "u_present", "u_future" \

		# , "C_Total_words", "C_Total_words_1", "C_Nouns", "C_Nouns_1", "C_Nouns_2", "C_Verbs", "C_Verbs_1", "C_Verbs_2" \
		# , "C_Adjectives", "C_Adjectives_1", "C_Adjectives_2", "C_Adverbs", "C_Adverbs1", "C_Adverbs_2", "C_Sentences", "C_Sentences_1", "C_clauses", "C_clauses_1", "C_noun_phrases", "C_noun_phrases_1" \
		# , "C_phrases", "C_phrases_1", "C_punctuation", "C_punctuation_1", "C_punctuation_2", "C_mispell_words", "C_mispell_words_1", "C_Function_words" \
		# , "C_Function_words_1", "C_Function_words_2", "C_redundancy", "C_characters", "C_characters_1", "C_characters_2", "C_url", "C_url_1", "C_url_2", "C_Modal_verb", "C_modal_verbs_1", "C_modal_verbs_2" \
		# , "C_Average_sentence_length", "C_Pausality", "C_Expressivity", "C_Average_clauses", "C_Average_word_length", "C_typo" \
		# , "C_first_singular_people", "C_first_singular_people_1", "C_first_singular_people_2", "C_first_plural_people", "C_first_plural_people_1", "C_first_plural_people_2" \
		# , "C_second_people", "C_second_people_1", "C_second_people_2", "C_third_people", "C_third_people_1", "C_third_people_2", "C_lexical_complexity" \
		# , "C_email", "C_email_1", "C_phone", "C_phone_1", "C_location", "C_location_1", "C_organization", "C_organization_1", "C_person", "C_person_1", "C_time", "C_time_1", "C_past", "C_present", "C_future"\

		# , "sc_Total_words", "sc_Nouns", "sc_Verbs", "sc_Adjectives", "sc_Adverbs", "sc_Sentences", "sc_clauses", "sc_noun_phrases", "sc_phrases", "sc_punctuation", "sc_mispell_words", "sc_Function_words" \
		# , "sc_redundancy", "sc_characters", "sc_url", "sc_Modal_verb", "sc_Average_sentence_length", "sc_Pausality", "sc_Expressivity", "sc_Average_clauses" \
		# , "sc_Average_word_length", "sc_typo", "sc_first_singular_people", "sc_first_plural_people", "sc_second_people", "sc_third_people", "sc_lexical_complexity" \
		# , "sc_video", "sc_image", "sc_audio", "sc_email", "sc_phone", "sc_location", "sc_organization", "sc_person", "sc_time", "sc_past", "sc_present", "sc_future" \

		# , "s_ARI", "s_CL", "s_GF", "s_FKG", "s_FRE", "u_ARI", "u_CL", "u_GF", "u_FKG", "u_FRE", "c_ARI", "c_CL", "c_GF", "c_FKG", "c_FRE", "sc_ARI", "sc_CL", "sc_GF", "sc_FKG", "sc_FRE"\
		# , "s_posemo", "s_negemo", "s_cogproc", "u_posemo", "u_negemo", "u_cogproc", "c_posemo", "c_negemo", "c_cogproc", "sc_posemo", "sc_negemo", "sc_cogproc" \
		# , "s_insight", "s_cause", "s_discrepancies", "s_tentative", "s_certain", "s_differentiation" \
		# , "u_insight", "u_cause", "u_discrepancies", "u_tentative", "u_certain", "u_differentiation" \
		# , "c_insight", "c_cause", "c_discrepancies", "c_tentative", "c_certain", "c_differentiation" \
		# , "sc_insight", "sc_cause", "sc_discrepancies", "sc_tentative", "sc_certain", "sc_differentiation" \
		# , "s_negate", "u_negate", "c_negate", "sc_negate", "s_motion", "u_motion", "c_motion", "sc_motion"


		f.write("%s\t", %("project_name", "state", "Number_rewards","New_backers", \
			"existing_backers", "goal", "pledged"))




		f.write(str(project_name) + "\t" + self.jsondata["state"] + "\t" + str(len(self.jsondata["rewards"])) + "\t" + str(self.jsondata["New backers"]) + "\t" + \
			str(self.jsondata["existing-backers"]) + "\t" + str(self.jsondata["goal"]) + "\t" + str(self.jsondata["pledged"]) + "\t" + \
			
			"\n")
		# self.NER_file = open("./Result/Analysis_"+str(date_type) + "_" + Variable_list.sub_title_name + "_NER_result.txt", 'r')
		# self.NER_data = dict()

		# for line in self.NER_file:
		# 	NER_list = line.split("\t")

		# 	if self.project_name == NER_list[0]:
		# 		self.NER_data["S_location"] = NER_list[1].strip()
		# 		self.NER_data["S_organization"] = NER_list[2].strip()
		# 		self.NER_data["S_person"] = NER_list[3].strip()
		# 		self.NER_data["S_time"] = NER_list[10].strip()
		# 		self.NER_data["U_location"] = NER_list[4].strip()
		# 		self.NER_data["U_organization"] = NER_list[5].strip()
		# 		self.NER_data["U_person"] = NER_list[6].strip()
		# 		self.NER_data["U_time"] = NER_list[11].strip()
		# 		self.NER_data["C_location"] = NER_list[7].strip()
		# 		self.NER_data["C_organization"] = NER_list[8].strip()
		# 		self.NER_data["C_person"] = NER_list[9].strip()
		# 		self.NER_data["C_time"] = NER_list[12].strip()
		# 		self.NER_data["SC_location"] = NER_list[13].strip()
		# 		self.NER_data["SC_organization"] = NER_list[14].strip()
		# 		self.NER_data["SC_person"] = NER_list[15].strip()
		# 		self.NER_data["SC_time"] = NER_list[16].strip()
		# 		break
		# 	else:
		# 		self.NER_data["S_location"] = 0
		# 		self.NER_data["S_organization"] = 0
		# 		self.NER_data["S_person"] = 0
		# 		self.NER_data["S_time"] = 0
		# 		self.NER_data["U_location"] = 0
		# 		self.NER_data["U_organization"] = 0
		# 		self.NER_data["U_person"] = 0
		# 		self.NER_data["U_time"] = 0
		# 		self.NER_data["C_location"] = 0
		# 		self.NER_data["C_organization"] = 0
		# 		self.NER_data["C_person"] = 0
		# 		self.NER_data["C_time"] = 0
		# 		self.NER_data["SC_location"] = 0
		# 		self.NER_data["SC_organization"] = 0
		# 		self.NER_data["SC_person"] = 0
		# 		self.NER_data["SC_time"] = 0

		# if self.o_jsondata["u_email_link_count"] == 0 or self.date_jsondata[str(date_type) + "_U_viewable_update_count"] == 0:
		# 	self. ["u_email_link_count_1"] = 0
		# else:
		# 	self.o_jsondata["u_email_link_count_1"] = float(self.o_jsondata["u_email_link_count"]) / self.date_jsondata[str(date_type) + "_U_viewable_update_count"]

		# if self.o_jsondata["u_phone_link_count"] == 0 or self.date_jsondata[str(date_type) + "_U_viewable_update_count"] == 0:
		# 	self.o_jsondata["u_phone_link_count_1"] = 0
		# else:
		# 	self.o_jsondata["u_phone_link_count_1"] = float(self.o_jsondata["u_phone_link_count"]) / self.date_jsondata[str(date_type) + "_U_viewable_update_count"]

		# if self.date_jsondata[str(date_type) + "_U_image"] == 0 or self.date_jsondata[str(date_type) + "_U_viewable_update_count"] == 0:
		# 	self.date_jsondata[str(date_type) + "_U_image_1"] = 0
		# else:
		# 	self.date_jsondata[str(date_type) + "_U_image_1"] = float(self.date_jsondata[str(date_type) + "_U_image"]) / self.date_jsondata[str(date_type) + "_U_viewable_update_count"]

		# if self.date_jsondata[str(date_type) + "_U_video"] == 0 or self.date_jsondata[str(date_type) + "_U_viewable_update_count"] == 0:
		# 	self.date_jsondata[str(date_type) + "_U_video_1"] = 0
		# else:
		# 	self.date_jsondata[str(date_type) + "_U_video_1"] = float(self.date_jsondata[str(date_type) + "_U_video"]) / \
		# 														self.date_jsondata[str(date_type) + "_U_viewable_update_count"]

		# if self.date_jsondata[str(date_type) + "_U_audio"] == 0 or self.date_jsondata[str(date_type) + "_U_viewable_update_count"] == 0:
		# 	self.date_jsondata[str(date_type) + "_U_audio_1"] = 0
		# else:
		# 	self.date_jsondata[str(date_type) + "_U_audio_1"] = float(self.date_jsondata[str(date_type) + "_U_audio"]) / \
		# 														self.date_jsondata[str(date_type) + "_U_viewable_update_count"]

		# if self.NER_data["U_location"] == 0 or self.date_jsondata[str(date_type) + "_U_viewable_update_count"] == 0:
		# 	self.NER_data["U_location_1"] = 0
		# else:
		# 	self.NER_data["U_location_1"] = float(self.NER_data["U_location"]) / self.date_jsondata[str(date_type) + "_U_viewable_update_count"]

		# if self.NER_data["U_organization"] == 0 or self.date_jsondata[str(date_type) + "_U_viewable_update_count"] == 0:
		# 	self.NER_data["U_organization_1"] = 0
		# else:
		# 	self.NER_data["U_organization_1"] = float(self.NER_data["U_organization"]) / self.date_jsondata[str(date_type) + "_U_viewable_update_count"]

		# if self.NER_data["U_person"] == 0 or self.date_jsondata[str(date_type) + "_U_viewable_update_count"] == 0:
		# 	self.NER_data["U_person_1"] = 0
		# else:
		# 	self.NER_data["U_person_1"] = float(self.NER_data["U_person"]) / self.date_jsondata[str(date_type) + "_U_viewable_update_count"]

		# if self.NER_data["U_time"] == 0 or self.date_jsondata[str(date_type) + "_U_viewable_update_count"] == 0:
		# 	self.NER_data["U_time_1"] = 0
		# else:
		# 	self.NER_data["U_time_1"] = float(self.NER_data["U_time"]) / self.date_jsondata[str(date_type) + "_U_viewable_update_count"]

		# if self.o_jsondata["c_email_link_count"] == 0 or self.date_jsondata[str(date_type) + "_creator_comments"] == 0:
		# 	self.o_jsondata["c_email_link_count_1"] = 0
		# else:
		# 	self.o_jsondata["c_email_link_count_1"] = float(self.o_jsondata["c_email_link_count"]) / self.date_jsondata[str(date_type) + "_creator_comments"]

		# if self.o_jsondata["c_phone_link_count"] == 0 or self.date_jsondata[str(date_type) + "_creator_comments"] == 0:
		# 	self.o_jsondata["c_phone_link_count_1"] = 0
		# else:
		# 	self.o_jsondata["c_phone_link_count_1"] = float(self.o_jsondata["c_phone_link_count"]) / self.date_jsondata[str(date_type) + "_creator_comments"]

		# if self.NER_data["C_location"] == 0 or self.date_jsondata[str(date_type) + "_creator_comments"] == 0:
		# 	self.NER_data["C_location_1"] = 0
		# else:
		# 	self.NER_data["C_location_1"] = float(self.NER_data["C_location"]) / self.date_jsondata[str(date_type) + "_creator_comments"]

		# if self.NER_data["C_organization"] == 0 or self.date_jsondata[str(date_type) + "_creator_comments"] == 0:
		# 	self.NER_data["C_organization_1"] = 0
		# else:
		# 	self.NER_data["C_organization_1"] = float(self.NER_data["C_organization"]) / self.date_jsondata[str(date_type) + "_creator_comments"]

		# if self.NER_data["C_person"] == 0 or self.date_jsondata[str(date_type) + "_creator_comments"] == 0:
		# 	self.NER_data["C_person_1"] = 0
		# else:
		# 	self.NER_data["C_person_1"] = float(self.NER_data["C_person"]) / self.date_jsondata[str(date_type) + "_creator_comments"]

		# if self.NER_data["C_time"] == 0 or self.date_jsondata[str(date_type) + "_creator_comments"] == 0:
		# 	self.NER_data["C_time_1"] = 0
		# else:
		# 	self.NER_data["C_time_1"] = float(self.NER_data["C_time"]) / self.date_jsondata[str(date_type) + "_creator_comments"]

		# self.tense_data = {str(date_type) + "_s_past": 0, str(date_type) + "_s_present": 0, str(date_type) + "_s_future": 0,\
		# str(date_type) + "_u_past": 0, str(date_type) + "_u_present": 0, str(date_type) + "_u_future": 0,\
		# str(date_type) + "_c_past": 0, str(date_type) + "_c_present": 0, str(date_type) + "_c_future": 0,\
		# str(date_type) + "_sc_past": 0, str(date_type) + "_sc_present": 0, str(date_type) + "_sc_future": 0
		# }

		# self.liwc_data = {str(date_type) + "_s_cogproc": 0, str(date_type) + "_u_cogproc": 0, str(date_type) + "_c_cogproc": 0, str(date_type) + "_sc_cogproc": 0,
		# 				  str(date_type) + "_s_negemo": 0, str(date_type) + "_u_negemo": 0, str(date_type) + "_c_negemo": 0, str(date_type) + "_sc_negemo": 0,
		# 				  str(date_type) + "_s_posemo": 0, str(date_type) + "_u_posemo": 0, str(date_type) + "_c_posemo": 0, str(date_type) + "_sc_posemo": 0,
		# 				  str(date_type) + "_s_insight": 0, str(date_type) + "_s_cause": 0, str(date_type) + "_s_discrepancies": 0,
		# 				  str(date_type) + "_s_tentative": 0, str(date_type) + "_s_certain": 0, str(date_type) + "_s_differentiation": 0,
		# 				  str(date_type) + "_u_insight": 0, str(date_type) + "_u_cause": 0, str(date_type) + "_u_discrepancies": 0, 
		# 				  str(date_type) + "_u_tentative": 0, str(date_type) + "_u_certain": 0, str(date_type) + "_u_differentiation": 0,
		# 				  str(date_type) + "_c_insight": 0, str(date_type) + "_c_cause": 0, str(date_type) + "_c_discrepancies": 0, 
		# 				  str(date_type) + "_c_tentative": 0, str(date_type) + "_c_certain": 0, str(date_type) + "_c_differentiation": 0,
		# 				  str(date_type) + "_sc_insight": 0, str(date_type) + "_sc_cause": 0, str(date_type) + "_sc_discrepancies": 0, 
		# 				  str(date_type) + "_sc_tentative": 0, str(date_type) + "_sc_certain": 0, str(date_type) + "_sc_differentiation": 0,
		# 				  str(date_type) + "_s_negate": 0, str(date_type) + "_u_negate": 0, str(date_type) + "_c_negate": 0, str(date_type) + "_sc_negate": 0,
		# 				  str(date_type) + "_s_motion": 0, str(date_type) + "_u_motion": 0, str(date_type) + "_c_motion": 0, str(date_type) + "_sc_motion": 0}

		# # self.liwc_file = open("LIWC2015 Results (LIWC (50652 files)).csv", 'r')
		# self.liwc_file = open("./Result/LIWC2015 Results (script (10740 files)).csv", 'r')

		# self.reader = csv.reader(self.liwc_file, delimiter=',')
		# for line in self.reader:
		# 	if line[0] == "Filename":
		# 		continue
		# 	else:
		# 		if line[0].split("_")[1] == self.project_name:
		# 			if line[0].split("_")[2] == str(date_type) + ".txt":
		# 				if line[0].split("_")[0] == "s":
		# 					self.tense_data[str(date_type) + "_s_past"] = line[64].strip()
		# 					self.tense_data[str(date_type) + "_s_present"] = line[65].strip()
		# 					self.tense_data[str(date_type) + "_s_future"] = line[66].strip()

		# 					self.liwc_data[str(date_type) + "_s_negate"] = line[24].strip()
		# 					self.liwc_data[str(date_type) + "_s_posemo"] = line[32].strip()
		# 					self.liwc_data[str(date_type) + "_s_negemo"] = line[33].strip()
		# 					self.liwc_data[str(date_type) + "_s_cogproc"] = line[42].strip()
		# 					self.liwc_data[str(date_type) + "_s_insight"] = line[43].strip()
		# 					self.liwc_data[str(date_type) + "_s_cause"] = line[45].strip()
		# 					self.liwc_data[str(date_type) + "_s_discrepancies"] = line[46].strip()
		# 					self.liwc_data[str(date_type) + "_s_tentative"] = line[47].strip()
		# 					self.liwc_data[str(date_type) + "_s_certain"] = line[48].strip()
		# 					self.liwc_data[str(date_type) + "_s_differentiation"] = line[49].strip()
		# 					self.liwc_data[str(date_type) + "_s_motion"] = line[68].strip()

		# 				if line[0].split("_")[0] == "u":
		# 					self.tense_data[str(date_type) + "_u_past"] = line[64].strip()
		# 					self.tense_data[str(date_type) + "_u_present"] = line[65].strip()
		# 					self.tense_data[str(date_type) + "_u_future"] = line[66].strip()

		# 					self.liwc_data[str(date_type) + "_u_negate"] = line[24].strip()
		# 					self.liwc_data[str(date_type) + "_u_posemo"] = line[32].strip()
		# 					self.liwc_data[str(date_type) + "_u_negemo"] = line[33].strip()
		# 					self.liwc_data[str(date_type) + "_u_cogproc"] = line[42].strip()
		# 					self.liwc_data[str(date_type) + "_u_insight"] = line[43].strip()
		# 					self.liwc_data[str(date_type) + "_u_cause"] = line[45].strip()
		# 					self.liwc_data[str(date_type) + "_u_discrepancies"] = line[46].strip()
		# 					self.liwc_data[str(date_type) + "_u_tentative"] = line[47].strip()
		# 					self.liwc_data[str(date_type) + "_u_certain"] = line[48].strip()
		# 					self.liwc_data[str(date_type) + "_u_differentiation"] = line[49].strip()
		# 					self.liwc_data[str(date_type) + "_u_motion"] = line[68].strip()
		# 				if line[0].split("_")[0] == "c":
		# 					self.tense_data[str(date_type) + "_c_past"] = line[64].strip()
		# 					self.tense_data[str(date_type) + "_c_present"] = line[65].strip()
		# 					self.tense_data[str(date_type) + "_c_future"] = line[66].strip()

		# 					self.liwc_data[str(date_type) + "_c_negate"] = line[24].strip()
		# 					self.liwc_data[str(date_type) + "_c_posemo"] = line[32].strip()
		# 					self.liwc_data[str(date_type) + "_c_negemo"] = line[33].strip()
		# 					self.liwc_data[str(date_type) + "_c_cogproc"] = line[42].strip()
		# 					self.liwc_data[str(date_type) + "_c_insight"] = line[43].strip()
		# 					self.liwc_data[str(date_type) + "_c_cause"] = line[45].strip()
		# 					self.liwc_data[str(date_type) + "_c_discrepancies"] = line[46].strip()
		# 					self.liwc_data[str(date_type) + "_c_tentative"] = line[47].strip()
		# 					self.liwc_data[str(date_type) + "_c_certain"] = line[48].strip()
		# 					self.liwc_data[str(date_type) + "_c_differentiation"] = line[49].strip()
		# 					self.liwc_data[str(date_type) + "_c_motion"] = line[68].strip()
		# 				if line[0].split("_")[0] == "sc":
		# 					self.tense_data[str(date_type) + "_sc_past"] = line[64].strip()
		# 					self.tense_data[str(date_type) + "_sc_present"] = line[65].strip()
		# 					self.tense_data[str(date_type) + "_sc_future"] = line[66].strip()

		# 					self.liwc_data[str(date_type) + "_sc_negate"] = line[24].strip()
		# 					self.liwc_data[str(date_type) + "_sc_posemo"] = line[32].strip()
		# 					self.liwc_data[str(date_type) + "_sc_negemo"] = line[33].strip()
		# 					self.liwc_data[str(date_type) + "_sc_cogproc"] = line[42].strip()
		# 					self.liwc_data[str(date_type) + "_sc_insight"] = line[43].strip()
		# 					self.liwc_data[str(date_type) + "_sc_cause"] = line[45].strip()
		# 					self.liwc_data[str(date_type) + "_sc_discrepancies"] = line[46].strip()
		# 					self.liwc_data[str(date_type) + "_sc_tentative"] = line[47].strip()
		# 					self.liwc_data[str(date_type) + "_sc_certain"] = line[48].strip()
		# 					self.liwc_data[str(date_type) + "_sc_differentiation"] = line[49].strip()
		# 					self.liwc_data[str(date_type) + "_sc_motion"] = line[68].strip()



	def result_print(self, date_type):

		if os.path.isfile("./Result/" + str(date_type) + "_" + Variable_list.sub_title_name + "_result.txt") == False:
			f = open("./Result/"+str(date_type) + "_" + Variable_list.sub_title_name + "_result.txt", "w")
			f.write(
				"%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t\n"
				% ("project_name", "state","Number_rewards","New_backers", "existing_backers" ,"backed_project", "created_project", "facebook_ID", "External_link",
	 "creator_before_comments", "creator_after_comments", "time1" \
	 , "goal", "pledged", "total_updates_count", "viewable_updates_count", "total_comments_count", "creator_comments_count", "backers_comments_count", "total_backers_count", "total_rewards_backers" \

	 , "s_Total_words", "s_Nouns", "s_Verbs" \
	 , "s_Adjectives", "s_Adverbs", "s_Sentences", "s_clauses", "s_noun_phrases", "s_phrases", "s_punctuation", "s_mispell_words", "s_Function_words" \
	 , "s_redundancy", "s_characters", "s_url", "s_Modal_verb", "s_Average_sentence_length", "s_Pausality", "s_Expressivity", "s_Average_clauses" \
	 , "s_Average_word_length", "s_typo", "s_first_singular_people", "s_first_plural_people", "s_second_people", "s_third_people", "s_lexical_complexity" \
	 , "s_video", "s_image", "s_audio", "s_email", "s_phone", "s_location", "s_organization", "s_person", "s_time", "s_past", "s_present", "s_future" \

	 , "U_Total_words", "U_Total_words_1", "U_Nouns", "U_Nouns_1", "U_Nouns_2", "U_Verbs", "U_Verbs_1", "U_Verbs_2" \
	 , "U_Adjectives", "U_Adjectives_1", "U_Adjectives_2", "U_Adverbs", "U_Adverbs1", "U_Adverbs_2", "U_Sentences", "U_Sentences_1", "U_clauses", "U_clauses_1", "U_noun_phrases", "U_noun_phrases_1" \
	 , "U_phrases", "U_phrases_1", "U_punctuation", "U_punctuation_1", "U_punctuation_2", "U_mispell_words", "U_mispell_words_1", "U_Function_words" \
	 , "U_Function_words_1", "U_Function_words_2", "U_redundancy", "U_characters", "U_characters_1", "U_characters_2", "U_url", "U_url_1", "U_url_2", "U_Modal_verb", "U_modal_verbs_1", "U_modal_verbs_2" \
	 , "U_Average_sentence_length", "U_Pausality", "U_Expressivity", "U_Average_clauses", "U_Average_word_length", "U_typo" \
	 , "U_first_singular_people", "U_first_singular_people_1", "U_first_singular_people_2", "U_first_plural_people", "U_first_plural_people_1", "U_first_plural_people_2" \
	 , "U_second_people", "U_second_people_1", "U_second_people_2", "U_third_people", "U_third_people_1", "U_third_people_2", "U_lexical_complexity", "u_video", "u_video_1", "u_image", "u_image_1", "u_audio", "u_audio_1", "u_email", "u_email_1", "u_phone", "u_phone_1" \
	 , "u_location", "u_location_1", "u_organization", "u_organization_1", "u_person", "u_person_1", "u_time", "u_time_1", "u_past", "u_present", "u_future" \

	 , "C_Total_words", "C_Total_words_1", "C_Nouns", "C_Nouns_1", "C_Nouns_2", "C_Verbs", "C_Verbs_1", "C_Verbs_2" \
	 , "C_Adjectives", "C_Adjectives_1", "C_Adjectives_2", "C_Adverbs", "C_Adverbs1", "C_Adverbs_2", "C_Sentences", "C_Sentences_1", "C_clauses", "C_clauses_1", "C_noun_phrases", "C_noun_phrases_1" \
	 , "C_phrases", "C_phrases_1", "C_punctuation", "C_punctuation_1", "C_punctuation_2", "C_mispell_words", "C_mispell_words_1", "C_Function_words" \
	 , "C_Function_words_1", "C_Function_words_2", "C_redundancy", "C_characters", "C_characters_1", "C_characters_2", "C_url", "C_url_1", "C_url_2", "C_Modal_verb", "C_modal_verbs_1", "C_modal_verbs_2" \
	 , "C_Average_sentence_length", "C_Pausality", "C_Expressivity", "C_Average_clauses", "C_Average_word_length", "C_typo" \
	 , "C_first_singular_people", "C_first_singular_people_1", "C_first_singular_people_2", "C_first_plural_people", "C_first_plural_people_1", "C_first_plural_people_2" \
	 , "C_second_people", "C_second_people_1", "C_second_people_2", "C_third_people", "C_third_people_1", "C_third_people_2", "C_lexical_complexity" \
	 , "C_email", "C_email_1", "C_phone", "C_phone_1", "C_location", "C_location_1", "C_organization", "C_organization_1", "C_person", "C_person_1", "C_time", "C_time_1", "C_past", "C_present", "C_future"\

	 , "sc_Total_words", "sc_Nouns", "sc_Verbs", "sc_Adjectives", "sc_Adverbs", "sc_Sentences", "sc_clauses", "sc_noun_phrases", "sc_phrases", "sc_punctuation", "sc_mispell_words", "sc_Function_words" \
	 , "sc_redundancy", "sc_characters", "sc_url", "sc_Modal_verb", "sc_Average_sentence_length", "sc_Pausality", "sc_Expressivity", "sc_Average_clauses" \
	 , "sc_Average_word_length", "sc_typo", "sc_first_singular_people", "sc_first_plural_people", "sc_second_people", "sc_third_people", "sc_lexical_complexity" \
	 , "sc_video", "sc_image", "sc_audio", "sc_email", "sc_phone", "sc_location", "sc_organization", "sc_person", "sc_time", "sc_past", "sc_present", "sc_future" \

	 , "s_ARI", "s_CL", "s_GF", "s_FKG", "s_FRE", "u_ARI", "u_CL", "u_GF", "u_FKG", "u_FRE", "c_ARI", "c_CL", "c_GF", "c_FKG", "c_FRE", "sc_ARI", "sc_CL", "sc_GF", "sc_FKG", "sc_FRE"\
	 , "s_posemo", "s_negemo", "s_cogproc", "u_posemo", "u_negemo", "u_cogproc", "c_posemo", "c_negemo", "c_cogproc", "sc_posemo", "sc_negemo", "sc_cogproc" \
	 , "s_insight", "s_cause", "s_discrepancies", "s_tentative", "s_certain", "s_differentiation" \
	 , "u_insight", "u_cause", "u_discrepancies", "u_tentative", "u_certain", "u_differentiation" \
	 , "c_insight", "c_cause", "c_discrepancies", "c_tentative", "c_certain", "c_differentiation" \
	 , "sc_insight", "sc_cause", "sc_discrepancies", "sc_tentative", "sc_certain", "sc_differentiation" \
	 , "s_negate", "u_negate", "c_negate", "sc_negate", "s_motion", "u_motion", "c_motion", "sc_motion"))

		else:
			f = open("./Result/"+str(date_type) + "_" + Variable_list.sub_title_name + "_result.txt", "a")

		f.write(str(self.project_name) +"\t" + self.jsondata["state"] +"\t"+str(len(self.jsondata["rewards"])) + "\t" + str(self.jsondata["New backers"]) + "\t" + str(self.jsondata["existing-backers"]) +"\t" + str(self.jsondata["creator"]["backed_projects_count"]) + "\t" + str(self.jsondata["creator"]["created_projects_count"]) + "\t"+ str(self.jsondata["facebook_check"]) + "\t" + str(self.jsondata["creator"]["link_count"]) + "\t" + str(self.jsondata["creator"]["before_comment_count"]) + "\t" + str(self.date_jsondata[str(date_type) + "_creator_after_comments"]) + "\t" + str(self.jsondata["creator"]["time1"]) + "\t" \
				+ str(self.jsondata["goal"]) + "\t" + str(self.jsondata["pledged"]) + "\t" + str(self.date_jsondata[str(date_type) + "_U_total_update_count"]) + "\t" + str(self.date_jsondata[str(date_type) + "_U_viewable_update_count"]) + "\t" \
				+ str(self.date_jsondata[str(date_type) + "_total_comments"]) + "\t" + str(self.date_jsondata[str(date_type) + "_creator_comments"]) + "\t" + str(self.date_jsondata[str(date_type) + "_backers_comments"]) + "\t" \
				+ str(self.jsondata["backers_count"]) + "\t" + str(self.jsondata["total_rewards_backers"]) + "\t" \

				+ str(self.s_jsondata["Total_words"]) + "\t" + str(self.s_jsondata["Nouns"]) + "\t" + str(self.s_jsondata["Verbs"]) + "\t" + str(self.s_jsondata["Adjectives"]) + "\t" + str(self.s_jsondata["Adverbs"]) + "\t" + str(self.s_jsondata["Sentences"]) + "\t" + str(self.s_jsondata["clauses"]) + "\t" \
				+ str(self.s_jsondata["noun_phrases"]) + "\t" + str(self.s_jsondata["phrases"]) + "\t" + str(self.s_jsondata["punctuation"]) + "\t" + str(self.s_jsondata["mispell_words"]) + "\t" + str(self.s_jsondata["Function_words"]) + "\t" \
				+ str(self.s_jsondata["redundancy"]) + "\t" + str(self.s_jsondata["characters"]) + "\t" + str(self.s_jsondata["url"]) + "\t" + str(self.s_jsondata["Modal_verb"]) + "\t" \
				+ str(self.s_jsondata["Average_sentence_length"]) + "\t" + str(self.s_jsondata["Pausality"]) + "\t" + str(self.s_jsondata["Expressivity"]) + "\t" + str(self.s_jsondata["Average_clauses"]) + "\t" + str(self.s_jsondata["Average_word_length"]) + "\t" + str(self.s_jsondata["typo"]) + "\t" \
				+ str(self.s_jsondata["first_singular_people"]) + "\t" + str(self.s_jsondata["first_plural_people"]) + "\t" + str(self.s_jsondata["second_people"]) + "\t" + str(self.s_jsondata["third_people"]) + "\t" + str(self.s_jsondata["lexical_complexity"]) + "\t" \
				+ str(self.jsondata["story_content"]["video_count"]) + "\t" + str(self.jsondata["story_content"]["image_count"]) + "\t" + str(self.jsondata["story_content"]["audio_count"]) + "\t" + str(self.o_jsondata["s_email_link_count"]) + "\t" + str(self.o_jsondata["s_phone_link_count"]) + "\t" \
				+ str(self.NER_data["S_location"]) + "\t" + str(self.NER_data["S_organization"]) + "\t" + str(self.NER_data["S_person"]) + "\t" + str(self.NER_data["S_time"]) + "\t" \
				+ str(self.tense_data[str(date_type) + "_s_past"]) + "\t" + str(self.tense_data[str(date_type) + "_s_present"]) + "\t" + str(self.tense_data[str(date_type) + "_s_future"]) + "\t" \
 
				+ str(self.u_jsondata["Total_words"]) + "\t" + str(self.u_jsondata["Total_words_1"]) + "\t" + str(self.u_jsondata["Nouns"]) + "\t" + str(self.u_jsondata["Nouns_1"]) + "\t" + str(self.u_jsondata["Nouns_2"]) + "\t" \
				+ str(self.u_jsondata["Verbs"]) + "\t" + str(self.u_jsondata["Verbs_1"]) + "\t" + str(self.u_jsondata["Verbs_2"]) + "\t" + str(self.u_jsondata["Adjectives"]) + "\t" + str(self.u_jsondata["Adjectives_1"]) + "\t" + str(self.u_jsondata["Adjectives_2"]) + "\t" \
				+ str(self.u_jsondata["Adverbs"]) + "\t" + str(self.u_jsondata["Adverbs_1"]) + "\t" + str(self.u_jsondata["Adverbs_2"]) + "\t" + str(self.u_jsondata["Sentences"]) + "\t" + str(self.u_jsondata["Sentences_1"]) + "\t" \
				+ str(self.u_jsondata["clauses"]) + "\t" + str(self.u_jsondata["clauses_1"]) + "\t" + str(self.u_jsondata["noun_phrases"]) + "\t" + str(self.u_jsondata["noun_phrases_1"]) + "\t" \
				+ str(self.u_jsondata["phrases"]) + "\t" + str(self.u_jsondata["phrases_1"]) + "\t" + str(self.u_jsondata["punctuation"]) + "\t" + str(self.u_jsondata["punctuation_1"]) + "\t" + str(self.u_jsondata["punctuation_2"]) + "\t" \
				+ str(self.u_jsondata["mispell_words"]) + "\t" + str(self.u_jsondata["mispell_words_1"]) + "\t" + str(self.u_jsondata["Function_words"]) + "\t" + str(self.u_jsondata["Function_words_1"]) + "\t" + str(self.u_jsondata["Function_words_2"]) + "\t" \
				+ str(self.u_jsondata["redundancy"]) + "\t" + str(self.u_jsondata["characters"]) + "\t" + str(self.u_jsondata["characters_1"]) + "\t" + str(self.u_jsondata["characters_2"]) + "\t" \
				+ str(self.u_jsondata["url"]) + "\t" + str(self.u_jsondata["url_1"]) + "\t" + str(self.u_jsondata["url_2"]) + "\t" + str(self.u_jsondata["Modal_verb"]) + "\t" + str(self.u_jsondata["modal_verbs_1"]) + "\t" + str(self.u_jsondata["modal_verbs_2"]) + "\t" \
				+ str(self.u_jsondata["Average_sentence_length"]) + "\t" + str(self.u_jsondata["Pausality"]) + "\t" + str(self.u_jsondata["Expressivity"]) + "\t" + str(self.u_jsondata["Average_clauses"]) + "\t" + str(self.u_jsondata["Average_word_length"]) + "\t" \
				+ str(self.u_jsondata["typo"]) + "\t" + str(self.u_jsondata["first_singular_people"]) + "\t" + str(self.u_jsondata["first_singular_people_1"]) + "\t" + str(self.u_jsondata["first_singular_people_2"]) + "\t" \
				+ str(self.u_jsondata["first_plural_people"]) + "\t" + str(self.u_jsondata["first_plural_people_1"]) + "\t" + str(self.u_jsondata["first_plural_people_2"]) + "\t" \
				+ str(self.u_jsondata["second_people"]) + "\t" + str(self.u_jsondata["second_people_1"]) + "\t" + str(self.u_jsondata["second_people_2"]) + "\t" \
				+ str(self.u_jsondata["third_people"]) + "\t" + str(self.u_jsondata["third_people_1"]) + "\t" + str(self.u_jsondata["third_people_2"]) + "\t" + str(self.u_jsondata["lexical_complexity"]) + "\t" \
				+ str(self.date_jsondata[str(date_type) + "_U_video"]) + "\t" + str(self.date_jsondata[str(date_type) + "_U_video_1"]) + "\t" + str(self.date_jsondata[str(date_type) + "_U_image"]) + "\t" + str(self.date_jsondata[str(date_type) + "_U_image_1"]) + "\t" \
				+ str(self.date_jsondata[str(date_type) + "_U_audio"]) + "\t" + str(self.date_jsondata[str(date_type) + "_U_audio_1"]) + "\t" \
				+ str(self.o_jsondata["u_email_link_count"]) + "\t" + str(self.o_jsondata["u_email_link_count_1"]) + "\t" + str(self.o_jsondata["u_phone_link_count"]) + "\t" + str(self.o_jsondata["u_phone_link_count_1"]) + "\t" \
				+ str(self.NER_data["U_location"]) + "\t" + str(self.NER_data["U_location_1"]) + "\t" + str(self.NER_data["U_organization"]) + "\t" + str(self.NER_data["U_organization_1"]) + "\t" \
				+ str(self.NER_data["U_person"]) + "\t" + str(self.NER_data["U_person_1"]) + "\t" + str(self.NER_data["U_time"]) + "\t" + str(self.NER_data["U_time_1"]) + "\t" \
				+ str(self.tense_data[str(date_type) + "_u_past"]) + "\t" + str(self.tense_data[str(date_type) + "_u_present"]) + "\t" + str(self.tense_data[str(date_type) + "_u_future"]) + "\t" \

				+ str(self.c_jsondata["Total_words"]) + "\t" + str(self.c_jsondata["Total_words_1"]) + "\t" + str(self.c_jsondata["Nouns"]) + "\t" + str(self.c_jsondata["Nouns_1"]) + "\t" + str(self.c_jsondata["Nouns_2"]) + "\t" \
				+ str(self.c_jsondata["Verbs"]) + "\t" + str(self.c_jsondata["Verbs_1"]) + "\t" + str(self.c_jsondata["Verbs_2"]) + "\t" + str(self.c_jsondata["Adjectives"]) + "\t" + str(self.c_jsondata["Adjectives_1"]) + "\t" + str(self.c_jsondata["Adjectives_2"]) + "\t" \
				+ str(self.c_jsondata["Adverbs"]) + "\t" + str(self.c_jsondata["Adverbs_1"]) + "\t" + str(self.c_jsondata["Adverbs_2"]) + "\t" + str(self.c_jsondata["Sentences"]) + "\t" + str(self.c_jsondata["Sentences_1"]) + "\t" \
				+ str(self.c_jsondata["clauses"]) + "\t" + str(self.c_jsondata["clauses_1"]) + "\t" + str(self.c_jsondata["noun_phrases"]) + "\t" + str(self.c_jsondata["noun_phrases_1"]) + "\t" \
				+ str(self.c_jsondata["phrases"]) + "\t" + str(self.c_jsondata["phrases_1"]) + "\t" + str(self.c_jsondata["punctuation"]) + "\t" + str(self.c_jsondata["punctuation_1"]) + "\t" + str(self.c_jsondata["punctuation_2"]) + "\t" \
				+ str(self.c_jsondata["mispell_words"]) + "\t" + str(self.c_jsondata["mispell_words_1"]) + "\t" + str(self.c_jsondata["Function_words"]) + "\t" + str(self.c_jsondata["Function_words_1"]) + "\t" + str(self.c_jsondata["Function_words_2"]) + "\t" \
				+ str(self.c_jsondata["redundancy"]) + "\t" + str(self.c_jsondata["characters"]) + "\t" + str(self.c_jsondata["characters_1"]) + "\t" + str(self.c_jsondata["characters_2"]) + "\t" \
				+ str(self.c_jsondata["url"]) + "\t" + str(self.c_jsondata["url_1"]) + "\t" + str(self.c_jsondata["url_2"]) + "\t" + str(self.c_jsondata["Modal_verb"]) + "\t" + str(self.c_jsondata["modal_verbs_1"]) + "\t" + str(self.c_jsondata["modal_verbs_2"]) + "\t" \
				+ str(self.c_jsondata["Average_sentence_length"]) + "\t" + str(self.c_jsondata["Pausality"]) + "\t" + str(self.c_jsondata["Expressivity"]) + "\t" + str(self.c_jsondata["Average_clauses"]) + "\t" + str(self.c_jsondata["Average_word_length"]) + "\t" \
				+ str(self.c_jsondata["typo"]) + "\t" + str(self.c_jsondata["first_singular_people"]) + "\t" + str(self.c_jsondata["first_singular_people_1"]) + "\t" + str(self.c_jsondata["first_singular_people_2"]) + "\t" \
				+ str(self.c_jsondata["first_plural_people"]) + "\t" + str(self.c_jsondata["first_plural_people_1"]) + "\t" + str(self.c_jsondata["first_plural_people_2"]) + "\t" \
				+ str(self.c_jsondata["second_people"]) + "\t" + str(self.c_jsondata["second_people_1"]) + "\t" + str(self.c_jsondata["second_people_2"]) + "\t" \
				+ str(self.c_jsondata["third_people"]) + "\t" + str(self.c_jsondata["third_people_1"]) + "\t" + str(self.c_jsondata["third_people_2"]) + "\t" + str(self.c_jsondata["lexical_complexity"]) + "\t" \
				+ str(self.o_jsondata["c_email_link_count"]) + "\t" + str(self.o_jsondata["c_email_link_count_1"]) + "\t" + str(self.o_jsondata["c_phone_link_count"]) + "\t" + str(self.o_jsondata["c_phone_link_count_1"]) + "\t" \
				+ str(self.NER_data["C_location"]) + "\t" + str(self.NER_data["C_location_1"]) + "\t" + str(self.NER_data["C_organization"]) + "\t" + str(self.NER_data["C_organization_1"]) + "\t" \
				+ str(self.NER_data["C_person"]) + "\t" + str(self.NER_data["C_person_1"]) + "\t" + str(self.NER_data["C_time"]) + "\t" + str(self.NER_data["C_time_1"]) + "\t" \
				+ str(self.tense_data[str(date_type) + "_c_past"]) + "\t" + str(self.tense_data[str(date_type) + "_c_present"]) + "\t" + str(self.tense_data[str(date_type) + "_c_future"]) + "\t" \

				+ str(self.sc_jsondata["Total_words"]) + "\t" + str(self.sc_jsondata["Nouns"]) + "\t" + str(self.sc_jsondata["Verbs"]) + "\t" + str(self.sc_jsondata["Adjectives"]) + "\t" + str(self.sc_jsondata["Adverbs"]) + "\t" + str(self.sc_jsondata["Sentences"]) + "\t" + str(self.sc_jsondata["clauses"]) + "\t" \
				+ str(self.sc_jsondata["noun_phrases"]) + "\t" + str(self.sc_jsondata["phrases"]) + "\t" + str(self.sc_jsondata["punctuation"]) + "\t" + str(self.sc_jsondata["mispell_words"]) + "\t" + str(self.sc_jsondata["Function_words"]) + "\t" \
				+ str(self.sc_jsondata["redundancy"]) + "\t" + str(self.sc_jsondata["characters"]) + "\t" + str(self.sc_jsondata["url"]) + "\t" + str(self.sc_jsondata["Modal_verb"]) + "\t" \
				+ str(self.sc_jsondata["Average_sentence_length"]) + "\t" + str(self.sc_jsondata["Pausality"]) + "\t" + str(self.sc_jsondata["Expressivity"]) + "\t" + str(self.sc_jsondata["Average_clauses"]) + "\t" + str(self.sc_jsondata["Average_word_length"]) + "\t" + str(self.sc_jsondata["typo"]) + "\t" \
				+ str(self.sc_jsondata["first_singular_people"]) + "\t" + str(self.sc_jsondata["first_plural_people"]) + "\t" + str(self.sc_jsondata["second_people"]) + "\t" + str(self.sc_jsondata["third_people"]) + "\t" + str(self.sc_jsondata["lexical_complexity"]) + "\t" \
				+ str(self.jsondata["story_content"]["video_count"]) + "\t" + str(self.jsondata["story_content"]["image_count"]) + "\t" + str(self.jsondata["story_content"]["audio_count"]) + "\t" + str(self.o_jsondata["sc_email_link_count"]) + "\t" + str(self.o_jsondata["sc_phone_link_count"]) + "\t" \
				+ str(self.NER_data["SC_location"]) + "\t" + str(self.NER_data["SC_organization"]) + "\t" + str(self.NER_data["SC_person"]) + "\t" + str(self.NER_data["SC_time"]) + "\t" \
				+ str(self.tense_data[str(date_type) + "_sc_past"]) + "\t" + str(self.tense_data[str(date_type) + "_sc_present"]) + "\t" + str(self.tense_data[str(date_type) + "_sc_future"])

				+ "\t" + str(self.s_jsondata["s_ari"]) + "\t" + str(self.s_jsondata["s_CL"]) + "\t" + str(self.s_jsondata["s_GF"]) + "\t" + str(self.s_jsondata["s_FKG"]) + "\t" + str(self.s_jsondata["s_FRE"]) \
				+ "\t" + str(self.u_jsondata["u_ari"]) + "\t" + str(self.u_jsondata["u_CL"]) + "\t" + str(self.u_jsondata["u_GF"]) + "\t" + str(self.u_jsondata["u_FKG"]) + "\t" + str(self.u_jsondata["u_FRE"]) \
				+ "\t" + str(self.c_jsondata["c_ari"]) + "\t" + str(self.c_jsondata["c_CL"]) + "\t" + str(self.c_jsondata["c_GF"]) + "\t" + str(self.c_jsondata["c_FKG"]) + "\t" + str(self.c_jsondata["c_FRE"]) \
				+ "\t" + str(self.sc_jsondata["sc_ari"]) + "\t" + str(self.sc_jsondata["sc_CL"]) + "\t" + str(self.sc_jsondata["sc_GF"]) + "\t" + str(self.sc_jsondata["sc_FKG"]) + "\t" + str(self.sc_jsondata["sc_FRE"]) \
				+ "\t" + str(self.liwc_data[str(date_type) + "_s_posemo"]) + "\t" + str(self.liwc_data[str(date_type) + "_s_negemo"]) + "\t" + str(self.liwc_data[str(date_type) + "_s_cogproc"]) \
				+ "\t" + str(self.liwc_data[str(date_type) + "_u_posemo"]) + "\t" + str(self.liwc_data[str(date_type) + "_u_negemo"]) + "\t" + str(self.liwc_data[str(date_type) + "_u_cogproc"]) \
				+ "\t" + str(self.liwc_data[str(date_type) + "_c_posemo"]) + "\t" + str(self.liwc_data[str(date_type) + "_c_negemo"]) + "\t" + str(self.liwc_data[str(date_type) + "_c_cogproc"]) \
				+ "\t" + str(self.liwc_data[str(date_type) + "_sc_posemo"]) + "\t" + str(self.liwc_data[str(date_type) + "_sc_negemo"]) + "\t" + str(self.liwc_data[str(date_type) + "_sc_cogproc"]) \
				+ "\t" + str(self.liwc_data[str(date_type) + "_s_insight"]) + "\t" + str(self.liwc_data[str(date_type) + "_s_cause"]) + "\t" + str(self.liwc_data[str(date_type) + "_s_discrepancies"]) + "\t" + str(self.liwc_data[str(date_type) + "_s_tentative"]) + "\t" + str(self.liwc_data[str(date_type) + "_s_certain"]) + "\t" + str(self.liwc_data[str(date_type) + "_s_differentiation"]) \
				+ "\t" + str(self.liwc_data[str(date_type) + "_u_insight"]) + "\t" + str(self.liwc_data[str(date_type) + "_u_cause"]) + "\t" + str(self.liwc_data[str(date_type) + "_u_discrepancies"]) + "\t" + str(self.liwc_data[str(date_type) + "_u_tentative"]) + "\t" + str(self.liwc_data[str(date_type) + "_u_certain"]) + "\t" + str(self.liwc_data[str(date_type) + "_u_differentiation"]) \
				+ "\t" + str(self.liwc_data[str(date_type) + "_c_insight"]) + "\t" + str(self.liwc_data[str(date_type) + "_c_cause"]) + "\t" + str(self.liwc_data[str(date_type) + "_c_discrepancies"]) + "\t" + str(self.liwc_data[str(date_type) + "_c_tentative"]) + "\t" + str(self.liwc_data[str(date_type) + "_c_certain"]) + "\t" + str(self.liwc_data[str(date_type) + "_c_differentiation"]) \
				+ "\t" + str(self.liwc_data[str(date_type) + "_sc_insight"]) + "\t" + str(self.liwc_data[str(date_type) + "_sc_cause"]) + "\t" + str(self.liwc_data[str(date_type) + "_sc_discrepancies"]) + "\t" + str(self.liwc_data[str(date_type) + "_sc_tentative"]) + "\t" + str(self.liwc_data[str(date_type) + "_sc_certain"]) + "\t" + str(self.liwc_data[str(date_type) + "_sc_differentiation"]) \
				+ "\t" + str(self.liwc_data[str(date_type) + "_s_negate"]) + "\t" + str(self.liwc_data[str(date_type) + "_u_negate"]) + "\t" + str(self.liwc_data[str(date_type) + "_c_negate"]) + "\t" + str(self.liwc_data[str(date_type) + "_sc_negate"]) \
				+ "\t" + str(self.liwc_data[str(date_type) + "_s_motion"]) + "\t" + str(self.liwc_data[str(date_type) + "_u_motion"]) + "\t" + str(self.liwc_data[str(date_type) + "_c_motion"]) + "\t" + str(self.liwc_data[str(date_type) + "_sc_motion"])
				+ "\n")
		f.close()