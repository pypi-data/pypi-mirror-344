(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_monkey"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/monkey.js":
/*!*************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/monkey.js ***!
  \*************************************************************************************************/
/***/ ((module) => {

/*
Language: Monkey
Description: Monkey2 is an easy to use, cross platform, games oriented programming language from Blitz Research.
Author: Arthur Bikmullin <devolonter@gmail.com>
Website: https://blitzresearch.itch.io/monkey2
*/

function monkey(hljs) {
  const NUMBER = {
    className: 'number',
    relevance: 0,
    variants: [
      {
        begin: '[$][a-fA-F0-9]+'
      },
      hljs.NUMBER_MODE
    ]
  };

  return {
    name: 'Monkey',
    case_insensitive: true,
    keywords: {
      keyword: 'public private property continue exit extern new try catch ' +
        'eachin not abstract final select case default const local global field ' +
        'end if then else elseif endif while wend repeat until forever for ' +
        'to step next return module inline throw import',

      built_in: 'DebugLog DebugStop Error Print ACos ACosr ASin ASinr ATan ATan2 ATan2r ATanr Abs Abs Ceil ' +
        'Clamp Clamp Cos Cosr Exp Floor Log Max Max Min Min Pow Sgn Sgn Sin Sinr Sqrt Tan Tanr Seed PI HALFPI TWOPI',

      literal: 'true false null and or shl shr mod'
    },
    illegal: /\/\*/,
    contains: [
      hljs.COMMENT('#rem', '#end'),
      hljs.COMMENT(
        "'",
        '$',
        {
          relevance: 0
        }
      ),
      {
        className: 'function',
        beginKeywords: 'function method',
        end: '[(=:]|$',
        illegal: /\n/,
        contains: [ hljs.UNDERSCORE_TITLE_MODE ]
      },
      {
        className: 'class',
        beginKeywords: 'class interface',
        end: '$',
        contains: [
          {
            beginKeywords: 'extends implements'
          },
          hljs.UNDERSCORE_TITLE_MODE
        ]
      },
      {
        className: 'built_in',
        begin: '\\b(self|super)\\b'
      },
      {
        className: 'meta',
        begin: '\\s*#',
        end: '$',
        keywords: {
          'meta-keyword': 'if else elseif endif end then'
        }
      },
      {
        className: 'meta',
        begin: '^\\s*strict\\b'
      },
      {
        beginKeywords: 'alias',
        end: '=',
        contains: [ hljs.UNDERSCORE_TITLE_MODE ]
      },
      hljs.QUOTE_STRING_MODE,
      NUMBER
    ]
  };
}

module.exports = monkey;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfbW9ua2V5LmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBOztBQUVBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsV0FBVztBQUNYO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9tb25rZXkuanMiXSwic291cmNlc0NvbnRlbnQiOlsiLypcbkxhbmd1YWdlOiBNb25rZXlcbkRlc2NyaXB0aW9uOiBNb25rZXkyIGlzIGFuIGVhc3kgdG8gdXNlLCBjcm9zcyBwbGF0Zm9ybSwgZ2FtZXMgb3JpZW50ZWQgcHJvZ3JhbW1pbmcgbGFuZ3VhZ2UgZnJvbSBCbGl0eiBSZXNlYXJjaC5cbkF1dGhvcjogQXJ0aHVyIEJpa211bGxpbiA8ZGV2b2xvbnRlckBnbWFpbC5jb20+XG5XZWJzaXRlOiBodHRwczovL2JsaXR6cmVzZWFyY2guaXRjaC5pby9tb25rZXkyXG4qL1xuXG5mdW5jdGlvbiBtb25rZXkoaGxqcykge1xuICBjb25zdCBOVU1CRVIgPSB7XG4gICAgY2xhc3NOYW1lOiAnbnVtYmVyJyxcbiAgICByZWxldmFuY2U6IDAsXG4gICAgdmFyaWFudHM6IFtcbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICdbJF1bYS1mQS1GMC05XSsnXG4gICAgICB9LFxuICAgICAgaGxqcy5OVU1CRVJfTU9ERVxuICAgIF1cbiAgfTtcblxuICByZXR1cm4ge1xuICAgIG5hbWU6ICdNb25rZXknLFxuICAgIGNhc2VfaW5zZW5zaXRpdmU6IHRydWUsXG4gICAga2V5d29yZHM6IHtcbiAgICAgIGtleXdvcmQ6ICdwdWJsaWMgcHJpdmF0ZSBwcm9wZXJ0eSBjb250aW51ZSBleGl0IGV4dGVybiBuZXcgdHJ5IGNhdGNoICcgK1xuICAgICAgICAnZWFjaGluIG5vdCBhYnN0cmFjdCBmaW5hbCBzZWxlY3QgY2FzZSBkZWZhdWx0IGNvbnN0IGxvY2FsIGdsb2JhbCBmaWVsZCAnICtcbiAgICAgICAgJ2VuZCBpZiB0aGVuIGVsc2UgZWxzZWlmIGVuZGlmIHdoaWxlIHdlbmQgcmVwZWF0IHVudGlsIGZvcmV2ZXIgZm9yICcgK1xuICAgICAgICAndG8gc3RlcCBuZXh0IHJldHVybiBtb2R1bGUgaW5saW5lIHRocm93IGltcG9ydCcsXG5cbiAgICAgIGJ1aWx0X2luOiAnRGVidWdMb2cgRGVidWdTdG9wIEVycm9yIFByaW50IEFDb3MgQUNvc3IgQVNpbiBBU2luciBBVGFuIEFUYW4yIEFUYW4yciBBVGFuciBBYnMgQWJzIENlaWwgJyArXG4gICAgICAgICdDbGFtcCBDbGFtcCBDb3MgQ29zciBFeHAgRmxvb3IgTG9nIE1heCBNYXggTWluIE1pbiBQb3cgU2duIFNnbiBTaW4gU2luciBTcXJ0IFRhbiBUYW5yIFNlZWQgUEkgSEFMRlBJIFRXT1BJJyxcblxuICAgICAgbGl0ZXJhbDogJ3RydWUgZmFsc2UgbnVsbCBhbmQgb3Igc2hsIHNociBtb2QnXG4gICAgfSxcbiAgICBpbGxlZ2FsOiAvXFwvXFwqLyxcbiAgICBjb250YWluczogW1xuICAgICAgaGxqcy5DT01NRU5UKCcjcmVtJywgJyNlbmQnKSxcbiAgICAgIGhsanMuQ09NTUVOVChcbiAgICAgICAgXCInXCIsXG4gICAgICAgICckJyxcbiAgICAgICAge1xuICAgICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgICB9XG4gICAgICApLFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdmdW5jdGlvbicsXG4gICAgICAgIGJlZ2luS2V5d29yZHM6ICdmdW5jdGlvbiBtZXRob2QnLFxuICAgICAgICBlbmQ6ICdbKD06XXwkJyxcbiAgICAgICAgaWxsZWdhbDogL1xcbi8sXG4gICAgICAgIGNvbnRhaW5zOiBbIGhsanMuVU5ERVJTQ09SRV9USVRMRV9NT0RFIF1cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ2NsYXNzJyxcbiAgICAgICAgYmVnaW5LZXl3b3JkczogJ2NsYXNzIGludGVyZmFjZScsXG4gICAgICAgIGVuZDogJyQnLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luS2V5d29yZHM6ICdleHRlbmRzIGltcGxlbWVudHMnXG4gICAgICAgICAgfSxcbiAgICAgICAgICBobGpzLlVOREVSU0NPUkVfVElUTEVfTU9ERVxuICAgICAgICBdXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdidWlsdF9pbicsXG4gICAgICAgIGJlZ2luOiAnXFxcXGIoc2VsZnxzdXBlcilcXFxcYidcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ21ldGEnLFxuICAgICAgICBiZWdpbjogJ1xcXFxzKiMnLFxuICAgICAgICBlbmQ6ICckJyxcbiAgICAgICAga2V5d29yZHM6IHtcbiAgICAgICAgICAnbWV0YS1rZXl3b3JkJzogJ2lmIGVsc2UgZWxzZWlmIGVuZGlmIGVuZCB0aGVuJ1xuICAgICAgICB9XG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdtZXRhJyxcbiAgICAgICAgYmVnaW46ICdeXFxcXHMqc3RyaWN0XFxcXGInXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbktleXdvcmRzOiAnYWxpYXMnLFxuICAgICAgICBlbmQ6ICc9JyxcbiAgICAgICAgY29udGFpbnM6IFsgaGxqcy5VTkRFUlNDT1JFX1RJVExFX01PREUgXVxuICAgICAgfSxcbiAgICAgIGhsanMuUVVPVEVfU1RSSU5HX01PREUsXG4gICAgICBOVU1CRVJcbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gbW9ua2V5O1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9