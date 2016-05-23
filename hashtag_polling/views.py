import os
import pdb

from django.shortcuts import render
from django.template import loader, Context
from django.http import HttpResponse
from django.template.context_processors import csrf
from .forms import DateForm
from TwitterAPI import TwitterAPI, TwitterRestPager
from datetime import datetime

api = TwitterAPI(
  os.environ['consumer_key'],
  os.environ['consumer_secret'],
  os.environ['access_token_key'],
  os.environ['access_token_secret']
)

# Create your views here.

def index(request):
  return render(request, 'index.html', {})


def search(request):
  # form = DateForm(request.GET)

  query = request.GET['q']
  date = request.GET['date']
  formatted_date = datetime.strptime(date, '%m/%d/%Y').strftime('%Y-%m-%d')

  # json_string = api.request('search/tweets', {'q': '%23' + query + ' since:2016-05-11'})
  # decoded_json = json_string.json()

  r = TwitterRestPager(api, 'search/tweets', {'q': '%23' + query + ' since:' + formatted_date, 'count': 100})
  maxRT = 0
  tweet = {}
  count = 0
  for item in r.get_iterator(wait=2):
    print(item['text'])

    if 'text' in item:
      if item['retweet_count'] > maxRT:
        tweet = {'text': item['text'], 'rt_count': item['retweet_count']}
      count += 1
    elif 'message' in item and item['code'] == 88:
      print('SUSPEND, RATE LIMIT EXCEEDED: %s' % item['message'])
      break

  print(count)

  # pdb.set_trace()
  #
  #
  # for item in decoded_json['statuses']:
  #   print(item['text'])
  # c = Context({'results': decoded_json['statuses']})


  t = loader.get_template('results.html')
  c = Context({'count': count, 'tweet': tweet})
  return HttpResponse(t.render(c))

