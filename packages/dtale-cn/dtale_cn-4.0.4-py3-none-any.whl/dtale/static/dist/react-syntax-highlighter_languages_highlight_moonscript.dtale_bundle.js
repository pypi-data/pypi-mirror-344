(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_moonscript"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/moonscript.js":
/*!*****************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/moonscript.js ***!
  \*****************************************************************************************************/
/***/ ((module) => {

/*
Language: MoonScript
Author: Billy Quith <chinbillybilbo@gmail.com>
Description: MoonScript is a programming language that transcompiles to Lua.
Origin: coffeescript.js
Website: http://moonscript.org/
Category: scripting
*/

function moonscript(hljs) {
  const KEYWORDS = {
    keyword:
      // Moonscript keywords
      'if then not for in while do return else elseif break continue switch and or ' +
      'unless when class extends super local import export from using',
    literal:
      'true false nil',
    built_in:
      '_G _VERSION assert collectgarbage dofile error getfenv getmetatable ipairs load ' +
      'loadfile loadstring module next pairs pcall print rawequal rawget rawset require ' +
      'select setfenv setmetatable tonumber tostring type unpack xpcall coroutine debug ' +
      'io math os package string table'
  };
  const JS_IDENT_RE = '[A-Za-z$_][0-9A-Za-z$_]*';
  const SUBST = {
    className: 'subst',
    begin: /#\{/,
    end: /\}/,
    keywords: KEYWORDS
  };
  const EXPRESSIONS = [
    hljs.inherit(hljs.C_NUMBER_MODE,
      {
        starts: {
          end: '(\\s*/)?',
          relevance: 0
        }
      }), // a number tries to eat the following slash to prevent treating it as a regexp
    {
      className: 'string',
      variants: [
        {
          begin: /'/,
          end: /'/,
          contains: [ hljs.BACKSLASH_ESCAPE ]
        },
        {
          begin: /"/,
          end: /"/,
          contains: [
            hljs.BACKSLASH_ESCAPE,
            SUBST
          ]
        }
      ]
    },
    {
      className: 'built_in',
      begin: '@__' + hljs.IDENT_RE
    },
    {
      begin: '@' + hljs.IDENT_RE // relevance booster on par with CoffeeScript
    },
    {
      begin: hljs.IDENT_RE + '\\\\' + hljs.IDENT_RE // inst\method
    }
  ];
  SUBST.contains = EXPRESSIONS;

  const TITLE = hljs.inherit(hljs.TITLE_MODE, {
    begin: JS_IDENT_RE
  });
  const POSSIBLE_PARAMS_RE = '(\\(.*\\)\\s*)?\\B[-=]>';
  const PARAMS = {
    className: 'params',
    begin: '\\([^\\(]',
    returnBegin: true,
    /* We need another contained nameless mode to not have every nested
    pair of parens to be called "params" */
    contains: [
      {
        begin: /\(/,
        end: /\)/,
        keywords: KEYWORDS,
        contains: [ 'self' ].concat(EXPRESSIONS)
      }
    ]
  };

  return {
    name: 'MoonScript',
    aliases: [ 'moon' ],
    keywords: KEYWORDS,
    illegal: /\/\*/,
    contains: EXPRESSIONS.concat([
      hljs.COMMENT('--', '$'),
      {
        className: 'function', // function: -> =>
        begin: '^\\s*' + JS_IDENT_RE + '\\s*=\\s*' + POSSIBLE_PARAMS_RE,
        end: '[-=]>',
        returnBegin: true,
        contains: [
          TITLE,
          PARAMS
        ]
      },
      {
        begin: /[\(,:=]\s*/, // anonymous function start
        relevance: 0,
        contains: [
          {
            className: 'function',
            begin: POSSIBLE_PARAMS_RE,
            end: '[-=]>',
            returnBegin: true,
            contains: [ PARAMS ]
          }
        ]
      },
      {
        className: 'class',
        beginKeywords: 'class',
        end: '$',
        illegal: /[:="\[\]]/,
        contains: [
          {
            beginKeywords: 'extends',
            endsWithParent: true,
            illegal: /[:="\[\]]/,
            contains: [ TITLE ]
          },
          TITLE
        ]
      },
      {
        className: 'name', // table
        begin: JS_IDENT_RE + ':',
        end: ':',
        returnBegin: true,
        returnEnd: true,
        relevance: 0
      }
    ])
  };
}

module.exports = moonscript;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfbW9vbnNjcmlwdC5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxlQUFlO0FBQ2YsWUFBWTtBQUNaO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFNBQVM7QUFDVDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0EsR0FBRztBQUNIO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsV0FBVztBQUNYO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvbW9vbnNjcmlwdC5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKlxuTGFuZ3VhZ2U6IE1vb25TY3JpcHRcbkF1dGhvcjogQmlsbHkgUXVpdGggPGNoaW5iaWxseWJpbGJvQGdtYWlsLmNvbT5cbkRlc2NyaXB0aW9uOiBNb29uU2NyaXB0IGlzIGEgcHJvZ3JhbW1pbmcgbGFuZ3VhZ2UgdGhhdCB0cmFuc2NvbXBpbGVzIHRvIEx1YS5cbk9yaWdpbjogY29mZmVlc2NyaXB0LmpzXG5XZWJzaXRlOiBodHRwOi8vbW9vbnNjcmlwdC5vcmcvXG5DYXRlZ29yeTogc2NyaXB0aW5nXG4qL1xuXG5mdW5jdGlvbiBtb29uc2NyaXB0KGhsanMpIHtcbiAgY29uc3QgS0VZV09SRFMgPSB7XG4gICAga2V5d29yZDpcbiAgICAgIC8vIE1vb25zY3JpcHQga2V5d29yZHNcbiAgICAgICdpZiB0aGVuIG5vdCBmb3IgaW4gd2hpbGUgZG8gcmV0dXJuIGVsc2UgZWxzZWlmIGJyZWFrIGNvbnRpbnVlIHN3aXRjaCBhbmQgb3IgJyArXG4gICAgICAndW5sZXNzIHdoZW4gY2xhc3MgZXh0ZW5kcyBzdXBlciBsb2NhbCBpbXBvcnQgZXhwb3J0IGZyb20gdXNpbmcnLFxuICAgIGxpdGVyYWw6XG4gICAgICAndHJ1ZSBmYWxzZSBuaWwnLFxuICAgIGJ1aWx0X2luOlxuICAgICAgJ19HIF9WRVJTSU9OIGFzc2VydCBjb2xsZWN0Z2FyYmFnZSBkb2ZpbGUgZXJyb3IgZ2V0ZmVudiBnZXRtZXRhdGFibGUgaXBhaXJzIGxvYWQgJyArXG4gICAgICAnbG9hZGZpbGUgbG9hZHN0cmluZyBtb2R1bGUgbmV4dCBwYWlycyBwY2FsbCBwcmludCByYXdlcXVhbCByYXdnZXQgcmF3c2V0IHJlcXVpcmUgJyArXG4gICAgICAnc2VsZWN0IHNldGZlbnYgc2V0bWV0YXRhYmxlIHRvbnVtYmVyIHRvc3RyaW5nIHR5cGUgdW5wYWNrIHhwY2FsbCBjb3JvdXRpbmUgZGVidWcgJyArXG4gICAgICAnaW8gbWF0aCBvcyBwYWNrYWdlIHN0cmluZyB0YWJsZSdcbiAgfTtcbiAgY29uc3QgSlNfSURFTlRfUkUgPSAnW0EtWmEteiRfXVswLTlBLVphLXokX10qJztcbiAgY29uc3QgU1VCU1QgPSB7XG4gICAgY2xhc3NOYW1lOiAnc3Vic3QnLFxuICAgIGJlZ2luOiAvI1xcey8sXG4gICAgZW5kOiAvXFx9LyxcbiAgICBrZXl3b3JkczogS0VZV09SRFNcbiAgfTtcbiAgY29uc3QgRVhQUkVTU0lPTlMgPSBbXG4gICAgaGxqcy5pbmhlcml0KGhsanMuQ19OVU1CRVJfTU9ERSxcbiAgICAgIHtcbiAgICAgICAgc3RhcnRzOiB7XG4gICAgICAgICAgZW5kOiAnKFxcXFxzKi8pPycsXG4gICAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICAgIH1cbiAgICAgIH0pLCAvLyBhIG51bWJlciB0cmllcyB0byBlYXQgdGhlIGZvbGxvd2luZyBzbGFzaCB0byBwcmV2ZW50IHRyZWF0aW5nIGl0IGFzIGEgcmVnZXhwXG4gICAge1xuICAgICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICAgIHZhcmlhbnRzOiBbXG4gICAgICAgIHtcbiAgICAgICAgICBiZWdpbjogLycvLFxuICAgICAgICAgIGVuZDogLycvLFxuICAgICAgICAgIGNvbnRhaW5zOiBbIGhsanMuQkFDS1NMQVNIX0VTQ0FQRSBdXG4gICAgICAgIH0sXG4gICAgICAgIHtcbiAgICAgICAgICBiZWdpbjogL1wiLyxcbiAgICAgICAgICBlbmQ6IC9cIi8sXG4gICAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICAgIGhsanMuQkFDS1NMQVNIX0VTQ0FQRSxcbiAgICAgICAgICAgIFNVQlNUXG4gICAgICAgICAgXVxuICAgICAgICB9XG4gICAgICBdXG4gICAgfSxcbiAgICB7XG4gICAgICBjbGFzc05hbWU6ICdidWlsdF9pbicsXG4gICAgICBiZWdpbjogJ0BfXycgKyBobGpzLklERU5UX1JFXG4gICAgfSxcbiAgICB7XG4gICAgICBiZWdpbjogJ0AnICsgaGxqcy5JREVOVF9SRSAvLyByZWxldmFuY2UgYm9vc3RlciBvbiBwYXIgd2l0aCBDb2ZmZWVTY3JpcHRcbiAgICB9LFxuICAgIHtcbiAgICAgIGJlZ2luOiBobGpzLklERU5UX1JFICsgJ1xcXFxcXFxcJyArIGhsanMuSURFTlRfUkUgLy8gaW5zdFxcbWV0aG9kXG4gICAgfVxuICBdO1xuICBTVUJTVC5jb250YWlucyA9IEVYUFJFU1NJT05TO1xuXG4gIGNvbnN0IFRJVExFID0gaGxqcy5pbmhlcml0KGhsanMuVElUTEVfTU9ERSwge1xuICAgIGJlZ2luOiBKU19JREVOVF9SRVxuICB9KTtcbiAgY29uc3QgUE9TU0lCTEVfUEFSQU1TX1JFID0gJyhcXFxcKC4qXFxcXClcXFxccyopP1xcXFxCWy09XT4nO1xuICBjb25zdCBQQVJBTVMgPSB7XG4gICAgY2xhc3NOYW1lOiAncGFyYW1zJyxcbiAgICBiZWdpbjogJ1xcXFwoW15cXFxcKF0nLFxuICAgIHJldHVybkJlZ2luOiB0cnVlLFxuICAgIC8qIFdlIG5lZWQgYW5vdGhlciBjb250YWluZWQgbmFtZWxlc3MgbW9kZSB0byBub3QgaGF2ZSBldmVyeSBuZXN0ZWRcbiAgICBwYWlyIG9mIHBhcmVucyB0byBiZSBjYWxsZWQgXCJwYXJhbXNcIiAqL1xuICAgIGNvbnRhaW5zOiBbXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAvXFwoLyxcbiAgICAgICAgZW5kOiAvXFwpLyxcbiAgICAgICAga2V5d29yZHM6IEtFWVdPUkRTLFxuICAgICAgICBjb250YWluczogWyAnc2VsZicgXS5jb25jYXQoRVhQUkVTU0lPTlMpXG4gICAgICB9XG4gICAgXVxuICB9O1xuXG4gIHJldHVybiB7XG4gICAgbmFtZTogJ01vb25TY3JpcHQnLFxuICAgIGFsaWFzZXM6IFsgJ21vb24nIF0sXG4gICAga2V5d29yZHM6IEtFWVdPUkRTLFxuICAgIGlsbGVnYWw6IC9cXC9cXCovLFxuICAgIGNvbnRhaW5zOiBFWFBSRVNTSU9OUy5jb25jYXQoW1xuICAgICAgaGxqcy5DT01NRU5UKCctLScsICckJyksXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ2Z1bmN0aW9uJywgLy8gZnVuY3Rpb246IC0+ID0+XG4gICAgICAgIGJlZ2luOiAnXlxcXFxzKicgKyBKU19JREVOVF9SRSArICdcXFxccyo9XFxcXHMqJyArIFBPU1NJQkxFX1BBUkFNU19SRSxcbiAgICAgICAgZW5kOiAnWy09XT4nLFxuICAgICAgICByZXR1cm5CZWdpbjogdHJ1ZSxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICBUSVRMRSxcbiAgICAgICAgICBQQVJBTVNcbiAgICAgICAgXVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC9bXFwoLDo9XVxccyovLCAvLyBhbm9ueW1vdXMgZnVuY3Rpb24gc3RhcnRcbiAgICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIGNsYXNzTmFtZTogJ2Z1bmN0aW9uJyxcbiAgICAgICAgICAgIGJlZ2luOiBQT1NTSUJMRV9QQVJBTVNfUkUsXG4gICAgICAgICAgICBlbmQ6ICdbLT1dPicsXG4gICAgICAgICAgICByZXR1cm5CZWdpbjogdHJ1ZSxcbiAgICAgICAgICAgIGNvbnRhaW5zOiBbIFBBUkFNUyBdXG4gICAgICAgICAgfVxuICAgICAgICBdXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdjbGFzcycsXG4gICAgICAgIGJlZ2luS2V5d29yZHM6ICdjbGFzcycsXG4gICAgICAgIGVuZDogJyQnLFxuICAgICAgICBpbGxlZ2FsOiAvWzo9XCJcXFtcXF1dLyxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbktleXdvcmRzOiAnZXh0ZW5kcycsXG4gICAgICAgICAgICBlbmRzV2l0aFBhcmVudDogdHJ1ZSxcbiAgICAgICAgICAgIGlsbGVnYWw6IC9bOj1cIlxcW1xcXV0vLFxuICAgICAgICAgICAgY29udGFpbnM6IFsgVElUTEUgXVxuICAgICAgICAgIH0sXG4gICAgICAgICAgVElUTEVcbiAgICAgICAgXVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnbmFtZScsIC8vIHRhYmxlXG4gICAgICAgIGJlZ2luOiBKU19JREVOVF9SRSArICc6JyxcbiAgICAgICAgZW5kOiAnOicsXG4gICAgICAgIHJldHVybkJlZ2luOiB0cnVlLFxuICAgICAgICByZXR1cm5FbmQ6IHRydWUsXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfVxuICAgIF0pXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gbW9vbnNjcmlwdDtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==