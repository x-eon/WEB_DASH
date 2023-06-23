import os
import dash
import sqlite3 as sql
from dash import html, ctx, dcc, Input, Output, State, dash_table

import pandas as pd

class DataBase:

    def __init__(self, nameDB, nameTable):
        cleartable = False
        self.nameFiledb = nameDB + '.db'
        self.nameTable = nameTable
        fileName = False
        tabName = False
        if os.path.exists(self.nameFiledb) == True:  # если файл базы существует
            fileName = True
            tables = self.getTablesdb(self.nameFiledb)
            for tab in tables:  # проверка наличия таблицы
                if tab == nameTable:
                    tabName = True
                    break

        conn = sql.connect(self.nameFiledb, timeout=10)
        cur = conn.cursor()

        # если нет файла или таблицы
        if fileName == False: print('нет файла базы ', self.nameFiledb, ' создадим новый')
        if tabName == False: print('нет таблицы: "', nameTable, '" создадим новую')

        if fileName == False or tabName == False:
            cur.execute("CREATE TABLE IF NOT EXISTS " + nameTable +
                        " (n  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT," +
                        " user_id TEXT," +
                        " user_name TEXT," +
                        " wallet TEXT," +
                        " balance REAL," +
                        " pool_percent REAL," +
                        " income_period REAL," +
                        " income_cleane REAL," +
                        " profit_percent REAL," +
                        " commission REAL," +
                        " income_balance  REAL," +
                        " dt date not null DEFAULT CURRENT_DATE," +
                        " version int DEFAULT 1);")
            conn.commit()
        elif tabName and cleartable == True:  # удалить таблицу
            cur.execute("drop TABLE " + nameTable + ";")
            conn.commit()

    def getTablesdb(self, namedb):
        tables = []
        try:
            conn = sql.connect(namedb, timeout=10)
            cur = conn.cursor()
            sqlstr = "SELECT * FROM sqlite_master WHERE type='table'"
            tablesdb = cur.execute(sqlstr).fetchmany(100)
            for tab in tablesdb:
                tables.append(tab[1])
        except Exception as inst:
            print('error tabs', inst)
        return tables

    #def insTab(self, user_id, user_name, wallet, balance, pool_percent, income_period, income_cleane, profit_percent,commission, income_balance):

    def insTab(self, item):
        try:
            #item = [user_id, user_name, wallet, balance, pool_percent, income_period, income_cleane, profit_percent, commission, income_balance]
            conn = sql.connect(self.nameFiledb, timeout=10)
            cur = conn.cursor()
            cur.execute("INSERT INTO usertab VALUES(null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_DATE, 1);",item)
            conn.commit()
        except Exception as ex:
            print('error:', ex)

    def test_to_db(self):
        item = ['123456', 'test_name', 'koshel', 100, 222, 43, 43, 12, 2,32]
        return item

    def selTab(self, sqlstr, size):
        conn = sql.connect(self.nameFiledb, timeout=10)
        cur = conn.cursor()
        return cur.execute(sqlstr).fetchmany(size)

    def getTabDF(self, nameTab):
        df = pd.DataFrame()
        if os.path.exists(self.nameFiledb) == True:  # если файл базы существует
            conn = sql.connect(self.nameFiledb, timeout=10)
            df = pd.read_sql('SELECT * FROM ' + nameTab, conn)   #.fetchmany(size)

        return df

    def getValue(self, tabname, column, value, size):
        try:
            conn = sql.connect(self.nameFiledb, timeout=10)
            cur = conn.cursor()
            value1 = value.replace("'", "''")
            sqlstr = "SELECT " + column + " FROM " + tabname + " WHERE " + column + " = " + "'" + value1 + "';"
            res = cur.execute(sqlstr).fetchmany(size)
        except Exception as inst:
            print('error', inst)
        return res

    def clearTable(self, nameTable):
        conn = sql.connect(self.nameFiledb, timeout=10)
        cur = conn.cursor()
        cur.execute("drop TABLE " + nameTable + ";")
        conn.commit()

    def testDublicate(self, tabname, column, value):
        res = False
        val = self.getValue(tabname, column, value, 1)
        if len(val) > 0:
            res = True
        return res

