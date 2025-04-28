(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_step21"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/step21.js":
/*!*************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/step21.js ***!
  \*************************************************************************************************/
/***/ ((module) => {

/*
Language: STEP Part 21
Contributors: Adam Joseph Cook <adam.joseph.cook@gmail.com>
Description: Syntax highlighter for STEP Part 21 files (ISO 10303-21).
Website: https://en.wikipedia.org/wiki/ISO_10303-21
*/

function step21(hljs) {
  const STEP21_IDENT_RE = '[A-Z_][A-Z0-9_.]*';
  const STEP21_KEYWORDS = {
    $pattern: STEP21_IDENT_RE,
    keyword: 'HEADER ENDSEC DATA'
  };
  const STEP21_START = {
    className: 'meta',
    begin: 'ISO-10303-21;',
    relevance: 10
  };
  const STEP21_CLOSE = {
    className: 'meta',
    begin: 'END-ISO-10303-21;',
    relevance: 10
  };

  return {
    name: 'STEP Part 21',
    aliases: [
      'p21',
      'step',
      'stp'
    ],
    case_insensitive: true, // STEP 21 is case insensitive in theory, in practice all non-comments are capitalized.
    keywords: STEP21_KEYWORDS,
    contains: [
      STEP21_START,
      STEP21_CLOSE,
      hljs.C_LINE_COMMENT_MODE,
      hljs.C_BLOCK_COMMENT_MODE,
      hljs.COMMENT('/\\*\\*!', '\\*/'),
      hljs.C_NUMBER_MODE,
      hljs.inherit(hljs.APOS_STRING_MODE, {
        illegal: null
      }),
      hljs.inherit(hljs.QUOTE_STRING_MODE, {
        illegal: null
      }),
      {
        className: 'string',
        begin: "'",
        end: "'"
      },
      {
        className: 'symbol',
        variants: [
          {
            begin: '#',
            end: '\\d+',
            illegal: '\\W'
          }
        ]
      }
    ]
  };
}

module.exports = step21;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfc3RlcDIxLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EseUJBQXlCO0FBQ3pCO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsNkJBQTZCO0FBQzdCO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL3N0ZXAyMS5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKlxuTGFuZ3VhZ2U6IFNURVAgUGFydCAyMVxuQ29udHJpYnV0b3JzOiBBZGFtIEpvc2VwaCBDb29rIDxhZGFtLmpvc2VwaC5jb29rQGdtYWlsLmNvbT5cbkRlc2NyaXB0aW9uOiBTeW50YXggaGlnaGxpZ2h0ZXIgZm9yIFNURVAgUGFydCAyMSBmaWxlcyAoSVNPIDEwMzAzLTIxKS5cbldlYnNpdGU6IGh0dHBzOi8vZW4ud2lraXBlZGlhLm9yZy93aWtpL0lTT18xMDMwMy0yMVxuKi9cblxuZnVuY3Rpb24gc3RlcDIxKGhsanMpIHtcbiAgY29uc3QgU1RFUDIxX0lERU5UX1JFID0gJ1tBLVpfXVtBLVowLTlfLl0qJztcbiAgY29uc3QgU1RFUDIxX0tFWVdPUkRTID0ge1xuICAgICRwYXR0ZXJuOiBTVEVQMjFfSURFTlRfUkUsXG4gICAga2V5d29yZDogJ0hFQURFUiBFTkRTRUMgREFUQSdcbiAgfTtcbiAgY29uc3QgU1RFUDIxX1NUQVJUID0ge1xuICAgIGNsYXNzTmFtZTogJ21ldGEnLFxuICAgIGJlZ2luOiAnSVNPLTEwMzAzLTIxOycsXG4gICAgcmVsZXZhbmNlOiAxMFxuICB9O1xuICBjb25zdCBTVEVQMjFfQ0xPU0UgPSB7XG4gICAgY2xhc3NOYW1lOiAnbWV0YScsXG4gICAgYmVnaW46ICdFTkQtSVNPLTEwMzAzLTIxOycsXG4gICAgcmVsZXZhbmNlOiAxMFxuICB9O1xuXG4gIHJldHVybiB7XG4gICAgbmFtZTogJ1NURVAgUGFydCAyMScsXG4gICAgYWxpYXNlczogW1xuICAgICAgJ3AyMScsXG4gICAgICAnc3RlcCcsXG4gICAgICAnc3RwJ1xuICAgIF0sXG4gICAgY2FzZV9pbnNlbnNpdGl2ZTogdHJ1ZSwgLy8gU1RFUCAyMSBpcyBjYXNlIGluc2Vuc2l0aXZlIGluIHRoZW9yeSwgaW4gcHJhY3RpY2UgYWxsIG5vbi1jb21tZW50cyBhcmUgY2FwaXRhbGl6ZWQuXG4gICAga2V5d29yZHM6IFNURVAyMV9LRVlXT1JEUyxcbiAgICBjb250YWluczogW1xuICAgICAgU1RFUDIxX1NUQVJULFxuICAgICAgU1RFUDIxX0NMT1NFLFxuICAgICAgaGxqcy5DX0xJTkVfQ09NTUVOVF9NT0RFLFxuICAgICAgaGxqcy5DX0JMT0NLX0NPTU1FTlRfTU9ERSxcbiAgICAgIGhsanMuQ09NTUVOVCgnL1xcXFwqXFxcXCohJywgJ1xcXFwqLycpLFxuICAgICAgaGxqcy5DX05VTUJFUl9NT0RFLFxuICAgICAgaGxqcy5pbmhlcml0KGhsanMuQVBPU19TVFJJTkdfTU9ERSwge1xuICAgICAgICBpbGxlZ2FsOiBudWxsXG4gICAgICB9KSxcbiAgICAgIGhsanMuaW5oZXJpdChobGpzLlFVT1RFX1NUUklOR19NT0RFLCB7XG4gICAgICAgIGlsbGVnYWw6IG51bGxcbiAgICAgIH0pLFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgICAgICBiZWdpbjogXCInXCIsXG4gICAgICAgIGVuZDogXCInXCJcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3N5bWJvbCcsXG4gICAgICAgIHZhcmlhbnRzOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgYmVnaW46ICcjJyxcbiAgICAgICAgICAgIGVuZDogJ1xcXFxkKycsXG4gICAgICAgICAgICBpbGxlZ2FsOiAnXFxcXFcnXG4gICAgICAgICAgfVxuICAgICAgICBdXG4gICAgICB9XG4gICAgXVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IHN0ZXAyMTtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==