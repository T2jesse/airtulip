/**
 * Top testimonials — Flickity (vendor.js).
 * Continuous drift: update slider `x`, then `positionSlider()` (same pattern as Metafizzy’s internal animate → positionSlider).
 * @see https://flickity.metafizzy.co/options.html — freeScroll + wrapAround; no built‑in marquee speed, so we drive `x` manually.
 */
(function () {
  if (customElements.get('top-testimonials-carousel')) return;

  const MIN_WIDTH = 768;

  class TopTestimonialsCarousel extends HTMLElement {
    connectedCallback() {
      if (this._connected) return;
      this._connected = true;
      this.applyCardShadowOffsets();

      this._onResize =
        this._onResize ||
        theme.utils.debounce(() => {
          if (this.slides.length < 2) return;
          const on = this.autoplayOn();
          if (!this.carousel) {
            this.mount();
            return;
          }
          if (this._lastAutoplayOn !== undefined && on !== this._lastAutoplayOn) {
            this.teardown();
            this.mount();
            return;
          }
          this.carousel.resize();
        }, 200);

      const boot = () => {
        if (this._booted) return;
        this._booted = true;
        this.mount();
        if (this.slides.length < 2) return;
        window.addEventListener('resize', this._onResize);
        if (window.matchMedia) {
          this._mq = window.matchMedia(`(min-width: ${MIN_WIDTH}px)`);
          this._mq.addEventListener('change', this._onResize);
        }
      };
      requestAnimationFrame(boot);
      this._bootTimer = setTimeout(boot, 50);
    }

    get slides() {
      return Array.from(this.querySelectorAll('.top-testimonials__slide'));
    }

    get track() {
      return this.querySelector('.top-testimonials-carousel__track');
    }

    applyCardShadowOffsets() {
      const root = this.closest('.shopify-section');
      if (!root || this.dataset.shadowEnabled !== 'true') return;
      const angle = (parseFloat(this.dataset.shadowAngle) || 0) * (Math.PI / 180);
      let x = Math.cos(angle) * (parseFloat(this.dataset.shadowDistance) || 0);
      let y = Math.sin(angle) * (parseFloat(this.dataset.shadowDistance) || 0);
      if (theme.config.rtl) x *= -1;
      root.style.setProperty('--tt-card-sx', `${Math.round(x * 100) / 100}px`);
      root.style.setProperty('--tt-card-sy', `${Math.round(y * 100) / 100}px`);
    }

    /** Theme editor: show motion even when OS “reduce motion” is on. Storefront still respects a11y. */
    motionOkForAutoplay() {
      try {
        if (typeof Shopify !== 'undefined' && Shopify.designMode) return true;
      } catch (e) {}
      try {
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return false;
      } catch (e) {}
      return !(window.theme && theme.config && theme.config.motionReduced);
    }

    autoplayOn() {
      if (this.dataset.autoplayDesktop !== 'true') return false;
      try {
        if (!window.matchMedia(`(min-width: ${MIN_WIDTH}px)`).matches) return false;
      } catch (e) {
        return false;
      }
      const ms = parseInt(this.dataset.autoplayDelay || '15000', 10);
      if (!Number.isFinite(ms) || ms < 250) return false;
      return this.motionOkForAutoplay();
    }

    stepPx() {
      const first = this.slides[0];
      if (!first) return 0;
      let w = first.getBoundingClientRect().width;
      if (w < 2 && this.carousel && this.carousel.slides && this.carousel.slides[0]) {
        const s = this.carousel.slides[0].size;
        if (s && s.outerWidth) w = s.outerWidth;
      }
      return w > 1 ? w : first.offsetWidth;
    }

    mount() {
      this.teardown();
      if (this.slides.length < 2) return;

      const el = this.track;
      if (!el || typeof Flickity === 'undefined') return;

      const drift = this.autoplayOn();

      this.carousel = new Flickity(el, {
        cellSelector: '.top-testimonials__slide',
        groupCells: false,
        contain: !drift,
        cellAlign: 'left',
        pageDots: this.dataset.pageDots === 'true',
        prevNextButtons: false,
        wrapAround: drift || this.dataset.wrapAround === 'true',
        adaptiveHeight: false,
        rightToLeft: theme.config.rtl,
        freeScroll: drift,
        autoPlay: false,
      });

      this._lastAutoplayOn = drift;

      const finishResize = () => {
        this.carousel.resize();
        if (drift) {
          this.carousel.x = 0;
          if (typeof this.carousel.positionSlider === 'function') {
            this.carousel.positionSlider();
          } else if (typeof this.carousel.settle === 'function') {
            this.carousel.settle(0);
          }
          this.startDrift();
        }
      };
      requestAnimationFrame(() => {
        this.carousel.resize();
        requestAnimationFrame(finishResize);
      });

      this._nav = (e) => {
        if (!this.carousel) return;
        const p = e.target.closest?.('[data-top-testimonials-prev]');
        const n = e.target.closest?.('[data-top-testimonials-next]');
        if (!p && !n) return;
        e.preventDefault();
        e.stopPropagation();
        if (drift) this.pauseDrift();
        this.carousel.uiChange?.();
        p ? this.carousel.previous() : this.carousel.next();
      };
      this.addEventListener('click', this._nav, true);

      if (typeof Shopify !== 'undefined' && Shopify.designMode) {
        this._blockSel = (e) => {
          const slide = e.target.closest?.('.top-testimonials__slide');
          if (!slide || !this.carousel) return;
          const cell = this.carousel.getCell(slide);
          if (!cell) return;
          const i = this.carousel.getCellSlideIndex(cell);
          if (i >= 0) this.carousel.select(i);
        };
        this.addEventListener('shopify:block:select', this._blockSel);
      }
    }

    pauseDrift() {
      this._driftPaused = true;
      clearTimeout(this._driftResumeTimer);
      const ms = parseInt(this.dataset.autoplayDelay || '15000', 10);
      const wait = Math.min(12000, Math.max(2000, Number.isFinite(ms) ? ms : 15000));
      this._driftResumeTimer = setTimeout(() => {
        this._driftPaused = false;
        this._driftTs = 0;
      }, wait);
    }

    startDrift() {
      this.stopDriftLoop();
      this._driftPaused = false;
      this._driftTs = 0;

      const onVis = () => {
        this._driftPaused = document.hidden;
        if (!document.hidden) this._driftTs = 0;
      };
      document.addEventListener('visibilitychange', onVis);
      this._vis = onVis;

      const onEnter = () => {
        this._driftPaused = true;
      };
      const onLeave = () => {
        this._driftPaused = false;
        this._driftTs = 0;
      };
      this.addEventListener('mouseenter', onEnter);
      this.addEventListener('mouseleave', onLeave);
      this._me = onEnter;
      this._ml = onLeave;

      const onDragEnd = () => {
        clearTimeout(this._driftResumeTimer);
        this._driftPaused = true;
        this._driftResumeTimer = setTimeout(() => {
          this._driftPaused = false;
          this._driftTs = 0;
        }, 800);
      };
      this.carousel.on('dragEnd', onDragEnd);
      this._dragEnd = onDragEnd;

      const tick = (ts) => {
        this._raf = null;
        if (!this.carousel || !this.autoplayOn()) return;

        if (this._driftPaused) {
          this._raf = requestAnimationFrame(tick);
          return;
        }

        if (!this._driftTs) this._driftTs = ts;
        const dt = ts - this._driftTs;
        this._driftTs = ts;

        const step = this.stepPx();
        const delayMs = parseInt(this.dataset.autoplayDelay || '15000', 10);
        const sec = Math.max(0.25, delayMs / 1000);
        if (step < 2) {
          this._raf = requestAnimationFrame(tick);
          return;
        }

        const delta = ((step / sec) * dt) / 1000;
        this.carousel.x -= delta;
        if (typeof this.carousel.positionSlider === 'function') {
          this.carousel.positionSlider();
        } else if (typeof this.carousel.settle === 'function') {
          this.carousel.settle(this.carousel.x);
        }

        this._raf = requestAnimationFrame(tick);
      };
      this._raf = requestAnimationFrame(tick);
    }

    stopDriftLoop() {
      if (this._raf) {
        cancelAnimationFrame(this._raf);
        this._raf = null;
      }
      clearTimeout(this._driftResumeTimer);
      this._driftResumeTimer = null;
      if (this._vis) {
        document.removeEventListener('visibilitychange', this._vis);
        this._vis = null;
      }
      if (this._me) {
        this.removeEventListener('mouseenter', this._me);
        this.removeEventListener('mouseleave', this._ml);
        this._me = this._ml = null;
      }
      if (this.carousel && this._dragEnd) {
        this.carousel.off('dragEnd', this._dragEnd);
        this._dragEnd = null;
      }
    }

    teardown() {
      this.stopDriftLoop();
      if (this._nav) {
        this.removeEventListener('click', this._nav, true);
        this._nav = null;
      }
      if (this._blockSel) {
        this.removeEventListener('shopify:block:select', this._blockSel);
        this._blockSel = null;
      }
      if (this.carousel) {
        this.carousel.destroy();
        this.carousel = null;
      }
      this._lastAutoplayOn = undefined;
    }

    disconnectedCallback() {
      clearTimeout(this._bootTimer);
      if (this._mq) {
        this._mq.removeEventListener('change', this._onResize);
        this._mq = null;
      }
      window.removeEventListener('resize', this._onResize);
      this._connected = false;
      this._booted = false;
      this.teardown();
    }
  }

  customElements.define('top-testimonials-carousel', TopTestimonialsCarousel);
})();
