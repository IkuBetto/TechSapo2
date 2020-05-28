from django.shortcuts import render,redirect
from login.models import Users,Clients,Company,Connection,Business_talk,mail_password,Client_stage,Business_talk_stage
from datetime import datetime
import datetime as dt
from django.http import HttpResponse
from . import forms
from django.db.models import Q
from django.core.mail import send_mail
from email.mime.text import MIMEText
import smtplib
import pandas as pd
import os
UPLOAD_DIR = os.path.dirname(os.path.abspath(__file__)) + '/file/'
UPLOAD_DIR2 = os.path.dirname(os.path.abspath(__file__)) + '/file2/'

#ログイン画面に遷移する
def index(request):
	#today=dt.datetime.now()

	#ログインフォームを準備
	form = forms.login(request.GET or None)

	# user = Business_talk_stage(stage="失注")
	# user.save()
	# user = Users(name='別当郁',
	# 	           tel='080-2675-2670',
	# 	           department='管理部',
	# 	           position='一般',
	# 	           email="7416094@gmail.com",
	# 	           user_id="abcopqi3",
	# 	           password="11021102aA",
	# 	           update_at=today)
	# user.save()
	error=[]
	return  render(request,'login/login.html',{"form":form,"error":error})

#ログインに成功するとホーム画面に遷移
#失敗するとエラー文をログイン画面に表示
def home(request):
	#フォームに入力された情報を取得
	form = forms.login(request.POST)
	#formに正しい値が入力されたら
	if form.is_valid():
		#ユーザーIDとパスワードが一致するユーザーのid,メールアドレス,ユーザーID,パスワードを取得
		users=Users.objects.values('id','email','user_id','password').filter(user_id=form.cleaned_data["user_id"],password=form.cleaned_data["password"])
		#ユーザーIDとパスワードが一致するユーザーがいれば
		if users.first() != None:
			#ユーザーのidをセッションで管理
			request.session['id'] = users[0]["id"]
			#home_func呼び出し
			#今日登録した見込み客と今日予定されている商談を取得
			clients,business_talk = home_func()
			content=[]#今日登録した見込み客や今日予定されている商談がなければtemplateに送る
			# return render(request,'login/log.html',{"log":business_talk[0]["date"]})
			#今日登録した見込み客と今日予定されている商談が両方ともあれば
			if clients.first() != None and business_talk.first() != None:
				return render(request,'login/home.html',{"clients":clients,"business_talk":business_talk})
			#今日登録した見込み客がないかつ今日予定されている商談があれば
			elif clients.first() == None and business_talk.first() != None:
				return render(request,'login/home.html',{"clients":content,"business_talk":business_talk})
			#今日登録した見込み客があるかつ今日予定されている商談がなければ
			elif clients.first() != None and business_talk.first() == None:
				return render(request,'login/home.html',{"clients":clients,"business_talk":content})
			#今日登録した見込み客と今日予定されている商談が両方ともなければ
			else:
				return render(request,'login/home.html',{"client":content,"business_talk":content})
	#ユーザーIDとパスワードが一致するユーザーがいなければ
	error="ユーザーIDまたはパスワードが違います"
	return  render(request,'login/login.html',{"form":form,"error":error})
def home_display(request):
	#home_func呼び出し
	#今日登録した見込み客と今日予定されている商談を取得
	clients,business_talk = home_func()

	#今日登録した見込み客や今日予定されている商談がなければtemplateに送る
	content=[]
	# return render(request,'login/log.html',{"log":business_talk[0]["date"]})
	#今日登録した見込み客と今日予定されている商談が両方ともあれば
	if clients.first() != None and business_talk.first() != None:
		return render(request,'login/home.html',{"clients":clients,"business_talk":business_talk})
	#今日登録した見込み客がないかつ今日予定されている商談があれば
	elif clients.first() == None and business_talk.first() != None:
		return render(request,'login/home.html',{"clients":content,"business_talk":business_talk})
	#今日登録した見込み客があるかつ今日予定されている商談がなければ
	elif clients.first() != None and business_talk.first() == None:
		return render(request,'login/home.html',{"clients":clients,"business_talk":content})
	#今日登録した見込み客と今日予定されている商談が両方ともなければ
	else:
		return render(request,'login/home.html',{"client":content,"business_talk":content})
