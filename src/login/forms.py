from django import forms
# from .models import Clients
# class Clients(forms.ModelForm):
	# class Meta:
	# 	model = Clients
	# 	fields = ['clients_name','company_id','clients_mail','tel','web_site_link','stage_id','industry',
	# 		'annual_revenue','accuracy','address','memo1','memo2']
	# 	labels = {
	# 			'clients_name':'担当者',
	# 			'company_id':'会社名',
	# 			'clients_mail':'mail',
	# 			'tel':'TEL',
	# 			'web_site_link':'WEB',
	# 			'stage_id':'ステージ',
	# 			'industry':'業界',
	# 			'accuracy':'確度',
	# 			'annual_revenue':'想定収益',
	# 			'address':'住所',
	# 			'memo1':'メモ1',
	# 			'memo2':'メモ2'
	# 	}
	# 	widgets = {
	# 			'company_id':forms.TextInput(),
	# 			'tel':forms.TextInput(),
	# 			'clients_mail':forms.EmailInput(),
	# 			'web_sit_link':forms.TextInput(),
	# 			'stage_id':forms.TextInput(),
	# 			# 'accuracy':forms.TextInput(),
	# 			'clients_name':forms.TextInput(),
	# 			'industry':forms.TextInput(),
	# 			'annual_revenue':forms.TextInput(),
	# 			'address':forms.TextInput(),
	# 			'memo1':forms.Textarea(attrs={'cols':70,'rows':10}),
	# 			'memo2':forms.Textarea(attrs={'cols':70,'rows':10})

	# 	}
EMPTY_CHOICES = (
    ('', '-'*10),
)

CHOICES = (
    ('連絡済み', '連絡済み'),
    ('今後対応', '今後対応'),
    ('連絡不要','連絡不要'),
    ('失注','失注'),
    ('完了','完了'),
)
# CHOICES2 = (
#     ('check_conditions', '条件確認'),
#     ('needs_analysis', 'ニーズ分析'),
#     ('proposal','提案'),
#     ('decision_making','意思決定'),
#     ('estimate','見積り'),
#     ('negotiation','交渉'),
#     ('orders','受注'),
#     ('Forfeit','失注'),
# )
CHOICES2 = (
    ('条件確認', '条件確認'),
    ('ニーズ分析', 'ニーズ分析'),
    ('提案','提案'),
    ('意思決定','意思決定'),
    ('見積り','見積り'),
    ('交渉','交渉'),
    ('受注','受注'),
    ('失注','失注'),
)
class login(forms.Form):
    user_id = forms.CharField(
        label='ユーザーID',
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder':"ユーザーID"})
    )
    password = forms.CharField(
        label='パスワード',
        max_length=10,
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder':"パスワード"})
    )
class create_clients(forms.Form):
    index = forms.IntegerField()
    company = forms.CharField(
        label='会社名',
        max_length=20,
        required=True,
        widget=forms.TextInput()
    )
    TEL = forms.CharField(
        label='TEL',
        max_length=20,
        required=True,
        widget=forms.TextInput()
    )
    mail = forms.EmailField(
        label='mail',
        required=True,
        widget=forms.EmailInput()
    )
    web = forms.CharField(
        label='WEB',
        max_length=50,
        required=True,
        widget=forms.TextInput()
    )
    # stage = forms.CharField(
    #     label='ステージ',
    #     max_length=10,
    #     required=True,
    #     widget=forms.TextInput()
    # )
    stage = forms.ChoiceField(
        label='ステージ',
        widget=forms.Select,
        choices=EMPTY_CHOICES + CHOICES,
        required=True,
    )
    accuracy = forms.CharField(
        label='確度',
        max_length=10,
        required=True,
        widget=forms.TextInput()
    )
    name = forms.CharField(
        label='担当者',
        max_length=10,
        required=True,
        widget=forms.TextInput()
    )
    industry = forms.CharField(
        label='業界',
        max_length=10,
        required=True,
        widget=forms.TextInput()
    )
    revenue = forms.CharField(
        label='想定収益',
        max_length=10,
        required=True,
        widget=forms.TextInput()
    )
    address = forms.CharField(
        label='住所',
        max_length=50,
        required=True,
        widget=forms.TextInput()
    )
    memo1 = forms.CharField(
        label='メモ1',
        max_length=50,
        required=True,
        widget=forms.Textarea(attrs={'cols':70,'rows':10})
    )
    memo2 = forms.CharField(
        label='メモ2',
        max_length=50,
        required=True,
        widget=forms.Textarea(attrs={'cols':70,'rows':10})
    )
