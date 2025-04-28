(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_sml"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/sml.js":
/*!**********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/sml.js ***!
  \**********************************************************************************************/
/***/ ((module) => {

/*
Language: SML (Standard ML)
Author: Edwin Dalorzo <edwin@dalorzo.org>
Description: SML language definition.
Website: https://www.smlnj.org
Origin: ocaml.js
Category: functional
*/
function sml(hljs) {
  return {
    name: 'SML (Standard ML)',
    aliases: [ 'ml' ],
    keywords: {
      $pattern: '[a-z_]\\w*!?',
      keyword:
        /* according to Definition of Standard ML 97  */
        'abstype and andalso as case datatype do else end eqtype ' +
        'exception fn fun functor handle if in include infix infixr ' +
        'let local nonfix of op open orelse raise rec sharing sig ' +
        'signature struct structure then type val with withtype where while',
      built_in:
        /* built-in types according to basis library */
        'array bool char exn int list option order real ref string substring vector unit word',
      literal:
        'true false NONE SOME LESS EQUAL GREATER nil'
    },
    illegal: /\/\/|>>/,
    contains: [
      {
        className: 'literal',
        begin: /\[(\|\|)?\]|\(\)/,
        relevance: 0
      },
      hljs.COMMENT(
        '\\(\\*',
        '\\*\\)',
        {
          contains: [ 'self' ]
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
      { /* don't color identifiers, but safely catch all identifiers with ' */
        begin: '[a-z_]\\w*\'[\\w\']*'
      },
      hljs.inherit(hljs.APOS_STRING_MODE, {
        className: 'string',
        relevance: 0
      }),
      hljs.inherit(hljs.QUOTE_STRING_MODE, {
        illegal: null
      }),
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
        begin: /[-=]>/ // relevance booster
      }
    ]
  };
}

module.exports = sml;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfc21sLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFFBQVE7QUFDUjtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1AsUUFBUTtBQUNSO0FBQ0E7QUFDQSxPQUFPO0FBQ1AsUUFBUTtBQUNSO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUCxRQUFRO0FBQ1I7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL3NtbC5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKlxuTGFuZ3VhZ2U6IFNNTCAoU3RhbmRhcmQgTUwpXG5BdXRob3I6IEVkd2luIERhbG9yem8gPGVkd2luQGRhbG9yem8ub3JnPlxuRGVzY3JpcHRpb246IFNNTCBsYW5ndWFnZSBkZWZpbml0aW9uLlxuV2Vic2l0ZTogaHR0cHM6Ly93d3cuc21sbmoub3JnXG5PcmlnaW46IG9jYW1sLmpzXG5DYXRlZ29yeTogZnVuY3Rpb25hbFxuKi9cbmZ1bmN0aW9uIHNtbChobGpzKSB7XG4gIHJldHVybiB7XG4gICAgbmFtZTogJ1NNTCAoU3RhbmRhcmQgTUwpJyxcbiAgICBhbGlhc2VzOiBbICdtbCcgXSxcbiAgICBrZXl3b3Jkczoge1xuICAgICAgJHBhdHRlcm46ICdbYS16X11cXFxcdyohPycsXG4gICAgICBrZXl3b3JkOlxuICAgICAgICAvKiBhY2NvcmRpbmcgdG8gRGVmaW5pdGlvbiBvZiBTdGFuZGFyZCBNTCA5NyAgKi9cbiAgICAgICAgJ2Fic3R5cGUgYW5kIGFuZGFsc28gYXMgY2FzZSBkYXRhdHlwZSBkbyBlbHNlIGVuZCBlcXR5cGUgJyArXG4gICAgICAgICdleGNlcHRpb24gZm4gZnVuIGZ1bmN0b3IgaGFuZGxlIGlmIGluIGluY2x1ZGUgaW5maXggaW5maXhyICcgK1xuICAgICAgICAnbGV0IGxvY2FsIG5vbmZpeCBvZiBvcCBvcGVuIG9yZWxzZSByYWlzZSByZWMgc2hhcmluZyBzaWcgJyArXG4gICAgICAgICdzaWduYXR1cmUgc3RydWN0IHN0cnVjdHVyZSB0aGVuIHR5cGUgdmFsIHdpdGggd2l0aHR5cGUgd2hlcmUgd2hpbGUnLFxuICAgICAgYnVpbHRfaW46XG4gICAgICAgIC8qIGJ1aWx0LWluIHR5cGVzIGFjY29yZGluZyB0byBiYXNpcyBsaWJyYXJ5ICovXG4gICAgICAgICdhcnJheSBib29sIGNoYXIgZXhuIGludCBsaXN0IG9wdGlvbiBvcmRlciByZWFsIHJlZiBzdHJpbmcgc3Vic3RyaW5nIHZlY3RvciB1bml0IHdvcmQnLFxuICAgICAgbGl0ZXJhbDpcbiAgICAgICAgJ3RydWUgZmFsc2UgTk9ORSBTT01FIExFU1MgRVFVQUwgR1JFQVRFUiBuaWwnXG4gICAgfSxcbiAgICBpbGxlZ2FsOiAvXFwvXFwvfD4+LyxcbiAgICBjb250YWluczogW1xuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdsaXRlcmFsJyxcbiAgICAgICAgYmVnaW46IC9cXFsoXFx8XFx8KT9cXF18XFwoXFwpLyxcbiAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICB9LFxuICAgICAgaGxqcy5DT01NRU5UKFxuICAgICAgICAnXFxcXChcXFxcKicsXG4gICAgICAgICdcXFxcKlxcXFwpJyxcbiAgICAgICAge1xuICAgICAgICAgIGNvbnRhaW5zOiBbICdzZWxmJyBdXG4gICAgICAgIH1cbiAgICAgICksXG4gICAgICB7IC8qIHR5cGUgdmFyaWFibGUgKi9cbiAgICAgICAgY2xhc3NOYW1lOiAnc3ltYm9sJyxcbiAgICAgICAgYmVnaW46ICdcXCdbQS1aYS16X10oPyFcXCcpW1xcXFx3XFwnXSonXG4gICAgICAgIC8qIHRoZSBncmFtbWFyIGlzIGFtYmlndW91cyBvbiBob3cgJ2EnYiBzaG91bGQgYmUgaW50ZXJwcmV0ZWQgYnV0IG5vdCB0aGUgY29tcGlsZXIgKi9cbiAgICAgIH0sXG4gICAgICB7IC8qIHBvbHltb3JwaGljIHZhcmlhbnQgKi9cbiAgICAgICAgY2xhc3NOYW1lOiAndHlwZScsXG4gICAgICAgIGJlZ2luOiAnYFtBLVpdW1xcXFx3XFwnXSonXG4gICAgICB9LFxuICAgICAgeyAvKiBtb2R1bGUgb3IgY29uc3RydWN0b3IgKi9cbiAgICAgICAgY2xhc3NOYW1lOiAndHlwZScsXG4gICAgICAgIGJlZ2luOiAnXFxcXGJbQS1aXVtcXFxcd1xcJ10qJyxcbiAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICB9LFxuICAgICAgeyAvKiBkb24ndCBjb2xvciBpZGVudGlmaWVycywgYnV0IHNhZmVseSBjYXRjaCBhbGwgaWRlbnRpZmllcnMgd2l0aCAnICovXG4gICAgICAgIGJlZ2luOiAnW2Etel9dXFxcXHcqXFwnW1xcXFx3XFwnXSonXG4gICAgICB9LFxuICAgICAgaGxqcy5pbmhlcml0KGhsanMuQVBPU19TVFJJTkdfTU9ERSwge1xuICAgICAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH0pLFxuICAgICAgaGxqcy5pbmhlcml0KGhsanMuUVVPVEVfU1RSSU5HX01PREUsIHtcbiAgICAgICAgaWxsZWdhbDogbnVsbFxuICAgICAgfSksXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ251bWJlcicsXG4gICAgICAgIGJlZ2luOlxuICAgICAgICAgICdcXFxcYigwW3hYXVthLWZBLUYwLTlfXStbTGxuXT98JyArXG4gICAgICAgICAgJzBbb09dWzAtN19dK1tMbG5dP3wnICtcbiAgICAgICAgICAnMFtiQl1bMDFfXStbTGxuXT98JyArXG4gICAgICAgICAgJ1swLTldWzAtOV9dKihbTGxuXXwoXFxcXC5bMC05X10qKT8oW2VFXVstK10/WzAtOV9dKyk/KT8pJyxcbiAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogL1stPV0+LyAvLyByZWxldmFuY2UgYm9vc3RlclxuICAgICAgfVxuICAgIF1cbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBzbWw7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=