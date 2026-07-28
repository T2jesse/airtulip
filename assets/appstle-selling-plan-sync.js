/**
 * Appstle subscription widget renders selling_plan as radio inputs outside the
 * theme product form. Sync the selected plan into a hidden input inside the form
 * so /cart/add receives selling_plan (15% discount + subscription terms).
 */
(function () {
  const APPSTLE_EVENTS = [
    'AppstleSubscription:SubscriptionWidget:widgetInitialised',
    'AppstleSubscription:SubscriptionWidget:SubscriptionWidgetUpdated',
    'AppstleSubscription:SubscriptionWidget:SellingPlanSelected',
    'AppstleSubscription:SubscriptionWidget:SellingPlanDeSelected',
    'AppstleSubscription:SubscriptionWidget:sellingPlanChanged'
  ];

  function getSelectedSellingPlanId() {
    const selected = document.querySelector(
      '.appstle_sub_widget input[name="selling_plan"]:checked'
    );
    return selected && selected.value ? selected.value : '';
  }

  function syncSellingPlanInputs() {
    const planId = getSelectedSellingPlanId();
    document
      .querySelectorAll('form[data-type="add-to-cart-form"] [data-appstle-selling-plan-input]')
      .forEach((input) => {
        input.value = planId;
      });
  }

  APPSTLE_EVENTS.forEach((eventName) => {
    document.addEventListener(eventName, syncSellingPlanInputs);
  });

  document.addEventListener('change', (event) => {
    if (event.target && event.target.name === 'selling_plan') {
      syncSellingPlanInputs();
    }
  });

  document.addEventListener('submit', (event) => {
    if (event.target && event.target.matches('form[data-type="add-to-cart-form"]')) {
      syncSellingPlanInputs();
    }
  }, true);

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', syncSellingPlanInputs);
  } else {
    syncSellingPlanInputs();
  }
})();
