(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_inform7"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/inform7.js":
/*!**************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/inform7.js ***!
  \**************************************************************************************************/
/***/ ((module) => {

/*
Language: Inform 7
Author: Bruno Dias <bruno.r.dias@gmail.com>
Description: Language definition for Inform 7, a DSL for writing parser interactive fiction.
Website: http://inform7.com
*/

function inform7(hljs) {
  const START_BRACKET = '\\[';
  const END_BRACKET = '\\]';
  return {
    name: 'Inform 7',
    aliases: ['i7'],
    case_insensitive: true,
    keywords: {
      // Some keywords more or less unique to I7, for relevance.
      keyword:
        // kind:
        'thing room person man woman animal container ' +
        'supporter backdrop door ' +
        // characteristic:
        'scenery open closed locked inside gender ' +
        // verb:
        'is are say understand ' +
        // misc keyword:
        'kind of rule'
    },
    contains: [
      {
        className: 'string',
        begin: '"',
        end: '"',
        relevance: 0,
        contains: [
          {
            className: 'subst',
            begin: START_BRACKET,
            end: END_BRACKET
          }
        ]
      },
      {
        className: 'section',
        begin: /^(Volume|Book|Part|Chapter|Section|Table)\b/,
        end: '$'
      },
      {
        // Rule definition
        // This is here for relevance.
        begin: /^(Check|Carry out|Report|Instead of|To|Rule|When|Before|After)\b/,
        end: ':',
        contains: [
          {
            // Rule name
            begin: '\\(This',
            end: '\\)'
          }
        ]
      },
      {
        className: 'comment',
        begin: START_BRACKET,
        end: END_BRACKET,
        contains: ['self']
      }
    ]
  };
}

module.exports = inform7;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfaW5mb3JtNy5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvaW5mb3JtNy5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKlxuTGFuZ3VhZ2U6IEluZm9ybSA3XG5BdXRob3I6IEJydW5vIERpYXMgPGJydW5vLnIuZGlhc0BnbWFpbC5jb20+XG5EZXNjcmlwdGlvbjogTGFuZ3VhZ2UgZGVmaW5pdGlvbiBmb3IgSW5mb3JtIDcsIGEgRFNMIGZvciB3cml0aW5nIHBhcnNlciBpbnRlcmFjdGl2ZSBmaWN0aW9uLlxuV2Vic2l0ZTogaHR0cDovL2luZm9ybTcuY29tXG4qL1xuXG5mdW5jdGlvbiBpbmZvcm03KGhsanMpIHtcbiAgY29uc3QgU1RBUlRfQlJBQ0tFVCA9ICdcXFxcWyc7XG4gIGNvbnN0IEVORF9CUkFDS0VUID0gJ1xcXFxdJztcbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnSW5mb3JtIDcnLFxuICAgIGFsaWFzZXM6IFsnaTcnXSxcbiAgICBjYXNlX2luc2Vuc2l0aXZlOiB0cnVlLFxuICAgIGtleXdvcmRzOiB7XG4gICAgICAvLyBTb21lIGtleXdvcmRzIG1vcmUgb3IgbGVzcyB1bmlxdWUgdG8gSTcsIGZvciByZWxldmFuY2UuXG4gICAgICBrZXl3b3JkOlxuICAgICAgICAvLyBraW5kOlxuICAgICAgICAndGhpbmcgcm9vbSBwZXJzb24gbWFuIHdvbWFuIGFuaW1hbCBjb250YWluZXIgJyArXG4gICAgICAgICdzdXBwb3J0ZXIgYmFja2Ryb3AgZG9vciAnICtcbiAgICAgICAgLy8gY2hhcmFjdGVyaXN0aWM6XG4gICAgICAgICdzY2VuZXJ5IG9wZW4gY2xvc2VkIGxvY2tlZCBpbnNpZGUgZ2VuZGVyICcgK1xuICAgICAgICAvLyB2ZXJiOlxuICAgICAgICAnaXMgYXJlIHNheSB1bmRlcnN0YW5kICcgK1xuICAgICAgICAvLyBtaXNjIGtleXdvcmQ6XG4gICAgICAgICdraW5kIG9mIHJ1bGUnXG4gICAgfSxcbiAgICBjb250YWluczogW1xuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgICAgICBiZWdpbjogJ1wiJyxcbiAgICAgICAgZW5kOiAnXCInLFxuICAgICAgICByZWxldmFuY2U6IDAsXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgY2xhc3NOYW1lOiAnc3Vic3QnLFxuICAgICAgICAgICAgYmVnaW46IFNUQVJUX0JSQUNLRVQsXG4gICAgICAgICAgICBlbmQ6IEVORF9CUkFDS0VUXG4gICAgICAgICAgfVxuICAgICAgICBdXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdzZWN0aW9uJyxcbiAgICAgICAgYmVnaW46IC9eKFZvbHVtZXxCb29rfFBhcnR8Q2hhcHRlcnxTZWN0aW9ufFRhYmxlKVxcYi8sXG4gICAgICAgIGVuZDogJyQnXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICAvLyBSdWxlIGRlZmluaXRpb25cbiAgICAgICAgLy8gVGhpcyBpcyBoZXJlIGZvciByZWxldmFuY2UuXG4gICAgICAgIGJlZ2luOiAvXihDaGVja3xDYXJyeSBvdXR8UmVwb3J0fEluc3RlYWQgb2Z8VG98UnVsZXxXaGVufEJlZm9yZXxBZnRlcilcXGIvLFxuICAgICAgICBlbmQ6ICc6JyxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICAvLyBSdWxlIG5hbWVcbiAgICAgICAgICAgIGJlZ2luOiAnXFxcXChUaGlzJyxcbiAgICAgICAgICAgIGVuZDogJ1xcXFwpJ1xuICAgICAgICAgIH1cbiAgICAgICAgXVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnY29tbWVudCcsXG4gICAgICAgIGJlZ2luOiBTVEFSVF9CUkFDS0VULFxuICAgICAgICBlbmQ6IEVORF9CUkFDS0VULFxuICAgICAgICBjb250YWluczogWydzZWxmJ11cbiAgICAgIH1cbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gaW5mb3JtNztcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==