import tweepy,webbrowser,sys
import keys
#from tweetutilities import print_tweets
from operator import itemgetter
from wordcloud import WordCloud

import matplotlib.pyplot as plt
import seaborn as sns

def topt_5 (dub_list,num=5):

	topt_5=  sorted(dub_list ,key = itemgetter('tweet_volume'),reverse=True)[:num]
	lst_1 =[(x['name'],x['tweet_volume']) for x in topt_5]
	lst_2 =[x['url'] for x in topt_5]
	return (lst_1,lst_2)

def wordcloud_trending_topics(dub_list):
	dct_trending = { trend['name'] : trend['tweet_volume'] for trend in dub_list}

	wordcloud = WordCloud(width= 1500,height=1500,prefer_horizontal=0.80,min_font_size=14
						,colormap = 'prism',background_color = 'white')
	wordcloud = wordcloud.fit_words(dct_trending)
	plt.imshow(wordcloud)
	return wordcloud

def connection(consumer_key,consumer_secret,access_token,access_token_secret):

	auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
	auth.set_access_token(access_token,access_token_secret)
	api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
	return api

if __name__ == '__main__':
	if sys.argv[1:]:
		consumer_key, consumer_secret, access_token, access_token_secret = sys.argv[1:]
	else:
		consumer_key = input('enter your consumer_key : ')
		consumer_secret = input('enter your consumer_secret : ')
		access_token = input('enter your access_token :  ')
		access_token_secret = input('enter your access_token_secret : ')
	try:
		if not consumer_key:
			consumer_key = keys.consumer_key
			consumer_secret = keys.consumer_secret
			access_token = keys.access_token
			access_token_secret = keys.access_token_secret
	except:
		print('please update keys.py')

	api = connection(consumer_key,consumer_secret,access_token,access_token_secret)
	idd = 0
	try:

		idd = int(input('enter the id of your place : '))
	except:
		print('enter valid id num')

	if  not idd:
		idd = 560743

	#idd = int(input('id of the trending place you are looking for : '))

	dub_trends = api.trends_place(id = idd)
	dub_list = dub_trends[0]['trends']
	dub_list = [t for t in dub_list if t['tweet_volume']]
	# dublin list contain a list of dictionary with the following keys: 'name'
	#url' 'promoted_content' 'query''tweet_volume'

	wordcloud = wordcloud_trending_topics(dub_list)
	plt.imshow(wordcloud)
	top_trend,urls = topt_5(dub_list)

	for link in urls:
		webbrowser.open(link)

	print(top_trend)
	img = wordcloud.to_file('trending_dub.png')




