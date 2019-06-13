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
      this.$form = $('#problem-create-form');
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
        title: '',
        description: '',
        epsilon: '',
        max_vm_size: 64,
        max_exec_time: 5,
        checker: '',
        is_visible: false,
        tests_examples: [{input:'', output:''}],
        tests: [{input:'', output:''}],
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

        getEmptyTestObject: function () {
          return {input:'', output:''};
        },

        clearEmptyTestsExamples: function () {
          this.tests_examples = this.clearEmptyTests(this.tests_examples);
        },

        clearEmptyTestsReal: function () {
          this.tests = this.clearEmptyTests(this.tests);
        },

        clearEmptyTests: function (tests) {

          for (let i = tests.length - 1; i >= 0; i--)
          {
            let test = tests[i];

            let input = test.input.toString().trim();
            let output = test.output.toString().trim();

            if (!input.length && !output.length) {
              tests.splice(i, 1);
            }
          }

          return tests;
        },

        addEmptyTestExample: function () {
          this.tests_examples.push(this.getEmptyTestObject());
        },

        addEmptyTest: function () {
          this.tests.push(this.getEmptyTestObject());
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

            let data = {
              title: this.title,
              description: this.description,
              epsilon: this.epsilon,
              max_vm_size: this.max_vm_size,
              max_exec_time: this.max_exec_time,
              checker: this.checker,
              is_visible: this.is_visible,
              tests_examples: JSON.stringify(this.clearEmptyTests(this.tests_examples)),
              tests: JSON.stringify(this.clearEmptyTests(this.tests)),
            };

            $.post(this.apiRoute, data).done(response => {
              if (response.status !== 'ok') {
                this.setError(response.error);
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
