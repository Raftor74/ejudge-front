$(document).ready(function () {

  const JSSnippets = window.JSSnippets;
  const csrfToken = JSSnippets.getCookie('csrftoken');

  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken", csrfToken);
    }
  });

  /* Настройка VeeValidate */
  const dictionary = {
    ru: {
      messages: {
        required: () => 'Заполните данное поле'
      }
    },
  };


  Vue.use(VeeValidate, {
    aria: true,
    locale: 'ru',
    dictionary: dictionary,
    classes: true,
    classNames: {
      valid: 'is-valid',
      invalid: 'is-invalid'
    }
  });

});