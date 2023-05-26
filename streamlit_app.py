import streamlit as st
import pandas as pd
import datetime
from datetime import datetime
import altair as alt 
import time


def load_data(sheet_id, sheet_data):
    """Loads data from Google Sheets"""
    gsheet_data = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(sheet_id, sheet_data)
    url = gsheet_data.replace(" ","")
    df = pd.read_csv(url, on_bad_lines='skip')
    df = df.iloc[:,:22].fillna('')
    df['Battery In Voltage'] = pd.to_numeric(df['Battery In Voltage'])
    df['Battery Out Voltage'] = pd.to_numeric(df['Battery Out Voltage'])
    df['Amount '] = pd.to_numeric(df['Amount '])
    # df['Security Amount'] = pd.to_numeric(df['Security Amount'])
    # df['Penalty Amount '] = pd.to_numeric(df['Penalty Amount '])
    
    data = pd.DataFrame({
        'Timestamp':df['Timestamp'],
        'Customer name':df['Customer name'],
        'Battery_in':df['Battery In'],
        'Battery_in_volt':df['Battery In Voltage'],
        'Battery_out':df['Battery Out'],
        'Battery_Out_volt':df['Battery Out Voltage'],   
        'Amount':df['Amount '],
        'Security_amt':df['Security Amount'],
        'Penalty_amt':df['Penalty Amount '],
        'Supervisor':df['Shift supervisor'],
        'Plan':df['Is there any plan?'],
        'Battery_submit?':df['Is the customer submitting or collecting battery?'],
        'Center':df['Center']
    })
    
    today = datetime.today().date()
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])
    filtered_data = data[data['Timestamp'].dt.date == today]
    filtered_data['hour'] = filtered_data['Timestamp'].dt.hour
    
    first_dict = {'190': [], '200 Plan': [],'300':[],'330':[],'250':[],'150':[],'130 plan':[],
              '4500 plan':[],'2500 plan':[],'1260 plan':[],'280 plan':[],'430 plan':[]}
    start_hour = filtered_data['hour'].iloc[0]
    
    for hour in filtered_data['Timestamp'].dt.hour.unique():
        try:
            count_190 = filtered_data[(filtered_data['Amount'] == 190.0) &
                                      (filtered_data['hour'] >= hour) &
                                      (filtered_data['hour'] < hour + 1)]['Amount'].value_counts()[190.0]
            first_dict['190'].append(count_190)
        except:
            first_dict['190'].append(0)

        try:
            count_200 = filtered_data[(filtered_data['Amount'] == 200) & 
                                  (filtered_data['Plan'] != '430 plan') &
                                  (filtered_data['hour'] >= hour) &
                                  (filtered_data['hour'] < hour + 1)]['Amount'].value_counts()[200]
            first_dict['200 Plan'].append(count_200)
        except:
            first_dict['200 Plan'].append(0)
        
        try:
            count_300 = filtered_data[(filtered_data['Amount'] == 300) & 
                                    (filtered_data['hour'] >= hour) &
                                    (filtered_data['hour'] < hour + 1)]['Amount'].value_counts()[300]
            first_dict['300'].append(count_300)
        except:
            first_dict['300'].append(0)  
        
        try:
            count_330 = filtered_data[(filtered_data['Amount'] == 330) & 
                                    (filtered_data['hour'] >= hour) &
                                    (filtered_data['hour'] < hour + 1)]['Amount'].value_counts()[330]
            first_dict['330'].append(count_330)
        except:
            first_dict['330'].append(0) 
        
        try:
            count_250 = filtered_data[(filtered_data['Amount'] == 250) & 
                                    (filtered_data['hour'] >= hour) &
                                    (filtered_data['hour'] < hour + 1)]['Amount'].value_counts()[250]
            first_dict['250'].append(count_250)
        except:
            first_dict['250'].append(0)
            
        try:
            count_150 = filtered_data[(filtered_data['Amount'] == 150) & 
                                    (filtered_data['hour'] >= hour) &
                                    (filtered_data['hour'] < hour + 1)]['Amount'].value_counts()[150]
            first_dict['150'].append(count_150)
        except:
            first_dict['150'].append(0)
            
   
            
        try:
             count_130 = filtered_data[(filtered_data['Plan'] == '130 plan') & (filtered_data['hour'] >= hour) &
                                  (filtered_data['hour'] < hour + 1)]['Amount'].value_counts().values[0]
             first_dict['130 plan'].append(count_130)
              
        except:
            first_dict['130 plan'].append(0)
                   
            
        try:
             count_4500 = filtered_data[(filtered_data['Plan'] == '4500 plan') & (filtered_data['hour'] >= hour) &
                               (filtered_data['hour'] < hour + 1)]['Amount'].value_counts().values[0]
             first_dict['4500 plan'].append(count_4500)
              
        except:
            first_dict['4500 plan'].append(0)
        

        try:
             count_2500 = filtered_data[(filtered_data['Plan'] == '2500 plan') & (filtered_data['hour'] >= hour) &
                                  (filtered_data['hour'] < hour + 1)]['Amount'].value_counts().values[0]
             first_dict['2500 plan'].append(count_2500)
              
        except:
            first_dict['2500 plan'].append(0)
               
            

        try:
             count_1260 = filtered_data[(filtered_data['Plan'] == '1260 plan') & (filtered_data['hour'] >= hour) &
                                  (filtered_data['hour'] < hour + 1)]['Amount'].value_counts().values[0]
             first_dict['1260 plan'].append(count_1260)
              
        except:
            first_dict['1260 plan'].append(0)
             
            
        try:
             count_280 = filtered_data[(filtered_data['Plan'] == '280 plan') & (filtered_data['hour'] >= hour) &
                                  (filtered_data['hour'] < hour + 1)]['Amount'].value_counts().values[0]
             first_dict['280 plan'].append(count_280)
              
        except:
            first_dict['280 plan'].append(0)
            
            
        try:
            count_430 = filtered_data[(filtered_data['Amount'] == 200) & 
                                    (filtered_data['Plan'] == '430 plan') &
                                    (filtered_data['hour'] >= hour) &
                                    (filtered_data['hour'] < hour + 1)]['Amount'].value_counts()[200]
            first_dict['430 plan'].append(count_430)
        except:
            first_dict['430 plan'].append(0)    



        start_hour += 1


    
    dict_to_dataframe=pd.DataFrame(first_dict)
    # generate a list of labels based on the number of rows
    labels = [f"{i+filtered_data['hour'].iloc[0]}-{i+(filtered_data['hour'].iloc[0]+1)}" for i in range(len(dict_to_dataframe))]

    # set the index to the custom labels
    dict_to_dataframe.set_index(pd.Index(labels), inplace=True)
    dict_to_dataframe.index.name = 'Timestamp'
    
    return dict_to_dataframe


