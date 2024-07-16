import streamlit as st
# from streamlit_modal import Modal   
# from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import pandas as pd
import pandas_market_calendars as mcal
# import numpy as np
import yfinance as yf

import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
import pyrebase
from firebase_admin import db
# from collections import OrderedDict
# import pytz 
import datetime
# import time
# import json
# import matplotlib.pyplot as plt
# import numpy as np
# from marketwatch import MarketWatch
# import requests
# from bs4 import BeautifulSoup
# from pandas_datareader import data as pdr
# from pandas_datareader.yahoo.options import Options 

if not firebase_admin._apps:
    cred = credentials.Certificate('optionssim-473a4-4d9f929e1d77.json') 
    #Firebase requires authenatication to access its services
    default_app = firebase_admin.initialize_app(cred, {'databaseURL': 'https://optionssim-473a4-default-rtdb.firebaseio.com'}) 
    #In streamlit you need to initialise the web app, and this is how you do it. You also initialise the revelant databases, used in the code.

firebaseConfig = {
  'apiKey': "AIzaSyBEXJOZUxxZYRX-uvi0yHAaSC5uKWc-gP8",
  'authDomain': "optionssim-473a4.firebaseapp.com",
  'databaseURL': "https://optionssim-473a4-default-rtdb.firebaseio.com",
  'projectId': "optionssim-473a4",
  'storageBucket': "optionssim-473a4.appspot.com",
  'messagingSenderId': "130784006614",
  'appId': "1:130784006614:web:4fe5c17e07ad5e25b45477",
  'measurementId': "G-R4QV9BKD1Y"
}

firebase = pyrebase.initialize_app(firebaseConfig) #Initialis config
authSignIn = firebase.auth()
ref = db.reference('/')


calendar = mcal.get_calendar("NYSE")
#print(calendar.tz.zone)

now = datetime.datetime.now()
#print(now)
nowDate = datetime.datetime.today()
schedule = calendar.schedule(start_date='2023-01-01', end_date='2025-12-25')
#print(schedule)

isMarketOpen = calendar.open_at_time(schedule, pd.Timestamp(now, tz='Europe/London') )
#print(isMarketOpen)


df = pd.read_csv("fortune500stocks.csv")
# Create a DataFrame from the data

class SessionState:
    def __init__(self):
        self.logged_in = False
        self.freebalance_value = None

def loginsignup_page():
    global username
    st.image(image='Tradeblazer-removebg-preview.png')
    
    st.title("Login / Sign up Page")  
    choice = st.selectbox('Login or Sign Up', ["Login","Sign up"])
    #Title of the page and provides a selection box to pick between Login and Sign up
    

    if choice=="Sign up":
        
        st.subheader("Sign up")
        username = st.text_input("Enter unique username")
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        password2 = st.text_input("Enter Password again", type="password")
        #Asks for necessary Sign up details such as Username, Email and Password

        if st.button("Create account") and password==password2:
            user = auth.create_user(email = email, password =password, uid = username)
        
        #Once button is pressed, it creates a new user with their email, password and username they inputted

            user_data = {
                "userID" : username,
                "contracts": "",
                "valOfContracts" : 0,
                "freebalance": 10000,
                "invested": 0,
                "percentageChange": 0
               
            }

            #Data in JSON format for database, this will be all the relevant data for a trader.

            traders_ref = db.reference("traders")
            traders_ref.push().set(user_data)
            
            #Adds those keys as a child to the 'traders' key in the database.
            
            st.success("Account successfully created!")
            st.markdown("Please login using email and password")
            st.balloons()
        else: 
            st.write("Passwords do not match!")
        
    else:
        st.subheader("Login")
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password") 
        #Indicates with subheader that it is on Login page and outputs input fields for email and pw.

        if st.button("Login"):
            try:
                user = auth.get_user_by_email(email) #Obtains the email from database using the email inputted from user
                login = authSignIn.sign_in_with_email_and_password(email, password)
                st.session_state.username = user.uid 
                st.session_state.useremail = user.email
                st.session_state.logged_in = True #Useful for switching to main page

                #Obtains the username and email from session_state which is used to share variables in different pages for each user sesssion. 

                Usernm = user.uid
                st.write("Welcome",Usernm)

                if 'Usernm' not in st.session_state:
                    st.session_state['Usernm'] = Usernm
                st.session_state['Usernm'] = Usernm

                userData = ref.order_by_child('userID').equal_to(st.session_state.username).get()   
                for user_id, user_data in userData.items():
                    freebalance_value = user_data.get('freebalance', None)
                    invested_value = user_data.get('invested',None)
                    
                if 'freebalance_value' not in st.session_state:
                     st.session_state['freebalance_value'] = freebalance_value
                st.session_state['freebalance_value'] = freebalance_value 

                if 'invested_value' not in st.session_state:
                    st.session_state['invested_value'] = invested_value
                st.session_state['invested_value'] = invested_value


            except:
                st.warning("Login failed")
                
        # if st.button("Login"):
        #     try:
        #         user = auth.get_user_by_email
            
        
