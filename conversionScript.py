file_ = open('common_words_source.txt')
lines = file_.readlines()
lines = [x.split(' ') for x in lines]
nouns = [word[1] for word in lines if word[2] == 'n']
adjectives = [word[1] for word in lines if word[2] == 'j']
verbs = [word[1] for word in lines if word[2] == 'v']
for i in range(0, len(verbs)):
	verb = verbs[i]
	if verbs[i].endswith('e') and verbs[i][-2] != 'e':
		verb = verbs[i][:-1]
	verb += 'ing'
	verbs[i] = verb
nounFile = open('wordLists/objects.list', 'w')
nounString = '\n'.join(nouns)
nounFile.write(nounString)
nounFile.close()
adjectiveFile = open('wordLists/adjectives.list', 'w')
adjectveString = '\n'.join(adjectives)
adjectiveFile.write(adjectveString)
adjectiveFile.close()
verbFile = open('wordLists/actions.list', 'w')
verbString = '\n'.join(verbs)
verbFile.write(verbString)
verbFile.close()