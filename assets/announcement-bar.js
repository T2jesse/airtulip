/**
 * Announcement bar carousel (<announcement-bar>).
 * Depends on globals from vendor.js + theme.js: Flickity, Motion, theme, Shopify.
 */
class AnnouncementBar extends HTMLElement {
  constructor() {
    super();

    if (!theme.config.isTouch || Shopify.designMode) {
      Motion.inView(this, this.init.bind(this), { margin: '200px 0px 200px 0px' });
    } else {
      new theme.initWhenVisible(this.init.bind(this));
    }
  }

  static get observedAttributes() {
    return ['selected-index'];
  }

  get selectedIndex() {
    return parseInt(this.getAttribute('selected-index')) || 0;
  }

  set selectedIndex(index) {
    this.setAttribute('selected-index', Math.min(Math.max(index, 0), this.items.length - 1).toString());
  }

  get items() {
    return (this._items = this._items || Array.from(this.children));
  }

  get autoplay() {
    return this.hasAttribute('autoplay');
  }

  get speed() {
    return this.hasAttribute('autoplay') ? parseInt(this.getAttribute('autoplay-speed')) * 1000 : 5000;
  }

  /**
   * Liquid only sets aria-hidden on blocks after the first; Flickity with accessibility: false
   * never adds it to slide 1 — so theme CSS never hides the previous slide's copy. Keep attrs in sync.
   */
  syncSlidesA11y() {
    if (!this.slider) return;
    const slides = this.querySelectorAll('.flickity-slider .announcement__slide');
    slides.forEach((slide, i) => {
      if (i === this.slider.selectedIndex) {
        slide.removeAttribute('aria-hidden');
      } else {
        slide.setAttribute('aria-hidden', 'true');
      }
    });
  }

  init() {
    if (this.initialized) return;
    this.initialized = true;

    if (this.items.length > 1) {
      this.slider = new Flickity(this, {
        accessibility: false,
        fade: true,
        pageDots: false,
        prevNextButtons: false,
        wrapAround: true,
        rightToLeft: theme.config.rtl,
        autoPlay: this.autoplay ? this.speed : false,
        on: {
          ready: () => {
            setTimeout(() => {
              this.setAttribute('loaded', '');
              this.syncSlidesA11y();
            });
          },
        },
      });

      this.slider.on('change', this.onChange.bind(this));
      this.addEventListener('slider:previous', () => this.slider.previous());
      this.addEventListener('slider:next', () => this.slider.next());
      this.addEventListener('slider:play', () => this.slider.playPlayer());
      this.addEventListener('slider:pause', () => this.slider.pausePlayer());

      if (Shopify.designMode) {
        this.addEventListener('shopify:block:select', (event) => this.slider.select(this.items.indexOf(event.target)));
      }
    }
  }

  disconnectedCallback() {
    if (this.slider) this.slider.destroy();
  }

  attributeChangedCallback(name, oldValue, newValue) {
    if (name === 'selected-index' && oldValue !== null && oldValue !== newValue) {
      const focusableEvents = 'button, [href]';

      const fromElement = this.items[parseInt(oldValue)];
      const toElement = this.items[parseInt(newValue)];

      fromElement.querySelectorAll(focusableEvents).forEach((el) => {
        el.setAttribute('tabindex', '-1');
      });
      toElement.querySelectorAll(focusableEvents).forEach((el) => {
        el.removeAttribute('tabindex');
      });
    }
  }

  onChange() {
    this.selectedIndex = this.slider.selectedIndex;
    this.syncSlidesA11y();
    this.dispatchEvent(
      new CustomEvent('slider:change', {
        bubbles: true,
        detail: { currentPage: this.slider.selectedIndex },
      })
    );
  }
}

customElements.define('announcement-bar', AnnouncementBar);
