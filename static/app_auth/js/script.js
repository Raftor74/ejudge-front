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
      this.initApplications();
    },

    initVariables: function () {
      this.JSSnippets = window.JSSnippets;
      this.loginApp = null;
      this.registrationApp = null;
      this.apiRoute = '';
    },

    initElements: function () {
      this.$loginApp = $('#login-app');
      this.$registrationApp = $('#registration-app');
      this.$loginForm = $('#login-form');
      this.$registrationForm = $('#registration-form');

    },

    initApplications: function () {
      this.initLoginApp();
      this.initRegistrationApp();
    },

    initLoginApp: function () {
      if (!this.JSSnippets.isElementExist(this.$loginApp)) {
        return false;
      }

      if (!this.JSSnippets.isElementExist(this.$loginForm)) {
        return false;
      }

      let el = this.$loginApp.attr('id');
      this.apiRoute = this.$loginForm.attr('action');
      this.initLoginVueApp(el);
    },

    initRegistrationApp: function () {
      if (!this.JSSnippets.isElementExist(this.$registrationApp)) {
        return false;
      }

      if (!this.JSSnippets.isElementExist(this.$registrationForm)) {
        return false;
      }

      let el = this.$registrationApp.attr('id');
      this.apiRoute = this.$registrationForm.attr('action');
      this.initRegistrationVueApp(el);
    },

    initLoginVueApp: function (el) {
      const elSelector = '#' + el;
      const delimiters = ['[[', ']]'];

      const data = {
        login: '',
        password: '',
        error: '',
      };

      const methods = {
        submitForm: function () {
          this.error = '';
          this.$validator.validate().then(valid => {
            if (!valid) {
              return false;
            }

            let data = {
              login: this.login,
              password: this.password,
            };

            $.post(this.apiRoute, data).done(response => {
              if (response.status !== 'ok') {
                this.error = response.error;
                return false;
              }

              window.location.reload();
            });
          });
        }
      };

      const computed = {};

      this.loginApp = new Vue({
        el: elSelector,
        delimiters: delimiters,
        data: data,
        methods: methods,
        computed: computed,
        mounted: function () {

        },
      });
    },

    initRegistrationVueApp: function (el) {
      const elSelector = '#' + el;
      const delimiters = ['[[', ']]'];
      const data = {
        login: '',
        email: '',
        firstName: '',
        lastName: '',
        password: '',
        confirmPassword: '',
        error: '',
      };
      const methods = {
        submitForm: function () {
          this.error = '';
          this.$validator.validate().then(valid => {
            if (!valid) {
              return false;
            }

            let data = {
              login: this.login,
              password: this.password,
            };

            $.post(this.apiRoute, data).done(response => {
              if (response.status !== 'ok') {
                this.error = response.error;
                return false;
              }

              window.location.reload();
            });
          });
        }
      };
      const computed = {};

      this.registrationApp = new Vue({
        el: elSelector,
        data: data,
        delimiters: delimiters,
        methods: methods,
        computed: computed,
        mounted: function () {

        },
      });
    },

  };

  app.initialize();
})();