class UsersTable:

    def  dataTable(self):
        _columns = ['one', 'two', 'tree']
        _data = pd.DataFrame([[1,2,3],[1,2,3],[1,2,3]])
        dict_data = _data.to_dict()
        data_dash = self.maketTable(_columns, dict_data)
        print('data:',data_dash)
        return data_dash

    def maketTable(self, _columns, dict_data):
        _tab = dash_table.DataTable(
            id='tab-interactiv',
            columns=_columns,
            data=dict_data,
            editable=True,
            fill_width=False,
            sort_action="native",
            sort_mode="multi",
            column_selectable="multi",  # "single",
            row_selectable="single",
            row_deletable=True,
            selected_rows=[],
            page_action="native",
            page_current=0,
            page_size=12,
            style_header={'backgroundColor': 'black', 'color': 'yellow', 'border': '1px solid gray'},
            style_data={'backgroundColor': 'black', 'color': 'silver', 'whiteSpace': 'normal',
                        'height': 'auto', 'lineHeight': '18px', 'border': '1px solid gray'},
            style_cell={'textAlign': 'left', 'overflow': 'hidden', 'textOverflow': 'ellipsis'},
            # style_cell_conditional=[
            #     {'if': {'column_id': 'Num'}, 'maxWidth': 45},
            #     {'if': {'column_id': 'UserID'}, 'maxWidth': 80},
            #     {'if': {'column_id': 'UserName'}, 'maxWidth': 120},
            #     {'if': {'column_id': 'type'}, 'maxWidth': 80},
            #     {'if': {'column_id': 'Case'}, 'maxWidth': 80},
            #     {'if': {'column_id': 'InCase'}, 'maxWidth': 80},
            #     {'if': {'column_id': 'InDateCase'}, 'maxWidth': 80},
            #     {'if': {'column_id': 'OutCase'}, 'maxWidth': 80},
            #     {'if': {'column_id': 'OutDateCase'}, 'maxWidth': 80},
            #     {'if': {'column_id': 'Other'}, 'maxWidth': 300},
            #     {'if': {'column_id': 'dt'}, 'maxWidth': 50},
            #     {'if': {'column_id': 'version'}, 'maxWidth': 20},
            # ],
            style_as_list_view=False,
        )
        return _tab

