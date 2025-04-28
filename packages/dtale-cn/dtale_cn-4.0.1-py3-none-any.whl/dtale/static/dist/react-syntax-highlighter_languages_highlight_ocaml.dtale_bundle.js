(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_ocaml"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/ocaml.js":
/*!************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/ocaml.js ***!
  \************************************************************************************************/
/***/ ((module) => {

/*
Language: OCaml
Author: Mehdi Dogguy <mehdi@dogguy.org>
Contributors: Nicolas Braud-Santoni <nicolas.braud-santoni@ens-cachan.fr>, Mickael Delahaye <mickael.delahaye@gmail.com>
Description: OCaml language definition.
Website: https://ocaml.org
Category: functional
*/

function ocaml(hljs) {
  /* missing support for heredoc-like string (OCaml 4.0.2+) */
  return {
    name: 'OCaml',
    aliases: ['ml'],
    keywords: {
      $pattern: '[a-z_]\\w*!?',
      keyword:
        'and as assert asr begin class constraint do done downto else end ' +
        'exception external for fun function functor if in include ' +
        'inherit! inherit initializer land lazy let lor lsl lsr lxor match method!|10 method ' +
        'mod module mutable new object of open! open or private rec sig struct ' +
        'then to try type val! val virtual when while with ' +
        /* camlp4 */
        'parser value',
      built_in:
        /* built-in types */
        'array bool bytes char exn|5 float int int32 int64 list lazy_t|5 nativeint|5 string unit ' +
        /* (some) types in Pervasives */
        'in_channel out_channel ref',
      literal:
        'true false'
    },
    illegal: /\/\/|>>/,
    contains: [
      {
        className: 'literal',
        begin: '\\[(\\|\\|)?\\]|\\(\\)',
        relevance: 0
      },
      hljs.COMMENT(
        '\\(\\*',
        '\\*\\)',
        {
          contains: ['self']
        }
      ),
      { /* type variable */
        className: 'symbol',
        begin: '\'[A-Za-z_](?!\')[\\w\']*'
        /* the grammar is ambiguous on how 'a'b should be interpreted but not the compiler */
      },
      { /* polymorphic variant */
        className: 'type',
        begin: '`[A-Z][\\w\']*'
      },
      { /* module or constructor */
        className: 'type',
        begin: '\\b[A-Z][\\w\']*',
        relevance: 0
      },
      { /* don't color identifiers, but safely catch all identifiers with '*/
        begin: '[a-z_]\\w*\'[\\w\']*', relevance: 0
      },
      hljs.inherit(hljs.APOS_STRING_MODE, {className: 'string', relevance: 0}),
      hljs.inherit(hljs.QUOTE_STRING_MODE, {illegal: null}),
      {
        className: 'number',
        begin:
          '\\b(0[xX][a-fA-F0-9_]+[Lln]?|' +
          '0[oO][0-7_]+[Lln]?|' +
          '0[bB][01_]+[Lln]?|' +
          '[0-9][0-9_]*([Lln]|(\\.[0-9_]*)?([eE][-+]?[0-9_]+)?)?)',
        relevance: 0
      },
      {
        begin: /->/ // relevance booster
      }
    ]
  }
}

module.exports = ocaml;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfb2NhbWwuZHRhbGVfYnVuZGxlLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxRQUFRO0FBQ1I7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQLFFBQVE7QUFDUjtBQUNBO0FBQ0EsT0FBTztBQUNQLFFBQVE7QUFDUjtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1AsUUFBUTtBQUNSO0FBQ0EsT0FBTztBQUNQLDJDQUEyQyxrQ0FBa0M7QUFDN0UsNENBQTRDLGNBQWM7QUFDMUQ7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL29jYW1sLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogT0NhbWxcbkF1dGhvcjogTWVoZGkgRG9nZ3V5IDxtZWhkaUBkb2dndXkub3JnPlxuQ29udHJpYnV0b3JzOiBOaWNvbGFzIEJyYXVkLVNhbnRvbmkgPG5pY29sYXMuYnJhdWQtc2FudG9uaUBlbnMtY2FjaGFuLmZyPiwgTWlja2FlbCBEZWxhaGF5ZSA8bWlja2FlbC5kZWxhaGF5ZUBnbWFpbC5jb20+XG5EZXNjcmlwdGlvbjogT0NhbWwgbGFuZ3VhZ2UgZGVmaW5pdGlvbi5cbldlYnNpdGU6IGh0dHBzOi8vb2NhbWwub3JnXG5DYXRlZ29yeTogZnVuY3Rpb25hbFxuKi9cblxuZnVuY3Rpb24gb2NhbWwoaGxqcykge1xuICAvKiBtaXNzaW5nIHN1cHBvcnQgZm9yIGhlcmVkb2MtbGlrZSBzdHJpbmcgKE9DYW1sIDQuMC4yKykgKi9cbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnT0NhbWwnLFxuICAgIGFsaWFzZXM6IFsnbWwnXSxcbiAgICBrZXl3b3Jkczoge1xuICAgICAgJHBhdHRlcm46ICdbYS16X11cXFxcdyohPycsXG4gICAgICBrZXl3b3JkOlxuICAgICAgICAnYW5kIGFzIGFzc2VydCBhc3IgYmVnaW4gY2xhc3MgY29uc3RyYWludCBkbyBkb25lIGRvd250byBlbHNlIGVuZCAnICtcbiAgICAgICAgJ2V4Y2VwdGlvbiBleHRlcm5hbCBmb3IgZnVuIGZ1bmN0aW9uIGZ1bmN0b3IgaWYgaW4gaW5jbHVkZSAnICtcbiAgICAgICAgJ2luaGVyaXQhIGluaGVyaXQgaW5pdGlhbGl6ZXIgbGFuZCBsYXp5IGxldCBsb3IgbHNsIGxzciBseG9yIG1hdGNoIG1ldGhvZCF8MTAgbWV0aG9kICcgK1xuICAgICAgICAnbW9kIG1vZHVsZSBtdXRhYmxlIG5ldyBvYmplY3Qgb2Ygb3BlbiEgb3BlbiBvciBwcml2YXRlIHJlYyBzaWcgc3RydWN0ICcgK1xuICAgICAgICAndGhlbiB0byB0cnkgdHlwZSB2YWwhIHZhbCB2aXJ0dWFsIHdoZW4gd2hpbGUgd2l0aCAnICtcbiAgICAgICAgLyogY2FtbHA0ICovXG4gICAgICAgICdwYXJzZXIgdmFsdWUnLFxuICAgICAgYnVpbHRfaW46XG4gICAgICAgIC8qIGJ1aWx0LWluIHR5cGVzICovXG4gICAgICAgICdhcnJheSBib29sIGJ5dGVzIGNoYXIgZXhufDUgZmxvYXQgaW50IGludDMyIGludDY0IGxpc3QgbGF6eV90fDUgbmF0aXZlaW50fDUgc3RyaW5nIHVuaXQgJyArXG4gICAgICAgIC8qIChzb21lKSB0eXBlcyBpbiBQZXJ2YXNpdmVzICovXG4gICAgICAgICdpbl9jaGFubmVsIG91dF9jaGFubmVsIHJlZicsXG4gICAgICBsaXRlcmFsOlxuICAgICAgICAndHJ1ZSBmYWxzZSdcbiAgICB9LFxuICAgIGlsbGVnYWw6IC9cXC9cXC98Pj4vLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ2xpdGVyYWwnLFxuICAgICAgICBiZWdpbjogJ1xcXFxbKFxcXFx8XFxcXHwpP1xcXFxdfFxcXFwoXFxcXCknLFxuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH0sXG4gICAgICBobGpzLkNPTU1FTlQoXG4gICAgICAgICdcXFxcKFxcXFwqJyxcbiAgICAgICAgJ1xcXFwqXFxcXCknLFxuICAgICAgICB7XG4gICAgICAgICAgY29udGFpbnM6IFsnc2VsZiddXG4gICAgICAgIH1cbiAgICAgICksXG4gICAgICB7IC8qIHR5cGUgdmFyaWFibGUgKi9cbiAgICAgICAgY2xhc3NOYW1lOiAnc3ltYm9sJyxcbiAgICAgICAgYmVnaW46ICdcXCdbQS1aYS16X10oPyFcXCcpW1xcXFx3XFwnXSonXG4gICAgICAgIC8qIHRoZSBncmFtbWFyIGlzIGFtYmlndW91cyBvbiBob3cgJ2EnYiBzaG91bGQgYmUgaW50ZXJwcmV0ZWQgYnV0IG5vdCB0aGUgY29tcGlsZXIgKi9cbiAgICAgIH0sXG4gICAgICB7IC8qIHBvbHltb3JwaGljIHZhcmlhbnQgKi9cbiAgICAgICAgY2xhc3NOYW1lOiAndHlwZScsXG4gICAgICAgIGJlZ2luOiAnYFtBLVpdW1xcXFx3XFwnXSonXG4gICAgICB9LFxuICAgICAgeyAvKiBtb2R1bGUgb3IgY29uc3RydWN0b3IgKi9cbiAgICAgICAgY2xhc3NOYW1lOiAndHlwZScsXG4gICAgICAgIGJlZ2luOiAnXFxcXGJbQS1aXVtcXFxcd1xcJ10qJyxcbiAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICB9LFxuICAgICAgeyAvKiBkb24ndCBjb2xvciBpZGVudGlmaWVycywgYnV0IHNhZmVseSBjYXRjaCBhbGwgaWRlbnRpZmllcnMgd2l0aCAnKi9cbiAgICAgICAgYmVnaW46ICdbYS16X11cXFxcdypcXCdbXFxcXHdcXCddKicsIHJlbGV2YW5jZTogMFxuICAgICAgfSxcbiAgICAgIGhsanMuaW5oZXJpdChobGpzLkFQT1NfU1RSSU5HX01PREUsIHtjbGFzc05hbWU6ICdzdHJpbmcnLCByZWxldmFuY2U6IDB9KSxcbiAgICAgIGhsanMuaW5oZXJpdChobGpzLlFVT1RFX1NUUklOR19NT0RFLCB7aWxsZWdhbDogbnVsbH0pLFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdudW1iZXInLFxuICAgICAgICBiZWdpbjpcbiAgICAgICAgICAnXFxcXGIoMFt4WF1bYS1mQS1GMC05X10rW0xsbl0/fCcgK1xuICAgICAgICAgICcwW29PXVswLTdfXStbTGxuXT98JyArXG4gICAgICAgICAgJzBbYkJdWzAxX10rW0xsbl0/fCcgK1xuICAgICAgICAgICdbMC05XVswLTlfXSooW0xsbl18KFxcXFwuWzAtOV9dKik/KFtlRV1bLStdP1swLTlfXSspPyk/KScsXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC8tPi8gLy8gcmVsZXZhbmNlIGJvb3N0ZXJcbiAgICAgIH1cbiAgICBdXG4gIH1cbn1cblxubW9kdWxlLmV4cG9ydHMgPSBvY2FtbDtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==