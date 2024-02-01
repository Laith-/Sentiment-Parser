import os.path

def main():
    running = True
    while running:
        option = mainMenu()
        menuChoice(option)
    
def mainMenu():
    print('Select an option:')
    print('  1. Clean a file')
    print('  2. Display file statistics')
    print('  3. Quit')
    choice = input('> ')
    error = True
    
    while not choice.isdigit():
        print('Invalid choice. Please try again.')
        choice = input('> ')
    if 1 <= int(choice) <= 3:
        return int(choice)
    else:
        while error:
            print('Invalid choice. Please try again.')
            choice = input('> ')
            while not choice.isdigit():
                print('Invalid choice. Please try again.')
                choice = input('> ')            
            
            if 1 <= int(choice) <= 3:
                error = False
                return int(choice)         
    
    
def menuChoice(option):
    if option == 1:
        file = getFile()
        cleanFile(file)
    
    if option == 2:
        clean = checkClean()
        calcSentiment(clean)
    
    if option == 3:
        print('Goodbye.')
        quit()
        
def getFile():
    file = input('Enter a filename > ').lower()
    
    error = True
    if file.endswith('.txt'):
        if os.path.exists(file):
            return file
        else:
            error = True
        
    else:
        while error:
            print('Invalid file name. Please try again.')
            file = input('Enter a filename > ')
            if file.endswith('.txt'):
                error = False
                if os.path.exists(file):
                    return file 
                else:
                    error = True

def openFile(path):
    file = open(path)
    content = list(file.read().strip().lower())
    return content

def replaceChar(content):
    for letter in content:
        if letter == '-':
            letter = ' '
        if letter == "'":
            letter = ' '
    return content

def parseTokens(content):
    parse_list = ''.join(content).split()
    return parse_list

def parsePunctuation(content):
    list_of_punctuation = ['.','!','?']
    list_sentence = []
    sentences = []
    for word in content:
        if word[len(word)-1] not in list_of_punctuation:
            list_sentence.append(word)
        else:
            list_sentence.append(word)
            sentences.append(''.join(list_sentence))
            list_sentence = []
            
    cleaned_file = open(file_name[:-4] + '_clean.txt')   
    cleaned_file.write(''.join(file_List)) 
    cleaned_file.close() 
    
    print('New file,', file_name[:-4] + '_clean.txt', 'has been created.')

def checkClean():
    file = input('Enter a filename > ').lower()
    
    error = True
    if os.path.exists(file):
        clean_path = str(os.path.splitext(file)[0]) + '_clean.txt'
        if os.path.exists(clean_path):
            error = False
            return clean_path
        else:
            print('You need to create the cleaned version of', file, 'first.')
    else:
        while error:
            print('Invalid file name. Please try again.')
            file = input('Enter a filename > ')
            if os.path.exists(file):
                clean_path = str(os.path.splitext(file)[0]) + '_clean.txt'
                if os.path.exists(clean_path):
                    error = False
                    return clean_path 
                else:
                    error = False
                    print('You need to create the cleaned version of', file, 'first.')                
    
def importPolarities():
    polarities = {}
    
    import_polarities = open('word_polarities.txt').readlines()
    for line in range(len(import_polarities)):
        import_polarities[line] = import_polarities[line].strip().lower()
    
    for polarity in import_polarities:
        split = polarity.split(',')
        polarities[str(split[0])] = int(split[1])
    return polarities
    
def calcSentiment(path):
    polarities = importPolarities()
    content = open(path).readlines()
    for line in range(len(content)):
        content[line] = content[line].strip().lower()
        
    pos_word = 0
    neg_word = 0
    ntrl_word = 0
    unkn_word = 0

    pos_sen = 0
    neg_sen = 0
    ntrl_sen = 0
        
    for line in content:
        line = line.split()
        for word in line:
            if word in polarities:
                polarity = polarities.get(str(word))
                if polarity == 1:
                    pos_word += polarity
                elif polarity == -1:
                    neg_word += polarity
                elif polarity == 0:
                    ntrl_word += polarity
            else:
                unkn_word += 1

            tally = pos_word + neg_word
            
        if tally > 0:
            pos_sen += 1
        elif tally < 0:
            neg_sen += -1
        else:
            ntrl_sen += 1
    
        pos_word = 0
        neg_word = 0
        ntrl_word = 0
    
    tally = pos_sen + neg_sen + ntrl_sen

    if ntrl_sen > tally:
        sentiment = 'NEUTRAL'
    if tally > 0:
        sentiment = 'POSITIVE'
    if tally < 0:
        sentiment = 'NEGATIVE'
    
    words = {}
    
    for line in content:
        line = line.split()
        for word in line:
            if word not in words:
                words[str(word)] = 1
            else:
                add = words.get(str(word))
                words[str(word)] = int(words[str(word)] + int(add))
                add = 0
            
            
    # this statement returns a list of keys in the dictionary, sorted by their
    # values. In this case, keys are letters and values are occurrences.
    sorted_words = sorted(words, key=lambda letter:words[letter])
    
    # the returned list is sorted from lowest to highest. You can make it highest
    # to lowest by calling the list's reverse method.
    sorted_words.reverse()
    
    if len(sorted_words) < 15:
        top15 = ['','','','','','','','','','','','','','','']
        for i in range(len(sorted_words)):
            pass
            
    else:
        top15 = sorted_words
        
    
    old_path = str(path[:-10])+'.txt'
    
    print('+-----------------------------------------------------------------------------+')
    print('| Filename           :'+old_path.ljust(56)+'|')
    print('| Positive Sentences :'+str(pos_sen).ljust(56)+'|')
    print('| Negative Sentences :'+str(neg_word).ljust(56)+'|')
    print('| Neutral Sentences  :'+str(ntrl_word).ljust(56)+'|')
    print('| Unknown Sentences  :'+''.ljust(56)+'|')
    print('| Overall Sentiment  :'+sentiment.ljust(56)+'|')
    print('+-----------------------------------------------------------------------------+')
    print('| 15 Most Used Words                                                          |')
    print('+-----------------------------------------------------------------------------+')
    print('|                         |                         |                         |')
    print('|                         |                         |                         |')
    print('|                         |                         |                         |')
    print('|                         |                         |                         |')
    print('|                         |                         |                         |')
    print('+-----------------------------------------------------------------------------+')
    
main()
