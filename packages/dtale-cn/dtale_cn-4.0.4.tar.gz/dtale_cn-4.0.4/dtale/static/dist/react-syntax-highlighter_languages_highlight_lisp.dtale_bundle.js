(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_lisp"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/lisp.js":
/*!***********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/lisp.js ***!
  \***********************************************************************************************/
/***/ ((module) => {

/*
Language: Lisp
Description: Generic lisp syntax
Author: Vasily Polovnyov <vast@whiteants.net>
Category: lisp
*/

function lisp(hljs) {
  var LISP_IDENT_RE = '[a-zA-Z_\\-+\\*\\/<=>&#][a-zA-Z0-9_\\-+*\\/<=>&#!]*';
  var MEC_RE = '\\|[^]*?\\|';
  var LISP_SIMPLE_NUMBER_RE = '(-|\\+)?\\d+(\\.\\d+|\\/\\d+)?((d|e|f|l|s|D|E|F|L|S)(\\+|-)?\\d+)?';
  var LITERAL = {
    className: 'literal',
    begin: '\\b(t{1}|nil)\\b'
  };
  var NUMBER = {
    className: 'number',
    variants: [
      {begin: LISP_SIMPLE_NUMBER_RE, relevance: 0},
      {begin: '#(b|B)[0-1]+(/[0-1]+)?'},
      {begin: '#(o|O)[0-7]+(/[0-7]+)?'},
      {begin: '#(x|X)[0-9a-fA-F]+(/[0-9a-fA-F]+)?'},
      {begin: '#(c|C)\\(' + LISP_SIMPLE_NUMBER_RE + ' +' + LISP_SIMPLE_NUMBER_RE, end: '\\)'}
    ]
  };
  var STRING = hljs.inherit(hljs.QUOTE_STRING_MODE, {illegal: null});
  var COMMENT = hljs.COMMENT(
    ';', '$',
    {
      relevance: 0
    }
  );
  var VARIABLE = {
    begin: '\\*', end: '\\*'
  };
  var KEYWORD = {
    className: 'symbol',
    begin: '[:&]' + LISP_IDENT_RE
  };
  var IDENT = {
    begin: LISP_IDENT_RE,
    relevance: 0
  };
  var MEC = {
    begin: MEC_RE
  };
  var QUOTED_LIST = {
    begin: '\\(', end: '\\)',
    contains: ['self', LITERAL, STRING, NUMBER, IDENT]
  };
  var QUOTED = {
    contains: [NUMBER, STRING, VARIABLE, KEYWORD, QUOTED_LIST, IDENT],
    variants: [
      {
        begin: '[\'`]\\(', end: '\\)'
      },
      {
        begin: '\\(quote ', end: '\\)',
        keywords: {name: 'quote'}
      },
      {
        begin: '\'' + MEC_RE
      }
    ]
  };
  var QUOTED_ATOM = {
    variants: [
      {begin: '\'' + LISP_IDENT_RE},
      {begin: '#\'' + LISP_IDENT_RE + '(::' + LISP_IDENT_RE + ')*'}
    ]
  };
  var LIST = {
    begin: '\\(\\s*', end: '\\)'
  };
  var BODY = {
    endsWithParent: true,
    relevance: 0
  };
  LIST.contains = [
    {
      className: 'name',
      variants: [
        {
          begin: LISP_IDENT_RE,
          relevance: 0,
        },
        {begin: MEC_RE}
      ]
    },
    BODY
  ];
  BODY.contains = [QUOTED, QUOTED_ATOM, LIST, LITERAL, NUMBER, STRING, COMMENT, VARIABLE, KEYWORD, MEC, IDENT];

  return {
    name: 'Lisp',
    illegal: /\S/,
    contains: [
      NUMBER,
      hljs.SHEBANG(),
      LITERAL,
      STRING,
      COMMENT,
      QUOTED,
      QUOTED_ATOM,
      LIST,
      IDENT
    ]
  };
}

module.exports = lisp;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfbGlzcC5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0Esa0JBQWtCLEVBQUU7QUFDcEI7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPLDJDQUEyQztBQUNsRCxPQUFPLGdDQUFnQztBQUN2QyxPQUFPLGdDQUFnQztBQUN2QyxPQUFPLDRDQUE0QztBQUNuRCxPQUFPO0FBQ1A7QUFDQTtBQUNBLHFEQUFxRCxjQUFjO0FBQ25FO0FBQ0EsTUFBTTtBQUNOO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0EsbUJBQW1CO0FBQ25CLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU8sNEJBQTRCO0FBQ25DLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFNBQVM7QUFDVCxTQUFTO0FBQ1Q7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9saXNwLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogTGlzcFxuRGVzY3JpcHRpb246IEdlbmVyaWMgbGlzcCBzeW50YXhcbkF1dGhvcjogVmFzaWx5IFBvbG92bnlvdiA8dmFzdEB3aGl0ZWFudHMubmV0PlxuQ2F0ZWdvcnk6IGxpc3BcbiovXG5cbmZ1bmN0aW9uIGxpc3AoaGxqcykge1xuICB2YXIgTElTUF9JREVOVF9SRSA9ICdbYS16QS1aX1xcXFwtK1xcXFwqXFxcXC88PT4mI11bYS16QS1aMC05X1xcXFwtKypcXFxcLzw9PiYjIV0qJztcbiAgdmFyIE1FQ19SRSA9ICdcXFxcfFteXSo/XFxcXHwnO1xuICB2YXIgTElTUF9TSU1QTEVfTlVNQkVSX1JFID0gJygtfFxcXFwrKT9cXFxcZCsoXFxcXC5cXFxcZCt8XFxcXC9cXFxcZCspPygoZHxlfGZ8bHxzfER8RXxGfEx8UykoXFxcXCt8LSk/XFxcXGQrKT8nO1xuICB2YXIgTElURVJBTCA9IHtcbiAgICBjbGFzc05hbWU6ICdsaXRlcmFsJyxcbiAgICBiZWdpbjogJ1xcXFxiKHR7MX18bmlsKVxcXFxiJ1xuICB9O1xuICB2YXIgTlVNQkVSID0ge1xuICAgIGNsYXNzTmFtZTogJ251bWJlcicsXG4gICAgdmFyaWFudHM6IFtcbiAgICAgIHtiZWdpbjogTElTUF9TSU1QTEVfTlVNQkVSX1JFLCByZWxldmFuY2U6IDB9LFxuICAgICAge2JlZ2luOiAnIyhifEIpWzAtMV0rKC9bMC0xXSspPyd9LFxuICAgICAge2JlZ2luOiAnIyhvfE8pWzAtN10rKC9bMC03XSspPyd9LFxuICAgICAge2JlZ2luOiAnIyh4fFgpWzAtOWEtZkEtRl0rKC9bMC05YS1mQS1GXSspPyd9LFxuICAgICAge2JlZ2luOiAnIyhjfEMpXFxcXCgnICsgTElTUF9TSU1QTEVfTlVNQkVSX1JFICsgJyArJyArIExJU1BfU0lNUExFX05VTUJFUl9SRSwgZW5kOiAnXFxcXCknfVxuICAgIF1cbiAgfTtcbiAgdmFyIFNUUklORyA9IGhsanMuaW5oZXJpdChobGpzLlFVT1RFX1NUUklOR19NT0RFLCB7aWxsZWdhbDogbnVsbH0pO1xuICB2YXIgQ09NTUVOVCA9IGhsanMuQ09NTUVOVChcbiAgICAnOycsICckJyxcbiAgICB7XG4gICAgICByZWxldmFuY2U6IDBcbiAgICB9XG4gICk7XG4gIHZhciBWQVJJQUJMRSA9IHtcbiAgICBiZWdpbjogJ1xcXFwqJywgZW5kOiAnXFxcXConXG4gIH07XG4gIHZhciBLRVlXT1JEID0ge1xuICAgIGNsYXNzTmFtZTogJ3N5bWJvbCcsXG4gICAgYmVnaW46ICdbOiZdJyArIExJU1BfSURFTlRfUkVcbiAgfTtcbiAgdmFyIElERU5UID0ge1xuICAgIGJlZ2luOiBMSVNQX0lERU5UX1JFLFxuICAgIHJlbGV2YW5jZTogMFxuICB9O1xuICB2YXIgTUVDID0ge1xuICAgIGJlZ2luOiBNRUNfUkVcbiAgfTtcbiAgdmFyIFFVT1RFRF9MSVNUID0ge1xuICAgIGJlZ2luOiAnXFxcXCgnLCBlbmQ6ICdcXFxcKScsXG4gICAgY29udGFpbnM6IFsnc2VsZicsIExJVEVSQUwsIFNUUklORywgTlVNQkVSLCBJREVOVF1cbiAgfTtcbiAgdmFyIFFVT1RFRCA9IHtcbiAgICBjb250YWluczogW05VTUJFUiwgU1RSSU5HLCBWQVJJQUJMRSwgS0VZV09SRCwgUVVPVEVEX0xJU1QsIElERU5UXSxcbiAgICB2YXJpYW50czogW1xuICAgICAge1xuICAgICAgICBiZWdpbjogJ1tcXCdgXVxcXFwoJywgZW5kOiAnXFxcXCknXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogJ1xcXFwocXVvdGUgJywgZW5kOiAnXFxcXCknLFxuICAgICAgICBrZXl3b3Jkczoge25hbWU6ICdxdW90ZSd9XG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogJ1xcJycgKyBNRUNfUkVcbiAgICAgIH1cbiAgICBdXG4gIH07XG4gIHZhciBRVU9URURfQVRPTSA9IHtcbiAgICB2YXJpYW50czogW1xuICAgICAge2JlZ2luOiAnXFwnJyArIExJU1BfSURFTlRfUkV9LFxuICAgICAge2JlZ2luOiAnI1xcJycgKyBMSVNQX0lERU5UX1JFICsgJyg6OicgKyBMSVNQX0lERU5UX1JFICsgJykqJ31cbiAgICBdXG4gIH07XG4gIHZhciBMSVNUID0ge1xuICAgIGJlZ2luOiAnXFxcXChcXFxccyonLCBlbmQ6ICdcXFxcKSdcbiAgfTtcbiAgdmFyIEJPRFkgPSB7XG4gICAgZW5kc1dpdGhQYXJlbnQ6IHRydWUsXG4gICAgcmVsZXZhbmNlOiAwXG4gIH07XG4gIExJU1QuY29udGFpbnMgPSBbXG4gICAge1xuICAgICAgY2xhc3NOYW1lOiAnbmFtZScsXG4gICAgICB2YXJpYW50czogW1xuICAgICAgICB7XG4gICAgICAgICAgYmVnaW46IExJU1BfSURFTlRfUkUsXG4gICAgICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgICB9LFxuICAgICAgICB7YmVnaW46IE1FQ19SRX1cbiAgICAgIF1cbiAgICB9LFxuICAgIEJPRFlcbiAgXTtcbiAgQk9EWS5jb250YWlucyA9IFtRVU9URUQsIFFVT1RFRF9BVE9NLCBMSVNULCBMSVRFUkFMLCBOVU1CRVIsIFNUUklORywgQ09NTUVOVCwgVkFSSUFCTEUsIEtFWVdPUkQsIE1FQywgSURFTlRdO1xuXG4gIHJldHVybiB7XG4gICAgbmFtZTogJ0xpc3AnLFxuICAgIGlsbGVnYWw6IC9cXFMvLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBOVU1CRVIsXG4gICAgICBobGpzLlNIRUJBTkcoKSxcbiAgICAgIExJVEVSQUwsXG4gICAgICBTVFJJTkcsXG4gICAgICBDT01NRU5ULFxuICAgICAgUVVPVEVELFxuICAgICAgUVVPVEVEX0FUT00sXG4gICAgICBMSVNULFxuICAgICAgSURFTlRcbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gbGlzcDtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==