#今日登録した見込み客と今日予定されている商談を取得する関数
def home_func():
	#今日の日付取得
	today=dt.datetime.today()
	#今日登録した見込み客を取得
	clients = Clients.objects.all().values("clients_name", "company_id","clients_mail","tel").filter(created_at__date=today)
	for i in range(len(clients)):
		#company_idが一致する企業を取得
		company=Company.objects.values('name').filter(id=int(clients[i]["company_id"]))
		#companyのキーを新しく生成し、企業名を値とする
		clients[i]["company"]=company[0]["name"]
	#今日予定されている商談を取得
	business_talk = Business_talk.objects.all().values("name","stage_id","company_id","client_representive","date").filter(date=today)
	for i in range(len(business_talk)):
		#company_idが一致する企業を取得
		company=Company.objects.values('name').filter(id=int(business_talk[i]["company_id"]))
		#companyのキーを新しく生成し、企業名を値とする
		business_talk[i]["company"]=company[0]["name"]
		#ステージIDが一致するステージを取得
		stage_table = Business_talk_stage.objects.values("stage").filter(id=business_talk[i]["stage_id"])
		#stageのキーを新しく生成し、ステージ名を値とする
		business_talk[i]["stage"]=stage_table[0]["stage"]
	return clients,business_talk

#見込み客を表示する画面に遷移
def client(request):
	#検索用のラジオボタンとテキストボックスを準備
	form = forms.search_clients(request.GET or None)
	#ファイルインポート用のファイルフォームを取得
	form2 = forms.UploadFileForm2(request.POST or None)
	#見込み客を取得
	clients = Clients.objects.all().values("clients_name", "company_id","clients_mail","tel")
	for i in range(len(clients)):
		#company_idは一致する企業を取得
		company=Company.objects.values('name').filter(id=int(clients[i]["company_id"]))
		#companyのキーを新しく生成し、企業名を値とする
		clients[i]["company"]=company[0]["name"]
	#見込み客がいれば
	if clients.first() != None:
		return render(request,'login/future_client.html',{"clients":clients,"form":form,"form2":form2})

	#見込み客がいなければ
	content=[]
	
	return render(request,'login/future_client.html',{"clients":content,"form":form,"form2":form2})

#新しく見込み客を登録する画面に遷移
def create_client(request):
	#見込み客の情報を登録するためのフォームを準備
	form = forms.create_clients(request.GET or None)
	#indexがnullだとformの情報を受け取れないためとりあえず0を入れておく
	form = forms.create_clients(initial = {"index":0})
	return render(request,'login/new_future_client.html',{"form":form})

#登録した見込み客を保存する
def save_client(request):
	
	today=dt.datetime.now()
	#登録された見込み客の情報を受け取る
	form = forms.create_clients(request.POST)
	#フォームに正しい値が入力されていたら
	if form.is_valid():
		#企業名を取得
		company_name = form.cleaned_data["company"]
		#Companyテーブルの中から企業名が一致するレコードを取得
		company = Company.objects.filter(name=str(company_name))
		#レコードがなければ(登録されていない企業なら)
		if company.first() is None:
		#form = form.save()
			#新しい企業のレコードをinsert
			company_table = Company(name = form.cleaned_data["company"],
									mail = form.cleaned_data["mail"],
									tel = form.cleaned_data["TEL"],
									web_site_link = form.cleaned_data["web"],
									industry = form.cleaned_data["industry"],
									address = form.cleaned_data["address"],
									)
			#レコードを保存
			company_table.save()
		#入力されたステージIDと一致するステージを取得
		stage = Client_stage.objects.values('id').filter(stage=form.cleaned_data["stage"])
		#フォームから取得した企業名と一致するレコードのidを取得
		new_id = Company.objects.values('id').filter(name=company_name)
		#見込み客をinsert
		clients_table = Clients(clients_name=form.cleaned_data["name"],
		           company_id = new_id[0]["id"],
		           clients_mail=form.cleaned_data["mail"],
		           tel=form.cleaned_data["TEL"],
		           web_site_link=form.cleaned_data["web"],
		           stage_id=stage[0]["id"],
		           industry=form.cleaned_data["industry"],
		           annual_revenue=form.cleaned_data["revenue"],
		           accuracy=form.cleaned_data["accuracy"],
		           address=form.cleaned_data["address"],
		           memo1=form.cleaned_data["memo1"],
		           memo2=form.cleaned_data["memo2"],
		           )
		#レコードを保存
		clients_table.save()
		# form = form.save()
		
	

		

	return redirect('client')

