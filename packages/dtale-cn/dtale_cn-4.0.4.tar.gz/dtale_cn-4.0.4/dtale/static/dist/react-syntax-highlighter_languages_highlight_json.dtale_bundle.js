(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_json"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/json.js":
/*!***********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/json.js ***!
  \***********************************************************************************************/
/***/ ((module) => {

/*
Language: JSON
Description: JSON (JavaScript Object Notation) is a lightweight data-interchange format.
Author: Ivan Sagalaev <maniac@softwaremaniacs.org>
Website: http://www.json.org
Category: common, protocols
*/

function json(hljs) {
  const LITERALS = {
    literal: 'true false null'
  };
  const ALLOWED_COMMENTS = [
    hljs.C_LINE_COMMENT_MODE,
    hljs.C_BLOCK_COMMENT_MODE
  ];
  const TYPES = [
    hljs.QUOTE_STRING_MODE,
    hljs.C_NUMBER_MODE
  ];
  const VALUE_CONTAINER = {
    end: ',',
    endsWithParent: true,
    excludeEnd: true,
    contains: TYPES,
    keywords: LITERALS
  };
  const OBJECT = {
    begin: /\{/,
    end: /\}/,
    contains: [
      {
        className: 'attr',
        begin: /"/,
        end: /"/,
        contains: [hljs.BACKSLASH_ESCAPE],
        illegal: '\\n'
      },
      hljs.inherit(VALUE_CONTAINER, {
        begin: /:/
      })
    ].concat(ALLOWED_COMMENTS),
    illegal: '\\S'
  };
  const ARRAY = {
    begin: '\\[',
    end: '\\]',
    contains: [hljs.inherit(VALUE_CONTAINER)], // inherit is a workaround for a bug that makes shared modes with endsWithParent compile only the ending of one of the parents
    illegal: '\\S'
  };
  TYPES.push(OBJECT, ARRAY);
  ALLOWED_COMMENTS.forEach(function(rule) {
    TYPES.push(rule);
  });
  return {
    name: 'JSON',
    contains: TYPES,
    keywords: LITERALS,
    illegal: '\\S'
  };
}

module.exports = json;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfanNvbi5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsY0FBYztBQUNkLFlBQVk7QUFDWjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEdBQUc7QUFDSDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvanNvbi5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKlxuTGFuZ3VhZ2U6IEpTT05cbkRlc2NyaXB0aW9uOiBKU09OIChKYXZhU2NyaXB0IE9iamVjdCBOb3RhdGlvbikgaXMgYSBsaWdodHdlaWdodCBkYXRhLWludGVyY2hhbmdlIGZvcm1hdC5cbkF1dGhvcjogSXZhbiBTYWdhbGFldiA8bWFuaWFjQHNvZnR3YXJlbWFuaWFjcy5vcmc+XG5XZWJzaXRlOiBodHRwOi8vd3d3Lmpzb24ub3JnXG5DYXRlZ29yeTogY29tbW9uLCBwcm90b2NvbHNcbiovXG5cbmZ1bmN0aW9uIGpzb24oaGxqcykge1xuICBjb25zdCBMSVRFUkFMUyA9IHtcbiAgICBsaXRlcmFsOiAndHJ1ZSBmYWxzZSBudWxsJ1xuICB9O1xuICBjb25zdCBBTExPV0VEX0NPTU1FTlRTID0gW1xuICAgIGhsanMuQ19MSU5FX0NPTU1FTlRfTU9ERSxcbiAgICBobGpzLkNfQkxPQ0tfQ09NTUVOVF9NT0RFXG4gIF07XG4gIGNvbnN0IFRZUEVTID0gW1xuICAgIGhsanMuUVVPVEVfU1RSSU5HX01PREUsXG4gICAgaGxqcy5DX05VTUJFUl9NT0RFXG4gIF07XG4gIGNvbnN0IFZBTFVFX0NPTlRBSU5FUiA9IHtcbiAgICBlbmQ6ICcsJyxcbiAgICBlbmRzV2l0aFBhcmVudDogdHJ1ZSxcbiAgICBleGNsdWRlRW5kOiB0cnVlLFxuICAgIGNvbnRhaW5zOiBUWVBFUyxcbiAgICBrZXl3b3JkczogTElURVJBTFNcbiAgfTtcbiAgY29uc3QgT0JKRUNUID0ge1xuICAgIGJlZ2luOiAvXFx7LyxcbiAgICBlbmQ6IC9cXH0vLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ2F0dHInLFxuICAgICAgICBiZWdpbjogL1wiLyxcbiAgICAgICAgZW5kOiAvXCIvLFxuICAgICAgICBjb250YWluczogW2hsanMuQkFDS1NMQVNIX0VTQ0FQRV0sXG4gICAgICAgIGlsbGVnYWw6ICdcXFxcbidcbiAgICAgIH0sXG4gICAgICBobGpzLmluaGVyaXQoVkFMVUVfQ09OVEFJTkVSLCB7XG4gICAgICAgIGJlZ2luOiAvOi9cbiAgICAgIH0pXG4gICAgXS5jb25jYXQoQUxMT1dFRF9DT01NRU5UUyksXG4gICAgaWxsZWdhbDogJ1xcXFxTJ1xuICB9O1xuICBjb25zdCBBUlJBWSA9IHtcbiAgICBiZWdpbjogJ1xcXFxbJyxcbiAgICBlbmQ6ICdcXFxcXScsXG4gICAgY29udGFpbnM6IFtobGpzLmluaGVyaXQoVkFMVUVfQ09OVEFJTkVSKV0sIC8vIGluaGVyaXQgaXMgYSB3b3JrYXJvdW5kIGZvciBhIGJ1ZyB0aGF0IG1ha2VzIHNoYXJlZCBtb2RlcyB3aXRoIGVuZHNXaXRoUGFyZW50IGNvbXBpbGUgb25seSB0aGUgZW5kaW5nIG9mIG9uZSBvZiB0aGUgcGFyZW50c1xuICAgIGlsbGVnYWw6ICdcXFxcUydcbiAgfTtcbiAgVFlQRVMucHVzaChPQkpFQ1QsIEFSUkFZKTtcbiAgQUxMT1dFRF9DT01NRU5UUy5mb3JFYWNoKGZ1bmN0aW9uKHJ1bGUpIHtcbiAgICBUWVBFUy5wdXNoKHJ1bGUpO1xuICB9KTtcbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnSlNPTicsXG4gICAgY29udGFpbnM6IFRZUEVTLFxuICAgIGtleXdvcmRzOiBMSVRFUkFMUyxcbiAgICBpbGxlZ2FsOiAnXFxcXFMnXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0ganNvbjtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==