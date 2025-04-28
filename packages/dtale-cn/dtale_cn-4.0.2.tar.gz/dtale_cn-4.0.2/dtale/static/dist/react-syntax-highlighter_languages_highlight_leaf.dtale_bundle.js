(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_leaf"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/leaf.js":
/*!***********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/leaf.js ***!
  \***********************************************************************************************/
/***/ ((module) => {

/*
Language: Leaf
Author: Hale Chan <halechan@qq.com>
Description: Based on the Leaf reference from https://vapor.github.io/documentation/guide/leaf.html.
*/

function leaf(hljs) {
  return {
    name: 'Leaf',
    contains: [
      {
        className: 'function',
        begin: '#+' + '[A-Za-z_0-9]*' + '\\(',
        end: / \{/,
        returnBegin: true,
        excludeEnd: true,
        contains: [
          {
            className: 'keyword',
            begin: '#+'
          },
          {
            className: 'title',
            begin: '[A-Za-z_][A-Za-z_0-9]*'
          },
          {
            className: 'params',
            begin: '\\(',
            end: '\\)',
            endsParent: true,
            contains: [
              {
                className: 'string',
                begin: '"',
                end: '"'
              },
              {
                className: 'variable',
                begin: '[A-Za-z_][A-Za-z_0-9]*'
              }
            ]
          }
        ]
      }
    ]
  };
}

module.exports = leaf;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfbGVhZi5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsaUJBQWlCO0FBQ2pCO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFdBQVc7QUFDWDtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxlQUFlO0FBQ2Y7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvbGVhZi5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKlxuTGFuZ3VhZ2U6IExlYWZcbkF1dGhvcjogSGFsZSBDaGFuIDxoYWxlY2hhbkBxcS5jb20+XG5EZXNjcmlwdGlvbjogQmFzZWQgb24gdGhlIExlYWYgcmVmZXJlbmNlIGZyb20gaHR0cHM6Ly92YXBvci5naXRodWIuaW8vZG9jdW1lbnRhdGlvbi9ndWlkZS9sZWFmLmh0bWwuXG4qL1xuXG5mdW5jdGlvbiBsZWFmKGhsanMpIHtcbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnTGVhZicsXG4gICAgY29udGFpbnM6IFtcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnZnVuY3Rpb24nLFxuICAgICAgICBiZWdpbjogJyMrJyArICdbQS1aYS16XzAtOV0qJyArICdcXFxcKCcsXG4gICAgICAgIGVuZDogLyBcXHsvLFxuICAgICAgICByZXR1cm5CZWdpbjogdHJ1ZSxcbiAgICAgICAgZXhjbHVkZUVuZDogdHJ1ZSxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBjbGFzc05hbWU6ICdrZXl3b3JkJyxcbiAgICAgICAgICAgIGJlZ2luOiAnIysnXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICBjbGFzc05hbWU6ICd0aXRsZScsXG4gICAgICAgICAgICBiZWdpbjogJ1tBLVphLXpfXVtBLVphLXpfMC05XSonXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICBjbGFzc05hbWU6ICdwYXJhbXMnLFxuICAgICAgICAgICAgYmVnaW46ICdcXFxcKCcsXG4gICAgICAgICAgICBlbmQ6ICdcXFxcKScsXG4gICAgICAgICAgICBlbmRzUGFyZW50OiB0cnVlLFxuICAgICAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICAgICAge1xuICAgICAgICAgICAgICAgIGNsYXNzTmFtZTogJ3N0cmluZycsXG4gICAgICAgICAgICAgICAgYmVnaW46ICdcIicsXG4gICAgICAgICAgICAgICAgZW5kOiAnXCInXG4gICAgICAgICAgICAgIH0sXG4gICAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgICBjbGFzc05hbWU6ICd2YXJpYWJsZScsXG4gICAgICAgICAgICAgICAgYmVnaW46ICdbQS1aYS16X11bQS1aYS16XzAtOV0qJ1xuICAgICAgICAgICAgICB9XG4gICAgICAgICAgICBdXG4gICAgICAgICAgfVxuICAgICAgICBdXG4gICAgICB9XG4gICAgXVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IGxlYWY7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=