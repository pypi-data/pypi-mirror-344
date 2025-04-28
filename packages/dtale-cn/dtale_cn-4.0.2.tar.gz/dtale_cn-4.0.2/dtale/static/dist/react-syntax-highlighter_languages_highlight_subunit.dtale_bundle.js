(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_subunit"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/subunit.js":
/*!**************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/subunit.js ***!
  \**************************************************************************************************/
/***/ ((module) => {

/*
Language: SubUnit
Author: Sergey Bronnikov <sergeyb@bronevichok.ru>
Website: https://pypi.org/project/python-subunit/
*/

function subunit(hljs) {
  const DETAILS = {
    className: 'string',
    begin: '\\[\n(multipart)?',
    end: '\\]\n'
  };
  const TIME = {
    className: 'string',
    begin: '\\d{4}-\\d{2}-\\d{2}(\\s+)\\d{2}:\\d{2}:\\d{2}\.\\d+Z'
  };
  const PROGRESSVALUE = {
    className: 'string',
    begin: '(\\+|-)\\d+'
  };
  const KEYWORDS = {
    className: 'keyword',
    relevance: 10,
    variants: [
      {
        begin: '^(test|testing|success|successful|failure|error|skip|xfail|uxsuccess)(:?)\\s+(test)?'
      },
      {
        begin: '^progress(:?)(\\s+)?(pop|push)?'
      },
      {
        begin: '^tags:'
      },
      {
        begin: '^time:'
      }
    ]
  };
  return {
    name: 'SubUnit',
    case_insensitive: true,
    contains: [
      DETAILS,
      TIME,
      PROGRESSVALUE,
      KEYWORDS
    ]
  };
}

module.exports = subunit;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfc3VidW5pdC5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxnQkFBZ0IsRUFBRSxLQUFLLEVBQUUsS0FBSyxFQUFFLFVBQVUsRUFBRSxLQUFLLEVBQUUsS0FBSyxFQUFFO0FBQzFEO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9zdWJ1bml0LmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogU3ViVW5pdFxuQXV0aG9yOiBTZXJnZXkgQnJvbm5pa292IDxzZXJnZXliQGJyb25ldmljaG9rLnJ1PlxuV2Vic2l0ZTogaHR0cHM6Ly9weXBpLm9yZy9wcm9qZWN0L3B5dGhvbi1zdWJ1bml0L1xuKi9cblxuZnVuY3Rpb24gc3VidW5pdChobGpzKSB7XG4gIGNvbnN0IERFVEFJTFMgPSB7XG4gICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICBiZWdpbjogJ1xcXFxbXFxuKG11bHRpcGFydCk/JyxcbiAgICBlbmQ6ICdcXFxcXVxcbidcbiAgfTtcbiAgY29uc3QgVElNRSA9IHtcbiAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgIGJlZ2luOiAnXFxcXGR7NH0tXFxcXGR7Mn0tXFxcXGR7Mn0oXFxcXHMrKVxcXFxkezJ9OlxcXFxkezJ9OlxcXFxkezJ9XFwuXFxcXGQrWidcbiAgfTtcbiAgY29uc3QgUFJPR1JFU1NWQUxVRSA9IHtcbiAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgIGJlZ2luOiAnKFxcXFwrfC0pXFxcXGQrJ1xuICB9O1xuICBjb25zdCBLRVlXT1JEUyA9IHtcbiAgICBjbGFzc05hbWU6ICdrZXl3b3JkJyxcbiAgICByZWxldmFuY2U6IDEwLFxuICAgIHZhcmlhbnRzOiBbXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnXih0ZXN0fHRlc3Rpbmd8c3VjY2Vzc3xzdWNjZXNzZnVsfGZhaWx1cmV8ZXJyb3J8c2tpcHx4ZmFpbHx1eHN1Y2Nlc3MpKDo/KVxcXFxzKyh0ZXN0KT8nXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogJ15wcm9ncmVzcyg6PykoXFxcXHMrKT8ocG9wfHB1c2gpPydcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnXnRhZ3M6J1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICdedGltZTonXG4gICAgICB9XG4gICAgXVxuICB9O1xuICByZXR1cm4ge1xuICAgIG5hbWU6ICdTdWJVbml0JyxcbiAgICBjYXNlX2luc2Vuc2l0aXZlOiB0cnVlLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBERVRBSUxTLFxuICAgICAgVElNRSxcbiAgICAgIFBST0dSRVNTVkFMVUUsXG4gICAgICBLRVlXT1JEU1xuICAgIF1cbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBzdWJ1bml0O1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9