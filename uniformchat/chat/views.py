from tokenize import Double
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseRedirect
from .GroupMeAPI import groupmeapi as grme
from .DiscordAPI import discordapi as dapi
from .SlackAPI import slackapi as sapi
from datetime import datetime, date, time
from dateutil.parser import parse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from   django.contrib.messages import success
import json, requests
import psycopg2
from .encryption import *
from django.contrib.auth.decorators import login_required

g = grme()
d = dapi()
s = sapi()

#Temp username
#appusername = 'admin3'

#database connection
hostname = 'ec2-54-173-77-184.compute-1.amazonaws.com'
database = 'd2jg1tt725t1j4'
username = 'orysgydtilkzew'
pwd = '3c9add640649eec2525bc7871bcddebf38c054788f25ceee8e10b99d5fb40c62'
port_id = 5432
conn = psycopg2.connect(
    host = hostname,
    dbname = database,
    user = username,
    password = pwd,
    port = port_id)
cur = conn.cursor()


#GLOBAL USER VAR
redirectURL_GroupMe = "https://oauth.groupme.com/oauth/authorize?client_id=iUNSRzS3IDBTAIEy5BSg9in8goZVVXto5i762YjI9dtXSiDb"
redirectURL_Discord = "https://discord.com/api/oauth2/authorize?client_id=963435798294847488&permissions=67584&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fchat%2Fdiscordauth%2F&response_type=code&scope=bot%20messages.read%20identify%20guilds"
redirectURL_Slack = "https://slack.com/oauth/v2/authorize?client_id=3374157642694.3380563549894&scope=incoming-webhook,channels:history,chat:write&user_scope=channels:read,chat:write,groups:history,groups:read,groups:write,identify,channels:history"
redirectBack = "https://uniform-chat.herokuapp.com/messages"
redirectBack_discd = "https://uniform-chat.herokuapp.com/messages/adddiscchat_d/"
groupid_gme = 1
groupid_disc = 1
groupid_slack = '1'

#global var to know what accounts user has connected 
#groupme_conn = False
#discord_conn = False
#slack_conn = False

def home(request):
    if request.user.is_authenticated:
        return render(request, 'home3.html')
    else:
        return render(request, 'home2.html')

@login_required(login_url='https://uniform-chat.herokuapp.com/login/')
def tutorials(request):
    return render(request, 'home.html')

def authhub(request):
    global appusername
    appusername = request.user.username
    #reading key file
    conn = psycopg2.connect(
        host = hostname,
        dbname = database,
        user = username,
        password = pwd,
        port = port_id)
    cur = conn.cursor()

    db= "SELECT * FROM users WHERE username = '"+appusername+"';"

    cur.execute(db)
    conn.commit()
    allaccounts= cur.fetchall()
    cur.close()
    conn.close()

    global groupme_conn
    groupme_conn = False
    global slack_conn
    slack_conn = False
    global discord_conn
    discord_conn = False

    for accounts in allaccounts:
        discord_conn = False
        if (accounts [2] != '0'):
            discord_conn = True
        if (accounts [3] != '0'):
            groupme_conn = True
        if (accounts [4] != '0'):
            slack_conn = True

    return render(request, 'authhub.html', {'groupme':groupme_conn,'discord':discord_conn,'slack':slack_conn, 'username':appusername})

@login_required(login_url='https://uniform-chat.herokuapp.com/login/')
def messages(request):
    global appusername
    appusername = request.user.username
    #reading key file
    conn = psycopg2.connect(
        host = hostname,
        dbname = database,
        user = username,
        password = pwd,
        port = port_id)
    cur = conn.cursor()

    db= "SELECT * FROM users WHERE username = '"+appusername+"';"

    cur.execute(db)
    conn.commit()
    allaccounts= cur.fetchall()
    cur.close()
    conn.close()

    for accounts in allaccounts:
        discordex = accounts [2]
        groupmeex = accounts [3]
        slackex = accounts[4]
    
    global groupme_conn
    groupme_conn = False
    global slack_conn
    slack_conn = False
    global discord_conn
    discord_conn = False
    if(groupmeex == '0' and discordex == '0' and slackex == '0'):
        #RIDIRECT TO NEW PAGS
        return redirect('authhub')
    if (groupmeex != '0'):
        print(" TRUE ") 
        groupme_conn = True
        global groupme_at
        groupme_at = returnGroupMeKey(appusername)
    if (discordex != '0'):
        discord_conn = True
        global discord_at
        discord_at = discordex
    if (slackex != '0'):
        slack_conn = True
        global slack_at
        slack_at = slackex  

    return render(request, 'messages.html')

