import py_dss_interface
import numpy as np
import pandas as pd
import plotly.express as px



#realizando a integração dss com o pyhton
dss_file = r"C:\py-dss-interface_pg\pythonProject\Microgrid_test\15m.dss"
dss = py_dss_interface.DSS()
dss.text("compile [{}]".format(dss_file))
dss.solution.solve()


dss.monitors.first()
dss.monitors.next()

dataframe_powers = pd.DataFrame(index=range(96), columns=['V1'])
for i in range(29):
    dss.monitors.next()
    dataframe_powers['V1'] = dss.monitors.channel(1)[:96]
    plot_powers_after = px.line(dataframe_powers, x=dataframe_powers.index/4, y=dataframe_powers.columns[0:])
    plot_powers_after.update_layout(
        xaxis_title="Tempo (h)",
        yaxis_title="Tensão (V)",
        legend_title="Legenda",
        plot_bgcolor="white",
        font=dict(size=25)
    )
    plot_powers_after.update_xaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey'
    )
    plot_powers_after.update_yaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey',
        dtick=5
    )
    plot_powers_after.show()
