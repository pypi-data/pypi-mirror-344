(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_pythonRepl"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/python-repl.js":
/*!******************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/python-repl.js ***!
  \******************************************************************************************************/
/***/ ((module) => {

/*
Language: Python REPL
Requires: python.js
Author: Josh Goebel <hello@joshgoebel.com>
Category: common
*/

function pythonRepl(hljs) {
  return {
    aliases: [ 'pycon' ],
    contains: [
      {
        className: 'meta',
        starts: {
          // a space separates the REPL prefix from the actual code
          // this is purely for cleaner HTML output
          end: / |$/,
          starts: {
            end: '$',
            subLanguage: 'python'
          }
        },
        variants: [
          {
            begin: /^>>>(?=[ ]|$)/
          },
          {
            begin: /^\.\.\.(?=[ ]|$)/
          }
        ]
      }
    ]
  };
}

module.exports = pythonRepl;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfcHl0aG9uUmVwbC5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFNBQVM7QUFDVDtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvcHl0aG9uLXJlcGwuanMiXSwic291cmNlc0NvbnRlbnQiOlsiLypcbkxhbmd1YWdlOiBQeXRob24gUkVQTFxuUmVxdWlyZXM6IHB5dGhvbi5qc1xuQXV0aG9yOiBKb3NoIEdvZWJlbCA8aGVsbG9Aam9zaGdvZWJlbC5jb20+XG5DYXRlZ29yeTogY29tbW9uXG4qL1xuXG5mdW5jdGlvbiBweXRob25SZXBsKGhsanMpIHtcbiAgcmV0dXJuIHtcbiAgICBhbGlhc2VzOiBbICdweWNvbicgXSxcbiAgICBjb250YWluczogW1xuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdtZXRhJyxcbiAgICAgICAgc3RhcnRzOiB7XG4gICAgICAgICAgLy8gYSBzcGFjZSBzZXBhcmF0ZXMgdGhlIFJFUEwgcHJlZml4IGZyb20gdGhlIGFjdHVhbCBjb2RlXG4gICAgICAgICAgLy8gdGhpcyBpcyBwdXJlbHkgZm9yIGNsZWFuZXIgSFRNTCBvdXRwdXRcbiAgICAgICAgICBlbmQ6IC8gfCQvLFxuICAgICAgICAgIHN0YXJ0czoge1xuICAgICAgICAgICAgZW5kOiAnJCcsXG4gICAgICAgICAgICBzdWJMYW5ndWFnZTogJ3B5dGhvbidcbiAgICAgICAgICB9XG4gICAgICAgIH0sXG4gICAgICAgIHZhcmlhbnRzOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgYmVnaW46IC9ePj4+KD89WyBdfCQpL1xuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgYmVnaW46IC9eXFwuXFwuXFwuKD89WyBdfCQpL1xuICAgICAgICAgIH1cbiAgICAgICAgXVxuICAgICAgfVxuICAgIF1cbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBweXRob25SZXBsO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9