@login_required(login_url='https://uniform-chat.herokuapp.com/login/')
def updateM(request):
    global appusername
    appusername = request.user.username
    conn = psycopg2.connect(
        host = hostname,
        dbname = database,
        user = username,
        password = pwd,
        port = port_id)
    cur = conn.cursor()

    db= "SELECT * FROM read WHERE username = '"+appusername+"';"

    cur.execute(db)
    conn.commit()
    allchats_r = cur.fetchall()
    cur.close()


    conversations = []
    if groupme_conn:
        listOfChats = g.listChats_GroupMe(groupme_at)
        convos= json.loads(listOfChats)

        for chat in convos['response']:
            snippet = chat['messages']['preview']['text']
            if(len(snippet) > 80):
                snippet = snippet[:80] + "..."
            snippet=snippet.replace("'", "")
            time = datetime.fromtimestamp(chat['messages']['last_message_created_at'])
            chat['time'] = time.strftime("%b %d, %Y | %I:%M %P")

            convers = {
                'platform':'GroupMe',
                'snippet' : snippet,
                'group_id': str(chat['group_id']),
                'name' : chat['name'],
                'time' : chat['time']
            }
            conversations.append(convers)
        
    if discord_conn:
        cur = conn.cursor()

        db= "SELECT * FROM discord_ch WHERE username = '"+appusername+"';"

        cur.execute(db)
        conn.commit()
        allchannels = cur.fetchall()
        cur.close()
        for channel in allchannels:
            channid = channel[1]
            channname = channel[2]
            channnum = channel[3]

            x='{"messages": '+((d.getMessages_Discord(channid)).decode("utf-8"))+ '}'
            discmsgs = json.loads(x)
            for msg in discmsgs['messages']:
                snippet = msg['content']
                if(len(snippet) > 80):
                    snippet = snippet[:80] + "..."
                time = msg['timestamp']
                break

            dt = parse(time)
            convers = {
                'platform':'Discord',
                'snippet' : snippet,
                'group_id': channnum,
                'name' : channname,
                'time' : dt.strftime("%b %d, %Y | %I:%M %P")
            }
            conversations.append(convers)
    if slack_conn:
        cur = conn.cursor()

        db= "SELECT * FROM slack_ch WHERE username = '"+appusername+"';"

        cur.execute(db)
        conn.commit()
        allchannels = cur.fetchall()
        cur.close()

        for channel in allchannels:
            channid = channel[1]
            channname = channel[2]
            channnum = channel[3]
            try:
                x=s.get_messages_slack(channid)
            except:
                break
            for msg in x:
                snippet = msg['text']
                if(len(snippet) > 80):
                    snippet = snippet[:80] + "..."
                ts= float(msg['ts'])
                break

            time = datetime.fromtimestamp(ts)
            convers = {
                'platform':'Slack',
                'snippet' : snippet,
                'group_id' : channnum,
                'name' : str(channname),
                'time' : time.strftime("%b %d, %Y | %I:%M %P")
            }
            conversations.append(convers)

    sorted_convo = list(reversed(sorted(conversations,key=lambda  x:datetime.strptime(x['time'],'%b %d, %Y | %I:%M %p'))))
    mess_str = '{"response": ['
    for x in sorted_convo[:-1]:
        mess_str+= json.dumps(x) +', '
    mess_str += json.dumps(sorted_convo[-1]) + ']}'

    allmessages= json.loads(mess_str)
    count = 0
    for chat in allmessages['response']:
        new = True
        for chats_r in allchats_r:
            if (chats_r[1] == str(chat['group_id'])):
                new = False
                if(chats_r[2] != chat['snippet']):
                    read ='true'
                    cur = conn.cursor()

                    db= "UPDATE read SET snippet =  '" + chat['snippet'] + "', uread = 'false' WHERE chanID = '" + str(chat['group_id']) + "'"

                    cur.execute(db)
                    conn.commit()
                    cur.close()
                break
        
        if (new == True):
            cur = conn.cursor()

            db= "INSERT INTO read (username, chanID, snippet, uread) VALUES ( '" + appusername + "', '" + str(chat['group_id']) + "', '" + chat['snippet'] + "', 'false')"

            cur.execute(db)
            conn.commit()
            cur.close()

        cur = conn.cursor()
        db= "SELECT * FROM read WHERE username = '"+appusername+"' AND chanid = '"+str(chat['group_id'])+"';"

        cur.execute(db)
        conn.commit()
        ifread = cur.fetchall()
        cur.close()

        read = 'true'
        for z in ifread:
            if (z[3] == 'false'):
                read ='false'
                count +=1
        chat['read'] = read


    mess_str = '{"newm": "'+str(count)+'", ' + json.dumps(allmessages)[1:] 

    cur = conn.cursor()

    db = "SELECT * FROM messages WHERE username = '"+appusername+"'"

    cur.execute(db)
    conn.commit()
    ifread = cur.fetchall()
    cur.close()

    new = True
    for chats_r in ifread:
        if (chats_r[0] == appusername):
            new = False
            break
    
    if (new == True):
        cur = conn.cursor()

        db= "INSERT INTO messages (username, json) VALUES ( '" + appusername + "', '" + mess_str + "')"

        cur.execute(db)
        conn.commit()
        cur.close()
        conn.close()


        allmessages= json.loads(mess_str)
        return JsonResponse(allmessages)
    else:
        if (chats_r[1] == mess_str):
            conn.close()
            allmessages= json.loads(mess_str)
            return JsonResponse(allmessages)
        else :
            cur = conn.cursor()

            db= "UPDATE messages SET json = '"+mess_str+"' WHERE username = '"+appusername+"';"

            cur.execute(db)
            conn.commit()
            cur.close()
            conn.close()
            allmessages= json.loads(mess_str)
            return JsonResponse(allmessages)


