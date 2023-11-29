#!/usr/bin/env python
# coding: utf-8

# In[1]:


import telebot
import time
from telebot import types
import json
import torch
import argparse, os

def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)
        
parser = argparse.ArgumentParser()
parser.add_argument('-mp','--main_path', help= 'paste path to main QA.json file')
parser.add_argument('-p','--path', help= 'paste path to test.json file')
parser.add_argument('-m','--model', help= 'paste path to model file', type=dir_path)

args = vars(parser.parse_args())
path_to_main = args["main_path"]
path_to_test = args["path"]
path_to_data = args["model"]



#from transformers import GPT2Tokenizer , GPT2ForSequenceClassification
#output_dir = './gptmodel_save/'
#model = GPT2ForSequenceClassification.from_pretrained(output_dir)
#tokenizer = GPT2Tokenizer.from_pretrained(output_dir)

from transformers import BertConfig, BertForSequenceClassification, BertTokenizer
#output_dir = './model_save/'
output_dir = path_to_data

model = BertForSequenceClassification.from_pretrained(output_dir)
tokenizer = BertTokenizer.from_pretrained(output_dir)


token = '6705181314:AAH1F4h1C_rpM5pkcu3tXdeHkznDxIESz3o'
bot = telebot.TeleBot(token, parse_mode='None')
bot_name = 'ITMO BOT'

#model= torch.load('/Users/mac/Desktop/test/model.pth')


def menu():
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('help', callback_data='help'))   
        markup.add(types.InlineKeyboardButton('contact', callback_data='contact'))   
        markup.add(types.InlineKeyboardButton('main questions', callback_data='main questions'))  
        markup.add(types.InlineKeyboardButton('more questions', callback_data='more questions')) 
        markup.add(types.InlineKeyboardButton('application', callback_data='application'))    
        return markup
def main():       
    @bot.message_handler(commands=['start'])  # Ответ на команду /start
    def start(message):
        mess = f'hi, <b>{message.from_user.first_name}</b>!\nI am - <b>{bot_name}</b>'
        markup = menu()
        bot.send_message(message.chat.id, mess, reply_markup=markup, parse_mode='html')

def restart(message):
    mess = f'hi, <b>{message.from_user.first_name}</b>!\nI am - <b>{bot_name}</b>'
    markup = menu()
    bot.send_message(message.chat.id, mess, reply_markup=markup, parse_mode='html')


# In[2]:


with open(path_to_main, 'r') as json_data:
    main_intents = json.load(json_data)
corpse = []
responses = []
for intent in main_intents['intents']:
    tag = intent['tag']
    response = intent['responses']
    print(tag+"\n")
    corpse.append(tag)# here we are appending the word with its tag
    responses.append(response)


# In[3]:


from nltk.tokenize import regexp_tokenize
@bot.callback_query_handler(func=lambda call: True)
def message_reply(call):
    if call.data == 'contact':
        mess = 'click on mail to get contact with staff'
        bot.send_message(call.message.chat.id,mess)
        mess = """
Program coordinator --  aakarabintseva@itmo.ru
International office -- international@itmo.ru
Student office -- aakiseleva@itmo.ru
Migration office -- aakhalilova@itmo.ru 
"""
        bot.send_message(call.message.chat.id,mess)
        time.sleep(5)
        restart(call.message)
    elif call.data == 'help': 
        mess = """
contact --  to find Email address of specific staff in ITMO
main questions -- to answer most frequent questions from candidates
more questions -- to answer other questions
application -- to redirect to page to fill application
"""
        bot.send_message(call.message.chat.id,mess)
        time.sleep(5)
        restart(call.message)
    elif call.data == 'main questions':
        mess = 'please choose interested item'
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for i in range(len(corpse)):            
            markup.add(corpse[i])  
        msg = bot.send_message(call.message.chat.id,mess, reply_markup=markup)
        bot.register_next_step_handler(msg, main_questions)
    elif call.data == 'more questions':
        msg = bot.send_message(call.message.chat.id, 'please write to questions')
        bot.register_next_step_handler(msg, more_questions)
    elif call.data == 'application':
        linked_user = 'https://signup.itmo.ru/master'
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text='redirect to ITMO',
                            url=linked_user))
        mess = 'click to redirect to application form'
        bot.send_message(call.message.chat.id,mess, reply_markup=markup)
        time.sleep(5)
        restart(call.message)
    


def main_questions(message):
    def tokenize(sentence):
        return regexp_tokenize(sentence, pattern="\w+")

    def score_words(x,y):
          """ returns the jaccard similarity between two lists """
          intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
          union_cardinality = len(set.union(*[set(x), set(y)]))
          return intersection_cardinality/float(union_cardinality)
    sentence = message.text
    if(any(sentence.lower()==item.lower() for item in ["quit","finish","over","bye","goodbye"])):
        print(f"{bot_name}: Goodbye , have a nice day")

    similarity = []
    for i in corpse:
        similarity.append(score_words(sentence,i))
    #print(similarity)
    
    if(max(similarity) > 0.5 and len(tokenize(sentence))==1 ):
        print(f"{bot_name}: "+responses[similarity.index(max(similarity))][0])
    
    mess = responses[similarity.index(max(similarity))][0]
    bot.send_message(message.chat.id, mess)

    time.sleep(5)
    restart(message)
    


# In[ ]:


import spacy
import random
import re
from torch import nn

with open(path_to_test, 'r') as json_data:
        intents = json.load(json_data)
    
