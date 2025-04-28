(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_haskell"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/haskell.js":
/*!**************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/haskell.js ***!
  \**************************************************************************************************/
/***/ ((module) => {

/*
Language: Haskell
Author: Jeremy Hull <sourdrums@gmail.com>
Contributors: Zena Treep <zena.treep@gmail.com>
Website: https://www.haskell.org
Category: functional
*/

function haskell(hljs) {
  const COMMENT = {
    variants: [
      hljs.COMMENT('--', '$'),
      hljs.COMMENT(
        /\{-/,
        /-\}/,
        {
          contains: ['self']
        }
      )
    ]
  };

  const PRAGMA = {
    className: 'meta',
    begin: /\{-#/,
    end: /#-\}/
  };

  const PREPROCESSOR = {
    className: 'meta',
    begin: '^#',
    end: '$'
  };

  const CONSTRUCTOR = {
    className: 'type',
    begin: '\\b[A-Z][\\w\']*', // TODO: other constructors (build-in, infix).
    relevance: 0
  };

  const LIST = {
    begin: '\\(',
    end: '\\)',
    illegal: '"',
    contains: [
      PRAGMA,
      PREPROCESSOR,
      {
        className: 'type',
        begin: '\\b[A-Z][\\w]*(\\((\\.\\.|,|\\w+)\\))?'
      },
      hljs.inherit(hljs.TITLE_MODE, {
        begin: '[_a-z][\\w\']*'
      }),
      COMMENT
    ]
  };

  const RECORD = {
    begin: /\{/,
    end: /\}/,
    contains: LIST.contains
  };

  return {
    name: 'Haskell',
    aliases: ['hs'],
    keywords:
      'let in if then else case of where do module import hiding ' +
      'qualified type data newtype deriving class instance as default ' +
      'infix infixl infixr foreign export ccall stdcall cplusplus ' +
      'jvm dotnet safe unsafe family forall mdo proc rec',
    contains: [
      // Top-level constructions.
      {
        beginKeywords: 'module',
        end: 'where',
        keywords: 'module where',
        contains: [
          LIST,
          COMMENT
        ],
        illegal: '\\W\\.|;'
      },
      {
        begin: '\\bimport\\b',
        end: '$',
        keywords: 'import qualified as hiding',
        contains: [
          LIST,
          COMMENT
        ],
        illegal: '\\W\\.|;'
      },
      {
        className: 'class',
        begin: '^(\\s*)?(class|instance)\\b',
        end: 'where',
        keywords: 'class family instance where',
        contains: [
          CONSTRUCTOR,
          LIST,
          COMMENT
        ]
      },
      {
        className: 'class',
        begin: '\\b(data|(new)?type)\\b',
        end: '$',
        keywords: 'data family type newtype deriving',
        contains: [
          PRAGMA,
          CONSTRUCTOR,
          LIST,
          RECORD,
          COMMENT
        ]
      },
      {
        beginKeywords: 'default',
        end: '$',
        contains: [
          CONSTRUCTOR,
          LIST,
          COMMENT
        ]
      },
      {
        beginKeywords: 'infix infixl infixr',
        end: '$',
        contains: [
          hljs.C_NUMBER_MODE,
          COMMENT
        ]
      },
      {
        begin: '\\bforeign\\b',
        end: '$',
        keywords: 'foreign import export ccall stdcall cplusplus jvm ' +
                  'dotnet safe unsafe',
        contains: [
          CONSTRUCTOR,
          hljs.QUOTE_STRING_MODE,
          COMMENT
        ]
      },
      {
        className: 'meta',
        begin: '#!\\/usr\\/bin\\/env\ runhaskell',
        end: '$'
      },
      // "Whitespaces".
      PRAGMA,
      PREPROCESSOR,

      // Literals and names.

      // TODO: characters.
      hljs.QUOTE_STRING_MODE,
      hljs.C_NUMBER_MODE,
      CONSTRUCTOR,
      hljs.inherit(hljs.TITLE_MODE, {
        begin: '^[_a-z][\\w\']*'
      }),
      COMMENT,
      { // No markup, relevance booster
        begin: '->|<-'
      }
    ]
  };
}

module.exports = haskell;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfaGFza2VsbC5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsV0FBVztBQUNYLFlBQVk7QUFDWjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBLGNBQWM7QUFDZCxjQUFjO0FBQ2Q7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBOztBQUVBO0FBQ0EsY0FBYztBQUNkLFlBQVk7QUFDWjtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLDBCQUEwQjtBQUMxQixPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLDBCQUEwQjtBQUMxQixPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBOztBQUVBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBLFFBQVE7QUFDUjtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9oYXNrZWxsLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogSGFza2VsbFxuQXV0aG9yOiBKZXJlbXkgSHVsbCA8c291cmRydW1zQGdtYWlsLmNvbT5cbkNvbnRyaWJ1dG9yczogWmVuYSBUcmVlcCA8emVuYS50cmVlcEBnbWFpbC5jb20+XG5XZWJzaXRlOiBodHRwczovL3d3dy5oYXNrZWxsLm9yZ1xuQ2F0ZWdvcnk6IGZ1bmN0aW9uYWxcbiovXG5cbmZ1bmN0aW9uIGhhc2tlbGwoaGxqcykge1xuICBjb25zdCBDT01NRU5UID0ge1xuICAgIHZhcmlhbnRzOiBbXG4gICAgICBobGpzLkNPTU1FTlQoJy0tJywgJyQnKSxcbiAgICAgIGhsanMuQ09NTUVOVChcbiAgICAgICAgL1xcey0vLFxuICAgICAgICAvLVxcfS8sXG4gICAgICAgIHtcbiAgICAgICAgICBjb250YWluczogWydzZWxmJ11cbiAgICAgICAgfVxuICAgICAgKVxuICAgIF1cbiAgfTtcblxuICBjb25zdCBQUkFHTUEgPSB7XG4gICAgY2xhc3NOYW1lOiAnbWV0YScsXG4gICAgYmVnaW46IC9cXHstIy8sXG4gICAgZW5kOiAvIy1cXH0vXG4gIH07XG5cbiAgY29uc3QgUFJFUFJPQ0VTU09SID0ge1xuICAgIGNsYXNzTmFtZTogJ21ldGEnLFxuICAgIGJlZ2luOiAnXiMnLFxuICAgIGVuZDogJyQnXG4gIH07XG5cbiAgY29uc3QgQ09OU1RSVUNUT1IgPSB7XG4gICAgY2xhc3NOYW1lOiAndHlwZScsXG4gICAgYmVnaW46ICdcXFxcYltBLVpdW1xcXFx3XFwnXSonLCAvLyBUT0RPOiBvdGhlciBjb25zdHJ1Y3RvcnMgKGJ1aWxkLWluLCBpbmZpeCkuXG4gICAgcmVsZXZhbmNlOiAwXG4gIH07XG5cbiAgY29uc3QgTElTVCA9IHtcbiAgICBiZWdpbjogJ1xcXFwoJyxcbiAgICBlbmQ6ICdcXFxcKScsXG4gICAgaWxsZWdhbDogJ1wiJyxcbiAgICBjb250YWluczogW1xuICAgICAgUFJBR01BLFxuICAgICAgUFJFUFJPQ0VTU09SLFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICd0eXBlJyxcbiAgICAgICAgYmVnaW46ICdcXFxcYltBLVpdW1xcXFx3XSooXFxcXCgoXFxcXC5cXFxcLnwsfFxcXFx3KylcXFxcKSk/J1xuICAgICAgfSxcbiAgICAgIGhsanMuaW5oZXJpdChobGpzLlRJVExFX01PREUsIHtcbiAgICAgICAgYmVnaW46ICdbX2Etel1bXFxcXHdcXCddKidcbiAgICAgIH0pLFxuICAgICAgQ09NTUVOVFxuICAgIF1cbiAgfTtcblxuICBjb25zdCBSRUNPUkQgPSB7XG4gICAgYmVnaW46IC9cXHsvLFxuICAgIGVuZDogL1xcfS8sXG4gICAgY29udGFpbnM6IExJU1QuY29udGFpbnNcbiAgfTtcblxuICByZXR1cm4ge1xuICAgIG5hbWU6ICdIYXNrZWxsJyxcbiAgICBhbGlhc2VzOiBbJ2hzJ10sXG4gICAga2V5d29yZHM6XG4gICAgICAnbGV0IGluIGlmIHRoZW4gZWxzZSBjYXNlIG9mIHdoZXJlIGRvIG1vZHVsZSBpbXBvcnQgaGlkaW5nICcgK1xuICAgICAgJ3F1YWxpZmllZCB0eXBlIGRhdGEgbmV3dHlwZSBkZXJpdmluZyBjbGFzcyBpbnN0YW5jZSBhcyBkZWZhdWx0ICcgK1xuICAgICAgJ2luZml4IGluZml4bCBpbmZpeHIgZm9yZWlnbiBleHBvcnQgY2NhbGwgc3RkY2FsbCBjcGx1c3BsdXMgJyArXG4gICAgICAnanZtIGRvdG5ldCBzYWZlIHVuc2FmZSBmYW1pbHkgZm9yYWxsIG1kbyBwcm9jIHJlYycsXG4gICAgY29udGFpbnM6IFtcbiAgICAgIC8vIFRvcC1sZXZlbCBjb25zdHJ1Y3Rpb25zLlxuICAgICAge1xuICAgICAgICBiZWdpbktleXdvcmRzOiAnbW9kdWxlJyxcbiAgICAgICAgZW5kOiAnd2hlcmUnLFxuICAgICAgICBrZXl3b3JkczogJ21vZHVsZSB3aGVyZScsXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgTElTVCxcbiAgICAgICAgICBDT01NRU5UXG4gICAgICAgIF0sXG4gICAgICAgIGlsbGVnYWw6ICdcXFxcV1xcXFwufDsnXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogJ1xcXFxiaW1wb3J0XFxcXGInLFxuICAgICAgICBlbmQ6ICckJyxcbiAgICAgICAga2V5d29yZHM6ICdpbXBvcnQgcXVhbGlmaWVkIGFzIGhpZGluZycsXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgTElTVCxcbiAgICAgICAgICBDT01NRU5UXG4gICAgICAgIF0sXG4gICAgICAgIGlsbGVnYWw6ICdcXFxcV1xcXFwufDsnXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdjbGFzcycsXG4gICAgICAgIGJlZ2luOiAnXihcXFxccyopPyhjbGFzc3xpbnN0YW5jZSlcXFxcYicsXG4gICAgICAgIGVuZDogJ3doZXJlJyxcbiAgICAgICAga2V5d29yZHM6ICdjbGFzcyBmYW1pbHkgaW5zdGFuY2Ugd2hlcmUnLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIENPTlNUUlVDVE9SLFxuICAgICAgICAgIExJU1QsXG4gICAgICAgICAgQ09NTUVOVFxuICAgICAgICBdXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdjbGFzcycsXG4gICAgICAgIGJlZ2luOiAnXFxcXGIoZGF0YXwobmV3KT90eXBlKVxcXFxiJyxcbiAgICAgICAgZW5kOiAnJCcsXG4gICAgICAgIGtleXdvcmRzOiAnZGF0YSBmYW1pbHkgdHlwZSBuZXd0eXBlIGRlcml2aW5nJyxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICBQUkFHTUEsXG4gICAgICAgICAgQ09OU1RSVUNUT1IsXG4gICAgICAgICAgTElTVCxcbiAgICAgICAgICBSRUNPUkQsXG4gICAgICAgICAgQ09NTUVOVFxuICAgICAgICBdXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbktleXdvcmRzOiAnZGVmYXVsdCcsXG4gICAgICAgIGVuZDogJyQnLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIENPTlNUUlVDVE9SLFxuICAgICAgICAgIExJU1QsXG4gICAgICAgICAgQ09NTUVOVFxuICAgICAgICBdXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbktleXdvcmRzOiAnaW5maXggaW5maXhsIGluZml4cicsXG4gICAgICAgIGVuZDogJyQnLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIGhsanMuQ19OVU1CRVJfTU9ERSxcbiAgICAgICAgICBDT01NRU5UXG4gICAgICAgIF1cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnXFxcXGJmb3JlaWduXFxcXGInLFxuICAgICAgICBlbmQ6ICckJyxcbiAgICAgICAga2V5d29yZHM6ICdmb3JlaWduIGltcG9ydCBleHBvcnQgY2NhbGwgc3RkY2FsbCBjcGx1c3BsdXMganZtICcgK1xuICAgICAgICAgICAgICAgICAgJ2RvdG5ldCBzYWZlIHVuc2FmZScsXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgQ09OU1RSVUNUT1IsXG4gICAgICAgICAgaGxqcy5RVU9URV9TVFJJTkdfTU9ERSxcbiAgICAgICAgICBDT01NRU5UXG4gICAgICAgIF1cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ21ldGEnLFxuICAgICAgICBiZWdpbjogJyMhXFxcXC91c3JcXFxcL2JpblxcXFwvZW52XFwgcnVuaGFza2VsbCcsXG4gICAgICAgIGVuZDogJyQnXG4gICAgICB9LFxuICAgICAgLy8gXCJXaGl0ZXNwYWNlc1wiLlxuICAgICAgUFJBR01BLFxuICAgICAgUFJFUFJPQ0VTU09SLFxuXG4gICAgICAvLyBMaXRlcmFscyBhbmQgbmFtZXMuXG5cbiAgICAgIC8vIFRPRE86IGNoYXJhY3RlcnMuXG4gICAgICBobGpzLlFVT1RFX1NUUklOR19NT0RFLFxuICAgICAgaGxqcy5DX05VTUJFUl9NT0RFLFxuICAgICAgQ09OU1RSVUNUT1IsXG4gICAgICBobGpzLmluaGVyaXQoaGxqcy5USVRMRV9NT0RFLCB7XG4gICAgICAgIGJlZ2luOiAnXltfYS16XVtcXFxcd1xcJ10qJ1xuICAgICAgfSksXG4gICAgICBDT01NRU5ULFxuICAgICAgeyAvLyBObyBtYXJrdXAsIHJlbGV2YW5jZSBib29zdGVyXG4gICAgICAgIGJlZ2luOiAnLT58PC0nXG4gICAgICB9XG4gICAgXVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IGhhc2tlbGw7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=