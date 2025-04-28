(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_nodeRepl"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/node-repl.js":
/*!****************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/node-repl.js ***!
  \****************************************************************************************************/
/***/ ((module) => {

/*
Language: Node REPL
Requires: javascript.js
Author: Marat Nagayev <nagaevmt@yandex.ru>
Category: scripting
*/

/** @type LanguageFn */
function nodeRepl(hljs) {
  return {
    name: 'Node REPL',
    contains: [
      {
        className: 'meta',
        starts: {
          // a space separates the REPL prefix from the actual code
          // this is purely for cleaner HTML output
          end: / |$/,
          starts: {
            end: '$',
            subLanguage: 'javascript'
          }
        },
        variants: [
          {
            begin: /^>(?=[ ]|$)/
          },
          {
            begin: /^\.\.\.(?=[ ]|$)/
          }
        ]
      }
    ]
  };
}

module.exports = nodeRepl;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfbm9kZVJlcGwuZHRhbGVfYnVuZGxlLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFNBQVM7QUFDVDtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvbm9kZS1yZXBsLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogTm9kZSBSRVBMXG5SZXF1aXJlczogamF2YXNjcmlwdC5qc1xuQXV0aG9yOiBNYXJhdCBOYWdheWV2IDxuYWdhZXZtdEB5YW5kZXgucnU+XG5DYXRlZ29yeTogc2NyaXB0aW5nXG4qL1xuXG4vKiogQHR5cGUgTGFuZ3VhZ2VGbiAqL1xuZnVuY3Rpb24gbm9kZVJlcGwoaGxqcykge1xuICByZXR1cm4ge1xuICAgIG5hbWU6ICdOb2RlIFJFUEwnLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ21ldGEnLFxuICAgICAgICBzdGFydHM6IHtcbiAgICAgICAgICAvLyBhIHNwYWNlIHNlcGFyYXRlcyB0aGUgUkVQTCBwcmVmaXggZnJvbSB0aGUgYWN0dWFsIGNvZGVcbiAgICAgICAgICAvLyB0aGlzIGlzIHB1cmVseSBmb3IgY2xlYW5lciBIVE1MIG91dHB1dFxuICAgICAgICAgIGVuZDogLyB8JC8sXG4gICAgICAgICAgc3RhcnRzOiB7XG4gICAgICAgICAgICBlbmQ6ICckJyxcbiAgICAgICAgICAgIHN1Ykxhbmd1YWdlOiAnamF2YXNjcmlwdCdcbiAgICAgICAgICB9XG4gICAgICAgIH0sXG4gICAgICAgIHZhcmlhbnRzOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgYmVnaW46IC9ePig/PVsgXXwkKS9cbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiAvXlxcLlxcLlxcLig/PVsgXXwkKS9cbiAgICAgICAgICB9XG4gICAgICAgIF1cbiAgICAgIH1cbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gbm9kZVJlcGw7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=