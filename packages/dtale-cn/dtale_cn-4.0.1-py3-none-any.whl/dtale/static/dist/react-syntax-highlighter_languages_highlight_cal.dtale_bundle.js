(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_cal"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/cal.js":
/*!**********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/cal.js ***!
  \**********************************************************************************************/
/***/ ((module) => {

/*
Language: C/AL
Author: Kenneth Fuglsang Christensen <kfuglsang@gmail.com>
Description: Provides highlighting of Microsoft Dynamics NAV C/AL code files
Website: https://docs.microsoft.com/en-us/dynamics-nav/programming-in-c-al
*/

/** @type LanguageFn */
function cal(hljs) {
  const KEYWORDS =
    'div mod in and or not xor asserterror begin case do downto else end exit for if of repeat then to ' +
    'until while with var';
  const LITERALS = 'false true';
  const COMMENT_MODES = [
    hljs.C_LINE_COMMENT_MODE,
    hljs.COMMENT(
      /\{/,
      /\}/,
      {
        relevance: 0
      }
    ),
    hljs.COMMENT(
      /\(\*/,
      /\*\)/,
      {
        relevance: 10
      }
    )
  ];
  const STRING = {
    className: 'string',
    begin: /'/,
    end: /'/,
    contains: [{
      begin: /''/
    }]
  };
  const CHAR_STRING = {
    className: 'string',
    begin: /(#\d+)+/
  };
  const DATE = {
    className: 'number',
    begin: '\\b\\d+(\\.\\d+)?(DT|D|T)',
    relevance: 0
  };
  const DBL_QUOTED_VARIABLE = {
    className: 'string', // not a string technically but makes sense to be highlighted in the same style
    begin: '"',
    end: '"'
  };

  const PROCEDURE = {
    className: 'function',
    beginKeywords: 'procedure',
    end: /[:;]/,
    keywords: 'procedure|10',
    contains: [
      hljs.TITLE_MODE,
      {
        className: 'params',
        begin: /\(/,
        end: /\)/,
        keywords: KEYWORDS,
        contains: [
          STRING,
          CHAR_STRING
        ]
      }
    ].concat(COMMENT_MODES)
  };

  const OBJECT = {
    className: 'class',
    begin: 'OBJECT (Table|Form|Report|Dataport|Codeunit|XMLport|MenuSuite|Page|Query) (\\d+) ([^\\r\\n]+)',
    returnBegin: true,
    contains: [
      hljs.TITLE_MODE,
      PROCEDURE
    ]
  };

  return {
    name: 'C/AL',
    case_insensitive: true,
    keywords: {
      keyword: KEYWORDS,
      literal: LITERALS
    },
    illegal: /\/\*/,
    contains: [
      STRING,
      CHAR_STRING,
      DATE,
      DBL_QUOTED_VARIABLE,
      hljs.NUMBER_MODE,
      OBJECT,
      PROCEDURE
    ]
  };
}

module.exports = cal;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfY2FsLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxTQUFTO0FBQ1QsU0FBUztBQUNUO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0EsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvY2FsLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogQy9BTFxuQXV0aG9yOiBLZW5uZXRoIEZ1Z2xzYW5nIENocmlzdGVuc2VuIDxrZnVnbHNhbmdAZ21haWwuY29tPlxuRGVzY3JpcHRpb246IFByb3ZpZGVzIGhpZ2hsaWdodGluZyBvZiBNaWNyb3NvZnQgRHluYW1pY3MgTkFWIEMvQUwgY29kZSBmaWxlc1xuV2Vic2l0ZTogaHR0cHM6Ly9kb2NzLm1pY3Jvc29mdC5jb20vZW4tdXMvZHluYW1pY3MtbmF2L3Byb2dyYW1taW5nLWluLWMtYWxcbiovXG5cbi8qKiBAdHlwZSBMYW5ndWFnZUZuICovXG5mdW5jdGlvbiBjYWwoaGxqcykge1xuICBjb25zdCBLRVlXT1JEUyA9XG4gICAgJ2RpdiBtb2QgaW4gYW5kIG9yIG5vdCB4b3IgYXNzZXJ0ZXJyb3IgYmVnaW4gY2FzZSBkbyBkb3dudG8gZWxzZSBlbmQgZXhpdCBmb3IgaWYgb2YgcmVwZWF0IHRoZW4gdG8gJyArXG4gICAgJ3VudGlsIHdoaWxlIHdpdGggdmFyJztcbiAgY29uc3QgTElURVJBTFMgPSAnZmFsc2UgdHJ1ZSc7XG4gIGNvbnN0IENPTU1FTlRfTU9ERVMgPSBbXG4gICAgaGxqcy5DX0xJTkVfQ09NTUVOVF9NT0RFLFxuICAgIGhsanMuQ09NTUVOVChcbiAgICAgIC9cXHsvLFxuICAgICAgL1xcfS8sXG4gICAgICB7XG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfVxuICAgICksXG4gICAgaGxqcy5DT01NRU5UKFxuICAgICAgL1xcKFxcKi8sXG4gICAgICAvXFwqXFwpLyxcbiAgICAgIHtcbiAgICAgICAgcmVsZXZhbmNlOiAxMFxuICAgICAgfVxuICAgIClcbiAgXTtcbiAgY29uc3QgU1RSSU5HID0ge1xuICAgIGNsYXNzTmFtZTogJ3N0cmluZycsXG4gICAgYmVnaW46IC8nLyxcbiAgICBlbmQ6IC8nLyxcbiAgICBjb250YWluczogW3tcbiAgICAgIGJlZ2luOiAvJycvXG4gICAgfV1cbiAgfTtcbiAgY29uc3QgQ0hBUl9TVFJJTkcgPSB7XG4gICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICBiZWdpbjogLygjXFxkKykrL1xuICB9O1xuICBjb25zdCBEQVRFID0ge1xuICAgIGNsYXNzTmFtZTogJ251bWJlcicsXG4gICAgYmVnaW46ICdcXFxcYlxcXFxkKyhcXFxcLlxcXFxkKyk/KERUfER8VCknLFxuICAgIHJlbGV2YW5jZTogMFxuICB9O1xuICBjb25zdCBEQkxfUVVPVEVEX1ZBUklBQkxFID0ge1xuICAgIGNsYXNzTmFtZTogJ3N0cmluZycsIC8vIG5vdCBhIHN0cmluZyB0ZWNobmljYWxseSBidXQgbWFrZXMgc2Vuc2UgdG8gYmUgaGlnaGxpZ2h0ZWQgaW4gdGhlIHNhbWUgc3R5bGVcbiAgICBiZWdpbjogJ1wiJyxcbiAgICBlbmQ6ICdcIidcbiAgfTtcblxuICBjb25zdCBQUk9DRURVUkUgPSB7XG4gICAgY2xhc3NOYW1lOiAnZnVuY3Rpb24nLFxuICAgIGJlZ2luS2V5d29yZHM6ICdwcm9jZWR1cmUnLFxuICAgIGVuZDogL1s6O10vLFxuICAgIGtleXdvcmRzOiAncHJvY2VkdXJlfDEwJyxcbiAgICBjb250YWluczogW1xuICAgICAgaGxqcy5USVRMRV9NT0RFLFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdwYXJhbXMnLFxuICAgICAgICBiZWdpbjogL1xcKC8sXG4gICAgICAgIGVuZDogL1xcKS8sXG4gICAgICAgIGtleXdvcmRzOiBLRVlXT1JEUyxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICBTVFJJTkcsXG4gICAgICAgICAgQ0hBUl9TVFJJTkdcbiAgICAgICAgXVxuICAgICAgfVxuICAgIF0uY29uY2F0KENPTU1FTlRfTU9ERVMpXG4gIH07XG5cbiAgY29uc3QgT0JKRUNUID0ge1xuICAgIGNsYXNzTmFtZTogJ2NsYXNzJyxcbiAgICBiZWdpbjogJ09CSkVDVCAoVGFibGV8Rm9ybXxSZXBvcnR8RGF0YXBvcnR8Q29kZXVuaXR8WE1McG9ydHxNZW51U3VpdGV8UGFnZXxRdWVyeSkgKFxcXFxkKykgKFteXFxcXHJcXFxcbl0rKScsXG4gICAgcmV0dXJuQmVnaW46IHRydWUsXG4gICAgY29udGFpbnM6IFtcbiAgICAgIGhsanMuVElUTEVfTU9ERSxcbiAgICAgIFBST0NFRFVSRVxuICAgIF1cbiAgfTtcblxuICByZXR1cm4ge1xuICAgIG5hbWU6ICdDL0FMJyxcbiAgICBjYXNlX2luc2Vuc2l0aXZlOiB0cnVlLFxuICAgIGtleXdvcmRzOiB7XG4gICAgICBrZXl3b3JkOiBLRVlXT1JEUyxcbiAgICAgIGxpdGVyYWw6IExJVEVSQUxTXG4gICAgfSxcbiAgICBpbGxlZ2FsOiAvXFwvXFwqLyxcbiAgICBjb250YWluczogW1xuICAgICAgU1RSSU5HLFxuICAgICAgQ0hBUl9TVFJJTkcsXG4gICAgICBEQVRFLFxuICAgICAgREJMX1FVT1RFRF9WQVJJQUJMRSxcbiAgICAgIGhsanMuTlVNQkVSX01PREUsXG4gICAgICBPQkpFQ1QsXG4gICAgICBQUk9DRURVUkVcbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gY2FsO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9