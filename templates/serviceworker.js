importScripts('https://storage.googleapis.com/workbox-cdn/releases/6.2.0/workbox-sw.js');

workbox.core.setCacheNameDetails({
    prefix: 'metropolis',
    suffix: 'v2'
});

workbox.routing.setDefaultHandler(
    new workbox.strategies.NetworkOnly()
);

workbox.precaching.precacheAndRoute([
    {url: '/static/js/jquery-3.6.0.min.js', revision: '3.6.0'},
    {url: '/static/css/materialize.min.css', revision: '1.0.0' },
    {url: '/static/js/materialize.min.js', revision: '1.0.0' },
    {url: '/static/css/fullcalendar.min.css', revision: '5.9.0'},
    {url: '/static/js/fullcalendar.min.js', revision: '5.9.0'},
    {url: '/static/css/select2.min.css', revision: '4.1.0-rc.0'},
    {url: '/static/js/select2.min.js', revision: '4.1.0-rc.0'},
    {url: '/static/css/mapbox-gl.css', revision: '2.4.1'},
    {url: '/static/js/mapbox-gl.js', revision: '2.4.1'},
    {url: '/static/css/mapbox-gl-geocoder.css', revision: '4.7.2'},
    {url: '/static/js/mapbox-gl-geocoder.min.js', revision: '4.7.2'},
    {url: '/static/js/quicklink.umd.js', revision: '2.2.0'},
    {url: '/static/js/luxon.min.js', revision: '2.0.2'},
    {url: '/static/js/popper.min.js', revision: '2.9.2'},
    {url: '/static/core/css/index-banner.css', revision: '4'},
    {url: '/static/core/js/schedule.js', revision: '3'},
    {url: '/static/css/material-design-iconic-font.min.css', revision: '2.2.0'},
    {url: '/static/fonts/Material-Design-Iconic-Font.woff2', revision: '2.2.0'},
    {url: '/static/core/img/logo-light-transparent.png', revision: '1'},
    {url: '/static/core/img/logo-dark-transparent.png', revision: '2'},
    {url: '/static/core/img/top-banner.png', revision: '1'},
], {
    directoryIndex: null,
    cleanUrls: false,
});

workbox.routing.registerRoute(
    new RegExp('\/api.+'),
    new workbox.strategies.NetworkFirst()
);

workbox.recipes.offlineFallback({
    pageFallback: '/offline/',
});

workbox.recipes.googleFontsCache();

workbox.core.clientsClaim();
