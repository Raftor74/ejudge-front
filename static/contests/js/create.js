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
      this.$form = $('#contest-create-form');
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
      const select2Options = {
        minimumInputLength: 1,
        allowClear: true,
        placeholder: "Введите номер или название задачи",
        ajax: {
          url: "/api/v1/problems/search/",
          delay: 300,
          type: "post",
          cache: true,
          processResults: function (response, params) {
            return {
              results: response.data
            };
          }
        }
      };

      const data = {
        success: '',
        error: '',
        name: '',
        duration: '',
        scope_system: '',
        start_time: '',
        select2_selected: '',
        select2_options: select2Options,
        is_closed: false,
        is_visible: true,
        secret_word: '',
        problems: [],
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

        removeTask: function (index) {
          this.problems.splice(index, 1);
        },

        addTask: function (task) {
          let isProblemExist = false;
          $.each(this.problems, (key, value) =>{
            if(parseInt(value.id) === parseInt(task.id)) {
              isProblemExist = true;
            }
          });

          if (!isProblemExist) {
            this.problems.push({
              id: task.id,
              title: task.title,
            });
          }
        },

        submitForm: function () {
          this.clearNotifications();
          this.$validator.validate().then(valid => {
            if (!valid) {
              return false;
            }

            if (!this.problems.length) {
              this.setError("Выберите хотя бы одну задачу для турнира");
              source.JSSnippets.focusOnElement(source.$formError);
              return false;
            }

            let data = {
              name: this.name,
              duration: this.duration,
              scope_system: this.scope_system,
              start_time: this.start_time,
              is_closed: this.is_closed ? "Y" : '',
              is_visible: this.is_visible ? "Y" : '',
              secret_word: this.secret_word,
              problems: JSON.stringify(this.problems),
            };

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
      const watch = {};

      this.application = new Vue({
        el: elSelector,
        delimiters: delimiters,
        data: data,
        methods: methods,
        computed: computed,
        watch: watch,
        mounted: function () {
          let that = this;

          $('#search_problem').on('select2:select', function(e) {
              that.addTask(e.params.data);
              that.select2_selected = '';
              $('#search_problem').val('').trigger('change');
          });

        },
      });
    },
  };

  app.initialize();
})();
