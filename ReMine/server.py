from flask import Flask, request, render_template, jsonify, Response

import subprocess
import sys
import os
from subprocess import Popen, PIPE

from gevent.wsgi import WSGIServer

from flask_cors import CORS, cross_origin

import libtmux

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
@cross_origin(origin='*')
def render():

    return render_template('example.html')


# @app.route('/C')
# @cross_origin(origin='*')
# def runC():
#     #subprocess.call(['make', '-C', '../c++'])
#     process =Popen(['./../c++/q1'],stdout = PIPE,stderr = PIPE)
#     stdout,stderr = process.communicate()
#     return stdout

# @app.route('/remine', methods =['POST'])
# @cross_origin(origin='*')
# def runRemine():
#     #subprocess.call(['bash','remine-ie.sh'])
#     ret = []
#     with open('results_remine/remine_result.txt','r') as f:
#         for line in f:
#             ret.append(line)
#     input = request.data
#     #text = input.get('text')
#     print(input)
#     return jsonify({'tuple':ret})

@app.route('/remine', methods =['POST'])
@cross_origin(origin='*')
def runRemine():
    default_input_model = 'pre_train/segmentation.model'
    #process = Popen(stdin=PIPE, stdout=PIPE, stderr=PIPE)
    input_path = 'tmp_remine/tokenized_test.txt'
    pos_path = 'tmp_remine/pos_tags_test.txt'
    dep_path = 'tmp_remine/deps_test.txt'
    ems_path = 'tmp_remine/remine_entity_position.txt'

    command = '{} {} {} {}'.formmat(input_path, pos_path, dep_path,ems_path)

    pane.send_keys(command, enter =True)
    #stdout,stderr = process.communicate(input = b' {}\n{}\n{}\n'.formmat(input_path, pos_path, dep_path))
    # subprocess.call(['./bin/remine',
    #                  '--input_file', '{}'.format(input_path),
    #                  '--pos_file', '{}'.format(pos_path),
    #                  '--deps_file', '{}'.format(dep_path),
    #                  '--model', '{}'.format(model_path),
    #                  '--mode', '0'])
    #os.waitpid(pid, 0)

    output_path = 'remine_tokenized_segmented_sentences.txt'
    with open('tmp_remine/{}'.format(output_path), 'r') as f:
        for line in f:
            ret.append(line)
    #input = request.data
    #text = input.get('text')
    #print(input)
    return jsonify({'tuple':ret})

if __name__=='__main__':
    #app.run(debug = True, host = '0.0.0.0',port=1111)
    # app.run(debug = True, host = 'localhost', port=5000)
    server = libtmux.Server()
    session = server.find_where({"session_name": "preload"})
    window = session.new_window(attach=False, window_name="test")
    pane = window.split_window(attach=False)
    pane.send_keys('./bin/remine --model pre_train/segmentation.model --mode 1', enter=False)

    #session.send_keys('', enter=True)
    http_server = WSGIServer(('0.0.0.0', 1111), app)

    http_server.serve_forever()

