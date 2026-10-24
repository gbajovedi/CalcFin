/**
 * HP 17bII+ Silver — Service Worker (Offline-First & Auto-Update)
 */

const CACHE_NAME = 'hp17bii-pwa-v1.0';

const PRECACHE_ASSETS = [
  './',
  './index.html',
  './Calculadora%20Financeira%2017bIi.html',
  './manifest.webmanifest',
  './icons/icon.svg',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/apple-touch-icon.png'
];

// Instalação: Cacheia os arquivos locais e força ativação imediata
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(PRECACHE_ASSETS).catch((err) => {
        console.warn('[PWA-SW] Pré-cacheamento parcial de recursos:', err);
      });
    }).then(() => self.skipWaiting())
  );
});

// Ativação: Limpa caches antigos e assume controle imediato das páginas
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      );
    }).then(() => self.clients.claim())
  );
});

// Interceptação de requisições:
// - Páginas HTML / Navegação: Network-First com fallback para o cache (garante novidades em commits).
// - Recursos estáticos / Fontes: Cache-First com atualização em background (Stale-While-Revalidate).
self.addEventListener('fetch', (event) => {
  const req = event.request;

  // Ignorar requisições não-GET
  if (req.method !== 'GET') return;

  const url = new URL(req.url);

  // Navegações / HTML: Network-First para receber os novos commits do GitHub Pages
  if (req.mode === 'navigate' || req.headers.get('accept')?.includes('text/html')) {
    event.respondWith(
      fetch(req)
        .then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            const clone = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(req, clone));
          }
          return networkResponse;
        })
        .catch(() => {
          return caches.match(req).then((cachedResponse) => {
            return cachedResponse || caches.match('./index.html') || caches.match('./');
          });
        })
    );
    return;
  }

  // Recursos estáticos (mesma origem ou Google Fonts)
  event.respondWith(
    caches.match(req).then((cachedResponse) => {
      const fetchPromise = fetch(req)
        .then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            const clone = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(req, clone));
          }
          return networkResponse;
        })
        .catch(() => {
          // Se offline e não estiver em cache, falha silenciosamente
        });

      return cachedResponse || fetchPromise;
    })
  );
});

