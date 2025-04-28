(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_clean"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/clean.js":
/*!************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/clean.js ***!
  \************************************************************************************************/
/***/ ((module) => {

/*
Language: Clean
Author: Camil Staps <info@camilstaps.nl>
Category: functional
Website: http://clean.cs.ru.nl
*/

/** @type LanguageFn */
function clean(hljs) {
  return {
    name: 'Clean',
    aliases: [
      'icl',
      'dcl'
    ],
    keywords: {
      keyword:
        'if let in with where case of class instance otherwise ' +
        'implementation definition system module from import qualified as ' +
        'special code inline foreign export ccall stdcall generic derive ' +
        'infix infixl infixr',
      built_in:
        'Int Real Char Bool',
      literal:
        'True False'
    },
    contains: [
      hljs.C_LINE_COMMENT_MODE,
      hljs.C_BLOCK_COMMENT_MODE,
      hljs.APOS_STRING_MODE,
      hljs.QUOTE_STRING_MODE,
      hljs.C_NUMBER_MODE,
      { // relevance booster
        begin: '->|<-[|:]?|#!?|>>=|\\{\\||\\|\\}|:==|=:|<>'
      }
    ]
  };
}

module.exports = clean;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfY2xlYW4uZHRhbGVfYnVuZGxlLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxRQUFRO0FBQ1Isc0NBQXNDLFVBQVU7QUFDaEQ7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL2NsZWFuLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogQ2xlYW5cbkF1dGhvcjogQ2FtaWwgU3RhcHMgPGluZm9AY2FtaWxzdGFwcy5ubD5cbkNhdGVnb3J5OiBmdW5jdGlvbmFsXG5XZWJzaXRlOiBodHRwOi8vY2xlYW4uY3MucnUubmxcbiovXG5cbi8qKiBAdHlwZSBMYW5ndWFnZUZuICovXG5mdW5jdGlvbiBjbGVhbihobGpzKSB7XG4gIHJldHVybiB7XG4gICAgbmFtZTogJ0NsZWFuJyxcbiAgICBhbGlhc2VzOiBbXG4gICAgICAnaWNsJyxcbiAgICAgICdkY2wnXG4gICAgXSxcbiAgICBrZXl3b3Jkczoge1xuICAgICAga2V5d29yZDpcbiAgICAgICAgJ2lmIGxldCBpbiB3aXRoIHdoZXJlIGNhc2Ugb2YgY2xhc3MgaW5zdGFuY2Ugb3RoZXJ3aXNlICcgK1xuICAgICAgICAnaW1wbGVtZW50YXRpb24gZGVmaW5pdGlvbiBzeXN0ZW0gbW9kdWxlIGZyb20gaW1wb3J0IHF1YWxpZmllZCBhcyAnICtcbiAgICAgICAgJ3NwZWNpYWwgY29kZSBpbmxpbmUgZm9yZWlnbiBleHBvcnQgY2NhbGwgc3RkY2FsbCBnZW5lcmljIGRlcml2ZSAnICtcbiAgICAgICAgJ2luZml4IGluZml4bCBpbmZpeHInLFxuICAgICAgYnVpbHRfaW46XG4gICAgICAgICdJbnQgUmVhbCBDaGFyIEJvb2wnLFxuICAgICAgbGl0ZXJhbDpcbiAgICAgICAgJ1RydWUgRmFsc2UnXG4gICAgfSxcbiAgICBjb250YWluczogW1xuICAgICAgaGxqcy5DX0xJTkVfQ09NTUVOVF9NT0RFLFxuICAgICAgaGxqcy5DX0JMT0NLX0NPTU1FTlRfTU9ERSxcbiAgICAgIGhsanMuQVBPU19TVFJJTkdfTU9ERSxcbiAgICAgIGhsanMuUVVPVEVfU1RSSU5HX01PREUsXG4gICAgICBobGpzLkNfTlVNQkVSX01PREUsXG4gICAgICB7IC8vIHJlbGV2YW5jZSBib29zdGVyXG4gICAgICAgIGJlZ2luOiAnLT58PC1bfDpdP3wjIT98Pj49fFxcXFx7XFxcXHx8XFxcXHxcXFxcfXw6PT18PTp8PD4nXG4gICAgICB9XG4gICAgXVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IGNsZWFuO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9