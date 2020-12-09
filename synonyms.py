'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 14, 2016.
'''

import math


def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''
    
    sum_of_squares = 0.0  
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    
    return math.sqrt(sum_of_squares)

'''
def cosine_similarity(vec1, vec2):
    dot  = -1

    for key in vec1:
        if key in vec2:
            dot+= vec1[key]*vec2[key]
    if(dot == -1):
        return -1
    else:
        return ((dot+1)/(norm(vec1)*norm(vec2)))
'''
def cosine_similarity(vec1, vec2):
    dot  = 0

    for key in vec1:
        if key in vec2:
            dot+= vec1[key]*vec2[key]

    return ((dot)/(norm(vec1)*norm(vec2)))
      
#print(cosine_similarity({"a": 1, "b": 2, "c": 3}, {"b": 4, "c": 5, "d": 6}))

def build_semantic_descriptors(sentences):
    d = {}
    for i in range(len(sentences)):
        prev = set()
        #prev.update("")
        for j in range(len(sentences[i])):
            currword = sentences[i][j]  # CHeck if currword is in prev before proceeding!
            if currword not in prev:
                if(j == 0):
                    prev.add(currword)
                else:

                    for elem in prev:
                        #print(prev)
                        #print(elem)
                        if elem in d:
                            #d[elem] +=1
                            if currword in d[elem]:
                                d[elem][currword] += 1
                            else:
                                d[elem][currword] = 1
                        else:
                            d[elem] = {currword : 1}
                        if currword in d:
                            if elem in d[currword]:
                                d[currword][elem] += 1
                            else:
                                d[currword][elem] = 1
                        else:
                            d[currword] = {elem: 1}
                    prev.add(currword)
    return d



#print(build_semantic_descriptors(sentences))
def build_semantic_descriptors_from_files(filenames):
    sentences = []
    for i in range(len(filenames)): 
        r = open(filenames[i], "r", encoding="latin1")
        f = r.read().replace("\n", " ")
        #print(f) 
        f = f.lower()
        f = f.replace(",", "")
        f = f.replace(":", "")
        f = f.replace(";", "")
        f = f.replace("--", " ")
        f = f.replace("-"," ")
        f = f.replace("?", ".")
        f = f.replace("!", ".")
        temp = f.split(".")
        #print(temp)
        for j in range(len(temp)):
            #print(temp[j])
            temp[j] = temp[j].split()
            #print(temp[j])
        sentences.extend(temp)
        #sentences.pop(-1)
        r.close()
        #print(sentences)
    return build_semantic_descriptors(sentences)


#semantic_descriptors = build_semantic_descriptors_from_files(["book1.txt", "book2.txt"])


def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    maxdot = -2
    max_choice = ""

    for i in range(len(choices)):
        if (word in semantic_descriptors) and (choices[i] in semantic_descriptors):
            a = semantic_descriptors[word]
            b = semantic_descriptors[choices[i]]
            curdot = similarity_fn(a,b)
            if curdot > maxdot:
                maxdot = curdot
                max_choice = choices[i]
            
        else:
            curdot = -1
            if curdot > maxdot:
                maxdot = curdot
                max_choice = choices[i]
    return max_choice

def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    r = open(filename, "r", encoding="latin1")
    f = r.readlines()
    for i in range(len(f)):
        f[i] = f[i].split()
    correct = 0
    total = 0
    for j in range(len(f)):
        choices = f[j][2:]
        x = most_similar_word(f[j][0], choices, semantic_descriptors, similarity_fn)
        #print(x)
        if x == f[j][1]:
            correct += 1
        total+=1
    return correct/total * 100
        
#print(run_similarity_test("test.txt", semantic_descriptors, cosine_similarity))  

if __name__ == "__main__":
    sentences = [["i", "am", "a", "sick", "man"],
["i", "am", "a", "spiteful", "man"],
["i", "am", "an", "unattractive", "man"],
["i", "believe", "my", "liver", "is", "diseased"],
["however", "i", "know", "nothing", "at", "all", "about", "my",
"disease", "and", "do", "not", "know", "for", "certain", "what", "ails", "me"]]
    semantic_descriptors = build_semantic_descriptors_from_files(["book1.txt", "book2.txt"])
    #semantic_descriptors = build_semantic_descriptors_from_files(["sample_case.txt"])
    #print(semantic_descriptors)
    print(run_similarity_test("test.txt", semantic_descriptors, cosine_similarity))

    #derek = {'legislation': {'closer': 3, 'sector': 3, 'section': 1, 'onto': 1}, 'closer': {'legislation': 3, 'sector': 3}, 'sector': {'legislation': 3, 'closer': 3}, 'section': {'legislation': 1, 'onto': 1}, 'onto': {'section': 1, 'legislation': 1}, 'record': {'toe': 1}, 'toe': {'record': 1}}
    #print(run_similarity_test("sample_test.txt", semantic_descriptors, cosine_similarity))