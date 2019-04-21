import os
import numpy as np
import argparse

# to read the input
def read(configuration):

	initial_state = []

	data = configuration.split(",")

	for element in data:
		initial_state.append(int(element))

	return np.reshape(initial_state,(3,3))

# To locate the blank tile
def blank_tile_location(A):
	loc = np.argwhere(A == 0)
	return loc

# To move up
def up(B):
	A= np.copy(B)
	loc = blank_tile_location(A)

	row = loc[:,0]
	col = loc[:,1]

	if row == 0:
		status = False
	else: # row == 1 or row == 2:
		A[row,col] = A[row -1 ,col]
		A[row -1,col]= 0

		status = True

	return A, status

#to move down
def down(B):
	A= np.copy(B)
	loc = blank_tile_location(A)

	row = loc[:,0]
	col = loc[:,1]

	if row == 2:
		status = False
	else: # row == 1 or row == 2:
		temp = A[row+1 ,col]
		A[row+1,col]= A[row,col]
		A[row,col] = temp
		status = True
	return A, status

# to move left 
def left(B):
	A= np.copy(B)
	loc = blank_tile_location(A)

	row = loc[:,0]
	col = loc[:,1]

	if col == 0:
		status = False
	else: # row == 1 or row == 2:
		temp = A[row ,col-1]
		A[row,col-1]= A[row,col]
		A[row,col] = temp
		status = True
	return A, status

# to move right
def right(B):
	A= np.copy(B)
	loc = blank_tile_location(A)

	row = loc[:,0]
	col = loc[:,1]

	#print(row,col)
	if col == 2:
		status = False
	else: # row == 1 or row == 2:
		temp = A[row ,col+1]
		A[row,col+1]= A[row,col]
		A[row,col] = temp
		status = True
	return A, status

# to check if the node is repeated
def isRepeated_set(node,n_set):
	node_set = set_conversion(node)
	return node_set in n_set

# to check if the goal is reached
def goal_check(B,goal_node):
	status = np.array_equal(B,goal_node)
	return status

# to convert a node into a set fo integers
def set_conversion(A):
	i = j = 0
	for iter1 in A:
		for iter2 in iter1:
			j+=iter2*(10**i)
			i+=1
	return j

# initializing the goal node
goal_node = np.array([[1,2,3],[4,5,6],[7,8,0]])

#initializing node lise
node_list = []
node_set = set([])

#to get the input from the user
parser = argparse.ArgumentParser()

parser.add_argument('Initial_node')

args = parser.parse_args()

initial_node = read(args.Initial_node)

node_list.append(initial_node)
node_set.add(set_conversion(initial_node))


child_index = []
child_index.append(0)
temp_index = []
count = 0
child_node_number = 0

node_info = []
found = False


while len(child_index)>0:

	temp_index = []
	for i in child_index:

		new_node, status = up(node_list[i])
		if status == True and not isRepeated_set(new_node,node_set):
			child_node_number += 1
			temp_index.append(child_node_number)
			node_list.append(new_node)
			temp_node_info = np.array([child_node_number,i,0])
			node_info.append(temp_node_info)
			node_set.add(set_conversion(new_node))

			if goal_check(new_node,goal_node):
				found = True
				goal_index = child_node_number
				break

		new_node, status = down(node_list[i])
		if status == True and not isRepeated_set(new_node,node_set):
			child_node_number += 1
			node_list.append(new_node)
			temp_node_info = np.array([child_node_number,i,0])
			node_info.append(temp_node_info)
			temp_index.append(child_node_number)
			node_set.add(set_conversion(new_node))
			if goal_check(new_node,goal_node):
				found = True
				goal_index = child_node_number
				break

		new_node, status = right(node_list[i])
		if status == True and not isRepeated_set(new_node,node_set):
			child_node_number += 1
			node_list.append(new_node)
			temp_node_info = np.array([child_node_number,i,0])
			node_info.append(temp_node_info)
			temp_index.append(child_node_number)
			node_set.add(set_conversion(new_node))
			if goal_check(new_node,goal_node):
				found = True
				goal_index = child_node_number
				break

		new_node, status = left(node_list[i])
		if status == True and not isRepeated_set(new_node,node_set):
			child_node_number += 1
			node_list.append(new_node)
			temp_node_info = np.array([child_node_number,i,0])
			node_info.append(temp_node_info)
			temp_index.append(child_node_number)
			node_set.add(set_conversion(new_node))
			if goal_check(new_node,goal_node):
				found = True
				goal_index = child_node_number
				break
	if found == True:
		# finding the node path to reach the goal node
		node_path = []
		gl_temp = goal_index-1
		node_path.append(node_list[goal_index])
		print(node_path)

		while gl_temp>0:
			x = node_info[gl_temp]
			gl_temp = x[1]
			node_path.append(node_list[gl_temp])
		print('goal reached',found)
		node_path.reverse()


		node_path_t = np.asarray(node_path)
		#print(node_path_t)

		with open('nodes_path.txt', 'w') as node_path_file:
			for i in node_path_t:
				t = np.empty([1,9])
				count = 0
				for j in i.T:
					for k in j:
						t[0,count] = k
						count+=1
				np.savetxt(node_path_file,t,delimiter='\t')
		break

	child_index = temp_index
	count+=1

node_info_t = np.asarray(node_info)

#writing the output to the file
with open('nodes_info.txt', 'w') as node_info_file:
	for i in node_info_t:
		t = np.empty([1,3])
		t[0,:]=i
		np.savetxt(node_info_file,t,delimiter='\t')

node_list_t = np.asarray(node_list)

#writing the output to the file
with open('nodes_list.txt', 'w') as node_list_file:
	for i in node_list_t:
		t = np.empty([1,9])
		count = 0
		for j in i.T:
			for k in j:
				t[0,count] = k
				count+=1
		np.savetxt(node_list_file,t,delimiter='\t')

# If the goal node is not reached
if found==False:
	print('goal node cannot be reached')