class search_clients(forms.Form):
	radio = forms.ChoiceField(
		label="search",
        widget=forms.RadioSelect,
        choices=(('all','全て表示'),('mail', 'メールアドレス'),('company_name','会社名')),
        initial= 'all',
        required=True,)
	search_box = forms.CharField(
        max_length=20,
        widget=forms.TextInput(),
        required=False,
    )

class create_mail(forms.Form):
    to = forms.CharField(
        label='TO:',
        required=True,
        max_length=80,
        #width=500px,
        widget=forms.TextInput()
    )
    cc = forms.CharField(
        label='CC:',
        required=False,
        max_length=80,
        #width=500px,
        widget=forms.TextInput()
    )
    bcc = forms.CharField(
        label='BCC:',
        required=False,
        max_length=80,
        #width=500px,
        widget=forms.TextInput()
    )
    title = forms.CharField(
        label='件名:',
        required=True,
        max_length=80,
        #width=500px,
        widget=forms.TextInput()
    )
    text = forms.CharField(
        label='本文',
        max_length=50,
        required=True,
        widget=forms.Textarea(attrs={'cols':30,'rows':50})
    )


class UploadFileForm(forms.Form):
    file  = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'accept':'.csv'})
        )
class UploadFileForm2(forms.Form):
    file  = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'accept':'.csv'})
        )
class search_business_talk(forms.Form):
    # radio = forms.ChoiceField(
    #     label="search",
    #     widget=forms.RadioSelect,
    #     choices=(('all','全て表示'),('business_talk_name', '商談名'),('clients_name','クライアント名')),
    #     initial= 'all',
    #     required=True,)
    radio2 = forms.ChoiceField(
        label="search",
        widget=forms.RadioSelect,
        choices=(('all','全て表示'),('complete','完了'),('not_complete','未完了')),
        initial='all',
        required=True,)
    # search_box = forms.CharField(
    #     max_length=20,
    #     widget=forms.TextInput(),
    #     required=False,
    # )

class create_business_talk(forms.Form):
    # index = forms.IntegerField()
    name = forms.CharField(
        label='商談名',
        max_length=30,
        required=True,
        widget=forms.TextInput()
    )
    company = forms.CharField(
        label='会社名',
        max_length=20,
        required=True,
        widget=forms.TextInput()
    )
    mail = forms.EmailField(
        label='mail',
        required=True,
        widget=forms.EmailInput()
    )
    tel = forms.CharField(
        label='TEL',
        max_length=20,
        required=True,
        widget=forms.TextInput()
    )
    client_name = forms.CharField(
        label='担当者',
        max_length=20,
        required=True,
        widget=forms.TextInput()
    )
    web = forms.CharField(
        label='WEB',
        max_length=50,
        required=True,
        widget=forms.TextInput()
    )
    stage = forms.ChoiceField(
        label='ステージ',
        widget=forms.Select,
        choices=EMPTY_CHOICES + CHOICES2,
        required=True
    )
    accuracy = forms.CharField(
        label='確度',
        max_length=10,
        required=True,
        widget=forms.TextInput()
    )
    next_step = forms.ChoiceField(
        label='ネクストステップ',
        widget=forms.Select,
        choices=EMPTY_CHOICES + CHOICES2,
        required=True
    )
    date = forms.DateTimeField(label='商談日時',
                               required=True,
                               input_formats=['%Y-%m-%d %H:%M'],
                               initial="2019-09-01 03:00"
                            )
    content = forms.CharField(
        label='商談内容',
        max_length=50,
        required=True,
        widget=forms.Textarea(attrs={'cols':70,'rows':10})
    )
    memo1 = forms.CharField(
        label='メモ1',
        max_length=50,
        required=True,
        widget=forms.Textarea(attrs={'cols':70,'rows':10})
    )
    memo2 = forms.CharField(
        label='メモ2',
        max_length=50,
        required=True,
        widget=forms.Textarea(attrs={'cols':70,'rows':10})
    )

class setting(forms.Form):
    # index = forms.IntegerField()
    mail = forms.EmailField(
        label='メールアドレス',
        max_length=30,
        required=True,
        widget=forms.EmailInput()
    )
    password = forms.CharField(
        label='password',
        max_length=30,
        required=True,
        widget=forms.TextInput()
    )