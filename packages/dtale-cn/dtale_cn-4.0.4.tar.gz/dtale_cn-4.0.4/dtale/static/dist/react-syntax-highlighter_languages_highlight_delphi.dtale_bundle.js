(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_delphi"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/delphi.js":
/*!*************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/delphi.js ***!
  \*************************************************************************************************/
/***/ ((module) => {

/*
Language: Delphi
Website: https://www.embarcadero.com/products/delphi
*/

/** @type LanguageFn */
function delphi(hljs) {
  const KEYWORDS =
    'exports register file shl array record property for mod while set ally label uses raise not ' +
    'stored class safecall var interface or private static exit index inherited to else stdcall ' +
    'override shr asm far resourcestring finalization packed virtual out and protected library do ' +
    'xorwrite goto near function end div overload object unit begin string on inline repeat until ' +
    'destructor write message program with read initialization except default nil if case cdecl in ' +
    'downto threadvar of try pascal const external constructor type public then implementation ' +
    'finally published procedure absolute reintroduce operator as is abstract alias assembler ' +
    'bitpacked break continue cppdecl cvar enumerator experimental platform deprecated ' +
    'unimplemented dynamic export far16 forward generic helper implements interrupt iochecks ' +
    'local name nodefault noreturn nostackframe oldfpccall otherwise saveregisters softfloat ' +
    'specialize strict unaligned varargs ';
  const COMMENT_MODES = [
    hljs.C_LINE_COMMENT_MODE,
    hljs.COMMENT(/\{/, /\}/, {
      relevance: 0
    }),
    hljs.COMMENT(/\(\*/, /\*\)/, {
      relevance: 10
    })
  ];
  const DIRECTIVE = {
    className: 'meta',
    variants: [
      {
        begin: /\{\$/,
        end: /\}/
      },
      {
        begin: /\(\*\$/,
        end: /\*\)/
      }
    ]
  };
  const STRING = {
    className: 'string',
    begin: /'/,
    end: /'/,
    contains: [{
      begin: /''/
    }]
  };
  const NUMBER = {
    className: 'number',
    relevance: 0,
    // Source: https://www.freepascal.org/docs-html/ref/refse6.html
    variants: [
      {
        // Hexadecimal notation, e.g., $7F.
        begin: '\\$[0-9A-Fa-f]+'
      },
      {
        // Octal notation, e.g., &42.
        begin: '&[0-7]+'
      },
      {
        // Binary notation, e.g., %1010.
        begin: '%[01]+'
      }
    ]
  };
  const CHAR_STRING = {
    className: 'string',
    begin: /(#\d+)+/
  };
  const CLASS = {
    begin: hljs.IDENT_RE + '\\s*=\\s*class\\s*\\(',
    returnBegin: true,
    contains: [hljs.TITLE_MODE]
  };
  const FUNCTION = {
    className: 'function',
    beginKeywords: 'function constructor destructor procedure',
    end: /[:;]/,
    keywords: 'function constructor|10 destructor|10 procedure|10',
    contains: [
      hljs.TITLE_MODE,
      {
        className: 'params',
        begin: /\(/,
        end: /\)/,
        keywords: KEYWORDS,
        contains: [
          STRING,
          CHAR_STRING,
          DIRECTIVE
        ].concat(COMMENT_MODES)
      },
      DIRECTIVE
    ].concat(COMMENT_MODES)
  };
  return {
    name: 'Delphi',
    aliases: [
      'dpr',
      'dfm',
      'pas',
      'pascal',
      'freepascal',
      'lazarus',
      'lpr',
      'lfm'
    ],
    case_insensitive: true,
    keywords: KEYWORDS,
    illegal: /"|\$[G-Zg-z]|\/\*|<\/|\|/,
    contains: [
      STRING,
      CHAR_STRING,
      hljs.NUMBER_MODE,
      NUMBER,
      CLASS,
      FUNCTION,
      DIRECTIVE
    ].concat(COMMENT_MODES)
  };
}

module.exports = delphi;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfZGVscGhpLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0Esb0JBQW9CLE1BQU07QUFDMUI7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0Esa0JBQWtCO0FBQ2xCLGdCQUFnQjtBQUNoQixPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL2RlbHBoaS5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKlxuTGFuZ3VhZ2U6IERlbHBoaVxuV2Vic2l0ZTogaHR0cHM6Ly93d3cuZW1iYXJjYWRlcm8uY29tL3Byb2R1Y3RzL2RlbHBoaVxuKi9cblxuLyoqIEB0eXBlIExhbmd1YWdlRm4gKi9cbmZ1bmN0aW9uIGRlbHBoaShobGpzKSB7XG4gIGNvbnN0IEtFWVdPUkRTID1cbiAgICAnZXhwb3J0cyByZWdpc3RlciBmaWxlIHNobCBhcnJheSByZWNvcmQgcHJvcGVydHkgZm9yIG1vZCB3aGlsZSBzZXQgYWxseSBsYWJlbCB1c2VzIHJhaXNlIG5vdCAnICtcbiAgICAnc3RvcmVkIGNsYXNzIHNhZmVjYWxsIHZhciBpbnRlcmZhY2Ugb3IgcHJpdmF0ZSBzdGF0aWMgZXhpdCBpbmRleCBpbmhlcml0ZWQgdG8gZWxzZSBzdGRjYWxsICcgK1xuICAgICdvdmVycmlkZSBzaHIgYXNtIGZhciByZXNvdXJjZXN0cmluZyBmaW5hbGl6YXRpb24gcGFja2VkIHZpcnR1YWwgb3V0IGFuZCBwcm90ZWN0ZWQgbGlicmFyeSBkbyAnICtcbiAgICAneG9yd3JpdGUgZ290byBuZWFyIGZ1bmN0aW9uIGVuZCBkaXYgb3ZlcmxvYWQgb2JqZWN0IHVuaXQgYmVnaW4gc3RyaW5nIG9uIGlubGluZSByZXBlYXQgdW50aWwgJyArXG4gICAgJ2Rlc3RydWN0b3Igd3JpdGUgbWVzc2FnZSBwcm9ncmFtIHdpdGggcmVhZCBpbml0aWFsaXphdGlvbiBleGNlcHQgZGVmYXVsdCBuaWwgaWYgY2FzZSBjZGVjbCBpbiAnICtcbiAgICAnZG93bnRvIHRocmVhZHZhciBvZiB0cnkgcGFzY2FsIGNvbnN0IGV4dGVybmFsIGNvbnN0cnVjdG9yIHR5cGUgcHVibGljIHRoZW4gaW1wbGVtZW50YXRpb24gJyArXG4gICAgJ2ZpbmFsbHkgcHVibGlzaGVkIHByb2NlZHVyZSBhYnNvbHV0ZSByZWludHJvZHVjZSBvcGVyYXRvciBhcyBpcyBhYnN0cmFjdCBhbGlhcyBhc3NlbWJsZXIgJyArXG4gICAgJ2JpdHBhY2tlZCBicmVhayBjb250aW51ZSBjcHBkZWNsIGN2YXIgZW51bWVyYXRvciBleHBlcmltZW50YWwgcGxhdGZvcm0gZGVwcmVjYXRlZCAnICtcbiAgICAndW5pbXBsZW1lbnRlZCBkeW5hbWljIGV4cG9ydCBmYXIxNiBmb3J3YXJkIGdlbmVyaWMgaGVscGVyIGltcGxlbWVudHMgaW50ZXJydXB0IGlvY2hlY2tzICcgK1xuICAgICdsb2NhbCBuYW1lIG5vZGVmYXVsdCBub3JldHVybiBub3N0YWNrZnJhbWUgb2xkZnBjY2FsbCBvdGhlcndpc2Ugc2F2ZXJlZ2lzdGVycyBzb2Z0ZmxvYXQgJyArXG4gICAgJ3NwZWNpYWxpemUgc3RyaWN0IHVuYWxpZ25lZCB2YXJhcmdzICc7XG4gIGNvbnN0IENPTU1FTlRfTU9ERVMgPSBbXG4gICAgaGxqcy5DX0xJTkVfQ09NTUVOVF9NT0RFLFxuICAgIGhsanMuQ09NTUVOVCgvXFx7LywgL1xcfS8sIHtcbiAgICAgIHJlbGV2YW5jZTogMFxuICAgIH0pLFxuICAgIGhsanMuQ09NTUVOVCgvXFwoXFwqLywgL1xcKlxcKS8sIHtcbiAgICAgIHJlbGV2YW5jZTogMTBcbiAgICB9KVxuICBdO1xuICBjb25zdCBESVJFQ1RJVkUgPSB7XG4gICAgY2xhc3NOYW1lOiAnbWV0YScsXG4gICAgdmFyaWFudHM6IFtcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC9cXHtcXCQvLFxuICAgICAgICBlbmQ6IC9cXH0vXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogL1xcKFxcKlxcJC8sXG4gICAgICAgIGVuZDogL1xcKlxcKS9cbiAgICAgIH1cbiAgICBdXG4gIH07XG4gIGNvbnN0IFNUUklORyA9IHtcbiAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgIGJlZ2luOiAvJy8sXG4gICAgZW5kOiAvJy8sXG4gICAgY29udGFpbnM6IFt7XG4gICAgICBiZWdpbjogLycnL1xuICAgIH1dXG4gIH07XG4gIGNvbnN0IE5VTUJFUiA9IHtcbiAgICBjbGFzc05hbWU6ICdudW1iZXInLFxuICAgIHJlbGV2YW5jZTogMCxcbiAgICAvLyBTb3VyY2U6IGh0dHBzOi8vd3d3LmZyZWVwYXNjYWwub3JnL2RvY3MtaHRtbC9yZWYvcmVmc2U2Lmh0bWxcbiAgICB2YXJpYW50czogW1xuICAgICAge1xuICAgICAgICAvLyBIZXhhZGVjaW1hbCBub3RhdGlvbiwgZS5nLiwgJDdGLlxuICAgICAgICBiZWdpbjogJ1xcXFwkWzAtOUEtRmEtZl0rJ1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgLy8gT2N0YWwgbm90YXRpb24sIGUuZy4sICY0Mi5cbiAgICAgICAgYmVnaW46ICcmWzAtN10rJ1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgLy8gQmluYXJ5IG5vdGF0aW9uLCBlLmcuLCAlMTAxMC5cbiAgICAgICAgYmVnaW46ICclWzAxXSsnXG4gICAgICB9XG4gICAgXVxuICB9O1xuICBjb25zdCBDSEFSX1NUUklORyA9IHtcbiAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgIGJlZ2luOiAvKCNcXGQrKSsvXG4gIH07XG4gIGNvbnN0IENMQVNTID0ge1xuICAgIGJlZ2luOiBobGpzLklERU5UX1JFICsgJ1xcXFxzKj1cXFxccypjbGFzc1xcXFxzKlxcXFwoJyxcbiAgICByZXR1cm5CZWdpbjogdHJ1ZSxcbiAgICBjb250YWluczogW2hsanMuVElUTEVfTU9ERV1cbiAgfTtcbiAgY29uc3QgRlVOQ1RJT04gPSB7XG4gICAgY2xhc3NOYW1lOiAnZnVuY3Rpb24nLFxuICAgIGJlZ2luS2V5d29yZHM6ICdmdW5jdGlvbiBjb25zdHJ1Y3RvciBkZXN0cnVjdG9yIHByb2NlZHVyZScsXG4gICAgZW5kOiAvWzo7XS8sXG4gICAga2V5d29yZHM6ICdmdW5jdGlvbiBjb25zdHJ1Y3RvcnwxMCBkZXN0cnVjdG9yfDEwIHByb2NlZHVyZXwxMCcsXG4gICAgY29udGFpbnM6IFtcbiAgICAgIGhsanMuVElUTEVfTU9ERSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAncGFyYW1zJyxcbiAgICAgICAgYmVnaW46IC9cXCgvLFxuICAgICAgICBlbmQ6IC9cXCkvLFxuICAgICAgICBrZXl3b3JkczogS0VZV09SRFMsXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgU1RSSU5HLFxuICAgICAgICAgIENIQVJfU1RSSU5HLFxuICAgICAgICAgIERJUkVDVElWRVxuICAgICAgICBdLmNvbmNhdChDT01NRU5UX01PREVTKVxuICAgICAgfSxcbiAgICAgIERJUkVDVElWRVxuICAgIF0uY29uY2F0KENPTU1FTlRfTU9ERVMpXG4gIH07XG4gIHJldHVybiB7XG4gICAgbmFtZTogJ0RlbHBoaScsXG4gICAgYWxpYXNlczogW1xuICAgICAgJ2RwcicsXG4gICAgICAnZGZtJyxcbiAgICAgICdwYXMnLFxuICAgICAgJ3Bhc2NhbCcsXG4gICAgICAnZnJlZXBhc2NhbCcsXG4gICAgICAnbGF6YXJ1cycsXG4gICAgICAnbHByJyxcbiAgICAgICdsZm0nXG4gICAgXSxcbiAgICBjYXNlX2luc2Vuc2l0aXZlOiB0cnVlLFxuICAgIGtleXdvcmRzOiBLRVlXT1JEUyxcbiAgICBpbGxlZ2FsOiAvXCJ8XFwkW0ctWmctel18XFwvXFwqfDxcXC98XFx8LyxcbiAgICBjb250YWluczogW1xuICAgICAgU1RSSU5HLFxuICAgICAgQ0hBUl9TVFJJTkcsXG4gICAgICBobGpzLk5VTUJFUl9NT0RFLFxuICAgICAgTlVNQkVSLFxuICAgICAgQ0xBU1MsXG4gICAgICBGVU5DVElPTixcbiAgICAgIERJUkVDVElWRVxuICAgIF0uY29uY2F0KENPTU1FTlRfTU9ERVMpXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gZGVscGhpO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9