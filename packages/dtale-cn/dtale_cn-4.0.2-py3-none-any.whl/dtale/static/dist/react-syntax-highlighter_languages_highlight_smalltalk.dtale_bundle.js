(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_smalltalk"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/smalltalk.js":
/*!****************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/smalltalk.js ***!
  \****************************************************************************************************/
/***/ ((module) => {

/*
Language: Smalltalk
Description: Smalltalk is an object-oriented, dynamically typed reflective programming language.
Author: Vladimir Gubarkov <xonixx@gmail.com>
Website: https://en.wikipedia.org/wiki/Smalltalk
*/

function smalltalk(hljs) {
  const VAR_IDENT_RE = '[a-z][a-zA-Z0-9_]*';
  const CHAR = {
    className: 'string',
    begin: '\\$.{1}'
  };
  const SYMBOL = {
    className: 'symbol',
    begin: '#' + hljs.UNDERSCORE_IDENT_RE
  };
  return {
    name: 'Smalltalk',
    aliases: [ 'st' ],
    keywords: 'self super nil true false thisContext', // only 6
    contains: [
      hljs.COMMENT('"', '"'),
      hljs.APOS_STRING_MODE,
      {
        className: 'type',
        begin: '\\b[A-Z][A-Za-z0-9_]*',
        relevance: 0
      },
      {
        begin: VAR_IDENT_RE + ':',
        relevance: 0
      },
      hljs.C_NUMBER_MODE,
      SYMBOL,
      CHAR,
      {
        // This looks more complicated than needed to avoid combinatorial
        // explosion under V8. It effectively means `| var1 var2 ... |` with
        // whitespace adjacent to `|` being optional.
        begin: '\\|[ ]*' + VAR_IDENT_RE + '([ ]+' + VAR_IDENT_RE + ')*[ ]*\\|',
        returnBegin: true,
        end: /\|/,
        illegal: /\S/,
        contains: [ {
          begin: '(\\|[ ]*)?' + VAR_IDENT_RE
        } ]
      },
      {
        begin: '#\\(',
        end: '\\)',
        contains: [
          hljs.APOS_STRING_MODE,
          CHAR,
          hljs.C_NUMBER_MODE,
          SYMBOL
        ]
      }
    ]
  };
}

module.exports = smalltalk;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfc21hbGx0YWxrLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLGlCQUFpQixFQUFFO0FBQ25CO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFVBQVU7QUFDVixPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL3NtYWxsdGFsay5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKlxuTGFuZ3VhZ2U6IFNtYWxsdGFsa1xuRGVzY3JpcHRpb246IFNtYWxsdGFsayBpcyBhbiBvYmplY3Qtb3JpZW50ZWQsIGR5bmFtaWNhbGx5IHR5cGVkIHJlZmxlY3RpdmUgcHJvZ3JhbW1pbmcgbGFuZ3VhZ2UuXG5BdXRob3I6IFZsYWRpbWlyIEd1YmFya292IDx4b25peHhAZ21haWwuY29tPlxuV2Vic2l0ZTogaHR0cHM6Ly9lbi53aWtpcGVkaWEub3JnL3dpa2kvU21hbGx0YWxrXG4qL1xuXG5mdW5jdGlvbiBzbWFsbHRhbGsoaGxqcykge1xuICBjb25zdCBWQVJfSURFTlRfUkUgPSAnW2Etel1bYS16QS1aMC05X10qJztcbiAgY29uc3QgQ0hBUiA9IHtcbiAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgIGJlZ2luOiAnXFxcXCQuezF9J1xuICB9O1xuICBjb25zdCBTWU1CT0wgPSB7XG4gICAgY2xhc3NOYW1lOiAnc3ltYm9sJyxcbiAgICBiZWdpbjogJyMnICsgaGxqcy5VTkRFUlNDT1JFX0lERU5UX1JFXG4gIH07XG4gIHJldHVybiB7XG4gICAgbmFtZTogJ1NtYWxsdGFsaycsXG4gICAgYWxpYXNlczogWyAnc3QnIF0sXG4gICAga2V5d29yZHM6ICdzZWxmIHN1cGVyIG5pbCB0cnVlIGZhbHNlIHRoaXNDb250ZXh0JywgLy8gb25seSA2XG4gICAgY29udGFpbnM6IFtcbiAgICAgIGhsanMuQ09NTUVOVCgnXCInLCAnXCInKSxcbiAgICAgIGhsanMuQVBPU19TVFJJTkdfTU9ERSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAndHlwZScsXG4gICAgICAgIGJlZ2luOiAnXFxcXGJbQS1aXVtBLVphLXowLTlfXSonLFxuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiBWQVJfSURFTlRfUkUgKyAnOicsXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfSxcbiAgICAgIGhsanMuQ19OVU1CRVJfTU9ERSxcbiAgICAgIFNZTUJPTCxcbiAgICAgIENIQVIsXG4gICAgICB7XG4gICAgICAgIC8vIFRoaXMgbG9va3MgbW9yZSBjb21wbGljYXRlZCB0aGFuIG5lZWRlZCB0byBhdm9pZCBjb21iaW5hdG9yaWFsXG4gICAgICAgIC8vIGV4cGxvc2lvbiB1bmRlciBWOC4gSXQgZWZmZWN0aXZlbHkgbWVhbnMgYHwgdmFyMSB2YXIyIC4uLiB8YCB3aXRoXG4gICAgICAgIC8vIHdoaXRlc3BhY2UgYWRqYWNlbnQgdG8gYHxgIGJlaW5nIG9wdGlvbmFsLlxuICAgICAgICBiZWdpbjogJ1xcXFx8WyBdKicgKyBWQVJfSURFTlRfUkUgKyAnKFsgXSsnICsgVkFSX0lERU5UX1JFICsgJykqWyBdKlxcXFx8JyxcbiAgICAgICAgcmV0dXJuQmVnaW46IHRydWUsXG4gICAgICAgIGVuZDogL1xcfC8sXG4gICAgICAgIGlsbGVnYWw6IC9cXFMvLFxuICAgICAgICBjb250YWluczogWyB7XG4gICAgICAgICAgYmVnaW46ICcoXFxcXHxbIF0qKT8nICsgVkFSX0lERU5UX1JFXG4gICAgICAgIH0gXVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICcjXFxcXCgnLFxuICAgICAgICBlbmQ6ICdcXFxcKScsXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgaGxqcy5BUE9TX1NUUklOR19NT0RFLFxuICAgICAgICAgIENIQVIsXG4gICAgICAgICAgaGxqcy5DX05VTUJFUl9NT0RFLFxuICAgICAgICAgIFNZTUJPTFxuICAgICAgICBdXG4gICAgICB9XG4gICAgXVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IHNtYWxsdGFsaztcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==