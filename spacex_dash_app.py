# Import required libraries
import pandas as pd
import dash
from dash import html,dcc
from dash.dependencies import Input, Output
import plotly.express as px
import wget

wget.download("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")


# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()


# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                            options=[
                                                         {'label': 'ALL SITES', 'value': 'ALL'},
                                                         {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                         {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                         {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                         {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                                    ],
                                            value='ALL',
                                            placeholder="Select a Launch Site here", 
                                            searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,max=10000,step=1000,
                                                marks={0: '0', 2500:'2500',5000:'5000',
                                                7500:'7500', 10000: '10000'},
                                                value=[min_payload,max_payload]),
                                               
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'))

def build_graph(entered_site):
    if entered_site == 'ALL':
        pie = px.pie(data_frame = spacex_df, names='Launch Site', values='class' ,title='Total Launches by Site')
        return pie
    else:
        selected_df=spacex_df.loc[spacex_df['Launch Site'] == entered_site]
        piechart = px.pie(data_frame = selected_df, names='class',title=f'Total Success Launch for Site {entered_site}')
        return piechart

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')])

def scatter_chart(entered_site, slider):
    if entered_site == 'ALL':
        filtered_data = spacex_df[(spacex_df['Payload Mass (kg)']>=slider[0])
        &(spacex_df['Payload Mass (kg)']<=slider[1])]
        scatter = px.scatter(data_frame=filtered_data, x="Payload Mass (kg)", y="class", 
        color="Booster Version Category",title="Correlation between Payload and Success for all Sites")
        return scatter
    else:
        selected_df=spacex_df.loc[spacex_df['Launch Site'] == entered_site]
        filtered_data = selected_df[(selected_df['Payload Mass (kg)']>=slider[0])
        &(selected_df['Payload Mass (kg)']<=slider[1])]
        scatter = px.scatter(data_frame=filtered_data, x="Payload Mass (kg)", y="class", 
        color="Booster Version Category")
        return scatter

# Run the app
if __name__ == '__main__':
    app.run_server()