def load_data_daywise(sheet_id, sheet_data,date):
    """Loads data from Google Sheets"""
    gsheet_data = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(sheet_id, sheet_data)
    url = gsheet_data.replace(" ","")
    df = pd.read_csv(url, on_bad_lines='skip')
    df = df.iloc[:,:22].fillna('')
    df['Battery In Voltage'] = pd.to_numeric(df['Battery In Voltage'])
    df['Battery Out Voltage'] = pd.to_numeric(df['Battery Out Voltage'])
    df['Amount '] = pd.to_numeric(df['Amount '])
    # df['Security Amount'] = pd.to_numeric(df['Security Amount'])
    # df['Penalty Amount '] = pd.to_numeric(df['Penalty Amount '])
    
    data = pd.DataFrame({
        'Timestamp':df['Timestamp'],
        'Customer name':df['Customer name'],
        'Battery_in':df['Battery In'],
        'Battery_in_volt':df['Battery In Voltage'],
        'Battery_out':df['Battery Out'],
        'Battery_Out_volt':df['Battery Out Voltage'],   
        'Amount':df['Amount '],
        'Security_amt':df['Security Amount'],
        'Penalty_amt':df['Penalty Amount '],
        'Supervisor':df['Shift supervisor'],
        'Plan':df['Is there any plan?'],
        'Battery_submit?':df['Is the customer submitting or collecting battery?'],
        'Center':df['Center']
    })
    
    today = datetime.today().date()
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])
    filtered_data = data[data['Timestamp'].dt.strftime('%Y-%m-%d') == date]
    # df_filtered = df[df['date'].dt.strftime('%Y-%m-%d') == '2014-01-01']
    filtered_data['hour'] = filtered_data['Timestamp'].dt.hour
    
    first_dict = {'190': [], '200 Plan': [],'300':[],'330':[],'250':[],'150':[],'130 plan':[],
              '4500 plan':[],'2500 plan':[],'1260 plan':[],'280 plan':[],'430 plan':[]}
    start_hour = filtered_data['hour'].iloc[0]
    
    for hour in filtered_data['Timestamp'].dt.hour.unique():
        try:
            count_190 = filtered_data[(filtered_data['Amount'] == 190.0) &
                                      (filtered_data['hour'] >= hour) &
                                      (filtered_data['hour'] < hour + 1)]['Amount'].value_counts()[190.0]
            first_dict['190'].append(count_190)
        except:
            first_dict['190'].append(0)

        try:
            count_200 = filtered_data[(filtered_data['Amount'] == 200) & 
                                  (filtered_data['Plan'] != '430 plan') &
                                  (filtered_data['hour'] >= hour) &
                                  (filtered_data['hour'] < hour + 1)]['Amount'].value_counts()[200]
            first_dict['200 Plan'].append(count_200)
        except:
            first_dict['200 Plan'].append(0)
        
        try:
            count_300 = filtered_data[(filtered_data['Amount'] == 300) & 
                                    (filtered_data['hour'] >= hour) &
                                    (filtered_data['hour'] < hour + 1)]['Amount'].value_counts()[300]
            first_dict['300'].append(count_300)
        except:
            first_dict['300'].append(0)  
        
        try:
            count_330 = filtered_data[(filtered_data['Amount'] == 330) & 
                                    (filtered_data['hour'] >= hour) &
                                    (filtered_data['hour'] < hour + 1)]['Amount'].value_counts()[330]
            first_dict['330'].append(count_330)
        except:
            first_dict['330'].append(0) 
        
        try:
            count_250 = filtered_data[(filtered_data['Amount'] == 250) & 
                                    (filtered_data['hour'] >= hour) &
                                    (filtered_data['hour'] < hour + 1)]['Amount'].value_counts()[250]
            first_dict['250'].append(count_250)
        except:
            first_dict['250'].append(0)
            
        try:
            count_150 = filtered_data[(filtered_data['Amount'] == 150) & 
                                    (filtered_data['hour'] >= hour) &
                                    (filtered_data['hour'] < hour + 1)]['Amount'].value_counts()[150]
            first_dict['150'].append(count_150)
        except:
            first_dict['150'].append(0)
            
   
            
        try:
             count_130 = filtered_data[(filtered_data['Plan'] == '130 plan') & (filtered_data['hour'] >= hour) &
                                  (filtered_data['hour'] < hour + 1)]['Amount'].value_counts().values[0]
             first_dict['130 plan'].append(count_130)
              
        except:
            first_dict['130 plan'].append(0)
                   
            
        try:
             count_4500 = filtered_data[(filtered_data['Plan'] == '4500 plan') & (filtered_data['hour'] >= hour) &
                               (filtered_data['hour'] < hour + 1)]['Amount'].value_counts().values[0]
             first_dict['4500 plan'].append(count_4500)
              
        except:
            first_dict['4500 plan'].append(0)
        

        try:
             count_2500 = filtered_data[(filtered_data['Plan'] == '2500 plan') & (filtered_data['hour'] >= hour) &
                                  (filtered_data['hour'] < hour + 1)]['Amount'].value_counts().values[0]
             first_dict['2500 plan'].append(count_2500)
              
        except:
            first_dict['2500 plan'].append(0)
               
            

        try:
             count_1260 = filtered_data[(filtered_data['Plan'] == '1260 plan') & (filtered_data['hour'] >= hour) &
                                  (filtered_data['hour'] < hour + 1)]['Amount'].value_counts().values[0]
             first_dict['1260 plan'].append(count_1260)
              
        except:
            first_dict['1260 plan'].append(0)
             
            
        try:
             count_280 = filtered_data[(filtered_data['Plan'] == '280 plan') & (filtered_data['hour'] >= hour) &
                                  (filtered_data['hour'] < hour + 1)]['Amount'].value_counts().values[0]
             first_dict['280 plan'].append(count_280)
              
        except:
            first_dict['280 plan'].append(0)
            
            
        try:
            count_430 = filtered_data[(filtered_data['Amount'] == 200) & 
                                    (filtered_data['Plan'] == '430 plan') &
                                    (filtered_data['hour'] >= hour) &
                                    (filtered_data['hour'] < hour + 1)]['Amount'].value_counts()[200]
            first_dict['430 plan'].append(count_430)
        except:
            first_dict['430 plan'].append(0)    



        start_hour += 1


    
    dict_to_dataframe=pd.DataFrame(first_dict)
    # generate a list of labels based on the number of rows
    labels = [f"{i+filtered_data['hour'].iloc[0]}-{i+(filtered_data['hour'].iloc[0]+1)}" for i in range(len(dict_to_dataframe))]

    # set the index to the custom labels
    dict_to_dataframe.set_index(pd.Index(labels), inplace=True)
    
    return dict_to_dataframe


