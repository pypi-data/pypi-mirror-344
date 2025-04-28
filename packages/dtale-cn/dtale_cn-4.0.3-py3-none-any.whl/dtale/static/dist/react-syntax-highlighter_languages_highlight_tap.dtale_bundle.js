(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_tap"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/tap.js":
/*!**********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/tap.js ***!
  \**********************************************************************************************/
/***/ ((module) => {

/*
Language: Test Anything Protocol
Description: TAP, the Test Anything Protocol, is a simple text-based interface between testing modules in a test harness.
Requires: yaml.js
Author: Sergey Bronnikov <sergeyb@bronevichok.ru>
Website: https://testanything.org
*/

function tap(hljs) {
  return {
    name: 'Test Anything Protocol',
    case_insensitive: true,
    contains: [
      hljs.HASH_COMMENT_MODE,
      // version of format and total amount of testcases
      {
        className: 'meta',
        variants: [
          {
            begin: '^TAP version (\\d+)$'
          },
          {
            begin: '^1\\.\\.(\\d+)$'
          }
        ]
      },
      // YAML block
      {
        begin: /---$/,
        end: '\\.\\.\\.$',
        subLanguage: 'yaml',
        relevance: 0
      },
      // testcase number
      {
        className: 'number',
        begin: ' (\\d+) '
      },
      // testcase status and description
      {
        className: 'symbol',
        variants: [
          {
            begin: '^ok'
          },
          {
            begin: '^not ok'
          }
        ]
      }
    ]
  };
}

module.exports = tap;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfdGFwLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFdBQVc7QUFDWDtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsV0FBVztBQUNYO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL3RhcC5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKlxuTGFuZ3VhZ2U6IFRlc3QgQW55dGhpbmcgUHJvdG9jb2xcbkRlc2NyaXB0aW9uOiBUQVAsIHRoZSBUZXN0IEFueXRoaW5nIFByb3RvY29sLCBpcyBhIHNpbXBsZSB0ZXh0LWJhc2VkIGludGVyZmFjZSBiZXR3ZWVuIHRlc3RpbmcgbW9kdWxlcyBpbiBhIHRlc3QgaGFybmVzcy5cblJlcXVpcmVzOiB5YW1sLmpzXG5BdXRob3I6IFNlcmdleSBCcm9ubmlrb3YgPHNlcmdleWJAYnJvbmV2aWNob2sucnU+XG5XZWJzaXRlOiBodHRwczovL3Rlc3Rhbnl0aGluZy5vcmdcbiovXG5cbmZ1bmN0aW9uIHRhcChobGpzKSB7XG4gIHJldHVybiB7XG4gICAgbmFtZTogJ1Rlc3QgQW55dGhpbmcgUHJvdG9jb2wnLFxuICAgIGNhc2VfaW5zZW5zaXRpdmU6IHRydWUsXG4gICAgY29udGFpbnM6IFtcbiAgICAgIGhsanMuSEFTSF9DT01NRU5UX01PREUsXG4gICAgICAvLyB2ZXJzaW9uIG9mIGZvcm1hdCBhbmQgdG90YWwgYW1vdW50IG9mIHRlc3RjYXNlc1xuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdtZXRhJyxcbiAgICAgICAgdmFyaWFudHM6IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbjogJ15UQVAgdmVyc2lvbiAoXFxcXGQrKSQnXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbjogJ14xXFxcXC5cXFxcLihcXFxcZCspJCdcbiAgICAgICAgICB9XG4gICAgICAgIF1cbiAgICAgIH0sXG4gICAgICAvLyBZQU1MIGJsb2NrXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAvLS0tJC8sXG4gICAgICAgIGVuZDogJ1xcXFwuXFxcXC5cXFxcLiQnLFxuICAgICAgICBzdWJMYW5ndWFnZTogJ3lhbWwnLFxuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH0sXG4gICAgICAvLyB0ZXN0Y2FzZSBudW1iZXJcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnbnVtYmVyJyxcbiAgICAgICAgYmVnaW46ICcgKFxcXFxkKykgJ1xuICAgICAgfSxcbiAgICAgIC8vIHRlc3RjYXNlIHN0YXR1cyBhbmQgZGVzY3JpcHRpb25cbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnc3ltYm9sJyxcbiAgICAgICAgdmFyaWFudHM6IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbjogJ15vaydcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiAnXm5vdCBvaydcbiAgICAgICAgICB9XG4gICAgICAgIF1cbiAgICAgIH1cbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gdGFwO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9