class WebServer:

    def __init__(self):

        self.dict_settings = {}
        self.folder_path = os.path.dirname(os.path.realpath(__file__))
        self.load_set()
    #    self.db = DataBase('trading_bot', 'usertab')

   #     df = self.db.getTabDF('usertab')
        #print('df:',df)

     #   self.db.test_to_db()
        #item = ['123456', 'test_name', 'koshel', 100, 222, 43, 43, 12, 2, 32]

        self.utab = UsersTable()

        app = dash.Dash()
        self.out_mode = 'orders'
        self.app = app
        self.card_list = []
        self.bal_val = 100
        self.pnl_val1 = 10
        self.order_count1 = 300
        self.date_val = '01.06.2023-03.06.2023'
        self.cicle_num = 3
        self.pnl_val2 = 5
        self.order_count2 = 100
        self.page()
        self.add_num = 0

        @app.callback(
            Output("multy-block", "children"),
            [Input("button-setting", "n_clicks"),
             Input("button-orders", "n_clicks"),
             Input("button-users", "n_clicks"),
             Input("button-add", "n_clicks")],
             suppress_callback_exceptions=True
        )
        def selector(setting_clicks,orders_clicks,users_clicks,add_clicks):
            # {'name': 'BTC', 'Open': '1d12h23m5s','Step': '2' + ' ' + 'Short','PNL': '12' + '$','Balance': '-12' + '$', 'Set': '1/2/3/4/5' }
            res = self.orders()
            print('>> ',setting_clicks,'|',orders_clicks,'|',users_clicks,'[',ctx.triggered_id,']',add_clicks)
            print('selector ctx',ctx.triggered[0]['prop_id'],ctx.triggered,ctx.states)

            if ctx.triggered_id == "button-setting":
                res = self.setting()
            elif ctx.triggered_id == "button-orders":
                res = self.orders()
            elif ctx.triggered_id == "button-users":
                res = self.users()
            return res

        @app.callback(
            Output("button-add", "n_clicks"),
            [Input("button-add", "n_clicks")],
            suppress_callback_exceptions = True
        )
        def add_card(add_clicks):
            name = 'BTC'
            open = '1d12h23m5s'
            step = 2
            order_type = 'Short'
            pnl = 12
            balance = -12
            set = '1/2/3/4/5'
            print('add_clicks',add_clicks)
            if add_clicks != None:
                card = self.card_pattern(name, open, step, order_type, pnl, balance, set)
                gen_card = self.generate_card(app, card)
                self.card_list.append(gen_card)

        # ==================== block 2 ===============================
        @app.callback(
            Output("button-start", "n_clicks"),
            Input("button-start", "n_clicks"),
            prevent_initial_call=True
        )
        def but_start(n_clicks):
            print('button-start:', n_clicks)
            return 0

        @app.callback(
            Output("button-stop", "n_clicks"),
            Input("button-stop", "n_clicks"),
            suppress_callback_exceptions=True
        )
        def but_stop(n_clicks):
            print('button-stop:', n_clicks)
            return 0

        @app.callback(
            Output("button-pause", "n_clicks"),
            Input("button-pause", "n_clicks"),
            suppress_callback_exceptions=True
        )
        def but_pause(n_clicks):
            print('button-pause:', n_clicks)
            return 0

        #----------------- SETT ----------------------
        @app.callback(
            Output('save-btn', "n_clicks"),
            [Input('save-btn', "n_clicks"),
             Input('settings-box', "value")],
             prevent_initial_call=True,
            # suppress_callback_exceptions=True
        )
        def save_setings(n_clicks,set_values):
           # print('set_values:', type(set_values),set_values)

            lst_sett = set_values.split('\n')
            print('save lst',lst_sett)
            self.saveFile('settings.txt',lst_sett)
            #self.recognize_set(set_values)
            return 0




        # ---------------------------------------
        app.run_server(debug=True)

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def generate_buttons(self, app, num):
        # Создаем кнопку с текстом
        btn = html.Button('X', id=f"button-{num}")
        # Создаем колбэк для каждой кнопки
        @app.callback(
            Output(f"button-{num}", "n_clicks"),
            [Input(f"button-{num}", "n_clicks")],
            suppress_callback_exceptions=True
        )
        # Функция-колбэк, которая меняет стиль кнопки при клике на нее
        def update_button_style(n_clicks):
            button_id = ctx.inputs_list[0]['id']
            print('GEN_ctx:',button_id,self.card_list)
            #print('CARD:', self.card_list[button_id])
            return 0

        return btn

    # Создаем список с данными для карточек
    def card_pattern(self, name,open,step,order_type,pnl,balance,set):
        res =  {'title': name,
                'Open': open,
                'Step':str(step)+' '+order_type,
                'PNL':str(pnl)+'$',
                'Balance':str(balance)+'$',
                'Set':set
                }
        return res

    # Создаем функцию для формирования карточек
    def generate_card(self, app, card):
        but_num = f"button-{self.add_num}"
        res = html.Div([
            html.Div([
                html.H2(card['title']),
                html.Div('.'),
                html.Div('.'),
                #html.Button('[X]', id="button-X"),
                self.generate_buttons(app, self.add_num)
            ],style={'columnCount': 4,'height': '40px'}),

            html.Div('Open: '+card['Open']),
            html.Div('Step: '+card['Step']),
            html.Div('PNL: ' + card['PNL']),
            html.Div('Balance: ' + card['Balance']),
            html.Div('Set: ' + card['Set']),
            html.Div('______________________'),
            html.Div([
                html.Div('Black list?'),
                html.Button('yes', id=f"button-{self.add_num}")
            ], style={'columnCount': 2, 'height': '40px','margin-left': '16px'}),
        ],style={'width': '46mm', 'height': '45mm', 'border': '1px solid black', 'padding': '5px','margin-left': '5px'})
        self.add_num = self.add_num + 1
        return res

    # Создаем макет страницы с таблицей карточек
    #-----------------------------------------------

    def top_sect1(self):
        res = html.Div([
            html.Div(html.H3('Баланс: '+str(self.bal_val)+' $',style={'margin-left': '10px'}),style={'height': 56,'border': '1px solid black'}),
            html.Div(html.H3('PNL: '+str(self.pnl_val1)+' $',style={'margin-left': '10px'}),style={'height': 56,'border': '1px solid black'}),
            html.Div(html.H3('Количество сделок: '+str(self.order_count1),style={'margin-left': '10px'}),style={'height': 56,'border': '1px solid black'}),
            ])
        return res

    def top_sect2(self):
        res = html.Div([
            html.Div(html.H3('Цикл №: ' + str(self.cicle_num),style={'margin-left': '10px'}),style={'height': 41,'border': '1px solid black'}),
            html.Div(html.H3('Дата: '+str(self.date_val),style={'margin-left': '10px'}),style={'height': 41,'border': '1px solid black'}),
            html.Div(html.H3('PNL: '+str(self.pnl_val2)+' $',style={'margin-left': '10px'}),style={'height': 41,'border': '1px solid black'}),
            html.Div(html.H3('Количество сделок: '+str(self.order_count2),style={'margin-left': '10px'}),style={'height': 41,'border': '1px solid black'})
            ])
        return res

    def top_sect3(self):
        res = html.Div([
            html.Br(),
            html.Button('Запустить', id="button-start",style={'width': '60mm','height': '40px'}),
            html.Br(),
            html.Button('Остановить', id="button-stop",style={'width': '60mm','height': '40px'}),
            html.Br(),
            html.Button('Пауза', id="button-pause",style={'width': '60mm','height': '40px'}),
            ],style={'textAlign': 'center', 'border': '2px solid black', 'height': 166,'width': 260})
        return res

