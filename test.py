import py_dss_interface
import numpy as np
import pandas as pd
import plotly.express as px



#realizando a integração dss com o pyhton
dss_file = r"C:\py-dss-interface_pg\pythonProject\Microgrid_test\15m.dss"
dss = py_dss_interface.DSS()
dss.text("compile [{}]".format(dss_file))


#plotando saida da bateria - MICROGRID
dss.monitors.first()

dataframe_powers = pd.DataFrame(index=range(96), columns=['Pa (kW)', 'Qa (kvar)', 'Pb (kW)', 'Qb (kvar)', 'Pc (kW)', 'Qc (kvar)'])
dataframe_powers['Pa (kW)'] = dss.monitors.channel(1)[:96]
dataframe_powers['Qa (kvar)'] = dss.monitors.channel(2)[:96]
dataframe_powers['Pb (kW)'] = dss.monitors.channel(3)[:96]
dataframe_powers['Qb (kvar)'] = dss.monitors.channel(4)[:96]
dataframe_powers['Pc (kW)'] = dss.monitors.channel(5)[:96]
dataframe_powers['Qc (kvar)'] = dss.monitors.channel(6)[:96]

dataframe_total = pd.DataFrame(index=range(96), columns=['Pt (kW)', 'Qt (kvar)'])
dataframe_total['Pt (kW)'] = dataframe_powers['Pa (kW)'] + dataframe_powers['Pb (kW)'] + dataframe_powers['Pc (kW)']
dataframe_total['Qt (kvar)'] = dataframe_powers['Qa (kvar)'] + dataframe_powers['Qb (kvar)'] + dataframe_powers['Qc (kvar)']


