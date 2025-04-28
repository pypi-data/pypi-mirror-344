(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_clojureRepl"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/clojure-repl.js":
/*!*******************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/clojure-repl.js ***!
  \*******************************************************************************************************/
/***/ ((module) => {

/*
Language: Clojure REPL
Description: Clojure REPL sessions
Author: Ivan Sagalaev <maniac@softwaremaniacs.org>
Requires: clojure.js
Website: https://clojure.org
Category: lisp
*/

/** @type LanguageFn */
function clojureRepl(hljs) {
  return {
    name: 'Clojure REPL',
    contains: [
      {
        className: 'meta',
        begin: /^([\w.-]+|\s*#_)?=>/,
        starts: {
          end: /$/,
          subLanguage: 'clojure'
        }
      }
    ]
  };
}

module.exports = clojureRepl;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfY2xvanVyZVJlcGwuZHRhbGVfYnVuZGxlLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvY2xvanVyZS1yZXBsLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogQ2xvanVyZSBSRVBMXG5EZXNjcmlwdGlvbjogQ2xvanVyZSBSRVBMIHNlc3Npb25zXG5BdXRob3I6IEl2YW4gU2FnYWxhZXYgPG1hbmlhY0Bzb2Z0d2FyZW1hbmlhY3Mub3JnPlxuUmVxdWlyZXM6IGNsb2p1cmUuanNcbldlYnNpdGU6IGh0dHBzOi8vY2xvanVyZS5vcmdcbkNhdGVnb3J5OiBsaXNwXG4qL1xuXG4vKiogQHR5cGUgTGFuZ3VhZ2VGbiAqL1xuZnVuY3Rpb24gY2xvanVyZVJlcGwoaGxqcykge1xuICByZXR1cm4ge1xuICAgIG5hbWU6ICdDbG9qdXJlIFJFUEwnLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ21ldGEnLFxuICAgICAgICBiZWdpbjogL14oW1xcdy4tXSt8XFxzKiNfKT89Pi8sXG4gICAgICAgIHN0YXJ0czoge1xuICAgICAgICAgIGVuZDogLyQvLFxuICAgICAgICAgIHN1Ykxhbmd1YWdlOiAnY2xvanVyZSdcbiAgICAgICAgfVxuICAgICAgfVxuICAgIF1cbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBjbG9qdXJlUmVwbDtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==