ref = db.reference("/traders")

# userData = ref.order_by_child('userID').equal_to(st.session_state.username).get()   
# for user_id, user_data in userData.items():
#     freebalance_value = user_data.get('freebalance', None)
#     invested_value = user_data.get('invested',None)
#     #st.write(freebalance_value)
#     print(invested_value)



def mainPage():
    st.title("Main page")
    #st.write(st.session_state.freebalance_value)
    
    # ref = db.reference("/traders")

    # userData = ref.order_by_child('userID').equal_to(usrnm).get()   
    # for user_id, user_data in userData.items():
    #     freebalance_value = user_data.get('freebalance', None)
    #     invested_value = user_data.get('invested',None)
    #     st.write(freebalance_value)
    #     st.write(invested_value)
    
    # st.write("### Free Balance " + str( "%.2f" % st.session_state.freebalance_value))
    # st.write("### Invested: " + str( "%.2f" % st.session_state.invested_value))
    
    userData = ref.order_by_child('userID').equal_to(st.session_state.username).get()   
    for user_id, user_data in userData.items():
        contracts = user_data.get('contracts', None)
    #Checks the json database to get the contract data, with all the info such as contract name, premium, bid ask etc.
      
    totalPnl = 0
    totalPnlAfterHours = 0
    allPositionsDf = pd.DataFrame(columns=['Contract', 'Current Price', 'Purchase Price', 'QTY', 'P/L', 'Percentage Change']) #Creates column names for the open positions
    allPositionsDfAfterHours = pd.DataFrame(columns=['Contract', 'Current Price', 'Purchase Price', 'QTY', 'P/L', 'Percentage Change']) #Creates column names 
    #if contracts != "": talk about how when all positions closed, this gave an error
    
    if 'contracts' not in user_data or contracts == "":
        st.write("Looks empty, go trade something!") 
    elif 'contracts' in user_data: #error if you put if

        for key, value in contracts.items():
            contractName = value['contractName']
            quantityContract = value['quantity']
            premiumContract = value['premiumPaid']
            symbolForPnL = contractName.split("2")[0]
            #Gets the corresponding values and the symbol

            contractForPnL = yf.Ticker(symbolForPnL)   
            optionChainForPnL = contractForPnL.option_chain()
            selectedRowCall = optionChainForPnL.calls[optionChainForPnL.calls['contractSymbol'] == contractName]
            selectedRowPut = optionChainForPnL.puts[optionChainForPnL.puts['contractSymbol'] == contractName]
            #Gets the chain for the corresponding contract

            if len(selectedRowCall.index) != 0:
                bidProfit = (selectedRowCall.iloc[0]['bid']) * quantityContract * 100 - premiumContract
                totalPnl += bidProfit
                lastPrice = (selectedRowCall.iloc[0]['lastPrice'])
                lastPriceProfit = lastPrice * quantityContract * 100 - premiumContract
                
                totalPnlAfterHours += lastPriceProfit #Calculates the total pnl after hours
                percentageChangeCallAfterHours = lastPriceProfit / premiumContract * 100
                percentageChangeCall = bidProfit / premiumContract * 100
                #Gets the data and calclates PnL and Pecentage Change

                #st.write(f"Percentage Change: {percentageChangeCall:.2f}%")

                if isMarketOpen == True:

                    positionData = {
                        'Contract' : contractName,
                        'Current Price' : (selectedRowCall.iloc[0]['bid']),
                        'Purchase Price' : value['purchasePrice'],
                        'QTY' : quantityContract,
                        'P/L' : bidProfit,
                        'Percentage Change' : "%.2f" % percentageChangeCall #two decimal places

                    }
                    #Creates Dictionary which we can then use o make a dataframe later. 

                    #st.dataframe(positionData) write about how this does not make it horiz
                    #positionDf =  pd.DataFrame.from_dict(positionData, orient='index').T
                    # st.dataframe(positionDf) talk about how this doesn't start at 1 and starts at 0
                    #st.dataframe(positionDf.rename(index=lambda x: x + 1))

                    allPositionsDf = allPositionsDf.append(positionData, ignore_index=True) #Appends each contract to the data frame
                else:
                    positionData = {
                        'Contract' : contractName,
                        'Current Price' : (selectedRowCall.iloc[0]['lastPrice']),
                        'Purchase Price' : value['purchasePrice'],
                        'QTY' : quantityContract,
                        'P/L' : lastPriceProfit,
                        'Percentage Change' : "%.2f" % percentageChangeCallAfterHours #two decimal places

                    }
                    allPositionsDfAfterHours = allPositionsDfAfterHours.append(positionData, ignore_index=True)
                    #st.dataframe(positionData) write about how this does not make it horiz
                    #positionDf =  pd.DataFrame.from_dict(positionData, orient='index').T
                    # st.dataframe(positionDf) talk about how this doesn't start at 1 and starts at 0
                    #st.dataframe(positionDf.rename(index=lambda x: x + 1))                   
                   

            if len(selectedRowPut.index) != 0:
                bidProfit = (selectedRowPut.iloc[0]['bid']) * quantityContract * 100 - premiumContract   
                totalPnl += (selectedRowPut.iloc[0]['bid']) * quantityContract * 100 - premiumContract
                lastPrice = (selectedRowPut.iloc[0]['lastPrice'])
                lastPriceProfit = lastPrice * quantityContract * 100 - premiumContract
                totalPnlAfterHours += lastPriceProfit
                percentageChangePutAfterHours = lastPriceProfit / premiumContract * 100
                percentageChangePut = bidProfit / premiumContract * 100    
                #st.write(f"Percentage Change: {percentageChangePut:.2f}%")
                
                if isMarketOpen == True:
                    positionData = {
                        'Contract' : contractName,
                        'Current Price' : (selectedRowPut.iloc[0]['bid']),
                        'Purchase Price' : value['purchasePrice'],
                        'QTY' : quantityContract,
                        'P/L' : bidProfit,
                        'Percentage Change' : "%.2f" % percentageChangePut #two decimal places

                    }
                    #st.dataframe(positionData) write about how this does not make it horiz
                    #positionDf =  pd.DataFrame.from_dict(positionData, orient='index').T
                    # st.dataframe(positionDf) talk about how this doesn't start at 1 and starts at 0
                    #st.dataframe(positionDf.rename(index=lambda x: x + 1))
                    allPositionsDf = allPositionsDf.append(positionData, ignore_index=True)
                    gd = GridOptionsBuilder.from_dataframe(allPositionsDf)
                    gd.configure_selection(selection_mode='multiple', use_checkbox=True)
                    gridoptions = gd.build()
                    


                else:
                    positionData = {
                        'Contract' : contractName,
                        'Current Price' : (selectedRowPut.iloc[0]['lastPrice']),
                        'Purchase Price' : value['purchasePrice'],
                        'QTY' : quantityContract,
                        'P/L' : lastPriceProfit,
                        'Percentage Change' : "%.2f" % percentageChangePutAfterHours #two decimal places

                    }
                    #st.dataframe(positionData) write about how this does not make it horiz
                    #positionDf =  pd.DataFrame.from_dict(positionData, orient='index').T
                    # st.dataframe(positionDf) talk about how this doesn't start at 1 and starts at 0
                    #st.dataframe(positionDf.rename(index=lambda x: x + 1))
                    allPositionsDfAfterHours = allPositionsDfAfterHours.append(positionData, ignore_index=True)

        
        if isMarketOpen == True:


            st.dataframe(allPositionsDf.rename(index=lambda x: x + 1))  

        else:
            st.dataframe(allPositionsDfAfterHours.rename(index=lambda x: x + 1)) 
            
            # st.dataframe(selectedRowCall)
            # st.dataframe(selectedRowPut)
            #st.write(contractName)

        investedPlusTotalPnl = st.session_state.invested_value + totalPnl
        totalPercentageReturn = (investedPlusTotalPnl/st.session_state.invested_value - 1) * 100
        investedPlusTotalPnlAfterHours = st.session_state.invested_value + totalPnlAfterHours
        totalPercentageReturnAfterHours = (investedPlusTotalPnlAfterHours/st.session_state.invested_value - 1) * 100

    #st.write(totalPnl)
        if isMarketOpen == True:
            st.write(f"P/L Open: {totalPnl:.2f}")   
            st.write(f"Total Value of all trades: {investedPlusTotalPnl}")
            st.write(f"Total Percentage Change: {totalPercentageReturn:.2f}%")

        else:
            st.write(f"P/L Open: {totalPnlAfterHours:.2f}")
            st.write(f"Total Value of all trades: {investedPlusTotalPnlAfterHours}")
            st.write(f"Total Percentage Change: {totalPercentageReturnAfterHours:.2f}%")

                         

        if 'totalPnl' not in st.session_state:
            st.session_state['totalPnl'] = totalPnl
        st.session_state['totalPnl'] = totalPnl  

        

        if isMarketOpen == False:
            #st.write(totalPnlAfterHours)

            pass 
        if 'investedPlusTotalPnl' not in st.session_state:
            st.session_state['investedPlusTotalPnl'] = investedPlusTotalPnl
        st.session_state['investedPlusTotalPnl'] = investedPlusTotalPnl

        # dataToPlotValue = investedPlusTotalPnl + st.session_state.freebalance_value

        # dataToPlotDf = pd.DataFrame(columns=['Time', 'Unrealized P/L'])
   

        # st.write(dataToPlotValue)
        


        selectedContractToClose = st.selectbox("Select contract to close", allPositionsDfAfterHours) # Creates select box
      

        userData = ref.order_by_child('userID').equal_to(usrnm).get()
        if st.button("Close"):
            for key,value in contracts.items():
                if value['contractName'] == selectedContractToClose:
                    st.session_state.invested_value -= value['premiumPaid']
                    selectedRowCloseContract = allPositionsDfAfterHours[allPositionsDfAfterHours['Contract'] == selectedContractToClose]
                    closeProfit = (selectedRowCloseContract.iloc[0]['P/L'])
                    st.session_state.freebalance_value += value['premiumPaid'] + closeProfit
                    #takes value away from invested value and adds to free balance, while calculating the profit
                    for user_id, user_data in userData.items():
                        ref.child(user_id).update({'freebalance': st.session_state.freebalance_value})
                        ref.child(user_id).update({'invested': st.session_state.invested_value})
                    #Updates the values
            for user_id, user_data in userData.items():
                if 'contracts' in user_data:
                    contractsInContracts = user_data['contracts']
                    if contractsInContracts:
                        for contract_id, contract_data in contractsInContracts.items():
                            if 'contractName' in contract_data and contract_data['contractName'] == selectedContractToClose:
                                ref.child(user_id).child('contracts').child(contract_id).delete()
            #Iterates through the database and deletes the contract and its children which is the values such as PnL, contract name etc.

                # if selectedContractToClose == user_data['contractName']:
                #     ref.child(user_id).child('contracts').delete()
      
    investedPlusFree = st.session_state.invested_value + st.session_state.freebalance_value
    realizedPercentageChange = ((investedPlusFree / 10000)- 1)  * 100
    print(realizedPercentageChange)
    for user_id, user_data in userData.items():
        ref.child(user_id).update({'percentageChange': realizedPercentageChange})
    #Realized percent change is the percent change of the whole 10,000 after you close your position, this 

            # if 'freebalance_value' not in st.session_state:
            #     st.session_state['freebalance_value'] = freebalance_value
            #st.session_state['freebalance_value'] = freebalance_value    





 
     