def load_data_daywise1(sheet_id, sheet_data,date):
    """Loads data from Google Sheets"""
    gsheet_data = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(sheet_id, sheet_data)
    url = gsheet_data.replace(" ","")
    df = pd.read_csv(url, on_bad_lines='skip')
    df = df.iloc[:,:22].fillna('')
    df['Battery In Voltage'] = pd.to_numeric(df['Battery In Voltage'])
    df['Battery Out Voltage'] = pd.to_numeric(df['Battery Out Voltage'])
    df['Amount '] = pd.to_numeric(df['Amount '])
    # df['Security Amount'] = pd.to_numeric(df['Security Amount'])
    # df['Penalty Amount '] = pd.to_numeric(df['Penalty Amount '])
    
    data = pd.DataFrame({
        'Timestamp':df['Timestamp'],
        'Customer name':df['Customer name'],
        'Battery_in':df['Battery In'],
        'Battery_in_volt':df['Battery In Voltage'],
        'Battery_out':df['Battery Out'],
        'Battery_Out_volt':df['Battery Out Voltage'],   
        'Amount':df['Amount '],
        'Security_amt':df['Security Amount'],
        'Penalty_amt':df['Penalty Amount '],
        'Supervisor':df['Shift supervisor'],
        'Plan':df['Is there any plan?'],
        'Battery_submit?':df['Is the customer submitting or collecting battery?'],
        'Center':df['Center']
    })
    
    today = datetime.today().date()
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])
    filtered_data = data[data['Timestamp'].dt.strftime('%Y-%m-%d') == date]
    # df_filtered = df[df['date'].dt.strftime('%Y-%m-%d') == '2014-01-01']
    filtered_data['hour'] = filtered_data['Timestamp'].dt.hour
    
    first_dict = {'Swappings': []}
    start_hour = filtered_data['hour'].iloc[0]
    
    for hour in filtered_data['Timestamp'].dt.hour.unique():
        try:
            count_190 = filtered_data[(filtered_data['Battery_out'].notnull() & (filtered_data['Battery_out'].str.strip() != "")) &
                                  (filtered_data['hour'] >= start_hour) &
                                  (filtered_data['hour'] < start_hour + 1)]['Battery_out'].count()
            first_dict['Swappings'].append(count_190)
        except:
            first_dict['Swappings'].append(0)




        start_hour += 1


    
    dict_to_dataframe=pd.DataFrame(first_dict)
    # generate a list of labels based on the number of rows
    labels = [f"{i+filtered_data['hour'].iloc[0]}-{i+(filtered_data['hour'].iloc[0]+1)}" for i in range(len(dict_to_dataframe))]

    # set the index to the custom labels
    dict_to_dataframe.set_index(pd.Index(labels), inplace=True)
    
    ### Adding Best Day Swappings


    best_day_swappings = ['0', '11', '17', '12', '18', '15', '12', '8', '14', '8', '5', '21', '16', '9', '10', '13', '10','8', '207']
    dict_to_dataframe['Total Best Day'] = best_day_swappings[:len(dict_to_dataframe)]

    sums=[]
    for i in range(len(dict_to_dataframe)):
        
        if i==0:
            sums.append(dict_to_dataframe.iloc[i].values[0])
        else:
            first=sums[i-1]
            second=dict_to_dataframe.iloc[i].values[0]
            total=first+second
            sums.append(total)

    dict_to_dataframe['Total Swaps yet'] = sums
        
    sums_best_day = []

    sums_best_day = []

    if len(dict_to_dataframe) < 17:
        for i in range(len(dict_to_dataframe)):
            if i == 0:
                sums_best_day.append(int(best_day_swappings[i]))
            else:
                first = int(sums_best_day[i-1])
                second = int(best_day_swappings[i])
                total = first + second
                sums_best_day.append(total)

        dict_to_dataframe['Total Best Day yet'] = sums_best_day
    else:
        for i in range(len(dict_to_dataframe)):
            if i == 0:
                sums_best_day.append(int(best_day_swappings[i]))
            else:
                first = int(sums_best_day[i-1])
                second = int(best_day_swappings[i])
                total = first + second
                sums_best_day.append(total)

        dict_to_dataframe['Total Best Day yet'] = sums_best_day

        values_list = dict_to_dataframe['Total Best Day yet'].values.tolist()
        last_element = values_list.pop(-1)
        values_list.insert(18, 207)
        dict_to_dataframe['Total Best Day yet'] = values_list

        
    return dict_to_dataframe


