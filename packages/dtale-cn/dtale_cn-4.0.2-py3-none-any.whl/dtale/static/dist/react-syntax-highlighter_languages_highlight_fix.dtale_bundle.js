(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_fix"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/fix.js":
/*!**********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/fix.js ***!
  \**********************************************************************************************/
/***/ ((module) => {

/*
Language: FIX
Author: Brent Bradbury <brent@brentium.com>
*/

/** @type LanguageFn */
function fix(hljs) {
  return {
    name: 'FIX',
    contains: [{
      begin: /[^\u2401\u0001]+/,
      end: /[\u2401\u0001]/,
      excludeEnd: true,
      returnBegin: true,
      returnEnd: false,
      contains: [
        {
          begin: /([^\u2401\u0001=]+)/,
          end: /=([^\u2401\u0001=]+)/,
          returnEnd: true,
          returnBegin: false,
          className: 'attr'
        },
        {
          begin: /=/,
          end: /([\u2401\u0001])/,
          excludeEnd: true,
          excludeBegin: true,
          className: 'string'
        }
      ]
    }],
    case_insensitive: true
  };
}

module.exports = fix;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfZml4LmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxTQUFTO0FBQ1Q7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL2ZpeC5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKlxuTGFuZ3VhZ2U6IEZJWFxuQXV0aG9yOiBCcmVudCBCcmFkYnVyeSA8YnJlbnRAYnJlbnRpdW0uY29tPlxuKi9cblxuLyoqIEB0eXBlIExhbmd1YWdlRm4gKi9cbmZ1bmN0aW9uIGZpeChobGpzKSB7XG4gIHJldHVybiB7XG4gICAgbmFtZTogJ0ZJWCcsXG4gICAgY29udGFpbnM6IFt7XG4gICAgICBiZWdpbjogL1teXFx1MjQwMVxcdTAwMDFdKy8sXG4gICAgICBlbmQ6IC9bXFx1MjQwMVxcdTAwMDFdLyxcbiAgICAgIGV4Y2x1ZGVFbmQ6IHRydWUsXG4gICAgICByZXR1cm5CZWdpbjogdHJ1ZSxcbiAgICAgIHJldHVybkVuZDogZmFsc2UsXG4gICAgICBjb250YWluczogW1xuICAgICAgICB7XG4gICAgICAgICAgYmVnaW46IC8oW15cXHUyNDAxXFx1MDAwMT1dKykvLFxuICAgICAgICAgIGVuZDogLz0oW15cXHUyNDAxXFx1MDAwMT1dKykvLFxuICAgICAgICAgIHJldHVybkVuZDogdHJ1ZSxcbiAgICAgICAgICByZXR1cm5CZWdpbjogZmFsc2UsXG4gICAgICAgICAgY2xhc3NOYW1lOiAnYXR0cidcbiAgICAgICAgfSxcbiAgICAgICAge1xuICAgICAgICAgIGJlZ2luOiAvPS8sXG4gICAgICAgICAgZW5kOiAvKFtcXHUyNDAxXFx1MDAwMV0pLyxcbiAgICAgICAgICBleGNsdWRlRW5kOiB0cnVlLFxuICAgICAgICAgIGV4Y2x1ZGVCZWdpbjogdHJ1ZSxcbiAgICAgICAgICBjbGFzc05hbWU6ICdzdHJpbmcnXG4gICAgICAgIH1cbiAgICAgIF1cbiAgICB9XSxcbiAgICBjYXNlX2luc2Vuc2l0aXZlOiB0cnVlXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gZml4O1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9