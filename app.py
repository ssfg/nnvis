#library imports
import os
import sys
sys.path.insert(0, './Helpers')

from pymongo_store import*

#Flask imports
from flask import Flask, request
from flask.ext.restful import Api, Resource, reqparse
import json

# import neural net and constuct
from neural_net import NeuralNet

mongo = [{
      "id":"4353245325",
      "url":"./data/JSON/260115175012.json",
      "name":"Tom's experiment"
    },{
      "id":"4353245425",
      "url":"./data/JSON/271015175012.json",
      "name":"Sam's experiment"
    }]

# this is for a single instance get
class NeuralResource(Resource):

  # in response to the get request calls this function
  def get(self,_id):
    "Get results from a particular neural network"
    print(_id)

    dbClient = DatabaseClient()

    experimentOBJ = dbClient.get(_id)
    # print experimentOBJ

    # tries to get the result from neuralNet class in neural_net
    # passing in the ID ID!!
    # url = None
    # for m in mongo:
    #   if(m['id'] == ID):
    #     url = m['url']
    #     break

    # if url == None:
    #   return {'data':'FAIL'}

    # data = None
    # with open(url) as data_file:    
    #     data = json.load(data_file)

    # try:
    #   # result = neuralNet.result(ID)
    #   result = {'data': data}
    # except Exception as error:
    #   return str(error), 500

    return {'data': experimentOBJ}

# this is for a multiple instance get
class NeuralResources(Resource):

  # in response to the post request to run a new neural net
  def post(self):
    "Run a new neural network"

    # this gets the data passed in the post request?
    data = request.get_json()
    
    # then tries to run the neural net!
    try:
      print "DATA RESPONSE: "
      # result = neuralNet.run(data)
    except Exception as error:
      return str(error), 500

    # then in response, returns the result ID used reference the object ??
    # return result
    return {"data": data}

  # gets the list of neural networks from somewhere, needs to be populated from another file.
  def get(self):
    "Return a list of neural networks"

    dbClient = DatabaseClient()

    results = dbClient.query()
    # print results

    response = []

    for result in results:
      resultId = result['_id']
      resultHN = result['HUMAN_NAME']
      response.append({
          "id": resultId,
          "name": resultHN
        })

    # return ['one','two']
    return response

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

@app.route('/meta')
def meta():
  return app.send_static_file('views/meta.html')

@app.route('/pca')
def pca():
  return app.send_static_file('views/pca.html')

@app.route('/layerEpoch')
def layer():
  return app.send_static_file('views/layerEpoch.html')

@app.route('/iter2')
def iter2():
  return app.send_static_file('views/iter2.html')

@app.route('/iter1')
def iter1():
  return app.send_static_file('views/iter1.html')


# this is what we're running - sets up the server 
if __name__ == '__main__':

  # Add api resources (sets up the routes for the data stuff)
  api.add_resource(NeuralResource, '/results/<string:_id>')
  api.add_resource(NeuralResources, '/results')

  #Run Server on port 0.0.0.0
  app.run(host='0.0.0.0', port=8000, debug=True)