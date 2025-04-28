(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_gcode"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/gcode.js":
/*!************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/gcode.js ***!
  \************************************************************************************************/
/***/ ((module) => {

/*
 Language: G-code (ISO 6983)
 Contributors: Adam Joseph Cook <adam.joseph.cook@gmail.com>
 Description: G-code syntax highlighter for Fanuc and other common CNC machine tool controls.
 Website: https://www.sis.se/api/document/preview/911952/
 */

function gcode(hljs) {
  const GCODE_IDENT_RE = '[A-Z_][A-Z0-9_.]*';
  const GCODE_CLOSE_RE = '%';
  const GCODE_KEYWORDS = {
    $pattern: GCODE_IDENT_RE,
    keyword: 'IF DO WHILE ENDWHILE CALL ENDIF SUB ENDSUB GOTO REPEAT ENDREPEAT ' +
      'EQ LT GT NE GE LE OR XOR'
  };
  const GCODE_START = {
    className: 'meta',
    begin: '([O])([0-9]+)'
  };
  const NUMBER = hljs.inherit(hljs.C_NUMBER_MODE, {
    begin: '([-+]?((\\.\\d+)|(\\d+)(\\.\\d*)?))|' + hljs.C_NUMBER_RE
  });
  const GCODE_CODE = [
    hljs.C_LINE_COMMENT_MODE,
    hljs.C_BLOCK_COMMENT_MODE,
    hljs.COMMENT(/\(/, /\)/),
    NUMBER,
    hljs.inherit(hljs.APOS_STRING_MODE, {
      illegal: null
    }),
    hljs.inherit(hljs.QUOTE_STRING_MODE, {
      illegal: null
    }),
    {
      className: 'name',
      begin: '([G])([0-9]+\\.?[0-9]?)'
    },
    {
      className: 'name',
      begin: '([M])([0-9]+\\.?[0-9]?)'
    },
    {
      className: 'attr',
      begin: '(VC|VS|#)',
      end: '(\\d+)'
    },
    {
      className: 'attr',
      begin: '(VZOFX|VZOFY|VZOFZ)'
    },
    {
      className: 'built_in',
      begin: '(ATAN|ABS|ACOS|ASIN|SIN|COS|EXP|FIX|FUP|ROUND|LN|TAN)(\\[)',
      contains: [
        NUMBER
      ],
      end: '\\]'
    },
    {
      className: 'symbol',
      variants: [
        {
          begin: 'N',
          end: '\\d+',
          illegal: '\\W'
        }
      ]
    }
  ];

  return {
    name: 'G-code (ISO 6983)',
    aliases: ['nc'],
    // Some implementations (CNC controls) of G-code are interoperable with uppercase and lowercase letters seamlessly.
    // However, most prefer all uppercase and uppercase is customary.
    case_insensitive: true,
    keywords: GCODE_KEYWORDS,
    contains: [
      {
        className: 'meta',
        begin: GCODE_CLOSE_RE
      },
      GCODE_START
    ].concat(GCODE_CODE)
  };
}

module.exports = gcode;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfZ2NvZGUuZHRhbGVfYnVuZGxlLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxHQUFHO0FBQ0g7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL2djb2RlLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG4gTGFuZ3VhZ2U6IEctY29kZSAoSVNPIDY5ODMpXG4gQ29udHJpYnV0b3JzOiBBZGFtIEpvc2VwaCBDb29rIDxhZGFtLmpvc2VwaC5jb29rQGdtYWlsLmNvbT5cbiBEZXNjcmlwdGlvbjogRy1jb2RlIHN5bnRheCBoaWdobGlnaHRlciBmb3IgRmFudWMgYW5kIG90aGVyIGNvbW1vbiBDTkMgbWFjaGluZSB0b29sIGNvbnRyb2xzLlxuIFdlYnNpdGU6IGh0dHBzOi8vd3d3LnNpcy5zZS9hcGkvZG9jdW1lbnQvcHJldmlldy85MTE5NTIvXG4gKi9cblxuZnVuY3Rpb24gZ2NvZGUoaGxqcykge1xuICBjb25zdCBHQ09ERV9JREVOVF9SRSA9ICdbQS1aX11bQS1aMC05Xy5dKic7XG4gIGNvbnN0IEdDT0RFX0NMT1NFX1JFID0gJyUnO1xuICBjb25zdCBHQ09ERV9LRVlXT1JEUyA9IHtcbiAgICAkcGF0dGVybjogR0NPREVfSURFTlRfUkUsXG4gICAga2V5d29yZDogJ0lGIERPIFdISUxFIEVORFdISUxFIENBTEwgRU5ESUYgU1VCIEVORFNVQiBHT1RPIFJFUEVBVCBFTkRSRVBFQVQgJyArXG4gICAgICAnRVEgTFQgR1QgTkUgR0UgTEUgT1IgWE9SJ1xuICB9O1xuICBjb25zdCBHQ09ERV9TVEFSVCA9IHtcbiAgICBjbGFzc05hbWU6ICdtZXRhJyxcbiAgICBiZWdpbjogJyhbT10pKFswLTldKyknXG4gIH07XG4gIGNvbnN0IE5VTUJFUiA9IGhsanMuaW5oZXJpdChobGpzLkNfTlVNQkVSX01PREUsIHtcbiAgICBiZWdpbjogJyhbLStdPygoXFxcXC5cXFxcZCspfChcXFxcZCspKFxcXFwuXFxcXGQqKT8pKXwnICsgaGxqcy5DX05VTUJFUl9SRVxuICB9KTtcbiAgY29uc3QgR0NPREVfQ09ERSA9IFtcbiAgICBobGpzLkNfTElORV9DT01NRU5UX01PREUsXG4gICAgaGxqcy5DX0JMT0NLX0NPTU1FTlRfTU9ERSxcbiAgICBobGpzLkNPTU1FTlQoL1xcKC8sIC9cXCkvKSxcbiAgICBOVU1CRVIsXG4gICAgaGxqcy5pbmhlcml0KGhsanMuQVBPU19TVFJJTkdfTU9ERSwge1xuICAgICAgaWxsZWdhbDogbnVsbFxuICAgIH0pLFxuICAgIGhsanMuaW5oZXJpdChobGpzLlFVT1RFX1NUUklOR19NT0RFLCB7XG4gICAgICBpbGxlZ2FsOiBudWxsXG4gICAgfSksXG4gICAge1xuICAgICAgY2xhc3NOYW1lOiAnbmFtZScsXG4gICAgICBiZWdpbjogJyhbR10pKFswLTldK1xcXFwuP1swLTldPyknXG4gICAgfSxcbiAgICB7XG4gICAgICBjbGFzc05hbWU6ICduYW1lJyxcbiAgICAgIGJlZ2luOiAnKFtNXSkoWzAtOV0rXFxcXC4/WzAtOV0/KSdcbiAgICB9LFxuICAgIHtcbiAgICAgIGNsYXNzTmFtZTogJ2F0dHInLFxuICAgICAgYmVnaW46ICcoVkN8VlN8IyknLFxuICAgICAgZW5kOiAnKFxcXFxkKyknXG4gICAgfSxcbiAgICB7XG4gICAgICBjbGFzc05hbWU6ICdhdHRyJyxcbiAgICAgIGJlZ2luOiAnKFZaT0ZYfFZaT0ZZfFZaT0ZaKSdcbiAgICB9LFxuICAgIHtcbiAgICAgIGNsYXNzTmFtZTogJ2J1aWx0X2luJyxcbiAgICAgIGJlZ2luOiAnKEFUQU58QUJTfEFDT1N8QVNJTnxTSU58Q09TfEVYUHxGSVh8RlVQfFJPVU5EfExOfFRBTikoXFxcXFspJyxcbiAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgIE5VTUJFUlxuICAgICAgXSxcbiAgICAgIGVuZDogJ1xcXFxdJ1xuICAgIH0sXG4gICAge1xuICAgICAgY2xhc3NOYW1lOiAnc3ltYm9sJyxcbiAgICAgIHZhcmlhbnRzOiBbXG4gICAgICAgIHtcbiAgICAgICAgICBiZWdpbjogJ04nLFxuICAgICAgICAgIGVuZDogJ1xcXFxkKycsXG4gICAgICAgICAgaWxsZWdhbDogJ1xcXFxXJ1xuICAgICAgICB9XG4gICAgICBdXG4gICAgfVxuICBdO1xuXG4gIHJldHVybiB7XG4gICAgbmFtZTogJ0ctY29kZSAoSVNPIDY5ODMpJyxcbiAgICBhbGlhc2VzOiBbJ25jJ10sXG4gICAgLy8gU29tZSBpbXBsZW1lbnRhdGlvbnMgKENOQyBjb250cm9scykgb2YgRy1jb2RlIGFyZSBpbnRlcm9wZXJhYmxlIHdpdGggdXBwZXJjYXNlIGFuZCBsb3dlcmNhc2UgbGV0dGVycyBzZWFtbGVzc2x5LlxuICAgIC8vIEhvd2V2ZXIsIG1vc3QgcHJlZmVyIGFsbCB1cHBlcmNhc2UgYW5kIHVwcGVyY2FzZSBpcyBjdXN0b21hcnkuXG4gICAgY2FzZV9pbnNlbnNpdGl2ZTogdHJ1ZSxcbiAgICBrZXl3b3JkczogR0NPREVfS0VZV09SRFMsXG4gICAgY29udGFpbnM6IFtcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnbWV0YScsXG4gICAgICAgIGJlZ2luOiBHQ09ERV9DTE9TRV9SRVxuICAgICAgfSxcbiAgICAgIEdDT0RFX1NUQVJUXG4gICAgXS5jb25jYXQoR0NPREVfQ09ERSlcbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBnY29kZTtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==