#見込み客編集画面での更新を行う
def save_client2(request):
	
	today=dt.datetime.now()
	#登録された見込み客の情報を受け取る
	form = forms.create_clients(request.POST)
	#フォームに正しい値が入力されていれば
	if form.is_valid():
		#企業名を取得
		company_name = form.cleaned_data["company"]
		#Companyテーブルの中から企業名が一致するレコードを取得
		company = Company.objects.filter(name=str(company_name))
		#レコードがなければ(登録されていない企業なら)
		if company.first() is None:
		#form = form.save()
			#新しい企業のレコードをinsert
			company_table = Company(name = form.cleaned_data["company"],
									mail = form.cleaned_data["mail"],
									tel = form.cleaned_data["TEL"],
									web_site_link = form.cleaned_data["web"],
									industry = form.cleaned_data["industry"],
									address = form.cleaned_data["address"],
									)
			company_table.save()
		#入力されたステージIDと一致するステージを取得
		stage = Client_stage.objects.values('id').filter(stage=form.cleaned_data["stage"])
		#フォームから取得した企業名と一致するレコードのidを取得
		new_id = Company.objects.values('id').filter(name=company_name)
		#見込み客をupdate
		Clients.objects.filter(id=form.cleaned_data["index"]).update(clients_name=form.cleaned_data["name"],
																           company_id = new_id[0]["id"],
																           clients_mail=form.cleaned_data["mail"],
																           tel=form.cleaned_data["TEL"],
																           web_site_link=form.cleaned_data["web"],
																           stage_id=stage[0]["id"],
																           industry=form.cleaned_data["industry"],
																           annual_revenue=form.cleaned_data["revenue"],
																           accuracy=form.cleaned_data["accuracy"],
																           address=form.cleaned_data["address"],
																           memo1=form.cleaned_data["memo1"],
																           memo2=form.cleaned_data["memo2"],)
		# connection_table = Connection(clients_name=form.cleaned_data["name"],
		# form = form.save()
		
	

		

	return redirect('client')

#見込み客検索
def search_clients(request):
	#検索用のラジオボタンとテキストボックスを準備
	form = forms.search_clients(request.POST)
	#ファイルインポート用のファイルフォームを取得
	form2 = forms.UploadFileForm(request.POST or None)

	if form.is_valid():
		#ラジオボタンで選択された項目を取得
		r = form.cleaned_data["radio"]
		#検索ワードを取得
		search_word = form.cleaned_data["search_box"]
		#全て表示を選択したら
		if r == "all":
			return  redirect('client')
		#メールアドレスを選択したら
		elif r == "mail":
			#入力されたワードがメールアドレスに含まれているレコードを取得
			clients = Clients.objects.all().values("clients_name", "company_id","clients_mail","tel").filter(clients_mail__contains=search_word)
			for i in range(len(clients)):
				company=Company.objects.values('name').filter(id=int(clients[i]["company_id"]))
				clients[i]["company"]=company[0]["name"]
			if clients.first() != None:
				return render(request,'login/future_client.html',{"clients":clients,"form":form,"form2":form2})
		#企業名を選択したら
		elif r == "company_name":
			#入力されたワードが企業名に含まれているレコードを取得
			company_search = Company.objects.values('id').filter(name__contains=search_word)
			clients = Clients.objects.all().values("clients_name", "company_id","clients_mail","tel").filter(company_id=company_search[0]["id"])
			for i in range(len(clients)):
				company=Company.objects.values('name').filter(id=int(clients[i]["company_id"]))
				clients[i]["company"]=company[0]["name"]
			if clients.first() != None:
				return render(request,'login/future_client.html',{"clients":clients,"form":form,"form2":form2})
	content=[]
	return render(request,'login/contact_information.html',{"clients":content,"form":form,"form2":form2})
#見込み客編集画面に遷移
def edit_clients(request):
	if request.method == 'POST':
		count=0
		#どの行のボタンが押されたかを探索
		while True:
			if "edit_btn_"+str(count) in request.POST:
				btn_id = count
				break
			count+=1

		#ボタンが押された行の見込み客情報を取得
		clients = Clients.objects.filter(company_id=btn_id)
		company = Company.objects.values('name').filter(id = clients[0].company_id)
		stage = Client_stage.objects.values('stage').filter(id = clients[0].stage_id)
		#フォームの初期値をDBに保存されている情報にする
		form = forms.create_clients(initial = {"company" : company[0]["name"],
											   "TEL" : clients[0].tel,
											   "mail" : clients[0].clients_mail,
											   "web" : clients[0].web_site_link,
											   "stage" : stage[0]["stage"],
											   "accuracy" : clients[0].accuracy,
											   "name" : clients[0].clients_name,
											   "industry" : clients[0].industry,
											   "revenue" : clients[0].annual_revenue,
											   "address" : clients[0].address,
											   "memo1" : clients[0].memo1,
											   "memo2" : clients[0].memo2,
											   "index": clients[0].id

			})

	return render(request,'login/edit_future_client.html',{"form":form})