def Getdataformistakes(date):
    import pandas as pd
    import datetime as dt
    from datetime import datetime
    import time
    sheet_id="1NikKhqY7u3AGsm9Fpk9UaqNFyzmyojuz8-iqUGh295g"
    sheet_data="Form Responses 1"

    gsheet_data = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(sheet_id, sheet_data)

    url = gsheet_data.replace(" ","")
    df=pd.read_csv(url, on_bad_lines='skip')
    df=df.iloc[:,:22].fillna('')


    df['Battery In Voltage']=pd.to_numeric(df['Battery In Voltage'])
    df['Battery Out Voltage']=pd.to_numeric(df['Battery Out Voltage'])
    df['Amount ']=pd.to_numeric(df['Amount '])



    data=pd.DataFrame({
                      'Timestamp':df['Timestamp'],'Customer name':df['Customer name'],'Battery_in':df['Battery In'],'Battery_in_volt':df['Battery In Voltage'],'Battery_out':df['Battery Out'],'Battery_Out_volt':df['Battery Out Voltage'],   
                       'Amount':df['Amount '],'Security_amt':df['Security Amount'],'Penalty_amt':df['Penalty Amount '],'Supervisor':df['Shift supervisor'],'Plan':df['Is there any plan?'],
                      'Battery_submit?':df['Is the customer submitting or collecting battery?'],'Center':df['Center']
                       })
   
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])
    start_date = pd.Timestamp(dt.date.today().replace(day=1))
    end_date = pd.Timestamp(dt.date.today())
    
    filtered_data = data.loc[pd.to_datetime(data['Timestamp']).dt.normalize().between(pd.Timestamp(start_date), pd.Timestamp(end_date))]

    
    filtered_data['date'] = filtered_data['Timestamp'].dt.date
    filtered_data['date'] = pd.to_datetime(filtered_data['date'])
    
    
        
    final_dict = { 'Name': [], 'Battery Out': [],'Shift supervisor1':[], 'Battery_out_date': [],'Battery In': [],'Shift supervisor2':[],'Battery_in_date':[]}
    for i in range(filtered_data.shape[0]):

        List=[]
        List.append(filtered_data['Customer name'].iloc[i])
        List.append(filtered_data['Battery_out'].iloc[i])

        for j in range(i+1,filtered_data.shape[0]):
            if filtered_data['Customer name'].iloc[j]==List[0]:
                if filtered_data['Battery_in'].iloc[j]!= List[1]:

                    final_dict['Name'].append(List[0])
                    final_dict['Battery Out'].append(List[1])
                    final_dict['Shift supervisor1'].append(filtered_data['Supervisor'].iloc[i])
                    final_dict['Battery_out_date'].append(str(filtered_data['Timestamp'].iloc[i]))
                    final_dict['Battery In'].append(filtered_data['Battery_in'].iloc[j])
                    final_dict['Shift supervisor2'].append(filtered_data['Supervisor'].iloc[j])                
                    final_dict['Battery_in_date'].append(str(filtered_data['Timestamp'].iloc[j]))
                    break
                else:
                    break
    Inout_matching_data=pd.DataFrame(final_dict)
    Inout_matching_data['Battery_out_date'] = pd.to_datetime(Inout_matching_data['Battery_out_date'])
    Inout_matching_data['Battery_in_date'] = pd.to_datetime(Inout_matching_data['Battery_in_date'])

    Inout_matching_data.sort_values(by='Battery_in_date',inplace=True)

    df_filtered=(Inout_matching_data[Inout_matching_data['Battery_in_date'].dt.strftime('%Y-%m-%d') == date]).reset_index(drop=True)
    

    
    return df_filtered

