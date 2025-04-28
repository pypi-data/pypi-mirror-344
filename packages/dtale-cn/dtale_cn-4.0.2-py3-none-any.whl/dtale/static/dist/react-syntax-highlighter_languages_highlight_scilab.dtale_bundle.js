(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_scilab"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/scilab.js":
/*!*************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/scilab.js ***!
  \*************************************************************************************************/
/***/ ((module) => {

/*
Language: Scilab
Author: Sylvestre Ledru <sylvestre.ledru@scilab-enterprises.com>
Origin: matlab.js
Description: Scilab is a port from Matlab
Website: https://www.scilab.org
Category: scientific
*/

function scilab(hljs) {
  const COMMON_CONTAINS = [
    hljs.C_NUMBER_MODE,
    {
      className: 'string',
      begin: '\'|\"',
      end: '\'|\"',
      contains: [ hljs.BACKSLASH_ESCAPE,
        {
          begin: '\'\''
        } ]
    }
  ];

  return {
    name: 'Scilab',
    aliases: [ 'sci' ],
    keywords: {
      $pattern: /%?\w+/,
      keyword: 'abort break case clear catch continue do elseif else endfunction end for function ' +
        'global if pause return resume select try then while',
      literal:
        '%f %F %t %T %pi %eps %inf %nan %e %i %z %s',
      built_in: // Scilab has more than 2000 functions. Just list the most commons
       'abs and acos asin atan ceil cd chdir clearglobal cosh cos cumprod deff disp error ' +
       'exec execstr exists exp eye gettext floor fprintf fread fsolve imag isdef isempty ' +
       'isinfisnan isvector lasterror length load linspace list listfiles log10 log2 log ' +
       'max min msprintf mclose mopen ones or pathconvert poly printf prod pwd rand real ' +
       'round sinh sin size gsort sprintf sqrt strcat strcmps tring sum system tanh tan ' +
       'type typename warning zeros matrix'
    },
    illegal: '("|#|/\\*|\\s+/\\w+)',
    contains: [
      {
        className: 'function',
        beginKeywords: 'function',
        end: '$',
        contains: [
          hljs.UNDERSCORE_TITLE_MODE,
          {
            className: 'params',
            begin: '\\(',
            end: '\\)'
          }
        ]
      },
      // seems to be a guard against [ident]' or [ident].
      // perhaps to prevent attributes from flagging as keywords?
      {
        begin: '[a-zA-Z_][a-zA-Z_0-9]*[\\.\']+',
        relevance: 0
      },
      {
        begin: '\\[',
        end: '\\][\\.\']*',
        relevance: 0,
        contains: COMMON_CONTAINS
      },
      hljs.COMMENT('//', '$')
    ].concat(COMMON_CONTAINS)
  };
}

module.exports = scilab;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfc2NpbGFiLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxVQUFVO0FBQ1Y7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvc2NpbGFiLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogU2NpbGFiXG5BdXRob3I6IFN5bHZlc3RyZSBMZWRydSA8c3lsdmVzdHJlLmxlZHJ1QHNjaWxhYi1lbnRlcnByaXNlcy5jb20+XG5PcmlnaW46IG1hdGxhYi5qc1xuRGVzY3JpcHRpb246IFNjaWxhYiBpcyBhIHBvcnQgZnJvbSBNYXRsYWJcbldlYnNpdGU6IGh0dHBzOi8vd3d3LnNjaWxhYi5vcmdcbkNhdGVnb3J5OiBzY2llbnRpZmljXG4qL1xuXG5mdW5jdGlvbiBzY2lsYWIoaGxqcykge1xuICBjb25zdCBDT01NT05fQ09OVEFJTlMgPSBbXG4gICAgaGxqcy5DX05VTUJFUl9NT0RFLFxuICAgIHtcbiAgICAgIGNsYXNzTmFtZTogJ3N0cmluZycsXG4gICAgICBiZWdpbjogJ1xcJ3xcXFwiJyxcbiAgICAgIGVuZDogJ1xcJ3xcXFwiJyxcbiAgICAgIGNvbnRhaW5zOiBbIGhsanMuQkFDS1NMQVNIX0VTQ0FQRSxcbiAgICAgICAge1xuICAgICAgICAgIGJlZ2luOiAnXFwnXFwnJ1xuICAgICAgICB9IF1cbiAgICB9XG4gIF07XG5cbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnU2NpbGFiJyxcbiAgICBhbGlhc2VzOiBbICdzY2knIF0sXG4gICAga2V5d29yZHM6IHtcbiAgICAgICRwYXR0ZXJuOiAvJT9cXHcrLyxcbiAgICAgIGtleXdvcmQ6ICdhYm9ydCBicmVhayBjYXNlIGNsZWFyIGNhdGNoIGNvbnRpbnVlIGRvIGVsc2VpZiBlbHNlIGVuZGZ1bmN0aW9uIGVuZCBmb3IgZnVuY3Rpb24gJyArXG4gICAgICAgICdnbG9iYWwgaWYgcGF1c2UgcmV0dXJuIHJlc3VtZSBzZWxlY3QgdHJ5IHRoZW4gd2hpbGUnLFxuICAgICAgbGl0ZXJhbDpcbiAgICAgICAgJyVmICVGICV0ICVUICVwaSAlZXBzICVpbmYgJW5hbiAlZSAlaSAleiAlcycsXG4gICAgICBidWlsdF9pbjogLy8gU2NpbGFiIGhhcyBtb3JlIHRoYW4gMjAwMCBmdW5jdGlvbnMuIEp1c3QgbGlzdCB0aGUgbW9zdCBjb21tb25zXG4gICAgICAgJ2FicyBhbmQgYWNvcyBhc2luIGF0YW4gY2VpbCBjZCBjaGRpciBjbGVhcmdsb2JhbCBjb3NoIGNvcyBjdW1wcm9kIGRlZmYgZGlzcCBlcnJvciAnICtcbiAgICAgICAnZXhlYyBleGVjc3RyIGV4aXN0cyBleHAgZXllIGdldHRleHQgZmxvb3IgZnByaW50ZiBmcmVhZCBmc29sdmUgaW1hZyBpc2RlZiBpc2VtcHR5ICcgK1xuICAgICAgICdpc2luZmlzbmFuIGlzdmVjdG9yIGxhc3RlcnJvciBsZW5ndGggbG9hZCBsaW5zcGFjZSBsaXN0IGxpc3RmaWxlcyBsb2cxMCBsb2cyIGxvZyAnICtcbiAgICAgICAnbWF4IG1pbiBtc3ByaW50ZiBtY2xvc2UgbW9wZW4gb25lcyBvciBwYXRoY29udmVydCBwb2x5IHByaW50ZiBwcm9kIHB3ZCByYW5kIHJlYWwgJyArXG4gICAgICAgJ3JvdW5kIHNpbmggc2luIHNpemUgZ3NvcnQgc3ByaW50ZiBzcXJ0IHN0cmNhdCBzdHJjbXBzIHRyaW5nIHN1bSBzeXN0ZW0gdGFuaCB0YW4gJyArXG4gICAgICAgJ3R5cGUgdHlwZW5hbWUgd2FybmluZyB6ZXJvcyBtYXRyaXgnXG4gICAgfSxcbiAgICBpbGxlZ2FsOiAnKFwifCN8L1xcXFwqfFxcXFxzKy9cXFxcdyspJyxcbiAgICBjb250YWluczogW1xuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdmdW5jdGlvbicsXG4gICAgICAgIGJlZ2luS2V5d29yZHM6ICdmdW5jdGlvbicsXG4gICAgICAgIGVuZDogJyQnLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIGhsanMuVU5ERVJTQ09SRV9USVRMRV9NT0RFLFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGNsYXNzTmFtZTogJ3BhcmFtcycsXG4gICAgICAgICAgICBiZWdpbjogJ1xcXFwoJyxcbiAgICAgICAgICAgIGVuZDogJ1xcXFwpJ1xuICAgICAgICAgIH1cbiAgICAgICAgXVxuICAgICAgfSxcbiAgICAgIC8vIHNlZW1zIHRvIGJlIGEgZ3VhcmQgYWdhaW5zdCBbaWRlbnRdJyBvciBbaWRlbnRdLlxuICAgICAgLy8gcGVyaGFwcyB0byBwcmV2ZW50IGF0dHJpYnV0ZXMgZnJvbSBmbGFnZ2luZyBhcyBrZXl3b3Jkcz9cbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICdbYS16QS1aX11bYS16QS1aXzAtOV0qW1xcXFwuXFwnXSsnLFxuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnXFxcXFsnLFxuICAgICAgICBlbmQ6ICdcXFxcXVtcXFxcLlxcJ10qJyxcbiAgICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgICBjb250YWluczogQ09NTU9OX0NPTlRBSU5TXG4gICAgICB9LFxuICAgICAgaGxqcy5DT01NRU5UKCcvLycsICckJylcbiAgICBdLmNvbmNhdChDT01NT05fQ09OVEFJTlMpXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gc2NpbGFiO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9