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
      this.systemStartApiRoute = this.JSSnippets.getPropertyOrDefault(window.SYSTEM_START_API_ROUTE, '');
      this.systemReloadApiRoute = this.JSSnippets.getPropertyOrDefault(window.SYSTEM_RELOAD_API_ROUTE, '');
      this.systemStopApiRoute = this.JSSnippets.getPropertyOrDefault(window.SYSTEM_STOP_API_ROUTE, '');
      this.systemStatusApiRoute = this.JSSnippets.getPropertyOrDefault(window.SYSTEM_STATUS_API_ROUTE, '');
    },

    initElements: function () {
      this.$application = $('#app');
    },

    initApplication: function () {
      if (!this.JSSnippets.isElementExist(this.$application)) {
        return false;
      }

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
        systemStatus: {},
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

        sendSystemControlRequest: function (url) {
          return new Promise((resolve, reject) => {
            $.post(url, {}, function (response) {
              if (response.status !== "ok") {
                reject(response);
              } else {
                resolve(response);
              }
            })
          });
        },

        startSystem: function () {
          this.sendSystemControlRequest(source.systemStartApiRoute)
          .then((response) => {
            this.clearNotifications().setSuccess("Система Ejudge запущена").getSystemStatus();
          })
          .catch((response) => {
            this.clearNotifications().setError(response.error);
          });
        },
        stopSystem: function () {
          this.sendSystemControlRequest(source.systemStopApiRoute)
          .then((response) => {
            this.clearNotifications().setSuccess("Система Ejudge остановлена").getSystemStatus();
          })
          .catch((response) => {
            this.clearNotifications().setError(response.error);
          });
        },
        reloadSystem: function () {
          this.sendSystemControlRequest(source.systemReloadApiRoute)
          .then((response) => {
            this.clearNotifications().setSuccess("Система Ejudge перезапущена").getSystemStatus();
          })
          .catch((response) => {
            this.clearNotifications().setError(response.error);
          });
        },
        getSystemStatus: function () {
          this.sendSystemControlRequest(source.systemStatusApiRoute)
          .then((response) => {
            this.systemStatus = response.data
          })
          .catch((response) => {
            this.clearNotifications().setError(response.error);
          });
        }
      };
      const computed = {};

      this.application = new Vue({
        el: elSelector,
        delimiters: delimiters,
        data: data,
        methods: methods,
        computed: computed,
        mounted: function () {
          this.getSystemStatus();
        },
      });
    },
  };

  app.initialize();
})();
