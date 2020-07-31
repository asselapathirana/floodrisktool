import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import utilities
import components as c
import x2d_model as  x2dm
import copy
import flask 
import numpy as np
import base64
import plotly.graph_objects as go
import time
from dash.exceptions import PreventUpdate
import figure 



server = flask.Flask(__name__)
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, server=server)

dirName = './data/sealevels/'
dirName2= './data/upstreamBC/'
filelist = os.listdir(dirName)
filelist2 = os.listdir(dirName2)


options=[{'label':x, 'value':x} for x in filelist]
options2 = [{'label':x, 'value':x} for x in filelist2]
x2d_results = x2dm.read_2d_names()

app.layout = html.Container(
   
    html.Div(
        [
            html.Div([
                html.Row(html.Col(html.Card(html.H1("FLOOD HAZARD AND RISK SIMULATOR"),body=True))),
                html.Row([
                         html.Col(html.Card(html.Div([
                                    html.Div([
                                       html.Div(c.upstream_bc_graph(options2)), 
                                       html.Div(c.static_map(app)),
                                       html.Div(c.sea_level_graph(options)), 
                           
                                   ])
                             ]),body=True), lg=6),
                         html.Col(html.Card(html.Div([
                                  
                                   html.Div(c.land_subs()),
                                   html.Div([
                                       html.Button(
                                                   "Interventions + ",
                                                   id="collapse-button",
                                                   className="mb-3",
                                                   color="primary",
                                               ),
                                       html.Collapse(html.Div(c.intervention()), id="collapse",)
                                       
                                   ]),
                                   dcc.Loading(html.Div([
                                            html.Div(c.div_button_list()),
                                            html.Div(id="trig_fun2", style=dict(display='none')),
                                            html.Div(c.wl_cantho_graph()),
                                            html.Div(id = 'trigger1',children=0, style=dict(display='none')),
                                   ])),                                   
                                  
                                   
                                   html.Div([
                                       dcc.Loading(id="loading-2", 
                                                   children=[            
                                                       html.Div(c.div_button2_list(), style=dict(display='none')),
                                                       html.Div(c.x2d_map()),
                                                       ]),
                                       html.Div(id = 'trigger2',children=0, style=dict(display='none')),
                                   ]),                                   
                             ]),body=True), lg=6),
                 ]),
            ]),
      ]),
    )

                     
            
      
@app.callback(dash.dependencies.Output('button1','disabled'),
              [dash.dependencies.Input('button1','n_clicks'),
               dash.dependencies.Input('trigger1','children')])   
def trigger_function1(n_clicks, trigger):
    if n_clicks is None:
        raise PreventUpdate
    
    context = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    context_value = dash.callback_context.triggered[0]['value']    
    
    if context == 'button1':
        if n_clicks > 0 :
            #print("disabling")
            #return True
            return False
        else:
            return False
    
    else:
        return False    

@app.callback(
    [dash.dependencies.Output('model_output_graph', 'children'),
     dash.dependencies.Output('trigger1','children'),
     dash.dependencies.Output('trig_fun2','children')],
    [dash.dependencies.Input('button1', 'n_clicks')],
    [dash.dependencies.State('graph-from-file', 'figure'),
     dash.dependencies.State('upstreamBC-graph', 'figure')]    
    )
def run_model(n_clicks, fig_sl, fig_us):
    if n_clicks is None:
        raise PreventUpdate
    elif fig_sl and fig_us and fig_sl['data'] and fig_us['data'] :
        sldata=fig_sl['data'][-1]['y']
        usbc1data=fig_us['data'][-2]['y']
        usbc2data=fig_us['data'][-1]['y']
        ret=utilities.run_model(sldata, usbc1data, usbc2data)
        xv,yv = ret
        pty=max(yv)

        ptx= xv[np.argmax(yv, axis=0)]
        print(ptx,pty)
        data=[
                dict(x=xv,
                     y = yv,
                     mode= 'lines',
                     line=dict(color='blue', width=1),
                     name= 'Water level (m)'),  
                dict(x=[ptx],
                    y = [pty],
                    mode='markers',
                    #opacity=1,
                    marker={
                        'size': 5,
                        #'line': {'width': 0.5, 'color': 'white'},
                        'color':'rgb(55, 83, 109)',
                    },
                    
                    name= 'Max. Water level: {:.2f} m'.format(pty)),
                ]        
        new_figure=dcc.Graph(
            figure={
            'data':data,
            'layout':dict(
                xaxis={'title': 'Day No.'},
                yaxis={'title': 'Water level'},
                title = "Water level near Can Tho",
                legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1
                        ),               
            ),
            })
                
            
        #print(max(ret))
        ret= (new_figure)
    else:
        ret=(dcc.Graph(
            figure={'data':[
                         {'x':[],'y':[]}
                        ], 
                 "layout":{}
                 }))
    return [ret,1, pty]


