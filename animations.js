(function () {
  'use strict';

  if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') return;

  gsap.registerPlugin(ScrollTrigger);

  // Recalcula as posições de trigger depois que fontes (Newsreader/General
  // Sans) e imagens tardias terminam de carregar. Sem isso, uma seção como
  // o footer -- calculada antes do reflow final da página -- pode herdar um
  // "start" desatualizado e, por usar once: true, nunca mais reavaliar seu
  // estado (fica preso no opacity:0 do gsap.from).
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(function () {
      ScrollTrigger.refresh();
    });
  }
  window.addEventListener('load', function () {
    ScrollTrigger.refresh();
  });

  var mm = gsap.matchMedia();

  mm.add(
    {
      reduceMotion: '(prefers-reduced-motion: reduce)',
      // isDesktop existe só para garantir que ALGUMA query sempre bata: o
      // handler do gsap.matchMedia() só executa quando pelo menos uma
      // condição do objeto é verdadeira -- com apenas isMobile (max-width),
      // uma tela desktop sem prefers-reduced-motion não batia em nada e o
      // callback nunca rodava (bug real encontrado em QA, ver relatório).
      isMobile: '(max-width: 767px)',
      isDesktop: '(min-width: 768px)'
    },
    function (context) {
      var reduceMotion = context.conditions.reduceMotion;
      var isMobile = context.conditions.isMobile;

      // Nada é escondido via CSS neste site -- todo estado "de" das animações é
      // definido pelo próprio GSAP (gsap.from). Se prefers-reduced-motion estiver
      // ativo, simplesmente não criamos nenhuma tween: o conteúdo permanece no
      // estado final (visível, sem transform) desde o primeiro paint.
      if (reduceMotion) {
        return;
      }

      var yShort = isMobile ? 14 : 20;
      var yBase = isMobile ? 18 : 26;
      var durShort = isMobile ? 0.5 : 0.6;
      var durBase = isMobile ? 0.6 : 0.8;
      var ease = 'power2.out';

      // Reveal de moldura (cortina de cima pra baixo) usado nos blocos de
      // fotografia/mídia -- distingue a entrada de imagem da entrada de
      // texto (fade+y) sem depender de nenhuma técnica proibida sobre os
      // assets oficiais (aqui só se aplica a fotografia editorial comum).
      var clipHidden = 'inset(0% 0% 100% 0%)';
      var clipVisible = 'inset(0% 0% 0% 0%)';
      var durReveal = isMobile ? 0.7 : 0.9;

      /* =====================================================
         Hero — entrada imediata (acima da dobra, não é scroll-driven)
         Símbolo/descritor à direita já têm animação própria em CSS
         (styles.css) e não são tocados por este timeline (só ganham
         um parallax leve no wrapper logo abaixo).
         ===================================================== */
      var heroTl = gsap.timeline({ defaults: { ease: ease } });
      heroTl
        .from('.hero .eyebrow', { opacity: 0, y: 12, duration: durShort })
        .from(
          '.hero__headline',
          { opacity: 0, y: yBase, duration: durBase },
          '-=0.35'
        )
        .from(
          '.hero__subtext',
          { opacity: 0, y: yShort, duration: durShort },
          '-=0.4'
        )
        .from(
          '.hero__cta',
          { opacity: 0, y: yShort, duration: durShort },
          '-=0.3'
        );

      // Parallax sutil: o grupo símbolo+descritor sobe um pouco mais devagar
      // que o restante da hero enquanto a seção sai de tela, dando profundidade
      // no scroll. Aplicado no wrapper (.hero__visual), nunca no <img> do
      // símbolo oficial, que já tem sua própria animação CSS de entrada e cuja
      // geometria/transform não deve ser disputada por duas fontes diferentes.
      gsap.to('.hero__visual', {
        yPercent: -10,
        ease: 'none',
        scrollTrigger: {
          trigger: '.hero',
          start: 'top top',
          end: 'bottom top',
          scrub: true
        }
      });

      /* =====================================================
         Sobre — texto (eyebrow/headline/parágrafos/credenciais) com
         stagger leve, depois mosaico com stagger próprio.
         ===================================================== */
      var aboutTextTl = gsap.timeline({
        defaults: { opacity: 0, y: yBase, duration: durBase, ease: ease },
        scrollTrigger: { trigger: '.about__intro', start: 'top 80%', once: true }
      });
      aboutTextTl
        .from('.about__eyebrow', {})
        .from('.about__headline', {}, '-=0.45')
        .from('.about__text p', { stagger: 0.08 }, '-=0.4');

      gsap.from('.about__credentials li', {
        opacity: 0,
        y: yShort,
        duration: durShort,
        stagger: 0.06,
        ease: ease,
        scrollTrigger: { trigger: '.about__credentials', start: 'top 85%', once: true }
      });

      gsap.fromTo(
        '.about__mosaic-item',
        { clipPath: clipHidden },
        {
          clipPath: clipVisible,
          duration: durReveal,
          stagger: 0.12,
          ease: ease,
          scrollTrigger: { trigger: '.about__mosaic', start: 'top 80%', once: true }
        }
      );

      /* =====================================================
         Tratamentos — coluna de introdução, depois o card do
         tratamento (foto + título + texto + procedimentos).
         ===================================================== */
      var servicesTl = gsap.timeline({
        defaults: { opacity: 0, y: yBase, duration: durBase, ease: ease },
        scrollTrigger: { trigger: '.services__split', start: 'top 80%', once: true }
      });
      servicesTl
        .from('.services__intro > *', {})
        .fromTo(
          '.services__media',
          { clipPath: clipHidden },
          {
            clipPath: clipVisible,
            opacity: 1,
            y: 0,
            duration: durReveal,
            ease: ease
          },
          '-=0.5'
        )
        .from('.services__pillar-copy', { y: isMobile ? 16 : 24 }, '-=0.55')
        .from(
          '.services__procedures li',
          { y: 10, duration: durShort, stagger: 0.06 },
          '-=0.35'
        );

      /* =====================================================
         Experiência — headline/texto, imagem (reveal) e conceitos
         (stagger discreto).
         ===================================================== */
      var experienceTl = gsap.timeline({
        defaults: { opacity: 0, ease: ease },
        scrollTrigger: { trigger: '.experience__inner', start: 'top 80%', once: true }
      });
      experienceTl
        .from('.experience__headline', { y: yBase, duration: durBase })
        .from('.experience__text', { y: yShort, duration: durShort }, '-=0.45')
        .fromTo(
          '.experience__media',
          { clipPath: clipHidden, opacity: 0 },
          { clipPath: clipVisible, opacity: 1, duration: durReveal, ease: ease },
          '-=0.5'
        )
        .from(
          '.experience__concept',
          { y: yShort, duration: durShort, stagger: 0.1 },
          '-=0.4'
        );

      /* =====================================================
         Prova Social — depoimento principal entra primeiro, os dois
         secundários entram depois com stagger pequeno.
         ===================================================== */
      var testimonialsTl = gsap.timeline({
        defaults: { opacity: 0, y: yBase, duration: durBase, ease: ease },
        scrollTrigger: { trigger: '.testimonials__grid', start: 'top 80%', once: true }
      });
      testimonialsTl
        .from('.testimonial--featured', { scale: 0.97 })
        .from(
          ['.testimonial--second', '.testimonial--third'],
          { y: yShort, duration: durShort, stagger: 0.12 },
          '-=0.45'
        );

      /* =====================================================
         Localização — texto simples, depois mapa com o mesmo reveal
         de cortina usado nos outros blocos de mídia da página.
         ===================================================== */
      var locationTl = gsap.timeline({
        defaults: { opacity: 0, ease: ease },
        scrollTrigger: { trigger: '.location__inner', start: 'top 80%', once: true }
      });
      locationTl
        .from('.location__content > *', {
          y: yShort,
          duration: durShort,
          stagger: 0.06
        })
        .fromTo(
          '.location__map',
          { clipPath: clipHidden },
          { clipPath: clipVisible, opacity: 1, duration: durReveal, ease: ease },
          '-=0.35'
        );

      /* =====================================================
         Footer — colunas (marca/nav/contato) com stagger leve,
         depois a linha inferior de créditos.
         ===================================================== */
      var footerTl = gsap.timeline({
        defaults: { opacity: 0, y: yShort, duration: durShort, ease: ease },
        scrollTrigger: { trigger: '.site-footer', start: 'top 90%', once: true }
      });
      footerTl
        .from('.site-footer__top > *', { stagger: 0.08 })
        .from('.site-footer__bottom', {}, '-=0.2');
    }
  );

  /* ===========================================================
     CTAs primários (WhatsApp) — leve atração magnética ao mouse.
     Só em dispositivos com mouse de precisão (hover + pointer:fine);
     em touch/reduced-motion os botões ficam só com o hover CSS já
     existente (translateY + cor), sem nenhuma tween nova.
     =========================================================== */
  mm.add(
    {
      canHover: '(hover: hover) and (pointer: fine)',
      reduceMotion: '(prefers-reduced-motion: reduce)'
    },
    function (context) {
      if (context.conditions.reduceMotion || !context.conditions.canHover) return;

      var cleanups = [];
      var LIFT = -2; // px -- mesmo valor do antigo .button--primary:hover translateY(-2px)

      gsap.utils.toArray('.button--primary').forEach(function (btn) {
        // O hover/active em CSS (transform: translateY) fica com prioridade
        // de cascata mais baixa que o inline style que o GSAP escreve, então
        // nestes botões (dispositivos com mouse) o JS assume o "lift" por
        // completo -- reproduzido abaixo -- para não brigar com o CSS.
        // Em touch/reduced-motion (fora deste matchMedia) o CSS original
        // continua sendo a única fonte, intacto.
        var xTo = gsap.quickTo(btn, 'x', { duration: 0.4, ease: 'power3' });
        var yTo = gsap.quickTo(btn, 'y', { duration: 0.4, ease: 'power3' });
        var scaleTo = gsap.quickTo(btn, 'scale', { duration: 0.15, ease: 'power2.out' });

        function onMove(event) {
          var rect = btn.getBoundingClientRect();
          var relX = event.clientX - rect.left - rect.width / 2;
          var relY = event.clientY - rect.top - rect.height / 2;
          xTo(relX * 0.25);
          yTo(LIFT + relY * 0.25);
        }

        function onLeave() {
          xTo(0);
          yTo(0);
          scaleTo(1);
        }

        function onDown() {
          scaleTo(0.97);
        }

        function onUp() {
          scaleTo(1);
        }

        btn.addEventListener('mousemove', onMove);
        btn.addEventListener('mouseleave', onLeave);
        btn.addEventListener('mousedown', onDown);
        btn.addEventListener('mouseup', onUp);

        cleanups.push(function () {
          btn.removeEventListener('mousemove', onMove);
          btn.removeEventListener('mouseleave', onLeave);
          btn.removeEventListener('mousedown', onDown);
          btn.removeEventListener('mouseup', onUp);
        });
      });

      return function () {
        cleanups.forEach(function (fn) { fn(); });
      };
    }
  );
})();
