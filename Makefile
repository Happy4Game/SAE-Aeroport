all : 
	@del -R html
	@pdoc -o html ./AirportInfoWidget.py ./AirportListWidget.py ./BddControler.py ./CountryListWidget.py ./Main.py ./RouteWidget.py ./ViewDataCo2Widget.py ./ViewDataRouteWidget.py ./ViewDataWidget.py