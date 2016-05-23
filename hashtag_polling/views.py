import os
from django.shortcuts import render
from django.template import loader, Context
from django.http import HttpResponse
from TwitterAPI import TwitterAPI

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
  query = request.GET['q']
  t = loader.get_template('results.html')

  json_string = api.request('search/tweets', {'q': query, 'count': 4})
  decoded_json = json_string.json()

  for item in decoded_json['statuses']:
    print(item['text'])


  c = Context({'results': decoded_json['statuses']})
  return HttpResponse(t.render(c))