def Getdatafornamemistakes(date):
    import pandas as pd
    import datetime as dt
    from datetime import datetime
    import time
    sheet_id="1NikKhqY7u3AGsm9Fpk9UaqNFyzmyojuz8-iqUGh295g"
    sheet_data="Form Responses 1"

    gsheet_data = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(sheet_id, sheet_data)

    url = gsheet_data.replace(" ","")
    df=pd.read_csv(url, on_bad_lines='skip')
    df=df.iloc[:,:22].fillna('')


    df['Battery In Voltage']=pd.to_numeric(df['Battery In Voltage'])
    df['Battery Out Voltage']=pd.to_numeric(df['Battery Out Voltage'])
    df['Amount ']=pd.to_numeric(df['Amount '])



    data=pd.DataFrame({
                      'Timestamp':df['Timestamp'],'Customer name':df['Customer name'],'Battery_in':df['Battery In'],'Battery_in_volt':df['Battery In Voltage'],'Battery_out':df['Battery Out'],'Battery_Out_volt':df['Battery Out Voltage'],   
                       'Amount':df['Amount '],'Security_amt':df['Security Amount'],'Penalty_amt':df['Penalty Amount '],'Supervisor':df['Shift supervisor'],'Plan':df['Is there any plan?'],
                      'Battery_submit?':df['Is the customer submitting or collecting battery?'],'Center':df['Center']
                       })
   
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])
    start_date = pd.Timestamp(dt.date.today().replace(day=1))
    end_date = pd.Timestamp(dt.date.today())
    
    filtered_data = data.loc[pd.to_datetime(data['Timestamp']).dt.normalize().between(pd.Timestamp(start_date), pd.Timestamp(end_date))]

    
    filtered_data['date'] = filtered_data['Timestamp'].dt.date
    filtered_data['date'] = pd.to_datetime(filtered_data['date'])
    
    dict1 = {'Battery Out':[],'Customer 1':[],'Battery out time':[],'Supervisor when battery out':[],
         'Battery In':[],'Customer 2':[],'Battery in time':[],'Supervisor when battery in':[]}

    for i in range(filtered_data.shape[0]):
        List1 = []
        List1.append(filtered_data['Battery_out'].iloc[i])
        List1.append(filtered_data['Customer name'].iloc[i])
        for j in range(i+1,filtered_data.shape[0]):
            if filtered_data['Battery_in'].iloc[j] == List1[0]:
                if filtered_data['Customer name'].iloc[j]!= List1[1]:

                    dict1['Battery Out'].append(List1[0])
                    dict1['Customer 1'].append(List1[1])
                    dict1['Battery out time'].append(filtered_data['Timestamp'].iloc[i])
                    dict1['Supervisor when battery out'].append(filtered_data['Supervisor'].iloc[i])


                    dict1['Battery in time'].append(filtered_data['Timestamp'].iloc[j])
                    dict1['Supervisor when battery in'].append(filtered_data['Supervisor'].iloc[j])
                    dict1['Battery In'].append(filtered_data['Battery_in'].iloc[j])
                    dict1['Customer 2'].append(filtered_data['Customer name'].iloc[j])

                    break
                else:
                    break

    dataframeformistakes = pd.DataFrame(dict1)
    dataframeformistakes['Battery out time'] = pd.to_datetime(dataframeformistakes['Battery out time'])
    dataframeformistakes['Battery in time'] = pd.to_datetime(dataframeformistakes['Battery in time'])

    dataframeformistakes.sort_values(by='Battery in time',inplace=True)
    df_filtered=(dataframeformistakes[dataframeformistakes['Battery in time'].dt.strftime('%Y-%m-%d') == date]).reset_index(drop=True)
    return df_filtered


