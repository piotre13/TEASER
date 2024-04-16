import geopandas
import folium, io
from folium.plugins import Draw
from folium_jsbutton import JsButton
import webbrowser
import json
download_folder = '/data'

world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
cities = geopandas.read_file(geopandas.datasets.get_path('naturalearth_cities'))

m = world.explore()


#folium.TileLayer('Stamen Toner', control=True).add_to(m)  # use folium to add alternative tiles
  # use folium to add layer control

Draw(

    export=True,

    filename="/my_data.geojson",

    position="topleft",

    draw_options={"polyline": {"allowIntersection": False}},

    edit_options={"poly": {"allowIntersection": False}},

    show_geometry_on_click = True

).add_to(m)

# JsButton(
#     title='<i class="fas fa-crosshairs"></i>',function="""
#     function(btn, map) {
#        saveAs(drawnItems.toGeoJSON(),"drawnItems");
#     }
#     """).add_to(m)
#modify script tag contents to automate the savings into data folder


script_addition = ''' 
<head>
<script src="https://cdnjs.cloudflare.com/ajax/libs/FileSaver.js/2.0.5/FileSaver.min.js"></script>
 
<script>
</head>
<body>
   <style>
                #export {
                    position: absolute;
                    top: 5px;
                    right: 10px;
                    z-index: 999;
                    background: white;
                    color: black;
                    padding: 6px;
                    border-radius: 4px;
                    font-family: 'Helvetica Neue';
                    cursor: pointer;
                    font-size: 12px;
                    text-decoration: none;
                    top: 90px;
                }
            </style>
            <a href='#' id='export'>Export</a>
            
             document.getElementById('export').onclick = function(e) {
                var data = drawnItems.toGeoJSON();
                var convertedData = 'text/json;charset=utf-8,'
                    + encodeURIComponent(JSON.stringify(data));
                document.getElementById('export').setAttribute(
                    'href', 'data:' + convertedData
                );
                document.getElementById('export').setAttribute(
                    'download', "/my_data.geojson"
                );
                saveAs (convertedData);
   </body>         }'''

# m.get_root().render()
# # script =f"""
# #        {m.get_name()}.on('layeradd', function(e) {{
# #        layer = e.layer;
# #        if (layer.toGeoJSON()) {{
# #        document.getElementById('export').click()}} }})"""
# e = folium.Element(script_addition)
# html = m.get_root()
# html.script.add_child(e)


# Add a callback to handle drawn objects
# m.add_child(folium.features.FeatureGroup(name='drawn_objects').add_child(
#     folium.features.TopoJson(
#         data='{}',
#         object_path='objects.geojson',
#         style_function=lambda x: {'color': 'red', 'fillOpacity': 0.1},
#         onEachFeature=handle_drawn_object
#     )
# ))
folium.LayerControl().add_to(m)
m.show_in_browser()
#m.save('example.html')

webbrowser.open('map_template.html')
print('stocazzo')

