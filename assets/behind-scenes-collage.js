/**
 * Behind-the-scenes collage — horizontal flex panels expand on hover (fine pointer) or click/tap.
 */
class BehindScenesCollage extends HTMLElement {
  constructor() {
    super();
    this.onDocumentPointer = this.onDocumentPointer.bind(this);
    this.onPanelClick = this.onPanelClick.bind(this);
    this.onTrackPointerLeave = this.onTrackPointerLeave.bind(this);
    this.onPanelPointerEnter = this.onPanelPointerEnter.bind(this);
    this.onBlockSelect = this.onBlockSelect.bind(this);
  }

  connectedCallback() {
    this.track = this.querySelector('[data-bts-track]');
    if (!this.track) return;

    this.panels = Array.from(this.track.querySelectorAll('[data-bts-panel]'));
    if (this.panels.length === 0) return;

    this.hoverCapable = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

    this.panels.forEach((panel) => {
      panel.addEventListener('click', this.onPanelClick);
      if (this.hoverCapable) {
        panel.addEventListener('pointerenter', this.onPanelPointerEnter);
      }
    });

    if (this.hoverCapable) {
      this.track.addEventListener('pointerleave', this.onTrackPointerLeave);
    }

    document.addEventListener('click', this.onDocumentPointer);

    if (typeof Shopify !== 'undefined' && Shopify.designMode) {
      document.addEventListener('shopify:block:select', this.onBlockSelect);
    }
  }

  disconnectedCallback() {
    document.removeEventListener('click', this.onDocumentPointer);
    document.removeEventListener('shopify:block:select', this.onBlockSelect);

    if (!this.panels) return;

    this.panels.forEach((panel) => {
      panel.removeEventListener('click', this.onPanelClick);
      panel.removeEventListener('pointerenter', this.onPanelPointerEnter);
    });

    if (this.track) {
      this.track.removeEventListener('pointerleave', this.onTrackPointerLeave);
    }
  }

  setExpanded(panel) {
    if (!panel) return;
    this.panels.forEach((item) => {
      const active = item === panel;
      item.classList.toggle('is-expanded', active);
      item.setAttribute('aria-expanded', active ? 'true' : 'false');
    });
    this.track.classList.add('has-active');
    this.classList.add('is-active');
  }

  clearExpanded() {
    this.panels.forEach((panel) => {
      panel.classList.remove('is-expanded');
      panel.setAttribute('aria-expanded', 'false');
    });
    this.track.classList.remove('has-active');
    this.classList.remove('is-active');
  }

  onPanelPointerEnter(event) {
    this.setExpanded(event.currentTarget);
  }

  onTrackPointerLeave() {
    this.clearExpanded();
  }

  onPanelClick(event) {
    const panel = event.currentTarget;
    if (panel.classList.contains('is-expanded') && this.track.classList.contains('has-active')) {
      this.clearExpanded();
      return;
    }
    this.setExpanded(panel);
    event.stopPropagation();
  }

  onDocumentPointer(event) {
    if (!this.track.classList.contains('has-active')) return;
    if (this.contains(event.target)) return;
    this.clearExpanded();
  }

  onBlockSelect(event) {
    const panel = event.target.closest('[data-bts-panel]');
    if (!panel || !this.contains(panel)) return;
    this.setExpanded(panel);
  }
}

customElements.define('behind-scenes-collage', BehindScenesCollage);
