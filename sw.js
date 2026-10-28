/* Neon Stack 3D service worker — precaches the whole game for offline play.
   Bump CACHE when shipping changes; the old cache is deleted on activate. */
const CACHE = 'neon-blocks-v5';
const ASSETS = [
  './',
  './index.html',
  './manifest.webmanifest',
  './icons/apple-touch-icon-180.png',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/maskable-512.png',
  './vendor/addons/controls/ArcballControls.js',
  './vendor/addons/controls/DragControls.js',
  './vendor/addons/controls/FirstPersonControls.js',
  './vendor/addons/controls/FlyControls.js',
  './vendor/addons/controls/MapControls.js',
  './vendor/addons/controls/OrbitControls.js',
  './vendor/addons/controls/PointerLockControls.js',
  './vendor/addons/controls/TrackballControls.js',
  './vendor/addons/controls/TransformControls.js',
  './vendor/addons/geometries/BoxLineGeometry.js',
  './vendor/addons/geometries/ConvexGeometry.js',
  './vendor/addons/geometries/DecalGeometry.js',
  './vendor/addons/geometries/InstancedPointsGeometry.js',
  './vendor/addons/geometries/ParametricGeometries.js',
  './vendor/addons/geometries/ParametricGeometry.js',
  './vendor/addons/geometries/RoundedBoxGeometry.js',
  './vendor/addons/geometries/TeapotGeometry.js',
  './vendor/addons/geometries/TextGeometry.js',
  './vendor/addons/postprocessing/AfterimagePass.js',
  './vendor/addons/postprocessing/BloomPass.js',
  './vendor/addons/postprocessing/BokehPass.js',
  './vendor/addons/postprocessing/ClearPass.js',
  './vendor/addons/postprocessing/CubeTexturePass.js',
  './vendor/addons/postprocessing/DotScreenPass.js',
  './vendor/addons/postprocessing/EffectComposer.js',
  './vendor/addons/postprocessing/FilmPass.js',
  './vendor/addons/postprocessing/GTAOPass.js',
  './vendor/addons/postprocessing/GlitchPass.js',
  './vendor/addons/postprocessing/HalftonePass.js',
  './vendor/addons/postprocessing/LUTPass.js',
  './vendor/addons/postprocessing/MaskPass.js',
  './vendor/addons/postprocessing/OutlinePass.js',
  './vendor/addons/postprocessing/OutputPass.js',
  './vendor/addons/postprocessing/Pass.js',
  './vendor/addons/postprocessing/RenderPass.js',
  './vendor/addons/postprocessing/RenderPixelatedPass.js',
  './vendor/addons/postprocessing/RenderTransitionPass.js',
  './vendor/addons/postprocessing/SAOPass.js',
  './vendor/addons/postprocessing/SMAAPass.js',
  './vendor/addons/postprocessing/SSAARenderPass.js',
  './vendor/addons/postprocessing/SSAOPass.js',
  './vendor/addons/postprocessing/SSRPass.js',
  './vendor/addons/postprocessing/SavePass.js',
  './vendor/addons/postprocessing/ShaderPass.js',
  './vendor/addons/postprocessing/TAARenderPass.js',
  './vendor/addons/postprocessing/TexturePass.js',
  './vendor/addons/postprocessing/UnrealBloomPass.js',
  './vendor/addons/shaders/ACESFilmicToneMappingShader.js',
  './vendor/addons/shaders/AfterimageShader.js',
  './vendor/addons/shaders/BasicShader.js',
  './vendor/addons/shaders/BleachBypassShader.js',
  './vendor/addons/shaders/BlendShader.js',
  './vendor/addons/shaders/BokehShader.js',
  './vendor/addons/shaders/BokehShader2.js',
  './vendor/addons/shaders/BrightnessContrastShader.js',
  './vendor/addons/shaders/ColorCorrectionShader.js',
  './vendor/addons/shaders/ColorifyShader.js',
  './vendor/addons/shaders/ConvolutionShader.js',
  './vendor/addons/shaders/CopyShader.js',
  './vendor/addons/shaders/DOFMipMapShader.js',
  './vendor/addons/shaders/DepthLimitedBlurShader.js',
  './vendor/addons/shaders/DigitalGlitch.js',
  './vendor/addons/shaders/DotScreenShader.js',
  './vendor/addons/shaders/ExposureShader.js',
  './vendor/addons/shaders/FXAAShader.js',
  './vendor/addons/shaders/FilmShader.js',
  './vendor/addons/shaders/FocusShader.js',
  './vendor/addons/shaders/FreiChenShader.js',
  './vendor/addons/shaders/GTAOShader.js',
  './vendor/addons/shaders/GammaCorrectionShader.js',
  './vendor/addons/shaders/GodRaysShader.js',
  './vendor/addons/shaders/HalftoneShader.js',
  './vendor/addons/shaders/HorizontalBlurShader.js',
  './vendor/addons/shaders/HorizontalTiltShiftShader.js',
  './vendor/addons/shaders/HueSaturationShader.js',
  './vendor/addons/shaders/KaleidoShader.js',
  './vendor/addons/shaders/LuminosityHighPassShader.js',
  './vendor/addons/shaders/LuminosityShader.js',
  './vendor/addons/shaders/MMDToonShader.js',
  './vendor/addons/shaders/MirrorShader.js',
  './vendor/addons/shaders/NormalMapShader.js',
  './vendor/addons/shaders/OutputShader.js',
  './vendor/addons/shaders/PoissonDenoiseShader.js',
  './vendor/addons/shaders/RGBShiftShader.js',
  './vendor/addons/shaders/SAOShader.js',
  './vendor/addons/shaders/SMAAShader.js',
  './vendor/addons/shaders/SSAOShader.js',
  './vendor/addons/shaders/SSRShader.js',
  './vendor/addons/shaders/SepiaShader.js',
  './vendor/addons/shaders/SobelOperatorShader.js',
  './vendor/addons/shaders/SubsurfaceScatteringShader.js',
  './vendor/addons/shaders/TechnicolorShader.js',
  './vendor/addons/shaders/ToonShader.js',
  './vendor/addons/shaders/TriangleBlurShader.js',
  './vendor/addons/shaders/UnpackDepthRGBAShader.js',
  './vendor/addons/shaders/VelocityShader.js',
  './vendor/addons/shaders/VerticalBlurShader.js',
  './vendor/addons/shaders/VerticalTiltShiftShader.js',
  './vendor/addons/shaders/VignetteShader.js',
  './vendor/addons/shaders/VolumeShader.js',
  './vendor/addons/shaders/WaterRefractionShader.js',
  './vendor/three.module.js'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE)
      .then(cache => cache.addAll(ASSETS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  if (req.mode === 'navigate') {
    event.respondWith(
      caches.match('./index.html').then(hit => hit || fetch(req).then(res => {
        if (res.ok) {
          const copy = res.clone();
          caches.open(CACHE).then(c => c.put('./index.html', copy));
        }
        return res;
      }))
    );
    return;
  }

  event.respondWith(
    caches.match(req).then(hit => hit || fetch(req).then(res => {
      if (res.ok) {
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put(req, copy));
      }
      return res;
    }))
  );
});
