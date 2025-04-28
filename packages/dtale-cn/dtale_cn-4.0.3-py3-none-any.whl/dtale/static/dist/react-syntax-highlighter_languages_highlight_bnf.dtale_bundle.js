(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_bnf"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/bnf.js":
/*!**********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/bnf.js ***!
  \**********************************************************************************************/
/***/ ((module) => {

/*
Language: Backus–Naur Form
Website: https://en.wikipedia.org/wiki/Backus–Naur_form
Author: Oleg Efimov <efimovov@gmail.com>
*/

/** @type LanguageFn */
function bnf(hljs) {
  return {
    name: 'Backus–Naur Form',
    contains: [
      // Attribute
      {
        className: 'attribute',
        begin: /</,
        end: />/
      },
      // Specific
      {
        begin: /::=/,
        end: /$/,
        contains: [
          {
            begin: /</,
            end: />/
          },
          // Common
          hljs.C_LINE_COMMENT_MODE,
          hljs.C_BLOCK_COMMENT_MODE,
          hljs.APOS_STRING_MODE,
          hljs.QUOTE_STRING_MODE
        ]
      }
    ]
  };
}

module.exports = bnf;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfYm5mLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFdBQVc7QUFDWDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvYm5mLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogQmFja3Vz4oCTTmF1ciBGb3JtXG5XZWJzaXRlOiBodHRwczovL2VuLndpa2lwZWRpYS5vcmcvd2lraS9CYWNrdXPigJNOYXVyX2Zvcm1cbkF1dGhvcjogT2xlZyBFZmltb3YgPGVmaW1vdm92QGdtYWlsLmNvbT5cbiovXG5cbi8qKiBAdHlwZSBMYW5ndWFnZUZuICovXG5mdW5jdGlvbiBibmYoaGxqcykge1xuICByZXR1cm4ge1xuICAgIG5hbWU6ICdCYWNrdXPigJNOYXVyIEZvcm0nLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICAvLyBBdHRyaWJ1dGVcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnYXR0cmlidXRlJyxcbiAgICAgICAgYmVnaW46IC88LyxcbiAgICAgICAgZW5kOiAvPi9cbiAgICAgIH0sXG4gICAgICAvLyBTcGVjaWZpY1xuICAgICAge1xuICAgICAgICBiZWdpbjogLzo6PS8sXG4gICAgICAgIGVuZDogLyQvLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiAvPC8sXG4gICAgICAgICAgICBlbmQ6IC8+L1xuICAgICAgICAgIH0sXG4gICAgICAgICAgLy8gQ29tbW9uXG4gICAgICAgICAgaGxqcy5DX0xJTkVfQ09NTUVOVF9NT0RFLFxuICAgICAgICAgIGhsanMuQ19CTE9DS19DT01NRU5UX01PREUsXG4gICAgICAgICAgaGxqcy5BUE9TX1NUUklOR19NT0RFLFxuICAgICAgICAgIGhsanMuUVVPVEVfU1RSSU5HX01PREVcbiAgICAgICAgXVxuICAgICAgfVxuICAgIF1cbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBibmY7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=