def Getdataentries(date):
    import pandas as pd
    import datetime as dt
    from pandas import Timestamp
    from datetime import datetime
    import math
    import warnings
    warnings.filterwarnings('ignore')
    sheet_id="1NikKhqY7u3AGsm9Fpk9UaqNFyzmyojuz8-iqUGh295g"
    sheet_data="Form Responses 1"

    gsheet_data = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(sheet_id, sheet_data)

    url = gsheet_data.replace(" ","")
    df=pd.read_csv(url, on_bad_lines='skip')
    df=df.iloc[:,:22].fillna('')

    df['Battery In Voltage']=pd.to_numeric(df['Battery In Voltage'])
    df['Battery Out Voltage']=pd.to_numeric(df['Battery Out Voltage'])
    df['Amount ']=pd.to_numeric(df['Amount '])


    data=pd.DataFrame({
                      'Timestamp':df['Timestamp'],'Customer name':df['Customer name'],'Battery_in':df['Battery In'],'Battery_in_volt':df['Battery In Voltage'],'Battery_out':df['Battery Out'],'Battery_Out_volt':df['Battery Out Voltage'],   
                       'Amount':df['Amount '],'Security_amt':df['Security Amount'],'Penalty_amt':df['Penalty Amount '],'Supervisor':df['Shift supervisor'],'Plan':df['Is there any plan?'],
                      'Battery_submit?':df['Is the customer submitting or collecting battery?'],'Center':df['Center']
                       })

    data['Timestamp'] = pd.to_datetime(data['Timestamp'])
    data['Date'] = data['Timestamp'].dt.date
    data['Date'] = pd.to_datetime(data['Date'])

    sheet_id1="1gFlgJWIuyEjdR4xCaWB7aog4IYtP_62h9RMkcW6Zlpg"
    sheet_data1="Form Responses 1"

    gsheet_data1 = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(sheet_id1, sheet_data1)

    url1 = gsheet_data1.replace(" ","")
    df1=pd.read_csv(url1, on_bad_lines='skip')
    df1["Timestamp"] = pd.to_datetime(df1["Timestamp"])
    df1['DATE'] = pd.to_datetime(df1['DATE'])

    g4_swappings = data[(data['Center'] == 'G4') & (data['Date'] == date) &  (data['Battery_out']!='') ].shape[0]

    laptop_entries = df1.loc[(df1['DATE'] == date) & df1['Battery Number SL (only write number, please do not write SL)']]['Battery Number SL (only write number, please do not write SL)'].count()
    results = f"<p style='font-size: 24px;'>Total G4 Swappings: {g4_swappings}</p><br><p style='font-size: 24px;'>Total Laptop Entries: {laptop_entries}</p>"
    
        
    return results
    



