const CACHE = 'metropolis-v1';

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE).then(cache => {
            return cache.addAll([
                '/offline/',
                '/static/css/materialize.min.css',
                '/static/css/material-design-iconic-font.min.css',
                '/static/css/fullcalendar.min.css',
                '/static/css/select2.min.css',
                '/static/css/mapbox-gl.css',
                '/static/css/mapbox-gl-geocoder.css',
                '/static/js/materialize.min.js',
                '/static/js/jquery-3.6.0.min.js',
                '/static/js/fullcalendar.min.js',
                '/static/js/select2.min.js',
                '/static/js/quicklink.umd.js',
                '/static/js/mapbox-gl.js',
                '/static/js/mapbox-gl-geocoder.min.js',
                '/static/core/img/logo-light-transparent.png',
                '/static/core/img/logo-dark-transparent.png',
                '/static/fonts/Material-Design-Iconic-Font.woff2',
            ]);
        })
    );
});

self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(keys => Promise.all(
            keys.map(key => {
                if (key != CACHE) {
                    console.log("delete " + key);
                    return caches.delete(key);
                }
            })
        ))
    );
});

self.addEventListener("fetch", event => {
    event.respondWith(
        caches.match(event.request)
        .then(function (response) {
            return response || fetch(event.request);
        })
        .catch(function () {
            return caches.match('/offline/');
        }),
    );
});
