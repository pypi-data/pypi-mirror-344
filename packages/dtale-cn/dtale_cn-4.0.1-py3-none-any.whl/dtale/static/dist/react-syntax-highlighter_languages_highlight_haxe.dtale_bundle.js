(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_haxe"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/haxe.js":
/*!***********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/haxe.js ***!
  \***********************************************************************************************/
/***/ ((module) => {

/*
Language: Haxe
Description: Haxe is an open source toolkit based on a modern, high level, strictly typed programming language.
Author: Christopher Kaster <ikasoki@gmail.com> (Based on the actionscript.js language file by Alexander Myadzel)
Contributors: Kenton Hamaluik <kentonh@gmail.com>
Website: https://haxe.org
*/

function haxe(hljs) {

  const HAXE_BASIC_TYPES = 'Int Float String Bool Dynamic Void Array ';

  return {
    name: 'Haxe',
    aliases: ['hx'],
    keywords: {
      keyword: 'break case cast catch continue default do dynamic else enum extern ' +
               'for function here if import in inline never new override package private get set ' +
               'public return static super switch this throw trace try typedef untyped using var while ' +
               HAXE_BASIC_TYPES,
      built_in:
        'trace this',
      literal:
        'true false null _'
    },
    contains: [
      {
        className: 'string', // interpolate-able strings
        begin: '\'',
        end: '\'',
        contains: [
          hljs.BACKSLASH_ESCAPE,
          {
            className: 'subst', // interpolation
            begin: '\\$\\{',
            end: '\\}'
          },
          {
            className: 'subst', // interpolation
            begin: '\\$',
            end: /\W\}/
          }
        ]
      },
      hljs.QUOTE_STRING_MODE,
      hljs.C_LINE_COMMENT_MODE,
      hljs.C_BLOCK_COMMENT_MODE,
      hljs.C_NUMBER_MODE,
      {
        className: 'meta', // compiler meta
        begin: '@:',
        end: '$'
      },
      {
        className: 'meta', // compiler conditionals
        begin: '#',
        end: '$',
        keywords: {
          'meta-keyword': 'if else elseif end error'
        }
      },
      {
        className: 'type', // function types
        begin: ':[ \t]*',
        end: '[^A-Za-z0-9_ \t\\->]',
        excludeBegin: true,
        excludeEnd: true,
        relevance: 0
      },
      {
        className: 'type', // types
        begin: ':[ \t]*',
        end: '\\W',
        excludeBegin: true,
        excludeEnd: true
      },
      {
        className: 'type', // instantiation
        begin: 'new *',
        end: '\\W',
        excludeBegin: true,
        excludeEnd: true
      },
      {
        className: 'class', // enums
        beginKeywords: 'enum',
        end: '\\{',
        contains: [hljs.TITLE_MODE]
      },
      {
        className: 'class', // abstracts
        beginKeywords: 'abstract',
        end: '[\\{$]',
        contains: [
          {
            className: 'type',
            begin: '\\(',
            end: '\\)',
            excludeBegin: true,
            excludeEnd: true
          },
          {
            className: 'type',
            begin: 'from +',
            end: '\\W',
            excludeBegin: true,
            excludeEnd: true
          },
          {
            className: 'type',
            begin: 'to +',
            end: '\\W',
            excludeBegin: true,
            excludeEnd: true
          },
          hljs.TITLE_MODE
        ],
        keywords: {
          keyword: 'abstract from to'
        }
      },
      {
        className: 'class', // classes
        begin: '\\b(class|interface) +',
        end: '[\\{$]',
        excludeEnd: true,
        keywords: 'class interface',
        contains: [
          {
            className: 'keyword',
            begin: '\\b(extends|implements) +',
            keywords: 'extends implements',
            contains: [
              {
                className: 'type',
                begin: hljs.IDENT_RE,
                relevance: 0
              }
            ]
          },
          hljs.TITLE_MODE
        ]
      },
      {
        className: 'function',
        beginKeywords: 'function',
        end: '\\(',
        excludeEnd: true,
        illegal: '\\S',
        contains: [hljs.TITLE_MODE]
      }
    ],
    illegal: /<\//
  };
}

module.exports = haxe;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfaGF4ZS5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTs7QUFFQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsMEJBQTBCO0FBQzFCLHFCQUFxQjtBQUNyQixXQUFXO0FBQ1g7QUFDQTtBQUNBO0FBQ0Esc0JBQXNCO0FBQ3RCO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLGlCQUFpQjtBQUNqQjtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSxrQkFBa0I7QUFDbEI7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsV0FBVztBQUNYO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFdBQVc7QUFDWDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLGtCQUFrQjtBQUNsQjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsV0FBVztBQUNYO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9oYXhlLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogSGF4ZVxuRGVzY3JpcHRpb246IEhheGUgaXMgYW4gb3BlbiBzb3VyY2UgdG9vbGtpdCBiYXNlZCBvbiBhIG1vZGVybiwgaGlnaCBsZXZlbCwgc3RyaWN0bHkgdHlwZWQgcHJvZ3JhbW1pbmcgbGFuZ3VhZ2UuXG5BdXRob3I6IENocmlzdG9waGVyIEthc3RlciA8aWthc29raUBnbWFpbC5jb20+IChCYXNlZCBvbiB0aGUgYWN0aW9uc2NyaXB0LmpzIGxhbmd1YWdlIGZpbGUgYnkgQWxleGFuZGVyIE15YWR6ZWwpXG5Db250cmlidXRvcnM6IEtlbnRvbiBIYW1hbHVpayA8a2VudG9uaEBnbWFpbC5jb20+XG5XZWJzaXRlOiBodHRwczovL2hheGUub3JnXG4qL1xuXG5mdW5jdGlvbiBoYXhlKGhsanMpIHtcblxuICBjb25zdCBIQVhFX0JBU0lDX1RZUEVTID0gJ0ludCBGbG9hdCBTdHJpbmcgQm9vbCBEeW5hbWljIFZvaWQgQXJyYXkgJztcblxuICByZXR1cm4ge1xuICAgIG5hbWU6ICdIYXhlJyxcbiAgICBhbGlhc2VzOiBbJ2h4J10sXG4gICAga2V5d29yZHM6IHtcbiAgICAgIGtleXdvcmQ6ICdicmVhayBjYXNlIGNhc3QgY2F0Y2ggY29udGludWUgZGVmYXVsdCBkbyBkeW5hbWljIGVsc2UgZW51bSBleHRlcm4gJyArXG4gICAgICAgICAgICAgICAnZm9yIGZ1bmN0aW9uIGhlcmUgaWYgaW1wb3J0IGluIGlubGluZSBuZXZlciBuZXcgb3ZlcnJpZGUgcGFja2FnZSBwcml2YXRlIGdldCBzZXQgJyArXG4gICAgICAgICAgICAgICAncHVibGljIHJldHVybiBzdGF0aWMgc3VwZXIgc3dpdGNoIHRoaXMgdGhyb3cgdHJhY2UgdHJ5IHR5cGVkZWYgdW50eXBlZCB1c2luZyB2YXIgd2hpbGUgJyArXG4gICAgICAgICAgICAgICBIQVhFX0JBU0lDX1RZUEVTLFxuICAgICAgYnVpbHRfaW46XG4gICAgICAgICd0cmFjZSB0aGlzJyxcbiAgICAgIGxpdGVyYWw6XG4gICAgICAgICd0cnVlIGZhbHNlIG51bGwgXydcbiAgICB9LFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3N0cmluZycsIC8vIGludGVycG9sYXRlLWFibGUgc3RyaW5nc1xuICAgICAgICBiZWdpbjogJ1xcJycsXG4gICAgICAgIGVuZDogJ1xcJycsXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgaGxqcy5CQUNLU0xBU0hfRVNDQVBFLFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGNsYXNzTmFtZTogJ3N1YnN0JywgLy8gaW50ZXJwb2xhdGlvblxuICAgICAgICAgICAgYmVnaW46ICdcXFxcJFxcXFx7JyxcbiAgICAgICAgICAgIGVuZDogJ1xcXFx9J1xuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgY2xhc3NOYW1lOiAnc3Vic3QnLCAvLyBpbnRlcnBvbGF0aW9uXG4gICAgICAgICAgICBiZWdpbjogJ1xcXFwkJyxcbiAgICAgICAgICAgIGVuZDogL1xcV1xcfS9cbiAgICAgICAgICB9XG4gICAgICAgIF1cbiAgICAgIH0sXG4gICAgICBobGpzLlFVT1RFX1NUUklOR19NT0RFLFxuICAgICAgaGxqcy5DX0xJTkVfQ09NTUVOVF9NT0RFLFxuICAgICAgaGxqcy5DX0JMT0NLX0NPTU1FTlRfTU9ERSxcbiAgICAgIGhsanMuQ19OVU1CRVJfTU9ERSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnbWV0YScsIC8vIGNvbXBpbGVyIG1ldGFcbiAgICAgICAgYmVnaW46ICdAOicsXG4gICAgICAgIGVuZDogJyQnXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdtZXRhJywgLy8gY29tcGlsZXIgY29uZGl0aW9uYWxzXG4gICAgICAgIGJlZ2luOiAnIycsXG4gICAgICAgIGVuZDogJyQnLFxuICAgICAgICBrZXl3b3Jkczoge1xuICAgICAgICAgICdtZXRhLWtleXdvcmQnOiAnaWYgZWxzZSBlbHNlaWYgZW5kIGVycm9yJ1xuICAgICAgICB9XG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICd0eXBlJywgLy8gZnVuY3Rpb24gdHlwZXNcbiAgICAgICAgYmVnaW46ICc6WyBcXHRdKicsXG4gICAgICAgIGVuZDogJ1teQS1aYS16MC05XyBcXHRcXFxcLT5dJyxcbiAgICAgICAgZXhjbHVkZUJlZ2luOiB0cnVlLFxuICAgICAgICBleGNsdWRlRW5kOiB0cnVlLFxuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3R5cGUnLCAvLyB0eXBlc1xuICAgICAgICBiZWdpbjogJzpbIFxcdF0qJyxcbiAgICAgICAgZW5kOiAnXFxcXFcnLFxuICAgICAgICBleGNsdWRlQmVnaW46IHRydWUsXG4gICAgICAgIGV4Y2x1ZGVFbmQ6IHRydWVcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3R5cGUnLCAvLyBpbnN0YW50aWF0aW9uXG4gICAgICAgIGJlZ2luOiAnbmV3IConLFxuICAgICAgICBlbmQ6ICdcXFxcVycsXG4gICAgICAgIGV4Y2x1ZGVCZWdpbjogdHJ1ZSxcbiAgICAgICAgZXhjbHVkZUVuZDogdHJ1ZVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnY2xhc3MnLCAvLyBlbnVtc1xuICAgICAgICBiZWdpbktleXdvcmRzOiAnZW51bScsXG4gICAgICAgIGVuZDogJ1xcXFx7JyxcbiAgICAgICAgY29udGFpbnM6IFtobGpzLlRJVExFX01PREVdXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdjbGFzcycsIC8vIGFic3RyYWN0c1xuICAgICAgICBiZWdpbktleXdvcmRzOiAnYWJzdHJhY3QnLFxuICAgICAgICBlbmQ6ICdbXFxcXHskXScsXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgY2xhc3NOYW1lOiAndHlwZScsXG4gICAgICAgICAgICBiZWdpbjogJ1xcXFwoJyxcbiAgICAgICAgICAgIGVuZDogJ1xcXFwpJyxcbiAgICAgICAgICAgIGV4Y2x1ZGVCZWdpbjogdHJ1ZSxcbiAgICAgICAgICAgIGV4Y2x1ZGVFbmQ6IHRydWVcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGNsYXNzTmFtZTogJ3R5cGUnLFxuICAgICAgICAgICAgYmVnaW46ICdmcm9tICsnLFxuICAgICAgICAgICAgZW5kOiAnXFxcXFcnLFxuICAgICAgICAgICAgZXhjbHVkZUJlZ2luOiB0cnVlLFxuICAgICAgICAgICAgZXhjbHVkZUVuZDogdHJ1ZVxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgY2xhc3NOYW1lOiAndHlwZScsXG4gICAgICAgICAgICBiZWdpbjogJ3RvICsnLFxuICAgICAgICAgICAgZW5kOiAnXFxcXFcnLFxuICAgICAgICAgICAgZXhjbHVkZUJlZ2luOiB0cnVlLFxuICAgICAgICAgICAgZXhjbHVkZUVuZDogdHJ1ZVxuICAgICAgICAgIH0sXG4gICAgICAgICAgaGxqcy5USVRMRV9NT0RFXG4gICAgICAgIF0sXG4gICAgICAgIGtleXdvcmRzOiB7XG4gICAgICAgICAga2V5d29yZDogJ2Fic3RyYWN0IGZyb20gdG8nXG4gICAgICAgIH1cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ2NsYXNzJywgLy8gY2xhc3Nlc1xuICAgICAgICBiZWdpbjogJ1xcXFxiKGNsYXNzfGludGVyZmFjZSkgKycsXG4gICAgICAgIGVuZDogJ1tcXFxceyRdJyxcbiAgICAgICAgZXhjbHVkZUVuZDogdHJ1ZSxcbiAgICAgICAga2V5d29yZHM6ICdjbGFzcyBpbnRlcmZhY2UnLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIGNsYXNzTmFtZTogJ2tleXdvcmQnLFxuICAgICAgICAgICAgYmVnaW46ICdcXFxcYihleHRlbmRzfGltcGxlbWVudHMpICsnLFxuICAgICAgICAgICAga2V5d29yZHM6ICdleHRlbmRzIGltcGxlbWVudHMnLFxuICAgICAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICAgICAge1xuICAgICAgICAgICAgICAgIGNsYXNzTmFtZTogJ3R5cGUnLFxuICAgICAgICAgICAgICAgIGJlZ2luOiBobGpzLklERU5UX1JFLFxuICAgICAgICAgICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgICAgICAgICB9XG4gICAgICAgICAgICBdXG4gICAgICAgICAgfSxcbiAgICAgICAgICBobGpzLlRJVExFX01PREVcbiAgICAgICAgXVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnZnVuY3Rpb24nLFxuICAgICAgICBiZWdpbktleXdvcmRzOiAnZnVuY3Rpb24nLFxuICAgICAgICBlbmQ6ICdcXFxcKCcsXG4gICAgICAgIGV4Y2x1ZGVFbmQ6IHRydWUsXG4gICAgICAgIGlsbGVnYWw6ICdcXFxcUycsXG4gICAgICAgIGNvbnRhaW5zOiBbaGxqcy5USVRMRV9NT0RFXVxuICAgICAgfVxuICAgIF0sXG4gICAgaWxsZWdhbDogLzxcXC8vXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gaGF4ZTtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==