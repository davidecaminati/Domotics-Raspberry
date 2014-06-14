
from flask import Flask, url_for #, render_template, request, jsonify


app = Flask(__name__)


    
    
@app.route('/')
def api_root():
    return 'Welcome'
    
@app.route('/shutdown')
def api_shutdown():
    import subprocess
    subprocess.call(["shutdown", "-f", "-s", "-t", "1"])
    return 'shutdown'
    
@app.route('/reboot')
def api_reboot():
    import subprocess
    subprocess.call(["shutdown", "-f", "-r", "-t", "1"])
    return 'reboot'
    
if __name__ == '__main__':
    app.run(host='192.168.0.86',debug = True)
