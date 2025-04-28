(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_fsharp"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/fsharp.js":
/*!*************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/fsharp.js ***!
  \*************************************************************************************************/
/***/ ((module) => {

/*
Language: F#
Author: Jonas Follesø <jonas@follesoe.no>
Contributors: Troy Kershaw <hello@troykershaw.com>, Henrik Feldt <henrik@haf.se>
Website: https://docs.microsoft.com/en-us/dotnet/fsharp/
Category: functional
*/

/** @type LanguageFn */
function fsharp(hljs) {
  const TYPEPARAM = {
    begin: '<',
    end: '>',
    contains: [
      hljs.inherit(hljs.TITLE_MODE, {
        begin: /'[a-zA-Z0-9_]+/
      })
    ]
  };

  return {
    name: 'F#',
    aliases: ['fs'],
    keywords:
      'abstract and as assert base begin class default delegate do done ' +
      'downcast downto elif else end exception extern false finally for ' +
      'fun function global if in inherit inline interface internal lazy let ' +
      'match member module mutable namespace new null of open or ' +
      'override private public rec return sig static struct then to ' +
      'true try type upcast use val void when while with yield',
    illegal: /\/\*/,
    contains: [
      {
        // monad builder keywords (matches before non-bang kws)
        className: 'keyword',
        begin: /\b(yield|return|let|do)!/
      },
      {
        className: 'string',
        begin: '@"',
        end: '"',
        contains: [
          {
            begin: '""'
          }
        ]
      },
      {
        className: 'string',
        begin: '"""',
        end: '"""'
      },
      hljs.COMMENT('\\(\\*(\\s)', '\\*\\)', {
        contains: ["self"]
      }),
      {
        className: 'class',
        beginKeywords: 'type',
        end: '\\(|=|$',
        excludeEnd: true,
        contains: [
          hljs.UNDERSCORE_TITLE_MODE,
          TYPEPARAM
        ]
      },
      {
        className: 'meta',
        begin: '\\[<',
        end: '>\\]',
        relevance: 10
      },
      {
        className: 'symbol',
        begin: '\\B(\'[A-Za-z])\\b',
        contains: [hljs.BACKSLASH_ESCAPE]
      },
      hljs.C_LINE_COMMENT_MODE,
      hljs.inherit(hljs.QUOTE_STRING_MODE, {
        illegal: null
      }),
      hljs.C_NUMBER_MODE
    ]
  };
}

module.exports = fsharp;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfZnNoYXJwLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL2ZzaGFycC5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKlxuTGFuZ3VhZ2U6IEYjXG5BdXRob3I6IEpvbmFzIEZvbGxlc8O4IDxqb25hc0Bmb2xsZXNvZS5ubz5cbkNvbnRyaWJ1dG9yczogVHJveSBLZXJzaGF3IDxoZWxsb0B0cm95a2Vyc2hhdy5jb20+LCBIZW5yaWsgRmVsZHQgPGhlbnJpa0BoYWYuc2U+XG5XZWJzaXRlOiBodHRwczovL2RvY3MubWljcm9zb2Z0LmNvbS9lbi11cy9kb3RuZXQvZnNoYXJwL1xuQ2F0ZWdvcnk6IGZ1bmN0aW9uYWxcbiovXG5cbi8qKiBAdHlwZSBMYW5ndWFnZUZuICovXG5mdW5jdGlvbiBmc2hhcnAoaGxqcykge1xuICBjb25zdCBUWVBFUEFSQU0gPSB7XG4gICAgYmVnaW46ICc8JyxcbiAgICBlbmQ6ICc+JyxcbiAgICBjb250YWluczogW1xuICAgICAgaGxqcy5pbmhlcml0KGhsanMuVElUTEVfTU9ERSwge1xuICAgICAgICBiZWdpbjogLydbYS16QS1aMC05X10rL1xuICAgICAgfSlcbiAgICBdXG4gIH07XG5cbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnRiMnLFxuICAgIGFsaWFzZXM6IFsnZnMnXSxcbiAgICBrZXl3b3JkczpcbiAgICAgICdhYnN0cmFjdCBhbmQgYXMgYXNzZXJ0IGJhc2UgYmVnaW4gY2xhc3MgZGVmYXVsdCBkZWxlZ2F0ZSBkbyBkb25lICcgK1xuICAgICAgJ2Rvd25jYXN0IGRvd250byBlbGlmIGVsc2UgZW5kIGV4Y2VwdGlvbiBleHRlcm4gZmFsc2UgZmluYWxseSBmb3IgJyArXG4gICAgICAnZnVuIGZ1bmN0aW9uIGdsb2JhbCBpZiBpbiBpbmhlcml0IGlubGluZSBpbnRlcmZhY2UgaW50ZXJuYWwgbGF6eSBsZXQgJyArXG4gICAgICAnbWF0Y2ggbWVtYmVyIG1vZHVsZSBtdXRhYmxlIG5hbWVzcGFjZSBuZXcgbnVsbCBvZiBvcGVuIG9yICcgK1xuICAgICAgJ292ZXJyaWRlIHByaXZhdGUgcHVibGljIHJlYyByZXR1cm4gc2lnIHN0YXRpYyBzdHJ1Y3QgdGhlbiB0byAnICtcbiAgICAgICd0cnVlIHRyeSB0eXBlIHVwY2FzdCB1c2UgdmFsIHZvaWQgd2hlbiB3aGlsZSB3aXRoIHlpZWxkJyxcbiAgICBpbGxlZ2FsOiAvXFwvXFwqLyxcbiAgICBjb250YWluczogW1xuICAgICAge1xuICAgICAgICAvLyBtb25hZCBidWlsZGVyIGtleXdvcmRzIChtYXRjaGVzIGJlZm9yZSBub24tYmFuZyBrd3MpXG4gICAgICAgIGNsYXNzTmFtZTogJ2tleXdvcmQnLFxuICAgICAgICBiZWdpbjogL1xcYih5aWVsZHxyZXR1cm58bGV0fGRvKSEvXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgICAgICBiZWdpbjogJ0BcIicsXG4gICAgICAgIGVuZDogJ1wiJyxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbjogJ1wiXCInXG4gICAgICAgICAgfVxuICAgICAgICBdXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgICAgICBiZWdpbjogJ1wiXCJcIicsXG4gICAgICAgIGVuZDogJ1wiXCJcIidcbiAgICAgIH0sXG4gICAgICBobGpzLkNPTU1FTlQoJ1xcXFwoXFxcXCooXFxcXHMpJywgJ1xcXFwqXFxcXCknLCB7XG4gICAgICAgIGNvbnRhaW5zOiBbXCJzZWxmXCJdXG4gICAgICB9KSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnY2xhc3MnLFxuICAgICAgICBiZWdpbktleXdvcmRzOiAndHlwZScsXG4gICAgICAgIGVuZDogJ1xcXFwofD18JCcsXG4gICAgICAgIGV4Y2x1ZGVFbmQ6IHRydWUsXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgaGxqcy5VTkRFUlNDT1JFX1RJVExFX01PREUsXG4gICAgICAgICAgVFlQRVBBUkFNXG4gICAgICAgIF1cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ21ldGEnLFxuICAgICAgICBiZWdpbjogJ1xcXFxbPCcsXG4gICAgICAgIGVuZDogJz5cXFxcXScsXG4gICAgICAgIHJlbGV2YW5jZTogMTBcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3N5bWJvbCcsXG4gICAgICAgIGJlZ2luOiAnXFxcXEIoXFwnW0EtWmEtel0pXFxcXGInLFxuICAgICAgICBjb250YWluczogW2hsanMuQkFDS1NMQVNIX0VTQ0FQRV1cbiAgICAgIH0sXG4gICAgICBobGpzLkNfTElORV9DT01NRU5UX01PREUsXG4gICAgICBobGpzLmluaGVyaXQoaGxqcy5RVU9URV9TVFJJTkdfTU9ERSwge1xuICAgICAgICBpbGxlZ2FsOiBudWxsXG4gICAgICB9KSxcbiAgICAgIGhsanMuQ19OVU1CRVJfTU9ERVxuICAgIF1cbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBmc2hhcnA7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=