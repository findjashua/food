function initialize() {
	var map
	var mapOptions = {
		zoom: 16
	}
	map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions)
	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(function(position) {
			var pos = new google.maps.LatLng(position.coords.latitude, position.coords.longitude)
			map.setCenter(pos)
			getNearby(map)
		}, function() {
			handleNoGeolocation(true)
		})
	}
	google.maps.event.addListener(map, 'center_changed', function() {
		getNearby(map)
	})
}

function handleNoGeolocation(errorFlag) {
	if (errorFlag) {
		var content = 'Error: the geolocation service failed'
	} else {
		content = 'Your browser does not support geolocation'
	}

	var options = {
		map: map,
		position: new google.maps.LatLng(37, -122),
		content: content
	}
	map.setCenter(options.position)
	getNearby(map)
}

function getNearby(map) {
	loc = map.getCenter()
	$.ajax({
		url: '/near/' + loc.nb + '/' + loc.ob,
		success: function(data) {
			data = $.parseJSON(data)
			for (var i=0; i<data.length; i++) {
				var lat = parseFloat(data[i].latitude)
				var lng = parseFloat(data[i].longitude)
				var marker = new google.maps.Marker({
					position: new google.maps.LatLng(lat, lng),
					map: map,
					title: 'Food trucks near you'
				})
				addClickListenerToMarker(marker, data[i])
			}
		}
	})
}

function addClickListenerToMarker(marker, data) {
	google.maps.event.addListener(marker, 'click', function() {
		window.alert(data.applicant + ', ' + data.address)
	})
}

google.maps.event.addDomListener(window, 'load', initialize)