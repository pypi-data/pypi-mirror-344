(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_vbnet"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/vbnet.js":
/*!************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/vbnet.js ***!
  \************************************************************************************************/
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
Language: Visual Basic .NET
Description: Visual Basic .NET (VB.NET) is a multi-paradigm, object-oriented programming language, implemented on the .NET Framework.
Authors: Poren Chiang <ren.chiang@gmail.com>, Jan Pilzer
Website: https://docs.microsoft.com/dotnet/visual-basic/getting-started
Category: common
*/

/** @type LanguageFn */
function vbnet(hljs) {
  /**
   * Character Literal
   * Either a single character ("a"C) or an escaped double quote (""""C).
   */
  const CHARACTER = {
    className: 'string',
    begin: /"(""|[^/n])"C\b/
  };

  const STRING = {
    className: 'string',
    begin: /"/,
    end: /"/,
    illegal: /\n/,
    contains: [
      {
        // double quote escape
        begin: /""/
      }
    ]
  };

  /** Date Literals consist of a date, a time, or both separated by whitespace, surrounded by # */
  const MM_DD_YYYY = /\d{1,2}\/\d{1,2}\/\d{4}/;
  const YYYY_MM_DD = /\d{4}-\d{1,2}-\d{1,2}/;
  const TIME_12H = /(\d|1[012])(:\d+){0,2} *(AM|PM)/;
  const TIME_24H = /\d{1,2}(:\d{1,2}){1,2}/;
  const DATE = {
    className: 'literal',
    variants: [
      {
        // #YYYY-MM-DD# (ISO-Date) or #M/D/YYYY# (US-Date)
        begin: concat(/# */, either(YYYY_MM_DD, MM_DD_YYYY), / *#/)
      },
      {
        // #H:mm[:ss]# (24h Time)
        begin: concat(/# */, TIME_24H, / *#/)
      },
      {
        // #h[:mm[:ss]] A# (12h Time)
        begin: concat(/# */, TIME_12H, / *#/)
      },
      {
        // date plus time
        begin: concat(
          /# */,
          either(YYYY_MM_DD, MM_DD_YYYY),
          / +/,
          either(TIME_12H, TIME_24H),
          / *#/
        )
      }
    ]
  };

  const NUMBER = {
    className: 'number',
    relevance: 0,
    variants: [
      {
        // Float
        begin: /\b\d[\d_]*((\.[\d_]+(E[+-]?[\d_]+)?)|(E[+-]?[\d_]+))[RFD@!#]?/
      },
      {
        // Integer (base 10)
        begin: /\b\d[\d_]*((U?[SIL])|[%&])?/
      },
      {
        // Integer (base 16)
        begin: /&H[\dA-F_]+((U?[SIL])|[%&])?/
      },
      {
        // Integer (base 8)
        begin: /&O[0-7_]+((U?[SIL])|[%&])?/
      },
      {
        // Integer (base 2)
        begin: /&B[01_]+((U?[SIL])|[%&])?/
      }
    ]
  };

  const LABEL = {
    className: 'label',
    begin: /^\w+:/
  };

  const DOC_COMMENT = hljs.COMMENT(/'''/, /$/, {
    contains: [
      {
        className: 'doctag',
        begin: /<\/?/,
        end: />/
      }
    ]
  });

  const COMMENT = hljs.COMMENT(null, /$/, {
    variants: [
      {
        begin: /'/
      },
      {
        // TODO: Use `beforeMatch:` for leading spaces
        begin: /([\t ]|^)REM(?=\s)/
      }
    ]
  });

  const DIRECTIVES = {
    className: 'meta',
    // TODO: Use `beforeMatch:` for indentation once available
    begin: /[\t ]*#(const|disable|else|elseif|enable|end|externalsource|if|region)\b/,
    end: /$/,
    keywords: {
      'meta-keyword':
        'const disable else elseif enable end externalsource if region then'
    },
    contains: [ COMMENT ]
  };

  return {
    name: 'Visual Basic .NET',
    aliases: [ 'vb' ],
    case_insensitive: true,
    classNameAliases: {
      label: 'symbol'
    },
    keywords: {
      keyword:
        'addhandler alias aggregate ansi as async assembly auto binary by byref byval ' + /* a-b */
        'call case catch class compare const continue custom declare default delegate dim distinct do ' + /* c-d */
        'each equals else elseif end enum erase error event exit explicit finally for friend from function ' + /* e-f */
        'get global goto group handles if implements imports in inherits interface into iterator ' + /* g-i */
        'join key let lib loop me mid module mustinherit mustoverride mybase myclass ' + /* j-m */
        'namespace narrowing new next notinheritable notoverridable ' + /* n */
        'of off on operator option optional order overloads overridable overrides ' + /* o */
        'paramarray partial preserve private property protected public ' + /* p */
        'raiseevent readonly redim removehandler resume return ' + /* r */
        'select set shadows shared skip static step stop structure strict sub synclock ' + /* s */
        'take text then throw to try unicode until using when where while widening with withevents writeonly yield' /* t-y */,
      built_in:
        // Operators https://docs.microsoft.com/dotnet/visual-basic/language-reference/operators
        'addressof and andalso await directcast gettype getxmlnamespace is isfalse isnot istrue like mod nameof new not or orelse trycast typeof xor ' +
        // Type Conversion Functions https://docs.microsoft.com/dotnet/visual-basic/language-reference/functions/type-conversion-functions
        'cbool cbyte cchar cdate cdbl cdec cint clng cobj csbyte cshort csng cstr cuint culng cushort',
      type:
        // Data types https://docs.microsoft.com/dotnet/visual-basic/language-reference/data-types
        'boolean byte char date decimal double integer long object sbyte short single string uinteger ulong ushort',
      literal: 'true false nothing'
    },
    illegal:
      '//|\\{|\\}|endif|gosub|variant|wend|^\\$ ' /* reserved deprecated keywords */,
    contains: [
      CHARACTER,
      STRING,
      DATE,
      NUMBER,
      LABEL,
      DOC_COMMENT,
      COMMENT,
      DIRECTIVES
    ]
  };
}

module.exports = vbnet;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfdmJuZXQuZHRhbGVfYnVuZGxlLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7O0FBQUE7QUFDQSxXQUFXLFFBQVE7QUFDbkIsYUFBYTtBQUNiOztBQUVBO0FBQ0EsV0FBVyxrQkFBa0I7QUFDN0IsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7O0FBRUE7QUFDQSxXQUFXLHVCQUF1QjtBQUNsQyxhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFdBQVcsc0JBQXNCO0FBQ2pDLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBLHlCQUF5QixJQUFJLEtBQUssSUFBSSxLQUFLLEVBQUU7QUFDN0MseUJBQXlCLEVBQUUsSUFBSSxJQUFJLElBQUksSUFBSTtBQUMzQyxzQ0FBc0MsS0FBSztBQUMzQyx1QkFBdUIsSUFBSSxLQUFLLElBQUksRUFBRSxJQUFJO0FBQzFDO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEdBQUc7O0FBRUg7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEdBQUc7O0FBRUg7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBLGFBQWEsSUFBSTtBQUNqQjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL3ZibmV0LmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qKlxuICogQHBhcmFtIHtzdHJpbmd9IHZhbHVlXG4gKiBAcmV0dXJucyB7UmVnRXhwfVxuICogKi9cblxuLyoqXG4gKiBAcGFyYW0ge1JlZ0V4cCB8IHN0cmluZyB9IHJlXG4gKiBAcmV0dXJucyB7c3RyaW5nfVxuICovXG5mdW5jdGlvbiBzb3VyY2UocmUpIHtcbiAgaWYgKCFyZSkgcmV0dXJuIG51bGw7XG4gIGlmICh0eXBlb2YgcmUgPT09IFwic3RyaW5nXCIpIHJldHVybiByZTtcblxuICByZXR1cm4gcmUuc291cmNlO1xufVxuXG4vKipcbiAqIEBwYXJhbSB7Li4uKFJlZ0V4cCB8IHN0cmluZykgfSBhcmdzXG4gKiBAcmV0dXJucyB7c3RyaW5nfVxuICovXG5mdW5jdGlvbiBjb25jYXQoLi4uYXJncykge1xuICBjb25zdCBqb2luZWQgPSBhcmdzLm1hcCgoeCkgPT4gc291cmNlKHgpKS5qb2luKFwiXCIpO1xuICByZXR1cm4gam9pbmVkO1xufVxuXG4vKipcbiAqIEFueSBvZiB0aGUgcGFzc2VkIGV4cHJlc3NzaW9ucyBtYXkgbWF0Y2hcbiAqXG4gKiBDcmVhdGVzIGEgaHVnZSB0aGlzIHwgdGhpcyB8IHRoYXQgfCB0aGF0IG1hdGNoXG4gKiBAcGFyYW0geyhSZWdFeHAgfCBzdHJpbmcpW10gfSBhcmdzXG4gKiBAcmV0dXJucyB7c3RyaW5nfVxuICovXG5mdW5jdGlvbiBlaXRoZXIoLi4uYXJncykge1xuICBjb25zdCBqb2luZWQgPSAnKCcgKyBhcmdzLm1hcCgoeCkgPT4gc291cmNlKHgpKS5qb2luKFwifFwiKSArIFwiKVwiO1xuICByZXR1cm4gam9pbmVkO1xufVxuXG4vKlxuTGFuZ3VhZ2U6IFZpc3VhbCBCYXNpYyAuTkVUXG5EZXNjcmlwdGlvbjogVmlzdWFsIEJhc2ljIC5ORVQgKFZCLk5FVCkgaXMgYSBtdWx0aS1wYXJhZGlnbSwgb2JqZWN0LW9yaWVudGVkIHByb2dyYW1taW5nIGxhbmd1YWdlLCBpbXBsZW1lbnRlZCBvbiB0aGUgLk5FVCBGcmFtZXdvcmsuXG5BdXRob3JzOiBQb3JlbiBDaGlhbmcgPHJlbi5jaGlhbmdAZ21haWwuY29tPiwgSmFuIFBpbHplclxuV2Vic2l0ZTogaHR0cHM6Ly9kb2NzLm1pY3Jvc29mdC5jb20vZG90bmV0L3Zpc3VhbC1iYXNpYy9nZXR0aW5nLXN0YXJ0ZWRcbkNhdGVnb3J5OiBjb21tb25cbiovXG5cbi8qKiBAdHlwZSBMYW5ndWFnZUZuICovXG5mdW5jdGlvbiB2Ym5ldChobGpzKSB7XG4gIC8qKlxuICAgKiBDaGFyYWN0ZXIgTGl0ZXJhbFxuICAgKiBFaXRoZXIgYSBzaW5nbGUgY2hhcmFjdGVyIChcImFcIkMpIG9yIGFuIGVzY2FwZWQgZG91YmxlIHF1b3RlIChcIlwiXCJcIkMpLlxuICAgKi9cbiAgY29uc3QgQ0hBUkFDVEVSID0ge1xuICAgIGNsYXNzTmFtZTogJ3N0cmluZycsXG4gICAgYmVnaW46IC9cIihcIlwifFteL25dKVwiQ1xcYi9cbiAgfTtcblxuICBjb25zdCBTVFJJTkcgPSB7XG4gICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICBiZWdpbjogL1wiLyxcbiAgICBlbmQ6IC9cIi8sXG4gICAgaWxsZWdhbDogL1xcbi8sXG4gICAgY29udGFpbnM6IFtcbiAgICAgIHtcbiAgICAgICAgLy8gZG91YmxlIHF1b3RlIGVzY2FwZVxuICAgICAgICBiZWdpbjogL1wiXCIvXG4gICAgICB9XG4gICAgXVxuICB9O1xuXG4gIC8qKiBEYXRlIExpdGVyYWxzIGNvbnNpc3Qgb2YgYSBkYXRlLCBhIHRpbWUsIG9yIGJvdGggc2VwYXJhdGVkIGJ5IHdoaXRlc3BhY2UsIHN1cnJvdW5kZWQgYnkgIyAqL1xuICBjb25zdCBNTV9ERF9ZWVlZID0gL1xcZHsxLDJ9XFwvXFxkezEsMn1cXC9cXGR7NH0vO1xuICBjb25zdCBZWVlZX01NX0REID0gL1xcZHs0fS1cXGR7MSwyfS1cXGR7MSwyfS87XG4gIGNvbnN0IFRJTUVfMTJIID0gLyhcXGR8MVswMTJdKSg6XFxkKyl7MCwyfSAqKEFNfFBNKS87XG4gIGNvbnN0IFRJTUVfMjRIID0gL1xcZHsxLDJ9KDpcXGR7MSwyfSl7MSwyfS87XG4gIGNvbnN0IERBVEUgPSB7XG4gICAgY2xhc3NOYW1lOiAnbGl0ZXJhbCcsXG4gICAgdmFyaWFudHM6IFtcbiAgICAgIHtcbiAgICAgICAgLy8gI1lZWVktTU0tREQjIChJU08tRGF0ZSkgb3IgI00vRC9ZWVlZIyAoVVMtRGF0ZSlcbiAgICAgICAgYmVnaW46IGNvbmNhdCgvIyAqLywgZWl0aGVyKFlZWVlfTU1fREQsIE1NX0REX1lZWVkpLCAvICojLylcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIC8vICNIOm1tWzpzc10jICgyNGggVGltZSlcbiAgICAgICAgYmVnaW46IGNvbmNhdCgvIyAqLywgVElNRV8yNEgsIC8gKiMvKVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgLy8gI2hbOm1tWzpzc11dIEEjICgxMmggVGltZSlcbiAgICAgICAgYmVnaW46IGNvbmNhdCgvIyAqLywgVElNRV8xMkgsIC8gKiMvKVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgLy8gZGF0ZSBwbHVzIHRpbWVcbiAgICAgICAgYmVnaW46IGNvbmNhdChcbiAgICAgICAgICAvIyAqLyxcbiAgICAgICAgICBlaXRoZXIoWVlZWV9NTV9ERCwgTU1fRERfWVlZWSksXG4gICAgICAgICAgLyArLyxcbiAgICAgICAgICBlaXRoZXIoVElNRV8xMkgsIFRJTUVfMjRIKSxcbiAgICAgICAgICAvICojL1xuICAgICAgICApXG4gICAgICB9XG4gICAgXVxuICB9O1xuXG4gIGNvbnN0IE5VTUJFUiA9IHtcbiAgICBjbGFzc05hbWU6ICdudW1iZXInLFxuICAgIHJlbGV2YW5jZTogMCxcbiAgICB2YXJpYW50czogW1xuICAgICAge1xuICAgICAgICAvLyBGbG9hdFxuICAgICAgICBiZWdpbjogL1xcYlxcZFtcXGRfXSooKFxcLltcXGRfXSsoRVsrLV0/W1xcZF9dKyk/KXwoRVsrLV0/W1xcZF9dKykpW1JGREAhI10/L1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgLy8gSW50ZWdlciAoYmFzZSAxMClcbiAgICAgICAgYmVnaW46IC9cXGJcXGRbXFxkX10qKChVP1tTSUxdKXxbJSZdKT8vXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICAvLyBJbnRlZ2VyIChiYXNlIDE2KVxuICAgICAgICBiZWdpbjogLyZIW1xcZEEtRl9dKygoVT9bU0lMXSl8WyUmXSk/L1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgLy8gSW50ZWdlciAoYmFzZSA4KVxuICAgICAgICBiZWdpbjogLyZPWzAtN19dKygoVT9bU0lMXSl8WyUmXSk/L1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgLy8gSW50ZWdlciAoYmFzZSAyKVxuICAgICAgICBiZWdpbjogLyZCWzAxX10rKChVP1tTSUxdKXxbJSZdKT8vXG4gICAgICB9XG4gICAgXVxuICB9O1xuXG4gIGNvbnN0IExBQkVMID0ge1xuICAgIGNsYXNzTmFtZTogJ2xhYmVsJyxcbiAgICBiZWdpbjogL15cXHcrOi9cbiAgfTtcblxuICBjb25zdCBET0NfQ09NTUVOVCA9IGhsanMuQ09NTUVOVCgvJycnLywgLyQvLCB7XG4gICAgY29udGFpbnM6IFtcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnZG9jdGFnJyxcbiAgICAgICAgYmVnaW46IC88XFwvPy8sXG4gICAgICAgIGVuZDogLz4vXG4gICAgICB9XG4gICAgXVxuICB9KTtcblxuICBjb25zdCBDT01NRU5UID0gaGxqcy5DT01NRU5UKG51bGwsIC8kLywge1xuICAgIHZhcmlhbnRzOiBbXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAvJy9cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIC8vIFRPRE86IFVzZSBgYmVmb3JlTWF0Y2g6YCBmb3IgbGVhZGluZyBzcGFjZXNcbiAgICAgICAgYmVnaW46IC8oW1xcdCBdfF4pUkVNKD89XFxzKS9cbiAgICAgIH1cbiAgICBdXG4gIH0pO1xuXG4gIGNvbnN0IERJUkVDVElWRVMgPSB7XG4gICAgY2xhc3NOYW1lOiAnbWV0YScsXG4gICAgLy8gVE9ETzogVXNlIGBiZWZvcmVNYXRjaDpgIGZvciBpbmRlbnRhdGlvbiBvbmNlIGF2YWlsYWJsZVxuICAgIGJlZ2luOiAvW1xcdCBdKiMoY29uc3R8ZGlzYWJsZXxlbHNlfGVsc2VpZnxlbmFibGV8ZW5kfGV4dGVybmFsc291cmNlfGlmfHJlZ2lvbilcXGIvLFxuICAgIGVuZDogLyQvLFxuICAgIGtleXdvcmRzOiB7XG4gICAgICAnbWV0YS1rZXl3b3JkJzpcbiAgICAgICAgJ2NvbnN0IGRpc2FibGUgZWxzZSBlbHNlaWYgZW5hYmxlIGVuZCBleHRlcm5hbHNvdXJjZSBpZiByZWdpb24gdGhlbidcbiAgICB9LFxuICAgIGNvbnRhaW5zOiBbIENPTU1FTlQgXVxuICB9O1xuXG4gIHJldHVybiB7XG4gICAgbmFtZTogJ1Zpc3VhbCBCYXNpYyAuTkVUJyxcbiAgICBhbGlhc2VzOiBbICd2YicgXSxcbiAgICBjYXNlX2luc2Vuc2l0aXZlOiB0cnVlLFxuICAgIGNsYXNzTmFtZUFsaWFzZXM6IHtcbiAgICAgIGxhYmVsOiAnc3ltYm9sJ1xuICAgIH0sXG4gICAga2V5d29yZHM6IHtcbiAgICAgIGtleXdvcmQ6XG4gICAgICAgICdhZGRoYW5kbGVyIGFsaWFzIGFnZ3JlZ2F0ZSBhbnNpIGFzIGFzeW5jIGFzc2VtYmx5IGF1dG8gYmluYXJ5IGJ5IGJ5cmVmIGJ5dmFsICcgKyAvKiBhLWIgKi9cbiAgICAgICAgJ2NhbGwgY2FzZSBjYXRjaCBjbGFzcyBjb21wYXJlIGNvbnN0IGNvbnRpbnVlIGN1c3RvbSBkZWNsYXJlIGRlZmF1bHQgZGVsZWdhdGUgZGltIGRpc3RpbmN0IGRvICcgKyAvKiBjLWQgKi9cbiAgICAgICAgJ2VhY2ggZXF1YWxzIGVsc2UgZWxzZWlmIGVuZCBlbnVtIGVyYXNlIGVycm9yIGV2ZW50IGV4aXQgZXhwbGljaXQgZmluYWxseSBmb3IgZnJpZW5kIGZyb20gZnVuY3Rpb24gJyArIC8qIGUtZiAqL1xuICAgICAgICAnZ2V0IGdsb2JhbCBnb3RvIGdyb3VwIGhhbmRsZXMgaWYgaW1wbGVtZW50cyBpbXBvcnRzIGluIGluaGVyaXRzIGludGVyZmFjZSBpbnRvIGl0ZXJhdG9yICcgKyAvKiBnLWkgKi9cbiAgICAgICAgJ2pvaW4ga2V5IGxldCBsaWIgbG9vcCBtZSBtaWQgbW9kdWxlIG11c3Rpbmhlcml0IG11c3RvdmVycmlkZSBteWJhc2UgbXljbGFzcyAnICsgLyogai1tICovXG4gICAgICAgICduYW1lc3BhY2UgbmFycm93aW5nIG5ldyBuZXh0IG5vdGluaGVyaXRhYmxlIG5vdG92ZXJyaWRhYmxlICcgKyAvKiBuICovXG4gICAgICAgICdvZiBvZmYgb24gb3BlcmF0b3Igb3B0aW9uIG9wdGlvbmFsIG9yZGVyIG92ZXJsb2FkcyBvdmVycmlkYWJsZSBvdmVycmlkZXMgJyArIC8qIG8gKi9cbiAgICAgICAgJ3BhcmFtYXJyYXkgcGFydGlhbCBwcmVzZXJ2ZSBwcml2YXRlIHByb3BlcnR5IHByb3RlY3RlZCBwdWJsaWMgJyArIC8qIHAgKi9cbiAgICAgICAgJ3JhaXNlZXZlbnQgcmVhZG9ubHkgcmVkaW0gcmVtb3ZlaGFuZGxlciByZXN1bWUgcmV0dXJuICcgKyAvKiByICovXG4gICAgICAgICdzZWxlY3Qgc2V0IHNoYWRvd3Mgc2hhcmVkIHNraXAgc3RhdGljIHN0ZXAgc3RvcCBzdHJ1Y3R1cmUgc3RyaWN0IHN1YiBzeW5jbG9jayAnICsgLyogcyAqL1xuICAgICAgICAndGFrZSB0ZXh0IHRoZW4gdGhyb3cgdG8gdHJ5IHVuaWNvZGUgdW50aWwgdXNpbmcgd2hlbiB3aGVyZSB3aGlsZSB3aWRlbmluZyB3aXRoIHdpdGhldmVudHMgd3JpdGVvbmx5IHlpZWxkJyAvKiB0LXkgKi8sXG4gICAgICBidWlsdF9pbjpcbiAgICAgICAgLy8gT3BlcmF0b3JzIGh0dHBzOi8vZG9jcy5taWNyb3NvZnQuY29tL2RvdG5ldC92aXN1YWwtYmFzaWMvbGFuZ3VhZ2UtcmVmZXJlbmNlL29wZXJhdG9yc1xuICAgICAgICAnYWRkcmVzc29mIGFuZCBhbmRhbHNvIGF3YWl0IGRpcmVjdGNhc3QgZ2V0dHlwZSBnZXR4bWxuYW1lc3BhY2UgaXMgaXNmYWxzZSBpc25vdCBpc3RydWUgbGlrZSBtb2QgbmFtZW9mIG5ldyBub3Qgb3Igb3JlbHNlIHRyeWNhc3QgdHlwZW9mIHhvciAnICtcbiAgICAgICAgLy8gVHlwZSBDb252ZXJzaW9uIEZ1bmN0aW9ucyBodHRwczovL2RvY3MubWljcm9zb2Z0LmNvbS9kb3RuZXQvdmlzdWFsLWJhc2ljL2xhbmd1YWdlLXJlZmVyZW5jZS9mdW5jdGlvbnMvdHlwZS1jb252ZXJzaW9uLWZ1bmN0aW9uc1xuICAgICAgICAnY2Jvb2wgY2J5dGUgY2NoYXIgY2RhdGUgY2RibCBjZGVjIGNpbnQgY2xuZyBjb2JqIGNzYnl0ZSBjc2hvcnQgY3NuZyBjc3RyIGN1aW50IGN1bG5nIGN1c2hvcnQnLFxuICAgICAgdHlwZTpcbiAgICAgICAgLy8gRGF0YSB0eXBlcyBodHRwczovL2RvY3MubWljcm9zb2Z0LmNvbS9kb3RuZXQvdmlzdWFsLWJhc2ljL2xhbmd1YWdlLXJlZmVyZW5jZS9kYXRhLXR5cGVzXG4gICAgICAgICdib29sZWFuIGJ5dGUgY2hhciBkYXRlIGRlY2ltYWwgZG91YmxlIGludGVnZXIgbG9uZyBvYmplY3Qgc2J5dGUgc2hvcnQgc2luZ2xlIHN0cmluZyB1aW50ZWdlciB1bG9uZyB1c2hvcnQnLFxuICAgICAgbGl0ZXJhbDogJ3RydWUgZmFsc2Ugbm90aGluZydcbiAgICB9LFxuICAgIGlsbGVnYWw6XG4gICAgICAnLy98XFxcXHt8XFxcXH18ZW5kaWZ8Z29zdWJ8dmFyaWFudHx3ZW5kfF5cXFxcJCAnIC8qIHJlc2VydmVkIGRlcHJlY2F0ZWQga2V5d29yZHMgKi8sXG4gICAgY29udGFpbnM6IFtcbiAgICAgIENIQVJBQ1RFUixcbiAgICAgIFNUUklORyxcbiAgICAgIERBVEUsXG4gICAgICBOVU1CRVIsXG4gICAgICBMQUJFTCxcbiAgICAgIERPQ19DT01NRU5ULFxuICAgICAgQ09NTUVOVCxcbiAgICAgIERJUkVDVElWRVNcbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gdmJuZXQ7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=