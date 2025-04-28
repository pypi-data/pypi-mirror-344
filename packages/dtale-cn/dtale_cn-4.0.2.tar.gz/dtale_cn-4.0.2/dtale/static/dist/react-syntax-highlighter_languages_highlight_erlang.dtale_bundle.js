(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_erlang"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/erlang.js":
/*!*************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/erlang.js ***!
  \*************************************************************************************************/
/***/ ((module) => {

/*
Language: Erlang
Description: Erlang is a general-purpose functional language, with strict evaluation, single assignment, and dynamic typing.
Author: Nikolay Zakharov <nikolay.desh@gmail.com>, Dmitry Kovega <arhibot@gmail.com>
Website: https://www.erlang.org
Category: functional
*/

/** @type LanguageFn */
function erlang(hljs) {
  const BASIC_ATOM_RE = '[a-z\'][a-zA-Z0-9_\']*';
  const FUNCTION_NAME_RE = '(' + BASIC_ATOM_RE + ':' + BASIC_ATOM_RE + '|' + BASIC_ATOM_RE + ')';
  const ERLANG_RESERVED = {
    keyword:
      'after and andalso|10 band begin bnot bor bsl bzr bxor case catch cond div end fun if ' +
      'let not of orelse|10 query receive rem try when xor',
    literal:
      'false true'
  };

  const COMMENT = hljs.COMMENT('%', '$');
  const NUMBER = {
    className: 'number',
    begin: '\\b(\\d+(_\\d+)*#[a-fA-F0-9]+(_[a-fA-F0-9]+)*|\\d+(_\\d+)*(\\.\\d+(_\\d+)*)?([eE][-+]?\\d+)?)',
    relevance: 0
  };
  const NAMED_FUN = {
    begin: 'fun\\s+' + BASIC_ATOM_RE + '/\\d+'
  };
  const FUNCTION_CALL = {
    begin: FUNCTION_NAME_RE + '\\(',
    end: '\\)',
    returnBegin: true,
    relevance: 0,
    contains: [
      {
        begin: FUNCTION_NAME_RE,
        relevance: 0
      },
      {
        begin: '\\(',
        end: '\\)',
        endsWithParent: true,
        returnEnd: true,
        relevance: 0
        // "contains" defined later
      }
    ]
  };
  const TUPLE = {
    begin: /\{/,
    end: /\}/,
    relevance: 0
    // "contains" defined later
  };
  const VAR1 = {
    begin: '\\b_([A-Z][A-Za-z0-9_]*)?',
    relevance: 0
  };
  const VAR2 = {
    begin: '[A-Z][a-zA-Z0-9_]*',
    relevance: 0
  };
  const RECORD_ACCESS = {
    begin: '#' + hljs.UNDERSCORE_IDENT_RE,
    relevance: 0,
    returnBegin: true,
    contains: [
      {
        begin: '#' + hljs.UNDERSCORE_IDENT_RE,
        relevance: 0
      },
      {
        begin: /\{/,
        end: /\}/,
        relevance: 0
        // "contains" defined later
      }
    ]
  };

  const BLOCK_STATEMENTS = {
    beginKeywords: 'fun receive if try case',
    end: 'end',
    keywords: ERLANG_RESERVED
  };
  BLOCK_STATEMENTS.contains = [
    COMMENT,
    NAMED_FUN,
    hljs.inherit(hljs.APOS_STRING_MODE, {
      className: ''
    }),
    BLOCK_STATEMENTS,
    FUNCTION_CALL,
    hljs.QUOTE_STRING_MODE,
    NUMBER,
    TUPLE,
    VAR1,
    VAR2,
    RECORD_ACCESS
  ];

  const BASIC_MODES = [
    COMMENT,
    NAMED_FUN,
    BLOCK_STATEMENTS,
    FUNCTION_CALL,
    hljs.QUOTE_STRING_MODE,
    NUMBER,
    TUPLE,
    VAR1,
    VAR2,
    RECORD_ACCESS
  ];
  FUNCTION_CALL.contains[1].contains = BASIC_MODES;
  TUPLE.contains = BASIC_MODES;
  RECORD_ACCESS.contains[1].contains = BASIC_MODES;

  const DIRECTIVES = [
    "-module",
    "-record",
    "-undef",
    "-export",
    "-ifdef",
    "-ifndef",
    "-author",
    "-copyright",
    "-doc",
    "-vsn",
    "-import",
    "-include",
    "-include_lib",
    "-compile",
    "-define",
    "-else",
    "-endif",
    "-file",
    "-behaviour",
    "-behavior",
    "-spec"
  ];

  const PARAMS = {
    className: 'params',
    begin: '\\(',
    end: '\\)',
    contains: BASIC_MODES
  };
  return {
    name: 'Erlang',
    aliases: ['erl'],
    keywords: ERLANG_RESERVED,
    illegal: '(</|\\*=|\\+=|-=|/\\*|\\*/|\\(\\*|\\*\\))',
    contains: [
      {
        className: 'function',
        begin: '^' + BASIC_ATOM_RE + '\\s*\\(',
        end: '->',
        returnBegin: true,
        illegal: '\\(|#|//|/\\*|\\\\|:|;',
        contains: [
          PARAMS,
          hljs.inherit(hljs.TITLE_MODE, {
            begin: BASIC_ATOM_RE
          })
        ],
        starts: {
          end: ';|\\.',
          keywords: ERLANG_RESERVED,
          contains: BASIC_MODES
        }
      },
      COMMENT,
      {
        begin: '^-',
        end: '\\.',
        relevance: 0,
        excludeEnd: true,
        returnBegin: true,
        keywords: {
          $pattern: '-' + hljs.IDENT_RE,
          keyword: DIRECTIVES.map(x => `${x}|1.5`).join(" ")
        },
        contains: [PARAMS]
      },
      NUMBER,
      hljs.QUOTE_STRING_MODE,
      RECORD_ACCESS,
      VAR1,
      VAR2,
      TUPLE,
      {
        begin: /\.$/
      } // relevance booster
    ]
  };
}

module.exports = erlang;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfZXJsYW5nLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxjQUFjO0FBQ2QsWUFBWTtBQUNaO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0Esa0JBQWtCO0FBQ2xCLGdCQUFnQjtBQUNoQjtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0Esd0NBQXdDO0FBQ3hDO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsV0FBVztBQUNYO0FBQ0E7QUFDQSxpQkFBaUI7QUFDakI7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLDBDQUEwQyxFQUFFO0FBQzVDLFNBQVM7QUFDVDtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsUUFBUTtBQUNSO0FBQ0E7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvZXJsYW5nLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogRXJsYW5nXG5EZXNjcmlwdGlvbjogRXJsYW5nIGlzIGEgZ2VuZXJhbC1wdXJwb3NlIGZ1bmN0aW9uYWwgbGFuZ3VhZ2UsIHdpdGggc3RyaWN0IGV2YWx1YXRpb24sIHNpbmdsZSBhc3NpZ25tZW50LCBhbmQgZHluYW1pYyB0eXBpbmcuXG5BdXRob3I6IE5pa29sYXkgWmFraGFyb3YgPG5pa29sYXkuZGVzaEBnbWFpbC5jb20+LCBEbWl0cnkgS292ZWdhIDxhcmhpYm90QGdtYWlsLmNvbT5cbldlYnNpdGU6IGh0dHBzOi8vd3d3LmVybGFuZy5vcmdcbkNhdGVnb3J5OiBmdW5jdGlvbmFsXG4qL1xuXG4vKiogQHR5cGUgTGFuZ3VhZ2VGbiAqL1xuZnVuY3Rpb24gZXJsYW5nKGhsanMpIHtcbiAgY29uc3QgQkFTSUNfQVRPTV9SRSA9ICdbYS16XFwnXVthLXpBLVowLTlfXFwnXSonO1xuICBjb25zdCBGVU5DVElPTl9OQU1FX1JFID0gJygnICsgQkFTSUNfQVRPTV9SRSArICc6JyArIEJBU0lDX0FUT01fUkUgKyAnfCcgKyBCQVNJQ19BVE9NX1JFICsgJyknO1xuICBjb25zdCBFUkxBTkdfUkVTRVJWRUQgPSB7XG4gICAga2V5d29yZDpcbiAgICAgICdhZnRlciBhbmQgYW5kYWxzb3wxMCBiYW5kIGJlZ2luIGJub3QgYm9yIGJzbCBienIgYnhvciBjYXNlIGNhdGNoIGNvbmQgZGl2IGVuZCBmdW4gaWYgJyArXG4gICAgICAnbGV0IG5vdCBvZiBvcmVsc2V8MTAgcXVlcnkgcmVjZWl2ZSByZW0gdHJ5IHdoZW4geG9yJyxcbiAgICBsaXRlcmFsOlxuICAgICAgJ2ZhbHNlIHRydWUnXG4gIH07XG5cbiAgY29uc3QgQ09NTUVOVCA9IGhsanMuQ09NTUVOVCgnJScsICckJyk7XG4gIGNvbnN0IE5VTUJFUiA9IHtcbiAgICBjbGFzc05hbWU6ICdudW1iZXInLFxuICAgIGJlZ2luOiAnXFxcXGIoXFxcXGQrKF9cXFxcZCspKiNbYS1mQS1GMC05XSsoX1thLWZBLUYwLTldKykqfFxcXFxkKyhfXFxcXGQrKSooXFxcXC5cXFxcZCsoX1xcXFxkKykqKT8oW2VFXVstK10/XFxcXGQrKT8pJyxcbiAgICByZWxldmFuY2U6IDBcbiAgfTtcbiAgY29uc3QgTkFNRURfRlVOID0ge1xuICAgIGJlZ2luOiAnZnVuXFxcXHMrJyArIEJBU0lDX0FUT01fUkUgKyAnL1xcXFxkKydcbiAgfTtcbiAgY29uc3QgRlVOQ1RJT05fQ0FMTCA9IHtcbiAgICBiZWdpbjogRlVOQ1RJT05fTkFNRV9SRSArICdcXFxcKCcsXG4gICAgZW5kOiAnXFxcXCknLFxuICAgIHJldHVybkJlZ2luOiB0cnVlLFxuICAgIHJlbGV2YW5jZTogMCxcbiAgICBjb250YWluczogW1xuICAgICAge1xuICAgICAgICBiZWdpbjogRlVOQ1RJT05fTkFNRV9SRSxcbiAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogJ1xcXFwoJyxcbiAgICAgICAgZW5kOiAnXFxcXCknLFxuICAgICAgICBlbmRzV2l0aFBhcmVudDogdHJ1ZSxcbiAgICAgICAgcmV0dXJuRW5kOiB0cnVlLFxuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgICAgLy8gXCJjb250YWluc1wiIGRlZmluZWQgbGF0ZXJcbiAgICAgIH1cbiAgICBdXG4gIH07XG4gIGNvbnN0IFRVUExFID0ge1xuICAgIGJlZ2luOiAvXFx7LyxcbiAgICBlbmQ6IC9cXH0vLFxuICAgIHJlbGV2YW5jZTogMFxuICAgIC8vIFwiY29udGFpbnNcIiBkZWZpbmVkIGxhdGVyXG4gIH07XG4gIGNvbnN0IFZBUjEgPSB7XG4gICAgYmVnaW46ICdcXFxcYl8oW0EtWl1bQS1aYS16MC05X10qKT8nLFxuICAgIHJlbGV2YW5jZTogMFxuICB9O1xuICBjb25zdCBWQVIyID0ge1xuICAgIGJlZ2luOiAnW0EtWl1bYS16QS1aMC05X10qJyxcbiAgICByZWxldmFuY2U6IDBcbiAgfTtcbiAgY29uc3QgUkVDT1JEX0FDQ0VTUyA9IHtcbiAgICBiZWdpbjogJyMnICsgaGxqcy5VTkRFUlNDT1JFX0lERU5UX1JFLFxuICAgIHJlbGV2YW5jZTogMCxcbiAgICByZXR1cm5CZWdpbjogdHJ1ZSxcbiAgICBjb250YWluczogW1xuICAgICAge1xuICAgICAgICBiZWdpbjogJyMnICsgaGxqcy5VTkRFUlNDT1JFX0lERU5UX1JFLFxuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAvXFx7LyxcbiAgICAgICAgZW5kOiAvXFx9LyxcbiAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICAgIC8vIFwiY29udGFpbnNcIiBkZWZpbmVkIGxhdGVyXG4gICAgICB9XG4gICAgXVxuICB9O1xuXG4gIGNvbnN0IEJMT0NLX1NUQVRFTUVOVFMgPSB7XG4gICAgYmVnaW5LZXl3b3JkczogJ2Z1biByZWNlaXZlIGlmIHRyeSBjYXNlJyxcbiAgICBlbmQ6ICdlbmQnLFxuICAgIGtleXdvcmRzOiBFUkxBTkdfUkVTRVJWRURcbiAgfTtcbiAgQkxPQ0tfU1RBVEVNRU5UUy5jb250YWlucyA9IFtcbiAgICBDT01NRU5ULFxuICAgIE5BTUVEX0ZVTixcbiAgICBobGpzLmluaGVyaXQoaGxqcy5BUE9TX1NUUklOR19NT0RFLCB7XG4gICAgICBjbGFzc05hbWU6ICcnXG4gICAgfSksXG4gICAgQkxPQ0tfU1RBVEVNRU5UUyxcbiAgICBGVU5DVElPTl9DQUxMLFxuICAgIGhsanMuUVVPVEVfU1RSSU5HX01PREUsXG4gICAgTlVNQkVSLFxuICAgIFRVUExFLFxuICAgIFZBUjEsXG4gICAgVkFSMixcbiAgICBSRUNPUkRfQUNDRVNTXG4gIF07XG5cbiAgY29uc3QgQkFTSUNfTU9ERVMgPSBbXG4gICAgQ09NTUVOVCxcbiAgICBOQU1FRF9GVU4sXG4gICAgQkxPQ0tfU1RBVEVNRU5UUyxcbiAgICBGVU5DVElPTl9DQUxMLFxuICAgIGhsanMuUVVPVEVfU1RSSU5HX01PREUsXG4gICAgTlVNQkVSLFxuICAgIFRVUExFLFxuICAgIFZBUjEsXG4gICAgVkFSMixcbiAgICBSRUNPUkRfQUNDRVNTXG4gIF07XG4gIEZVTkNUSU9OX0NBTEwuY29udGFpbnNbMV0uY29udGFpbnMgPSBCQVNJQ19NT0RFUztcbiAgVFVQTEUuY29udGFpbnMgPSBCQVNJQ19NT0RFUztcbiAgUkVDT1JEX0FDQ0VTUy5jb250YWluc1sxXS5jb250YWlucyA9IEJBU0lDX01PREVTO1xuXG4gIGNvbnN0IERJUkVDVElWRVMgPSBbXG4gICAgXCItbW9kdWxlXCIsXG4gICAgXCItcmVjb3JkXCIsXG4gICAgXCItdW5kZWZcIixcbiAgICBcIi1leHBvcnRcIixcbiAgICBcIi1pZmRlZlwiLFxuICAgIFwiLWlmbmRlZlwiLFxuICAgIFwiLWF1dGhvclwiLFxuICAgIFwiLWNvcHlyaWdodFwiLFxuICAgIFwiLWRvY1wiLFxuICAgIFwiLXZzblwiLFxuICAgIFwiLWltcG9ydFwiLFxuICAgIFwiLWluY2x1ZGVcIixcbiAgICBcIi1pbmNsdWRlX2xpYlwiLFxuICAgIFwiLWNvbXBpbGVcIixcbiAgICBcIi1kZWZpbmVcIixcbiAgICBcIi1lbHNlXCIsXG4gICAgXCItZW5kaWZcIixcbiAgICBcIi1maWxlXCIsXG4gICAgXCItYmVoYXZpb3VyXCIsXG4gICAgXCItYmVoYXZpb3JcIixcbiAgICBcIi1zcGVjXCJcbiAgXTtcblxuICBjb25zdCBQQVJBTVMgPSB7XG4gICAgY2xhc3NOYW1lOiAncGFyYW1zJyxcbiAgICBiZWdpbjogJ1xcXFwoJyxcbiAgICBlbmQ6ICdcXFxcKScsXG4gICAgY29udGFpbnM6IEJBU0lDX01PREVTXG4gIH07XG4gIHJldHVybiB7XG4gICAgbmFtZTogJ0VybGFuZycsXG4gICAgYWxpYXNlczogWydlcmwnXSxcbiAgICBrZXl3b3JkczogRVJMQU5HX1JFU0VSVkVELFxuICAgIGlsbGVnYWw6ICcoPC98XFxcXCo9fFxcXFwrPXwtPXwvXFxcXCp8XFxcXCovfFxcXFwoXFxcXCp8XFxcXCpcXFxcKSknLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ2Z1bmN0aW9uJyxcbiAgICAgICAgYmVnaW46ICdeJyArIEJBU0lDX0FUT01fUkUgKyAnXFxcXHMqXFxcXCgnLFxuICAgICAgICBlbmQ6ICctPicsXG4gICAgICAgIHJldHVybkJlZ2luOiB0cnVlLFxuICAgICAgICBpbGxlZ2FsOiAnXFxcXCh8I3wvL3wvXFxcXCp8XFxcXFxcXFx8Onw7JyxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICBQQVJBTVMsXG4gICAgICAgICAgaGxqcy5pbmhlcml0KGhsanMuVElUTEVfTU9ERSwge1xuICAgICAgICAgICAgYmVnaW46IEJBU0lDX0FUT01fUkVcbiAgICAgICAgICB9KVxuICAgICAgICBdLFxuICAgICAgICBzdGFydHM6IHtcbiAgICAgICAgICBlbmQ6ICc7fFxcXFwuJyxcbiAgICAgICAgICBrZXl3b3JkczogRVJMQU5HX1JFU0VSVkVELFxuICAgICAgICAgIGNvbnRhaW5zOiBCQVNJQ19NT0RFU1xuICAgICAgICB9XG4gICAgICB9LFxuICAgICAgQ09NTUVOVCxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICdeLScsXG4gICAgICAgIGVuZDogJ1xcXFwuJyxcbiAgICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgICBleGNsdWRlRW5kOiB0cnVlLFxuICAgICAgICByZXR1cm5CZWdpbjogdHJ1ZSxcbiAgICAgICAga2V5d29yZHM6IHtcbiAgICAgICAgICAkcGF0dGVybjogJy0nICsgaGxqcy5JREVOVF9SRSxcbiAgICAgICAgICBrZXl3b3JkOiBESVJFQ1RJVkVTLm1hcCh4ID0+IGAke3h9fDEuNWApLmpvaW4oXCIgXCIpXG4gICAgICAgIH0sXG4gICAgICAgIGNvbnRhaW5zOiBbUEFSQU1TXVxuICAgICAgfSxcbiAgICAgIE5VTUJFUixcbiAgICAgIGhsanMuUVVPVEVfU1RSSU5HX01PREUsXG4gICAgICBSRUNPUkRfQUNDRVNTLFxuICAgICAgVkFSMSxcbiAgICAgIFZBUjIsXG4gICAgICBUVVBMRSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC9cXC4kL1xuICAgICAgfSAvLyByZWxldmFuY2UgYm9vc3RlclxuICAgIF1cbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBlcmxhbmc7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=