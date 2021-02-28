#coding:utf8
import itertools
import re
from collections import defaultdict

found_results = []

class CkyParser:
    def __init__(self, sentence):
        self.sentence = sentence
        self.rules = self.find_rules()
        self.table = self.create_table()
        self.print_matrix()
        self.print_result()
        
    def find_rules(self):
        lines = []
        with open("rules.gr", "r", encoding="utf8") as file:
            for line in file.readlines():
                lines.append(line.replace("\n", ""))
        rules = defaultdict(lambda: [])
        for line in lines:
            if line == "\r" or line == '' or line[0] == '#':
                continue

            matches = re.match(r'([^\s]+)\s+([^\s]+)(?:\s+([^\s]+))?', line)
            if matches:
                terminal = False if matches.group(3) else True
                left = matches.group(1)
    
                if terminal:
                    right = matches.group(2)
                else:
                    right = (matches.group(2), matches.group(3))
            
            rules[left].append(right)
        return rules
    
    # return Past_Adverb when word is 'dün'
    def find_matches(self, word, right1, right2):
        matches = []
        
        def search_rules(right):
            for left in self.rules:
                for rule in self.rules[left]:
                    if rule == (word or non_terminal):
                        matches.append(left)
        if word:
            search_rules(word)
        else:
            for non_terminal in itertools.product(right1, right2):
                search_rules(non_terminal)
        return matches
    
    def create_table(self):
        words = self.sentence.split()
        table = []
        for x in range(len(words)):
            table.append([])
            for y in range(len(words)):
                table[x].append([])
        for column in range(len(words)):
            table[column][column] = self.find_matches(words[column], None, None)
            for row in reversed(range(column + 1)):
                for s in range(row + 1, column + 1):
                    table[row][column].extend(self.find_matches(None, table[row][s - 1], table[s][column]))
        return table
    
    def print_result(self):
        print(self.sentence)
        if (len([p for p in self.table[0][len(self.table) - 1] if p == 'MAIN'])) > 0:
            found_results.append(1)
            print("CORRECT")
        else:
            found_results.append(0)
            print("NOT CORRECT")
            
    def print_matrix(self):
        print()
        for row in range(len(self.table)):
            for col in range(row, len(self.table)):
                print(self.table[row][col], end="")
            print()

sentences = ['dün arkadaş ım a hediye al dı m .',
             'arkadaş ım a hediye al dı m .',
             'dün hediye al dı m .',
             'yarın arkadaş ım a hediye al acak ım .',
             'tarihi roman lar ı keyifle oku yor um .',
             'tarihi roman lar ı oku yor um .',
             'roman lar ı keyifle oku yor um .',
             'roman ı keyifle oku yor um .',
             'sen arkadaş ım a hediye al dı n .',
             'tarihi roman lar oku du m .',
             'dün arkadaş ım a hediye al acak ım .',
             'roman ı tarihi keyifle oku yor um .',
             'ben arkadaş ım a hediye al dı n .',
             'tarihi bir roman lar oku du m .',
             'ben arkadaş ım a hediye al dı k .',
             'ben arkadaş ım a hediye al dı m .',
             'yarın baba m a yardımet ecek im .',
             'dün baba m a yardımet ecek im .',
             'ben okul a git ti m .',
             'sen okul a nezaman gel di n ?',
             'güzel karpuz meyve dir .']

true_results = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1]
for sentence in sentences:
        ckyParser = CkyParser(sentence)
        
correct_found = 0
for i in range(len(sentences)):
    if found_results[i] == true_results[i]:
        correct_found += 1
print()
print("Accuracy: ", correct_found * 100 / len(sentences), " - Total: ", len(sentences), " - Correctly Found: ", correct_found)  
