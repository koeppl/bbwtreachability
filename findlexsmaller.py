#!/usr/bin/env python3
""" find shortest path to next smaller word"""
# pylint: disable=bad-indentation,line-too-long,invalid-name

import argparse
import sys
import typing

import bwt

def path(start : str) -> typing.Tuple[str,str]:
	""" find shortest path to next smaller word"""
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
		for i in range(len(curnode)):
			update_stack(curnode[i:] + curnode[:i], str(i))
		update_stack(bwt.bijective_bwt(curnode), 'b')
		update_stack(bwt.bijective_bwt_inv(curnode), 'i')
		stack.sort(key = lambda x : len(paths[x]), reverse=True)
		# print(list(map(lambda x : len(paths[x]), stack)))
		if curnode < start:
			return (curnode, ''.join(paths[curnode]))
	return ("unreachable",'')


def compute_path(inputstring : str):
	""" find shortest path to next smaller word"""
	(to, tolabel) = path(inputstring)
	smallest_path_lenth = len(tolabel)
	if smallest_path_lenth == 0:
		print(to)
		sys.exit(0)
	print(f"first path found: from={inputstring} to={to} label={''.join(tolabel)}")

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='find shortest path to next smaller word')
	parser.add_argument('--start', '-s', required=True, type=str, help='string from we start')
	args = parser.parse_args()
	compute_path(args.start)
