const actionFormEl = document.getElementById('action-modal-form');
const actionModalTitle = document.querySelector('#action-modal .uk-modal-title');
const submitButtonEl = document.querySelector('#action-modal-form button[type=submit]');
const actionModalAlertEl = document.getElementById('action-modal-alert');

const forms = {
  buy: {
    title: 'Buy action',
    buttonText: 'Buy',
    formAction: '/actions/buy'
  },
  sell: {
    title: 'Sell action',
    buttonText: 'Sell',
    formAction: '/actions/sell'
  },
}

const updateActionModalForm = (formName, symbol = '', shares = '') => {
  const { title, buttonText, formAction } = forms[formName] || {};

  actionModalTitle.textContent = title;
  submitButtonEl.querySelector('.submit-content').textContent = buttonText;
  actionFormEl.setAttribute('action', formAction);
  actionFormEl.symbol.value = symbol;
  actionFormEl.shares.value = '';
  actionFormEl.shares.max = shares;
};

actionFormEl.addEventListener('submit', async (e) => {
  e.preventDefault();

  try {
    setLoading(true, submitButtonEl);
    setError(null, actionModalAlertEl);

    await sendFormData(e.target);
    
    location.reload();
  } catch (e) {
    setError(error, actionModalAlertEl);
  } finally {
    setLoading(false, submitButtonEl);
  }
});