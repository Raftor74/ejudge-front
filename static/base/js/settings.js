$(document).ready(function () {

  const JSSnippets = window.JSSnippets;
  const csrfToken = JSSnippets.getCookie('csrftoken');

  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
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


  /* Vue Обёртка для Select2 */
  Vue.component('select2', {
    props: ['options', 'value', 'data'],
    template: '#select2-template',
    mounted: function () {
      var vm = this;
      $(this.$el)
      // init select2
      .select2(this.options)
      .val(this.value)
      .trigger('change')
      // emit event on change.
      .on('change', function () {
        vm.$emit('input', this.value);
      })
    },
    watch: {
      value: function (value) {
        // update value
        $(this.$el)
        .val(value)
        .trigger('change')
      },
      options: function (options) {
        // update options
        $(this.$el).empty().select2(this.options)
      }
    },
    destroyed: function () {
      $(this.$el).off().select2('destroy')
    }
  });

});