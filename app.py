import random as rn
from flask import Flask,render_template,url_for,request
import pandas
import tempfile
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

app = Flask(__name__)


def delete(X):

    for k, v in X.items():
        for i in v:
            if i =='':
                v.remove('')
    return X


def random(X):
    if len(X)>0:
        x=rn.choice(X)
        X.remove(x)
    else:
        return ""
    return x


def tirage(X,y):

    dicte={}
    number_of_grps=len(y)
    nb=len(X)//len(y)

    for i in y:
        dicte[i]=[]
    while (X!=[]):
        for j in y :
            dicte[j].append(random(X))
    dicte=delete(dicte)
        
    return dicte,number_of_grps,nb+1

def emaill(person,equipe,sujet):
    team=""
    data = person.split("@")
    for ee in equipe:
        team +="- "+(ee.split("@"))[0]+"\n"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('mastersim1920@gmail.com', 'sim20192020')
    message = MIMEMultipart('alternative')
    message['Subject'] = 'Random'
    message['From'] = 'mastersim1920@gmail.com'
    message['To'] = person
    message.attach(MIMEText('Salam {} .\n Votre sujet  : {}.\n Votre equipe :\n {} \n Bon courage.'.format(data[0],sujet,team)))
    server.sendmail('mastersim1920@gmail.com',person, message.as_string())
    server.quit()
    print("well done !!")
    return 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/randomm', methods=['POST'])
def randomm():


    if request.method == 'POST':
        file_ = request.files["link"]

        code = request.form['code']
        data_xls = pandas.read_excel(file_)

        if(int(code)==134679):
            X=data_xls.iloc[:,0].values
            X = [x for x in X if str(x) != 'nan']
            Y=data_xls.iloc[:,1].values
            Y = [x for x in Y if str(x) != 'nan']
            result,b,c=tirage(list(X),list(Y))
            print(result)
            for k, v in result.items():
                for i in v:
                    a=emaill(i,v,k)
       
            print(result)

            
        else:
            return render_template('index.html')


   
    return render_template('docs.html',result=result)


if __name__ == '__main__':
    app.run(debug=False)


