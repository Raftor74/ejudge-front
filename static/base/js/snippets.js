$(document).ready(function () {
  window.JSSnippets = {

    isElementExist: function ($element) {
      return $element.length > 0;
    },

    getPropertyOrDefault: function (variable, _default) {
      return (typeof variable !== "undefined") ? variable : _default;
    },

    printConsoleError: function (error) {
      console.error(error);
    },

    getElementValueOrDefault: function ($element, _default) {
      return (this.isElementExist($element)) ? $element.val() : _default;
    },

    getElementTextOrDefault: function ($element, _default) {
      return (this.isElementExist($element)) ? $element.text() : _default;
    },

    getElementDataAttributeOrDefault: function ($element, key, _default) {
      return (this.isElementExist($element)) ? this.getPropertyOrDefault($element.data(key), _default) : _default;
    },

    setElementValue: function ($element, value) {
      return (this.isElementExist($element)) ? $element.val(value) : false;
    },

    setElementText: function ($element, value) {
      return (this.isElementExist($element)) ? $element.text(value) : false;
    },

    showElement: function ($element) {
      return (this.isElementExist($element)) ? $element.show() : false;
    },

    hideElement: function ($element) {
      return (this.isElementExist($element)) ? $element.hide() : false;
    },

    toggleElement: function ($element) {
      return (this.isElementExist($element)) ? $element.toggle() : false;
    },

    toggleElementClassActive: function ($element) {
      return (this.isElementExist($element))
        ? ($element.hasClass('active')) ? $element.removeClass('active') : $element.addClass('active')
        : false;
    },

    focusOnElement: function ($element) {
      return (this.isElementExist($element))
        ? $('body, html').scrollTop(parseInt($element.offset().top) - 120)
        : false;
    },

    getCookie: function getCookie(name) {
      let matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
      ));
      return matches ? decodeURIComponent(matches[1]) : undefined;
    }
  };
});