def maximum(list):
    output = list.sort()
    return output[0][-3:] , output[1][-3:]
    #return [output[1][-1],output[1][-2],output[1][-3]]
def multiple_question_detect(sent):
    sent = sent.replace('?',' ?')
    sent = re.sub(r'\s\s+',' ',sent)
    sent = re.sub(r"^\s+|\s+$", "", sent)
    sent = re.split('(?<=[.!?,]) +',sent)
    texts = []
    for i in range(len(sent)):
        sent[i] = re.sub('[^a-zA-Z0-9 ]', '', sent[i])
        sent[i] = re.sub(r"^\s+|\s+$", "", sent[i])
        if(len(sent[i])==0):
            texts.append(sent[i])
    
    for i in texts :
        sent.remove(i)
    return sent

def more_questions(message):

    sent = message.text

    sent = multiple_question_detect(sent)

    model.eval()
    max_length = 64
    print('item num :')
    print(len(sent))
    indexs = []
    if(len(sent)==1):
        encoding = tokenizer(sent, return_tensors='pt', max_length=max_length, truncation=True)
        b_input_ids = encoding['input_ids']
        #token_type_ids = encoding['token_type_ids']
        attention_mask = encoding['attention_mask']
        outputs = model(b_input_ids, 
                                    token_type_ids=None, 
                                    attention_mask=attention_mask)
        m = nn.Softmax(dim=1)
        outputs= m(outputs[0])
        prob , index = maximum(outputs[0])
        print(index)
        indexs.append(index)
        print(prob[-1])
        mess = ''
        if(prob[-1] > 0.5):
            for intent in intents['intents']:
                if index[-1]+1 == intent["tag"]:
                    mess = random.choice(intent['responses'])
                    print(random.choice(intent['responses']))
                
        else:
            mess = "Sorry I am unable to Process Your Request"
            mess += '\n'
            mess += "You may find the way forward in https://en.itmo.ru/en/viewjep/2/5/Big_Data_and_Machine_Learning.htm"
        print(mess)
        bot.send_message(message.chat.id, mess)
    elif(len(sent)>1):
        print(sent)
        for i in sent:
            encoding = tokenizer(i, return_tensors='pt', max_length=max_length, truncation=True)
            b_input_ids = encoding['input_ids']
            #token_type_ids = encoding['token_type_ids']
            attention_mask = encoding['attention_mask']
            outputs = model(b_input_ids, 
                                    token_type_ids=None, 
                                    attention_mask=attention_mask)
            m = nn.Softmax(dim=1)
            outputs= m(outputs[0])
            prob , index = maximum(outputs[0])
            print(index)
            indexs.append(index)
            print(prob)
            mess = ''
            if prob[-1] > 0.5:
                print('hi')
                for intent in intents['intents']:
                    if index[-1]+1 == intent["tag"]:
                        mess += random.choice(intent['responses'])
                        mess += '\n'
                        
                        print(random.choice(intent['responses']))
            else:
                mess += "Sorry I am unable to Process Your Request"
                mess += '\n'
                mess += "You may find the way forward in https://en.itmo.ru/en/viewjep/2/5/Big_Data_and_Machine_Learning.htm"
            bot.send_message(message.chat.id, mess) 
    
    

    time.sleep(5)
    mess = 'is this response answer your questions ?'
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Yes') 
    markup.add('No') 
    msg = bot.send_message(message.chat.id,mess, reply_markup=markup)
    bot.register_next_step_handler(msg, satisfaction,indexs)

def satisfaction(message,other_answer):
    if(message.text == 'Yes'):
        restart(message)
    elif(message.text == 'No'):
        mess = ''
        if(len(other_answer)==1):
            for index in reversed(range(len(other_answer[0]))[:-1]):
                print(index)
                for intent in intents['intents']:
                    if other_answer[0][index]+1 == intent["tag"]:
                        mess += random.choice(intent['responses'])
                        mess += '\n'
                        mess += '\n'
                    
                    print(random.choice(intent['responses']))
            bot.send_message(message.chat.id,mess)
            time.sleep(5)
            mess += 'if it is still does not answer your question , use instruction below'
            mess += '\n'
            mess += "You may find the way forward in https://en.itmo.ru/en/viewjep/2/5/Big_Data_and_Machine_Learning.htm"
            mess += '\n'
            mess += "You may write email to coordinator with aakarabintseva@itmo.ru"
            bot.send_message(message.chat.id,mess)
            time.sleep(5)
            restart(message)
        elif(len(other_answer)>1):
            mess = ''
            print('check :')
            print(other_answer)
            for i in range(len(other_answer)):
                for index in reversed(range(len(other_answer[i]))[:-1]):
                    for intent in intents['intents']:
                        if other_answer[i][index]+1 == intent["tag"]:
                            mess += random.choice(intent['responses'])
                            mess += '\n'
                            mess += '\n'
                        
                        #print(random.choice(intent['responses']))
            bot.send_message(message.chat.id,mess)
            time.sleep(5)
            mess = ''
            mess += 'if it is still does not answer your question , use instruction below'
            mess += '\n'
            mess += "You may find the way forward in https://en.itmo.ru/en/viewjep/2/5/Big_Data_and_Machine_Learning.htm"
            mess += '\n'
            mess += "You may write email to coordinator with aakarabintseva@itmo.ru"
            bot.send_message(message.chat.id,mess)
            time.sleep(5)
            restart(message)
    
if __name__ == "__main__":
        main()
        bot.polling(none_stop=True)


# In[ ]:




