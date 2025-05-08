#!/usr/bin/python3
def group_anagrams(words):
    anagram_dict = {}
    for word in words:
        sorted_word = ''.join(sorted(word))
        if sorted_word in anagram_dict:
            anagram_dict[sorted_word].append(word)
        else:
            anagram_dict[sorted_word] = [word]
    return list(anagram_dict.values())
 
 
words = ['lump', 'eat',  'me',  'tea', 'em', 'plum']
print(group_anagrams(words))

str = "string"
res = sorted(str)
print(res)