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
        required: () => 'Заполните данное поле',
        min: () => 'Кол-во символов меньше необходимого',
        max: () => 'Кол-во символов больше необходимого',
        confirmed: (field) => 'Значение не совпадает с полем ' + field.toString(),
        email: () => 'Указан недопустимый Email',
        numeric: () => 'Значение должно содержать только цифры',
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