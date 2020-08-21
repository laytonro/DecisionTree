#Layton Rosenfeld


#things to do:
#2) Test - make it return an error if the value does not exist
#3) other tests
#4) write paragraph


import math
from collections import Counter
import random

class Example:
    def __init__(self, category, dictionary):
        self.category = category
        self.dictionary = dictionary
        
class Node:
    def __init__(self, name):
        self.name = name
        self.childDict = {}

setOfCategories = []

def main(filename, percentLearning):
    input_file = open(filename, "r")
    headers = input_file.readline().strip().split(",")
    attributes = []
    attributes = headers[1:]
    examples = []
    for line in input_file:
        line = line.strip().split(",")
        examples.append(line)
    
    numLearn = int(len(examples) * (percentLearning/100))
    random.shuffle(examples)
    global setOfCategories
    setOfCategories = set([x[0] for x in examples])



        
#each example is class, that has a category and dictionary
#make dictionary for each example and has a key is the header-value(weather,wind,..etc) and the value is the actual value for that example

        
    listOfExampleObjectsL = []
    listOfExampleObjectsT = []
    count = 0
    for example in examples:
        category = example[0]
        dictionary = {}
        for num in range(1, len(headers)):
            dictionary[headers[num]] = example[num]            
        if count < numLearn:
            listOfExampleObjectsL.append(Example(category, dictionary))
        else:
            listOfExampleObjectsT.append(Example(category, dictionary))
        count += 1

            
       
    root = id3(listOfExampleObjectsL, attributes)
    printTree(root)
    print("total number of examples: "+ str(len(examples)))
    print("number of training examples: " + str(len(listOfExampleObjectsL)))
    print("number of testing examples: " + str(len(listOfExampleObjectsT)))
    if len(listOfExampleObjectsT) == 0:
        test(listOfExampleObjectsL, root)
    else:
        test(listOfExampleObjectsT, root)
        
#calculate the entropy for a passed through of data
# loop through categories, count how many have that category
def entropy(exList):
    entropy = 0
    for cat in setOfCategories:
        counter = 0
        for x in exList:
            if x.category == cat:
                counter += 1
        freq = counter/len(exList)
        if freq != 0:
            entropy -= (freq * math.log(freq,2))
    return entropy
        


def gain(S,A):
    gain = entropy(S)
    setOfValues = set([x.dictionary.get(A) for x in S])
    for value in setOfValues:
        listt = []
        for x in S:
            if x.dictionary.get(A) == value:
                listt.append(x)
        gain -= (len(listt)/len(S) * entropy(listt))
                    
    return gain


head = None 
empty = True
def id3(exList, aList):
   
    #find frequency of categories
    exCats = []
    for x in exList:
        exCats.append(x.category)
    catFreqs = Counter(exCats)
    
       
    if len(catFreqs) == 1:
        return Node(catFreqs.most_common(1)[0][0])
    if len(aList) == 0:
        return Node(catFreqs.most_common(1)[0][0])
    
    #finding which a to seperate with
    greatestGain = 0
    greatestA = None
    for a in aList:
        g = gain(exList, a)
        if g >= greatestGain:
            greatestGain = g
            greatestA = a
    newNode = Node(greatestA)
    setOfValues = set([x.dictionary.get(greatestA) for x in exList])
    aList.remove(greatestA)
    
    
    for value in setOfValues:
        newExList = []
        
        for x in exList :
            if x.dictionary.get(greatestA) == value:
                newExList.append(x)
        if len(newExList) == 0:
            newNode.name = catFreqs.most_common(1)[0][0]
            return newNode
        newNode.childDict[value] = id3(newExList, aList)
    return newNode
 

def printTree(node, level = 0):
    if len(node.childDict) == 0:
        print("     " * level + node.name)
    else:
        print("     " * level + node.name + "?")
    for childKey in node.childDict:
        print(("     " * (level + 1)) + childKey + ":")
        printTree(node.childDict[childKey], level+2)
  
  
#start at root and go through until the node is a category (with no children)
  #then see if mynode.category == node.category, add to counter to compute accuracy
def test(exList, root):
    correct = 0
    for x in exList:
       if testNode(x, root) == True:
            correct +=1
    print("% correct = " + str((correct/len(exList))*100))
        

   
def testNode(ex, node):
    if ex.dictionary[node.name] not in node.childDict:
        #print("ERROR: value not in tree: " + ex.dictionary[node.name])
        return False
    node = node.childDict[ex.dictionary[node.name]]
    if len(node.childDict) == 0:
        if node.name == ex.category:
            return True
        else:
            return False
    return testNode(ex, node)
    
    
        
        
        
#main("tennis.txt", 100)
#main("mushrooms.txt", 5)

#main("congress84.txt", 40)
main("primary-tumor.txt", 80)

