const CACHE = 'metropolis-v1';

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE).then(cache => {
            return cache.addAll([
                '/offline/'
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
