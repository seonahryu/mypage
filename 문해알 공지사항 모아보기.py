from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import webbrowser
from bs4 import BeautifulSoup
import requests

class Notice:
    def __init__(self, window):
        self.window = window
        self.window.title('SungKyunKwan University Notice')
        self.window.geometry('350x400')

        Label(self.window, text='').pack()

        frame=Frame(self.window, relief='solid', width=50) #frame의 width 조절 어떻게 해??
        frame.pack()

        Label(frame, text='Category', font=('Arial', 15, 'bold')).pack()

        
        self.category = IntVar()
        #Radiobutton(self.window, text='전체', value=10, variable=self.category).grid(row=1, column=0)
        Radiobutton(frame, text='학사', value=0, variable=self.category).pack()
        Radiobutton(frame, text='입학', value=1, variable=self.category).pack()
        Radiobutton(frame, text='취업', value=2, variable=self.category).pack()
        Radiobutton(frame, text='채용/모집', value=3, variable=self.category).pack()
        Radiobutton(frame, text='장학', value=4, variable=self.category).pack()
        Radiobutton(frame, text='행사/세미나', value=5, variable=self.category).pack()
        Radiobutton(frame, text='일반', value=6, variable=self.category).pack()

        Label(self.window, text='').pack()

        Label(self.window, text='Homepage', font=('Arial', 15, 'bold')).pack()

        Label(self.window, text='SKKU / SW / SCO', font=('Arial', 12)).pack()
        self.home_select=Entry(self.window)
        self.home_select.pack()

        links={'SKKU':'https://www.skku.edu/skku/campus/skk_comm/notice01.do?mode=list&&articleLimit=10&article.offset=',
               'SW':'https://sw.skku.edu/sw/notice.do?mode=list&&articleLimit=10&article.offset=',
               'SCO':'https://sco.skku.edu/sco/community/notice.do?mode=list&&articleLimit=10&article.offset='}
        #SKKU, Skku, sKku 등 이런 변수들 다 같은걸로 취급하려고 lower()나 upper() 함수 쓰려고 하는데 어떻게 해야하지??

        Label(self.window, text='').pack()
        Button(self.window, text='Search', command=lambda: self.error_msg() or self.notice(links[self.home_select.get()])).pack()
        #homepage error messagebox -> self.error_msg()

        Label(self.window, text='').pack()
        Button(self.window, text='Chatbot', command=self.chatbot).pack()

    def error_msg(self):
        if self.home_select.get() not in ['SKKU', 'SW', 'SCO']:
            messagebox.showerror('Error', '홈페이지명을 다시 입력해주십시오.')
            self.home_select.delete(0, END)
            

    def notice(self, link):
        nw = Toplevel()
        nw.title(f'{self.home_select.get()} Notice')
        nw.geometry('350x400')

        academics = []
        admissions = []
        employment = []
        recruitment = []
        scholarship = []
        events = []
        general = []
        title_lst = [academics, admissions, employment, recruitment, scholarship, events, general]

        academics_link = []
        admissions_link = []
        employment_link = []
        recruitment_link = []
        scholarship_link = []
        events_link = []
        general_link = []
        link_lst = [academics_link, admissions_link, employment_link, recruitment_link, scholarship_link, events_link, general_link]

        for i in range(0, 3):
            #홈페이지 1~3페이지 크롤링
            num = i * 10
            url = requests.get(f"{link}{num}")
            soup = BeautifulSoup(url.text, "html.parser")
            # html.parser : HTML 문법 규칙을 바탕으로 웹페이지의 내용을 해석하고, 의미와 구조를 분석하는 프로그램
            all_notices = soup.find_all('dt', "board-list-content-title")
            
            """
            <dt class="board-list-content-title ">
				<span class="c-board-list-category">[일반]</span>
                <a href="?mode=view&amp;articleNo=110739&amp;article.offset=0&amp;articleLimit=10" title="자세히 보기">
                    [자과캠] 도로 및 주차장 환경개선에 따른 도색 작업 시행 안내(11/18~11/19)
                </a>	
            </dt>
            """

            for dt in all_notices:
                a_tag = dt.find('a')
                href = a_tag['href']
                if a_tag:
                    text_a = a_tag.get_text(strip=True)
                    # strip=True : 앞뒤 공백 문자, 개행 문자 등 삭제하고 텍스트만 가져오도록

                type_span = dt.find("span", "c-board-list-category")
                if type_span:
                    type_text = type_span.get_text(strip=True)

                    if type_text == '[학사]':
                        academics.append(text_a)
                        academics_link.append(href)
                    if type_text == '[입학]':
                        admissions.append(text_a)
                        admissions_link.append(href)
                    if type_text == '[취업]':
                        employment.append(text_a)
                        employment_link.append(href)
                    if type_text == '[채용/모집]':
                        recruitment.append(text_a)
                        recruitment_link.append(href)
                    if type_text == '[장학]':
                        scholarship.append(text_a)
                        scholarship_link.append(href)
                    if type_text == '[행사/세미나]':
                        events.append(text_a)
                        events_link.append(href)
                    if type_text == '[일반]':
                        general.append(text_a)
                        general_link.append(href)

        self.error_nan(title_lst, self.category.get())
        # 해당 카테고리에 해당하는 공지사항이 없는 경우, error messagebox

        Label(nw, text=f'{self.home_select.get()} Notice {type_text}', font=('Arial', 15, 'bold')).pack()
        Label(nw, text='').pack()
        #nw에 어느 홈페이지의 어떤 category인지 Label 붙여주자!!

        self.button_attach(nw, title_lst, link_lst, self.category.get())
        self.home_select.delete(0, END) #'Notice' 창 열리면 Entry에 썼던 내용 삭제되도록


    def error_nan(self, title_lst, category):
        if len(title_lst[category])==0:
            messagebox.showerror('NaN', '해당 카테고리에 해당하는 공지사항이 존재하지 않습니다.')
        
    def button_attach(self, web, title_lst, link_lst, category):
        title = title_lst[category]
        link = link_lst[category]
        n = len(title)

        homepage_urls = {
            'SKKU': 'https://www.skku.edu/skku/campus/skk_comm/notice01.do',
            'SW': 'https://sw.skku.edu/sw/notice.do',
            'SCO': 'https://sco.skku.edu/sco/community/notice.do'
            }

        homepage_url = homepage_urls[self.home_select.get()]

        def link_web(i):
            full_url = f'{homepage_url}{link[i]}'
            webbrowser.open(full_url)

        for i in range(n):
            Button(web, text=title[i], command=lambda i=i: link_web(i), width=40).pack()
            """
            lambda i=i : 
            syntax for optional parameters. 
            Optional parameters’ defaults are evaluated when the functions themselves are evaluated,
            so making the default for the parameter i the current value of i solves the problem of the i taking on a different value later.
            """

    def chatbot(self):
        webbrowser.open('https://discord.com/oauth2/authorize?client_id=1173280356326182953&permissions=8&scope=bot')

if __name__ == "__main__":
    tk = Tk()
    app = Notice(tk)
    tk.mainloop()
