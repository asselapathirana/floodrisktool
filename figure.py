import plotly.graph_objects as go

def get_figure(app,filename):
    
    fig = go.Figure()
    
    # Add image
    img_width = 1753
    img_height = 1241
    scale_factor = 0.25
    # Add invisible scatter trace.
    # This trace is added to help the autoresize logic work.
    fig.add_trace(
        go.Scatter(
            x=[0, img_width * scale_factor],
            y=[0, img_height * scale_factor],
            mode="markers",
            marker_opacity=0
        )
    )
    
    # Configure axes
    fig.update_xaxes(
        visible=False,
        range=[0, img_width * scale_factor]
    )
    
    fig.update_yaxes(
        visible=False,
        range=[0, img_height * scale_factor],
        # the scaleanchor attribute ensures that the aspect ratio stays constant
        scaleanchor="x"
    )
    
    # Add image
    fig.add_layout_image(
        dict(
            x=0,
            sizex=img_width * scale_factor,
            y=img_height * scale_factor,
            sizey=img_height * scale_factor,
            xref="x",
            yref="y", 
            opacity=1.0,
            layer="below",
            sizing="stretch",
           source=app.get_asset_url(filename)
    )
        )
    
    # Configure other layout
    fig.update_layout(
        #width=img_width * scale_factor*1.25,
        #height=img_height * scale_factor*1.25,
        margin={"l": 0, "r": 0, "t": 20, "b": 0},
    )
        
      
    #            
 
    return fig