from Components import LoadData
import dash_table 


df, isDF = LoadData.LoadPrerecordedResults()
if isDF:   df = df.to_dict("records")
#df['Hora de llegada'] = None
#df['Tiempo de carrera'] = None
#df['Segundos de diferencia categ'] = None

fig =  dash_table.DataTable(
        id='mainTable',
        columns=[{"name": i, "id": i} 
                 for i in ["NOMBRE","NÚMERO","CATEGORIA","HORA SALIDA","HORA LLEGADA","TOTAL","POSICIÓN"]],
        data=df,
        style_cell=dict(textAlign='center'),
        style_header=dict(backgroundColor="#c8df52"),
        style_data=dict(backgroundColor="#dbe8d8"),
        
        filter_action="native",

        sort_action="custom",
        sort_mode="single",
    )