@login_required(login_url='https://uniform-chat.herokuapp.com/login/')
def updateMload(request):
    conn = psycopg2.connect(
        host = hostname,
        dbname = database,
        user = username,
        password = pwd,
        port = port_id)
    cur = conn.cursor()

    db = "SELECT * FROM messages WHERE username = '"+appusername+"'"

    cur.execute(db)
    conn.commit()
    ifread = cur.fetchall()
    cur.close()
    conn.close()

    new = True
    for chats_r in ifread:
        if (chats_r[0] == appusername):
            mess_str=chats_r[1]
            new = False
            break
    
    if (new == True):
        return JsonResponse(json.loads( '{"response": "none" }'))
    else:
        allmessages= json.loads(mess_str)
        return JsonResponse(allmessages)

def read_all(request):
    conn = psycopg2.connect(
        host = hostname,
        dbname = database,
        user = username,
        password = pwd,
        port = port_id)
    cur = conn.cursor()

    db = "UPDATE read SET uread = 'true' WHERE username = '"+appusername+"'"

    cur.execute(db)
    conn.commit()
    cur.close()
    conn.close()
    updateM(request)

    return render(request, 'messages.html')
        

@login_required(login_url='https://uniform-chat.herokuapp.com/login/')
def groupMe_login(request: HttpRequest):
    return redirect(redirectURL_GroupMe)

@login_required(login_url='https://uniform-chat.herokuapp.com/login/')
def groupMe_auth(request: HttpRequest):
    conn = psycopg2.connect(
        host = hostname,
        dbname = database,
        user = username,
        password = pwd,
        port = port_id)
    cur = conn.cursor()

    #To do store the token in the data base via the store group me function
    storeGroupMeKey(appusername, request.GET.get('access_token'))


    #TO DO : update/replace GROUPME TOKEN TO DATABASE THAT MATCHES appusername variable instead of just adding
    
    groupme_access_token = request.GET.get('access_token')

    groupme_query = "SELECT * FROM users WHERE username = '" + appusername + "';"
    cur.execute(groupme_query)
    conn.commit()
    groupme_query = cur.fetchall()
    cur.close()
    conn.close()

    #groupme_query[3] = groupme_access_token
    
    print(groupme_query)
    
    return redirect(redirectBack)


