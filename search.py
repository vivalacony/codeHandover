search.py
def omitted_words(search_input):
	deleteList = ['I', 'we', 'and', 'to', 'if', 'she', 'or', 'what', '&', ',', '?', ':', '@', 'or','"', '/', 'is',]
	
	for i in deleteList:
	 search_input = search_input.replace(i, "")
    
	return search_input
