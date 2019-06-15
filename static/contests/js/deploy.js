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
      this.$form = $('#deploy-form');
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
        contestStatus: [],
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

        getContestStatus: function () {
          this.requestContestStatus()
          .then((response) => {
            this.contestStatus = response.data;
          })
          .catch((error)=>{
            console.error(error)
          });
        },

        requestContestStatus: function () {
          return new Promise((resolve, reject) => {
            $.post(this.apiRoute, {"status": true}).done(response => {
              if (response.status !== 'ok') {
                reject(response);
              }
              resolve(response);
            });
          });
        },

        sendDeployAction: function(action, success_text) {
          let data = {};
          data[action] = true;
          $.post(this.apiRoute, data).done(response => {
            if (response.status !== 'ok') {
              this.setError(response.error);
              source.JSSnippets.focusOnElement(source.$formError);
              return false;
            }
            this.setSuccess(success_text);
            this.getContestStatus();
          });

          return false;
        },

        deployContest: function () {
          return this.sendDeployAction("deploy", "Турнир развёрнут");
        },

        reloadContest: function () {
          return this.sendDeployAction("reload", "Турнир переразвёрнут");
        },

        removeContest: function () {
          return this.sendDeployAction("remove", "Турнир свернут");
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
          this.getContestStatus();
        },
      });
    },
  };

  app.initialize();
})();
