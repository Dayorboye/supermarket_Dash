import dash
import pandas as pd
import numpy as np
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from dash import no_update

import sys
print(sys.version)
# Dash Application

app = dash.Dash(__name__)

server = app.server



# Datasets for The Supermarket Visualization

url = "XYZ_Company_Dataset.csv"
XYZ_Company_Datasets = pd.read_csv(url)

City_grp = XYZ_Company_Datasets.groupby('City')
City_Income = City_grp.agg({"gross income":["sum","mean","max"]})

     
abuja = City_Income.loc['Abuja',[('gross income',  'sum')]]
AbujaNam ="ABUJA INCOME (N)"
lagos = City_Income.loc['Abuja',[('gross income',  'sum')]]
LagosNam ="LAGOS INCOME (N)"
pH =  City_Income.loc['Port Harcourt',[('gross income',  'sum')]]
pHNam = "PORTHARCOUT INCOME (N)"

header = "SUPERMARKET BRANCHES PERFORMANCE"

Customer_option = XYZ_Company_Datasets['Customer type'].unique()




# Text field
def drawText(name,value):
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                                        html.Div(children=[html.Div(
                                        html.Div(html.H1(name, 
                                                                style={"text-align": "center", "font-size":"20px","font-family": "Abel","font-weight":"600","font-size": "18px",'color':'#7570b3'}),)),                       
                                        html.Div(
                                        html.Div(html.H1(value, 
                                                                style={"text-align": "center", "font-size":"20px","font-family": "Abel","font-weight":"600","font-size": "18px","color":"white"}),)),
                                                                ],), 
            ])
        ),
    ])

def drawTitle(title):
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                                        html.Div(children=[html.Div(
                                        html.Div(html.H1(title, 
                                                                style={'textAlign':'center','color':'#7570b3','font-size':'48'}),)),                       

                                                                ],), 
            ])
        ),
    ])

def dropdow():
     return html.Div([
          dbc.Card(
          dbc.CardBody([
                                   dcc.Dropdown(id='customer_type', 
                                                 # Update dropdown values using list comphrehension
                                                 options=[{
                                                        'label': i,
                                                        'value': i
                                                        } for i in Customer_option ],
                                                 placeholder="Select Customer", searchable = True , value = 'All Customers',)


          
          ])
          )
     ])

def tree_fig():
       return  html.Div([
       dbc.Card(
       dbc.CardBody([
              dcc.Graph(id='plot1',) 
       ])
       ),  
])

def bar_fig():
       return  html.Div([
       dbc.Card(
       dbc.CardBody([
              dcc.Graph(id='plot2',)
       ])
       ),  
])


def bar_fig1():
       return  html.Div([
       dbc.Card(
       dbc.CardBody([
              dcc.Graph(id='plot3',)
       ])
       ),  
])

def bar_fig2():
       return  html.Div([
       dbc.Card(
       dbc.CardBody([
              dcc.Graph(id='plot4',)
       ])
       ),  
])

def pie_fig():
       return  html.Div([
       dbc.Card(
       dbc.CardBody([
              dcc.Graph(id='plot5',) 
       ])
       ),  
])


# Application layout
# Build App

app = Dash(external_stylesheets=[dbc.themes.SLATE])
app.layout = html.Div([
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    drawTitle(header)
                ], width=12),                
            ], align='center'),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    drawText(AbujaNam,abuja)
                ], width=4),
                dbc.Col([
                    drawText(LagosNam,lagos)
                ], width=4),
                dbc.Col([
                    drawText(pHNam,pH)
                ], width=4),
            ], align='center'),
            html.Br(),
            dbc.Row([

                dbc.Col([
                    dropdow()
                ], width=6),
            ], align='center'), 
            html.Br(),
            dbc.Row([
                dbc.Col([
                    bar_fig() 
                ], width=4),
                dbc.Col([
                    bar_fig1()
                ], width=4),
                dbc.Col([
                    bar_fig2() 
                ], width=4),
            ], align='center'), 
            html.Br(),
            dbc.Row([
                dbc.Col([
                   tree_fig() 
                ], width=9),
                dbc.Col([
                    pie_fig()
                ], width=3),
            ], align='center'),      
        ]), color = 'dark'
    )
])

