(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_ini"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/ini.js":
/*!**********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/ini.js ***!
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
function lookahead(re) {
  return concat('(?=', re, ')');
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
Language: TOML, also INI
Description: TOML aims to be a minimal configuration file format that's easy to read due to obvious semantics.
Contributors: Guillaume Gomez <guillaume1.gomez@gmail.com>
Category: common, config
Website: https://github.com/toml-lang/toml
*/

function ini(hljs) {
  const NUMBERS = {
    className: 'number',
    relevance: 0,
    variants: [
      {
        begin: /([+-]+)?[\d]+_[\d_]+/
      },
      {
        begin: hljs.NUMBER_RE
      }
    ]
  };
  const COMMENTS = hljs.COMMENT();
  COMMENTS.variants = [
    {
      begin: /;/,
      end: /$/
    },
    {
      begin: /#/,
      end: /$/
    }
  ];
  const VARIABLES = {
    className: 'variable',
    variants: [
      {
        begin: /\$[\w\d"][\w\d_]*/
      },
      {
        begin: /\$\{(.*?)\}/
      }
    ]
  };
  const LITERALS = {
    className: 'literal',
    begin: /\bon|off|true|false|yes|no\b/
  };
  const STRINGS = {
    className: "string",
    contains: [hljs.BACKSLASH_ESCAPE],
    variants: [
      {
        begin: "'''",
        end: "'''",
        relevance: 10
      },
      {
        begin: '"""',
        end: '"""',
        relevance: 10
      },
      {
        begin: '"',
        end: '"'
      },
      {
        begin: "'",
        end: "'"
      }
    ]
  };
  const ARRAY = {
    begin: /\[/,
    end: /\]/,
    contains: [
      COMMENTS,
      LITERALS,
      VARIABLES,
      STRINGS,
      NUMBERS,
      'self'
    ],
    relevance: 0
  };

  const BARE_KEY = /[A-Za-z0-9_-]+/;
  const QUOTED_KEY_DOUBLE_QUOTE = /"(\\"|[^"])*"/;
  const QUOTED_KEY_SINGLE_QUOTE = /'[^']*'/;
  const ANY_KEY = either(
    BARE_KEY, QUOTED_KEY_DOUBLE_QUOTE, QUOTED_KEY_SINGLE_QUOTE
  );
  const DOTTED_KEY = concat(
    ANY_KEY, '(\\s*\\.\\s*', ANY_KEY, ')*',
    lookahead(/\s*=\s*[^#\s]/)
  );

  return {
    name: 'TOML, also INI',
    aliases: ['toml'],
    case_insensitive: true,
    illegal: /\S/,
    contains: [
      COMMENTS,
      {
        className: 'section',
        begin: /\[+/,
        end: /\]+/
      },
      {
        begin: DOTTED_KEY,
        className: 'attr',
        starts: {
          end: /$/,
          contains: [
            COMMENTS,
            ARRAY,
            LITERALS,
            VARIABLES,
            STRINGS,
            NUMBERS
          ]
        }
      }
    ]
  };
}

module.exports = ini;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfaW5pLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0EsV0FBVyxRQUFRO0FBQ25CLGFBQWE7QUFDYjs7QUFFQTtBQUNBLFdBQVcsa0JBQWtCO0FBQzdCLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBOztBQUVBO0FBQ0EsV0FBVyxrQkFBa0I7QUFDN0IsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0EsV0FBVyx1QkFBdUI7QUFDbEMsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXLHNCQUFzQjtBQUNqQyxhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsZUFBZTtBQUNmO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0Esb0JBQW9CLE9BQU87QUFDM0I7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvaW5pLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qKlxuICogQHBhcmFtIHtzdHJpbmd9IHZhbHVlXG4gKiBAcmV0dXJucyB7UmVnRXhwfVxuICogKi9cblxuLyoqXG4gKiBAcGFyYW0ge1JlZ0V4cCB8IHN0cmluZyB9IHJlXG4gKiBAcmV0dXJucyB7c3RyaW5nfVxuICovXG5mdW5jdGlvbiBzb3VyY2UocmUpIHtcbiAgaWYgKCFyZSkgcmV0dXJuIG51bGw7XG4gIGlmICh0eXBlb2YgcmUgPT09IFwic3RyaW5nXCIpIHJldHVybiByZTtcblxuICByZXR1cm4gcmUuc291cmNlO1xufVxuXG4vKipcbiAqIEBwYXJhbSB7UmVnRXhwIHwgc3RyaW5nIH0gcmVcbiAqIEByZXR1cm5zIHtzdHJpbmd9XG4gKi9cbmZ1bmN0aW9uIGxvb2thaGVhZChyZSkge1xuICByZXR1cm4gY29uY2F0KCcoPz0nLCByZSwgJyknKTtcbn1cblxuLyoqXG4gKiBAcGFyYW0gey4uLihSZWdFeHAgfCBzdHJpbmcpIH0gYXJnc1xuICogQHJldHVybnMge3N0cmluZ31cbiAqL1xuZnVuY3Rpb24gY29uY2F0KC4uLmFyZ3MpIHtcbiAgY29uc3Qgam9pbmVkID0gYXJncy5tYXAoKHgpID0+IHNvdXJjZSh4KSkuam9pbihcIlwiKTtcbiAgcmV0dXJuIGpvaW5lZDtcbn1cblxuLyoqXG4gKiBBbnkgb2YgdGhlIHBhc3NlZCBleHByZXNzc2lvbnMgbWF5IG1hdGNoXG4gKlxuICogQ3JlYXRlcyBhIGh1Z2UgdGhpcyB8IHRoaXMgfCB0aGF0IHwgdGhhdCBtYXRjaFxuICogQHBhcmFtIHsoUmVnRXhwIHwgc3RyaW5nKVtdIH0gYXJnc1xuICogQHJldHVybnMge3N0cmluZ31cbiAqL1xuZnVuY3Rpb24gZWl0aGVyKC4uLmFyZ3MpIHtcbiAgY29uc3Qgam9pbmVkID0gJygnICsgYXJncy5tYXAoKHgpID0+IHNvdXJjZSh4KSkuam9pbihcInxcIikgKyBcIilcIjtcbiAgcmV0dXJuIGpvaW5lZDtcbn1cblxuLypcbkxhbmd1YWdlOiBUT01MLCBhbHNvIElOSVxuRGVzY3JpcHRpb246IFRPTUwgYWltcyB0byBiZSBhIG1pbmltYWwgY29uZmlndXJhdGlvbiBmaWxlIGZvcm1hdCB0aGF0J3MgZWFzeSB0byByZWFkIGR1ZSB0byBvYnZpb3VzIHNlbWFudGljcy5cbkNvbnRyaWJ1dG9yczogR3VpbGxhdW1lIEdvbWV6IDxndWlsbGF1bWUxLmdvbWV6QGdtYWlsLmNvbT5cbkNhdGVnb3J5OiBjb21tb24sIGNvbmZpZ1xuV2Vic2l0ZTogaHR0cHM6Ly9naXRodWIuY29tL3RvbWwtbGFuZy90b21sXG4qL1xuXG5mdW5jdGlvbiBpbmkoaGxqcykge1xuICBjb25zdCBOVU1CRVJTID0ge1xuICAgIGNsYXNzTmFtZTogJ251bWJlcicsXG4gICAgcmVsZXZhbmNlOiAwLFxuICAgIHZhcmlhbnRzOiBbXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAvKFsrLV0rKT9bXFxkXStfW1xcZF9dKy9cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiBobGpzLk5VTUJFUl9SRVxuICAgICAgfVxuICAgIF1cbiAgfTtcbiAgY29uc3QgQ09NTUVOVFMgPSBobGpzLkNPTU1FTlQoKTtcbiAgQ09NTUVOVFMudmFyaWFudHMgPSBbXG4gICAge1xuICAgICAgYmVnaW46IC87LyxcbiAgICAgIGVuZDogLyQvXG4gICAgfSxcbiAgICB7XG4gICAgICBiZWdpbjogLyMvLFxuICAgICAgZW5kOiAvJC9cbiAgICB9XG4gIF07XG4gIGNvbnN0IFZBUklBQkxFUyA9IHtcbiAgICBjbGFzc05hbWU6ICd2YXJpYWJsZScsXG4gICAgdmFyaWFudHM6IFtcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC9cXCRbXFx3XFxkXCJdW1xcd1xcZF9dKi9cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAvXFwkXFx7KC4qPylcXH0vXG4gICAgICB9XG4gICAgXVxuICB9O1xuICBjb25zdCBMSVRFUkFMUyA9IHtcbiAgICBjbGFzc05hbWU6ICdsaXRlcmFsJyxcbiAgICBiZWdpbjogL1xcYm9ufG9mZnx0cnVlfGZhbHNlfHllc3xub1xcYi9cbiAgfTtcbiAgY29uc3QgU1RSSU5HUyA9IHtcbiAgICBjbGFzc05hbWU6IFwic3RyaW5nXCIsXG4gICAgY29udGFpbnM6IFtobGpzLkJBQ0tTTEFTSF9FU0NBUEVdLFxuICAgIHZhcmlhbnRzOiBbXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiBcIicnJ1wiLFxuICAgICAgICBlbmQ6IFwiJycnXCIsXG4gICAgICAgIHJlbGV2YW5jZTogMTBcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnXCJcIlwiJyxcbiAgICAgICAgZW5kOiAnXCJcIlwiJyxcbiAgICAgICAgcmVsZXZhbmNlOiAxMFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICdcIicsXG4gICAgICAgIGVuZDogJ1wiJ1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IFwiJ1wiLFxuICAgICAgICBlbmQ6IFwiJ1wiXG4gICAgICB9XG4gICAgXVxuICB9O1xuICBjb25zdCBBUlJBWSA9IHtcbiAgICBiZWdpbjogL1xcWy8sXG4gICAgZW5kOiAvXFxdLyxcbiAgICBjb250YWluczogW1xuICAgICAgQ09NTUVOVFMsXG4gICAgICBMSVRFUkFMUyxcbiAgICAgIFZBUklBQkxFUyxcbiAgICAgIFNUUklOR1MsXG4gICAgICBOVU1CRVJTLFxuICAgICAgJ3NlbGYnXG4gICAgXSxcbiAgICByZWxldmFuY2U6IDBcbiAgfTtcblxuICBjb25zdCBCQVJFX0tFWSA9IC9bQS1aYS16MC05Xy1dKy87XG4gIGNvbnN0IFFVT1RFRF9LRVlfRE9VQkxFX1FVT1RFID0gL1wiKFxcXFxcInxbXlwiXSkqXCIvO1xuICBjb25zdCBRVU9URURfS0VZX1NJTkdMRV9RVU9URSA9IC8nW14nXSonLztcbiAgY29uc3QgQU5ZX0tFWSA9IGVpdGhlcihcbiAgICBCQVJFX0tFWSwgUVVPVEVEX0tFWV9ET1VCTEVfUVVPVEUsIFFVT1RFRF9LRVlfU0lOR0xFX1FVT1RFXG4gICk7XG4gIGNvbnN0IERPVFRFRF9LRVkgPSBjb25jYXQoXG4gICAgQU5ZX0tFWSwgJyhcXFxccypcXFxcLlxcXFxzKicsIEFOWV9LRVksICcpKicsXG4gICAgbG9va2FoZWFkKC9cXHMqPVxccypbXiNcXHNdLylcbiAgKTtcblxuICByZXR1cm4ge1xuICAgIG5hbWU6ICdUT01MLCBhbHNvIElOSScsXG4gICAgYWxpYXNlczogWyd0b21sJ10sXG4gICAgY2FzZV9pbnNlbnNpdGl2ZTogdHJ1ZSxcbiAgICBpbGxlZ2FsOiAvXFxTLyxcbiAgICBjb250YWluczogW1xuICAgICAgQ09NTUVOVFMsXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3NlY3Rpb24nLFxuICAgICAgICBiZWdpbjogL1xcWysvLFxuICAgICAgICBlbmQ6IC9cXF0rL1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IERPVFRFRF9LRVksXG4gICAgICAgIGNsYXNzTmFtZTogJ2F0dHInLFxuICAgICAgICBzdGFydHM6IHtcbiAgICAgICAgICBlbmQ6IC8kLyxcbiAgICAgICAgICBjb250YWluczogW1xuICAgICAgICAgICAgQ09NTUVOVFMsXG4gICAgICAgICAgICBBUlJBWSxcbiAgICAgICAgICAgIExJVEVSQUxTLFxuICAgICAgICAgICAgVkFSSUFCTEVTLFxuICAgICAgICAgICAgU1RSSU5HUyxcbiAgICAgICAgICAgIE5VTUJFUlNcbiAgICAgICAgICBdXG4gICAgICAgIH1cbiAgICAgIH1cbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gaW5pO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9