
from todoist_api_python.api import TodoistAPI
from datetime import datetime,timedelta
import google.generativeai as genai
import json
import configparser
import requests

config = configparser.ConfigParser()
config.read('config.ini')
api_key = config['todoist']['apiKey']
gemini_api_key = config['gemini']['apiKey']
api = TodoistAPI(api_key)

#These Names are 
pNames = ["Chores", "Financial", "Personal", "Lumen", "Work"]

# Fetch tasks synchronously
def get_tasks_sync_today():
    projects = getProjectNames(pNames)
    return_tasks = []
    try:
        tasks = api.get_tasks()
        for t in tasks:
            if t.due and t.due.date and datetime.strptime(t.due.date, "%Y-%m-%d") <= datetime.now():
                # Get project name based on project_id
                project_name = next((p['name'] for p in projects if p['id'] == t.project_id), None)

                taskToAdd = {'task': t.content, 'project': project_name}
                return_tasks.append(taskToAdd)
        return return_tasks
    except Exception as error:
       return error

def get_tasks_today():
    projects = getProjectNames(pNames)
    return_tasks = []
      
    try:
        tasks = api.get_tasks()
        for t in tasks:
            if t.due and t.due.date and datetime.strptime(t.due.date, "%Y-%m-%d") <= datetime.now() and t.is_completed == False :
                # Get project name based on project_id
                
                project_name = next((p['name'] for p in projects if p['id'] == t.project_id), None)
                
                if project_name != None:
                    taskToAdd = {'task': t.content, 'project': project_name, 'due_date': t.due.date}
                    return_tasks.append(taskToAdd)
        return return_tasks 
    except Exception as error:
       return error

def get_complete_tasks_this_week():
    projects = getProjectNames()
    return_tasks = []
 
    try:
        url = "https://api.todoist.com/sync/v9/completed/get_all"
        headers = {
            "Authorization": f"Bearer {api_key}"
        }

        response = requests.get(url, headers=headers)
        tasks = response.json()['items']
        

        for t in tasks:
            completed_timestamp =  datetime.strptime(t["completed_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
            eight_days_ago = datetime.now() - timedelta(days=8)
            if eight_days_ago <= completed_timestamp <= datetime.now():
                # Get project name based on project_id
                project_name = next((p['name'] for p in projects if p['id'] == t['project_id']), None)

                taskToAdd = {
                'task': t['content'],
                'project': project_name,
                'task_id': t['task_id'],
                'completed_time': t["completed_at"]  # Use the parsed datetime object
                }
                return_tasks.append(taskToAdd)
      
       
        return return_tasks
    except Exception as error:
       return error
   
def getProjectNames(names):
    project_names = []
    try:
        projects = api.get_projects()
       
        for p in projects:
            if p.name in names:
                project_names.append({'id': p.id, 'name': p.name})
    except Exception as error:
        print(error)

    return project_names

def geminiSummary():
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-pro')
    prompt_prefix = "You are my personal assistant and you are going to be letting me know what my tasks are for today.  I'm going to present you a json " + \
                    "that has the following format: {'task': 'create 3 min video', 'project': 'eyecreality', 'due_date': '2024-04-08'}. " + \
                    "Create a paragraph response.  This should be designed to be read by a voice over artist. Always include a count of total tasks and summarize any tasks in Chores, Lumen or Work  " +\
                    "START WITH 'HERE ARE YOUR TASKS TODAY' " + \
                    "You should create the answer in the form of a paragraph. Do not return any special characters. Do not read out any web addresses and remove all special characters. BEGIN TASK LIST:\n"

    taskSummaryRequest = prompt_prefix + str(get_tasks_today())
    response = model.generate_content(taskSummaryRequest)
    #print(response.text)

    return response.text


text = geminiSummary()

print(text)

       
    