@login_required(login_url='https://uniform-chat.herokuapp.com/login/')
def discord_login(request: HttpRequest):
    return redirect(redirectURL_Discord)

@login_required(login_url='https://uniform-chat.herokuapp.com/login/')
def discord_auth(request: HttpRequest):
    conn = psycopg2.connect(
        host = hostname,
        dbname = database,
        user = username,
        password = pwd,
        port = port_id)
    cur = conn.cursor()

    access = json.loads(d.exchange_code(str(request.GET.get('code'))))
    db= "UPDATE users SET discord_auth = '"+access['access_token']+"' WHERE username = '"+appusername+"';"

    cur.execute(db)
    conn.commit()
    cur.close()
    conn.close()

    return redirect(redirectBack)

@login_required(login_url='https://uniform-chat.herokuapp.com/login/')
def slack_login(request:HttpRequest):

    return redirect(redirectURL_Slack)

@login_required(login_url='https://uniform-chat.herokuapp.com/login/')
def slack_auth(request:HttpRequest):
    conn = psycopg2.connect(
        host = hostname,
        dbname = database,
        user = username,
        password = pwd,
        port = port_id)
    cur = conn.cursor()

    db= "UPDATE users SET slack_auth = '1' WHERE username = '"+appusername+"';"

    cur.execute(db)
    conn.commit()
    cur.close()
    conn.close()
    return redirect(redirectBack)

def index(request):
    gc = json.loads(g.getGroupName_GroupMe(groupid_gme , groupme_at))['response']

    msgs = json.loads(g.getMessages_GroupMe(groupid_gme , groupme_at))['response']

    for msg in msgs['messages']:
        msg['created_at'] = datetime.fromtimestamp(msg['created_at'])

    return render(request, 'chat.html', {'msgs':msgs['messages'],'gc':gc})

#constantly requests
@login_required(login_url='https://uniform-chat.herokuapp.com/login/')
def update(request):
    if (groupid_gme != 1):
        gc = json.loads(g.getGroupName_GroupMe(groupid_gme , groupme_at))['response']

        msgs = json.loads(g.getMessages_GroupMe(groupid_gme , groupme_at))['response']
        msgs['name']= gc['name']
        msgs['platform']= "groupme"
        for msg in msgs['messages']:
            time = datetime.fromtimestamp(msg['created_at'])
            msg['created_at'] = time.strftime("%b %d, %Y | %I:%M %P")

        return JsonResponse(msgs)
    elif(groupid_disc !=1):
        try:
            x='{"messages": '+((d.getMessages_Discord(groupid_disc)).decode("utf-8"))+ '}'
            with open("sample.json", "w") as outfile:
                outfile.write(x)
            #print(x)
            msgs = json.loads(x)

            msgs['name']= groupname_disc
            msgs['platform']= "discord"
            for msg in msgs['messages']:
                msg['name'] =  msg['author']['username']
                msg['text'] = msg['content']
                time = msg['timestamp']
                dt = parse(time)
                msg['created_at'] = dt.strftime("%b %d, %Y | %I:%M %P")
            return JsonResponse(msgs)
        except Exception as e:
            print(e)
            return render(request, 'messages.html')
    elif(groupid_slack != '1'):
        try:
            conversation_history = []
            try:
                conversation_history = s.get_messages_slack(groupid_slack)
            except Exception as e:
                raise
            mess_str = '{"messages": ['
            for x in conversation_history[:-1]:
                mess_str+= json.dumps(x) +', '
            mess_str += json.dumps(conversation_history[-1]) + ']}'
            msgs = json.loads(mess_str)

            msgs['name']= groupname_slack
            msgs['platform'] = "slack"
            for msg in msgs['messages']:
                msg['name'] = msg['user']
                msg['text'] = msg['text']
                ts = float(msg['ts'])
                time = datetime.fromtimestamp(ts)
                msg['created_at'] = time.strftime("%b %d, %Y | %I:%M %P")
            return JsonResponse(msgs)
        except Exception as e:
            print(e)
            return render(request, 'messages.html')
    else:
        return HttpResponse(status=204)

