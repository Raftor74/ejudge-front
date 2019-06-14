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
    },

    initElements: function () {
      this.$application = $('#app');
      this.$form = $('#contest-edit-form');
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
          this.clearNotifications();
          this.$validator.validate().then(valid => {
            if (!valid) {
              return false;
            }

            let data = {};

            $.post(this.apiRoute, data).done(response => {
              if (response.status !== 'ok') {
                this.setError(response.error);
                source.JSSnippets.focusOnElement(source.$formError);
                return false;
              }

              window.location.href = response.data.redirect;
            });

            return false;
          });
        },
      };
      const computed = {};

      this.application = new Vue({
        el: elSelector,
        delimiters: delimiters,
        data: data,
        methods: methods,
        computed: computed,
        mounted: function () {

        },
      });
    },
  };

  app.initialize();
})();