@app.callback( [Output(component_id='plot1', component_property='figure'),
               Output(component_id='plot2',component_property='figure'),
               Output(component_id='plot3',component_property='figure'),
               Output(component_id='plot4',component_property='figure'),
               Output(component_id='plot5',component_property='figure'),],
              [Input(component_id='customer_type', component_property='value'),],
              
              )
# Add computation to callback function and return graph
def get_graph(Customer_type):
       
       if Customer_type == "All Customers":
            
            XYZ_Company_Datasetss = XYZ_Company_Datasets.copy()
            bar_fig = px.bar(XYZ_Company_Datasets, x='Product line', y='Total', color='City', title='TOTAL SALES')
            bar_fig1 = px.bar(XYZ_Company_Datasetss, x='Product line', y='Quantity', color='City', title='THE SUPERMARKET QUANTITY ORDER')
            bar_fig2 = px.bar(XYZ_Company_Datasetss, x='Product line', y='gross income', color='City', title='THE SUPERMARKET GROSS INCOME')
            tree_fig = px.treemap(XYZ_Company_Datasets, 
                            path=['City', 'Product line'], 
                            values='Total',
                            color='Total',
                            color_continuous_scale='RdBu',
                            title='PRODUCT LINE COUNT BY CITY')
            pie_fig = px.pie(XYZ_Company_Datasets, values='gross income', names='City', title='THE SUPERMARKET GROSS INCOME')
            pie_fig1 = px.pie(XYZ_Company_Datasets, values='Quantity', names='City', title='THE SUPERMARKET QUANTITY ORDER')
            pie_fig2 = px.pie(XYZ_Company_Datasets, values='Total', names='City', title='THE SUPERMARKET TOTAL SALES')
       else:
             XYZ_Company_Datasetss = XYZ_Company_Datasets[XYZ_Company_Datasets['Customer type'] == Customer_type]     
             bar_fig = px.bar(XYZ_Company_Datasetss, x='Product line', y='Total', color='City', title='THE SUPERMARKET TOTAL SALES')
             bar_fig1 = px.bar(XYZ_Company_Datasetss, x='Product line', y='Quantity', color='City', title='THE SUPERMARKET QUANTITY ORDER')
             bar_fig2 = px.bar(XYZ_Company_Datasetss, x='Product line', y='gross income', color='City', title='THE SUPERMARKET GROSS INCOME')
             tree_fig = px.treemap(XYZ_Company_Datasetss, 
                            path=['City', 'Product line'], 
                            values='Total',
                            color='Total',
                            color_continuous_scale='RdBu',
                            title='PRODUCT LINE COUNT BY CITY')
             pie_fig = px.pie(XYZ_Company_Datasetss, values='gross income', names='City', title='THE SUPERMARKET GROSS INCOME')
              
       return tree_fig,bar_fig,bar_fig1, bar_fig2,pie_fig




# Run the app
if __name__ == '__main__':
      app.run_server()







# import pandas as pd
# import dash
# import dash_html_components as html
# import dash_core_components as dcc
# from dash.dependencies import Input, Output, State
# import plotly.graph_objects as go
# import plotly.express as px
# from dash import no_update

# import sys
# print(sys.version)
# # Dash Application

# app = dash.Dash(__name__)

# server = app.server



# # Datasets for The Supermarket Visualization

# url = "XYZ_Company_Dataset.csv"
# XYZ_Company_Datasets = pd.read_csv(url)

# City_grp = XYZ_Company_Datasets.groupby('City')
# City_Income = City_grp.agg({"gross income":["sum","mean","max"]})

     
# abuja = City_Income.loc['Abuja',[('gross income',  'sum')]]
# lagos = City_Income.loc['Abuja',[('gross income',  'sum')]]
# pH =  City_Income.loc['Port Harcourt',[('gross income',  'sum')]]


# Customer_option = XYZ_Company_Datasets['Customer type'].unique()

