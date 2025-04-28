(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_brainfuck"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/brainfuck.js":
/*!****************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/brainfuck.js ***!
  \****************************************************************************************************/
/***/ ((module) => {

/*
Language: Brainfuck
Author: Evgeny Stepanischev <imbolk@gmail.com>
Website: https://esolangs.org/wiki/Brainfuck
*/

/** @type LanguageFn */
function brainfuck(hljs) {
  const LITERAL = {
    className: 'literal',
    begin: /[+-]/,
    relevance: 0
  };
  return {
    name: 'Brainfuck',
    aliases: ['bf'],
    contains: [
      hljs.COMMENT(
        '[^\\[\\]\\.,\\+\\-<> \r\n]',
        '[\\[\\]\\.,\\+\\-<> \r\n]',
        {
          returnEnd: true,
          relevance: 0
        }
      ),
      {
        className: 'title',
        begin: '[\\[\\]]',
        relevance: 0
      },
      {
        className: 'string',
        begin: '[\\.,]',
        relevance: 0
      },
      {
        // this mode works as the only relevance counter
        begin: /(?:\+\+|--)/,
        contains: [LITERAL]
      },
      LITERAL
    ]
  };
}

module.exports = brainfuck;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfYnJhaW5mdWNrLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvYnJhaW5mdWNrLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogQnJhaW5mdWNrXG5BdXRob3I6IEV2Z2VueSBTdGVwYW5pc2NoZXYgPGltYm9sa0BnbWFpbC5jb20+XG5XZWJzaXRlOiBodHRwczovL2Vzb2xhbmdzLm9yZy93aWtpL0JyYWluZnVja1xuKi9cblxuLyoqIEB0eXBlIExhbmd1YWdlRm4gKi9cbmZ1bmN0aW9uIGJyYWluZnVjayhobGpzKSB7XG4gIGNvbnN0IExJVEVSQUwgPSB7XG4gICAgY2xhc3NOYW1lOiAnbGl0ZXJhbCcsXG4gICAgYmVnaW46IC9bKy1dLyxcbiAgICByZWxldmFuY2U6IDBcbiAgfTtcbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnQnJhaW5mdWNrJyxcbiAgICBhbGlhc2VzOiBbJ2JmJ10sXG4gICAgY29udGFpbnM6IFtcbiAgICAgIGhsanMuQ09NTUVOVChcbiAgICAgICAgJ1teXFxcXFtcXFxcXVxcXFwuLFxcXFwrXFxcXC08PiBcXHJcXG5dJyxcbiAgICAgICAgJ1tcXFxcW1xcXFxdXFxcXC4sXFxcXCtcXFxcLTw+IFxcclxcbl0nLFxuICAgICAgICB7XG4gICAgICAgICAgcmV0dXJuRW5kOiB0cnVlLFxuICAgICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgICB9XG4gICAgICApLFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICd0aXRsZScsXG4gICAgICAgIGJlZ2luOiAnW1xcXFxbXFxcXF1dJyxcbiAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgICAgICBiZWdpbjogJ1tcXFxcLixdJyxcbiAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICAvLyB0aGlzIG1vZGUgd29ya3MgYXMgdGhlIG9ubHkgcmVsZXZhbmNlIGNvdW50ZXJcbiAgICAgICAgYmVnaW46IC8oPzpcXCtcXCt8LS0pLyxcbiAgICAgICAgY29udGFpbnM6IFtMSVRFUkFMXVxuICAgICAgfSxcbiAgICAgIExJVEVSQUxcbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gYnJhaW5mdWNrO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9