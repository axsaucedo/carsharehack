var passenger = {
    init : function() {

        $("#find-location-button").bind("click", function lookupGeoData() {
            console.log("here");
            myGeoPositionGeoPicker({
                startAddress     : 'White House, Washington',
                returnFieldMap   : {
                    'passenger-form-dest-lat' : '<LAT>',
                    'passenger-form-dest-long' : '<LNG>',
                    'passenger-form-city' : '<CITY>',
                    'passenger-form-country' : '<COUNTRY>',
                    'passenger-form-zip' : ' <ZIP>',
                    'passenger-form-address' : '<ADDRESS>'
                }
            });
        });


        function success(position) {
            var s = document.querySelector('#status');

            if (s.className == 'success') {
                // not sure why we're hitting this twice in FF, I think it's to do with a cached result coming back
                return;
            }

            s.innerHTML = "found you!";
            s.className = 'success';

            var mapcanvas = document.createElement('div');
            mapcanvas.id = 'mapcanvas';
            mapcanvas.style.height = '250px';
            mapcanvas.style.width = '100%';

            document.querySelector('article').appendChild(mapcanvas);

            var latlng = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);

            $('#passenger-form-curr-lat').attr("value", position.coords.latitude);
            $('#passenger-form-curr-long').attr("value", position.coords.longitude);

            var myOptions = {
                zoom: 15,
                center: latlng,
                mapTypeControl: false,
                navigationControlOptions: {style: google.maps.NavigationControlStyle.SMALL},
                mapTypeId: google.maps.MapTypeId.ROADMAP
            };
            var map = new google.maps.Map(document.getElementById("mapcanvas"), myOptions);

            var marker = new google.maps.Marker({
                position: latlng,
                map: map,
                title:"You are here! (at least within a "+position.coords.accuracy+" meter radius)"
            });
        }

        function error(msg) {
            var s = document.querySelector('#status');
            s.innerHTML = typeof msg == 'string' ? msg : "failed";
            s.className = 'fail';

            // console.log(arguments);
        }

        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(success, error);
        } else {
            error('not supported');
        }

    }
}

$(function() {
    passenger.init();
});