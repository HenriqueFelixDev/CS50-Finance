const setLoading = (isLoading, buttonElement) => {
  const spinnerEl = buttonElement.querySelector('[uk-spinner]');

  if (isLoading) {
    buttonElement.setAttribute('disabled', 'disabled');

    if (spinnerEl) {
      spinnerEl.classList.remove('uk-hidden');
    }
  } else {
    buttonElement.removeAttribute('disabled');

    if (spinnerEl) {
      spinnerEl.classList.add('uk-hidden');
    }
  }
}

const setError = (message, alertElement) => {
  alertElement.textContent = message;
  
  if (message) {
    alertElement.classList.remove('uk-hidden');
  } else {
    alertElement.classList.add('uk-hidden');
  }
}

const sendFormData = async (formElement) => {
  const result = await fetch(formElement.action, {
    method: 'post',
    body: new FormData(formElement),
  });

  if (result.ok) {
    return true;
  }

  const {
    error = 'unexpected error',
  } = await result.json().catch(() => ({}));

  throw error;
}