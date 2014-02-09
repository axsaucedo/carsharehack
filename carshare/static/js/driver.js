var driver = {
    init : function() {

        var get_passengers_url = $("#driver-site-info").attr("data-get_passengers");
        var passenger_container = $("#passengers-container");

//        function getCookie(name) {
//            var cookieValue = null;
//            if (document.cookie && document.cookie != '') {
//                var cookies = document.cookie.split(';');
//                for (var i = 0; i < cookies.length; i++) {
//                    var cookie = jQuery.trim(cookies[i]);
//                    // Does this cookie string begin with the name we want?
//                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
//                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                        break;
//                    }
//                }
//            }
//            return cookieValue;
//        }
//        var csrftoken = getCookie('csrftoken');
//
//        console.log(csrftoken);
//
//        function csrfSafeMethod(method) {
//            // these HTTP methods do not require CSRF protection
//            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
//        }
//        $.ajaxSetup({
//            crossDomain: false, // obviates need for sameOrigin test
//            beforeSend: function(xhr, settings) {
//                if (!csrfSafeMethod(settings.type)) {
//                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
//                }
//            }
//        });

        function ajax_get_passengers(latitude, longitude) {

            $.ajax({
                url: "/api/drivers/?format=json",
                dataType: "json",
                type: "GET",
                contentType: "application/json",
                data: {
                    latitude: latitude,
                    longitude: longitude,
//                    csrfmiddlewaretoken: csrftoken,
                },
                success : function(res) {
                    if (!res.error) {
                        console.log(res);
                    } else {

                    }
                }
            });

//            var frm = $('#driver-form');
//            console.log(frm.attr('action'));
//
//            function ajax_get_passengers(latitude, longitude) {
//
//                frm.submit(function () {
//                    $.ajax({
//                        url: frm.attr('action'),
//                        dataType: "json",
//                        type: "POST",
//                        contentType: "application/json",
//                        success: function (data) {
//                            console.log("hei");
//                        },
//                        error: function(data) {
//                            console.log("nope")
//                        }
//                    });
//                    return false;
//                });
//
//                console.log("submitted")
//
//                frm.submit();
//            }

//            setTimeout(function() { ajax_get_passengers(latitude, longitude) }, 1000);
        }

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

            $('#driver-form-lat').attr("value", position.coords.latitude);
            $('#driver-form-longx').attr("value", position.coords.longitude);

            ajax_get_passengers(position.coords.latitude, position.coords.longitude);

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
    driver.init();
});