#見込み客を連絡先に追加する
def to_connection(request):
	today=dt.datetime.now()
	form = forms.create_clients(request.POST)

	if form.is_valid():
		company_name = form.cleaned_data["company"]
		company = Company.objects.filter(name=str(company_name))
		if company.first() is None:
			company_table = Company(name = form.cleaned_data["company"],
									mail = form.cleaned_data["mail"],
									tel = form.cleaned_data["TEL"],
									web_site_link = form.cleaned_data["web"],
									industry = form.cleaned_data["industry"],
									address = form.cleaned_data["address"],
									)
			company_table.save()
		stage = Client_stage.objects.values('id').filter(stage=form.cleaned_data["stage"])

		new_id = Company.objects.values('id').filter(name=company_name)
		#Connectionテーブルに見込み客情報をinsert
		connection_table = Connection(clients_name=form.cleaned_data["name"],
		           company_id = new_id[0]["id"],
		           clients_mail=form.cleaned_data["mail"],
		           tel=form.cleaned_data["TEL"],
		           web_site_link=form.cleaned_data["web"],
		           stage_id=stage[0]["id"],
		           industry=form.cleaned_data["industry"],
		           annual_revenue=form.cleaned_data["revenue"],
		           accuracy=form.cleaned_data["accuracy"],
		           address=form.cleaned_data["address"],
		           memo1=form.cleaned_data["memo1"],
		           memo2=form.cleaned_data["memo2"],
		           )
		connection_table.save()

		index = form.cleaned_data["index"]
		#連絡先に追加した見込み客情報をClientsテーブルから削除
		Clients.objects.filter(id=index).delete()
		# form = form.save()
		
	

		

	return redirect('client')

#連絡先情報を表示する画面
def connection(request):
	form = forms.search_clients(request.GET or None)
	form2 = forms.UploadFileForm(request.POST or None)
	#連絡先のレコードを取得
	connection = Connection.objects.all().values("clients_name", "company_id","clients_mail","tel")
	for i in range(len(connection)):
		#連絡先のcompany_idとCompanyテーブルのidが一致する企業名を取得
		company=Company.objects.values('name').filter(id=int(connection[i]["company_id"]))
		connection[i]["company"]=company[0]["name"]

	if connection.first() != None:
		return render(request,'login/contact_information.html',{"clients":connection,"form":form,"form2":form2})
	content=[]
	return render(request,'login/contact_information.html',{"clients":content,"form":form,"form2":form2})
#連絡先の検索を行う
def search_connection(request):
	form = forms.search_clients(request.POST)
	form2 = forms.UploadFileForm(request.POST or None)
	if form.is_valid():
		#ラジオボタンで選択された項目を取得
		r = form.cleaned_data["radio"]
		#検索されたワードを取得
		search_word = form.cleaned_data["search_box"]
		#全て表示を選んだら
		if r == "all":
			return  redirect('connection')
		#メールアドレスを選んだら
		elif r == "mail":
			#入力されたワードがメールアドレスに含まれているレコードを取得
			connection = Connection.objects.all().values("clients_name", "company_id","clients_mail","tel").filter(clients_mail__contains=search_word)
			for i in range(len(connection)):
				company=Company.objects.values('name').filter(id=int(connection[i]["company_id"]))
				connection[i]["company"]=company[0]["name"]
			if connection.first() != None:
				return render(request,'login/contact_information.html',{"clients":connection,"form":form,"form2":form2})
		#企業名を選んだら
		elif r == "company_name":
			#入力されたワードが企業名に含まれているレコードを取得
			company_search = Company.objects.values('id').filter(name__contains=search_word)
			connection = Connection.objects.all().values("clients_name", "company_id","clients_mail","tel").filter(company_id=company_search[0]["id"])
			for i in range(len(connection)):
				company=Company.objects.values('name').filter(id=int(connection[i]["company_id"]))
				connection[i]["company"]=company[0]["name"]
			if connection.first() != None:
				return render(request,'login/contact_information.html',{"clients":connection,"form":form,"form2":form2})
	content=[]
	return render(request,'login/contact_information.html',{"clients":content,"form":form,"form2":form2})