# app.layout = html.Div(children=[ 
#                                 # TASK1: Add title to the dashboard

#                                 html.H1('SUPERMARKET BRANCHES PERFORMANCE',style={'textAlign':'center','color':'#7570b3','font-size':'48'}),
#                                 dcc.Dropdown(id='customer_type', 
#                                                      # Update dropdown values using list comphrehension
#                                                      options=[{
#                                                                'label': i,
#                                                                'value': i
#                                                                } for i in Customer_option ],
#                                                      placeholder="Select Customer", searchable = True , value = 'All Customers',
#                                                      style={'width':'50%', 'padding':'3px', 'font-size': '20px', 'text-align-last' : 'center'}),

#                         html.Div(children=[
#                         html.Div(children=[html.Div(
#                                         html.Div(html.H1("ABUJA INCOME (N)", 
#                                                                 style={"text-align": "center","color":"#161A1D","background-color": "#d3bd98",
#                                                                        "margin-bottom":"0","padding": "30px","font-size":"20px"
#                                                                        ,"font-family": "Abel","font-weight":"600","font-size": "16px"
                                                                       
                                        
#                                                                 }),),style={}),                       
#                                         html.Div(
#                                         html.Div(html.H1(abuja, 
#                                                                 style={"text-align": "center","color":"#161A1D","background-color":"#E8DAC5",
#                                                                        "margin-top":"0","padding": "30px","font-size":"20px"
#                                                                        ,"font-family": "Abel","font-weight":"400","font-size": "2em"
                                        
#                                                                 }),),style={}),
#                                                                 ],),
                        
#                           html.Div(children=[html.Div(
#                                         html.Div(html.H1("LAGOS INCOME (N)", 
#                                                                 style={"text-align": "center","color":"#161A1D","background-color": "#d3bd98",
#                                                                        "margin-bottom":"0","padding": "30px","font-size":"20px"
#                                                                        ,"font-family": "Abel","font-weight":"600","font-size": "16px"
                                                                       
                                        
#                                                                 }),),style={}),                       
#                                         html.Div(
#                                         html.Div(html.H1(lagos, 
#                                                                 style={"text-align": "center","color":"#161A1D","background-color":"#E8DAC5",
#                                                                        "margin-top":"0","padding": "30px","font-size":"20px"
#                                                                        ,"font-family": "Abel","font-weight":"400","font-size": "2em"
                                        
#                                                                 }),),style={}),
#                                                                 ],),

#                         html.Div(children=[html.Div(
#                                         html.Div(html.H1("PORT HARCOURT INCOME (N)", 
#                                                                 style={"text-align": "center","color":"#161A1D","background-color": "#d3bd98",
#                                                                        "margin-bottom":"0","padding": "30px","font-size":"20px"
#                                                                        ,"font-family": "Abel","font-weight":"600","font-size": "16px"
                                                                       
                                        
#                                                                 }),),style={}),                       
#                                         html.Div(
#                                         html.Div(html.H1(pH, 
#                                                                 style={"text-align": "center","color":"#161A1D","background-color":"#E8DAC5",
#                                                                        "margin-top":"0","padding": "30px","font-size":"20px"
#                                                                        ,"font-family": "Abel","font-weight":"400","font-size": "2em",
                                                                           
                                        
#                                                                 }),),style={}),
#                                                                 ],),
#                                                 ],
#                         style={"display": "flex","background-color": "#0e1012","padding": "30px 0 10px 0","justify-content": "space-around"}),
         
         
#         html.Div(dcc.Graph(id='plot1'),
#                                                 style={"background-color": "#161A1D",
#                                                 "padding": "60px",},),                       # Create an outer division 
                            
#         html.Div(children=[
                        
#                         html.Div(dcc.Graph(id='plot2', 
#                                                 style={"background-color": "#161A1D","text-align": "center",
#                                                 "height":"70vh"}),),
#                         html.Div(dcc.Graph(id='plot3',
#                                                 style={"background-color": "#161A1D","text-align": "center",
#                                                 "height":"70vh"}),),],
#                         style={"display": "flex","background-color": "#0e1012","padding-bottom": "60px","justify-content": "space-around"}),
                  
