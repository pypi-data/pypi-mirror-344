(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_shell"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/shell.js":
/*!************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/shell.js ***!
  \************************************************************************************************/
/***/ ((module) => {

/*
Language: Shell Session
Requires: bash.js
Author: TSUYUSATO Kitsune <make.just.on@gmail.com>
Category: common
Audit: 2020
*/

/** @type LanguageFn */
function shell(hljs) {
  return {
    name: 'Shell Session',
    aliases: [ 'console' ],
    contains: [
      {
        className: 'meta',
        // We cannot add \s (spaces) in the regular expression otherwise it will be too broad and produce unexpected result.
        // For instance, in the following example, it would match "echo /path/to/home >" as a prompt:
        // echo /path/to/home > t.exe
        begin: /^\s{0,3}[/~\w\d[\]()@-]*[>%$#]/,
        starts: {
          end: /[^\\](?=\s*$)/,
          subLanguage: 'bash'
        }
      }
    ]
  };
}

module.exports = shell;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfc2hlbGwuZHRhbGVfYnVuZGxlLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLG9CQUFvQixJQUFJO0FBQ3hCO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL3NoZWxsLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogU2hlbGwgU2Vzc2lvblxuUmVxdWlyZXM6IGJhc2guanNcbkF1dGhvcjogVFNVWVVTQVRPIEtpdHN1bmUgPG1ha2UuanVzdC5vbkBnbWFpbC5jb20+XG5DYXRlZ29yeTogY29tbW9uXG5BdWRpdDogMjAyMFxuKi9cblxuLyoqIEB0eXBlIExhbmd1YWdlRm4gKi9cbmZ1bmN0aW9uIHNoZWxsKGhsanMpIHtcbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnU2hlbGwgU2Vzc2lvbicsXG4gICAgYWxpYXNlczogWyAnY29uc29sZScgXSxcbiAgICBjb250YWluczogW1xuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdtZXRhJyxcbiAgICAgICAgLy8gV2UgY2Fubm90IGFkZCBcXHMgKHNwYWNlcykgaW4gdGhlIHJlZ3VsYXIgZXhwcmVzc2lvbiBvdGhlcndpc2UgaXQgd2lsbCBiZSB0b28gYnJvYWQgYW5kIHByb2R1Y2UgdW5leHBlY3RlZCByZXN1bHQuXG4gICAgICAgIC8vIEZvciBpbnN0YW5jZSwgaW4gdGhlIGZvbGxvd2luZyBleGFtcGxlLCBpdCB3b3VsZCBtYXRjaCBcImVjaG8gL3BhdGgvdG8vaG9tZSA+XCIgYXMgYSBwcm9tcHQ6XG4gICAgICAgIC8vIGVjaG8gL3BhdGgvdG8vaG9tZSA+IHQuZXhlXG4gICAgICAgIGJlZ2luOiAvXlxcc3swLDN9Wy9+XFx3XFxkW1xcXSgpQC1dKls+JSQjXS8sXG4gICAgICAgIHN0YXJ0czoge1xuICAgICAgICAgIGVuZDogL1teXFxcXF0oPz1cXHMqJCkvLFxuICAgICAgICAgIHN1Ykxhbmd1YWdlOiAnYmFzaCdcbiAgICAgICAgfVxuICAgICAgfVxuICAgIF1cbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBzaGVsbDtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==