(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_pony"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/pony.js":
/*!***********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/pony.js ***!
  \***********************************************************************************************/
/***/ ((module) => {

/*
Language: Pony
Author: Joe Eli McIlvain <joe.eli.mac@gmail.com>
Description: Pony is an open-source, object-oriented, actor-model,
             capabilities-secure, high performance programming language.
Website: https://www.ponylang.io
*/

function pony(hljs) {
  const KEYWORDS = {
    keyword:
      'actor addressof and as be break class compile_error compile_intrinsic ' +
      'consume continue delegate digestof do else elseif embed end error ' +
      'for fun if ifdef in interface is isnt lambda let match new not object ' +
      'or primitive recover repeat return struct then trait try type until ' +
      'use var where while with xor',
    meta:
      'iso val tag trn box ref',
    literal:
      'this false true'
  };

  const TRIPLE_QUOTE_STRING_MODE = {
    className: 'string',
    begin: '"""',
    end: '"""',
    relevance: 10
  };

  const QUOTE_STRING_MODE = {
    className: 'string',
    begin: '"',
    end: '"',
    contains: [ hljs.BACKSLASH_ESCAPE ]
  };

  const SINGLE_QUOTE_CHAR_MODE = {
    className: 'string',
    begin: '\'',
    end: '\'',
    contains: [ hljs.BACKSLASH_ESCAPE ],
    relevance: 0
  };

  const TYPE_NAME = {
    className: 'type',
    begin: '\\b_?[A-Z][\\w]*',
    relevance: 0
  };

  const PRIMED_NAME = {
    begin: hljs.IDENT_RE + '\'',
    relevance: 0
  };

  const NUMBER_MODE = {
    className: 'number',
    begin: '(-?)(\\b0[xX][a-fA-F0-9]+|\\b0[bB][01]+|(\\b\\d+(_\\d+)?(\\.\\d*)?|\\.\\d+)([eE][-+]?\\d+)?)',
    relevance: 0
  };

  /**
   * The `FUNCTION` and `CLASS` modes were intentionally removed to simplify
   * highlighting and fix cases like
   * ```
   * interface Iterator[A: A]
   *   fun has_next(): Bool
   *   fun next(): A?
   * ```
   * where it is valid to have a function head without a body
   */

  return {
    name: 'Pony',
    keywords: KEYWORDS,
    contains: [
      TYPE_NAME,
      TRIPLE_QUOTE_STRING_MODE,
      QUOTE_STRING_MODE,
      SINGLE_QUOTE_CHAR_MODE,
      PRIMED_NAME,
      NUMBER_MODE,
      hljs.C_LINE_COMMENT_MODE,
      hljs.C_BLOCK_COMMENT_MODE
    ]
  };
}

module.exports = pony;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfcG9ueS5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL3BvbnkuanMiXSwic291cmNlc0NvbnRlbnQiOlsiLypcbkxhbmd1YWdlOiBQb255XG5BdXRob3I6IEpvZSBFbGkgTWNJbHZhaW4gPGpvZS5lbGkubWFjQGdtYWlsLmNvbT5cbkRlc2NyaXB0aW9uOiBQb255IGlzIGFuIG9wZW4tc291cmNlLCBvYmplY3Qtb3JpZW50ZWQsIGFjdG9yLW1vZGVsLFxuICAgICAgICAgICAgIGNhcGFiaWxpdGllcy1zZWN1cmUsIGhpZ2ggcGVyZm9ybWFuY2UgcHJvZ3JhbW1pbmcgbGFuZ3VhZ2UuXG5XZWJzaXRlOiBodHRwczovL3d3dy5wb255bGFuZy5pb1xuKi9cblxuZnVuY3Rpb24gcG9ueShobGpzKSB7XG4gIGNvbnN0IEtFWVdPUkRTID0ge1xuICAgIGtleXdvcmQ6XG4gICAgICAnYWN0b3IgYWRkcmVzc29mIGFuZCBhcyBiZSBicmVhayBjbGFzcyBjb21waWxlX2Vycm9yIGNvbXBpbGVfaW50cmluc2ljICcgK1xuICAgICAgJ2NvbnN1bWUgY29udGludWUgZGVsZWdhdGUgZGlnZXN0b2YgZG8gZWxzZSBlbHNlaWYgZW1iZWQgZW5kIGVycm9yICcgK1xuICAgICAgJ2ZvciBmdW4gaWYgaWZkZWYgaW4gaW50ZXJmYWNlIGlzIGlzbnQgbGFtYmRhIGxldCBtYXRjaCBuZXcgbm90IG9iamVjdCAnICtcbiAgICAgICdvciBwcmltaXRpdmUgcmVjb3ZlciByZXBlYXQgcmV0dXJuIHN0cnVjdCB0aGVuIHRyYWl0IHRyeSB0eXBlIHVudGlsICcgK1xuICAgICAgJ3VzZSB2YXIgd2hlcmUgd2hpbGUgd2l0aCB4b3InLFxuICAgIG1ldGE6XG4gICAgICAnaXNvIHZhbCB0YWcgdHJuIGJveCByZWYnLFxuICAgIGxpdGVyYWw6XG4gICAgICAndGhpcyBmYWxzZSB0cnVlJ1xuICB9O1xuXG4gIGNvbnN0IFRSSVBMRV9RVU9URV9TVFJJTkdfTU9ERSA9IHtcbiAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgIGJlZ2luOiAnXCJcIlwiJyxcbiAgICBlbmQ6ICdcIlwiXCInLFxuICAgIHJlbGV2YW5jZTogMTBcbiAgfTtcblxuICBjb25zdCBRVU9URV9TVFJJTkdfTU9ERSA9IHtcbiAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgIGJlZ2luOiAnXCInLFxuICAgIGVuZDogJ1wiJyxcbiAgICBjb250YWluczogWyBobGpzLkJBQ0tTTEFTSF9FU0NBUEUgXVxuICB9O1xuXG4gIGNvbnN0IFNJTkdMRV9RVU9URV9DSEFSX01PREUgPSB7XG4gICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICBiZWdpbjogJ1xcJycsXG4gICAgZW5kOiAnXFwnJyxcbiAgICBjb250YWluczogWyBobGpzLkJBQ0tTTEFTSF9FU0NBUEUgXSxcbiAgICByZWxldmFuY2U6IDBcbiAgfTtcblxuICBjb25zdCBUWVBFX05BTUUgPSB7XG4gICAgY2xhc3NOYW1lOiAndHlwZScsXG4gICAgYmVnaW46ICdcXFxcYl8/W0EtWl1bXFxcXHddKicsXG4gICAgcmVsZXZhbmNlOiAwXG4gIH07XG5cbiAgY29uc3QgUFJJTUVEX05BTUUgPSB7XG4gICAgYmVnaW46IGhsanMuSURFTlRfUkUgKyAnXFwnJyxcbiAgICByZWxldmFuY2U6IDBcbiAgfTtcblxuICBjb25zdCBOVU1CRVJfTU9ERSA9IHtcbiAgICBjbGFzc05hbWU6ICdudW1iZXInLFxuICAgIGJlZ2luOiAnKC0/KShcXFxcYjBbeFhdW2EtZkEtRjAtOV0rfFxcXFxiMFtiQl1bMDFdK3woXFxcXGJcXFxcZCsoX1xcXFxkKyk/KFxcXFwuXFxcXGQqKT98XFxcXC5cXFxcZCspKFtlRV1bLStdP1xcXFxkKyk/KScsXG4gICAgcmVsZXZhbmNlOiAwXG4gIH07XG5cbiAgLyoqXG4gICAqIFRoZSBgRlVOQ1RJT05gIGFuZCBgQ0xBU1NgIG1vZGVzIHdlcmUgaW50ZW50aW9uYWxseSByZW1vdmVkIHRvIHNpbXBsaWZ5XG4gICAqIGhpZ2hsaWdodGluZyBhbmQgZml4IGNhc2VzIGxpa2VcbiAgICogYGBgXG4gICAqIGludGVyZmFjZSBJdGVyYXRvcltBOiBBXVxuICAgKiAgIGZ1biBoYXNfbmV4dCgpOiBCb29sXG4gICAqICAgZnVuIG5leHQoKTogQT9cbiAgICogYGBgXG4gICAqIHdoZXJlIGl0IGlzIHZhbGlkIHRvIGhhdmUgYSBmdW5jdGlvbiBoZWFkIHdpdGhvdXQgYSBib2R5XG4gICAqL1xuXG4gIHJldHVybiB7XG4gICAgbmFtZTogJ1BvbnknLFxuICAgIGtleXdvcmRzOiBLRVlXT1JEUyxcbiAgICBjb250YWluczogW1xuICAgICAgVFlQRV9OQU1FLFxuICAgICAgVFJJUExFX1FVT1RFX1NUUklOR19NT0RFLFxuICAgICAgUVVPVEVfU1RSSU5HX01PREUsXG4gICAgICBTSU5HTEVfUVVPVEVfQ0hBUl9NT0RFLFxuICAgICAgUFJJTUVEX05BTUUsXG4gICAgICBOVU1CRVJfTU9ERSxcbiAgICAgIGhsanMuQ19MSU5FX0NPTU1FTlRfTU9ERSxcbiAgICAgIGhsanMuQ19CTE9DS19DT01NRU5UX01PREVcbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gcG9ueTtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==