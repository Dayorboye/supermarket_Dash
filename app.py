
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update

import sys
print(sys.version)
# Dash Application

app = dash.Dash(__name__)



# Datasets for The Supermarket Visualization

url = "XYZ_Company_Dataset.csv"
XYZ_Company_Datasets = pd.read_csv(url)

City_grp = XYZ_Company_Datasets.groupby('City')
City_Income = City_grp.agg({"gross income":["sum","mean","max"]})

     
abuja = City_Income.loc['Abuja',[('gross income',  'sum')]]
lagos = City_Income.loc['Abuja',[('gross income',  'sum')]]
pH =  City_Income.loc['Port Harcourt',[('gross income',  'sum')]]

# uniquecustomer = XYZ_Company_Datasets['Customer type'].unique().tolist()
# Customer_type = []
# Customer_type.append({'label': 'Customer type', 'value': 'Customer type'})
# for customer in uniquecustomer:
#  Customer_type.append({'label': customer, 'value': customer}),
Customer_option = XYZ_Company_Datasets['Customer type'].unique()



import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import seaborn as sns; sns.set()


# Datasets for The Hospital Cluster Visualization
datasets = pd.read_excel("lagosHosptals.xlsx")

datasets_lat = datasets[["lat"]]
datasets_long = datasets[["long"]]

geo_datas = datasets[["lat"]]

geo_datas["lon"] = datasets_long

geo_datas["lat"]
geo_datas["lon"]

K_clusters = range(1,10)
kmeans = [KMeans(n_clusters=i) for i in K_clusters]
Y_axis = geo_datas[['lon']]
X_axis = geo_datas[['lat']]
score = [kmeans[i].fit(Y_axis).score(Y_axis) for i in range(len(kmeans))]
# Visualize
line_fig = px.line(x = K_clusters, y = score, title = 'Elbow Curve')


KMNs = KMeans(n_clusters=6)

KMNs.fit(geo_datas)

Labels = KMNs.predict(geo_datas)

Centroid = KMNs.cluster_centers_
a = Centroid[:,0]
b = Centroid[:,1]



fig = px.scatter(geo_datas, x = geo_datas["lat"], y = geo_datas["lon"],
              color = Labels, opacity = 0.8, size = geo_datas["lat"], size_max=30, title = 'LAGOS HOSPITAL CLUSTER')

