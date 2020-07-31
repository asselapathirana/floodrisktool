import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

def upstream_bc_graph(options2):
    upstream_bc = [html.Div([
                        html.H3("Upstream boundary conditions"),
                            html.Div([
                                html.Div([
                                    html.H5("Select Dataset"),
                                    dcc.Dropdown(
                                    id = "fileSet2",
                                    options = options2,
                                    placeholder = 'Select a dataset',
                                    value = options2[0]['value'],
                                    )]), 
                                html.Div([
                                    html.Div([
                                            html.H5("Scale up/down multiplier (-)"),                                
                                            dcc.Slider(
                                              id='bc-multi',
                                              min=0.5,
                                              max=1.5,
                                              value=1,
                                              marks={0.5:'0.5', 1:'1', 1.5:'1.5'},
                                              step=0.1),
                                      ]),
                                     
                                ]),
                            ]),
                        
                        dcc.Graph(id = 'upstreamBC-graph'),  
                        ]),
                    ]
    return upstream_bc


def static_map(app):
    img = [ html.Div(
            [
                html.Img(
                    src=app.get_asset_url('map1.png'),
                    className="img-fluid",
                         ),
            ]
          
                )
            ]
    return img
def sea_level_graph(options):
    sea_level = [html.Div([
            html.H3("Sealevel distribution"),     
                    html.Div([html.Div([
                        html.H5("Select Dataset"),
                        dcc.Dropdown(
                            id="fileSet",
                            options=options,
                            placeholder='Select a dataset',
                            value=options[0]['value'],
                            ), ]), 
                    html.Div([
                        html.H5("Phase change (h)"),
                        dcc.Slider(
                            id='day-slider',
                            min=0,
                            max=24,
                            value=0,
                            marks={0:'0hr', 12:'12hr', 24:'24hr'},
                            step=0.1
                            ),                 
                        html.H5("Increase sea-level (m)"),
                        dcc.Slider(
                            id='level-dif',
                            min=0,
                            max=2,
                            value=0,
                            marks={0:'0', 1:'1', 2:'2'},
                            step=0.1
                            ), ]), 
                    ]), 
                    
            
            dcc.Graph(id='graph-from-file'),
            ]),
            ]
    return sea_level

def div_button_list():
    return  [
             dbc.Button('Run model', id='button1'),
            ]

def wl_cantho_graph():
    wl_cantho = [
                html.Div(id="model_output_graph"),
               ]
    return wl_cantho


def div_button2_list():
    return  [
             dbc.Button('Run 2D urban flood model', id='button2', disabled=True),
            ]

def x2d_map():
    wl_cantho = [
                html.Div(id = "x2d_map"),
            ]
    return wl_cantho

def land_subs():
    return [
            html.Div([
                    html.H5("Land subsidence (m)"),                                
                    dcc.Slider(
                      id='land_sub',
                      min=0,
                      max=2,
                      value=0,
                      marks={0:'0.0', 0.5:'0.5', 1:'1', 1.5:'1.5', 2:'2'},
                      step=0.1),
              ]),          
        ]

def intervention():
    return [
        html.Div([
               html.H5("Intervention 1 - Reduction of flow due to dams upstream (%)"),                                
               dcc.Slider(
                 id='dams-effect',
                 min=0,
                 max=15,
                 value=0,
                 marks={0:'0', 5:'5',10:'10', 15:'15'},
                 step=0.1),
        ]),            
        
        html.Div([
                html.H5("Intervention  2 - Land subsistence control in Can Tho city (%)"),                                
                dcc.Slider(
                  id='land_subCont',
                  min=0,
                  max=100,
                  value=0,
                  marks={x:str(x) for x in range(0,101,10)},
                  step=1),
          ]),          
    ]
    