#sends message
def send(request):

    text = request.POST['text']

    g.sendMessage_GroupMe(text, groupid_gme,groupme_at)

    return None

def sendslack(request):

    text = request.POST['text']
    s.send_message_slack(text, groupid_slack)
    return None

#update gm id
@login_required(login_url='https://uniform-chat.herokuapp.com/login/')
def updategmID(request):
    global groupid_gme
    groupid_gme = request.POST['text']

    global groupid_disc
    groupid_disc = 1

    global groupid_slack
    groupid_slack = '1'

    conn = psycopg2.connect(
        host = hostname,
        dbname = database,
        user = username,
        password = pwd,
        port = port_id)
    cur = conn.cursor()

    db= "UPDATE read SET uread = 'true' WHERE username = '"+appusername+"' AND chanid = '"+str(groupid_gme)+"';"

    cur.execute(db)
    conn.commit()
    cur.close()
    conn.close()

    return render(request, 'messages.html')


#update disc id
@login_required(login_url='https://uniform-chat.herokuapp.com/login/')
def updatediscID(request):

    global groupid_gme
    groupid_gme = 1

    global groupid_slack
    groupid_slack = '1'

    global groupid_disc
    global groupname_disc

    conn = psycopg2.connect(
        host = hostname,
        dbname = database,
        user = username,
        password = pwd,
        port = port_id)
    cur = conn.cursor()

    db= "SELECT * FROM discord_ch WHERE username = '"+appusername+"' AND keyid = '" +request.POST['text']+ "';"

    cur.execute(db)
    conn.commit()
    achannel = cur.fetchall()
    cur.close()
    for channel in achannel:
        groupid_disc = int(channel[1])
        groupname_disc = channel[2]
    
    cur = conn.cursor()

    db= "UPDATE read SET uread = 'true' WHERE username = '"+appusername+"' AND chanid = '"+str(request.POST['text'])+"';"

    cur.execute(db)
    conn.commit()
    cur.close()
    conn.close()


    return render(request, 'messages.html')

@login_required(login_url='https://uniform-chat.herokuapp.com/login/')
def updateslackID(request):

    global groupid_gme
    groupid_gme = 1

    global groupid_disc
    groupid_disc = 1

    global groupid_slack
    global groupname_slack

    conn = psycopg2.connect(
        host = hostname,
        dbname = database,
        user = username,
        password = pwd,
        port = port_id)
    cur = conn.cursor()

    db= "SELECT * FROM slack_ch WHERE username = '"+appusername+"' AND keyid = '" +request.POST['text']+ "';"

    cur.execute(db)
    conn.commit()
    achannel = cur.fetchall()
    cur.close()

    for channel in achannel:
        groupid_slack = channel[1]
        groupname_slack = channel[2]

    cur = conn.cursor()

    db= "UPDATE read SET uread = 'true' WHERE username = '"+appusername+"' AND chanid = '"+str(request.POST['text'])+"';"

    cur.execute(db)
    conn.commit()
    cur.close()
    conn.close()

    return render(request, 'messages.html')
    


def signup_view(request):
    if request.method == 'POST':
        print("entered Post \n")
        sform = UserCreationForm(request.POST)
        if sform.is_valid():
            sform.save()

            appusername= sform.cleaned_data.get("username")
            global apppassword
            apppassword= sform.cleaned_data.get("password1")
            print(appusername,":",apppassword)
            conn = psycopg2.connect(
                host = hostname,
                dbname = database,
                user = username,
                password = pwd,
                port = port_id)
            cur = conn.cursor()

            db= "INSERT INTO users (username, password, discord_auth, groupme_auth, slack_auth) VALUES ( '" + appusername + "', '" + apppassword + "', '0', '0', '0')"

            cur.execute(db)
            conn.commit()
            cur.close()
            conn.close()

            return redirect('login')
    else:
        sform = UserCreationForm()
    return render(request, 'registration/signup.html', {'form':sform})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        print("entered login Post Request \n\n\n")
        if user is not None:
            login(request, user)
            fname = user.first_name
            global appusername
            appusername = username
            # messages.success(request, "Logged In Sucessfully!!")
            return redirect('messages')
        else:
            print("entered failed login\n")
            #messages.success(request, "CREDENTIALS ARE BAD!")
            return redirect('login')
    else: 
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form':form})
    # if request.method == 'POST':
    #     form = AuthenticationForm(data=request.POST)
    #     #global appusername
    #     appusername = form.get('username')
    #     print(appusername)
    #     #return redirect(redirectURL_GroupMe)
    # else:
    #     form = AuthenticationForm()
    

