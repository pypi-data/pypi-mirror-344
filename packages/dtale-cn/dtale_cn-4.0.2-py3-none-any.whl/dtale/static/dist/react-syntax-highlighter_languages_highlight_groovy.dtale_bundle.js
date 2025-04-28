(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_groovy"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/groovy.js":
/*!*************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/groovy.js ***!
  \*************************************************************************************************/
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
 * @param {RegExp | string } re
 * @returns {string}
 */
function lookahead(re) {
  return concat('(?=', re, ')');
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
 Language: Groovy
 Author: Guillaume Laforge <glaforge@gmail.com>
 Description: Groovy programming language implementation inspired from Vsevolod's Java mode
 Website: https://groovy-lang.org
 */

function variants(variants, obj = {}) {
  obj.variants = variants;
  return obj;
}

function groovy(hljs) {
  const IDENT_RE = '[A-Za-z0-9_$]+';
  const COMMENT = variants([
    hljs.C_LINE_COMMENT_MODE,
    hljs.C_BLOCK_COMMENT_MODE,
    hljs.COMMENT(
      '/\\*\\*',
      '\\*/',
      {
        relevance: 0,
        contains: [
          {
            // eat up @'s in emails to prevent them to be recognized as doctags
            begin: /\w+@/,
            relevance: 0
          },
          {
            className: 'doctag',
            begin: '@[A-Za-z]+'
          }
        ]
      }
    )
  ]);
  const REGEXP = {
    className: 'regexp',
    begin: /~?\/[^\/\n]+\//,
    contains: [ hljs.BACKSLASH_ESCAPE ]
  };
  const NUMBER = variants([
    hljs.BINARY_NUMBER_MODE,
    hljs.C_NUMBER_MODE
  ]);
  const STRING = variants([
    {
      begin: /"""/,
      end: /"""/
    },
    {
      begin: /'''/,
      end: /'''/
    },
    {
      begin: "\\$/",
      end: "/\\$",
      relevance: 10
    },
    hljs.APOS_STRING_MODE,
    hljs.QUOTE_STRING_MODE
  ],
  {
    className: "string"
  }
  );

  return {
    name: 'Groovy',
    keywords: {
      built_in: 'this super',
      literal: 'true false null',
      keyword:
            'byte short char int long boolean float double void ' +
            // groovy specific keywords
            'def as in assert trait ' +
            // common keywords with Java
            'abstract static volatile transient public private protected synchronized final ' +
            'class interface enum if else for while switch case break default continue ' +
            'throw throws try catch finally implements extends new import package return instanceof'
    },
    contains: [
      hljs.SHEBANG({
        binary: "groovy",
        relevance: 10
      }),
      COMMENT,
      STRING,
      REGEXP,
      NUMBER,
      {
        className: 'class',
        beginKeywords: 'class interface trait enum',
        end: /\{/,
        illegal: ':',
        contains: [
          {
            beginKeywords: 'extends implements'
          },
          hljs.UNDERSCORE_TITLE_MODE
        ]
      },
      {
        className: 'meta',
        begin: '@[A-Za-z]+',
        relevance: 0
      },
      {
        // highlight map keys and named parameters as attrs
        className: 'attr',
        begin: IDENT_RE + '[ \t]*:',
        relevance: 0
      },
      {
        // catch middle element of the ternary operator
        // to avoid highlight it as a label, named parameter, or map key
        begin: /\?/,
        end: /:/,
        relevance: 0,
        contains: [
          COMMENT,
          STRING,
          REGEXP,
          NUMBER,
          'self'
        ]
      },
      {
        // highlight labeled statements
        className: 'symbol',
        begin: '^[ \t]*' + lookahead(IDENT_RE + ':'),
        excludeBegin: true,
        end: IDENT_RE + ':',
        relevance: 0
      }
    ],
    illegal: /#|<\//
  };
}

module.exports = groovy;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfZ3Jvb3Z5LmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0EsV0FBVyxRQUFRO0FBQ25CLGFBQWE7QUFDYjs7QUFFQTtBQUNBLFdBQVcsa0JBQWtCO0FBQzdCLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBOztBQUVBO0FBQ0EsV0FBVyxrQkFBa0I7QUFDN0IsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0EsV0FBVyx1QkFBdUI7QUFDbEMsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBLG9DQUFvQztBQUNwQztBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsV0FBVztBQUNYO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxnQkFBZ0I7QUFDaEI7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvZ3Jvb3Z5LmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qKlxuICogQHBhcmFtIHtzdHJpbmd9IHZhbHVlXG4gKiBAcmV0dXJucyB7UmVnRXhwfVxuICogKi9cblxuLyoqXG4gKiBAcGFyYW0ge1JlZ0V4cCB8IHN0cmluZyB9IHJlXG4gKiBAcmV0dXJucyB7c3RyaW5nfVxuICovXG5mdW5jdGlvbiBzb3VyY2UocmUpIHtcbiAgaWYgKCFyZSkgcmV0dXJuIG51bGw7XG4gIGlmICh0eXBlb2YgcmUgPT09IFwic3RyaW5nXCIpIHJldHVybiByZTtcblxuICByZXR1cm4gcmUuc291cmNlO1xufVxuXG4vKipcbiAqIEBwYXJhbSB7UmVnRXhwIHwgc3RyaW5nIH0gcmVcbiAqIEByZXR1cm5zIHtzdHJpbmd9XG4gKi9cbmZ1bmN0aW9uIGxvb2thaGVhZChyZSkge1xuICByZXR1cm4gY29uY2F0KCcoPz0nLCByZSwgJyknKTtcbn1cblxuLyoqXG4gKiBAcGFyYW0gey4uLihSZWdFeHAgfCBzdHJpbmcpIH0gYXJnc1xuICogQHJldHVybnMge3N0cmluZ31cbiAqL1xuZnVuY3Rpb24gY29uY2F0KC4uLmFyZ3MpIHtcbiAgY29uc3Qgam9pbmVkID0gYXJncy5tYXAoKHgpID0+IHNvdXJjZSh4KSkuam9pbihcIlwiKTtcbiAgcmV0dXJuIGpvaW5lZDtcbn1cblxuLypcbiBMYW5ndWFnZTogR3Jvb3Z5XG4gQXV0aG9yOiBHdWlsbGF1bWUgTGFmb3JnZSA8Z2xhZm9yZ2VAZ21haWwuY29tPlxuIERlc2NyaXB0aW9uOiBHcm9vdnkgcHJvZ3JhbW1pbmcgbGFuZ3VhZ2UgaW1wbGVtZW50YXRpb24gaW5zcGlyZWQgZnJvbSBWc2V2b2xvZCdzIEphdmEgbW9kZVxuIFdlYnNpdGU6IGh0dHBzOi8vZ3Jvb3Z5LWxhbmcub3JnXG4gKi9cblxuZnVuY3Rpb24gdmFyaWFudHModmFyaWFudHMsIG9iaiA9IHt9KSB7XG4gIG9iai52YXJpYW50cyA9IHZhcmlhbnRzO1xuICByZXR1cm4gb2JqO1xufVxuXG5mdW5jdGlvbiBncm9vdnkoaGxqcykge1xuICBjb25zdCBJREVOVF9SRSA9ICdbQS1aYS16MC05XyRdKyc7XG4gIGNvbnN0IENPTU1FTlQgPSB2YXJpYW50cyhbXG4gICAgaGxqcy5DX0xJTkVfQ09NTUVOVF9NT0RFLFxuICAgIGhsanMuQ19CTE9DS19DT01NRU5UX01PREUsXG4gICAgaGxqcy5DT01NRU5UKFxuICAgICAgJy9cXFxcKlxcXFwqJyxcbiAgICAgICdcXFxcKi8nLFxuICAgICAge1xuICAgICAgICByZWxldmFuY2U6IDAsXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgLy8gZWF0IHVwIEAncyBpbiBlbWFpbHMgdG8gcHJldmVudCB0aGVtIHRvIGJlIHJlY29nbml6ZWQgYXMgZG9jdGFnc1xuICAgICAgICAgICAgYmVnaW46IC9cXHcrQC8sXG4gICAgICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGNsYXNzTmFtZTogJ2RvY3RhZycsXG4gICAgICAgICAgICBiZWdpbjogJ0BbQS1aYS16XSsnXG4gICAgICAgICAgfVxuICAgICAgICBdXG4gICAgICB9XG4gICAgKVxuICBdKTtcbiAgY29uc3QgUkVHRVhQID0ge1xuICAgIGNsYXNzTmFtZTogJ3JlZ2V4cCcsXG4gICAgYmVnaW46IC9+P1xcL1teXFwvXFxuXStcXC8vLFxuICAgIGNvbnRhaW5zOiBbIGhsanMuQkFDS1NMQVNIX0VTQ0FQRSBdXG4gIH07XG4gIGNvbnN0IE5VTUJFUiA9IHZhcmlhbnRzKFtcbiAgICBobGpzLkJJTkFSWV9OVU1CRVJfTU9ERSxcbiAgICBobGpzLkNfTlVNQkVSX01PREVcbiAgXSk7XG4gIGNvbnN0IFNUUklORyA9IHZhcmlhbnRzKFtcbiAgICB7XG4gICAgICBiZWdpbjogL1wiXCJcIi8sXG4gICAgICBlbmQ6IC9cIlwiXCIvXG4gICAgfSxcbiAgICB7XG4gICAgICBiZWdpbjogLycnJy8sXG4gICAgICBlbmQ6IC8nJycvXG4gICAgfSxcbiAgICB7XG4gICAgICBiZWdpbjogXCJcXFxcJC9cIixcbiAgICAgIGVuZDogXCIvXFxcXCRcIixcbiAgICAgIHJlbGV2YW5jZTogMTBcbiAgICB9LFxuICAgIGhsanMuQVBPU19TVFJJTkdfTU9ERSxcbiAgICBobGpzLlFVT1RFX1NUUklOR19NT0RFXG4gIF0sXG4gIHtcbiAgICBjbGFzc05hbWU6IFwic3RyaW5nXCJcbiAgfVxuICApO1xuXG4gIHJldHVybiB7XG4gICAgbmFtZTogJ0dyb292eScsXG4gICAga2V5d29yZHM6IHtcbiAgICAgIGJ1aWx0X2luOiAndGhpcyBzdXBlcicsXG4gICAgICBsaXRlcmFsOiAndHJ1ZSBmYWxzZSBudWxsJyxcbiAgICAgIGtleXdvcmQ6XG4gICAgICAgICAgICAnYnl0ZSBzaG9ydCBjaGFyIGludCBsb25nIGJvb2xlYW4gZmxvYXQgZG91YmxlIHZvaWQgJyArXG4gICAgICAgICAgICAvLyBncm9vdnkgc3BlY2lmaWMga2V5d29yZHNcbiAgICAgICAgICAgICdkZWYgYXMgaW4gYXNzZXJ0IHRyYWl0ICcgK1xuICAgICAgICAgICAgLy8gY29tbW9uIGtleXdvcmRzIHdpdGggSmF2YVxuICAgICAgICAgICAgJ2Fic3RyYWN0IHN0YXRpYyB2b2xhdGlsZSB0cmFuc2llbnQgcHVibGljIHByaXZhdGUgcHJvdGVjdGVkIHN5bmNocm9uaXplZCBmaW5hbCAnICtcbiAgICAgICAgICAgICdjbGFzcyBpbnRlcmZhY2UgZW51bSBpZiBlbHNlIGZvciB3aGlsZSBzd2l0Y2ggY2FzZSBicmVhayBkZWZhdWx0IGNvbnRpbnVlICcgK1xuICAgICAgICAgICAgJ3Rocm93IHRocm93cyB0cnkgY2F0Y2ggZmluYWxseSBpbXBsZW1lbnRzIGV4dGVuZHMgbmV3IGltcG9ydCBwYWNrYWdlIHJldHVybiBpbnN0YW5jZW9mJ1xuICAgIH0sXG4gICAgY29udGFpbnM6IFtcbiAgICAgIGhsanMuU0hFQkFORyh7XG4gICAgICAgIGJpbmFyeTogXCJncm9vdnlcIixcbiAgICAgICAgcmVsZXZhbmNlOiAxMFxuICAgICAgfSksXG4gICAgICBDT01NRU5ULFxuICAgICAgU1RSSU5HLFxuICAgICAgUkVHRVhQLFxuICAgICAgTlVNQkVSLFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdjbGFzcycsXG4gICAgICAgIGJlZ2luS2V5d29yZHM6ICdjbGFzcyBpbnRlcmZhY2UgdHJhaXQgZW51bScsXG4gICAgICAgIGVuZDogL1xcey8sXG4gICAgICAgIGlsbGVnYWw6ICc6JyxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbktleXdvcmRzOiAnZXh0ZW5kcyBpbXBsZW1lbnRzJ1xuICAgICAgICAgIH0sXG4gICAgICAgICAgaGxqcy5VTkRFUlNDT1JFX1RJVExFX01PREVcbiAgICAgICAgXVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnbWV0YScsXG4gICAgICAgIGJlZ2luOiAnQFtBLVphLXpdKycsXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgLy8gaGlnaGxpZ2h0IG1hcCBrZXlzIGFuZCBuYW1lZCBwYXJhbWV0ZXJzIGFzIGF0dHJzXG4gICAgICAgIGNsYXNzTmFtZTogJ2F0dHInLFxuICAgICAgICBiZWdpbjogSURFTlRfUkUgKyAnWyBcXHRdKjonLFxuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIC8vIGNhdGNoIG1pZGRsZSBlbGVtZW50IG9mIHRoZSB0ZXJuYXJ5IG9wZXJhdG9yXG4gICAgICAgIC8vIHRvIGF2b2lkIGhpZ2hsaWdodCBpdCBhcyBhIGxhYmVsLCBuYW1lZCBwYXJhbWV0ZXIsIG9yIG1hcCBrZXlcbiAgICAgICAgYmVnaW46IC9cXD8vLFxuICAgICAgICBlbmQ6IC86LyxcbiAgICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIENPTU1FTlQsXG4gICAgICAgICAgU1RSSU5HLFxuICAgICAgICAgIFJFR0VYUCxcbiAgICAgICAgICBOVU1CRVIsXG4gICAgICAgICAgJ3NlbGYnXG4gICAgICAgIF1cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIC8vIGhpZ2hsaWdodCBsYWJlbGVkIHN0YXRlbWVudHNcbiAgICAgICAgY2xhc3NOYW1lOiAnc3ltYm9sJyxcbiAgICAgICAgYmVnaW46ICdeWyBcXHRdKicgKyBsb29rYWhlYWQoSURFTlRfUkUgKyAnOicpLFxuICAgICAgICBleGNsdWRlQmVnaW46IHRydWUsXG4gICAgICAgIGVuZDogSURFTlRfUkUgKyAnOicsXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfVxuICAgIF0sXG4gICAgaWxsZWdhbDogLyN8PFxcLy9cbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBncm9vdnk7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=