def stockSearcherPage():
    
    st.title("Fortune 500 Stock Search")

    # Search bar for filtering the selectbox options
    
    search_term = st.text_input("Search by Company Name or Symbol")
    filtered_options = df[df["Security"].str.contains(search_term, case=False) | df["Symbol"].str.contains(search_term, case=False)] 
    #Adds a search filter for easier searching, no need to search the whole thing / Partial search

    # Dropdown select box
    selected_stock = st.selectbox("Select a Stock", filtered_options["Symbol"])
    print(selected_stock)
    
    # url = f'https://finance.yahoo.com/quote/{selected_stock}/options?p={selected_stock}'
    # response = requests.get(url)
    # soup = BeautifulSoup(response.text, 'html.parser')
    # table = soup.find_all('table')[0]
    # testDf = pd.read_html(str(table))[0]
    # st.write(testDf)


    stockOption = yf.Ticker(selected_stock)
    expDates = stockOption.options
    # st.write(expDates)
    # yf.pdr_override()
    # expDates = pdr.Options(selected_stock)
    # data = pdr.get_data_yahoo(selected_stock, start='2020-01-01')
    # st.write(data)
    # st.write(expDates)
    # st.write(stockOption)
    # headers = {'User-Agent': 'Firefox'}
    # response = requests.get(f'https://query1.finance.yahoo.com/v6/finance/options/{selected_stock}', headers=headers).json()
    # #st.write(response)

    

    

    selectedExpDate = st.selectbox("Select an Expiration Date", expDates) #select box with expiration dates

    tradingViewWidget = f"""
<div style="display: flex; justify-content: center;">
    <!-- TradingView Widget BEGIN -->
<div class="tradingview-widget-container">
  <div class="tradingview-widget-container__widget"></div>
  <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/" rel="noopener nofollow" target="_blank"><span class="blue-text">Track all markets on TradingView</span></a></div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-mini-symbol-overview.js" async>
  {{
    "symbol": "{selected_stock}",
    "width": 350,
    "height": 220,
    "locale": "en",
    "dateRange": "12M",
    "colorTheme": "dark",
    "isTransparent": true,
    "autosize": false,
    "largeChartUrl": "",
    "noTimeScale": false,
    "chartOnly": false
  }}
  </script>
</div>
<!-- TradingView Widget END -->

"""
    st.components.v1.html(tradingViewWidget, height=220)
    
    # Display selected stock's information
    # selected_stock_info = df[df["Symbol"] == selected_stock]
    # print(selected_stock_info)
    # st.write("Selected Stock Information:")
    # st.dataframe(selected_stock_info)

    st.write("Call Options") #Title 
    options = stockOption.option_chain(date=selectedExpDate) #Gets the chains
    calls = options.calls #Gets the call chain specifically
    st.dataframe(calls) #Outputs the call chain in a dataframe
   
    #global selectedCallContract

    selectedCallContract = st.selectbox("Select a Call strike", calls)
    selectedRowCall = calls[calls['contractSymbol'] == selectedCallContract]
    callAskPrice = selectedRowCall.iloc[0]['ask']
    #Adds the Contracts onto a select box and retrieves their ask price.


    
    callQuantity = st.number_input("Enter Quantity", min_value=1) 
    callPremium = callAskPrice * callQuantity * 100
    st.write("Premium:", callPremium)
    #Takes quantity and calculates the options premium from Ask prie

    ref = db.reference("/traders")
    userData = ref.order_by_child('userID').equal_to(usrnm).get()
    #Gets the current user from database, so data is manipulated under the current user only

    print(userData)
    
    # for user_id, user_data in userData.items():
    #     freebalance_value = user_data.get('freebalance', None)
    #     invested_value = user_data.get('invested',None)
    #     st.write(freebalance_value)
    
    # if 'freebalance_value' not in st.session_state:
    #     st.session_state['freebalance_value'] = freebalance_value
    
    #st.session_state['freebalance_value'] = freebalance_value
    
    
        


        # ref = db.reference("/traders")
        # userData = ref.order_by_child('userID').equal_to(usrnm).get()

        # print(userData)
        # for user_id, user_data in userData.items():
        #     freebalance_value = user_data.get('freebalance', None)
        #     invested_value = user_data.get('invested',None)
        #     st.write(freebalance_value)
            #if freebalance_value is not None:
            #    print(f"The value of 'freebalance' for user '{user_id}' is: {freebalance_value}")
            #else:
            #    print(f"'freebalance' not found for user '{user_id}'")
        
    if st.button('Trade Call'):
        if st.session_state.freebalance_value >= callPremium and isMarketOpen == True: #Checks if market is open
            if st.session_state.freebalance_value >= callPremium: #Checks if you can afford the trade

                st.session_state.freebalance_value -= callPremium
                st.session_state.invested_value += callPremium
                st.write(st.session_state.freebalance_value)
                #Subtracts freebalance value and adds to invested value using the premium value

                
                # if 'freebalance_value' not in st.session_state:
                #     st.session_state['freebalance_value'] = freebalance_value
                # st.session_state['freebalance_value'] = freebalance_value

                for user_id, user_data in userData.items():
                    ref.child(user_id).update({'freebalance': st.session_state.freebalance_value})
                    ref.child(user_id).update({'invested': st.session_state.invested_value})


                    contractRef = ref.child(user_id).child('contracts')

                    contractUpdate = {
                        'contractName':selectedCallContract,
                        'quantity': callQuantity,
                        'premiumPaid' : callPremium,
                        'purchasePrice' : callAskPrice
                    }   
                    
                    new_contract_ref = contractRef.push(contractUpdate)
                    #Goes to the relevant user and adds contract info which is essentially buying the contract


            elif st.session_state.freebalance_value <= callPremium:
                st.write("You can't afford this trade")
        
        elif isMarketOpen == False: #Checks if market is closed
            st.write("Market not open")

            
    st.write("Put Options") #Title
    puts = options.puts #Gets put chain (No need to obtain full chain as it was done already previously)
    st.dataframe(puts) #Outputs the put chain


    selectedPutContract = st.selectbox("Select a Put strike", puts)
    selectedRowCall = puts[puts['contractSymbol'] == selectedPutContract]
    putAskPrice = selectedRowCall.iloc[0]['ask']

    putQuantity = st.number_input("Enter Quantity", min_value=1, key="hi")
    putPremium = putAskPrice * putQuantity * 100
    st.write("Premium:", putPremium)

    if st.button("Trade put"):
        if st.session_state.freebalance_value >= callPremium and isMarketOpen == True: #Checks if market is open        
            if st.session_state.freebalance_value >= putPremium: 

                st.session_state.freebalance_value -= putPremium
                st.session_state.invested_value += putPremium
                st.write(st.session_state.freebalance_value)
                for user_id, user_data in userData.items():
                    ref.child(user_id).update({'freebalance': st.session_state.freebalance_value})
                    ref.child(user_id).update({'invested': st.session_state.invested_value})
                    contractRef = ref.child(user_id).child('contracts')

                    contractUpdate = {
                        'contractName':selectedPutContract,
                        'quantity': putQuantity,
                        'premiumPaid' : putPremium,
                        'purchasePrice' : putAskPrice
                    }   

                    new_contract_ref = contractRef.push(contractUpdate)
            elif st.session_state.freebalance_value <= putPremium:
                st.write("You can't afford this trade ahaha")        
        elif isMarketOpen == False:
            st.write("Market is closed")
