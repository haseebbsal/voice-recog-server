from flask import Flask,jsonify,request
from flask_cors import CORS
from document_reader import reader
from image_app import process_images
from voice_app import transcribe_audio
from llm_app import text_prompt
from nlp_app import llm_task_categorization
from pymongo import MongoClient
import json
# import urllib
# import requests
# import io
# import soundfile
import os
app = Flask(__name__)
CORS(app)
@app.route("/deleteTasks",methods=['POST'])
def delete():
    client = MongoClient("mongodb+srv://haseebb-sal:haskybeast123@haseebfirstcluster.1v5tosb.mongodb.net/voice-recog")
    client['voice-recog'].tasks.delete_many({})
    return jsonify('done')

@app.route("/tasks")
def get_data():
    client = MongoClient("mongodb+srv://haseebb-sal:haskybeast123@haseebfirstcluster.1v5tosb.mongodb.net/")
    task_data=client["voice-recog"].tasks.find()
    data=[]
    for i in task_data:
        data.append({'_id':str(i['_id']),'task_name':i['task_name'],'priority':i['priority']})
    print(data)
    return jsonify(data)
@app.route("/prompt",methods=['POST'])
def hello_world():
    print('files',request.files)
    print('form',request.form)
    prompt=request.form.get('prompt')
    pdf=request.files.get('pdf')
    image=request.files.get('image')
    audio=request.files.get('audio')
    client = MongoClient("mongodb+srv://haseebb-sal:haskybeast123@haseebfirstcluster.1v5tosb.mongodb.net/voice-recog")
    if(prompt and not pdf and not image and not audio):
        llm_generate=llm_task_categorization(prompt)
        data=eval(llm_generate)
        # print(data)
        client['voice-recog'].tasks.delete_many({})
        inserting_to_database=client['voice-recog'].tasks.insert_many(data)
        # llm_generate=text_prompt(prompt)
        # print(data)
        
        # print(type(llm_generate))
        return jsonify({'data':'done',"id":1})
    elif(pdf):
        content=''
        path=os.path.join('doc_data',pdf.filename)
        pdf.save(path)
        a=reader(path)
        for i in a:
            content+= i.page_content
        os.remove(path)
        llm_generate=llm_task_categorization(content)
        data=eval(llm_generate)
        # print(data)
        client = MongoClient("mongodb+srv://haseebb-sal:haskybeast123@haseebfirstcluster.1v5tosb.mongodb.net/voice-recog")
        client['voice-recog'].tasks.delete_many({})
        inserting_to_database=client['voice-recog'].tasks.insert_many(data)
        return jsonify({'data':'done',"id":1})
    elif(image):
        path=os.path.join('images',image.filename)
        image.save(path)
        processed=process_images(path)
        os.remove(path)
        llm_generate=llm_task_categorization(processed[0][1])
        data=eval(llm_generate)
        # print(data)
        client = MongoClient("mongodb+srv://haseebb-sal:haskybeast123@haseebfirstcluster.1v5tosb.mongodb.net/voice-recog")
        client['voice-recog'].tasks.delete_many({})
        inserting_to_database=client['voice-recog'].tasks.insert_many(data)
        return jsonify({"data":'done',"id":1})
    # elif(audio):
    #     pathee=os.path.join('audios',audio.filename)    
    #     audio.save(pathee)
    #     processed=transcribe_audio(pathee)
    #     os.remove(pathee)
    #     return jsonify({"data":processed,"id":1})
    return jsonify({"data":"nothing"})

if __name__=='__main__':
    app.run(port=3024,debug=True)