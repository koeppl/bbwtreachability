#!/usr/bin/env python3
""" abook replacement """
# pylint: disable=bad-indentation,line-too-long,invalid-name

import argparse
import bwt

def path(start : str, end: str, use_inverse : bool) -> str:
	""" return the path as a string, where b is for BBWT, i for inverse BBWT, and the number x for the x-th left rotation """
	paths = {start : [] }
	stack = [start]

	def update_stack(text : str, pathlabel : str):
		if text not in paths:
			paths[text] = paths[curnode] + [pathlabel]
			stack.append(text)
		elif len(paths[text]) > len(paths[curnode])+1:
			paths[text] = paths[curnode] + [pathlabel]


	while len(stack) > 0:
		curnode = stack.pop()
		for i in reversed(range(len(curnode))):
		#for i in range(len(curnode)):
			update_stack(curnode[i:] + curnode[:i], str(i))
		if use_inverse:
			update_stack(bwt.bijective_bwt_inv(curnode), 'i')
		update_stack(bwt.bijective_bwt(curnode), 'b')
		stack.sort(key = lambda x : len(paths[x]), reverse=True)
		# print(list(map(lambda x : len(paths[x]), stack)))
	if end in paths:
		return ''.join(paths[end])
	return "unreachable"

parser = argparse.ArgumentParser(description='outputs the path as a string, where b is for BBWT, i for inverse BBWT, and the number x for the x-th left rotation')
parser.add_argument('--start', '-s', required=True, type=str, nargs='?', help='string from we start', default=2)
parser.add_argument('--target', '-t', required=True, type=str, help='string where we want to go', default=3)
parser.add_argument('--use_inverse', '-i', action='store_true', required=False, help='do you also want to consider the inverse?', default=False)
args = parser.parse_args()

print(path(args.start, args.target, args.use_inverse))
