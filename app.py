#library imports
import os

#Flask imports
from flask import Flask, request
from flask.ext.restful import Api, Resource, reqparse
import json

# import neural net and constuct
from neural_net import NeuralNet

mongo = [{
      "id":"4353245325",
      "url":"./data/260115175012.json",
      "name":"Tom's experiment"
    },{
      "id":"4353245425",
      "url":"./data/271015175012.json",
      "name":"Sam's experiment"
    }]

# this is for a single instance get
class NeuralResource(Resource):

  # in response to the get request calls this function
  def get(self,timedate):
    "Get results from a particular neural network"
    print(timedate)
    # tries to get the result from neuralNet class in neural_net
    # passing in the timedate ID!!
    url = None
    for m in mongo:
      if(m['id'] == timedate):
        url = m['url']
        break

    if url == None:
      return {'data':'FAIL'}

    data = None
    with open(url) as data_file:    
        data = json.load(data_file)

    try:
      # result = neuralNet.result(timedate)
      result = {'data':data}
    except Exception as error:
      return str(error), 500

    return result

# this is for a multiple instance get
class NeuralResources(Resource):

  # in response to the post request to run a new neural net
  def post(self):
    "Run a new neural network"

    # this gets the data passed in the post request?
    data = request.get_json()
    
    # then tries to run the neural net!
    try:
      timedate = neuralNet.run(data)
    except Exception as error:
      return str(error), 500

    # then in response, returns the timedate ID used reference the object ??
    return timedate

  # gets the list of neural networks from somewhere, needs to be populated from another file.
  def get(self):
    "Return a list of neural networks"

    # return ['one','two']
    return mongo

# creates an instance of the Neural Net class?
neuralNet = NeuralNet()

#Find static path from relative path
currentPath = os.getcwd()
basePath = os.path.split(currentPath)[0]
staticPath = os.path.join(basePath,'SamProject-master','client')
print(staticPath)

#Define static folder path
app = Flask(__name__, static_folder=staticPath, static_url_path='')
api = Api(app)

# this is the route for the index page (need to make more)
@app.route('/')
def index():
  "Index file to run the front end components through angular JS"

  print(os.getcwd(),staticPath)
  return app.send_static_file('views/index.html')

@app.route('/epoch')
def epoch():
  return app.send_static_file('views/epoch.html')

@app.route('/meta')
def meta():
  return app.send_static_file('views/meta.html')

@app.route('/layer')
def layer():
  return app.send_static_file('views/layer.html')


# this is what we're running - sets up the server 
if __name__ == '__main__':

  # Add api resources (sets up the routes for the data stuff)
  api.add_resource(NeuralResource, '/results/<string:timedate>')
  api.add_resource(NeuralResources, '/results')

  #Run Server on port 0.0.0.0
  app.run(host='0.0.0.0', port=8000, debug=True)