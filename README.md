# train itmo_bot
# PLEASE BE CAREFUL TO REPLACE <> WITH RELATIVE PATH FROM YOUR LOCAL DEVICE
1. download test.json

2. train with <BERT_Fine_Tuning_Sentence_Classification.py>

3. save the parameters and load it in chatbot to acticate
   (if no virtualenv)
   1) pip install virtualenv
   (if no environment name called itmo_bot)
   2) virtualenv itmo_bot
   
   3) source itmo_bot/bin/activate
   
   4) pip install -r requirements.txt

command in terminal :

python <BERT_Fine_Tuning_Sentence_Classification.py> -p <test.json> -m <saving_model_path>


# Load model to itmo_bot
command in terminal :

python <research_chat_bot.py> -mp <main_QA.json> -p <test.json> -m <saving_model_path>


# Must download files to run whole process

BERT_Fine_Tuning_Sentence_Classification.py

research_chat_bot.py

test.json

main_QA.json
