(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_parser3"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/parser3.js":
/*!**************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/parser3.js ***!
  \**************************************************************************************************/
/***/ ((module) => {

/*
Language: Parser3
Requires: xml.js
Author: Oleg Volchkov <oleg@volchkov.net>
Website: https://www.parser.ru/en/
Category: template
*/

function parser3(hljs) {
  const CURLY_SUBCOMMENT = hljs.COMMENT(
    /\{/,
    /\}/,
    {
      contains: [ 'self' ]
    }
  );
  return {
    name: 'Parser3',
    subLanguage: 'xml',
    relevance: 0,
    contains: [
      hljs.COMMENT('^#', '$'),
      hljs.COMMENT(
        /\^rem\{/,
        /\}/,
        {
          relevance: 10,
          contains: [ CURLY_SUBCOMMENT ]
        }
      ),
      {
        className: 'meta',
        begin: '^@(?:BASE|USE|CLASS|OPTIONS)$',
        relevance: 10
      },
      {
        className: 'title',
        begin: '@[\\w\\-]+\\[[\\w^;\\-]*\\](?:\\[[\\w^;\\-]*\\])?(?:.*)$'
      },
      {
        className: 'variable',
        begin: /\$\{?[\w\-.:]+\}?/
      },
      {
        className: 'keyword',
        begin: /\^[\w\-.:]+/
      },
      {
        className: 'number',
        begin: '\\^#[0-9a-fA-F]+'
      },
      hljs.C_NUMBER_MODE
    ]
  };
}

module.exports = parser3;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfcGFyc2VyMy5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0EsT0FBTztBQUNQLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsZ0JBQWdCO0FBQ2hCLFdBQVc7QUFDWDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBLG1DQUFtQyxvQkFBb0I7QUFDdkQsT0FBTztBQUNQO0FBQ0E7QUFDQSxvQkFBb0IsWUFBWTtBQUNoQyxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvcGFyc2VyMy5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKlxuTGFuZ3VhZ2U6IFBhcnNlcjNcblJlcXVpcmVzOiB4bWwuanNcbkF1dGhvcjogT2xlZyBWb2xjaGtvdiA8b2xlZ0B2b2xjaGtvdi5uZXQ+XG5XZWJzaXRlOiBodHRwczovL3d3dy5wYXJzZXIucnUvZW4vXG5DYXRlZ29yeTogdGVtcGxhdGVcbiovXG5cbmZ1bmN0aW9uIHBhcnNlcjMoaGxqcykge1xuICBjb25zdCBDVVJMWV9TVUJDT01NRU5UID0gaGxqcy5DT01NRU5UKFxuICAgIC9cXHsvLFxuICAgIC9cXH0vLFxuICAgIHtcbiAgICAgIGNvbnRhaW5zOiBbICdzZWxmJyBdXG4gICAgfVxuICApO1xuICByZXR1cm4ge1xuICAgIG5hbWU6ICdQYXJzZXIzJyxcbiAgICBzdWJMYW5ndWFnZTogJ3htbCcsXG4gICAgcmVsZXZhbmNlOiAwLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBobGpzLkNPTU1FTlQoJ14jJywgJyQnKSxcbiAgICAgIGhsanMuQ09NTUVOVChcbiAgICAgICAgL1xcXnJlbVxcey8sXG4gICAgICAgIC9cXH0vLFxuICAgICAgICB7XG4gICAgICAgICAgcmVsZXZhbmNlOiAxMCxcbiAgICAgICAgICBjb250YWluczogWyBDVVJMWV9TVUJDT01NRU5UIF1cbiAgICAgICAgfVxuICAgICAgKSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnbWV0YScsXG4gICAgICAgIGJlZ2luOiAnXkAoPzpCQVNFfFVTRXxDTEFTU3xPUFRJT05TKSQnLFxuICAgICAgICByZWxldmFuY2U6IDEwXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICd0aXRsZScsXG4gICAgICAgIGJlZ2luOiAnQFtcXFxcd1xcXFwtXStcXFxcW1tcXFxcd147XFxcXC1dKlxcXFxdKD86XFxcXFtbXFxcXHdeO1xcXFwtXSpcXFxcXSk/KD86LiopJCdcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3ZhcmlhYmxlJyxcbiAgICAgICAgYmVnaW46IC9cXCRcXHs/W1xcd1xcLS46XStcXH0/L1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAna2V5d29yZCcsXG4gICAgICAgIGJlZ2luOiAvXFxeW1xcd1xcLS46XSsvXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdudW1iZXInLFxuICAgICAgICBiZWdpbjogJ1xcXFxeI1swLTlhLWZBLUZdKydcbiAgICAgIH0sXG4gICAgICBobGpzLkNfTlVNQkVSX01PREVcbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gcGFyc2VyMztcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==