#メール送信画面へ遷移する
def create_mail(request):
	#メール送信に必要なフォームを準備(To,Cc,Bcc,件名,本文)
	form = forms.create_mail(request.GET or None)
	return render(request,'login/create_mail.html',{"form":form})
#メールを送信する
def send_email(request):
	# EMAIL = '7416094@gmail.com'
	# PASSWORD = 'asftozfjmvcixmzh'
	#ログインしているユーザーのidを取得
	user = request.session['id']
	#ログインしているユーザーのメールアドレスとアプリパスワードを取得
	mail_and_password = mail_password.objects.values('mail','password').filter(user_index=user)
	EMAIL = mail_and_password[0]["mail"]#メールアドレス
	PASSWORD = mail_and_password[0]["password"]#アプリパスワード
	form = forms.create_mail(request.POST)
	if form.is_valid():
		TO = form.cleaned_data["to"]#Toを指定
		
		cc = form.cleaned_data["cc"]#Ccを指定
		
		bcc = form.cleaned_data["bcc"]#Bccを指定
		
		msg = MIMEText(form.cleaned_data["text"])#本文を指定

		msg['Subject'] = form.cleaned_data["title"]#件名を指定
		msg['From'] = EMAIL
		msg['To'] = TO
		msg['Cc'] = cc
		msg['Bcc'] = bcc
		#,ごとにメールアドレスを分離
		sendTolist = TO.split(',') + cc.split(',') + bcc.split(',')
		s = smtplib.SMTP(host='smtp.gmail.com', port=587)
		s.starttls()
		s.login(EMAIL, PASSWORD)
		#メールの送信
		s.sendmail(EMAIL, sendTolist, msg.as_string())
		s.quit()
		# subject = "題名"
		# message = "本文\\nです"
		# from_email = '7416094@gmail.com'  # 送信者
		# recipient_list = ["7416094@ed.tus.ac.jp"]  # 宛先リスト
		# send_mail(subject, message, from_email, recipient_list)
		return redirect('connection')
#連絡先画面にファイルをインポートする
def file_import(request):
	if request.method == 'POST':
		form = forms.UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			if 'file' in request.FILES:
				#フォームで取得したファイルを保存する関数
				#保存したファイルをpandasで読み込んだものを返す
				df = handle_uploaded_file(request.FILES['file'])
				#カラムごとに格納
				clients_name = df.loc[:,"clients_name"]
				company_name = df.loc[:,"company"]
				clients_mail = df.loc[:,"clients_mail"]
				tel = df.loc[:,"tel"]
				web_site_link = df.loc[:,"web_site_link"]
				stage_id = df.loc[:,"stage_id"]
				accuracy = df.loc[:,"accuracy"]
				industry = df.loc[:,"industry"]
				revenue = df.loc[:,"annual_revenue"]
				address = df.loc[:,"address"]
				memo1 = df.loc[:,"memo1"]
				memo2 = df.loc[:,"memo2"]
				#csvファイルの情報を一つずつConnectionテーブルに保存する
				for i in range(len(df)):

					company = Company.objects.filter(name=str(company_name[i]))

					if company.first() is None:
						company_table = Company(name = company_name[i],
												mail = clients_mail[i],
												tel = tel[i],
												web_site_link = web_site_link[i],
												industry = industry[i],
												address = address[i],
												)
						company_table.save()
					new_id = Company.objects.values('id').filter(name=company_name[i])
					connection = Connection.objects.filter(company_id=new_id[0]["id"])

					if connection.first() is None:
						connection_table = Connection(clients_name=clients_name[i],
					           						  company_id = new_id[0]["id"],
					           						  clients_mail=clients_mail[i],
					           						  tel=tel[i],
					           						  web_site_link=web_site_link[i],
					           						  stage_id=stage_id[i],
					           						  industry=industry[i],
					           						  annual_revenue=revenue[i],
					           						  accuracy=accuracy[i],
					           						  address=address[i],
					           						  memo1=memo1[i],
					           						  memo2=memo2[i],
					           						)
						connection_table.save()
				return redirect('connection')
			#ファイルが選択されていなかったらエラー文を返す
			else:
				form = forms.search_clients(request.GET or None)
				form2 = forms.UploadFileForm(request.POST or None)
				error = "ファイルを選択してください"
				connection = Connection.objects.all().values("clients_name", "company_id","clients_mail","tel")
				for i in range(len(connection)):
					company=Company.objects.values('name').filter(id=int(connection[i]["company_id"]))
					connection[i]["company"]=company[0]["name"]

				if connection.first() != None:
					return render(request,'login/contact_information.html',{"clients":connection,"form":form,"form2":form2,"error":error})
				content=[]
				return render(request,'login/contact_information.html',{"clients":content,"form":form,"form2":form2,"error":error})