#                                 """Main function starts from here """ 

def main():
    st.set_page_config(page_title="Model for hourly update", layout="wide")
    page = st.sidebar.selectbox("Select a page", ["Hourly Data","Entry Mistakes", "Swapping Distribution"])
    
    if page == "Hourly Data":
        # if st.sidebar.button("Load Hourly Data"):
        sheet_id = "1NikKhqY7u3AGsm9Fpk9UaqNFyzmyojuz8-iqUGh295g"
        sheet_data = "Form Responses 1"
        date = str(st.sidebar.date_input("Select start date"))
        data = load_data_daywise1(sheet_id, sheet_data,date)
        laptop_entries = Getdataentries(date)

        st.title("Battery Out")
            # st.write("This app shows Hourly battery out today.")

        st.write(data)
        
        st.title("Laptop Entries")
        st.write(laptop_entries,unsafe_allow_html=True)
#                            These lines of code can create button to fetch data 
        
    # elif page == "Hourly Data":
    #     if st.sidebar.button("Load Hourly Data"):
    #         sheet_id = "1NikKhqY7u3AGsm9Fpk9UaqNFyzmyojuz8-iqUGh295g"
    #         sheet_data = "Form Responses 1"
    #         data = load_data(sheet_id, sheet_data)

    #         st.title("Battery Out Today")
    #         # st.write("This app shows Hourly battery out today.")

    #         st.write(data)

    #         st.bar_chart(data)
    elif page == "Swapping Distribution":
        # st.title("Homepage")
        sheet_id = "1NikKhqY7u3AGsm9Fpk9UaqNFyzmyojuz8-iqUGh295g"
        sheet_data = "Form Responses 1"
        date = str(st.sidebar.date_input("Select start date"))

        data = load_data_daywise(sheet_id, sheet_data,date)

        st.title("Battery Out")
            # st.write("This app shows Hourly battery out today.")

        st.write(data)

        st.bar_chart(data)

    elif page == "Entry Mistakes":
        # st.title("Homepage")
        st.title("Entry Mistakes")
        date = str(st.sidebar.date_input("Select start date"))
        

        st.write(Getdataformistakes(date))
        st.write(Getdatafornamemistakes(date))


    

if __name__ == '__main__':
    main()