# Application layout
app.layout = html.Div(children=[ 
                                # TASK1: Add title to the dashboard

                                html.H1('SUPERMARKET BRANCHES PERFORMANCE',style={'textAlign':'center','color':'#7570b3','font-size':'48'}),
                                dcc.Dropdown(id='customer_type', 
                                                     # Update dropdown values using list comphrehension
                                                     options=[{
                                                               'label': i,
                                                               'value': i
                                                               } for i in Customer_option ],
                                                     placeholder="Select Customer", searchable = True , value = 'All Customers',
                                                     style={'width':'50%', 'padding':'3px', 'font-size': '20px', 'text-align-last' : 'center'}),

                        html.Div(children=[
                        html.Div(children=[html.Div(
                                        html.Div(html.H1("ABUJA INCOME (N)", 
                                                                style={"text-align": "center","color":"#161A1D","background-color": "#d3bd98",
                                                                       "margin-bottom":"0","padding": "30px","font-size":"20px"
                                                                       ,"font-family": "Abel","font-weight":"600","font-size": "16px"
                                                                       
                                        
                                                                }),),style={}),                       
                                        html.Div(
                                        html.Div(html.H1(abuja, 
                                                                style={"text-align": "center","color":"#161A1D","background-color":"#E8DAC5",
                                                                       "margin-top":"0","padding": "30px","font-size":"20px"
                                                                       ,"font-family": "Abel","font-weight":"400","font-size": "2em"
                                        
                                                                }),),style={}),
                                                                ],),
                        
                          html.Div(children=[html.Div(
                                        html.Div(html.H1("LAGOS INCOME (N)", 
                                                                style={"text-align": "center","color":"#161A1D","background-color": "#d3bd98",
                                                                       "margin-bottom":"0","padding": "30px","font-size":"20px"
                                                                       ,"font-family": "Abel","font-weight":"600","font-size": "16px"
                                                                       
                                        
                                                                }),),style={}),                       
                                        html.Div(
                                        html.Div(html.H1(lagos, 
                                                                style={"text-align": "center","color":"#161A1D","background-color":"#E8DAC5",
                                                                       "margin-top":"0","padding": "30px","font-size":"20px"
                                                                       ,"font-family": "Abel","font-weight":"400","font-size": "2em"
                                        
                                                                }),),style={}),
                                                                ],),

                        html.Div(children=[html.Div(
                                        html.Div(html.H1("PORT HARCOURT INCOME (N)", 
                                                                style={"text-align": "center","color":"#161A1D","background-color": "#d3bd98",
                                                                       "margin-bottom":"0","padding": "30px","font-size":"20px"
                                                                       ,"font-family": "Abel","font-weight":"600","font-size": "16px"
                                                                       
                                        
                                                                }),),style={}),                       
                                        html.Div(
                                        html.Div(html.H1(pH, 
                                                                style={"text-align": "center","color":"#161A1D","background-color":"#E8DAC5",
                                                                       "margin-top":"0","padding": "30px","font-size":"20px"
                                                                       ,"font-family": "Abel","font-weight":"400","font-size": "2em",
                                                                           
                                        
                                                                }),),style={}),
                                                                ],),
                                                ],
                        style={"display": "flex","background-color": "#0e1012","padding": "30px 0 10px 0","justify-content": "space-around"}),
         
         
        html.Div(dcc.Graph(id='plot1'),
                                                style={"background-color": "#161A1D",
                                                "padding": "60px",},),                       # Create an outer division 
                            
        html.Div(children=[
                        
                        html.Div(dcc.Graph(id='plot2', 
                                                style={"background-color": "#161A1D","text-align": "center",
                                                "height":"70vh"}),),
                        html.Div(dcc.Graph(id='plot3',
                                                style={"background-color": "#161A1D","text-align": "center",
                                                "height":"70vh"}),),],
                        style={"display": "flex","background-color": "#0e1012","padding-bottom": "60px","justify-content": "space-around"}),
                  
        html.Div(children=[
                        
                        html.Div(dcc.Graph(id='plot4', figure = line_fig,
                                                style={"background-color": "#161A1D","text-align": "center",
                                                "height":"70vh"}),),
                        html.Div(dcc.Graph(id='plot5', figure = fig,
                                                style={"background-color": "#161A1D","text-align": "center",
                                                "height":"70vh"}),),],
                        style={"display": "flex","background-color": "#0e1012","padding-bottom": "60px","justify-content": "space-around"}), 
                                   
                     # Graph layout
                               
                                # html.Div(dcc.Graph(figure=tree_fig)),
    
                                # html.Div([
                                #         html.Div(dcc.Graph( figure=bar_fig)),
                                #         html.Div(dcc.Graph(figure=pie_fig))
                                # ], style={'display': 'flex'}),
                                 
                                
                            
                                ],style={"height": "100vh"})

@app.callback( [Output(component_id='plot1', component_property='figure'),
               Output(component_id='plot2',component_property='figure'),
               Output(component_id='plot3',component_property='figure'),],
               [Input(component_id='customer_type', component_property='value'),],
              
              )
# Add computation to callback function and return graph
def get_graph(Customer_type):
       
       if Customer_type == "All Customers":
            
            XYZ_Company_Datasetss = XYZ_Company_Datasets.copy()
            bar_fig = px.bar(XYZ_Company_Datasets, x='Product line', y='Total', color='City', title='TOTAL SALES')
            tree_fig = px.treemap(XYZ_Company_Datasets, 
                            path=['City', 'Product line'], 
                            values='Total',
                            color='Total',
                            color_continuous_scale='RdBu',
                            title='PRODUCT LINE COUNT BY CITY')
            pie_fig = px.pie(XYZ_Company_Datasets, values='gross income', names='City', title='THE SUPERMARKET GROSS INCOME')
       else:
             XYZ_Company_Datasetss = XYZ_Company_Datasets[XYZ_Company_Datasets['Customer type'] == Customer_type]     
             bar_fig = px.bar(XYZ_Company_Datasetss, x='Product line', y='Total', color='City', title='TOTAL SALES')
             tree_fig = px.treemap(XYZ_Company_Datasetss, 
                            path=['City', 'Product line'], 
                            values='Total',
                            color='Total',
                            color_continuous_scale='RdBu',
                            title='PRODUCT LINE COUNT BY CITY')
             pie_fig = px.pie(XYZ_Company_Datasetss, values='gross income', names='City', title='THE SUPERMARKET GROSS INCOME')
              
       return tree_fig,bar_fig,pie_fig




# Run the app
if __name__ == '__main__':
      app.run_server()