#         html.Div(children=[
                        
#                         html.Div(dcc.Graph(id='plot4',
#                                                 style={"background-color": "#161A1D","text-align": "center",
#                                                 "height":"70vh"}),),
#                         html.Div(dcc.Graph(id='plot5', 
#                                                 style={"background-color": "#161A1D","text-align": "center",
#                                                 "height":"70vh"}),),],
#                         style={"display": "flex","background-color": "#0e1012","padding-bottom": "60px","justify-content": "space-around"}), 
                                   
#                      # Graph layout
                               
#                                 # html.Div(dcc.Graph(figure=tree_fig)),
    
#                                 # html.Div([
#                                 #         html.Div(dcc.Graph( figure=bar_fig)),
#                                 #         html.Div(dcc.Graph(figure=pie_fig))
#                                 # ], style={'display': 'flex'}),
                                 
                                
                            
#                                 ],style={"height": "100vh"})

# @app.callback( [Output(component_id='plot1', component_property='figure'),
#                Output(component_id='plot2',component_property='figure'),
#                Output(component_id='plot3',component_property='figure'),
#                Output(component_id='plot4',component_property='figure'),
#                Output(component_id='plot5',component_property='figure'),],
#               [Input(component_id='customer_type', component_property='value'),],
              
#               )
# # Add computation to callback function and return graph
# def get_graph(Customer_type):
       
#        if Customer_type == "All Customers":
            
#             XYZ_Company_Datasetss = XYZ_Company_Datasets.copy()
#             bar_fig = px.bar(XYZ_Company_Datasets, x='Product line', y='Total', color='City', title='TOTAL SALES')
#             bar_fig1 = px.bar(XYZ_Company_Datasetss, x='Product line', y='Quantity', color='City', title='THE SUPERMARKET QUANTITY ORDER')
#             bar_fig2 = px.bar(XYZ_Company_Datasetss, x='Product line', y='gross income', color='City', title='THE SUPERMARKET GROSS INCOME')
#             tree_fig = px.treemap(XYZ_Company_Datasets, 
#                             path=['City', 'Product line'], 
#                             values='Total',
#                             color='Total',
#                             color_continuous_scale='RdBu',
#                             title='PRODUCT LINE COUNT BY CITY')
#             pie_fig = px.pie(XYZ_Company_Datasets, values='gross income', names='City', title='THE SUPERMARKET GROSS INCOME')
#             pie_fig1 = px.pie(XYZ_Company_Datasets, values='Quantity', names='City', title='THE SUPERMARKET QUANTITY ORDER')
#             pie_fig2 = px.pie(XYZ_Company_Datasets, values='Total', names='City', title='THE SUPERMARKET TOTAL SALES')
#        else:
#              XYZ_Company_Datasetss = XYZ_Company_Datasets[XYZ_Company_Datasets['Customer type'] == Customer_type]     
#              bar_fig = px.bar(XYZ_Company_Datasetss, x='Product line', y='Total', color='City', title='THE SUPERMARKET TOTAL SALES')
#              bar_fig1 = px.bar(XYZ_Company_Datasetss, x='Product line', y='Quantity', color='City', title='THE SUPERMARKET QUANTITY ORDER')
#              bar_fig2 = px.bar(XYZ_Company_Datasetss, x='Product line', y='gross income', color='City', title='THE SUPERMARKET GROSS INCOME')
#              tree_fig = px.treemap(XYZ_Company_Datasetss, 
#                             path=['City', 'Product line'], 
#                             values='Total',
#                             color='Total',
#                             color_continuous_scale='RdBu',
#                             title='PRODUCT LINE COUNT BY CITY')
#              pie_fig = px.pie(XYZ_Company_Datasetss, values='gross income', names='City', title='THE SUPERMARKET GROSS INCOME')
              
#        return tree_fig,bar_fig,pie_fig,bar_fig1, bar_fig2




# # Run the app
# if __name__ == '__main__':
#       app.run_server()


 




