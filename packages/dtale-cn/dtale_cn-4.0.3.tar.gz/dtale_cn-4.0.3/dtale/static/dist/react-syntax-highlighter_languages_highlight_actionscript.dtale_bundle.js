(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_actionscript"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/actionscript.js":
/*!*******************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/actionscript.js ***!
  \*******************************************************************************************************/
/***/ ((module) => {

/**
 * @param {string} value
 * @returns {RegExp}
 * */

/**
 * @param {RegExp | string } re
 * @returns {string}
 */
function source(re) {
  if (!re) return null;
  if (typeof re === "string") return re;

  return re.source;
}

/**
 * @param {...(RegExp | string) } args
 * @returns {string}
 */
function concat(...args) {
  const joined = args.map((x) => source(x)).join("");
  return joined;
}

/*
Language: ActionScript
Author: Alexander Myadzel <myadzel@gmail.com>
Category: scripting
Audit: 2020
*/

/** @type LanguageFn */
function actionscript(hljs) {
  const IDENT_RE = /[a-zA-Z_$][a-zA-Z0-9_$]*/;
  const IDENT_FUNC_RETURN_TYPE_RE = /([*]|[a-zA-Z_$][a-zA-Z0-9_$]*)/;

  const AS3_REST_ARG_MODE = {
    className: 'rest_arg',
    begin: /[.]{3}/,
    end: IDENT_RE,
    relevance: 10
  };

  return {
    name: 'ActionScript',
    aliases: [ 'as' ],
    keywords: {
      keyword: 'as break case catch class const continue default delete do dynamic each ' +
        'else extends final finally for function get if implements import in include ' +
        'instanceof interface internal is namespace native new override package private ' +
        'protected public return set static super switch this throw try typeof use var void ' +
        'while with',
      literal: 'true false null undefined'
    },
    contains: [
      hljs.APOS_STRING_MODE,
      hljs.QUOTE_STRING_MODE,
      hljs.C_LINE_COMMENT_MODE,
      hljs.C_BLOCK_COMMENT_MODE,
      hljs.C_NUMBER_MODE,
      {
        className: 'class',
        beginKeywords: 'package',
        end: /\{/,
        contains: [ hljs.TITLE_MODE ]
      },
      {
        className: 'class',
        beginKeywords: 'class interface',
        end: /\{/,
        excludeEnd: true,
        contains: [
          { beginKeywords: 'extends implements' },
          hljs.TITLE_MODE
        ]
      },
      {
        className: 'meta',
        beginKeywords: 'import include',
        end: /;/,
        keywords: { 'meta-keyword': 'import include' }
      },
      {
        className: 'function',
        beginKeywords: 'function',
        end: /[{;]/,
        excludeEnd: true,
        illegal: /\S/,
        contains: [
          hljs.TITLE_MODE,
          {
            className: 'params',
            begin: /\(/,
            end: /\)/,
            contains: [
              hljs.APOS_STRING_MODE,
              hljs.QUOTE_STRING_MODE,
              hljs.C_LINE_COMMENT_MODE,
              hljs.C_BLOCK_COMMENT_MODE,
              AS3_REST_ARG_MODE
            ]
          },
          { begin: concat(/:\s*/, IDENT_FUNC_RETURN_TYPE_RE) }
        ]
      },
      hljs.METHOD_GUARD
    ],
    illegal: /#/
  };
}

module.exports = actionscript;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfYWN0aW9uc2NyaXB0LmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0EsV0FBVyxRQUFRO0FBQ25CLGFBQWE7QUFDYjs7QUFFQTtBQUNBLFdBQVcsa0JBQWtCO0FBQzdCLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBOztBQUVBO0FBQ0EsV0FBVyx1QkFBdUI7QUFDbEMsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQSxnQkFBZ0IsRUFBRTtBQUNsQjtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsZ0JBQWdCO0FBQ2hCO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLGdCQUFnQjtBQUNoQjtBQUNBO0FBQ0EsWUFBWSxxQ0FBcUM7QUFDakQ7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSxlQUFlO0FBQ2Ysb0JBQW9CO0FBQ3BCLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSxpQkFBaUI7QUFDakI7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsV0FBVztBQUNYLFlBQVk7QUFDWjtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9hY3Rpb25zY3JpcHQuanMiXSwic291cmNlc0NvbnRlbnQiOlsiLyoqXG4gKiBAcGFyYW0ge3N0cmluZ30gdmFsdWVcbiAqIEByZXR1cm5zIHtSZWdFeHB9XG4gKiAqL1xuXG4vKipcbiAqIEBwYXJhbSB7UmVnRXhwIHwgc3RyaW5nIH0gcmVcbiAqIEByZXR1cm5zIHtzdHJpbmd9XG4gKi9cbmZ1bmN0aW9uIHNvdXJjZShyZSkge1xuICBpZiAoIXJlKSByZXR1cm4gbnVsbDtcbiAgaWYgKHR5cGVvZiByZSA9PT0gXCJzdHJpbmdcIikgcmV0dXJuIHJlO1xuXG4gIHJldHVybiByZS5zb3VyY2U7XG59XG5cbi8qKlxuICogQHBhcmFtIHsuLi4oUmVnRXhwIHwgc3RyaW5nKSB9IGFyZ3NcbiAqIEByZXR1cm5zIHtzdHJpbmd9XG4gKi9cbmZ1bmN0aW9uIGNvbmNhdCguLi5hcmdzKSB7XG4gIGNvbnN0IGpvaW5lZCA9IGFyZ3MubWFwKCh4KSA9PiBzb3VyY2UoeCkpLmpvaW4oXCJcIik7XG4gIHJldHVybiBqb2luZWQ7XG59XG5cbi8qXG5MYW5ndWFnZTogQWN0aW9uU2NyaXB0XG5BdXRob3I6IEFsZXhhbmRlciBNeWFkemVsIDxteWFkemVsQGdtYWlsLmNvbT5cbkNhdGVnb3J5OiBzY3JpcHRpbmdcbkF1ZGl0OiAyMDIwXG4qL1xuXG4vKiogQHR5cGUgTGFuZ3VhZ2VGbiAqL1xuZnVuY3Rpb24gYWN0aW9uc2NyaXB0KGhsanMpIHtcbiAgY29uc3QgSURFTlRfUkUgPSAvW2EtekEtWl8kXVthLXpBLVowLTlfJF0qLztcbiAgY29uc3QgSURFTlRfRlVOQ19SRVRVUk5fVFlQRV9SRSA9IC8oWypdfFthLXpBLVpfJF1bYS16QS1aMC05XyRdKikvO1xuXG4gIGNvbnN0IEFTM19SRVNUX0FSR19NT0RFID0ge1xuICAgIGNsYXNzTmFtZTogJ3Jlc3RfYXJnJyxcbiAgICBiZWdpbjogL1suXXszfS8sXG4gICAgZW5kOiBJREVOVF9SRSxcbiAgICByZWxldmFuY2U6IDEwXG4gIH07XG5cbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnQWN0aW9uU2NyaXB0JyxcbiAgICBhbGlhc2VzOiBbICdhcycgXSxcbiAgICBrZXl3b3Jkczoge1xuICAgICAga2V5d29yZDogJ2FzIGJyZWFrIGNhc2UgY2F0Y2ggY2xhc3MgY29uc3QgY29udGludWUgZGVmYXVsdCBkZWxldGUgZG8gZHluYW1pYyBlYWNoICcgK1xuICAgICAgICAnZWxzZSBleHRlbmRzIGZpbmFsIGZpbmFsbHkgZm9yIGZ1bmN0aW9uIGdldCBpZiBpbXBsZW1lbnRzIGltcG9ydCBpbiBpbmNsdWRlICcgK1xuICAgICAgICAnaW5zdGFuY2VvZiBpbnRlcmZhY2UgaW50ZXJuYWwgaXMgbmFtZXNwYWNlIG5hdGl2ZSBuZXcgb3ZlcnJpZGUgcGFja2FnZSBwcml2YXRlICcgK1xuICAgICAgICAncHJvdGVjdGVkIHB1YmxpYyByZXR1cm4gc2V0IHN0YXRpYyBzdXBlciBzd2l0Y2ggdGhpcyB0aHJvdyB0cnkgdHlwZW9mIHVzZSB2YXIgdm9pZCAnICtcbiAgICAgICAgJ3doaWxlIHdpdGgnLFxuICAgICAgbGl0ZXJhbDogJ3RydWUgZmFsc2UgbnVsbCB1bmRlZmluZWQnXG4gICAgfSxcbiAgICBjb250YWluczogW1xuICAgICAgaGxqcy5BUE9TX1NUUklOR19NT0RFLFxuICAgICAgaGxqcy5RVU9URV9TVFJJTkdfTU9ERSxcbiAgICAgIGhsanMuQ19MSU5FX0NPTU1FTlRfTU9ERSxcbiAgICAgIGhsanMuQ19CTE9DS19DT01NRU5UX01PREUsXG4gICAgICBobGpzLkNfTlVNQkVSX01PREUsXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ2NsYXNzJyxcbiAgICAgICAgYmVnaW5LZXl3b3JkczogJ3BhY2thZ2UnLFxuICAgICAgICBlbmQ6IC9cXHsvLFxuICAgICAgICBjb250YWluczogWyBobGpzLlRJVExFX01PREUgXVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnY2xhc3MnLFxuICAgICAgICBiZWdpbktleXdvcmRzOiAnY2xhc3MgaW50ZXJmYWNlJyxcbiAgICAgICAgZW5kOiAvXFx7LyxcbiAgICAgICAgZXhjbHVkZUVuZDogdHJ1ZSxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICB7IGJlZ2luS2V5d29yZHM6ICdleHRlbmRzIGltcGxlbWVudHMnIH0sXG4gICAgICAgICAgaGxqcy5USVRMRV9NT0RFXG4gICAgICAgIF1cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ21ldGEnLFxuICAgICAgICBiZWdpbktleXdvcmRzOiAnaW1wb3J0IGluY2x1ZGUnLFxuICAgICAgICBlbmQ6IC87LyxcbiAgICAgICAga2V5d29yZHM6IHsgJ21ldGEta2V5d29yZCc6ICdpbXBvcnQgaW5jbHVkZScgfVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnZnVuY3Rpb24nLFxuICAgICAgICBiZWdpbktleXdvcmRzOiAnZnVuY3Rpb24nLFxuICAgICAgICBlbmQ6IC9beztdLyxcbiAgICAgICAgZXhjbHVkZUVuZDogdHJ1ZSxcbiAgICAgICAgaWxsZWdhbDogL1xcUy8sXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgaGxqcy5USVRMRV9NT0RFLFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGNsYXNzTmFtZTogJ3BhcmFtcycsXG4gICAgICAgICAgICBiZWdpbjogL1xcKC8sXG4gICAgICAgICAgICBlbmQ6IC9cXCkvLFxuICAgICAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICAgICAgaGxqcy5BUE9TX1NUUklOR19NT0RFLFxuICAgICAgICAgICAgICBobGpzLlFVT1RFX1NUUklOR19NT0RFLFxuICAgICAgICAgICAgICBobGpzLkNfTElORV9DT01NRU5UX01PREUsXG4gICAgICAgICAgICAgIGhsanMuQ19CTE9DS19DT01NRU5UX01PREUsXG4gICAgICAgICAgICAgIEFTM19SRVNUX0FSR19NT0RFXG4gICAgICAgICAgICBdXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7IGJlZ2luOiBjb25jYXQoLzpcXHMqLywgSURFTlRfRlVOQ19SRVRVUk5fVFlQRV9SRSkgfVxuICAgICAgICBdXG4gICAgICB9LFxuICAgICAgaGxqcy5NRVRIT0RfR1VBUkRcbiAgICBdLFxuICAgIGlsbGVnYWw6IC8jL1xuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IGFjdGlvbnNjcmlwdDtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==