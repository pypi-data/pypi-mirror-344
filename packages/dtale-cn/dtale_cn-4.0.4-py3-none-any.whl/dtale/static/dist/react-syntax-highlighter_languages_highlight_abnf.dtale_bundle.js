(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_abnf"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/abnf.js":
/*!***********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/abnf.js ***!
  \***********************************************************************************************/
/***/ ((module) => {

/**
 * @param {string} value
 * @returns {RegExp}
 * */

/**
 * @param {RegExp | string } re
 * @returns {string}
 */
function source(re) {
  if (!re) return null;
  if (typeof re === "string") return re;

  return re.source;
}

/**
 * @param {...(RegExp | string) } args
 * @returns {string}
 */
function concat(...args) {
  const joined = args.map((x) => source(x)).join("");
  return joined;
}

/*
Language: Augmented Backus-Naur Form
Author: Alex McKibben <alex@nullscope.net>
Website: https://tools.ietf.org/html/rfc5234
Audit: 2020
*/

/** @type LanguageFn */
function abnf(hljs) {
  const regexes = {
    ruleDeclaration: /^[a-zA-Z][a-zA-Z0-9-]*/,
    unexpectedChars: /[!@#$^&',?+~`|:]/
  };

  const keywords = [
    "ALPHA",
    "BIT",
    "CHAR",
    "CR",
    "CRLF",
    "CTL",
    "DIGIT",
    "DQUOTE",
    "HEXDIG",
    "HTAB",
    "LF",
    "LWSP",
    "OCTET",
    "SP",
    "VCHAR",
    "WSP"
  ];

  const commentMode = hljs.COMMENT(/;/, /$/);

  const terminalBinaryMode = {
    className: "symbol",
    begin: /%b[0-1]+(-[0-1]+|(\.[0-1]+)+){0,1}/
  };

  const terminalDecimalMode = {
    className: "symbol",
    begin: /%d[0-9]+(-[0-9]+|(\.[0-9]+)+){0,1}/
  };

  const terminalHexadecimalMode = {
    className: "symbol",
    begin: /%x[0-9A-F]+(-[0-9A-F]+|(\.[0-9A-F]+)+){0,1}/
  };

  const caseSensitivityIndicatorMode = {
    className: "symbol",
    begin: /%[si]/
  };

  const ruleDeclarationMode = {
    className: "attribute",
    begin: concat(regexes.ruleDeclaration, /(?=\s*=)/)
  };

  return {
    name: 'Augmented Backus-Naur Form',
    illegal: regexes.unexpectedChars,
    keywords: keywords,
    contains: [
      ruleDeclarationMode,
      commentMode,
      terminalBinaryMode,
      terminalDecimalMode,
      terminalHexadecimalMode,
      caseSensitivityIndicatorMode,
      hljs.QUOTE_STRING_MODE,
      hljs.NUMBER_MODE
    ]
  };
}

module.exports = abnf;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfYWJuZi5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBLFdBQVcsUUFBUTtBQUNuQixhQUFhO0FBQ2I7O0FBRUE7QUFDQSxXQUFXLGtCQUFrQjtBQUM3QixhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTs7QUFFQTtBQUNBLFdBQVcsdUJBQXVCO0FBQ2xDLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBLHFDQUFxQzs7QUFFckM7QUFDQTtBQUNBLDBDQUEwQyxJQUFJO0FBQzlDOztBQUVBO0FBQ0E7QUFDQSwwQ0FBMEMsSUFBSTtBQUM5Qzs7QUFFQTtBQUNBO0FBQ0EsbURBQW1ELElBQUk7QUFDdkQ7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL2FibmYuanMiXSwic291cmNlc0NvbnRlbnQiOlsiLyoqXG4gKiBAcGFyYW0ge3N0cmluZ30gdmFsdWVcbiAqIEByZXR1cm5zIHtSZWdFeHB9XG4gKiAqL1xuXG4vKipcbiAqIEBwYXJhbSB7UmVnRXhwIHwgc3RyaW5nIH0gcmVcbiAqIEByZXR1cm5zIHtzdHJpbmd9XG4gKi9cbmZ1bmN0aW9uIHNvdXJjZShyZSkge1xuICBpZiAoIXJlKSByZXR1cm4gbnVsbDtcbiAgaWYgKHR5cGVvZiByZSA9PT0gXCJzdHJpbmdcIikgcmV0dXJuIHJlO1xuXG4gIHJldHVybiByZS5zb3VyY2U7XG59XG5cbi8qKlxuICogQHBhcmFtIHsuLi4oUmVnRXhwIHwgc3RyaW5nKSB9IGFyZ3NcbiAqIEByZXR1cm5zIHtzdHJpbmd9XG4gKi9cbmZ1bmN0aW9uIGNvbmNhdCguLi5hcmdzKSB7XG4gIGNvbnN0IGpvaW5lZCA9IGFyZ3MubWFwKCh4KSA9PiBzb3VyY2UoeCkpLmpvaW4oXCJcIik7XG4gIHJldHVybiBqb2luZWQ7XG59XG5cbi8qXG5MYW5ndWFnZTogQXVnbWVudGVkIEJhY2t1cy1OYXVyIEZvcm1cbkF1dGhvcjogQWxleCBNY0tpYmJlbiA8YWxleEBudWxsc2NvcGUubmV0PlxuV2Vic2l0ZTogaHR0cHM6Ly90b29scy5pZXRmLm9yZy9odG1sL3JmYzUyMzRcbkF1ZGl0OiAyMDIwXG4qL1xuXG4vKiogQHR5cGUgTGFuZ3VhZ2VGbiAqL1xuZnVuY3Rpb24gYWJuZihobGpzKSB7XG4gIGNvbnN0IHJlZ2V4ZXMgPSB7XG4gICAgcnVsZURlY2xhcmF0aW9uOiAvXlthLXpBLVpdW2EtekEtWjAtOS1dKi8sXG4gICAgdW5leHBlY3RlZENoYXJzOiAvWyFAIyReJicsPyt+YHw6XS9cbiAgfTtcblxuICBjb25zdCBrZXl3b3JkcyA9IFtcbiAgICBcIkFMUEhBXCIsXG4gICAgXCJCSVRcIixcbiAgICBcIkNIQVJcIixcbiAgICBcIkNSXCIsXG4gICAgXCJDUkxGXCIsXG4gICAgXCJDVExcIixcbiAgICBcIkRJR0lUXCIsXG4gICAgXCJEUVVPVEVcIixcbiAgICBcIkhFWERJR1wiLFxuICAgIFwiSFRBQlwiLFxuICAgIFwiTEZcIixcbiAgICBcIkxXU1BcIixcbiAgICBcIk9DVEVUXCIsXG4gICAgXCJTUFwiLFxuICAgIFwiVkNIQVJcIixcbiAgICBcIldTUFwiXG4gIF07XG5cbiAgY29uc3QgY29tbWVudE1vZGUgPSBobGpzLkNPTU1FTlQoLzsvLCAvJC8pO1xuXG4gIGNvbnN0IHRlcm1pbmFsQmluYXJ5TW9kZSA9IHtcbiAgICBjbGFzc05hbWU6IFwic3ltYm9sXCIsXG4gICAgYmVnaW46IC8lYlswLTFdKygtWzAtMV0rfChcXC5bMC0xXSspKyl7MCwxfS9cbiAgfTtcblxuICBjb25zdCB0ZXJtaW5hbERlY2ltYWxNb2RlID0ge1xuICAgIGNsYXNzTmFtZTogXCJzeW1ib2xcIixcbiAgICBiZWdpbjogLyVkWzAtOV0rKC1bMC05XSt8KFxcLlswLTldKykrKXswLDF9L1xuICB9O1xuXG4gIGNvbnN0IHRlcm1pbmFsSGV4YWRlY2ltYWxNb2RlID0ge1xuICAgIGNsYXNzTmFtZTogXCJzeW1ib2xcIixcbiAgICBiZWdpbjogLyV4WzAtOUEtRl0rKC1bMC05QS1GXSt8KFxcLlswLTlBLUZdKykrKXswLDF9L1xuICB9O1xuXG4gIGNvbnN0IGNhc2VTZW5zaXRpdml0eUluZGljYXRvck1vZGUgPSB7XG4gICAgY2xhc3NOYW1lOiBcInN5bWJvbFwiLFxuICAgIGJlZ2luOiAvJVtzaV0vXG4gIH07XG5cbiAgY29uc3QgcnVsZURlY2xhcmF0aW9uTW9kZSA9IHtcbiAgICBjbGFzc05hbWU6IFwiYXR0cmlidXRlXCIsXG4gICAgYmVnaW46IGNvbmNhdChyZWdleGVzLnJ1bGVEZWNsYXJhdGlvbiwgLyg/PVxccyo9KS8pXG4gIH07XG5cbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnQXVnbWVudGVkIEJhY2t1cy1OYXVyIEZvcm0nLFxuICAgIGlsbGVnYWw6IHJlZ2V4ZXMudW5leHBlY3RlZENoYXJzLFxuICAgIGtleXdvcmRzOiBrZXl3b3JkcyxcbiAgICBjb250YWluczogW1xuICAgICAgcnVsZURlY2xhcmF0aW9uTW9kZSxcbiAgICAgIGNvbW1lbnRNb2RlLFxuICAgICAgdGVybWluYWxCaW5hcnlNb2RlLFxuICAgICAgdGVybWluYWxEZWNpbWFsTW9kZSxcbiAgICAgIHRlcm1pbmFsSGV4YWRlY2ltYWxNb2RlLFxuICAgICAgY2FzZVNlbnNpdGl2aXR5SW5kaWNhdG9yTW9kZSxcbiAgICAgIGhsanMuUVVPVEVfU1RSSU5HX01PREUsXG4gICAgICBobGpzLk5VTUJFUl9NT0RFXG4gICAgXVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IGFibmY7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=