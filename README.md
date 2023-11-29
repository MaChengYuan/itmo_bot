# train itmo_bot
#parameters from model is too big to be uploaded
1. download test.json

2. train with bert transofmer

3. save the parameters and load it in chatbot to acticate

   pip install virtualenv
   
   virtualenv <any_name>
   
   source <any_name>/bin/activate
   
   pip install -r requirements.txt

command in terminal :

python <bert_path.py> -p <datasets> -m <saving_model_path>



# load model to itmo_bot
command in terminal :

python <chat_bot.py> -mp <main_QA.json> -p <test.json> -m <saving_model_path>
