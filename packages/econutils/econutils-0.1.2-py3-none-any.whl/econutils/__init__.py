import uuid
from datetime import datetime
from IPython.display import display, Javascript
import urllib.request
import time

def get_token():
    current_time = datetime.now()
    key = f"{current_time.strftime('%Y%m%d%H%M%S%f')}-{uuid.uuid4()}"

    js_code = '''
    
    let url = window.location.href
    const regex = /\/user\/([^\/]+)\//;
    const match = url.match(regex);
    let username = match[1];
    let total_url = 'https://jupyter.proxy.econ.tu.ac.th/jupyterhub/authorize?username=' + username + '&secret=''' + key + '''';

    let complete = false;
    console.log("save: " + total_url);
    fetch(total_url,  
        {
            method: 'GET',
            headers: {
                'ngrok-skip-browser-warning': 'true'
            }
        })
        .then(response => 
        {
            complete = true;
            console.log('Data sent successfully')
        })
        .catch((error) => 
        {
            complete = true;
            console.error('Error:', error);
        });
    '''

    display(Javascript(js_code))

    time.sleep(0.5)

    contents = urllib.request.urlopen("https://jupyter.proxy.econ.tu.ac.th/jupyterhub/token?secret=" + key).read()
    result = contents.decode('utf-8')
    return result