@login_required(login_url='https://uniform-chat.herokuapp.com/login/')
def adddiscchat(request):
    
    return render(request, 'adddisc.html')

@login_required(login_url='https://uniform-chat.herokuapp.com/login/')
def disc_add(request):
    if request.method == 'POST':

        x=((d.getMessages_Discord(request.POST['gcid'])).decode("utf-8"))
        with open("sample.json", "w") as outfile:
            outfile.write(x)
        discmsgs = json.loads(x)

        uc = ""
        try:
            uc = discmsgs['message']
        except (RuntimeError, TypeError, NameError):
            pass
        if uc == "Unknown Channel":
            print("invalid channel id")
            return render(request, 'adddisc.html')
        else:
            conn = psycopg2.connect(
                host = hostname,
                dbname = database,
                user = username,
                password = pwd,
                port = port_id)
            cur = conn.cursor()

            count = "SELECT COUNT(*) FROM discord_ch;"
            cur.execute(count)
            conn.commit()
            countt = cur.fetchone()
            cur.close()
            conn.close()
            
            conn = psycopg2.connect(
                host = hostname,
                dbname = database,
                user = username,
                password = pwd,
                port = port_id)
            cur = conn.cursor()

            channel_db = "INSERT INTO discord_ch (username, channel_id, channel_name, keyid) VALUES ( %s, %s, %s ,%s)"
            channel_dbvalue = (appusername,request.POST['gcid'], request.POST['gcname'],countt)

            cur.execute(channel_db, channel_dbvalue)
            conn.commit()
            cur.close()
            conn.close()
            return redirect(redirectBack)

@login_required(login_url='https://uniform-chat.herokuapp.com/login/')
def addslackchat(request):
    
    return render(request, 'addslack.html')

@login_required(login_url='https://uniform-chat.herokuapp.com/login/')
def slack_add(request):
    if request.method == 'POST':

        schannelid=s.get_channel_slack(request.POST['gcname'])
        if schannelid == "None":
            print("invalid channel id")
            return render(request, 'adddisc.html')
        else:
            conn = psycopg2.connect(
                host = hostname,
                dbname = database,
                user = username,
                password = pwd,
                port = port_id)
            cur = conn.cursor()

            count = "SELECT COUNT(*) FROM slack_ch;"
            cur.execute(count)
            conn.commit()
            countt = cur.fetchall()
            cur.close()
            conn.close()

            conn = psycopg2.connect(
                host = hostname,
                dbname = database,
                user = username,
                password = pwd,
                port = port_id)
            cur = conn.cursor()

            channel_db = "INSERT INTO slack_ch (username, channel_id, channel_name, keyid) VALUES ( %s, %s, %s ,%s)"
            channel_dbvalue = (appusername,schannelid, request.POST['gcname'],(countt[-1][-1]+10000))

            cur.execute(channel_db, channel_dbvalue)
            conn.commit()
            cur.close()
            conn.close()

@login_required(login_url='https://uniform-chat.herokuapp.com/login/')
def deletedchann(request):
    conn = psycopg2.connect(
        host = hostname,
        dbname = database,
        user = username,
        password = pwd,
        port = port_id)
    cur = conn.cursor()

    count = "DELETE FROM discord_ch WHERE username = '"+appusername+"';"
    cur.execute(count)
    conn.commit()
    cur.close()
    conn.close()

    return render(request)

@login_required(login_url='https://uniform-chat.herokuapp.com/login/')
def deleteschann(request):
    conn = psycopg2.connect(
        host = hostname,
        dbname = database,
        user = username,
        password = pwd,
        port = port_id)
    cur = conn.cursor()

    count = "DELETE FROM slack_ch WHERE username = '"+appusername+"';"
    cur.execute(count)
    conn.commit()
    cur.close()
    conn.close()

    return render(request)


def logout_view(request):
    logout(request)
    return redirect('https://uniform-chat.herokuapp.com')