#==============================================================================================================================
    def page(self):
        # Создаем макет страницы с 4 блоками
        #for val in range(3):
        self.app.layout = html.Div([
                html.Div([
                    html.Div([self.block1()], style={'display': 'inline-block'}),
                    html.Div([self.block2()], style={'display': 'inline-block', 'margin-left': '0px'}),
                    # , 'vertical-align': 'top'
                ], style={'columnCount': 2, 'height': '200px', 'vertical-align': 'top', 'width': 700, 'margin-left': '0px'}),
                html.Div([
                    html.Div([self.block3()],
                             style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '0px', }),
                    html.Div(id='multy-block',
                             style={'display': 'inline-block', 'margin-left': '5px'})
                ], style={'columnCount': 2, 'margin-left': '0px', 'height': '400px', 'width': '680px',
                          'vertical-align': 'top'}),
               html.Div([
                   dcc.Textarea(id='settings-box', value='', style={'height': 1, 'width': 1}),
                   html.Button('', id='save-btn', style={'width': 1, 'height': 1}),
                   html.Div(id='users-block', style={'width': 1, 'height': 1})
                 #  html.Div(id='orders-block', style={'width': 1, 'height': 1})
               ],id='mult-block'),
               html.Div([self.GetData()])
            ]
        )

    def GetData(self):
        _data = self.getData()
        _names = [{'id': c, 'name': c} for c in _data.columns]
        self._oldDataTabe = self.utab.maketTable(_names, _data.to_dict('records'))
        print('maket:', len(self._oldDataTabe.data), self._oldDataTabe)
        return self._oldDataTabe

    def getData(self):

        lst = [{'id':12345,'name':'ivan','curence':1234},{'id':65845,'name':'fedja','curence':75859}]


        df = pd.DataFrame(lst)


        #if theme == 'theme': theme = 'common'
        #db = DataBase('iskin', 'PSYCHO')
        #tab = self.getTabDF('PSYCHO', gender, group, size)
       # print('DATA:',tab)

        return df

    def getTabDF(self, nameTab, gender, group, size):
        df = pd.DataFrame()
        # if os.path.exists(self.nameFiledb) == True:  # если файл базы существует
        #     conn = sqlite3.connect(self.nameFiledb, timeout=10)
        #     df = pd.read_sql('SELECT * FROM ' + nameTab, conn)   #.fetchmany(size)

        return df
