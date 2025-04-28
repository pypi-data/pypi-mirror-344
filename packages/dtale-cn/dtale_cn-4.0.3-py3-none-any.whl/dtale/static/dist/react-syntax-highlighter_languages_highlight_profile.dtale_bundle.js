(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_profile"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/profile.js":
/*!**************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/profile.js ***!
  \**************************************************************************************************/
/***/ ((module) => {

/*
Language: Python profiler
Description: Python profiler results
Author: Brian Beck <exogen@gmail.com>
*/

function profile(hljs) {
  return {
    name: 'Python profiler',
    contains: [
      hljs.C_NUMBER_MODE,
      {
        begin: '[a-zA-Z_][\\da-zA-Z_]+\\.[\\da-zA-Z_]{1,3}',
        end: ':',
        excludeEnd: true
      },
      {
        begin: '(ncalls|tottime|cumtime)',
        end: '$',
        keywords: 'ncalls tottime|10 cumtime|10 filename',
        relevance: 10
      },
      {
        begin: 'function calls',
        end: '$',
        contains: [ hljs.C_NUMBER_MODE ],
        relevance: 10
      },
      hljs.APOS_STRING_MODE,
      hljs.QUOTE_STRING_MODE,
      {
        className: 'string',
        begin: '\\(',
        end: '\\)$',
        excludeBegin: true,
        excludeEnd: true,
        relevance: 0
      }
    ]
  };
}

module.exports = profile;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfcHJvZmlsZS5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLHNEQUFzRCxJQUFJO0FBQzFEO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9wcm9maWxlLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogUHl0aG9uIHByb2ZpbGVyXG5EZXNjcmlwdGlvbjogUHl0aG9uIHByb2ZpbGVyIHJlc3VsdHNcbkF1dGhvcjogQnJpYW4gQmVjayA8ZXhvZ2VuQGdtYWlsLmNvbT5cbiovXG5cbmZ1bmN0aW9uIHByb2ZpbGUoaGxqcykge1xuICByZXR1cm4ge1xuICAgIG5hbWU6ICdQeXRob24gcHJvZmlsZXInLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBobGpzLkNfTlVNQkVSX01PREUsXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnW2EtekEtWl9dW1xcXFxkYS16QS1aX10rXFxcXC5bXFxcXGRhLXpBLVpfXXsxLDN9JyxcbiAgICAgICAgZW5kOiAnOicsXG4gICAgICAgIGV4Y2x1ZGVFbmQ6IHRydWVcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnKG5jYWxsc3x0b3R0aW1lfGN1bXRpbWUpJyxcbiAgICAgICAgZW5kOiAnJCcsXG4gICAgICAgIGtleXdvcmRzOiAnbmNhbGxzIHRvdHRpbWV8MTAgY3VtdGltZXwxMCBmaWxlbmFtZScsXG4gICAgICAgIHJlbGV2YW5jZTogMTBcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnZnVuY3Rpb24gY2FsbHMnLFxuICAgICAgICBlbmQ6ICckJyxcbiAgICAgICAgY29udGFpbnM6IFsgaGxqcy5DX05VTUJFUl9NT0RFIF0sXG4gICAgICAgIHJlbGV2YW5jZTogMTBcbiAgICAgIH0sXG4gICAgICBobGpzLkFQT1NfU1RSSU5HX01PREUsXG4gICAgICBobGpzLlFVT1RFX1NUUklOR19NT0RFLFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgICAgICBiZWdpbjogJ1xcXFwoJyxcbiAgICAgICAgZW5kOiAnXFxcXCkkJyxcbiAgICAgICAgZXhjbHVkZUJlZ2luOiB0cnVlLFxuICAgICAgICBleGNsdWRlRW5kOiB0cnVlLFxuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH1cbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gcHJvZmlsZTtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==