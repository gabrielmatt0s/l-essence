(function () {
  'use strict';

  var toggle = document.getElementById('navbar-toggle');
  var menu = document.getElementById('navbar-menu');

  if (!toggle || !menu) return;

  function openMenu() {
    menu.classList.add('is-open');
    toggle.setAttribute('aria-expanded', 'true');
    toggle.querySelector('.sr-only').textContent = 'Fechar menu';
    document.addEventListener('keydown', onKeydown);
    // setTimeout: .focus() síncrono aqui falha silenciosamente, pois
    // visibility:hidden->visible (via .is-open) ainda não foi recalculado
    // pelo navegador no mesmo tick em que a classe é adicionada.
    var firstLink = menu.querySelector('a');
    if (firstLink) {
      setTimeout(function () {
        firstLink.focus();
      }, 0);
    }
  }

  function closeMenu(returnFocus) {
    menu.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.querySelector('.sr-only').textContent = 'Abrir menu';
    document.removeEventListener('keydown', onKeydown);
    if (returnFocus) toggle.focus();
  }

  function onKeydown(event) {
    if (event.key === 'Escape') {
      closeMenu(true);
    }
  }

  toggle.addEventListener('click', function () {
    var isOpen = toggle.getAttribute('aria-expanded') === 'true';
    if (isOpen) {
      closeMenu(false);
    } else {
      openMenu();
    }
  });

  menu.querySelectorAll('a').forEach(function (link) {
    link.addEventListener('click', function () {
      closeMenu(false);
    });
  });

  var mediaQuery = window.matchMedia('(min-width: 1024px)');
  mediaQuery.addEventListener('change', function (event) {
    if (event.matches) closeMenu(false);
  });
})();

(function () {
  'use strict';

  var pillars = document.querySelector('.services__pillars');
  var dots = document.querySelectorAll('.services__pillars-dot');
  var prevArrow = document.querySelector('.services__pillars-arrow--prev');
  var nextArrow = document.querySelector('.services__pillars-arrow--next');
  var slides = document.querySelectorAll('.services__pillar-content');

  if (!pillars || !dots.length) return;

  var ticking = false;
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var carouselQuery = window.matchMedia('(min-width: 768px)');

  function goToIndex(index) {
    pillars.scrollTo({
      left: index * pillars.clientWidth,
      behavior: reduceMotion ? 'auto' : 'smooth'
    });
  }

  // Cada slide (Sorriso/Facial) tem sua própria altura natural (foto +
  // legenda); em vez de esticar os dois para a altura do mais alto (o que
  // deixa um vazio embaixo do mais curto), a altura da faixa acompanha só
  // o slide ativo. .services__media e .services__pillar-copy não têm
  // flex-grow, então a altura deles reflete sempre o conteúdo real, mesmo
  // quando o post pai está esticado pelo layout padrão do flex.
  function measureSlideHeight(slide) {
    var media = slide.querySelector('.services__media');
    var copy = slide.querySelector('.services__pillar-copy');
    return (media ? media.offsetHeight : 0) + (copy ? copy.offsetHeight : 0);
  }

  function syncPillarsHeight(index) {
    // Abaixo de 768px os dois pilares ficam empilhados (sem carrossel,
    // ver CSS) -- a altura precisa ficar livre para caber os dois.
    if (!carouselQuery.matches) {
      pillars.style.height = '';
      return;
    }
    var slide = slides[index];
    if (!slide) return;
    pillars.style.height = measureSlideHeight(slide) + 'px';
  }

  function updateActiveState() {
    ticking = false;
    var index = Math.round(pillars.scrollLeft / pillars.clientWidth);
    dots.forEach(function (dot, i) {
      dot.classList.toggle('is-active', i === index);
      dot.setAttribute('aria-current', i === index ? 'true' : 'false');
    });
    if (prevArrow) prevArrow.hidden = index === 0;
    if (nextArrow) nextArrow.hidden = index === dots.length - 1;
    syncPillarsHeight(index);
  }

  pillars.addEventListener('scroll', function () {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(updateActiveState);
  });

  dots.forEach(function (dot, i) {
    dot.addEventListener('click', function () {
      goToIndex(i);
    });
  });

  if (prevArrow) {
    prevArrow.addEventListener('click', function () {
      var index = Math.round(pillars.scrollLeft / pillars.clientWidth);
      goToIndex(Math.max(0, index - 1));
    });
  }

  if (nextArrow) {
    nextArrow.addEventListener('click', function () {
      var index = Math.round(pillars.scrollLeft / pillars.clientWidth);
      goToIndex(Math.min(dots.length - 1, index + 1));
    });
  }

  window.addEventListener('resize', function () {
    var index = Math.round(pillars.scrollLeft / pillars.clientWidth);
    syncPillarsHeight(index);
  });

  syncPillarsHeight(0);
})();

(function () {
  'use strict';

  var mosaic = document.querySelector('.about__mosaic');
  var mosaicDots = document.querySelectorAll('.about__mosaic-dot');

  if (!mosaic || !mosaicDots.length) return;

  var ticking = false;
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function updateActiveDot() {
    ticking = false;
    var index = Math.round(mosaic.scrollLeft / mosaic.clientWidth);
    mosaicDots.forEach(function (dot, i) {
      dot.classList.toggle('is-active', i === index);
      dot.setAttribute('aria-current', i === index ? 'true' : 'false');
    });
  }

  mosaic.addEventListener('scroll', function () {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(updateActiveDot);
  });

  mosaicDots.forEach(function (dot, i) {
    dot.addEventListener('click', function () {
      mosaic.scrollTo({
        left: i * mosaic.clientWidth,
        behavior: reduceMotion ? 'auto' : 'smooth'
      });
    });
  });
})();

(function () {
  'use strict';

  // Mapa carrega bem antes de entrar na viewport, para já estar
  // pronto quando o reveal do GSAP disparar em '.location__inner'
  // (start: 'top 80%'). Sem isso o iframe só começa a buscar os
  // tiles no momento do reveal e aparece em branco por um instante.
  var mapFrame = document.querySelector('.location__map-embed');
  if (!mapFrame) return;

  function loadMap() {
    if (mapFrame.src) return;
    mapFrame.src = mapFrame.getAttribute('data-src');
  }

  if ('IntersectionObserver' in window) {
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            loadMap();
            observer.disconnect();
          }
        });
      },
      { rootMargin: '1200px 0px' }
    );
    observer.observe(mapFrame);
  } else {
    loadMap();
  }
})();
