(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_angelscript"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/angelscript.js":
/*!******************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/angelscript.js ***!
  \******************************************************************************************************/
/***/ ((module) => {

/*
Language: AngelScript
Author: Melissa Geels <melissa@nimble.tools>
Category: scripting
Website: https://www.angelcode.com/angelscript/
*/

/** @type LanguageFn */
function angelscript(hljs) {
  var builtInTypeMode = {
    className: 'built_in',
    begin: '\\b(void|bool|int|int8|int16|int32|int64|uint|uint8|uint16|uint32|uint64|string|ref|array|double|float|auto|dictionary)'
  };

  var objectHandleMode = {
    className: 'symbol',
    begin: '[a-zA-Z0-9_]+@'
  };

  var genericMode = {
    className: 'keyword',
    begin: '<', end: '>',
    contains: [ builtInTypeMode, objectHandleMode ]
  };

  builtInTypeMode.contains = [ genericMode ];
  objectHandleMode.contains = [ genericMode ];

  return {
    name: 'AngelScript',
    aliases: ['asc'],

    keywords:
      'for in|0 break continue while do|0 return if else case switch namespace is cast ' +
      'or and xor not get|0 in inout|10 out override set|0 private public const default|0 ' +
      'final shared external mixin|10 enum typedef funcdef this super import from interface ' +
      'abstract|0 try catch protected explicit property',

    // avoid close detection with C# and JS
    illegal: '(^using\\s+[A-Za-z0-9_\\.]+;$|\\bfunction\\s*[^\\(])',

    contains: [
      { // 'strings'
        className: 'string',
        begin: '\'', end: '\'',
        illegal: '\\n',
        contains: [ hljs.BACKSLASH_ESCAPE ],
        relevance: 0
      },

      // """heredoc strings"""
      {
        className: 'string',
        begin: '"""', end: '"""'
      },

      { // "strings"
        className: 'string',
        begin: '"', end: '"',
        illegal: '\\n',
        contains: [ hljs.BACKSLASH_ESCAPE ],
        relevance: 0
      },

      hljs.C_LINE_COMMENT_MODE, // single-line comments
      hljs.C_BLOCK_COMMENT_MODE, // comment blocks

      { // metadata
        className: 'string',
        begin: '^\\s*\\[', end: '\\]',
      },

      { // interface or namespace declaration
        beginKeywords: 'interface namespace', end: /\{/,
        illegal: '[;.\\-]',
        contains: [
          { // interface or namespace name
            className: 'symbol',
            begin: '[a-zA-Z0-9_]+'
          }
        ]
      },

      { // class declaration
        beginKeywords: 'class', end: /\{/,
        illegal: '[;.\\-]',
        contains: [
          { // class name
            className: 'symbol',
            begin: '[a-zA-Z0-9_]+',
            contains: [
              {
                begin: '[:,]\\s*',
                contains: [
                  {
                    className: 'symbol',
                    begin: '[a-zA-Z0-9_]+'
                  }
                ]
              }
            ]
          }
        ]
      },

      builtInTypeMode, // built-in types
      objectHandleMode, // object handles

      { // literals
        className: 'literal',
        begin: '\\b(null|true|false)'
      },

      { // numbers
        className: 'number',
        relevance: 0,
        begin: '(-?)(\\b0[xXbBoOdD][a-fA-F0-9]+|(\\b\\d+(\\.\\d*)?f?|\\.\\d+f?)([eE][-+]?\\d+f?)?)'
      }
    ]
  };
}

module.exports = angelscript;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfYW5nZWxzY3JpcHQuZHRhbGVfYnVuZGxlLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQSwwQ0FBMEM7O0FBRTFDO0FBQ0EsUUFBUTtBQUNSO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPOztBQUVQO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTzs7QUFFUCxRQUFRO0FBQ1I7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87O0FBRVA7QUFDQTs7QUFFQSxRQUFRO0FBQ1I7QUFDQTtBQUNBLE9BQU87O0FBRVAsUUFBUTtBQUNSLHNEQUFzRDtBQUN0RCxvQkFBb0I7QUFDcEI7QUFDQSxZQUFZO0FBQ1o7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPOztBQUVQLFFBQVE7QUFDUix3Q0FBd0M7QUFDeEMsb0JBQW9CO0FBQ3BCO0FBQ0EsWUFBWTtBQUNaO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87O0FBRVA7QUFDQTs7QUFFQSxRQUFRO0FBQ1I7QUFDQTtBQUNBLE9BQU87O0FBRVAsUUFBUTtBQUNSO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9hbmdlbHNjcmlwdC5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKlxuTGFuZ3VhZ2U6IEFuZ2VsU2NyaXB0XG5BdXRob3I6IE1lbGlzc2EgR2VlbHMgPG1lbGlzc2FAbmltYmxlLnRvb2xzPlxuQ2F0ZWdvcnk6IHNjcmlwdGluZ1xuV2Vic2l0ZTogaHR0cHM6Ly93d3cuYW5nZWxjb2RlLmNvbS9hbmdlbHNjcmlwdC9cbiovXG5cbi8qKiBAdHlwZSBMYW5ndWFnZUZuICovXG5mdW5jdGlvbiBhbmdlbHNjcmlwdChobGpzKSB7XG4gIHZhciBidWlsdEluVHlwZU1vZGUgPSB7XG4gICAgY2xhc3NOYW1lOiAnYnVpbHRfaW4nLFxuICAgIGJlZ2luOiAnXFxcXGIodm9pZHxib29sfGludHxpbnQ4fGludDE2fGludDMyfGludDY0fHVpbnR8dWludDh8dWludDE2fHVpbnQzMnx1aW50NjR8c3RyaW5nfHJlZnxhcnJheXxkb3VibGV8ZmxvYXR8YXV0b3xkaWN0aW9uYXJ5KSdcbiAgfTtcblxuICB2YXIgb2JqZWN0SGFuZGxlTW9kZSA9IHtcbiAgICBjbGFzc05hbWU6ICdzeW1ib2wnLFxuICAgIGJlZ2luOiAnW2EtekEtWjAtOV9dK0AnXG4gIH07XG5cbiAgdmFyIGdlbmVyaWNNb2RlID0ge1xuICAgIGNsYXNzTmFtZTogJ2tleXdvcmQnLFxuICAgIGJlZ2luOiAnPCcsIGVuZDogJz4nLFxuICAgIGNvbnRhaW5zOiBbIGJ1aWx0SW5UeXBlTW9kZSwgb2JqZWN0SGFuZGxlTW9kZSBdXG4gIH07XG5cbiAgYnVpbHRJblR5cGVNb2RlLmNvbnRhaW5zID0gWyBnZW5lcmljTW9kZSBdO1xuICBvYmplY3RIYW5kbGVNb2RlLmNvbnRhaW5zID0gWyBnZW5lcmljTW9kZSBdO1xuXG4gIHJldHVybiB7XG4gICAgbmFtZTogJ0FuZ2VsU2NyaXB0JyxcbiAgICBhbGlhc2VzOiBbJ2FzYyddLFxuXG4gICAga2V5d29yZHM6XG4gICAgICAnZm9yIGlufDAgYnJlYWsgY29udGludWUgd2hpbGUgZG98MCByZXR1cm4gaWYgZWxzZSBjYXNlIHN3aXRjaCBuYW1lc3BhY2UgaXMgY2FzdCAnICtcbiAgICAgICdvciBhbmQgeG9yIG5vdCBnZXR8MCBpbiBpbm91dHwxMCBvdXQgb3ZlcnJpZGUgc2V0fDAgcHJpdmF0ZSBwdWJsaWMgY29uc3QgZGVmYXVsdHwwICcgK1xuICAgICAgJ2ZpbmFsIHNoYXJlZCBleHRlcm5hbCBtaXhpbnwxMCBlbnVtIHR5cGVkZWYgZnVuY2RlZiB0aGlzIHN1cGVyIGltcG9ydCBmcm9tIGludGVyZmFjZSAnICtcbiAgICAgICdhYnN0cmFjdHwwIHRyeSBjYXRjaCBwcm90ZWN0ZWQgZXhwbGljaXQgcHJvcGVydHknLFxuXG4gICAgLy8gYXZvaWQgY2xvc2UgZGV0ZWN0aW9uIHdpdGggQyMgYW5kIEpTXG4gICAgaWxsZWdhbDogJyhedXNpbmdcXFxccytbQS1aYS16MC05X1xcXFwuXSs7JHxcXFxcYmZ1bmN0aW9uXFxcXHMqW15cXFxcKF0pJyxcblxuICAgIGNvbnRhaW5zOiBbXG4gICAgICB7IC8vICdzdHJpbmdzJ1xuICAgICAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgICAgICBiZWdpbjogJ1xcJycsIGVuZDogJ1xcJycsXG4gICAgICAgIGlsbGVnYWw6ICdcXFxcbicsXG4gICAgICAgIGNvbnRhaW5zOiBbIGhsanMuQkFDS1NMQVNIX0VTQ0FQRSBdLFxuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH0sXG5cbiAgICAgIC8vIFwiXCJcImhlcmVkb2Mgc3RyaW5nc1wiXCJcIlxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgICAgICBiZWdpbjogJ1wiXCJcIicsIGVuZDogJ1wiXCJcIidcbiAgICAgIH0sXG5cbiAgICAgIHsgLy8gXCJzdHJpbmdzXCJcbiAgICAgICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICAgICAgYmVnaW46ICdcIicsIGVuZDogJ1wiJyxcbiAgICAgICAgaWxsZWdhbDogJ1xcXFxuJyxcbiAgICAgICAgY29udGFpbnM6IFsgaGxqcy5CQUNLU0xBU0hfRVNDQVBFIF0sXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfSxcblxuICAgICAgaGxqcy5DX0xJTkVfQ09NTUVOVF9NT0RFLCAvLyBzaW5nbGUtbGluZSBjb21tZW50c1xuICAgICAgaGxqcy5DX0JMT0NLX0NPTU1FTlRfTU9ERSwgLy8gY29tbWVudCBibG9ja3NcblxuICAgICAgeyAvLyBtZXRhZGF0YVxuICAgICAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgICAgICBiZWdpbjogJ15cXFxccypcXFxcWycsIGVuZDogJ1xcXFxdJyxcbiAgICAgIH0sXG5cbiAgICAgIHsgLy8gaW50ZXJmYWNlIG9yIG5hbWVzcGFjZSBkZWNsYXJhdGlvblxuICAgICAgICBiZWdpbktleXdvcmRzOiAnaW50ZXJmYWNlIG5hbWVzcGFjZScsIGVuZDogL1xcey8sXG4gICAgICAgIGlsbGVnYWw6ICdbOy5cXFxcLV0nLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIHsgLy8gaW50ZXJmYWNlIG9yIG5hbWVzcGFjZSBuYW1lXG4gICAgICAgICAgICBjbGFzc05hbWU6ICdzeW1ib2wnLFxuICAgICAgICAgICAgYmVnaW46ICdbYS16QS1aMC05X10rJ1xuICAgICAgICAgIH1cbiAgICAgICAgXVxuICAgICAgfSxcblxuICAgICAgeyAvLyBjbGFzcyBkZWNsYXJhdGlvblxuICAgICAgICBiZWdpbktleXdvcmRzOiAnY2xhc3MnLCBlbmQ6IC9cXHsvLFxuICAgICAgICBpbGxlZ2FsOiAnWzsuXFxcXC1dJyxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICB7IC8vIGNsYXNzIG5hbWVcbiAgICAgICAgICAgIGNsYXNzTmFtZTogJ3N5bWJvbCcsXG4gICAgICAgICAgICBiZWdpbjogJ1thLXpBLVowLTlfXSsnLFxuICAgICAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICAgICAge1xuICAgICAgICAgICAgICAgIGJlZ2luOiAnWzosXVxcXFxzKicsXG4gICAgICAgICAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgICAgICAgY2xhc3NOYW1lOiAnc3ltYm9sJyxcbiAgICAgICAgICAgICAgICAgICAgYmVnaW46ICdbYS16QS1aMC05X10rJ1xuICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIF1cbiAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgXVxuICAgICAgICAgIH1cbiAgICAgICAgXVxuICAgICAgfSxcblxuICAgICAgYnVpbHRJblR5cGVNb2RlLCAvLyBidWlsdC1pbiB0eXBlc1xuICAgICAgb2JqZWN0SGFuZGxlTW9kZSwgLy8gb2JqZWN0IGhhbmRsZXNcblxuICAgICAgeyAvLyBsaXRlcmFsc1xuICAgICAgICBjbGFzc05hbWU6ICdsaXRlcmFsJyxcbiAgICAgICAgYmVnaW46ICdcXFxcYihudWxsfHRydWV8ZmFsc2UpJ1xuICAgICAgfSxcblxuICAgICAgeyAvLyBudW1iZXJzXG4gICAgICAgIGNsYXNzTmFtZTogJ251bWJlcicsXG4gICAgICAgIHJlbGV2YW5jZTogMCxcbiAgICAgICAgYmVnaW46ICcoLT8pKFxcXFxiMFt4WGJCb09kRF1bYS1mQS1GMC05XSt8KFxcXFxiXFxcXGQrKFxcXFwuXFxcXGQqKT9mP3xcXFxcLlxcXFxkK2Y/KShbZUVdWy0rXT9cXFxcZCtmPyk/KSdcbiAgICAgIH1cbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gYW5nZWxzY3JpcHQ7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=