def leaderboardPage():
    st.title("Leaderboard")

    leaderboardDf = pd.DataFrame(columns=['username','percentage change']) #Creates the column names
    leadedboardData = ref.get() #gets database

    for traderId, traderInfo in leadedboardData.items():
        if "userID" in traderInfo and "percentageChange" in traderInfo:
            updateValues = {
                'Username' : traderInfo['userID'],
                'Percentage change' : traderInfo['percentageChange']
            }
            leaderboardDf = leaderboardDf.append(updateValues, ignore_index=True)
    #Iterates through database to get the percentage change and the user name
    leaderboardDf= leaderboardDf.dropna(axis=1, how='all')

    st.dataframe(leaderboardDf.rename(index=lambda x: x + 1))   
def settingsPage(): 
    st.title("Settings")

    if st.button("Close positions"):
        ref = db.reference("/traders")
        userData = ref.order_by_child('userID').equal_to(usrnm).get() #Goes to the trader database and finds current user
        for user_id, user_data in userData.items():
            ref.child(user_id).update({'contracts': ""})
            ref.child(user_id).update({'freebalance': 10000})
            ref.child(user_id).update({'invested': 0})
            ref.child(user_id).update({'percentageChange': 0})
        #Iterates through to find user and changes their values back to the default
        st.session_state.freebalance_value = 10000
        st.session_state.invested_value = 0
        #Changes the current session state to default values as well
    