@app.callback(dash.dependencies.Output('button2','disabled'),
              [dash.dependencies.Input('button2','n_clicks'),
               dash.dependencies.Input('trigger2','children'),
               dash.dependencies.Input('button1', 'children')])   
def trigger_function2(n_clicks2, trigger, n_clicks1):
    
    context = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    context_value = dash.callback_context.triggered[0]['value']    
    
    if context == 'button2':
        if n_clicks2 is None:
            raise PreventUpdate        
        if n_clicks2 > 0 :
            print("disabling")
            #return True
            return False
        else:
            if context == 'button1':
                if n_clicks1 is None:
                    raise PreventUpdate                
                if n_clicks1 >0 :
                    return False
            return False
    
    else:
        return False    


@app.callback(
    [dash.dependencies.Output('x2d_map', 'children'),
     dash.dependencies.Output('trigger2','children')],
    [dash.dependencies.Input('button2', 'n_clicks'),
     dash.dependencies.Input('trig_fun2', 'children')],
    [dash.dependencies.State('model_output_graph', 'children'),
     dash.dependencies.State('land_sub', 'value'),
     dash.dependencies.State('land_subCont','value'),
     ]    
    )
def run_model2D(n_clicks, mwl, wl_fig, lsub, lsubC): 
    if wl_fig and wl_fig['props'] and wl_fig['props']['figure'] and wl_fig['props']['figure']['data']:
        max_l=wl_fig['props']['figure']['data'][-1]['y'][0]
        _max_l=max_l + lsub*(100.-lsubC)/100.
        import time
        
        start = time.time()
      
        res = x2dm.get_image(x2d_results, _max_l)
        p1 = time.time()
        
        g1=dcc.Graph(id="graphxx1", figure = figure.get_figure(app,res[1]), 
                     #layout=go.Layout(title=go.layout.Title(text="Inundation depth(m)")),
                     )
        p2=time.time()
        g2=dcc.Graph(id="graphxx2", figure = figure.get_figure(app,res[2]), 
                     #layout=go.Layout(title=go.layout.Title(text="Damage per unit area($/m^2))")),
                     )        
        p3=time.time()
        print(p1 - start, p2-start, p3-start) 
        ret=[html.H4("Flood inundation"),html.H5("Estimated damage due to the flood event {:.2f} mil. USD".format(res[0])),
            g1,
            g2]
    else:
        ret=[]
    return [ret,1]
    
@app.callback(
    dash.dependencies.Output('graph-from-file', 'figure'),
    [dash.dependencies.Input('fileSet', 'value'),
     dash.dependencies.Input('day-slider', 'value'),
     dash.dependencies.Input('level-dif','value')
    ],
     [dash.dependencies.State('graph-from-file', 'relayoutData')])