def handle_uploaded_file(f):
    path = os.path.join(UPLOAD_DIR, f.name)
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    df = pd.read_csv(path)
    return df
#連絡先編集画面に遷移
def edit_connection(request):
	if request.method == 'POST':
		count=0
		#どの行の編集ボタンが押されたか選択
		while True:
			if "edit_btn_"+str(count) in request.POST:
				btn_id = count
				break
			count+=1

	connection = Connection.objects.filter(company_id=btn_id)
	company = Company.objects.values('name').filter(id = connection[0].company_id)
	stage = Client_stage.objects.values('stage').filter(id = connection[0].stage_id)
	#フォームの初期値をDBに保存されている情報にする
	form = forms.create_clients(initial = {"company" : company[0]["name"],
										   "TEL" : connection[0].tel,
										   "mail" : connection[0].clients_mail,
										   "web" : connection[0].web_site_link,
										   "stage" : stage[0]["stage"],
										   "accuracy" : connection[0].accuracy,
										   "name" : connection[0].clients_name,
										   "industry" : connection[0].industry,
										   "revenue" : connection[0].annual_revenue,
										   "address" : connection[0].address,
										   "memo1" : connection[0].memo1,
										   "memo2" : connection[0].memo2,
										   "index" : connection[0].id

		})
	return render(request, 'login/edit_connection.html', {'form': form})
#連絡先を編集しupdate
def save_connection(request):
	form = forms.create_clients(request.POST)

	if form.is_valid():
		company_name = form.cleaned_data["company"]
		company = Company.objects.filter(name=str(company_name))
		if company.first() is None:
		#form = form.save()
			company_table = Company(name = form.cleaned_data["company"],
									mail = form.cleaned_data["mail"],
									tel = form.cleaned_data["TEL"],
									web_site_link = form.cleaned_data["web"],
									industry = form.cleaned_data["industry"],
									address = form.cleaned_data["address"],
									)
			company_table.save()
		stage = Client_stage.objects.values('id').filter(stage=form.cleaned_data["stage"])

		new_id = Company.objects.values('id').filter(name=company_name)
		#連絡先をupdateする
		Connection.objects.filter(id=form.cleaned_data["index"]).update(clients_name=form.cleaned_data["name"],
																           company_id = new_id[0]["id"],
																           clients_mail=form.cleaned_data["mail"],
																           tel=form.cleaned_data["TEL"],
																           web_site_link=form.cleaned_data["web"],
																           stage_id=stage[0]["id"],
																           industry=form.cleaned_data["industry"],
																           annual_revenue=form.cleaned_data["revenue"],
																           accuracy=form.cleaned_data["accuracy"],
																           address=form.cleaned_data["address"],
																           memo1=form.cleaned_data["memo1"],
																           memo2=form.cleaned_data["memo2"],)
		# connection_table = Connection(clients_name=form.cleaned_data["name"],
		#            company_id = new_id[0]["id"],
		#            clients_mail=form.cleaned_data["mail"],
		#            tel=form.cleaned_data["TEL"],
		#            web_site_link=form.cleaned_data["web"],
		#            stage_id=form.cleaned_data["stage"],
		#            industry=form.cleaned_data["industry"],
		#            annual_revenue=form.cleaned_data["revenue"],
		#            accuracy=form.cleaned_data["accuracy"],
		#            address=form.cleaned_data["address"],
		#            memo1=form.cleaned_data["memo1"],
		#            memo2=form.cleaned_data["memo2"],
		#            )
		#
		# form = form.save()
	return redirect('connection')
