// Service Worker ─ FNT アドバンス アプリ集。手本：~/FNT-Apps/hanasaki-awase/sw.js
// 🔴 これと manifest.json が無いと、Android の Chrome は「アプリ」にできず、ただのショートカットとして入れる。
//    Galaxy はそのショートカットを再起動やしばらく経つと消す（2026-10-24 宮崎さん「ホーム画面に追加しても全部消えてしまう」）
// 戦略：Network First。オフライン時のみキャッシュへ。🔴 index.html を変えたら CACHE_NAME の版を上げる
const CACHE_NAME = 'fnt-advance-apps-v1.0.0';

const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './manifest.json',
  './FNT512-transparent.png',
  './icons/icon-192.png',
  './icons/app-neck.png',
  './icons/app-vorc.png',
  './icons/app-svv.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(ASSETS_TO_CACHE))
      .then(() => self.skipWaiting())
      .catch((err) => console.error('[SW] precache failed', err))
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((names) => Promise.all(names.map((name) => (name.startsWith('fnt-advance-apps-') && name !== CACHE_NAME) ? caches.delete(name) : null)))
      .then(() => self.clients.claim())
  );
});

// Network First。対象は同一オリジン＋Google Fonts
self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = req.url;
  const sameOrigin = url.startsWith(self.registration.scope);
  const isFont = url.startsWith('https://fonts.');
  if (!sameOrigin && !isFont) return;
  event.respondWith(
    fetch(req)
      .then((res) => {
        if (res && res.status === 200 && (res.type === 'basic' || res.type === 'cors')) {
          const clone = res.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(req, clone));
        }
        return res;
      })
      .catch(() =>
        caches.match(req).then((cached) => {
          if (cached) return cached;
          if (req.mode === 'navigate') return caches.match('./index.html');
          return new Response('Offline', { status: 503, statusText: 'Offline' });
        })
      )
  );
});
