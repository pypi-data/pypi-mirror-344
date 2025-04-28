(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_cos"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/cos.js":
/*!**********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/cos.js ***!
  \**********************************************************************************************/
/***/ ((module) => {

/*
Language: Caché Object Script
Author: Nikita Savchenko <zitros.lab@gmail.com>
Category: enterprise, scripting
Website: https://cedocs.intersystems.com/latest/csp/docbook/DocBook.UI.Page.cls
*/

/** @type LanguageFn */
function cos(hljs) {
  const STRINGS = {
    className: 'string',
    variants: [{
      begin: '"',
      end: '"',
      contains: [{ // escaped
        begin: "\"\"",
        relevance: 0
      }]
    }]
  };

  const NUMBERS = {
    className: "number",
    begin: "\\b(\\d+(\\.\\d*)?|\\.\\d+)",
    relevance: 0
  };

  const COS_KEYWORDS =
    'property parameter class classmethod clientmethod extends as break ' +
    'catch close continue do d|0 else elseif for goto halt hang h|0 if job ' +
    'j|0 kill k|0 lock l|0 merge new open quit q|0 read r|0 return set s|0 ' +
    'tcommit throw trollback try tstart use view while write w|0 xecute x|0 ' +
    'zkill znspace zn ztrap zwrite zw zzdump zzwrite print zbreak zinsert ' +
    'zload zprint zremove zsave zzprint mv mvcall mvcrt mvdim mvprint zquit ' +
    'zsync ascii';

  // registered function - no need in them due to all functions are highlighted,
  // but I'll just leave this here.

  // "$bit", "$bitcount",
  // "$bitfind", "$bitlogic", "$case", "$char", "$classmethod", "$classname",
  // "$compile", "$data", "$decimal", "$double", "$extract", "$factor",
  // "$find", "$fnumber", "$get", "$increment", "$inumber", "$isobject",
  // "$isvaliddouble", "$isvalidnum", "$justify", "$length", "$list",
  // "$listbuild", "$listdata", "$listfind", "$listfromstring", "$listget",
  // "$listlength", "$listnext", "$listsame", "$listtostring", "$listvalid",
  // "$locate", "$match", "$method", "$name", "$nconvert", "$next",
  // "$normalize", "$now", "$number", "$order", "$parameter", "$piece",
  // "$prefetchoff", "$prefetchon", "$property", "$qlength", "$qsubscript",
  // "$query", "$random", "$replace", "$reverse", "$sconvert", "$select",
  // "$sortbegin", "$sortend", "$stack", "$text", "$translate", "$view",
  // "$wascii", "$wchar", "$wextract", "$wfind", "$wiswide", "$wlength",
  // "$wreverse", "$xecute", "$zabs", "$zarccos", "$zarcsin", "$zarctan",
  // "$zcos", "$zcot", "$zcsc", "$zdate", "$zdateh", "$zdatetime",
  // "$zdatetimeh", "$zexp", "$zhex", "$zln", "$zlog", "$zpower", "$zsec",
  // "$zsin", "$zsqr", "$ztan", "$ztime", "$ztimeh", "$zboolean",
  // "$zconvert", "$zcrc", "$zcyc", "$zdascii", "$zdchar", "$zf",
  // "$ziswide", "$zlascii", "$zlchar", "$zname", "$zposition", "$zqascii",
  // "$zqchar", "$zsearch", "$zseek", "$zstrip", "$zwascii", "$zwchar",
  // "$zwidth", "$zwpack", "$zwbpack", "$zwunpack", "$zwbunpack", "$zzenkaku",
  // "$change", "$mv", "$mvat", "$mvfmt", "$mvfmts", "$mviconv",
  // "$mviconvs", "$mvinmat", "$mvlover", "$mvoconv", "$mvoconvs", "$mvraise",
  // "$mvtrans", "$mvv", "$mvname", "$zbitand", "$zbitcount", "$zbitfind",
  // "$zbitget", "$zbitlen", "$zbitnot", "$zbitor", "$zbitset", "$zbitstr",
  // "$zbitxor", "$zincrement", "$znext", "$zorder", "$zprevious", "$zsort",
  // "device", "$ecode", "$estack", "$etrap", "$halt", "$horolog",
  // "$io", "$job", "$key", "$namespace", "$principal", "$quit", "$roles",
  // "$storage", "$system", "$test", "$this", "$tlevel", "$username",
  // "$x", "$y", "$za", "$zb", "$zchild", "$zeof", "$zeos", "$zerror",
  // "$zhorolog", "$zio", "$zjob", "$zmode", "$znspace", "$zparent", "$zpi",
  // "$zpos", "$zreference", "$zstorage", "$ztimestamp", "$ztimezone",
  // "$ztrap", "$zversion"

  return {
    name: 'Caché Object Script',
    case_insensitive: true,
    aliases: [
      "cls"
    ],
    keywords: COS_KEYWORDS,
    contains: [
      NUMBERS,
      STRINGS,
      hljs.C_LINE_COMMENT_MODE,
      hljs.C_BLOCK_COMMENT_MODE,
      {
        className: "comment",
        begin: /;/,
        end: "$",
        relevance: 0
      },
      { // Functions and user-defined functions: write $ztime(60*60*3), $$myFunc(10), $$^Val(1)
        className: "built_in",
        begin: /(?:\$\$?|\.\.)\^?[a-zA-Z]+/
      },
      { // Macro command: quit $$$OK
        className: "built_in",
        begin: /\$\$\$[a-zA-Z]+/
      },
      { // Special (global) variables: write %request.Content; Built-in classes: %Library.Integer
        className: "built_in",
        begin: /%[a-z]+(?:\.[a-z]+)*/
      },
      { // Global variable: set ^globalName = 12 write ^globalName
        className: "symbol",
        begin: /\^%?[a-zA-Z][\w]*/
      },
      { // Some control constructions: do ##class(Package.ClassName).Method(), ##super()
        className: "keyword",
        begin: /##class|##super|#define|#dim/
      },
      // sub-languages: are not fully supported by hljs by 11/15/2015
      // left for the future implementation.
      {
        begin: /&sql\(/,
        end: /\)/,
        excludeBegin: true,
        excludeEnd: true,
        subLanguage: "sql"
      },
      {
        begin: /&(js|jscript|javascript)</,
        end: />/,
        excludeBegin: true,
        excludeEnd: true,
        subLanguage: "javascript"
      },
      {
        // this brakes first and last tag, but this is the only way to embed a valid html
        begin: /&html<\s*</,
        end: />\s*>/,
        subLanguage: "xml"
      }
    ]
  };
}

module.exports = cos;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfY29zLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLG1CQUFtQjtBQUNuQjtBQUNBO0FBQ0EsT0FBTztBQUNQLEtBQUs7QUFDTDs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLGlCQUFpQjtBQUNqQjtBQUNBO0FBQ0EsT0FBTztBQUNQLFFBQVE7QUFDUjtBQUNBO0FBQ0EsT0FBTztBQUNQLFFBQVE7QUFDUjtBQUNBO0FBQ0EsT0FBTztBQUNQLFFBQVEsdURBQXVEO0FBQy9EO0FBQ0E7QUFDQSxPQUFPO0FBQ1AsUUFBUTtBQUNSO0FBQ0E7QUFDQSxPQUFPO0FBQ1AsUUFBUTtBQUNSO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9jb3MuanMiXSwic291cmNlc0NvbnRlbnQiOlsiLypcbkxhbmd1YWdlOiBDYWNow6kgT2JqZWN0IFNjcmlwdFxuQXV0aG9yOiBOaWtpdGEgU2F2Y2hlbmtvIDx6aXRyb3MubGFiQGdtYWlsLmNvbT5cbkNhdGVnb3J5OiBlbnRlcnByaXNlLCBzY3JpcHRpbmdcbldlYnNpdGU6IGh0dHBzOi8vY2Vkb2NzLmludGVyc3lzdGVtcy5jb20vbGF0ZXN0L2NzcC9kb2Nib29rL0RvY0Jvb2suVUkuUGFnZS5jbHNcbiovXG5cbi8qKiBAdHlwZSBMYW5ndWFnZUZuICovXG5mdW5jdGlvbiBjb3MoaGxqcykge1xuICBjb25zdCBTVFJJTkdTID0ge1xuICAgIGNsYXNzTmFtZTogJ3N0cmluZycsXG4gICAgdmFyaWFudHM6IFt7XG4gICAgICBiZWdpbjogJ1wiJyxcbiAgICAgIGVuZDogJ1wiJyxcbiAgICAgIGNvbnRhaW5zOiBbeyAvLyBlc2NhcGVkXG4gICAgICAgIGJlZ2luOiBcIlxcXCJcXFwiXCIsXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfV1cbiAgICB9XVxuICB9O1xuXG4gIGNvbnN0IE5VTUJFUlMgPSB7XG4gICAgY2xhc3NOYW1lOiBcIm51bWJlclwiLFxuICAgIGJlZ2luOiBcIlxcXFxiKFxcXFxkKyhcXFxcLlxcXFxkKik/fFxcXFwuXFxcXGQrKVwiLFxuICAgIHJlbGV2YW5jZTogMFxuICB9O1xuXG4gIGNvbnN0IENPU19LRVlXT1JEUyA9XG4gICAgJ3Byb3BlcnR5IHBhcmFtZXRlciBjbGFzcyBjbGFzc21ldGhvZCBjbGllbnRtZXRob2QgZXh0ZW5kcyBhcyBicmVhayAnICtcbiAgICAnY2F0Y2ggY2xvc2UgY29udGludWUgZG8gZHwwIGVsc2UgZWxzZWlmIGZvciBnb3RvIGhhbHQgaGFuZyBofDAgaWYgam9iICcgK1xuICAgICdqfDAga2lsbCBrfDAgbG9jayBsfDAgbWVyZ2UgbmV3IG9wZW4gcXVpdCBxfDAgcmVhZCByfDAgcmV0dXJuIHNldCBzfDAgJyArXG4gICAgJ3Rjb21taXQgdGhyb3cgdHJvbGxiYWNrIHRyeSB0c3RhcnQgdXNlIHZpZXcgd2hpbGUgd3JpdGUgd3wwIHhlY3V0ZSB4fDAgJyArXG4gICAgJ3praWxsIHpuc3BhY2Ugem4genRyYXAgendyaXRlIHp3IHp6ZHVtcCB6endyaXRlIHByaW50IHpicmVhayB6aW5zZXJ0ICcgK1xuICAgICd6bG9hZCB6cHJpbnQgenJlbW92ZSB6c2F2ZSB6enByaW50IG12IG12Y2FsbCBtdmNydCBtdmRpbSBtdnByaW50IHpxdWl0ICcgK1xuICAgICd6c3luYyBhc2NpaSc7XG5cbiAgLy8gcmVnaXN0ZXJlZCBmdW5jdGlvbiAtIG5vIG5lZWQgaW4gdGhlbSBkdWUgdG8gYWxsIGZ1bmN0aW9ucyBhcmUgaGlnaGxpZ2h0ZWQsXG4gIC8vIGJ1dCBJJ2xsIGp1c3QgbGVhdmUgdGhpcyBoZXJlLlxuXG4gIC8vIFwiJGJpdFwiLCBcIiRiaXRjb3VudFwiLFxuICAvLyBcIiRiaXRmaW5kXCIsIFwiJGJpdGxvZ2ljXCIsIFwiJGNhc2VcIiwgXCIkY2hhclwiLCBcIiRjbGFzc21ldGhvZFwiLCBcIiRjbGFzc25hbWVcIixcbiAgLy8gXCIkY29tcGlsZVwiLCBcIiRkYXRhXCIsIFwiJGRlY2ltYWxcIiwgXCIkZG91YmxlXCIsIFwiJGV4dHJhY3RcIiwgXCIkZmFjdG9yXCIsXG4gIC8vIFwiJGZpbmRcIiwgXCIkZm51bWJlclwiLCBcIiRnZXRcIiwgXCIkaW5jcmVtZW50XCIsIFwiJGludW1iZXJcIiwgXCIkaXNvYmplY3RcIixcbiAgLy8gXCIkaXN2YWxpZGRvdWJsZVwiLCBcIiRpc3ZhbGlkbnVtXCIsIFwiJGp1c3RpZnlcIiwgXCIkbGVuZ3RoXCIsIFwiJGxpc3RcIixcbiAgLy8gXCIkbGlzdGJ1aWxkXCIsIFwiJGxpc3RkYXRhXCIsIFwiJGxpc3RmaW5kXCIsIFwiJGxpc3Rmcm9tc3RyaW5nXCIsIFwiJGxpc3RnZXRcIixcbiAgLy8gXCIkbGlzdGxlbmd0aFwiLCBcIiRsaXN0bmV4dFwiLCBcIiRsaXN0c2FtZVwiLCBcIiRsaXN0dG9zdHJpbmdcIiwgXCIkbGlzdHZhbGlkXCIsXG4gIC8vIFwiJGxvY2F0ZVwiLCBcIiRtYXRjaFwiLCBcIiRtZXRob2RcIiwgXCIkbmFtZVwiLCBcIiRuY29udmVydFwiLCBcIiRuZXh0XCIsXG4gIC8vIFwiJG5vcm1hbGl6ZVwiLCBcIiRub3dcIiwgXCIkbnVtYmVyXCIsIFwiJG9yZGVyXCIsIFwiJHBhcmFtZXRlclwiLCBcIiRwaWVjZVwiLFxuICAvLyBcIiRwcmVmZXRjaG9mZlwiLCBcIiRwcmVmZXRjaG9uXCIsIFwiJHByb3BlcnR5XCIsIFwiJHFsZW5ndGhcIiwgXCIkcXN1YnNjcmlwdFwiLFxuICAvLyBcIiRxdWVyeVwiLCBcIiRyYW5kb21cIiwgXCIkcmVwbGFjZVwiLCBcIiRyZXZlcnNlXCIsIFwiJHNjb252ZXJ0XCIsIFwiJHNlbGVjdFwiLFxuICAvLyBcIiRzb3J0YmVnaW5cIiwgXCIkc29ydGVuZFwiLCBcIiRzdGFja1wiLCBcIiR0ZXh0XCIsIFwiJHRyYW5zbGF0ZVwiLCBcIiR2aWV3XCIsXG4gIC8vIFwiJHdhc2NpaVwiLCBcIiR3Y2hhclwiLCBcIiR3ZXh0cmFjdFwiLCBcIiR3ZmluZFwiLCBcIiR3aXN3aWRlXCIsIFwiJHdsZW5ndGhcIixcbiAgLy8gXCIkd3JldmVyc2VcIiwgXCIkeGVjdXRlXCIsIFwiJHphYnNcIiwgXCIkemFyY2Nvc1wiLCBcIiR6YXJjc2luXCIsIFwiJHphcmN0YW5cIixcbiAgLy8gXCIkemNvc1wiLCBcIiR6Y290XCIsIFwiJHpjc2NcIiwgXCIkemRhdGVcIiwgXCIkemRhdGVoXCIsIFwiJHpkYXRldGltZVwiLFxuICAvLyBcIiR6ZGF0ZXRpbWVoXCIsIFwiJHpleHBcIiwgXCIkemhleFwiLCBcIiR6bG5cIiwgXCIkemxvZ1wiLCBcIiR6cG93ZXJcIiwgXCIkenNlY1wiLFxuICAvLyBcIiR6c2luXCIsIFwiJHpzcXJcIiwgXCIkenRhblwiLCBcIiR6dGltZVwiLCBcIiR6dGltZWhcIiwgXCIkemJvb2xlYW5cIixcbiAgLy8gXCIkemNvbnZlcnRcIiwgXCIkemNyY1wiLCBcIiR6Y3ljXCIsIFwiJHpkYXNjaWlcIiwgXCIkemRjaGFyXCIsIFwiJHpmXCIsXG4gIC8vIFwiJHppc3dpZGVcIiwgXCIkemxhc2NpaVwiLCBcIiR6bGNoYXJcIiwgXCIkem5hbWVcIiwgXCIkenBvc2l0aW9uXCIsIFwiJHpxYXNjaWlcIixcbiAgLy8gXCIkenFjaGFyXCIsIFwiJHpzZWFyY2hcIiwgXCIkenNlZWtcIiwgXCIkenN0cmlwXCIsIFwiJHp3YXNjaWlcIiwgXCIkendjaGFyXCIsXG4gIC8vIFwiJHp3aWR0aFwiLCBcIiR6d3BhY2tcIiwgXCIkendicGFja1wiLCBcIiR6d3VucGFja1wiLCBcIiR6d2J1bnBhY2tcIiwgXCIkenplbmtha3VcIixcbiAgLy8gXCIkY2hhbmdlXCIsIFwiJG12XCIsIFwiJG12YXRcIiwgXCIkbXZmbXRcIiwgXCIkbXZmbXRzXCIsIFwiJG12aWNvbnZcIixcbiAgLy8gXCIkbXZpY29udnNcIiwgXCIkbXZpbm1hdFwiLCBcIiRtdmxvdmVyXCIsIFwiJG12b2NvbnZcIiwgXCIkbXZvY29udnNcIiwgXCIkbXZyYWlzZVwiLFxuICAvLyBcIiRtdnRyYW5zXCIsIFwiJG12dlwiLCBcIiRtdm5hbWVcIiwgXCIkemJpdGFuZFwiLCBcIiR6Yml0Y291bnRcIiwgXCIkemJpdGZpbmRcIixcbiAgLy8gXCIkemJpdGdldFwiLCBcIiR6Yml0bGVuXCIsIFwiJHpiaXRub3RcIiwgXCIkemJpdG9yXCIsIFwiJHpiaXRzZXRcIiwgXCIkemJpdHN0clwiLFxuICAvLyBcIiR6Yml0eG9yXCIsIFwiJHppbmNyZW1lbnRcIiwgXCIkem5leHRcIiwgXCIkem9yZGVyXCIsIFwiJHpwcmV2aW91c1wiLCBcIiR6c29ydFwiLFxuICAvLyBcImRldmljZVwiLCBcIiRlY29kZVwiLCBcIiRlc3RhY2tcIiwgXCIkZXRyYXBcIiwgXCIkaGFsdFwiLCBcIiRob3JvbG9nXCIsXG4gIC8vIFwiJGlvXCIsIFwiJGpvYlwiLCBcIiRrZXlcIiwgXCIkbmFtZXNwYWNlXCIsIFwiJHByaW5jaXBhbFwiLCBcIiRxdWl0XCIsIFwiJHJvbGVzXCIsXG4gIC8vIFwiJHN0b3JhZ2VcIiwgXCIkc3lzdGVtXCIsIFwiJHRlc3RcIiwgXCIkdGhpc1wiLCBcIiR0bGV2ZWxcIiwgXCIkdXNlcm5hbWVcIixcbiAgLy8gXCIkeFwiLCBcIiR5XCIsIFwiJHphXCIsIFwiJHpiXCIsIFwiJHpjaGlsZFwiLCBcIiR6ZW9mXCIsIFwiJHplb3NcIiwgXCIkemVycm9yXCIsXG4gIC8vIFwiJHpob3JvbG9nXCIsIFwiJHppb1wiLCBcIiR6am9iXCIsIFwiJHptb2RlXCIsIFwiJHpuc3BhY2VcIiwgXCIkenBhcmVudFwiLCBcIiR6cGlcIixcbiAgLy8gXCIkenBvc1wiLCBcIiR6cmVmZXJlbmNlXCIsIFwiJHpzdG9yYWdlXCIsIFwiJHp0aW1lc3RhbXBcIiwgXCIkenRpbWV6b25lXCIsXG4gIC8vIFwiJHp0cmFwXCIsIFwiJHp2ZXJzaW9uXCJcblxuICByZXR1cm4ge1xuICAgIG5hbWU6ICdDYWNow6kgT2JqZWN0IFNjcmlwdCcsXG4gICAgY2FzZV9pbnNlbnNpdGl2ZTogdHJ1ZSxcbiAgICBhbGlhc2VzOiBbXG4gICAgICBcImNsc1wiXG4gICAgXSxcbiAgICBrZXl3b3JkczogQ09TX0tFWVdPUkRTLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBOVU1CRVJTLFxuICAgICAgU1RSSU5HUyxcbiAgICAgIGhsanMuQ19MSU5FX0NPTU1FTlRfTU9ERSxcbiAgICAgIGhsanMuQ19CTE9DS19DT01NRU5UX01PREUsXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogXCJjb21tZW50XCIsXG4gICAgICAgIGJlZ2luOiAvOy8sXG4gICAgICAgIGVuZDogXCIkXCIsXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfSxcbiAgICAgIHsgLy8gRnVuY3Rpb25zIGFuZCB1c2VyLWRlZmluZWQgZnVuY3Rpb25zOiB3cml0ZSAkenRpbWUoNjAqNjAqMyksICQkbXlGdW5jKDEwKSwgJCReVmFsKDEpXG4gICAgICAgIGNsYXNzTmFtZTogXCJidWlsdF9pblwiLFxuICAgICAgICBiZWdpbjogLyg/OlxcJFxcJD98XFwuXFwuKVxcXj9bYS16QS1aXSsvXG4gICAgICB9LFxuICAgICAgeyAvLyBNYWNybyBjb21tYW5kOiBxdWl0ICQkJE9LXG4gICAgICAgIGNsYXNzTmFtZTogXCJidWlsdF9pblwiLFxuICAgICAgICBiZWdpbjogL1xcJFxcJFxcJFthLXpBLVpdKy9cbiAgICAgIH0sXG4gICAgICB7IC8vIFNwZWNpYWwgKGdsb2JhbCkgdmFyaWFibGVzOiB3cml0ZSAlcmVxdWVzdC5Db250ZW50OyBCdWlsdC1pbiBjbGFzc2VzOiAlTGlicmFyeS5JbnRlZ2VyXG4gICAgICAgIGNsYXNzTmFtZTogXCJidWlsdF9pblwiLFxuICAgICAgICBiZWdpbjogLyVbYS16XSsoPzpcXC5bYS16XSspKi9cbiAgICAgIH0sXG4gICAgICB7IC8vIEdsb2JhbCB2YXJpYWJsZTogc2V0IF5nbG9iYWxOYW1lID0gMTIgd3JpdGUgXmdsb2JhbE5hbWVcbiAgICAgICAgY2xhc3NOYW1lOiBcInN5bWJvbFwiLFxuICAgICAgICBiZWdpbjogL1xcXiU/W2EtekEtWl1bXFx3XSovXG4gICAgICB9LFxuICAgICAgeyAvLyBTb21lIGNvbnRyb2wgY29uc3RydWN0aW9uczogZG8gIyNjbGFzcyhQYWNrYWdlLkNsYXNzTmFtZSkuTWV0aG9kKCksICMjc3VwZXIoKVxuICAgICAgICBjbGFzc05hbWU6IFwia2V5d29yZFwiLFxuICAgICAgICBiZWdpbjogLyMjY2xhc3N8IyNzdXBlcnwjZGVmaW5lfCNkaW0vXG4gICAgICB9LFxuICAgICAgLy8gc3ViLWxhbmd1YWdlczogYXJlIG5vdCBmdWxseSBzdXBwb3J0ZWQgYnkgaGxqcyBieSAxMS8xNS8yMDE1XG4gICAgICAvLyBsZWZ0IGZvciB0aGUgZnV0dXJlIGltcGxlbWVudGF0aW9uLlxuICAgICAge1xuICAgICAgICBiZWdpbjogLyZzcWxcXCgvLFxuICAgICAgICBlbmQ6IC9cXCkvLFxuICAgICAgICBleGNsdWRlQmVnaW46IHRydWUsXG4gICAgICAgIGV4Y2x1ZGVFbmQ6IHRydWUsXG4gICAgICAgIHN1Ykxhbmd1YWdlOiBcInNxbFwiXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogLyYoanN8anNjcmlwdHxqYXZhc2NyaXB0KTwvLFxuICAgICAgICBlbmQ6IC8+LyxcbiAgICAgICAgZXhjbHVkZUJlZ2luOiB0cnVlLFxuICAgICAgICBleGNsdWRlRW5kOiB0cnVlLFxuICAgICAgICBzdWJMYW5ndWFnZTogXCJqYXZhc2NyaXB0XCJcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIC8vIHRoaXMgYnJha2VzIGZpcnN0IGFuZCBsYXN0IHRhZywgYnV0IHRoaXMgaXMgdGhlIG9ubHkgd2F5IHRvIGVtYmVkIGEgdmFsaWQgaHRtbFxuICAgICAgICBiZWdpbjogLyZodG1sPFxccyo8LyxcbiAgICAgICAgZW5kOiAvPlxccyo+LyxcbiAgICAgICAgc3ViTGFuZ3VhZ2U6IFwieG1sXCJcbiAgICAgIH1cbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gY29zO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9