def quizPage():
    st.title("Quiz")
    questions = [
        "What is a 'long' position in trading?",
        "Which type of analysis involves examining past market data to predict future price movements?",
        "What does the term 'bid-ask spread' refer to?",
        "What is the purpose of a stop-loss order in trading?",
        "Which financial instrument represents ownership in a company?",
        "What is the main purpose of fundamental analysis in trading?",
        "In options trading, what does a 'call' option give the holder the right to do?",
        "What is the maximum potential loss for the buyer of an option?",
        "What is the intrinsic value of an option?",
        "What is the significance of the 'strike price' in options trading?"
    ]
    Qoptions = [
        ["A position taken by an investor who expects the price of an asset to increase.", "A position taken by an investor who expects the price of an asset to decrease.", "A position taken by an investor who is neutral on the price of an asset."],
        ["Technical analysis", "Fundamental analysis", "Sentiment analysis"],
        ["The difference between the highest price a buyer is willing to pay and the lowest price a seller is willing to accept.", "The difference between the opening and closing prices of a security over a specific period.", "The difference between the price at which an investor buys a security and the price at which it is sold."],
        ["To limit potential losses by automatically selling a security when it reaches a certain price.", "To buy a security at the lowest possible price.", "To maximize profits by holding onto a security for an extended period."],
        ["Stock", "Bond", "Option"],
        ["To analyze the intrinsic value of a security relative to its market price.", "To predict short-term price movements based on technical indicators.", "To speculate on market sentiment and psychology."],
        ["Buy the underlying asset at a predetermined price before the expiration date.", "Sell the underlying asset at a predetermined price before the expiration date.", "Receive the underlying asset at a predetermined price before the expiration date."],
        ["The premium paid for the option.", "The difference between the option's strike price and the market price of the underlying asset.", "Unlimited."],
        ["The value of the option if it were exercised immediately.", "The price at which the option was purchased.", "The difference between the option's strike price and the market price of the underlying asset."],
        ["It determines the price at which the underlying asset can be bought or sold.", "It indicates the likelihood of the option being exercised.", "It represents the option's current market value."]
    ]
    correct_answers = [0, 0, 0, 0, 0, 0, 0, 2, 0, 0] # Indices of correct options for each question

    # Display quiz questions
    num_questions = len(questions)
    user_answers = []
    for i in range(num_questions):
        st.subheader(f"Question {i+1}: {questions[i]}")
        selected_option = st.radio(f"Options:", Qoptions[i])
        user_answers.append(Qoptions[i].index(selected_option))

    if st.button("Calculate Score"):
    # Calculate score
        score = sum([1 for i in range(num_questions) if user_answers[i] == correct_answers[i]])
        st.success(f"You scored {score} out of {num_questions}.")


if not hasattr(st.session_state, 'logged_in') or not st.session_state.logged_in:
    loginsignup_page()
#If you are not logged in (just opened the app) then you will be directed to log in page. 
else:
    app_pages = {
        "Main" : mainPage,
        "Stock searcher" : stockSearcherPage,
        "Leaderboard" : leaderboardPage,
        "Settings" : settingsPage,
        "Quiz" : quizPage,
         #All the pages in the app

        }

    st.sidebar.title("Navigation")
    selected_page = st.sidebar.radio("Go to", list(app_pages.keys()))
    #Creates a side bar and adds radio button so you can go to those pages
    usrnm = st.session_state.username #This allows you to use the username outside of different functions and pages
    st.sidebar.title("Welcome: " + usrnm)
    st.sidebar.title(f"Free Balance: {st.session_state.freebalance_value:.2f}")
    # st.sidebar.title("Invested: " + str(st.session_state.invested_value))
    st.sidebar.title(f"Invested: {st.session_state.invested_value:.2f}") #Previous thing didn't work so you did that to make 2 s.f.
    

    app_pages[selected_page]()  
