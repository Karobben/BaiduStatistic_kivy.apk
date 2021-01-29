#!/usr/bin/env python3
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.network.urlrequest import UrlRequest
#from kivy_garden.wordcloud import WordCloud

# kivy font name
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path
resource_add_path("./font")
LabelBase.register(DEFAULT_FONT, 'FZZhuoYTJW_Zhong.ttf')


# Clipboard
Clipboard = None
from kivy.core.clipboard import Clipboard

# Else
import time, json
TIME =time.strftime("%Y%m%d", time.localtime())


from BarChart import BarChart


class HomePanel(BoxLayout):
	ID = str('000')
	token = open('Token.log','r').read().replace('\n','')

	def build(self):
		orientation = 'vertical'
		spacing = 10

	def Token(self):
		token = Clipboard.paste()
		f = open('Token.log','w')
		f.write(token)
		f.close()
		self.run()

	def ID_get(self):
		TOKEN = self.token
		url1 = "https://openapi.baidu.com/rest/2.0/tongji/config/getSiteList?access_token="
		url = url1+ TOKEN
		request = UrlRequest(url, self.ID_result, verify =False)

	def ID_result(self, request, data):
		try:
			Data = json.loads(data)
			ID = Data["list"][0]['site_id']
			#print(Date)
		except:
		    ID = 'Error: 001; Can\'t access Page ID'
		self.ID = str(ID)
		#print("\n\n\n\nLook here: ", ID)
		self.run()

	def Key_words(self):
		TOKEN = self.token
		url1 = "https://openapi.baidu.com/rest/2.0/tongji/report/getData?access_token="
		url2 = TOKEN +"&site_id="+self.ID+"&start_date=20200122"
		url3 = "&end_date=" + TIME + "&metrics=pv_count&method=source%2Fsearchword%2Fa"
		url = url1+url2+url3
		request = UrlRequest(url, self.Key_words_show, verify =False)

	def Key_words_show(self, request, data):
		try:
			Data = json.loads(data)
			#print("\n\n\n\nLook here: ", Data)
			#Data = ('??')#str(Data['result']['items'][0])
			Data = Data['result']['items'][0]
			Result = []
			for i in Data:
				Result += [i[0]['name']]
			#print("\n\n\n\n\n\n\n\nResult is Result", Result)
		except:
		    Result = ['Error 003; Go check the New_visitor_show()']
		print(Result)
		#self.Body_panel.visit_num.text = str(Num)#Location
		#self.Body_panel.new_visitor.text = str(Data)#Location
		'''
		wc = WordCloud(
		    label_options=dict(
		        font_size=15,
		        padding=(1, 1),
		    ),
		    label_cls='CloudLabel',
		    words = Result,
			size = self.size,
			pos  = self.pos
		)
		'''
		self.Body_panel.key_words.text = "\n".join(Result)

	def New_visitor(self):
		TOKEN = self.token
		url1 = "https://openapi.baidu.com/rest/2.0/tongji/report/getData?access_token="
		url2 = TOKEN +"&site_id="+self.ID+"&start_date=" + str(int(TIME) - 6)
		url3 = "&end_date="+TIME+"&metrics=new_visitor_ratio&method=source%2Fall%2Fa"
		url = url1+url2+url3
		request = UrlRequest(url, self.New_visitor_show, verify =False)
		#text = arg1.text
		#self.Body_panel.visit_num.text = 'loading...'
		self.Body_panel.new_visitor.text = 'loading...'

	def New_visitor_show(self, request, data):
		try:
			Data = json.loads(data)
			#print("\n\n\n\nLook here: ", Data)
			Data = str(Data['result']['pageSum'][0][0])+"%"
		except:
		    Data = 'Error 003; Go check the New_visitor_show()'

		#self.Body_panel.visit_num.text = str(Num)#Location
		self.Body_panel.new_visitor.text = str(Data)#Location

	def Visited_page(self):
		TOKEN = self.token
		url1 = "https://openapi.baidu.com/rest/2.0/tongji/report/getData?access_token="
		url2 = TOKEN +"&site_id="+self.ID+"&start_date="
		url3 = TIME + "&end_date="+TIME+"&metrics=pv_count%2Caverage_stay_time&method=visit%2Ftoppage%2Fa"
		url = url1+url2+url3
		request = UrlRequest(url, self.Visited_page_show, verify =False)
		#text = arg1.text
		#self.Body_panel.visit_num.text = 'loading...'
		self.Body_panel.visited_page.text = 'loading...'

	def Visited_page_show(self, request, data):
		try:
			Data = json.loads(data)
			#print("\n\n\n\nLook here: ", Data)
			Data = Data['result']
			'''
			for i, ii  in zip(Data['result']['items'][0], Data['result']['items'][1]):
			    tmp = i[0]['name']+"    |    "+ str(ii[0])
			    dist = len(i[0]['name']) - len(str(ii[0]))
			    if dist>0:
			        tmp +=" " * dist*4
			    elif dist<0:
			        tmp = " "*abs(dist) + tmp
			    Location += "\n" + tmp
			'''
			Result = Data['items']
			Page = ''
			Num = ''
			for i in Result[0]:
			    Page += i[0]['name'].replace('https://karobben.github.io/','').replace('https://karobben.github.io','Home') + '\n'
			for i in Result[1]:
				    Num += ' '.join(['Num:',str(i[0]),'Time:',str(i[1]), '\n'])
		except:
		     Page = 'Error: 002; cant find visited pages'

		#self.Body_panel.visit_num.text = str(Num)#Location
		self.Body_panel.visited_page.text = str(Page)#Location

	def Country_count_all(self):
	    TOKEN = self.token
	    url1 = "https://openapi.baidu.com/rest/2.0/tongji/report/getData?access_token="
	    url2 = TOKEN +"&site_id=" + self.ID+ "&start_date=20200122"
	    url3 = "&end_date="+TIME+"&metrics=pv_count&method=visit%2Fworld%2Fa"
	    url = url1+url2+url3
	    request = UrlRequest(url, self.Country_count_all_show, verify =False)
	    self.Body_panel.country_all.text = "loading..."

	def Country_count_all_show(self, request, data):
		Location = ""
		Num = 0
		try:
			Data = json.loads(data)
			for i, ii  in zip(Data['result']['items'][0], Data['result']['items'][1]):
				tmp = i[0]['name']+": "+ str(ii[0])
				Location +=  tmp + "\n"
				Num += ii[0]
		except:
			pass
		self.Body_panel.country_all.text = Location
		self.Body_panel.history_all_vist.text = str(Num)

	def Recent_visit(self):
	    TOKEN = self.token
	    url1 = "https://openapi.baidu.com/rest/2.0/tongji/report/getData?access_token="
	    url2 = TOKEN +"&site_id=" + self.ID+ "&start_date=" + str(int(TIME)-13)
	    url3 = "&end_date="+TIME+"&metrics=pv_count&method=overview%2FgetTimeTrendRpt"
	    url = url1+url2+url3
	    request = UrlRequest(url, self.Recent_visit_show, verify =False)

	def Recent_visit_show(self, request, data):
		try:
			Data = json.loads(data)
			Data = Data['result']["items"][1]
			List = []
			for i in Data:
				List += [i[0]]
			Box = BarChart()
			Box.List = List
			self.Body_panel.visit_line.clear_widgets()
			self.Body_panel.visit_line.add_widget(Box)
		except:
			pass

	def Country_count(self):
	    TOKEN = self.token
	    url1 = "https://openapi.baidu.com/rest/2.0/tongji/report/getData?access_token="
	    url2 = TOKEN +"&site_id=" + self.ID + "&start_date="
	    url3 = TIME + "&end_date="+TIME+"&metrics=pv_count&method=visit%2Fworld%2Fa"
	    url = url1+url2+url3
	    request = UrlRequest(url, self.Country_count_show, verify =False)
	    #text = arg1.text
	    #self.Body_panel.contry.text = "loading..."
	    self.Body_panel.today_vist.text = 'loading...'

	def Country_count_show(self, request, data):
		try:
			Data = json.loads(data)
			Location = []
			for i in Data['result']['items'][0]:
				Location += [i[0]['name']]
			Location_N = []
			Num = 0
			for i in Data['result']['items'][1]:
				Location_N += [str(i[0])]
				Num += i[0]
			Result = ""
			for i, ii in zip(Location, Location_N):
				Result += i+': '+str(ii)+'\n'
			Location = Result
		except:
			Location = ""
			Num = "Waiting for..."
		self.Body_panel.country_today.text = Location
		self.Body_panel.today_vist.text = str(Num)

	def Province_count(self):
	    TOKEN = self.token
	    url1 = "https://openapi.baidu.com/rest/2.0/tongji/report/getData?access_token="
	    url2 = TOKEN +"&site_id=" + self.ID + "&start_date="
	    url3 = TIME + "&end_date="+TIME+"&metrics=pv_count&method=overview%2FgetDistrictRpt"
	    url = url1+url2+url3
	    request = UrlRequest(url, self.Province_count_show, verify =False)
	    #text = arg1.text
	    self.Body_panel.provinves_today.text = "loading..."

	def Province_count_show(self, request, data):
		try:
			Data = json.loads(data)
			Location = []
			for i in Data['result']['items'][0]:
			    Location += [i[0]]
			Location_N = []
			for i in Data['result']['items'][1]:
				Location_N += [str(i[0])]
			Result = ""
			for i, ii in zip(Location, Location_N):
				Result += i+': '+str(ii)+'\n'
			Location = Result
		except:
			Location= "Come on..."

		self.Body_panel.provinves_today.text = Location

	def Comes_from(self):
		TOKEN = self.token
		url1 = "https://openapi.baidu.com/rest/2.0/tongji/report/getData?access_token="
		url2 = TOKEN +"&site_id=" + self.ID + "&start_date=20200122"
		url3 = "&end_date="+TIME+"&metrics=pv_count&method=source%2Flink%2Fa"
		url = url1+url2+url3
		request = UrlRequest(url, self.Comes_from_show, verify =False)
		#text = arg1.text
		self.Body_panel.comes_from.text = "loading..."

	def Comes_from_show(self, request, data):
		try:
			Data = json.loads(data)
			Data_n = Data['result']['items'][1]
			Data_s = Data['result']['items'][0]
			Result = {}
			for i in range(len(Data_n)):
				Result.update({Data_s[i][0]['name']:Data_n[i][0]})
			# Result Clean
			Result_clean = []
			for i in Result.keys():
				if "192." not in i and '127.0' not in i:
					site = i.replace("https://",'').replace("http://",'').replace("www.",'')
					Result_clean += [str(Result[i])+": "+site]
			Result = "\n".join(Result_clean)
		except:
			Result= "Error 007"

		self.Body_panel.comes_from.text = Result

	def Search_engine(self):
		TOKEN = self.token
		url1 = "https://openapi.baidu.com/rest/2.0/tongji/report/getData?access_token="
		url2 = TOKEN +"&site_id=" + self.ID + "&start_date=20200122"
		url3 = "&end_date="+TIME+"&metrics=pv_count&method=source%2Fengine%2Fa&area="
		url = url1+url2+url3
		request = UrlRequest(url, self.Search_engine_show, verify =False)
		#text = arg1.text
		self.Body_panel.search_engine.text = "loading..."

	def Search_engine_show(self, request, data):
		try:
			Data = json.loads(data)
			#try:
			Data_n = Data['result']['items'][1]
			Data_s = Data['result']['items'][0]
			Result = {}
			for i in range(len(Data_n)):
				Result.update({Data_s[i][0]['name']:Data_n[i][0]})
			# Result Clean
			Result_clean = []
			for i in Result.keys():
				if "192." not in i and '127.0' not in i:
					site = i.replace("https://",'').replace("http://",'').replace("www.",'')
					Result_clean += [str(Result[i])+": "+site]
			Result = "\n".join(Result_clean)
		except:
			Result = "Error: 13"

		self.Body_panel.search_engine.text = Result

	def run(self):
		self.token = open('Token.log','r').read().replace('\n','')
		self.Key_words()
		self.Visited_page()
		self.New_visitor()
		self.Country_count_all()
		self.Recent_visit()
		self.Country_count()
		self.Province_count()
		self.Comes_from()
		self.Search_engine()

	def __init__(self,**kwargs):
		def run():
			self.Visited_page()
			self.Country_count_all()
			self.Country_count()
			self.Province_count()

		super().__init__(**kwargs)
		# First layer
		#self.token = '121.357b1b69c96ff6c52ad67bf3b224a533.YD3yNXcprY4kFbz1_P8oiyKaX6TrALBy1glHGlD.QnVW1g'

		Body_panel = open("main.kv",'r').read()
		self.Body_panel = Builder.load_string(Body_panel)
		self.add_widget(self.Body_panel)

		self.ID_get()

		#self.Body_panel.visited_page.text = 'updating...'
		self.Body_panel.refresh_b.on_release = self.run
		self.Body_panel.token_sub.on_release = self.Token
		print()
		#self.Body_panel.visit_line.point = [0, 0, self.width, self.height]

		'''
		self.Visited_page()
		self.Country_count_all()
		self.Country_count()
		self.Province_count()
		Body Layer
		Scroll_test = ScrollView(size_hint=(1, None), size=(1000, 100))
		Scroll_test.add_widget(Label(text='10000\n'*100))
		Scroll_test.do_scroll = True


		self.Body_p =  MDBoxLayout(size_hint=(1, 10))

		Body_panel = open("layout/Body_panel.kv",'r').read()
		self.Body_panel = Builder.load_string(Body_panel)
		self.Body_p.add_widget(self.Body_panel)

		Tail_p =  MDBoxLayout(size_hint=(1, 2))
		Tail   = open('layout/Tail_banner.kv','r').read()
		self.Tail_banner = Builder.load_string(Tail)
		Tail_p.add_widget(self.Tail_banner)
		Tail_p.add_widget(Scroll_test)
		#Tail_p.add_widget(Button_fresh)

		# adding to the main panel
		self.add_widget(Header_p)
		self.add_widget(self.Body_p)
		self.add_widget(Tail_p)
		'''


class MainApp(MDApp):
    def build(self):
        self.Main = HomePanel()
        return self.Main



#Window.size = (1920/2, 1080/2)
if __name__ == '__main__':
    MainApp().run()
