from flask import Flask , render_template, url_for, request, redirect
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize

app = Flask(__name__)

@app.route('/')
def index():	
	return render_template('index.html')


@app.route('/getsentiment', methods=['POST'])
def getsentimentofsen():
	sentence = request.form['content']
	pos_list = {'know','aware'} #,'do','does','did'
	neg_list = {'decline'}
	stop_word = set(stopwords.words('english')) - {"not","n't"} #,"do","does","did"
	newStopWords = {'if','whether','however'}     #THINKING TO ADD WORDS LIKE BOOK OR ANSWER WHICH ARE NEUTRAL WORDS
	stop_words = stop_word.union(newStopWords)
	
	word_tokens = word_tokenize(sentence) 
	filtered_sentence = ""
	for w in word_tokens: 
		if w not in stop_words: 
			filtered_sentence = filtered_sentence +" " + w    
    #This function tells the percent of positive sentences in a para
	sid_obj = SentimentIntensityAnalyzer() 
	pos_count=0
	neg_count=0
	temp=sent_tokenize(filtered_sentence)
	for sen in temp: 
		sentiment_dict = sid_obj.polarity_scores(sen)
		if sentiment_dict['compound'] >= 0.05 :
			pos_count = pos_count + 1
		elif sentiment_dict['compound'] <= - 0.05 :
			neg_count = neg_count + 1
		else :  #This part will execute when vaderSentiment will give neutral i.e. 0.05 value. This part will cross check the value
			word_tokens = word_tokenize(sen)
		for w in word_tokens:
			if w in pos_list:
				if "n't" in sen or "not" in sen:
					neg_count = neg_count+1 
					break
			if w in neg_list:
				if "not" in sen or "not" in sen:
					pos_count=pos_count+1
					break
	print((pos_count-neg_count)*100/(pos_count+neg_count))				
	if (pos_count-neg_count)*100/(pos_count+neg_count) > 50:
		return "Positive"
	else:
		return "Negative"	


if __name__ == '__main__':
    app.run(debug=True)    