#商談を表示する画面に遷移
def business_talk(request):
	form = forms.search_business_talk(request.GET or None)
	#商談情報を取得
	business_talk = Business_talk.objects.all().values("name", "company_id","mail","tel","complete")
	for i in range(len(business_talk)):
		company=Company.objects.values('name').filter(id=int(business_talk[i]["company_id"]))
		business_talk[i]["company"]=company[0]["name"]
	#商談情報があれば
	if business_talk.first() != None:
		return render(request,'login/business_talk_display.html',{"clients":business_talk,"form":form})
	#商談情報がなければ
	content=[]
	return render(request,'login/business_talk_display.html', {"clients":content,'form': form})
#新しく商談を作る画面に遷移
def create_business_talk(request):
	form = forms.create_business_talk(request.GET or None)
	return render(request,'login/create_business_talk.html', {'form': form})
#商談を保存する
def save_business_talk(request):
	if request.method == "POST":
		form = forms.create_business_talk(request.POST)
		if form.is_valid():
			company_name = form.cleaned_data["company"]
			company = Company.objects.filter(name=str(company_name))
			if company.first() is None:			
				company_table = Company(name = form.cleaned_data["company"],
										mail = form.cleaned_data["mail"],
										tel = form.cleaned_data["tel"],
										web_site_link = form.cleaned_data["web"],
										industry = form.cleaned_data["industry"],
										address = form.cleaned_data["address"],
										)
				company_table.save()
			# return render(request, 'login/log.html', {'log': form.cleaned_data["stage"]})
			new_id = Company.objects.values('id').filter(name=company_name)
			stage = Business_talk_stage.objects.values('id').filter(stage=form.cleaned_data["stage"])
			next_step = Business_talk_stage.objects.values('id').filter(stage=form.cleaned_data["next_step"])
			#フォームに入力された商談情報をinsert
			business_talk_table = Business_talk(name=form.cleaned_data["name"],
			           company_id = new_id[0]["id"],
			           tel=form.cleaned_data["tel"],
			           mail=form.cleaned_data["mail"],
			           client_representive=form.cleaned_data["client_name"],
			           web_site_link=form.cleaned_data["web"],
			           date=form.cleaned_data["date"],
			           stage_id=stage[0]["id"],
			           accuracy=form.cleaned_data["accuracy"],
			           next_step=next_step[0]["id"],
			           content=form.cleaned_data["content"],
			           memo1=form.cleaned_data["memo1"],
			           memo2=form.cleaned_data["memo2"],
			           complete=int(b),
			           )
			business_talk_table.save()
			return redirect('business_talk')
		return render(request, 'login/log.html', {'log': form})
#商談を検索する
def search_business_talk(request):
	form = forms.search_business_talk(request.POST)
	if form.is_valid():
		#選択されたラジオボタンの項目を取得
		r = form.cleaned_data["radio2"]
		#全て表示を選択したら
		if r == "all":
			return  redirect('business_talk')
		#完了を選択したら
		elif r == "complete":
			#completeが1(完了)のレコードを取得
			business_talk = Business_talk.objects.all().values("name", "company_id","mail","tel").filter(complete=1)
			for i in range(len(business_talk)):
				company=Company.objects.values('name').filter(id=int(business_talk[i]["company_id"]))
				business_talk[i]["company"]=company[0]["name"]
			if business_talk.first() != None:
				return render(request,'login/business_talk_display.html',{"clients":business_talk,"form":form})
		#未完了を選択したら
		else:
			#completeが0(未完了)のレコードを取得
			business_talk = Business_talk.objects.all().values("name", "company_id","mail","tel").filter(complete=0)
			for i in range(len(business_talk)):
				company=Company.objects.values('name').filter(id=int(business_talk[i]["company_id"]))
				business_talk[i]["company"]=company[0]["name"]
			if business_talk.first() != None:
				return render(request,'login/business_talk_display.html',{"clients":business_talk,"form":form})
	content=[]
	return render(request,'login/business_talk_display.html', {"clients":content,'form': form})
#完了ボタンが押されたら
def complete_business_talk(request):
	form = forms.search_business_talk(request.GET or None)
	if request.method == 'POST':
		count=0
		#どの行の完了ボタンが押されたか探索
		while True:
			if "edit_btn_"+str(count) in request.POST:
				btn_id = count
				break
			count+=1
		#completeを1(完了)にupdate
		Business_talk.objects.filter(company_id=btn_id).update(complete=1)
		
	return redirect("Business_talk")
