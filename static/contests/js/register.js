(function () {

  const app = {
    initialize: function () {
      $(document).ready(() => {
        this.modules();
      });
    },

    modules: function () {
      this.initElements();
      this.initVariables();
      this.initApplication();
    },

    initVariables: function () {
      this.JSSnippets = window.JSSnippets;
      this.application = null;
      this.apiRoute = '';
      this.username = this.JSSnippets.getPropertyOrDefault(window.username, '');
    },

    initElements: function () {
      this.$application = $('#app');
      this.$form = $('#register-form');
      this.$formError = $('#form-error');
    },

    initApplication: function () {
      if (!this.JSSnippets.isElementExist(this.$application)) {
        return false;
      }

      if (!this.JSSnippets.isElementExist(this.$form)) {
        return false;
      }

      this.apiRoute = this.$form.attr('action');
      let el = this.$application.attr('id');

      this.initVueApplication(el);
    },

    initVueApplication: function (el) {
      let source = this;
      const elSelector = '#' + el;
      const delimiters = ['[[', ']]'];
      const data = {
        success: '',
        error: '',
        secret_word: '',
        username: source.username,
      };
      const methods = {
        setSuccess: function (text) {
          this.success = text;
          return this;
        },

        setError: function (text) {
          this.error = text;
          return this;
        },

        clearNotifications: function () {
          return this.setSuccess('').setError('');
        },

        submitForm: function () {
          this.error = '';
          this.$validator.validate().then(valid => {
            if (!valid) {
              return false;
            }

            let data = this.$data;

            $.post(this.apiRoute, data).done(response => {
              if (response.status !== 'ok') {
                this.error = response.error;
                return false;
              }

              window.location.href = response.data.redirect;
            });
          });
        },

      };
      const computed = {};
      const watch = {};

      this.application = new Vue({
        el: elSelector,
        delimiters: delimiters,
        data: data,
        methods: methods,
        computed: computed,
        watch: watch,
        mounted: function () {

        },
      });
    },
  };

  app.initialize();
})();
