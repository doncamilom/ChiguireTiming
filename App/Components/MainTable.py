from Components import LoadData
import dash_table 


df = LoadData.dataBase
df['Hora de llegada'] = None
df['Tiempo de carrera'] = None
df['Segundos de diferencia categ'] = None

fig =  dash_table.DataTable(
        id='mainTable',
        columns=[{"name": i, "id": i} 
                 for i in df.columns],
        data=df.to_dict('records'),
        style_cell=dict(textAlign='left'),
        style_header=dict(backgroundColor="paleturquoise"),
        style_data=dict(backgroundColor="lavender"),
        
        filter_action="native",

        sort_action="custom",
        sort_mode="single",
    )

