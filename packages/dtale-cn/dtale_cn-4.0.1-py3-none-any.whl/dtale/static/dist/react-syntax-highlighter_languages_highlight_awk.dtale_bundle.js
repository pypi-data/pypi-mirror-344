(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_awk"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/awk.js":
/*!**********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/awk.js ***!
  \**********************************************************************************************/
/***/ ((module) => {

/*
Language: Awk
Author: Matthew Daly <matthewbdaly@gmail.com>
Website: https://www.gnu.org/software/gawk/manual/gawk.html
Description: language definition for Awk scripts
*/

/** @type LanguageFn */
function awk(hljs) {
  const VARIABLE = {
    className: 'variable',
    variants: [
      {
        begin: /\$[\w\d#@][\w\d_]*/
      },
      {
        begin: /\$\{(.*?)\}/
      }
    ]
  };
  const KEYWORDS = 'BEGIN END if else while do for in break continue delete next nextfile function func exit|10';
  const STRING = {
    className: 'string',
    contains: [hljs.BACKSLASH_ESCAPE],
    variants: [
      {
        begin: /(u|b)?r?'''/,
        end: /'''/,
        relevance: 10
      },
      {
        begin: /(u|b)?r?"""/,
        end: /"""/,
        relevance: 10
      },
      {
        begin: /(u|r|ur)'/,
        end: /'/,
        relevance: 10
      },
      {
        begin: /(u|r|ur)"/,
        end: /"/,
        relevance: 10
      },
      {
        begin: /(b|br)'/,
        end: /'/
      },
      {
        begin: /(b|br)"/,
        end: /"/
      },
      hljs.APOS_STRING_MODE,
      hljs.QUOTE_STRING_MODE
    ]
  };
  return {
    name: 'Awk',
    keywords: {
      keyword: KEYWORDS
    },
    contains: [
      VARIABLE,
      STRING,
      hljs.REGEXP_MODE,
      hljs.HASH_COMMENT_MODE,
      hljs.NUMBER_MODE
    ]
  };
}

module.exports = awk;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfYXdrLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBLG9CQUFvQixPQUFPO0FBQzNCO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9hd2suanMiXSwic291cmNlc0NvbnRlbnQiOlsiLypcbkxhbmd1YWdlOiBBd2tcbkF1dGhvcjogTWF0dGhldyBEYWx5IDxtYXR0aGV3YmRhbHlAZ21haWwuY29tPlxuV2Vic2l0ZTogaHR0cHM6Ly93d3cuZ251Lm9yZy9zb2Z0d2FyZS9nYXdrL21hbnVhbC9nYXdrLmh0bWxcbkRlc2NyaXB0aW9uOiBsYW5ndWFnZSBkZWZpbml0aW9uIGZvciBBd2sgc2NyaXB0c1xuKi9cblxuLyoqIEB0eXBlIExhbmd1YWdlRm4gKi9cbmZ1bmN0aW9uIGF3ayhobGpzKSB7XG4gIGNvbnN0IFZBUklBQkxFID0ge1xuICAgIGNsYXNzTmFtZTogJ3ZhcmlhYmxlJyxcbiAgICB2YXJpYW50czogW1xuICAgICAge1xuICAgICAgICBiZWdpbjogL1xcJFtcXHdcXGQjQF1bXFx3XFxkX10qL1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC9cXCRcXHsoLio/KVxcfS9cbiAgICAgIH1cbiAgICBdXG4gIH07XG4gIGNvbnN0IEtFWVdPUkRTID0gJ0JFR0lOIEVORCBpZiBlbHNlIHdoaWxlIGRvIGZvciBpbiBicmVhayBjb250aW51ZSBkZWxldGUgbmV4dCBuZXh0ZmlsZSBmdW5jdGlvbiBmdW5jIGV4aXR8MTAnO1xuICBjb25zdCBTVFJJTkcgPSB7XG4gICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICBjb250YWluczogW2hsanMuQkFDS1NMQVNIX0VTQ0FQRV0sXG4gICAgdmFyaWFudHM6IFtcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC8odXxiKT9yPycnJy8sXG4gICAgICAgIGVuZDogLycnJy8sXG4gICAgICAgIHJlbGV2YW5jZTogMTBcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAvKHV8Yik/cj9cIlwiXCIvLFxuICAgICAgICBlbmQ6IC9cIlwiXCIvLFxuICAgICAgICByZWxldmFuY2U6IDEwXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogLyh1fHJ8dXIpJy8sXG4gICAgICAgIGVuZDogLycvLFxuICAgICAgICByZWxldmFuY2U6IDEwXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogLyh1fHJ8dXIpXCIvLFxuICAgICAgICBlbmQ6IC9cIi8sXG4gICAgICAgIHJlbGV2YW5jZTogMTBcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAvKGJ8YnIpJy8sXG4gICAgICAgIGVuZDogLycvXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogLyhifGJyKVwiLyxcbiAgICAgICAgZW5kOiAvXCIvXG4gICAgICB9LFxuICAgICAgaGxqcy5BUE9TX1NUUklOR19NT0RFLFxuICAgICAgaGxqcy5RVU9URV9TVFJJTkdfTU9ERVxuICAgIF1cbiAgfTtcbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnQXdrJyxcbiAgICBrZXl3b3Jkczoge1xuICAgICAga2V5d29yZDogS0VZV09SRFNcbiAgICB9LFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBWQVJJQUJMRSxcbiAgICAgIFNUUklORyxcbiAgICAgIGhsanMuUkVHRVhQX01PREUsXG4gICAgICBobGpzLkhBU0hfQ09NTUVOVF9NT0RFLFxuICAgICAgaGxqcy5OVU1CRVJfTU9ERVxuICAgIF1cbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBhd2s7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=