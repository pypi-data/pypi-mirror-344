(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_tcl"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/tcl.js":
/*!**********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/tcl.js ***!
  \**********************************************************************************************/
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
 * @param {RegExp | string } re
 * @returns {string}
 */
function optional(re) {
  return concat('(', re, ')?');
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
Language: Tcl
Description: Tcl is a very simple programming language.
Author: Radek Liska <radekliska@gmail.com>
Website: https://www.tcl.tk/about/language.html
*/

function tcl(hljs) {
  const TCL_IDENT = /[a-zA-Z_][a-zA-Z0-9_]*/;

  const NUMBER = {
    className: 'number',
    variants: [hljs.BINARY_NUMBER_MODE, hljs.C_NUMBER_MODE]
  };

  return {
    name: 'Tcl',
    aliases: ['tk'],
    keywords: 'after append apply array auto_execok auto_import auto_load auto_mkindex ' +
      'auto_mkindex_old auto_qualify auto_reset bgerror binary break catch cd chan clock ' +
      'close concat continue dde dict encoding eof error eval exec exit expr fblocked ' +
      'fconfigure fcopy file fileevent filename flush for foreach format gets glob global ' +
      'history http if incr info interp join lappend|10 lassign|10 lindex|10 linsert|10 list ' +
      'llength|10 load lrange|10 lrepeat|10 lreplace|10 lreverse|10 lsearch|10 lset|10 lsort|10 '+
      'mathfunc mathop memory msgcat namespace open package parray pid pkg::create pkg_mkIndex '+
      'platform platform::shell proc puts pwd read refchan regexp registry regsub|10 rename '+
      'return safe scan seek set socket source split string subst switch tcl_endOfWord '+
      'tcl_findLibrary tcl_startOfNextWord tcl_startOfPreviousWord tcl_wordBreakAfter '+
      'tcl_wordBreakBefore tcltest tclvars tell time tm trace unknown unload unset update '+
      'uplevel upvar variable vwait while',
    contains: [
      hljs.COMMENT(';[ \\t]*#', '$'),
      hljs.COMMENT('^[ \\t]*#', '$'),
      {
        beginKeywords: 'proc',
        end: '[\\{]',
        excludeEnd: true,
        contains: [
          {
            className: 'title',
            begin: '[ \\t\\n\\r]+(::)?[a-zA-Z_]((::)?[a-zA-Z0-9_])*',
            end: '[ \\t\\n\\r]',
            endsWithParent: true,
            excludeEnd: true
          }
        ]
      },
      {
        className: "variable",
        variants: [
          {
            begin: concat(
              /\$/,
              optional(/::/),
              TCL_IDENT,
              '(::',
              TCL_IDENT,
              ')*'
            )
          },
          {
            begin: '\\$\\{(::)?[a-zA-Z_]((::)?[a-zA-Z0-9_])*',
            end: '\\}',
            contains: [
              NUMBER
            ]
          }
        ]
      },
      {
        className: 'string',
        contains: [hljs.BACKSLASH_ESCAPE],
        variants: [
          hljs.inherit(hljs.QUOTE_STRING_MODE, {illegal: null})
        ]
      },
      NUMBER
    ]
  }
}

module.exports = tcl;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfdGNsLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0EsV0FBVyxRQUFRO0FBQ25CLGFBQWE7QUFDYjs7QUFFQTtBQUNBLFdBQVcsa0JBQWtCO0FBQzdCLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBOztBQUVBO0FBQ0EsV0FBVyxrQkFBa0I7QUFDN0IsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0EsV0FBVyx1QkFBdUI7QUFDbEMsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxxQkFBcUI7QUFDckI7QUFDQTtBQUNBO0FBQ0Esa0JBQWtCO0FBQ2xCO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFdBQVc7QUFDWDtBQUNBLDBCQUEwQjtBQUMxQixxQkFBcUI7QUFDckI7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBLGdEQUFnRCxjQUFjO0FBQzlEO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy90Y2wuanMiXSwic291cmNlc0NvbnRlbnQiOlsiLyoqXG4gKiBAcGFyYW0ge3N0cmluZ30gdmFsdWVcbiAqIEByZXR1cm5zIHtSZWdFeHB9XG4gKiAqL1xuXG4vKipcbiAqIEBwYXJhbSB7UmVnRXhwIHwgc3RyaW5nIH0gcmVcbiAqIEByZXR1cm5zIHtzdHJpbmd9XG4gKi9cbmZ1bmN0aW9uIHNvdXJjZShyZSkge1xuICBpZiAoIXJlKSByZXR1cm4gbnVsbDtcbiAgaWYgKHR5cGVvZiByZSA9PT0gXCJzdHJpbmdcIikgcmV0dXJuIHJlO1xuXG4gIHJldHVybiByZS5zb3VyY2U7XG59XG5cbi8qKlxuICogQHBhcmFtIHtSZWdFeHAgfCBzdHJpbmcgfSByZVxuICogQHJldHVybnMge3N0cmluZ31cbiAqL1xuZnVuY3Rpb24gb3B0aW9uYWwocmUpIHtcbiAgcmV0dXJuIGNvbmNhdCgnKCcsIHJlLCAnKT8nKTtcbn1cblxuLyoqXG4gKiBAcGFyYW0gey4uLihSZWdFeHAgfCBzdHJpbmcpIH0gYXJnc1xuICogQHJldHVybnMge3N0cmluZ31cbiAqL1xuZnVuY3Rpb24gY29uY2F0KC4uLmFyZ3MpIHtcbiAgY29uc3Qgam9pbmVkID0gYXJncy5tYXAoKHgpID0+IHNvdXJjZSh4KSkuam9pbihcIlwiKTtcbiAgcmV0dXJuIGpvaW5lZDtcbn1cblxuLypcbkxhbmd1YWdlOiBUY2xcbkRlc2NyaXB0aW9uOiBUY2wgaXMgYSB2ZXJ5IHNpbXBsZSBwcm9ncmFtbWluZyBsYW5ndWFnZS5cbkF1dGhvcjogUmFkZWsgTGlza2EgPHJhZGVrbGlza2FAZ21haWwuY29tPlxuV2Vic2l0ZTogaHR0cHM6Ly93d3cudGNsLnRrL2Fib3V0L2xhbmd1YWdlLmh0bWxcbiovXG5cbmZ1bmN0aW9uIHRjbChobGpzKSB7XG4gIGNvbnN0IFRDTF9JREVOVCA9IC9bYS16QS1aX11bYS16QS1aMC05X10qLztcblxuICBjb25zdCBOVU1CRVIgPSB7XG4gICAgY2xhc3NOYW1lOiAnbnVtYmVyJyxcbiAgICB2YXJpYW50czogW2hsanMuQklOQVJZX05VTUJFUl9NT0RFLCBobGpzLkNfTlVNQkVSX01PREVdXG4gIH07XG5cbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnVGNsJyxcbiAgICBhbGlhc2VzOiBbJ3RrJ10sXG4gICAga2V5d29yZHM6ICdhZnRlciBhcHBlbmQgYXBwbHkgYXJyYXkgYXV0b19leGVjb2sgYXV0b19pbXBvcnQgYXV0b19sb2FkIGF1dG9fbWtpbmRleCAnICtcbiAgICAgICdhdXRvX21raW5kZXhfb2xkIGF1dG9fcXVhbGlmeSBhdXRvX3Jlc2V0IGJnZXJyb3IgYmluYXJ5IGJyZWFrIGNhdGNoIGNkIGNoYW4gY2xvY2sgJyArXG4gICAgICAnY2xvc2UgY29uY2F0IGNvbnRpbnVlIGRkZSBkaWN0IGVuY29kaW5nIGVvZiBlcnJvciBldmFsIGV4ZWMgZXhpdCBleHByIGZibG9ja2VkICcgK1xuICAgICAgJ2Zjb25maWd1cmUgZmNvcHkgZmlsZSBmaWxlZXZlbnQgZmlsZW5hbWUgZmx1c2ggZm9yIGZvcmVhY2ggZm9ybWF0IGdldHMgZ2xvYiBnbG9iYWwgJyArXG4gICAgICAnaGlzdG9yeSBodHRwIGlmIGluY3IgaW5mbyBpbnRlcnAgam9pbiBsYXBwZW5kfDEwIGxhc3NpZ258MTAgbGluZGV4fDEwIGxpbnNlcnR8MTAgbGlzdCAnICtcbiAgICAgICdsbGVuZ3RofDEwIGxvYWQgbHJhbmdlfDEwIGxyZXBlYXR8MTAgbHJlcGxhY2V8MTAgbHJldmVyc2V8MTAgbHNlYXJjaHwxMCBsc2V0fDEwIGxzb3J0fDEwICcrXG4gICAgICAnbWF0aGZ1bmMgbWF0aG9wIG1lbW9yeSBtc2djYXQgbmFtZXNwYWNlIG9wZW4gcGFja2FnZSBwYXJyYXkgcGlkIHBrZzo6Y3JlYXRlIHBrZ19ta0luZGV4ICcrXG4gICAgICAncGxhdGZvcm0gcGxhdGZvcm06OnNoZWxsIHByb2MgcHV0cyBwd2QgcmVhZCByZWZjaGFuIHJlZ2V4cCByZWdpc3RyeSByZWdzdWJ8MTAgcmVuYW1lICcrXG4gICAgICAncmV0dXJuIHNhZmUgc2NhbiBzZWVrIHNldCBzb2NrZXQgc291cmNlIHNwbGl0IHN0cmluZyBzdWJzdCBzd2l0Y2ggdGNsX2VuZE9mV29yZCAnK1xuICAgICAgJ3RjbF9maW5kTGlicmFyeSB0Y2xfc3RhcnRPZk5leHRXb3JkIHRjbF9zdGFydE9mUHJldmlvdXNXb3JkIHRjbF93b3JkQnJlYWtBZnRlciAnK1xuICAgICAgJ3RjbF93b3JkQnJlYWtCZWZvcmUgdGNsdGVzdCB0Y2x2YXJzIHRlbGwgdGltZSB0bSB0cmFjZSB1bmtub3duIHVubG9hZCB1bnNldCB1cGRhdGUgJytcbiAgICAgICd1cGxldmVsIHVwdmFyIHZhcmlhYmxlIHZ3YWl0IHdoaWxlJyxcbiAgICBjb250YWluczogW1xuICAgICAgaGxqcy5DT01NRU5UKCc7WyBcXFxcdF0qIycsICckJyksXG4gICAgICBobGpzLkNPTU1FTlQoJ15bIFxcXFx0XSojJywgJyQnKSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW5LZXl3b3JkczogJ3Byb2MnLFxuICAgICAgICBlbmQ6ICdbXFxcXHtdJyxcbiAgICAgICAgZXhjbHVkZUVuZDogdHJ1ZSxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBjbGFzc05hbWU6ICd0aXRsZScsXG4gICAgICAgICAgICBiZWdpbjogJ1sgXFxcXHRcXFxcblxcXFxyXSsoOjopP1thLXpBLVpfXSgoOjopP1thLXpBLVowLTlfXSkqJyxcbiAgICAgICAgICAgIGVuZDogJ1sgXFxcXHRcXFxcblxcXFxyXScsXG4gICAgICAgICAgICBlbmRzV2l0aFBhcmVudDogdHJ1ZSxcbiAgICAgICAgICAgIGV4Y2x1ZGVFbmQ6IHRydWVcbiAgICAgICAgICB9XG4gICAgICAgIF1cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogXCJ2YXJpYWJsZVwiLFxuICAgICAgICB2YXJpYW50czogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiBjb25jYXQoXG4gICAgICAgICAgICAgIC9cXCQvLFxuICAgICAgICAgICAgICBvcHRpb25hbCgvOjovKSxcbiAgICAgICAgICAgICAgVENMX0lERU5ULFxuICAgICAgICAgICAgICAnKDo6JyxcbiAgICAgICAgICAgICAgVENMX0lERU5ULFxuICAgICAgICAgICAgICAnKSonXG4gICAgICAgICAgICApXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbjogJ1xcXFwkXFxcXHsoOjopP1thLXpBLVpfXSgoOjopP1thLXpBLVowLTlfXSkqJyxcbiAgICAgICAgICAgIGVuZDogJ1xcXFx9JyxcbiAgICAgICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgICAgIE5VTUJFUlxuICAgICAgICAgICAgXVxuICAgICAgICAgIH1cbiAgICAgICAgXVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICAgICAgY29udGFpbnM6IFtobGpzLkJBQ0tTTEFTSF9FU0NBUEVdLFxuICAgICAgICB2YXJpYW50czogW1xuICAgICAgICAgIGhsanMuaW5oZXJpdChobGpzLlFVT1RFX1NUUklOR19NT0RFLCB7aWxsZWdhbDogbnVsbH0pXG4gICAgICAgIF1cbiAgICAgIH0sXG4gICAgICBOVU1CRVJcbiAgICBdXG4gIH1cbn1cblxubW9kdWxlLmV4cG9ydHMgPSB0Y2w7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=