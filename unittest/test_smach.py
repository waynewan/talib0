from smach import *

def F1(rt):
	prev_state = rt['prev_state']
	curr_state = rt['curr_state']
	curr_event = rt['curr_event']
	print("{}--({})-->{}".format(prev_state,curr_event,curr_state))
	return []

def E1(rt):
	print("########################")
	print("# end with error:      #")
	print(rt['err'])
	print("########################")
	return None

machine_spec = {
	'state_names' : [ 'BEGIN', 'S1', 'S2', 'S3', 'S4', 'S5', 'TT', 'ERR' ],
	'action_vector' : [ F1,F1,F1,F1,F1,F1,F1,E1 ],
	'pathways' : [
		#   0     1     2     3     4     5     6     7    
		[ '---','E01','---','---','---','---','---','ERR', ], # 0
		[ '---','---','E02','---','---','---','---','ERR', ], # 1
		[ 'R01','---','---','E03','E04','E05','---','ERR', ], # 2
		[ 'R02','---','---','E03','E04','E05','---','ERR', ], # 3
		[ 'R03','---','---','E03','E04','E05','---','ERR', ], # 4
		[ '---','---','---','---','E04','---','E06','ERR', ], # 5
		[ '---','---','---','---','---','---','---','ERR', ], # 6
		[ '---','---','---','---','---','---','---','ERR', ], # 7
	],
	'terminal_states' : [ 6,7 ],
}

if(__name__=='__main__'):
	events = [ 'E01','E02','E03','E03','E05','E04','E05','E06' ]
	machine_rt = new_machine_rt(events=events)
	pprint("###################")
	pprint(machine_spec['action_vector'])
	print_statemachine(machine_spec)
	pprint("###################")
	rc = execute_machine(machine_spec,machine_rt)
	pprint("###################")
	print("final state:", machine_rt['curr_state'])
	print("last event:", machine_rt['curr_event'])
	if(rc==0):
		print("DONE - successful")
	else:
		print("FAILED - rc:", rc)

