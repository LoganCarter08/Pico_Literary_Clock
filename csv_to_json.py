import json 

class Quote:
    def __init__(self, line: str):
        splitted = line.split("|")
        self.time = splitted[0]
        self.highlight = splitted[1] 
        self.fullQuote = splitted[2].replace("<br/>", "<br>")
        self.book = splitted[3] 
        self.author = splitted[4]
    
    def toDict(self) -> dict:
        return {
            "highlight": self.highlight, 
            "fullQuote": self.fullQuote, 
            "book": self.book, 
            "author": self.author 
        }

quotes = {}

def dumpToFile(fileName: str, prettyJson):
    tempFileName = fileName.replace(":", "_")
    with open('circuit_python_files/lib/quotes/' + tempFileName + '.json', 'w') as json_file:
        prettyJson = json.dumps(timeQuotes)
        json_file.write(prettyJson)

with open('litclock_annotated.csv', 'r', encoding='utf-8') as file:
    timeQuote = ""
    timeQuotes = []
    for line in file:   
        newQuote = Quote(line)
        if newQuote.time != timeQuote: 
            if timeQuote != "": 
                #quotes[timeQuote] = timeQuotes 
                splitQuote = timeQuote.split(":")
                if (int(splitQuote[1]) + 1) % 60 != int(newQuote.time.split(":")[1]):
                    print("Missing: ", splitQuote[0], ":", int(splitQuote[1]) + 1)
                dumpToFile(timeQuote, timeQuotes)
                timeQuotes = [] 
            timeQuote = newQuote.time 
        timeQuotes.append(newQuote.toDict()) 
    #quotes[timeQuote] = timeQuotes 
    dumpToFile(timeQuote, timeQuotes)
