# train itmo_bot
#parameters from model is too big to be uploaded
1. download test.json

2. train with <bert_transformer.py>

3. save the parameters and load it in chatbot to acticate
   (if no virtualenv)
   1) pip install virtualenv
   
   2) virtualenv <any_name>
   
   3) source <any_name>/bin/activate
   
   4) pip install -r requirements.txt

command in terminal :

python <bert_transformer.py> -p <test.json> -m <saving_model_path>



# Load model to itmo_bot
command in terminal :

python <chat_bot.py> -mp <main_QA.json> -p <test.json> -m <saving_model_path>


# Must download files to run whole process

BERT_Fine_Tuning_Sentence_Classification.py

research_chat_bot.py

test.json

main_QA.json
