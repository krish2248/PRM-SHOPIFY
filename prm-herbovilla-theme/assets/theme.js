/**
 * PRM HerboVilla Theme JavaScript
 * Premium Ayurvedic Wellness Brand
 */

(function() {
  'use strict';

  // ============================================
  // UTILITY FUNCTIONS
  // ============================================
  
  const debounce = (fn, delay) => {
    let timeoutId;
    return (...args) => {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => fn.apply(this, args), delay);
    };
  };

  const formatMoney = (cents, format = '₹{{amount}}') => {
    if (typeof cents === 'string') cents = cents.replace('.', '');
    const value = (cents / 100).toFixed(2);
    return format.replace('{{amount}}', value).replace('{{amount_no_decimals}}', Math.floor(cents / 100));
  };

  const fetchJSON = async (url, options = {}) => {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        ...options.headers
      }
    });
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    return response.json();
  };

  // ============================================
  // HEADER
  // ============================================
  
  class Header {
    constructor() {
      this.header = document.querySelector('.header');
      this.menuToggle = document.querySelector('.header__menu-toggle');
      this.mobileMenu = document.querySelector('.mobile-menu');
      this.mobileMenuClose = document.querySelector('.mobile-menu__close');
      
      this.init();
    }

    init() {
      if (this.header) {
        this.handleScroll();
        window.addEventListener('scroll', debounce(() => this.handleScroll(), 10));
      }

      if (this.menuToggle && this.mobileMenu) {
        this.menuToggle.addEventListener('click', () => this.openMobileMenu());
        this.mobileMenuClose?.addEventListener('click', () => this.closeMobileMenu());
        this.mobileMenu.querySelectorAll('a').forEach(link => {
          link.addEventListener('click', () => this.closeMobileMenu());
        });
        document.addEventListener('keydown', (e) => {
          if (e.key === 'Escape' && this.mobileMenu.classList.contains('mobile-menu--open')) {
            this.closeMobileMenu();
          }
        });
      }
    }

    handleScroll() {
      if (window.scrollY > 50) {
        this.header.classList.add('header--scrolled');
      } else {
        this.header.classList.remove('header--scrolled');
      }
    }

    openMobileMenu() {
      this.mobileMenu.classList.add('mobile-menu--open');
      document.body.classList.add('no-scroll');
      document.querySelector('.overlay')?.classList.add('overlay--visible');
    }

    closeMobileMenu() {
      this.mobileMenu.classList.remove('mobile-menu--open');
      document.body.classList.remove('no-scroll');
      document.querySelector('.overlay')?.classList.remove('overlay--visible');
    }
  }

  // ============================================
  // CART DRAWER
  // ============================================
  
  class CartDrawer {
    constructor() {
      this.drawer = document.querySelector('.cart-drawer');
      this.overlay = document.querySelector('.overlay');
      this.cartCount = document.querySelector('.header__cart-count');
      this.cartTriggers = document.querySelectorAll('[data-cart-toggle]');
      this.closeBtn = document.querySelector('.cart-drawer__close');
      
      this.init();
    }

    init() {
      this.cartTriggers.forEach(trigger => {
        trigger.addEventListener('click', (e) => {
          e.preventDefault();
          this.open();
        });
      });

      this.closeBtn?.addEventListener('click', () => this.close());
      this.overlay?.addEventListener('click', () => this.close());

      document.addEventListener('cart:updated', (e) => this.render(e.detail));
      
      // Listen for add to cart forms
      document.addEventListener('submit', async (e) => {
        const form = e.target.closest('form[action="/cart/add"]');
        if (form) {
          e.preventDefault();
          await this.addItem(form);
        }
      });

      // Quick add buttons
      document.addEventListener('click', async (e) => {
        const btn = e.target.closest('[data-add-to-cart]');
        if (btn) {
          e.preventDefault();
          const variantId = btn.dataset.variantId;
          const quantity = btn.dataset.quantity || 1;
          await this.addItemById(variantId, quantity, btn);
        }
      });
    }

    open() {
      this.drawer?.classList.add('cart-drawer--open');
      this.overlay?.classList.add('overlay--visible');
      document.body.classList.add('no-scroll');
      this.fetchCart();
    }

    close() {
      this.drawer?.classList.remove('cart-drawer--open');
      this.overlay?.classList.remove('overlay--visible');
      document.body.classList.remove('no-scroll');
    }

    async fetchCart() {
      try {
        const cart = await fetchJSON('/cart.js');
        this.render(cart);
      } catch (error) {
        console.error('Error fetching cart:', error);
      }
    }

    async addItem(form) {
      const submitBtn = form.querySelector('[type="submit"]');
      submitBtn?.classList.add('btn--loading');
      
      try {
        const formData = new FormData(form);
        const response = await fetch('/cart/add.js', {
          method: 'POST',
          body: formData
        });
        
        if (!response.ok) throw new Error('Add to cart failed');
        
        await this.fetchCart();
        this.open();
      } catch (error) {
        console.error('Error adding to cart:', error);
      } finally {
        submitBtn?.classList.remove('btn--loading');
      }
    }

    async addItemById(variantId, quantity, btn) {
      btn?.classList.add('btn--loading');
      
      try {
        await fetchJSON('/cart/add.js', {
          method: 'POST',
          body: JSON.stringify({
            items: [{ id: variantId, quantity: parseInt(quantity) }]
          })
        });
        
        await this.fetchCart();
        this.open();
      } catch (error) {
        console.error('Error adding to cart:', error);
      } finally {
        btn?.classList.remove('btn--loading');
      }
    }

    async updateItem(key, quantity) {
      try {
        const cart = await fetchJSON('/cart/change.js', {
          method: 'POST',
          body: JSON.stringify({ id: key, quantity })
        });
        this.render(cart);
        this.updateCartCount(cart.item_count);
      } catch (error) {
        console.error('Error updating cart:', error);
      }
    }

    async removeItem(key) {
      await this.updateItem(key, 0);
    }

    render(cart) {
      const itemsContainer = this.drawer?.querySelector('.cart-drawer__items');
      const subtotalEl = this.drawer?.querySelector('.cart-drawer__subtotal-amount');
      const footerEl = this.drawer?.querySelector('.cart-drawer__footer');
      
      this.updateCartCount(cart.item_count);

      if (!itemsContainer) return;

      if (cart.item_count === 0) {
        itemsContainer.innerHTML = `
          <div class="cart-drawer__empty">
            <p>Your cart is empty</p>
            <a href="/collections/all" class="btn btn--primary mt-lg">Continue Shopping</a>
          </div>
        `;
        if (footerEl) footerEl.style.display = 'none';
        return;
      }

      if (footerEl) footerEl.style.display = 'block';

      itemsContainer.innerHTML = cart.items.map(item => `
        <div class="cart-drawer__item" data-key="${item.key}">
          <div class="cart-drawer__item-image">
            <img src="${item.image || (item.featured_image && item.featured_image.url) || ''}" alt="${item.title}" loading="lazy">
          </div>
          <div class="cart-drawer__item-details">
            <h4 class="cart-drawer__item-title">${item.product_title}</h4>
            ${item.variant_title && item.variant_title !== 'Default Title' ? `<p class="cart-drawer__item-variant">${item.variant_title}</p>` : ''}
            <p class="cart-drawer__item-price">${formatMoney(item.final_line_price)}</p>
            <div class="cart-drawer__item-actions">
              <div class="quantity-selector quantity-selector--sm">
                <button type="button" class="quantity-selector__btn" data-action="decrease" data-key="${item.key}">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                </button>
                <input type="number" class="quantity-selector__input" value="${item.quantity}" min="1" data-key="${item.key}">
                <button type="button" class="quantity-selector__btn" data-action="increase" data-key="${item.key}">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                </button>
              </div>
              <button type="button" class="cart-drawer__item-remove" data-action="remove" data-key="${item.key}">Remove</button>
            </div>
          </div>
        </div>
      `).join('');

      if (subtotalEl) {
        subtotalEl.textContent = formatMoney(cart.total_price);
      }

      // Add event listeners for quantity buttons
      itemsContainer.querySelectorAll('[data-action]').forEach(btn => {
        btn.addEventListener('click', (e) => {
          const key = btn.dataset.key;
          const action = btn.dataset.action;
          const input = itemsContainer.querySelector(`input[data-key="${key}"]`);
          let quantity = parseInt(input?.value || 1);

          if (action === 'increase') quantity++;
          else if (action === 'decrease') quantity = Math.max(0, quantity - 1);
          else if (action === 'remove') quantity = 0;

          this.updateItem(key, quantity);
        });
      });
    }

    updateCartCount(count) {
      if (this.cartCount) {
        this.cartCount.textContent = count;
        this.cartCount.style.display = count > 0 ? 'flex' : 'none';
      }
    }
  }

  // ============================================
  // CART PAGE (AJAX)
  // ============================================

  class CartPage {
    constructor() {
      this.container = document.querySelector('[data-cart-page]');
      if (!this.container) return;

      this.pageContainer = this.container.querySelector('[data-cart-page-container]');
      this.itemsContainer = this.container.querySelector('[data-cart-page-items]');
      this.summaryContainer = this.container.querySelector('[data-cart-page-summary]');
      this.countEl = this.container.querySelector('[data-cart-page-count]');
      this.headerCartCount = document.querySelector('.header__cart-count');
      this.freeShippingThreshold = 40000; // 400 rupees in cents/paise

      this.init();
    }

    init() {
      if (!this.itemsContainer) return;

      // Use event delegation on the items container for +/- and Remove buttons
      this.itemsContainer.addEventListener('click', (e) => {
        const qtyBtn = e.target.closest('.cart-qty-btn[data-action]');
        const removeBtn = e.target.closest('.cart-item__remove[data-line]');

        if (qtyBtn) {
          e.preventDefault();
          this.handleQuantityClick(qtyBtn);
        } else if (removeBtn) {
          e.preventDefault();
          this.handleRemoveClick(removeBtn);
        }
      });

      // Handle direct input changes (user types a quantity)
      this.itemsContainer.addEventListener('change', (e) => {
        const input = e.target.closest('.cart-qty-input[data-line]');
        if (input) {
          const line = parseInt(input.dataset.line);
          let quantity = parseInt(input.value);
          if (isNaN(quantity) || quantity < 0) quantity = 1;
          this.updateLine(line, quantity);
        }
      });
    }

    handleQuantityClick(btn) {
      const line = parseInt(btn.dataset.line);
      const action = btn.dataset.action;
      const input = this.itemsContainer.querySelector(`.cart-qty-input[data-line="${line}"]`);
      let quantity = parseInt(input?.value || 1);

      if (action === 'increase') {
        quantity++;
      } else if (action === 'decrease') {
        quantity = Math.max(0, quantity - 1);
      }

      // Immediately update the input visually
      if (input) input.value = quantity;

      this.updateLine(line, quantity);
    }

    handleRemoveClick(btn) {
      const line = parseInt(btn.dataset.line);
      // Visually fade out the item immediately
      const cartItem = btn.closest('.cart-item');
      if (cartItem) {
        cartItem.style.opacity = '0.5';
        cartItem.style.pointerEvents = 'none';
      }
      this.updateLine(line, 0);
    }

    async updateLine(line, quantity) {
      // Disable all buttons during update to prevent double-clicks
      this.setLoading(true);

      try {
        const cart = await fetchJSON('/cart/change.js', {
          method: 'POST',
          body: JSON.stringify({ line: line, quantity: quantity })
        });
        this.render(cart);
        // Also dispatch event so cart drawer stays in sync
        document.dispatchEvent(new CustomEvent('cart:updated', { detail: cart }));
      } catch (error) {
        console.error('CartPage: Error updating line', line, error);
        // On error, reload to get correct state
        window.location.reload();
      } finally {
        this.setLoading(false);
      }
    }

    setLoading(loading) {
      if (!this.itemsContainer) return;
      this.itemsContainer.querySelectorAll('.cart-qty-btn, .cart-item__remove').forEach(btn => {
        btn.disabled = loading;
      });
      this.itemsContainer.querySelectorAll('.cart-qty-input').forEach(input => {
        input.disabled = loading;
      });
    }

    render(cart) {
      // Update header cart count badge
      this.updateHeaderCount(cart.item_count);

      // If cart is empty, replace entire container with empty state
      if (cart.item_count === 0) {
        this.renderEmpty();
        return;
      }

      // Update cart count text in header
      if (this.countEl) {
        this.countEl.textContent = `${cart.item_count} ${cart.item_count === 1 ? 'item' : 'items'}`;
      }

      // Re-render cart items
      this.renderItems(cart);

      // Re-render summary (subtotal, shipping bar, total)
      this.renderSummary(cart);
    }

    renderItems(cart) {
      if (!this.itemsContainer) return;

      this.itemsContainer.innerHTML = cart.items.map((item, index) => {
        const line = index + 1; // Shopify lines are 1-based
        const imageUrl = item.image || (item.featured_image && item.featured_image.url) || '';
        const hasVariant = item.variant_title && item.variant_title !== 'Default Title';

        return `
          <div class="cart-item" data-cart-item data-line="${line}" data-key="${item.key}">
            <div class="cart-item__image">
              ${imageUrl ? `<img src="${imageUrl}" alt="${this.escapeHtml(item.title)}" width="120" height="120" loading="lazy">` : ''}
            </div>
            <div class="cart-item__details">
              <a href="${item.url}" class="cart-item__title">${this.escapeHtml(item.product_title)}</a>
              ${hasVariant ? `<p class="cart-item__variant">${this.escapeHtml(item.variant_title)}</p>` : ''}
              <span class="cart-item__price">${formatMoney(item.price)}</span>
            </div>
            <div class="cart-item__actions">
              <div class="cart-item__quantity">
                <button type="button" class="cart-qty-btn" data-action="decrease" data-line="${line}">\u2212</button>
                <input type="number" name="updates[]" value="${item.quantity}" min="0" class="cart-qty-input" data-line="${line}" aria-label="Quantity">
                <button type="button" class="cart-qty-btn" data-action="increase" data-line="${line}">+</button>
              </div>
              <span class="cart-item__total">${formatMoney(item.final_line_price)}</span>
              <button type="button" class="cart-item__remove" data-line="${line}">Remove</button>
            </div>
          </div>
        `;
      }).join('');
    }

    renderSummary(cart) {
      const subtotalEl = this.container.querySelector('[data-cart-page-subtotal]');
      const shippingEl = this.container.querySelector('[data-cart-page-shipping]');
      const totalEl = this.container.querySelector('[data-cart-page-total]');
      const shippingBar = this.container.querySelector('[data-cart-shipping-bar]');

      if (subtotalEl) subtotalEl.textContent = formatMoney(cart.total_price);
      if (totalEl) totalEl.textContent = formatMoney(cart.total_price);

      // Calculate shipping bar
      const remaining = this.freeShippingThreshold - cart.total_price;
      const progress = Math.min(100, (cart.total_price / this.freeShippingThreshold) * 100);

      if (shippingEl) {
        if (remaining <= 0) {
          shippingEl.textContent = 'FREE';
          shippingEl.classList.add('free');
        } else {
          shippingEl.textContent = 'Calculated at checkout';
          shippingEl.classList.remove('free');
        }
      }

      if (shippingBar) {
        const remainingRupees = Math.ceil(remaining / 100);
        if (remaining <= 0) {
          shippingBar.innerHTML = `
            <p>\uD83C\uDF89 You've unlocked FREE shipping!</p>
            <div class="free-shipping-progress">
              <div class="free-shipping-progress__bar" style="width: 100%"></div>
            </div>
          `;
        } else {
          shippingBar.innerHTML = `
            <p>Add <strong>\u20B9${remainingRupees}</strong> more for FREE shipping!</p>
            <div class="free-shipping-progress">
              <div class="free-shipping-progress__bar" style="width: ${progress}%"></div>
            </div>
          `;
        }
      }
    }

    renderEmpty() {
      if (!this.pageContainer) return;

      this.pageContainer.innerHTML = `
        <div class="cart-empty" data-cart-empty>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="9" cy="21" r="1"></circle>
            <circle cx="20" cy="21" r="1"></circle>
            <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
          </svg>
          <h2>Your cart is empty</h2>
          <p>Looks like you haven't added any products to your cart yet. Start shopping to discover our range of Ayurvedic wellness products.</p>
          <a href="/collections/all">Start Shopping</a>
        </div>
      `;
    }

    updateHeaderCount(count) {
      if (this.headerCartCount) {
        this.headerCartCount.textContent = count;
        this.headerCartCount.style.display = count > 0 ? 'flex' : 'none';
      }
    }

    escapeHtml(str) {
      const div = document.createElement('div');
      div.textContent = str;
      return div.innerHTML;
    }
  }

  // ============================================
  // PRODUCT GALLERY
  // ============================================
  
  class ProductGallery {
    constructor(container) {
      this.container = container;
      // Support multiple selector patterns - find the main image
      this.mainImage = document.querySelector('#main-product-image') || 
                       container.querySelector('.product-main-image img') ||
                       container.querySelector('.product-gallery__main img');
      // Find all thumbnails
      this.thumbs = container.querySelectorAll('.product-thumbnail, .product-gallery__thumb');
      
      console.log('ProductGallery initialized:', {
        container: container,
        mainImage: this.mainImage,
        thumbsCount: this.thumbs.length
      });
      
      this.init();
    }

    init() {
      if (this.thumbs.length === 0) {
        console.log('No thumbnails found');
        return;
      }
      
      this.thumbs.forEach((thumb, index) => {
        thumb.addEventListener('click', (e) => {
          e.preventDefault();
          e.stopPropagation();
          console.log('Thumbnail clicked:', index, thumb.dataset.imageUrl);
          this.selectThumb(thumb);
        });
      });
    }

    selectThumb(thumb) {
      // Remove active class from all thumbs
      this.thumbs.forEach(t => {
        t.classList.remove('product-gallery__thumb--active');
        t.classList.remove('active');
      });
      // Add active class to selected thumb
      thumb.classList.add('active');
      thumb.classList.add('product-gallery__thumb--active');
      
      // Get the image URL from data attribute or img src
      const imageUrl = thumb.dataset.imageUrl || thumb.getAttribute('data-image-url');
      const img = thumb.querySelector('img');
      
      console.log('Switching to image:', imageUrl);
      
      if (this.mainImage && imageUrl) {
        this.mainImage.src = imageUrl;
        this.mainImage.srcset = '';
        // Also update alt text
        if (img && img.alt) {
          this.mainImage.alt = img.alt;
        }
      } else if (this.mainImage && img) {
        // Try to get larger version of thumbnail
        let largeSrc = img.src;
        // Handle Shopify CDN image URLs
        largeSrc = largeSrc.replace(/_\d+x\d*\./, '_1200x.');
        largeSrc = largeSrc.replace(/_\d+x\./, '_1200x.');
        console.log('Using enlarged thumbnail:', largeSrc);
        this.mainImage.src = largeSrc;
        this.mainImage.srcset = '';
      }
    }
  }

  // ============================================
  // PRODUCT VARIANTS
  // ============================================
  
  class ProductVariants {
    constructor(container) {
      this.container = container;
      this.form = container.querySelector('form[action="/cart/add"]');
      this.variantInput = this.form?.querySelector('[name="id"]');
      this.priceEl = container.querySelector('.product-info__price-current');
      this.comparePriceEl = container.querySelector('.product-info__price-compare');
      this.options = container.querySelectorAll('.product-variant__option');
      this.productJson = this.getProductJson();
      
      this.init();
    }

    getProductJson() {
      const script = this.container.querySelector('[type="application/json"][data-product-json]');
      return script ? JSON.parse(script.textContent) : null;
    }

    init() {
      this.options.forEach(option => {
        option.addEventListener('click', () => this.selectOption(option));
      });
    }

    selectOption(option) {
      const group = option.closest('.product-variant__options');
      group?.querySelectorAll('.product-variant__option').forEach(o => {
        o.classList.remove('product-variant__option--selected');
      });
      option.classList.add('product-variant__option--selected');
      
      this.updateVariant();
    }

    updateVariant() {
      if (!this.productJson) return;

      const selectedOptions = Array.from(this.container.querySelectorAll('.product-variant__option--selected'))
        .map(o => o.textContent.trim());

      const variant = this.productJson.variants.find(v => {
        return v.options.every((opt, i) => opt === selectedOptions[i]);
      });

      if (variant) {
        if (this.variantInput) this.variantInput.value = variant.id;
        if (this.priceEl) this.priceEl.textContent = formatMoney(variant.price);
        if (this.comparePriceEl) {
          if (variant.compare_at_price > variant.price) {
            this.comparePriceEl.textContent = formatMoney(variant.compare_at_price);
            this.comparePriceEl.style.display = 'inline';
          } else {
            this.comparePriceEl.style.display = 'none';
          }
        }
      }
    }
  }

  // ============================================
  // QUANTITY SELECTOR
  // ============================================
  
  class QuantitySelector {
    constructor(container) {
      this.container = container;
      // Support multiple selector patterns
      this.input = container.querySelector('.quantity-selector__input') || 
                   container.querySelector('.quantity-input') ||
                   container.querySelector('input[name="quantity"]');
      this.decreaseBtn = container.querySelector('[data-action="decrease"]') ||
                         container.querySelector('.quantity-btn:first-child');
      this.increaseBtn = container.querySelector('[data-action="increase"]') ||
                         container.querySelector('.quantity-btn:last-child');
      
      this.init();
    }

    init() {
      if (this.decreaseBtn) {
        this.decreaseBtn.addEventListener('click', (e) => {
          e.preventDefault();
          this.decrease();
        });
      }
      if (this.increaseBtn) {
        this.increaseBtn.addEventListener('click', (e) => {
          e.preventDefault();
          this.increase();
        });
      }
      if (this.input) {
        this.input.addEventListener('change', () => this.validate());
        this.input.addEventListener('input', () => this.validate());
      }
    }

    decrease() {
      if (!this.input) return;
      const current = parseInt(this.input.value) || 1;
      const newValue = Math.max(1, current - 1);
      this.input.value = newValue;
      this.input.dispatchEvent(new Event('change', { bubbles: true }));
    }

    increase() {
      if (!this.input) return;
      const current = parseInt(this.input.value) || 1;
      const newValue = current + 1;
      this.input.value = newValue;
      this.input.dispatchEvent(new Event('change', { bubbles: true }));
    }

    validate() {
      if (!this.input) return;
      const value = parseInt(this.input.value);
      if (isNaN(value) || value < 1) {
        this.input.value = 1;
      }
    }
  }

  // ============================================
  // ACCORDIONS
  // ============================================
  
  class Accordion {
    constructor(container) {
      this.container = container;
      this.trigger = container.querySelector('.product-accordion__trigger');
      
      this.init();
    }

    init() {
      this.trigger?.addEventListener('click', () => this.toggle());
    }

    toggle() {
      this.container.classList.toggle('product-accordion--open');
    }
  }

  // ============================================
  // PRODUCT TABS
  // ============================================
  
  class ProductTabs {
    constructor(container) {
      this.container = container;
      this.tabBtns = container.querySelectorAll('.tab-btn');
      this.tabContents = container.querySelectorAll('.tab-content');
      
      this.init();
    }

    init() {
      this.tabBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
          e.preventDefault();
          this.switchTab(btn.dataset.tab);
        });
      });
    }

    switchTab(tabId) {
      // Remove active from all buttons
      this.tabBtns.forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.tab === tabId) {
          btn.classList.add('active');
        }
      });

      // Hide all content, show selected
      this.tabContents.forEach(content => {
        content.classList.remove('active');
        if (content.id === `tab-${tabId}`) {
          content.classList.add('active');
        }
      });
    }
  }

  // ============================================
  // CAROUSEL
  // ============================================
  
  class Carousel {
    constructor(container) {
      this.container = container;
      this.track = container.querySelector('[data-carousel-track]');
      this.prevBtn = container.querySelector('[data-carousel-prev]');
      this.nextBtn = container.querySelector('[data-carousel-next]');
      
      if (this.track) this.init();
    }

    init() {
      this.prevBtn?.addEventListener('click', () => this.scroll(-1));
      this.nextBtn?.addEventListener('click', () => this.scroll(1));
    }

    scroll(direction) {
      const item = this.track.querySelector(':scope > *');
      if (!item) return;
      
      const itemWidth = item.offsetWidth + parseInt(getComputedStyle(this.track).gap || 0);
      this.track.scrollBy({ left: direction * itemWidth, behavior: 'smooth' });
    }
  }

  // ============================================
  // NEWSLETTER FORM
  // ============================================
  
  class NewsletterForm {
    constructor(form) {
      this.form = form;
      this.init();
    }

    init() {
      this.form.addEventListener('submit', async (e) => {
        // Let Shopify handle the form submission
        // This is just for visual feedback
        const btn = this.form.querySelector('[type="submit"]');
        btn?.classList.add('btn--loading');
      });
    }
  }

  // ============================================
  // SMOOTH SCROLL
  // ============================================
  
  const initSmoothScroll = () => {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', (e) => {
        const targetId = anchor.getAttribute('href');
        if (targetId === '#') return;
        
        const target = document.querySelector(targetId);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    });
  };

  // ============================================
  // ANIMATION ON SCROLL
  // ============================================
  
  const initScrollAnimations = () => {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('animate-slide-up');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });

    document.querySelectorAll('[data-animate]').forEach(el => {
      observer.observe(el);
    });
  };

  // ============================================
  // INITIALIZE
  // ============================================
  
  const init = () => {
    // Header
    new Header();

    // Cart Drawer
    new CartDrawer();

    // Cart Page (AJAX quantity +/- and Remove)
    new CartPage();

    // Product Gallery - Initialize on product pages
    const productGallery = document.querySelector('.product-gallery');
    const productThumbnails = document.querySelector('.product-thumbnails');
    
    if (productGallery && productThumbnails) {
      console.log('Initializing product gallery');
      new ProductGallery(productGallery);
    }
    
    // Also try with product-template as container
    document.querySelectorAll('.product-template').forEach(el => {
      const gallery = el.querySelector('.product-gallery');
      if (gallery && gallery.querySelector('.product-thumbnail')) {
        console.log('Initializing gallery from product-template');
        new ProductGallery(gallery);
      }
    });

    // Product Variants
    document.querySelectorAll('.product-page, .product-template').forEach(el => {
      new ProductVariants(el);
    });

    // Quantity Selectors - support both class names
    document.querySelectorAll('.quantity-selector, .product-quantity-row .quantity-selector').forEach(el => {
      new QuantitySelector(el);
    });

    // Accordions
    document.querySelectorAll('.product-accordion').forEach(el => {
      new Accordion(el);
    });

    // Product Tabs
    document.querySelectorAll('.product-tabs').forEach(el => {
      new ProductTabs(el);
    });

    // Carousels
    document.querySelectorAll('[data-carousel]').forEach(el => {
      new Carousel(el);
    });

    // Newsletter Forms
    document.querySelectorAll('.newsletter__form').forEach(el => {
      new NewsletterForm(el);
    });

    // Smooth Scroll
    initSmoothScroll();

    // Scroll Animations
    initScrollAnimations();

    // Overlay click to close everything
    document.querySelector('.overlay')?.addEventListener('click', () => {
      document.querySelector('.mobile-menu')?.classList.remove('mobile-menu--open');
      document.querySelector('.cart-drawer')?.classList.remove('cart-drawer--open');
      document.querySelector('.overlay')?.classList.remove('overlay--visible');
      document.body.classList.remove('no-scroll');
    });
    
    // ============================================
    // DIRECT THUMBNAIL CLICK HANDLER (FALLBACK)
    // ============================================
    // This ensures thumbnail clicks work even if the class-based approach fails
    document.querySelectorAll('.product-thumbnail').forEach(thumb => {
      thumb.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        const mainImage = document.querySelector('#main-product-image');
        const imageUrl = this.dataset.imageUrl || this.getAttribute('data-image-url');
        
        console.log('Direct thumbnail click:', imageUrl);
        
        if (mainImage && imageUrl) {
          // Update main image
          mainImage.src = imageUrl;
          mainImage.srcset = '';
          
          // Update active state
          document.querySelectorAll('.product-thumbnail').forEach(t => {
            t.classList.remove('active');
          });
          this.classList.add('active');
        }
      });
    });
  };

  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
