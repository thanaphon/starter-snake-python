import bottle
import os
import random

from api import *


@bottle.route('/')
def static():
    return "the server is running"


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data
    print(data)

    print ("Starting game %s" % data["game"]["id"])
    return StartResponse("#00ff00")

#def peek_next(head, moving_ch):
    
    
#def check_collision(data,moving_ch):
#    next_loc = data['you']['body']
    
def get_prevmove(bodylog):
   (py,px) =  (bodylog['body'][0]['y'] - bodylog['body'][1]['y'], bodylog['body'][0]['x'] - bodylog['body'][1]['x'])
   if (-1,0) == (py,px):
       return 'up'
   if (1,0) == (py,px):
       return 'down'
   if (0,-1) == (py,px):
       return 'left'
   if (0,1) == (py,px):
       return 'right'
   return 'stay'

OPP_dir = {'up' : 'down' ,  'down' : 'up' , 'left' : 'right' , 'right': 'left','stay':'None'}    

@bottle.post('/move')
def move():
    data = bottle.request.json

    # TODO: Do things with data
    
    directions = ['up', 'down', 'left', 'right']
    
    #Get possible moving direction 
    
    #1) cannot get previous moving direction: move up y-1
    avoidlist = []
    avoidlist.append(OPP_dir[get_prevmove(data['you'])]) 
    #[ x for x in directions if x not in avoidlist]
    # set(directions) -set(avoidlist)    
    print(avoidlist)
    
    print (data)
    direction = 'up'
    
    while direction in avoidlist:
        direction = random.choice(directions)
    print ("Moving %s" % direction)
    
    return MoveResponse(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    # TODO: Do things with data

    print ("Game %s ended" % data["game"]["id"])


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=True)



#data  = { 'turn': 7, 'game': {  'id': 'ca6e31d8-2621-4474-8f0e-667c1b003130' }, 'board': { 'food': [{'y': 5, 'x': 7  }, {'y': 17, 'x': 0    }, { 'y': 13, 'x': 7 }],  'width': 20, 'snakes': [{'body': [{ 'y': 5,  'x': 0}, { 'y': 6,  'x': 0 }, {  'y': 7,  'x': 0}, {'y': 8, 'x': 0 }],  'health': 98,  'id':  '6e001a29-f14d-4ac9-ad9a-29d95f699050',  'name':  'Snake 1' }, { 'body': [{'y': 2,  'x': 19 }, { 'y': 2, 'x': 18  }, {'y': 2,  'x': 17}], 'health': 93,  'id': 'beb52136-e9a0-489d-8db5-8b659f344956',  'name':  'Snake 2' }],  'height': 20 },  'you': {  'body': [{'y': 5,  'x': 0}, { 'y': 6,  'x': 0  }, { 'y': 7, 'x': 0  }, {  'y': 8,  'x': 0 }],  'health': 98,  'id':  '6e001a29-f14d-4ac9-ad9a-29d95f699050',  'name':  'Snake 1'  }}