def update_sealevel_plot(value, day, dif, relayout_data):
    filePath = os.path.join(dirName, value)
    df=utilities.read_sealevel(filePath)
    df['Day']=df['Day'] - day/24.
    df=df[df['Day']>=0.0]
    data=[
            dict(x=df['Day'],
                 y=df['level']+dif,
                 mode= 'lines',
                 line=dict(color='blue', width=2),
                 name= 'Sea level + '+str(dif),)        
            ]
    if dif!=0:
        data.insert(0,
                    dict(x = df['Day'],
                            y = df['level'],
                            mode = 'lines', 
                            name = 'Sea level',
                            line=dict(color='orange', width=1, dash='dot'),
                        )                  
                    )    
    new_figure={
        'data':data,
        'layout':dict(
            xaxis={'title': 'Day No.'},
            yaxis={'title': 'Sealevel'},
            legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    ),               
                                  
        ),
        }
        
    
    # relayout_data contains data on the zoom and range actions
    
    if relayout_data :
        if 'xaxis.range[0]' in relayout_data:
            new_figure['layout']['xaxis']['range'] = [
                relayout_data['xaxis.range[0]'],
                relayout_data['xaxis.range[1]']
            ]
        if 'yaxis.range[0]' in relayout_data:
            new_figure['layout']['yaxis']['range'] = [
                relayout_data['yaxis.range[0]'],
                relayout_data['yaxis.range[1]']
            ]

    return new_figure    


@app.callback(
    dash.dependencies.Output('upstreamBC-graph', 'figure'),
    [dash.dependencies.Input('fileSet2', 'value'),
     dash.dependencies.Input('bc-multi', 'value'),
     dash.dependencies.Input('dams-effect','value')],
    [dash.dependencies.State('upstreamBC-graph', 'relayoutData')])
def update_upstreambc_plot(value, expol, redvalue, relayout_data):
    filePath2 = os.path.join(dirName2, value)
    df2=utilities.read_flow(filePath2)
    df2['Flow1'] = df2['Flow1']
    
    data=[
        dict(x = df2.index,
            y = df2['Flow1']*expol,
            mode = 'lines',
            line=dict(color='orange', width=2),
            name = 'Flow1 * '+ str(expol),
        ),
                
        dict(x = df2.index,
            y = df2['Flow2']*expol,
            mode = 'lines',
            line= dict(color='red', width=2),
            name = 'Flow2 * '+ str(expol),
            yaxis='y2'
        ),                        
             
            ]
    if expol!=1:
        data.insert(0,
                    dict(x = df2.index,
                         y = df2['Flow1'],
                         mode = 'lines', 
                         name = 'Flow1',
                         line=dict(color='orange', width=1, dash='dot'),
                        ), 
                    ),
        data.insert(0,
                    dict(x = df2.index,
                         y = df2['Flow2'],
                         mode = 'lines',
                         name = 'Flow2',
                         line= dict(color='red', width=1, dash='dot'),
                        ),
                    ),
    if redvalue!=0:
        data.append(
                  dict(x = df2.index,
                    y = df2['Flow1']*expol*((100-redvalue)/100),
                    mode = 'lines',
                    line=dict(color='green', width=2),
                    name = 'Flow1 reduced',
                    ),
                    ),
        data.append(
                  dict(x = df2.index,
                    y = df2['Flow2']*expol*((100-redvalue)/100),
                    mode = 'lines',
                    line=dict(color='blue', width=2),
                    name = 'Flow2 reduced',
                    ),
                    )        
        
    res= {
        'data': data
        ,
        'layout': dict(
            xaxis={'title': 'Day No.'},
            #yaxis={'title': 'Flow1'},
            yaxis=dict(
                        title='Flow1'
                    ),
            yaxis2=dict(
                title='Flow2',
                overlaying='y',
                side='right',
                color='black'
            ),
            legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    ),               
            

        )

    }
    
        
    
    if relayout_data :
        if 'xaxis.range[0]' in relayout_data:
            res['layout']['xaxis']['range'] = [
                relayout_data['xaxis.range[0]'],
                relayout_data['xaxis.range[1]'],
                #relayout_data['xaxis.range[2]']
            ]
        if 'yaxis.range[0]' in relayout_data:
            res['layout']['yaxis']['range'] = [
                relayout_data['yaxis.range[0]'],
                relayout_data['yaxis.range[1]'],
                relayout_data['yaxis2.range[0]'],
                relayout_data['yaxis2.range[1]'],
            ]
    
    return res

@app.callback(dash.dependencies.Output("collapse","is_open"),
              [dash.dependencies.Input("collapse-button","n_clicks")],
              [dash.dependencies.State("collapse","is_open")],
              )
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == '__main__':
    app.run_server(debug=True)
