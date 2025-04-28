(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_ebnf"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/ebnf.js":
/*!***********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/ebnf.js ***!
  \***********************************************************************************************/
/***/ ((module) => {

/*
Language: Extended Backus-Naur Form
Author: Alex McKibben <alex@nullscope.net>
Website: https://en.wikipedia.org/wiki/Extended_Backus–Naur_form
*/

/** @type LanguageFn */
function ebnf(hljs) {
  const commentMode = hljs.COMMENT(/\(\*/, /\*\)/);

  const nonTerminalMode = {
    className: "attribute",
    begin: /^[ ]*[a-zA-Z]+([\s_-]+[a-zA-Z]+)*/
  };

  const specialSequenceMode = {
    className: "meta",
    begin: /\?.*\?/
  };

  const ruleBodyMode = {
    begin: /=/,
    end: /[.;]/,
    contains: [
      commentMode,
      specialSequenceMode,
      {
        // terminals
        className: 'string',
        variants: [
          hljs.APOS_STRING_MODE,
          hljs.QUOTE_STRING_MODE,
          {
            begin: '`',
            end: '`'
          }
        ]
      }
    ]
  };

  return {
    name: 'Extended Backus-Naur Form',
    illegal: /\S/,
    contains: [
      commentMode,
      nonTerminalMode,
      ruleBodyMode
    ]
  };
}

module.exports = ebnf;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfZWJuZi5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0EsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL2VibmYuanMiXSwic291cmNlc0NvbnRlbnQiOlsiLypcbkxhbmd1YWdlOiBFeHRlbmRlZCBCYWNrdXMtTmF1ciBGb3JtXG5BdXRob3I6IEFsZXggTWNLaWJiZW4gPGFsZXhAbnVsbHNjb3BlLm5ldD5cbldlYnNpdGU6IGh0dHBzOi8vZW4ud2lraXBlZGlhLm9yZy93aWtpL0V4dGVuZGVkX0JhY2t1c+KAk05hdXJfZm9ybVxuKi9cblxuLyoqIEB0eXBlIExhbmd1YWdlRm4gKi9cbmZ1bmN0aW9uIGVibmYoaGxqcykge1xuICBjb25zdCBjb21tZW50TW9kZSA9IGhsanMuQ09NTUVOVCgvXFwoXFwqLywgL1xcKlxcKS8pO1xuXG4gIGNvbnN0IG5vblRlcm1pbmFsTW9kZSA9IHtcbiAgICBjbGFzc05hbWU6IFwiYXR0cmlidXRlXCIsXG4gICAgYmVnaW46IC9eWyBdKlthLXpBLVpdKyhbXFxzXy1dK1thLXpBLVpdKykqL1xuICB9O1xuXG4gIGNvbnN0IHNwZWNpYWxTZXF1ZW5jZU1vZGUgPSB7XG4gICAgY2xhc3NOYW1lOiBcIm1ldGFcIixcbiAgICBiZWdpbjogL1xcPy4qXFw/L1xuICB9O1xuXG4gIGNvbnN0IHJ1bGVCb2R5TW9kZSA9IHtcbiAgICBiZWdpbjogLz0vLFxuICAgIGVuZDogL1suO10vLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBjb21tZW50TW9kZSxcbiAgICAgIHNwZWNpYWxTZXF1ZW5jZU1vZGUsXG4gICAgICB7XG4gICAgICAgIC8vIHRlcm1pbmFsc1xuICAgICAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgICAgICB2YXJpYW50czogW1xuICAgICAgICAgIGhsanMuQVBPU19TVFJJTkdfTU9ERSxcbiAgICAgICAgICBobGpzLlFVT1RFX1NUUklOR19NT0RFLFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiAnYCcsXG4gICAgICAgICAgICBlbmQ6ICdgJ1xuICAgICAgICAgIH1cbiAgICAgICAgXVxuICAgICAgfVxuICAgIF1cbiAgfTtcblxuICByZXR1cm4ge1xuICAgIG5hbWU6ICdFeHRlbmRlZCBCYWNrdXMtTmF1ciBGb3JtJyxcbiAgICBpbGxlZ2FsOiAvXFxTLyxcbiAgICBjb250YWluczogW1xuICAgICAgY29tbWVudE1vZGUsXG4gICAgICBub25UZXJtaW5hbE1vZGUsXG4gICAgICBydWxlQm9keU1vZGVcbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gZWJuZjtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==