import requests
import json
import os
import argparse
import sys
import random

# printing required data only
def display_program(args, program):
	for key in program:
			if key not in ["colour", "logo", "report_path", "tagline", "can_view_teaser", "collaboration_enabled", "trial", "demo", "can_quick_view", "accept_invitation_path", "code", "safe_harbor_status", "safe_harbor_status_string", "teaser_path", "ended", "ongoing", "started", "in_progress","on_demand", "managed?", "started?" ,"can_submit_report", "secret_participation_type", "invited_status", "no_disclosure"]:
				if key == "name":
					print(key.title(), str(program[key]).title(), sep='\t\t: ')

				# filter to not print the field which is given as filter
				elif key == "license_key":
					if (args.type is None):			
						print("Type", str(program[key].replace('_',' ').replace('pro','')).title(), sep='\t\t: ')
				elif key == "participation":
					if (args.type is None):
						print((key.replace('_',' ')).title(), str(program[key]).title(), sep='\t: ')
				elif key == "scope_rank_url":
					if (args.type is None):
						print("Scope Rank", str(program[key]).title(), sep='\t: ')
				
				elif key == "program_url":
					print("Program URL", "https://bugcrowd.com" + str(program[key]), sep='\t: ')
				elif key == "industry_name":
					print("Industry", str(program[key]).title(), sep='\t: ')
				
				# print badge_type only when recent
				elif key == "badge_type":
					if program[key] == "recent":
						print((key.replace('_',' ')).title(), str(program[key]).title(), sep='\t: ')
				
				# print mix-max rewards without clutter
				elif key == "min_rewards":
					print("Min-Max Rewards", "$"+str(program["min_rewards"]) + "-$" + str(program["max_rewards"]), sep='\t: ')
				elif key == "max_rewards":
					pass

				elif program[key] not in  ["", "not_applicable", int(0) ]:
					print((key.replace('_',' ')).title(), str(program[key]).title(), sep='\t: ')
	print()


def filter(args, programs):
	# --latest
	if args.latest:
		for program in programs:
			if ('badge_type' in program) and (program['badge_type'] == "recent"):
				display_program(args, program)
		sys.exit()

	# implement filters
	filter_programs = []
	for program in programs:
		# --type filter
		if ((args.type is None) or ((args.type.lower() == "vdp" and program['license_key'] == "vdp_pro") or (args.type.lower() == "bounty" and program['license_key'] == "bug_bounty"))):

			# --part filter
			if ((args.part is None) or ((args.part.lower() == "private" and program['participation'] == "private") or (args.part.lower() == "public" and program['participation'] == "public"))):

				# --scope filter
				if ((args.scope is None) or (program['scope_rank_url'] == args.scope)):
					filter_programs.append(program)
	return filter_programs

def main():
	# Create an ArgumentParser object
	parser = argparse.ArgumentParser(description='Solution to your "Which program should I hack in BugCrowd?".')

	# Add command-line arguments
	parser.add_argument('-f', '--fresh', action='store_true', help='Generates a fresh program search and showcases recently added entries.')
	parser.add_argument('-l', '--latest', action='store_true', help='Display newly added Programs.')
	parser.add_argument('-n', '--name', action='store_true', help='Show only the Program name field.')
	parser.add_argument('-r', '--random', action='store_true', help='Select a random Program w/w.o. filters.')
	parser.add_argument('-t', '--type', type=str, help='Filter Programs based on Compensation Type (VDP, Bounty).')
	parser.add_argument('-p', '--part', type=str, help='Filter Programs based on Participation Status (Private/Public).')
	parser.add_argument('-s', '--scope', type=int, help='Filter Programs based on Scope rating (1-5).')


	# Parse the command-line arguments    
	args = parser.parse_args()
	programs=[]

	# --fresh
	if (args.fresh):
		if os.path.exists('bugcrowd.json'):
			os.remove('bugcrowd.json')

	if not os.path.isfile('bugcrowd.json'):
		r = requests.get('https://bugcrowd.com/programs.json')
		data_json = json.loads(r.text)
		meta = data_json['meta']
		pages = meta['totalPages']+1

		# going through all pages of bugcrowd programs to get json data
		for page in range(1,pages+1):
			r = requests.get('https://bugcrowd.com/programs.json?page[]='+str(page))
			obj = json.loads(r.text)

			# cleaning data other than programs to ez combine
			obj.pop("filteredQueryParams")
			obj.pop("meta")

			# replacing scope url with scope value
			count=0
			for program in obj['programs']:
				scope_url = 'https://bugcrowd.com/'+ obj['programs'][count]["scope_rank_url"]
				scope_rank = json.loads(requests.get(scope_url).text)["scopeRank"]
				obj['programs'][count]["scope_rank_url"] = scope_rank
				count+=1
			
			# writing data into bugcrowd.json for efficiency
			if page == 1:
				with open('bugcrowd.json', 'w') as f:
					json.dump(obj, f, indent=4)
			else:
				# append new program data to earlier pages
				with open('bugcrowd.json', 'r+') as f:
					file_obj = json.load(f)
					for program in obj['programs']:
						file_obj['programs'].append(program)
						f.seek(0)
						json.dump(file_obj, f, indent=4)

	# creating a list of programs
	with open('bugcrowd.json', 'r') as f:
		obj = json.load(f)
		for program in obj['programs']:
			programs.append(program)	

	# print programs after filtering 
	filter_programs= filter(args, programs)

	# --random ; pick a random Program after filters
	if args.random:
		random_program = random.choice(filter_programs)
		display_program(args, random_program)
		sys.exit()

	count=1
	for program in filter_programs:
		# --name
		if args.name:
			print(count, program["name"], sep=". ")
		else:
			print(count, end=".\n")
			display_program(args, program)
		count+=1

if __name__ == "__main__":
    main()
