import datetime
from bokeh.plotting import figure, show

def bar_with_time_series(dates, y, title= None, height = 250):
    p = figure(title=title,
               toolbar_location=None, tools="",
               x_axis_type="datetime",
               y_range = (0,3000),
               height = height
               )

    p.vbar(x=dates, top=y, 
           width=datetime.timedelta(days=1) - datetime.timedelta(days=.5)
           )
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    return p

def bar_simp(cats, y, title = None):
    p = figure(x_range=cats, height=350, title=title,
               toolbar_location=None, tools="")

    p.vbar(x=cats, top=y, width=0.9)
    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    show(p)


