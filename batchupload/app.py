from flask_httpauth import HTTPBasicAuth
from flask import Flask, request, session, jsonify, Response, make_response, send_file, render_template
from flask_admin import Admin
from flask_admin.contrib.fileadmin import FileAdmin
from flask_cors import CORS
from datetime import timedelta
import os.path as op



from Constants import REDIS_URL, MYSQL_URL
from utils import CustomJSONEncoder

from excelUpload import up_api

app = Flask(__name__)

# CORS(app, resources=r'/*', supports_credentials=True)

auth = HTTPBasicAuth()

# app.debug = True
# 处理jsonify返回的时间格式
app.json_encoder = CustomJSONEncoder
app.secret_key = "wdsad"

app.config["REDIS_URL"] = REDIS_URL

# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=0.5) # 配置7天有效
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1) # 配置7天有效

# admin = Admin(app, name='Flower And Shit', template_mode='bootstrap3')

# 允许所有跨域请求
@app.after_request
def after_request(response):
    # response.headers.add('Access-Control-Allow-Origin', requests.getHeader("Origin"))
    response.headers.add('Access-Control-Allow-Origin', "*")
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response


app.register_blueprint(up_api,url_prefix='/batchupload')
#app.register_blueprint(report_api,url_prefix='/report')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=7111,debug=True)


