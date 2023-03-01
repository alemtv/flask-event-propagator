import json, random, requests, time, datetime, threading
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# get params from config file
with open('config.json','r') as config:
    params = json.load(config)
    print(f'Config params: {params}')

# list for displaying data in the index.html file
response_list = [{}]

# class for managing background jobs
class NewThreadedTask(threading.Thread):
     def __init__(self):
         super(NewThreadedTask, self).__init__()
 
     def run(self):
        # get predefined JSON object list
        with open(params['events_file'], 'r') as file:
            events = json.load(file)

        # set job status
        params['job_status'] = 'In Progress'
        while params['job_status'] != 'Stop':
            # res_dict - tmp dictionary for storing response and status
            res_dict = {}
            # get random JSON object from predefined list
            event = random.choice(events)
            try:
                # send JSON object to a specific HTTP API endpoint
                res = requests.post(params['requests_endpoint'], json=event)
                status = res.status_code
                msg = res.json().get('message')
            except requests.exceptions.RequestException as e:
                status = 500
                msg = str(e)

            # just an extra check to make sure the list doesn't get too big
            if len(response_list) == params['response_limit']:
                response_list.clear()

            # gathering information for rendering index.html
            res_dict['datetime'] = datetime.datetime.now()
            res_dict['event'] = event
            res_dict['status'] = status
            res_dict['msg'] = msg
            response_list.append(res_dict)
                
            time.sleep(params['wait_time'])

        # set job status when the job is complete
        params['job_status'] = 'Ready'
        params['job_msg'] = 'Job has been completed'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', job_status=params['job_status'], msg=params['job_msg'], response_list=response_list)
    
    if request.form['submit'] == 'Start':
        if params['job_status'] == 'Ready':
            # new job is started (<input type="submit" name="submit" value="Start">)
            response_list.clear()
            new_thread = NewThreadedTask()
            new_thread.start()
            params['job_msg'] = 'Background job has been started successfully'
        else:
            params['job_msg'] = 'Job already started'
    else:
        # existing job is stopped (<input type="submit" name="submit" value="Stop">)
        if params['job_status'] in ('In Progress', 'Stop'):
            params['job_status'] = 'Stop'
            params['job_msg'] = 'The job is suspended'

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)