#===========================================================================================================================
    def block1(self):
        # Создаем блок 1
        res = html.Div([html.Button('test ADD', id="button-add",style={'width': '60mm','height': '40px'})],
            style={'width': '380px', 'height': '180px', 'padding': '5px', 'margin-left': '5px', 'margin-top': '5px'}
        )
        return res

        # Создаем блок 2
    def block2(self):
        res = html.Div([
            html.Div([self.top_sect1()],style={'width': '100%', 'margin-top': '0px','margin-left': '0px','border': '1px solid black',}),
            html.Div([self.top_sect2()],style={ 'width': '100%','margin-top': '0px','margin-left': '0px','border': '1px solid black',}),
            html.Div([self.top_sect3()],style={'width': '100%', 'margin-top': '0px','margin-left': '0px','border': '1px solid black',})
        ],style={'height':'180px','width':'822px','padding':'5px','margin-left':'5px','margin-top': '5px','columnCount': 3,})
        return res

    def block3(self):
        # Создаем блок 3
        res = html.Div([
            html.Div([
                html.Br(),
                html.Button('Настройки', id="button-setting",style={'width': '74mm','height': '60px'}),
                html.Br(),
                html.Button('Сделки', id="button-orders",style={'width': '74mm','height': '60px'}),
                html.Button('Юзеры', id="button-users",style={'width': '74mm','height': '60px'}),
                html.Br(),
            ], style={'margin-left': '30px','textAlign': 'center', 'width': '90px',}),
            #html.Div(id='settings_box')
        ],style={'width':'90mm','height':'1000px','border':'1px solid black','padding':'5px','margin-left':'10px','margin-top':'5px'})
        return res

    def __setting_list(self):
            xx = """
            Clean_star = True – чистый запуск (стираем кэш)
            Api_key = “” ключ
            Api_secret = “” секрет
            Trade_long = False – направление торговли всех пар
            Trade_short = True – направление торговли всех пар

            Auto_cancel_order =120 – автоотмена первого ордера в setka_1, задается в секундах.

            Grid1_vol = 100 – обьем первичной сетки в $
            Numb_grid = 15 – количество ордеров в сетках ( минимально 1 , максимально 10 )
            Mult1 = 1 – множитель кол-ва в первичной сетке, задаётся числовым значением с шагом 0.1
            Leverage_size – размер торгового плеча
            Grid1_profit =  5 – размер в %-ах тейк-профит для первого маркетного ордера в сетках
            Close_profit = 2  - общая прибыль ($) в режиме проторговки для закрытия позиций.
            Step – шаг задаваемый в %-ах, для расстояния между ордерами
            Mult_vol – множитель объёма в торговых сетках, задаётся числовым значением с шагом 0.1
            Mult_Step – множитель step, задаётся числовым значением с шагом 0.1
        
            Pair_limit =100 – количество торговых пар разрешённых к одновременной торговле
            Cycle_limit = 20– лимит торговых пар которые могут открываться одновременно
            Cycle_timer=45m – время в минутах, в течении которого новые позиции не будут открываться если условия цикла выполнены.

            order_vol= 70 – обьем основного ореда в %-ах. Минимальное значение 50. При значении 100, устанавливается один ордер

            Whitelist = [‘BTC’, ‘ETH’,….] -  список торговых пар по которым разрешено открытие новых позиций.
            Blacklist – список торговых пар по которым запрещено открытие новых позиций. При добавлении в список открытой позиции, алгоритм прекращает с ней работу.

            """

            dict_lst = html.Div("""""")

            return dict_lst
    def setting_default(self):

        res = """
        Clean_star =  True\n
        Api_key = .....\n
        Api_secret = ....\n
        Trade_long = False\n
        Trade_short = True\n
        Auto_cancel_order = 120\n
        Grid1_vol = 100\n
        Numb_grid = 15\n
        Mult1 = 1\n
        Leverage_size = 0\n
        Grid1_profit = 5\n
        Close_profit = 2\n
        Step = 1\n
        Mult_vol = 1\n
        Mult_Step = 1\n
        Pair_limit = 100\n
        Cycle_limit = 20\n
        Cycle_timer = 45\n
        order_vol = 70
        """
        return res

    def setting(self):
        res = html.Div([
            html.Label('Список торгуемых инструментов'),
            dcc.Input(id='Whitelist_box', value='BTC, ETH, XMR, XRP, BUSD, USDT', placeholder='Список торгуемых инструментов',
                      style={'color':'darkgreen','height': 40,'width': 400}),
            html.Div(style={'height': 6,'width': 404, 'margin-left': '0px'}),
            html.Label('Список блокированных инструментов'),
            dcc.Input(id='Blacklist_box',  value='LEO, ETC, TUSD, BCH, CRO, ARB', placeholder='Список блокированных инструментов',
                      style={'color':'darkred','height': 40, 'width': 400}),
            html.Div(style={'height': 6,'width': 404, 'margin-left': '0px'}),
            dcc.Textarea(id='settings_box', value=self.load_set(), placeholder='settings',
                         style={ 'height': 640,'width': 400}),
            html.Div(style={'height': 6,'width': 404, 'margin-left': '0px'}),
            html.Div([
                html.Button('default', id='default-btn', n_clicks=0, style={'height': 40, 'width': 120}),
                html.Button('cancel', id='cancel-btn', n_clicks=0, style={'height': 40,'width': 120}),
                html.Button('save', id='save-btn', n_clicks=0, style={'height': 40, 'width': 120}),
            ], style={'columnCount': 3, 'height': 46,'width': 404, 'margin-left': '0px'}),
        ], id='setting-block',
           style={'display': 'flex','flex-wrap': 'wrap', 'border': '1px solid black',
                  'padding': '5px', 'margin-left': '15px','margin-top': '5px' ,'height': 840,'width': 404})
        return res

    def orders(self):
        res = html.Div(children = self.card_list,
                       id='orders-block',
                       style={'display': 'flex', 'flex-wrap': 'wrap', 'border': '1px solid black',
                              'padding': '5px', 'margin-left': '15px', 'margin-top': '5px','width': 1148})
        return res

    def users(self):
        tab = self.utab.dataTable()
        res = html.Div(children = tab, id='users-block', style={'display': 'flex', 'flex-wrap': 'wrap', 'border': '1px solid black','padding': '5px', 'margin-left': '15px', 'margin-top': '5px'})
        return res

    def loadFile(self, filename):
        if os.path.exists(self.folder_path+'\\'+filename):
            res = ''
            with open(self.folder_path+'\\'+filename, 'r', encoding='utf8') as file:
                line = file.readlines()
                for _str in line:
                    res = res + _str + "\n"
            return res
        else:
            return 'no file: '+filename

    def saveFile(self, filename, set_values):
        with open(self.folder_path+'\\'+filename, 'w', encoding='utf8') as file:
            for _str in set_values:
                if _str != '':
                    res = _str + "\n"
                    file.write(res)

    def load_set(self):
        params = self.loadFile('settings.txt')
        print('load_set:', params)
        if 'no file' in params:
            params = self.setting_default()
        else:
            self.dict_settings = self.recognize_set(params)
        return params

    def recognize_set(self, params):
        par_list = params.split("\n")
        print('par_list:', par_list)
        for sett in par_list:
            try:
                if sett !="":
                    param = sett.split('=')
                   # print('sett', sett,'param',param)
                    self.dict_settings.update({param[0]:param[1]})
            except Exception as ex:
                print('ошибка параметра:',sett,ex)
        print('>>> ',self.dict_settings)

#-------------------------------------------------------------------------

def getData():

    lst = [{'id': 12345, 'name': 'ivan', 'curence': 1234}, {'id': 65845, 'name': 'fedja', 'curence': 75859}]

    df = pd.DataFrame(lst)

    #_names = [{'id': c, 'name': c} for c in _data.columns]
    # self._oldDataTabe = self.utab.maketTable(_names, _data.to_dict('records'))
    # print('maket:', len(self._oldDataTabe.data), self._oldDataTabe)

    return df

#--------------------------------------------------------------------------

if __name__ == '__main__':
    ws = WebServer()