plot_powers_after = px.line(dataframe_total, x=dataframe_total.index/4, y=dataframe_total.columns[0:])
plot_powers_after.update_layout(
    xaxis_title="Tempo (h)",
    yaxis_title="Potência (kW, kvar)",
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


#plotando o estado da bateria em relação a carga.
dss.monitors.next()
auxiliar = pd.DataFrame(index=range(96), columns=["kwh"])
auxiliar['kwh'] = dss.monitors.channel(1)[:96]
plot_powers_after2 = px.line(auxiliar, x=auxiliar.index/4, y=auxiliar.columns[0:])
plot_powers_after2.update_layout(
    xaxis_title="Tempo (h)",
    yaxis_title="Kwh",
    legend_title="Legenda",
    plot_bgcolor="white",
    font=dict(size=15)
)
plot_powers_after2.update_xaxes(
    mirror=True,
    ticks='outside',
    showline=True,
    linecolor='black',
    gridcolor='lightgrey'
)
plot_powers_after2.update_yaxes(
    mirror=True,
    ticks='outside',
    showline=True,
    linecolor='black',
    gridcolor='lightgrey',
    dtick=5
)
plot_powers_after2.show()







#plotando visão geral da potencia do circuito
dss.monitors.next()
dataframe_power_2 = pd.DataFrame(index=range(96), columns=['Pa (kW)', 'Qa (kvar)', 'Pb (kW)', 'Qb (kvar)', 'Pc (kW)', 'Qc (kvar)'])
dataframe_power_2['Pa (kW)'] = dss.monitors.channel(1)[:96]
dataframe_power_2['Qa (kvar)'] = dss.monitors.channel(2)[:96]
dataframe_power_2['Pb (kW)'] = dss.monitors.channel(3)[:96]
dataframe_power_2['Qb (kvar)'] = dss.monitors.channel(4)[:96]
dataframe_power_2['Pc (kW)'] = dss.monitors.channel(5)[:96]
dataframe_power_2['Qc (kvar)'] = dss.monitors.channel(6)[:96]

dataframe_total_2 = pd.DataFrame(index=range(96), columns=['Pt (kW)', 'Qt (kvar)'])
dataframe_total_2['Pt (kW)'] = dataframe_power_2['Pa (kW)'] + dataframe_power_2['Pb (kW)'] + dataframe_power_2['Pc (kW)']
dataframe_total_2['Qt (kvar)'] = dataframe_power_2['Qa (kvar)'] + dataframe_power_2['Qb (kvar)'] + dataframe_power_2['Qc (kvar)']


plot_powers_after3 = px.line(dataframe_total_2, x=dataframe_total_2.index/4, y=dataframe_total_2.columns[0:])
plot_powers_after3.update_layout(
    xaxis_title="Tempo (h)",
    yaxis_title="Potência (kW, kvar)",
    legend_title="Legenda",
    plot_bgcolor="white",
    font=dict(size=15)
)
plot_powers_after3.update_xaxes(
    mirror=True,
    ticks='outside',
    showline=True,
    linecolor='black',
    gridcolor='lightgrey'
)
plot_powers_after3.update_yaxes(
    mirror=True,
    ticks='outside',
    showline=True,
    linecolor='black',
    gridcolor='lightgrey',
    dtick=5
)
plot_powers_after3.show()

dss.monitors.next()
line_1 = pd.DataFrame(index=range(96), columns=['Pa (kW)', 'Qa (kvar)', 'Pb (kW)', 'Qb (kvar)', 'Pc (kW)', 'Qc (kvar)'])
line_1['Pa (kW)'] = dss.monitors.channel(1)[:96]
line_1['Qa (kvar)'] = dss.monitors.channel(2)[:96]
line_1['Pb (kW)'] = dss.monitors.channel(3)[:96]
line_1['Qb (kvar)'] = dss.monitors.channel(4)[:96]
line_1['Pc (kW)'] = dss.monitors.channel(5)[:96]
line_1['Qc (kvar)'] = dss.monitors.channel(6)[:96]

dss.monitors.next()
line_2 = pd.DataFrame(index=range(96), columns=['Pa (kW)', 'Qa (kvar)', 'Pb (kW)', 'Qb (kvar)', 'Pc (kW)', 'Qc (kvar)'])
line_2['Pa (kW)'] = dss.monitors.channel(1)[:96]
line_2['Qa (kvar)'] = dss.monitors.channel(2)[:96]
line_2['Pb (kW)'] = dss.monitors.channel(3)[:96]
line_2['Qb (kvar)'] = dss.monitors.channel(4)[:96]
line_2['Pc (kW)'] = dss.monitors.channel(5)[:96]
line_2['Qc (kvar)'] = dss.monitors.channel(6)[:96]

dss.monitors.next()
line_3 = pd.DataFrame(index=range(96), columns=['Pa (kW)', 'Qa (kvar)', 'Pb (kW)', 'Qb (kvar)', 'Pc (kW)', 'Qc (kvar)'])
line_3['Pa (kW)'] = dss.monitors.channel(1)[:96]
line_3['Qa (kvar)'] = dss.monitors.channel(2)[:96]
line_3['Pb (kW)'] = dss.monitors.channel(3)[:96]
line_3['Qb (kvar)'] = dss.monitors.channel(4)[:96]
line_3['Pc (kW)'] = dss.monitors.channel(5)[:96]
line_3['Qc (kvar)'] = dss.monitors.channel(6)[:96]

dss.monitors.next()
line_4 = pd.DataFrame(index=range(96), columns=['Pa (kW)', 'Qa (kvar)', 'Pb (kW)', 'Qb (kvar)', 'Pc (kW)', 'Qc (kvar)'])
line_4['Pa (kW)'] = dss.monitors.channel(1)[:96]
line_4['Qa (kvar)'] = dss.monitors.channel(2)[:96]
line_4['Pb (kW)'] = dss.monitors.channel(3)[:96]
line_4['Qb (kvar)'] = dss.monitors.channel(4)[:96]
line_4['Pc (kW)'] = dss.monitors.channel(5)[:96]
line_4['Qc (kvar)'] = dss.monitors.channel(6)[:96]

dss.monitors.next()
line_5 = pd.DataFrame(index=range(96), columns=['Pa (kW)', 'Qa (kvar)', 'Pb (kW)', 'Qb (kvar)', 'Pc (kW)', 'Qc (kvar)'])
line_5['Pa (kW)'] = dss.monitors.channel(1)[:96]
line_5['Qa (kvar)'] = dss.monitors.channel(2)[:96]
line_5['Pb (kW)'] = dss.monitors.channel(3)[:96]
line_5['Qb (kvar)'] = dss.monitors.channel(4)[:96]
line_5['Pc (kW)'] = dss.monitors.channel(5)[:96]
line_5['Qc (kvar)'] = dss.monitors.channel(6)[:96]
linha_total = pd.DataFrame(index=range(96), columns=['Pta (kW)', 'Ptb (kW)','Ptc (kW)'])
linha_total['Pta (kW)'] = line_1['Pa (kW)'] + line_2['Pa (kW)'] + line_3['Pa (kW)'] + line_4['Pa (kW)'] + line_5['Pa (kW)']
linha_total['Ptb (kW)'] = line_1['Pb (kW)'] + line_2['Pb (kW)'] + line_3['Pb (kW)'] + line_4['Pb (kW)'] + line_5['Pb (kW)']
linha_total['Ptc (kW)'] = line_1['Pc (kW)'] + line_2['Pc (kW)'] + line_3['Pc (kW)'] + line_4['Pc (kW)'] + line_5['Pc (kW)']
linha_total_test = pd.DataFrame(index=range(96), columns=['Pt (kW)'])
linha_total_test['Pt (kW)'] = linha_total['Pta (kW)'] + linha_total['Ptb (kW)'] + linha_total['Ptc (kW)']
plot_powers_after_4 = px.line(linha_total_test, x=linha_total_test.index/4, y=linha_total_test.columns[0:])
plot_powers_after_4.update_layout(
    xaxis_title="Tempo (h)",
    yaxis_title="Potência (kW, kvar)",
    legend_title="Legenda",
    plot_bgcolor="white",
    font=dict(size=25)
)
plot_powers_after_4.update_xaxes(
    mirror=True,
    ticks='outside',
    showline=True,
    linecolor='black',
    gridcolor='lightgrey'
)
plot_powers_after_4.update_yaxes(
    mirror=True,
    ticks='outside',
    showline=True,
    linecolor='black',
    gridcolor='lightgrey',
    dtick=5
)
plot_powers_after_4.show()
