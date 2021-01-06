#!C:\Users\Lenovo\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0\python.exe
from random import random
import requests
import time
import json
import sys
import re
import cgi, cgitb


newformdata = cgi.FieldStorage()

FORM = 1
FIELDS = 1
TITLE = 8
ID = 0
NAME = 1
DESCRIPTION = 2
TYPE = 3
VALUE = 4
OPTIONS = 1
URL = -2

types = {
    0: 'Short Answer',
    1: 'Paragraph',
    2: 'Radio',
    3: 'Dropdown',
    4: 'Checkboxes',
}

choice_types = ['Radio', 'Checkboxes', 'Dropdown']
choice_no=[2,3,4]
answer={}
def get_url(data):
    #print(data[URL])
    return 'https://docs.google.com/forms/d/e/' + data + '/formResponse'

def get_name(data):
    return data[FIELDS][TITLE]

def get_options(elem):
    options_raw = elem[VALUE][0][OPTIONS]
    return list(map(lambda l: l[0], options_raw))

def get_fields(data):
    fields = {}
    try:
        for elem in data[FORM][FIELDS]:
            field = {
                    'description': elem[DESCRIPTION],
                    'type': types.get(elem[TYPE]),
                    'id': elem[VALUE][0][ID],
                    'submit_id': 'entry.' + str(elem[VALUE][0][ID]),
                    }
            
            if field['type'] in choice_types:
                field['options'] = get_options(elem)

            fields[elem[NAME]] = field
    except:
        print("Content-type:text/html")
        print
        print("")
        print("")
    return fields

        
def parse_data(data_str,urlid):
    data = json.loads(data_str)
    global impdata
    impdata=data
    #myfunc(data)
    return {
        'url': get_url(urlid),
        'name': get_name(data),
        'fields': get_fields(data),
    }

def get_form(url,urlid):
    body = requests.get(url).text
    match = re.search(r'FB_PUBLIC_LOAD_DATA_ = ([^;]*);', body)
    if not match: return None
    data = parse_data(match.group(1),urlid)
    return data


def submit(form):
    payload = {}
    for name in form['fields']:
        field = form['fields'][name]
        if field['type'] in choice_types and field['value'] not in field['options']:
            payload[field['submit_id']] = '__other_option__'
            payload[field['submit_id'] + '.other_option_response'] = field['value']
        else:
            payload[field['submit_id']] = field['value']

    return requests.post(form['url'], data=payload)


def main(url,urlid):
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36'
    })

    form = get_form(url,urlid)
    # output(form) # uncomment this to print out the contents of the form
    fields = form['fields']
    # fill out the fields here
    # fields['Field Name']['value'] = 'What you want to submit'
    for el in impdata[FORM][FIELDS]:
        fields[el[NAME]]['value']=newformdata.getvalue(el[NAME])
      #  print(answer[name])
      
    #fields['Greek Sing Show']['value'] = 'Booth > Greek Sing'
    #fields['Best Ceremony']['value'] = 'Flag & Badge'
    #fields['Mac & Cheese']['value'] = 'Lobster Mac'
    #fields['What are your favorite colors?']['value'] = 'Purple, White, and Gold'
    #fields['If a man is unsatisfied with himself, with who he is, and he wants to make of himself a better man, what must he do?']['value'] = \
        #'Um... idk man, I thought it was Zach\'s job to tell me that?'
    
    submit(form)
    print("Content-type:text/html")
    print
    print("")
    print("")
    print("Form submitted")
    print("")
    
    #num_submitions = 0 # change this to spam more/less
   # for i in range(num_submitions):
  #      time.sleep(1 + random())
#        submit(form)


if __name__ == '__main__':
    # put your url here
    urlid=newformdata.getvalue('linkval')
    url = 'https://docs.google.com/forms/d/e/'+str(urlid)+'/viewform?usp=sf_link'
    main(url,urlid)
