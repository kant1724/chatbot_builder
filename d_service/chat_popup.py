from flask import Flask, render_template, request
from d_service import properties
import json

def dynamic_grid_pop(request):
    user = request.form['user']
    project = request.form['project']
    param_holder = request.form['param_holder']
    title = request.form['title']
    column_info = request.form['column_info']
    content = request.form['content']
    
    return render_template("chat_popup/dynamic_grid_pop.html", user = user, project = project, param_holder = str(param_holder), title = title, column_info = column_info, content = content)

def dynamic_info_pop(request):
    user = request.form['user']
    project = request.form['project']
    param_holder = request.form['param_holder']
    title = request.form['title']
    column_info = request.form['column_info']
    content = request.form['content']
    
    return render_template("chat_popup/dynamic_info_pop.html", user = user, project = project, param_holder = str(param_holder), title = title, column_info = column_info, content = content)

def hwp_report_pop(request):
    user = request.form['user']
    project = request.form['project']
    param_holder = request.form['param_holder']
    title = request.form['title']
    file_path = request.form['file_path']
    
    return render_template("chat_popup/hwp_report_pop.html", user = user, project = project, param_holder = str(param_holder), title = title, file_path = file_path, file_ip = properties.get_file_ip())
