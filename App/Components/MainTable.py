from Components import LoadData
import dash_table #plotly.graph_objects as go


df = LoadData.dataBase
df['Hora de llegada'] = '--'

fig =  dash_table.DataTable(
        id='mainTable',
        columns=[{"name": i, "id": i} 
                 for i in df.columns],
        data=df.to_dict('records'),
        style_cell=dict(textAlign='left'),
        style_header=dict(backgroundColor="paleturquoise"),
        style_data=dict(backgroundColor="lavender")
    )

