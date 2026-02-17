from route_finder import RouteFinder, StreamlitApp

route_finder = RouteFinder("Paris, France", network_type="drive")

app = StreamlitApp(route_finder)
app.run()