#設定画面に遷移
def setting_password(request):
	form = forms.setting(request.GET or None)
	#セッションにidが入っていたら
	if 'id' in request.session:
		#ログインしているユーザーのidを取得
		user = request.session['id']
		#ログインしているユーザーのメールアドレスとアプリパスワードを取得
		users = mail_password.objects.values("mail","password").filter(user_index=user)
		#メールアドレスとアプリパスワードが保存されていれば
		if users.first() != None:
			#設定フォームの初期値を取得したｔメールアドレスとアプリパスワードに設定
			form = forms.setting(initial = {'mail':users[0]['mail'],'password':users[0]['password']})
	return render(request,'login/setting.html',{'form':form})
#メールアドレスとアプリパスワードを保存または更新する
def save_password(request):
	form = forms.setting(request.POST)
	if form.is_valid():
		if 'id' in request.session:
			user = request.session['id']
			check = mail_password.objects.values('user_index').filter(user_index=user)
			mail = form.cleaned_data["mail"]
			password = form.cleaned_data["password"]
			#ユーザーのメールアドレスなどが保存されていれば
			if check.first() != None:
				#update
				mail_password.objects.filter(id=user).update(mail=mail,password=password,user_index=user)
			#ユーザーのメールアドレスなどが保存されていなければ「
			else:
				#insert
				mail_and_password = mail_password(mail = mail,password=password,user_index=user)
				mail_and_password.save()

				
	# if 'id' in request.session:
	# 	user = request.session['id']
	# 	users = Users.objects.values("email").filter(id=user)
	# 	user2 = users[0]["email"]
	return redirect('setting_password')
#見込み客画面にcsvファイルをインポートする
def import_clients(request):
	if request.method == 'POST':
		form = forms.UploadFileForm2(request.POST, request.FILES)
		if form.is_valid():
			#ファイルが選択されていれば
			if 'file' in request.FILES:
				df = handle_uploaded_file2(request.FILES['file'])
				
				clients_name = df.loc[:,"clients_name"]
				company_name = df.loc[:,"company"]
				clients_mail = df.loc[:,"clients_mail"]
				tel = df.loc[:,"tel"]
				web_site_link = df.loc[:,"web_site_link"]
				stage_id = df.loc[:,"stage_id"]
				accuracy = df.loc[:,"accuracy"]
				industry = df.loc[:,"industry"]
				revenue = df.loc[:,"annual_revenue"]
				address = df.loc[:,"address"]
				memo1 = df.loc[:,"memo1"]
				memo2 = df.loc[:,"memo2"]
				
				for i in range(len(df)):

					company = Company.objects.filter(name=str(company_name[i]))

					if company.first() is None:
						company_table = Company(name = company_name[i],
												mail = clients_mail[i],
												tel = tel[i],
												web_site_link = web_site_link[i],
												industry = industry[i],
												address = address[i],
												)
						company_table.save()
					new_id = Company.objects.values('id').filter(name=company_name[i])
					clients = Clients.objects.filter(company_id=new_id[0]["id"])

					if clients.first() is None:
						clients_table = Clients(clients_name=clients_name[i],
					           						  company_id = new_id[0]["id"],
					           						  clients_mail=clients_mail[i],
					           						  tel=tel[i],
					           						  web_site_link=web_site_link[i],
					           						  stage_id=stage_id[i],
					           						  industry=industry[i],
					           						  annual_revenue=revenue[i],
					           						  accuracy=accuracy[i],
					           						  address=address[i],
					           						  memo1=memo1[i],
					           						  memo2=memo2[i],
					           						)
						clients_table.save()
				return redirect('client')
			#return render(request,'login/log.html',{"log":clients_name[0]})
			#ファイルが選択されていなければ
			else:
				error="ファイルを選択してください"
				form = forms.search_clients(request.GET or None)
				form2 = forms.UploadFileForm2(request.POST or None)

				clients = Clients.objects.all().values("clients_name", "company_id","clients_mail","tel")
				for i in range(len(clients)):
					company=Company.objects.values('name').filter(id=int(clients[i]["company_id"]))
					clients[i]["company"]=company[0]["name"]

				if clients.first() != None:
					return render(request,'login/future_client.html',{"clients":clients,"form":form,"form2":form2,"error":error})
				content=[]
				
				return render(request,'login/future_client.html',{"clients":content,"form":form,"form2":form2,"error":error})
						

			  # アップロード完了画面にリダイレクト
def handle_uploaded_file2(f):
    path = os.path.join(UPLOAD_DIR2, f.name)
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    df = pd.read_csv(path)
    return df
	
