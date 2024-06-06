#!/usr/bin/env python3
""" brute-force check that any combinations of BBWT and rotation 
generates all strings having the same Parikh vector """
# pylint: disable=bad-indentation,line-too-long,invalid-name

import itertools
import argparse
import typing
import collections
import math

import bwt

def left_rotate(text):
	""" rotate a string to the left """
	return text[1:] + text[0]

def all_rotations(text):
	""" return all rotations of a string """
	return [text[i:] + text[:i] for i in range(len(text))]


parser = argparse.ArgumentParser(description='brute-force check that any combinations of BBWT and rotation generates all strings having the same Parikh vector')
parser.add_argument('--alphabetsize', '-a', required=False, type=int, nargs='?', help='number of distinct characters', default=2)
parser.add_argument('--length', '-l', required=False, type=int, help='length of the texts to valiate', default=3)
args = parser.parse_args()

def gen_lyndon_words(max_char : int, max_length : int):
	"""Lyndon.py Algorithms on strings and sequences based on Lyndon words. David Eppstein, October 2011.
	Generate nonempty Lyndon words of length <= max_length over an max_char-symbol alphabet.
		The words are generated in lexicographic order, using an algorithm from
		J.-P. Duval, Theor. Comput. Sci. 1988, doi:10.1016/0304-3975(88)90113-2.
		As shown by Berstel and Pocchiola, it takes constant average time
		per generated word."""
	w = [-1]                            # set up for first increment
	while w:
		w[-1] += 1                      # increment the last non-z symbol
		yield w
		m = len(w)
		while len(w) < max_length:               # repeat word to fill exactly max_length syms
			w.append(w[-m])
		while w and w[-1] == max_char - 1:     # delete trailing z's
			w.pop()

def intvec2str(vec : typing.List[int]) -> str:
	""" convert a list of integers to a string """
	return ''.join(map(lambda x : chr(ord('a')+x), vec))


def num_strings_with_parikh(parikh) -> int:
	""" return the number of strings having the same Parikh vector """
	length = sum(parikh.values())
	numerator = math.factorial(length)
	denominator = 1
	for value in parikh.values():
		denominator *= math.factorial(value)
	assert numerator % denominator == 0, f"numerator {numerator} is not divisible by denominator {denominator}"
	return numerator // denominator

def get_missing(accessed):
	""" return the missing strings  """
	l = []
	first_el = next(iter(accessed))
	targetstrings = set(itertools.permutations(first_el))
	for arr in targetstrings:
		s = ''.join(arr)
		if s not in accessed:
			l.append(s)
	return l

def run_computation():
	""" run the computation """
	for lyndonvec in gen_lyndon_words(args.alphabetsize, args.length):
		lyndonword = intvec2str(lyndonvec)
		parikh = collections.Counter(lyndonword)
		count = num_strings_with_parikh(parikh)
		stack = all_rotations(lyndonword)
		accessed = set()
		while len(stack) > 0:
			current_node = stack.pop()
			accessed.add(current_node)
			bbwt = bwt.bijective_bwt(current_node)
			if bbwt not in accessed:
				stack.append(bbwt)
				for rotation in all_rotations(bbwt):
					if rotation not in accessed:
						stack.append(rotation)
		assert len(accessed) == count, f"have {len(accessed)} strings, expected {count} strings for {lyndonword}: missing {get_missing(accessed)}"


if __name__ == '__main__':
	run_computation()
	print("done for all Lyndon words of length", args.length, "over an alphabet of size", args.alphabetsize, "characters")
