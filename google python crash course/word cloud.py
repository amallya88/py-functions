import wordcloud
import numpy as np
from matplotlib import pyplot as plt
import io
import sys


myFile = open("Clinton 1993 Inaugural Address.txt", 'r')
file_contents = myFile.read()


def calculate_frequencies(file_contents):
    # Here is a list of punctuations and uninteresting words you can use to process your text
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    uninteresting_words = ["the", "a", "to", "if", "is", "it", "of", "and", "or", "an", "as", "i", "me", "my", \
    "we", "our", "ours", "you", "your", "yours", "he", "she", "him", "his", "her", "hers", "its", "they", "them", \
    "their", "what", "which", "who", "whom", "this", "that", "am", "are", "was", "were", "be", "been", "being", \
    "have", "has", "had", "do", "does", "did", "but", "at", "by", "with", "from", "here", "when", "where", "how", \
    "all", "any", "both", "each", "few", "more", "some", "such", "no", "nor", "too", "very", "can", "will", "just", \
    "in", "for", "so", "would", "applause", "those", "these", "because", "than", "therefore"]
    
    # LEARNER CODE START HERE
    word_freq = {}
    file_contents = file_contents.lower()
    
    for word in file_contents.split():
        word = word.strip(punctuations)
        if word not in uninteresting_words and len(word) > 3:
            if(word not in word_freq):
                word_freq[word] = 0
            word_freq[word] += 1
                    
    #wordcloud
    cloud = wordcloud.WordCloud()
    cloud.generate_from_frequencies(word_freq)
    return cloud.to_array()


myimage = calculate_frequencies(file_contents)
plt.imshow(myimage, interpolation = 'nearest')
plt.axis('off')
plt.show()

