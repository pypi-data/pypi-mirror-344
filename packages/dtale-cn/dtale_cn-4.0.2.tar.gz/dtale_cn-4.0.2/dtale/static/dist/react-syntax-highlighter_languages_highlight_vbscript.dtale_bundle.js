(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_vbscript"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/vbscript.js":
/*!***************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/vbscript.js ***!
  \***************************************************************************************************/
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

/**
 * Any of the passed expresssions may match
 *
 * Creates a huge this | this | that | that match
 * @param {(RegExp | string)[] } args
 * @returns {string}
 */
function either(...args) {
  const joined = '(' + args.map((x) => source(x)).join("|") + ")";
  return joined;
}

/*
Language: VBScript
Description: VBScript ("Microsoft Visual Basic Scripting Edition") is an Active Scripting language developed by Microsoft that is modeled on Visual Basic.
Author: Nikita Ledyaev <lenikita@yandex.ru>
Contributors: Michal Gabrukiewicz <mgabru@gmail.com>
Website: https://en.wikipedia.org/wiki/VBScript
Category: scripting
*/

/** @type LanguageFn */
function vbscript(hljs) {
  const BUILT_IN_FUNCTIONS = ('lcase month vartype instrrev ubound setlocale getobject rgb getref string ' +
  'weekdayname rnd dateadd monthname now day minute isarray cbool round formatcurrency ' +
  'conversions csng timevalue second year space abs clng timeserial fixs len asc ' +
  'isempty maths dateserial atn timer isobject filter weekday datevalue ccur isdate ' +
  'instr datediff formatdatetime replace isnull right sgn array snumeric log cdbl hex ' +
  'chr lbound msgbox ucase getlocale cos cdate cbyte rtrim join hour oct typename trim ' +
  'strcomp int createobject loadpicture tan formatnumber mid ' +
  'split  cint sin datepart ltrim sqr ' +
  'time derived eval date formatpercent exp inputbox left ascw ' +
  'chrw regexp cstr err').split(" ");
  const BUILT_IN_OBJECTS = [
    "server",
    "response",
    "request",
    // take no arguments so can be called without ()
    "scriptengine",
    "scriptenginebuildversion",
    "scriptengineminorversion",
    "scriptenginemajorversion"
  ];

  const BUILT_IN_CALL = {
    begin: concat(either(...BUILT_IN_FUNCTIONS), "\\s*\\("),
    // relevance 0 because this is acting as a beginKeywords really
    relevance:0,
    keywords: {
      built_in: BUILT_IN_FUNCTIONS
    }
  };

  return {
    name: 'VBScript',
    aliases: ['vbs'],
    case_insensitive: true,
    keywords: {
      keyword:
        'call class const dim do loop erase execute executeglobal exit for each next function ' +
        'if then else on error option explicit new private property let get public randomize ' +
        'redim rem select case set stop sub while wend with end to elseif is or xor and not ' +
        'class_initialize class_terminate default preserve in me byval byref step resume goto',
      built_in: BUILT_IN_OBJECTS,
      literal:
        'true false null nothing empty'
    },
    illegal: '//',
    contains: [
      BUILT_IN_CALL,
      hljs.inherit(hljs.QUOTE_STRING_MODE, {contains: [{begin: '""'}]}),
      hljs.COMMENT(
        /'/,
        /$/,
        {
          relevance: 0
        }
      ),
      hljs.C_NUMBER_MODE
    ]
  };
}

module.exports = vbscript;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfdmJzY3JpcHQuZHRhbGVfYnVuZGxlLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7O0FBQUE7QUFDQSxXQUFXLFFBQVE7QUFDbkIsYUFBYTtBQUNiOztBQUVBO0FBQ0EsV0FBVyxrQkFBa0I7QUFDN0IsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7O0FBRUE7QUFDQSxXQUFXLHVCQUF1QjtBQUNsQyxhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFdBQVcsc0JBQXNCO0FBQ2pDLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7QUFDQSw0Q0FBNEMsWUFBWSxZQUFZLEVBQUU7QUFDdEU7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvdmJzY3JpcHQuanMiXSwic291cmNlc0NvbnRlbnQiOlsiLyoqXG4gKiBAcGFyYW0ge3N0cmluZ30gdmFsdWVcbiAqIEByZXR1cm5zIHtSZWdFeHB9XG4gKiAqL1xuXG4vKipcbiAqIEBwYXJhbSB7UmVnRXhwIHwgc3RyaW5nIH0gcmVcbiAqIEByZXR1cm5zIHtzdHJpbmd9XG4gKi9cbmZ1bmN0aW9uIHNvdXJjZShyZSkge1xuICBpZiAoIXJlKSByZXR1cm4gbnVsbDtcbiAgaWYgKHR5cGVvZiByZSA9PT0gXCJzdHJpbmdcIikgcmV0dXJuIHJlO1xuXG4gIHJldHVybiByZS5zb3VyY2U7XG59XG5cbi8qKlxuICogQHBhcmFtIHsuLi4oUmVnRXhwIHwgc3RyaW5nKSB9IGFyZ3NcbiAqIEByZXR1cm5zIHtzdHJpbmd9XG4gKi9cbmZ1bmN0aW9uIGNvbmNhdCguLi5hcmdzKSB7XG4gIGNvbnN0IGpvaW5lZCA9IGFyZ3MubWFwKCh4KSA9PiBzb3VyY2UoeCkpLmpvaW4oXCJcIik7XG4gIHJldHVybiBqb2luZWQ7XG59XG5cbi8qKlxuICogQW55IG9mIHRoZSBwYXNzZWQgZXhwcmVzc3Npb25zIG1heSBtYXRjaFxuICpcbiAqIENyZWF0ZXMgYSBodWdlIHRoaXMgfCB0aGlzIHwgdGhhdCB8IHRoYXQgbWF0Y2hcbiAqIEBwYXJhbSB7KFJlZ0V4cCB8IHN0cmluZylbXSB9IGFyZ3NcbiAqIEByZXR1cm5zIHtzdHJpbmd9XG4gKi9cbmZ1bmN0aW9uIGVpdGhlciguLi5hcmdzKSB7XG4gIGNvbnN0IGpvaW5lZCA9ICcoJyArIGFyZ3MubWFwKCh4KSA9PiBzb3VyY2UoeCkpLmpvaW4oXCJ8XCIpICsgXCIpXCI7XG4gIHJldHVybiBqb2luZWQ7XG59XG5cbi8qXG5MYW5ndWFnZTogVkJTY3JpcHRcbkRlc2NyaXB0aW9uOiBWQlNjcmlwdCAoXCJNaWNyb3NvZnQgVmlzdWFsIEJhc2ljIFNjcmlwdGluZyBFZGl0aW9uXCIpIGlzIGFuIEFjdGl2ZSBTY3JpcHRpbmcgbGFuZ3VhZ2UgZGV2ZWxvcGVkIGJ5IE1pY3Jvc29mdCB0aGF0IGlzIG1vZGVsZWQgb24gVmlzdWFsIEJhc2ljLlxuQXV0aG9yOiBOaWtpdGEgTGVkeWFldiA8bGVuaWtpdGFAeWFuZGV4LnJ1PlxuQ29udHJpYnV0b3JzOiBNaWNoYWwgR2FicnVraWV3aWN6IDxtZ2FicnVAZ21haWwuY29tPlxuV2Vic2l0ZTogaHR0cHM6Ly9lbi53aWtpcGVkaWEub3JnL3dpa2kvVkJTY3JpcHRcbkNhdGVnb3J5OiBzY3JpcHRpbmdcbiovXG5cbi8qKiBAdHlwZSBMYW5ndWFnZUZuICovXG5mdW5jdGlvbiB2YnNjcmlwdChobGpzKSB7XG4gIGNvbnN0IEJVSUxUX0lOX0ZVTkNUSU9OUyA9ICgnbGNhc2UgbW9udGggdmFydHlwZSBpbnN0cnJldiB1Ym91bmQgc2V0bG9jYWxlIGdldG9iamVjdCByZ2IgZ2V0cmVmIHN0cmluZyAnICtcbiAgJ3dlZWtkYXluYW1lIHJuZCBkYXRlYWRkIG1vbnRobmFtZSBub3cgZGF5IG1pbnV0ZSBpc2FycmF5IGNib29sIHJvdW5kIGZvcm1hdGN1cnJlbmN5ICcgK1xuICAnY29udmVyc2lvbnMgY3NuZyB0aW1ldmFsdWUgc2Vjb25kIHllYXIgc3BhY2UgYWJzIGNsbmcgdGltZXNlcmlhbCBmaXhzIGxlbiBhc2MgJyArXG4gICdpc2VtcHR5IG1hdGhzIGRhdGVzZXJpYWwgYXRuIHRpbWVyIGlzb2JqZWN0IGZpbHRlciB3ZWVrZGF5IGRhdGV2YWx1ZSBjY3VyIGlzZGF0ZSAnICtcbiAgJ2luc3RyIGRhdGVkaWZmIGZvcm1hdGRhdGV0aW1lIHJlcGxhY2UgaXNudWxsIHJpZ2h0IHNnbiBhcnJheSBzbnVtZXJpYyBsb2cgY2RibCBoZXggJyArXG4gICdjaHIgbGJvdW5kIG1zZ2JveCB1Y2FzZSBnZXRsb2NhbGUgY29zIGNkYXRlIGNieXRlIHJ0cmltIGpvaW4gaG91ciBvY3QgdHlwZW5hbWUgdHJpbSAnICtcbiAgJ3N0cmNvbXAgaW50IGNyZWF0ZW9iamVjdCBsb2FkcGljdHVyZSB0YW4gZm9ybWF0bnVtYmVyIG1pZCAnICtcbiAgJ3NwbGl0ICBjaW50IHNpbiBkYXRlcGFydCBsdHJpbSBzcXIgJyArXG4gICd0aW1lIGRlcml2ZWQgZXZhbCBkYXRlIGZvcm1hdHBlcmNlbnQgZXhwIGlucHV0Ym94IGxlZnQgYXNjdyAnICtcbiAgJ2NocncgcmVnZXhwIGNzdHIgZXJyJykuc3BsaXQoXCIgXCIpO1xuICBjb25zdCBCVUlMVF9JTl9PQkpFQ1RTID0gW1xuICAgIFwic2VydmVyXCIsXG4gICAgXCJyZXNwb25zZVwiLFxuICAgIFwicmVxdWVzdFwiLFxuICAgIC8vIHRha2Ugbm8gYXJndW1lbnRzIHNvIGNhbiBiZSBjYWxsZWQgd2l0aG91dCAoKVxuICAgIFwic2NyaXB0ZW5naW5lXCIsXG4gICAgXCJzY3JpcHRlbmdpbmVidWlsZHZlcnNpb25cIixcbiAgICBcInNjcmlwdGVuZ2luZW1pbm9ydmVyc2lvblwiLFxuICAgIFwic2NyaXB0ZW5naW5lbWFqb3J2ZXJzaW9uXCJcbiAgXTtcblxuICBjb25zdCBCVUlMVF9JTl9DQUxMID0ge1xuICAgIGJlZ2luOiBjb25jYXQoZWl0aGVyKC4uLkJVSUxUX0lOX0ZVTkNUSU9OUyksIFwiXFxcXHMqXFxcXChcIiksXG4gICAgLy8gcmVsZXZhbmNlIDAgYmVjYXVzZSB0aGlzIGlzIGFjdGluZyBhcyBhIGJlZ2luS2V5d29yZHMgcmVhbGx5XG4gICAgcmVsZXZhbmNlOjAsXG4gICAga2V5d29yZHM6IHtcbiAgICAgIGJ1aWx0X2luOiBCVUlMVF9JTl9GVU5DVElPTlNcbiAgICB9XG4gIH07XG5cbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnVkJTY3JpcHQnLFxuICAgIGFsaWFzZXM6IFsndmJzJ10sXG4gICAgY2FzZV9pbnNlbnNpdGl2ZTogdHJ1ZSxcbiAgICBrZXl3b3Jkczoge1xuICAgICAga2V5d29yZDpcbiAgICAgICAgJ2NhbGwgY2xhc3MgY29uc3QgZGltIGRvIGxvb3AgZXJhc2UgZXhlY3V0ZSBleGVjdXRlZ2xvYmFsIGV4aXQgZm9yIGVhY2ggbmV4dCBmdW5jdGlvbiAnICtcbiAgICAgICAgJ2lmIHRoZW4gZWxzZSBvbiBlcnJvciBvcHRpb24gZXhwbGljaXQgbmV3IHByaXZhdGUgcHJvcGVydHkgbGV0IGdldCBwdWJsaWMgcmFuZG9taXplICcgK1xuICAgICAgICAncmVkaW0gcmVtIHNlbGVjdCBjYXNlIHNldCBzdG9wIHN1YiB3aGlsZSB3ZW5kIHdpdGggZW5kIHRvIGVsc2VpZiBpcyBvciB4b3IgYW5kIG5vdCAnICtcbiAgICAgICAgJ2NsYXNzX2luaXRpYWxpemUgY2xhc3NfdGVybWluYXRlIGRlZmF1bHQgcHJlc2VydmUgaW4gbWUgYnl2YWwgYnlyZWYgc3RlcCByZXN1bWUgZ290bycsXG4gICAgICBidWlsdF9pbjogQlVJTFRfSU5fT0JKRUNUUyxcbiAgICAgIGxpdGVyYWw6XG4gICAgICAgICd0cnVlIGZhbHNlIG51bGwgbm90aGluZyBlbXB0eSdcbiAgICB9LFxuICAgIGlsbGVnYWw6ICcvLycsXG4gICAgY29udGFpbnM6IFtcbiAgICAgIEJVSUxUX0lOX0NBTEwsXG4gICAgICBobGpzLmluaGVyaXQoaGxqcy5RVU9URV9TVFJJTkdfTU9ERSwge2NvbnRhaW5zOiBbe2JlZ2luOiAnXCJcIid9XX0pLFxuICAgICAgaGxqcy5DT01NRU5UKFxuICAgICAgICAvJy8sXG4gICAgICAgIC8kLyxcbiAgICAgICAge1xuICAgICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgICB9XG4gICAgICApLFxuICAgICAgaGxqcy5DX05VTUJFUl9NT0RFXG4gICAgXVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IHZic2NyaXB0O1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9