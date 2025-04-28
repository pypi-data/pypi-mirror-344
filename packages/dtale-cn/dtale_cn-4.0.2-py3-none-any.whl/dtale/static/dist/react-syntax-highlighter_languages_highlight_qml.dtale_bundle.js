(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_qml"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/qml.js":
/*!**********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/qml.js ***!
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
 * @param {...(RegExp | string) } args
 * @returns {string}
 */
function concat(...args) {
  const joined = args.map((x) => source(x)).join("");
  return joined;
}

/*
Language: QML
Requires: javascript.js, xml.js
Author: John Foster <jfoster@esri.com>
Description: Syntax highlighting for the Qt Quick QML scripting language, based mostly off
             the JavaScript parser.
Website: https://doc.qt.io/qt-5/qmlapplications.html
Category: scripting
*/

function qml(hljs) {
  const KEYWORDS = {
    keyword:
      'in of on if for while finally var new function do return void else break catch ' +
      'instanceof with throw case default try this switch continue typeof delete ' +
      'let yield const export super debugger as async await import',
    literal:
      'true false null undefined NaN Infinity',
    built_in:
      'eval isFinite isNaN parseFloat parseInt decodeURI decodeURIComponent ' +
      'encodeURI encodeURIComponent escape unescape Object Function Boolean Error ' +
      'EvalError InternalError RangeError ReferenceError StopIteration SyntaxError ' +
      'TypeError URIError Number Math Date String RegExp Array Float32Array ' +
      'Float64Array Int16Array Int32Array Int8Array Uint16Array Uint32Array ' +
      'Uint8Array Uint8ClampedArray ArrayBuffer DataView JSON Intl arguments require ' +
      'module console window document Symbol Set Map WeakSet WeakMap Proxy Reflect ' +
      'Behavior bool color coordinate date double enumeration font geocircle georectangle ' +
      'geoshape int list matrix4x4 parent point quaternion real rect ' +
      'size string url variant vector2d vector3d vector4d ' +
      'Promise'
  };

  const QML_IDENT_RE = '[a-zA-Z_][a-zA-Z0-9\\._]*';

  // Isolate property statements. Ends at a :, =, ;, ,, a comment or end of line.
  // Use property class.
  const PROPERTY = {
    className: 'keyword',
    begin: '\\bproperty\\b',
    starts: {
      className: 'string',
      end: '(:|=|;|,|//|/\\*|$)',
      returnEnd: true
    }
  };

  // Isolate signal statements. Ends at a ) a comment or end of line.
  // Use property class.
  const SIGNAL = {
    className: 'keyword',
    begin: '\\bsignal\\b',
    starts: {
      className: 'string',
      end: '(\\(|:|=|;|,|//|/\\*|$)',
      returnEnd: true
    }
  };

  // id: is special in QML. When we see id: we want to mark the id: as attribute and
  // emphasize the token following.
  const ID_ID = {
    className: 'attribute',
    begin: '\\bid\\s*:',
    starts: {
      className: 'string',
      end: QML_IDENT_RE,
      returnEnd: false
    }
  };

  // Find QML object attribute. An attribute is a QML identifier followed by :.
  // Unfortunately it's hard to know where it ends, as it may contain scalars,
  // objects, object definitions, or javascript. The true end is either when the parent
  // ends or the next attribute is detected.
  const QML_ATTRIBUTE = {
    begin: QML_IDENT_RE + '\\s*:',
    returnBegin: true,
    contains: [
      {
        className: 'attribute',
        begin: QML_IDENT_RE,
        end: '\\s*:',
        excludeEnd: true,
        relevance: 0
      }
    ],
    relevance: 0
  };

  // Find QML object. A QML object is a QML identifier followed by { and ends at the matching }.
  // All we really care about is finding IDENT followed by { and just mark up the IDENT and ignore the {.
  const QML_OBJECT = {
    begin: concat(QML_IDENT_RE, /\s*\{/),
    end: /\{/,
    returnBegin: true,
    relevance: 0,
    contains: [
      hljs.inherit(hljs.TITLE_MODE, {
        begin: QML_IDENT_RE
      })
    ]
  };

  return {
    name: 'QML',
    aliases: [ 'qt' ],
    case_insensitive: false,
    keywords: KEYWORDS,
    contains: [
      {
        className: 'meta',
        begin: /^\s*['"]use (strict|asm)['"]/
      },
      hljs.APOS_STRING_MODE,
      hljs.QUOTE_STRING_MODE,
      { // template string
        className: 'string',
        begin: '`',
        end: '`',
        contains: [
          hljs.BACKSLASH_ESCAPE,
          {
            className: 'subst',
            begin: '\\$\\{',
            end: '\\}'
          }
        ]
      },
      hljs.C_LINE_COMMENT_MODE,
      hljs.C_BLOCK_COMMENT_MODE,
      {
        className: 'number',
        variants: [
          {
            begin: '\\b(0[bB][01]+)'
          },
          {
            begin: '\\b(0[oO][0-7]+)'
          },
          {
            begin: hljs.C_NUMBER_RE
          }
        ],
        relevance: 0
      },
      { // "value" container
        begin: '(' + hljs.RE_STARTERS_RE + '|\\b(case|return|throw)\\b)\\s*',
        keywords: 'return throw case',
        contains: [
          hljs.C_LINE_COMMENT_MODE,
          hljs.C_BLOCK_COMMENT_MODE,
          hljs.REGEXP_MODE,
          { // E4X / JSX
            begin: /</,
            end: />\s*[);\]]/,
            relevance: 0,
            subLanguage: 'xml'
          }
        ],
        relevance: 0
      },
      SIGNAL,
      PROPERTY,
      {
        className: 'function',
        beginKeywords: 'function',
        end: /\{/,
        excludeEnd: true,
        contains: [
          hljs.inherit(hljs.TITLE_MODE, {
            begin: /[A-Za-z$_][0-9A-Za-z$_]*/
          }),
          {
            className: 'params',
            begin: /\(/,
            end: /\)/,
            excludeBegin: true,
            excludeEnd: true,
            contains: [
              hljs.C_LINE_COMMENT_MODE,
              hljs.C_BLOCK_COMMENT_MODE
            ]
          }
        ],
        illegal: /\[|%/
      },
      {
        // hack: prevents detection of keywords after dots
        begin: '\\.' + hljs.IDENT_RE,
        relevance: 0
      },
      ID_ID,
      QML_ATTRIBUTE,
      QML_OBJECT
    ],
    illegal: /#/
  };
}

module.exports = qml;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfcW1sLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0EsV0FBVyxRQUFRO0FBQ25CLGFBQWE7QUFDYjs7QUFFQTtBQUNBLFdBQVcsa0JBQWtCO0FBQzdCLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBOztBQUVBO0FBQ0EsV0FBVyx1QkFBdUI7QUFDbEMsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTs7QUFFQSxtREFBbUQ7QUFDbkQ7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0Esa0JBQWtCO0FBQ2xCO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLHNCQUFzQjtBQUN0QjtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEscUVBQXFFLDBCQUEwQjtBQUMvRiw2REFBNkQsMkNBQTJDO0FBQ3hHO0FBQ0Esc0NBQXNDO0FBQ3RDLFlBQVk7QUFDWjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQSxRQUFRO0FBQ1I7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSwwQkFBMEI7QUFDMUIscUJBQXFCO0FBQ3JCO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQTtBQUNBLFdBQVc7QUFDWDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQLFFBQVE7QUFDUjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxZQUFZO0FBQ1o7QUFDQSx5QkFBeUI7QUFDekI7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsZ0JBQWdCO0FBQ2hCO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsV0FBVztBQUNYO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9xbWwuanMiXSwic291cmNlc0NvbnRlbnQiOlsiLyoqXG4gKiBAcGFyYW0ge3N0cmluZ30gdmFsdWVcbiAqIEByZXR1cm5zIHtSZWdFeHB9XG4gKiAqL1xuXG4vKipcbiAqIEBwYXJhbSB7UmVnRXhwIHwgc3RyaW5nIH0gcmVcbiAqIEByZXR1cm5zIHtzdHJpbmd9XG4gKi9cbmZ1bmN0aW9uIHNvdXJjZShyZSkge1xuICBpZiAoIXJlKSByZXR1cm4gbnVsbDtcbiAgaWYgKHR5cGVvZiByZSA9PT0gXCJzdHJpbmdcIikgcmV0dXJuIHJlO1xuXG4gIHJldHVybiByZS5zb3VyY2U7XG59XG5cbi8qKlxuICogQHBhcmFtIHsuLi4oUmVnRXhwIHwgc3RyaW5nKSB9IGFyZ3NcbiAqIEByZXR1cm5zIHtzdHJpbmd9XG4gKi9cbmZ1bmN0aW9uIGNvbmNhdCguLi5hcmdzKSB7XG4gIGNvbnN0IGpvaW5lZCA9IGFyZ3MubWFwKCh4KSA9PiBzb3VyY2UoeCkpLmpvaW4oXCJcIik7XG4gIHJldHVybiBqb2luZWQ7XG59XG5cbi8qXG5MYW5ndWFnZTogUU1MXG5SZXF1aXJlczogamF2YXNjcmlwdC5qcywgeG1sLmpzXG5BdXRob3I6IEpvaG4gRm9zdGVyIDxqZm9zdGVyQGVzcmkuY29tPlxuRGVzY3JpcHRpb246IFN5bnRheCBoaWdobGlnaHRpbmcgZm9yIHRoZSBRdCBRdWljayBRTUwgc2NyaXB0aW5nIGxhbmd1YWdlLCBiYXNlZCBtb3N0bHkgb2ZmXG4gICAgICAgICAgICAgdGhlIEphdmFTY3JpcHQgcGFyc2VyLlxuV2Vic2l0ZTogaHR0cHM6Ly9kb2MucXQuaW8vcXQtNS9xbWxhcHBsaWNhdGlvbnMuaHRtbFxuQ2F0ZWdvcnk6IHNjcmlwdGluZ1xuKi9cblxuZnVuY3Rpb24gcW1sKGhsanMpIHtcbiAgY29uc3QgS0VZV09SRFMgPSB7XG4gICAga2V5d29yZDpcbiAgICAgICdpbiBvZiBvbiBpZiBmb3Igd2hpbGUgZmluYWxseSB2YXIgbmV3IGZ1bmN0aW9uIGRvIHJldHVybiB2b2lkIGVsc2UgYnJlYWsgY2F0Y2ggJyArXG4gICAgICAnaW5zdGFuY2VvZiB3aXRoIHRocm93IGNhc2UgZGVmYXVsdCB0cnkgdGhpcyBzd2l0Y2ggY29udGludWUgdHlwZW9mIGRlbGV0ZSAnICtcbiAgICAgICdsZXQgeWllbGQgY29uc3QgZXhwb3J0IHN1cGVyIGRlYnVnZ2VyIGFzIGFzeW5jIGF3YWl0IGltcG9ydCcsXG4gICAgbGl0ZXJhbDpcbiAgICAgICd0cnVlIGZhbHNlIG51bGwgdW5kZWZpbmVkIE5hTiBJbmZpbml0eScsXG4gICAgYnVpbHRfaW46XG4gICAgICAnZXZhbCBpc0Zpbml0ZSBpc05hTiBwYXJzZUZsb2F0IHBhcnNlSW50IGRlY29kZVVSSSBkZWNvZGVVUklDb21wb25lbnQgJyArXG4gICAgICAnZW5jb2RlVVJJIGVuY29kZVVSSUNvbXBvbmVudCBlc2NhcGUgdW5lc2NhcGUgT2JqZWN0IEZ1bmN0aW9uIEJvb2xlYW4gRXJyb3IgJyArXG4gICAgICAnRXZhbEVycm9yIEludGVybmFsRXJyb3IgUmFuZ2VFcnJvciBSZWZlcmVuY2VFcnJvciBTdG9wSXRlcmF0aW9uIFN5bnRheEVycm9yICcgK1xuICAgICAgJ1R5cGVFcnJvciBVUklFcnJvciBOdW1iZXIgTWF0aCBEYXRlIFN0cmluZyBSZWdFeHAgQXJyYXkgRmxvYXQzMkFycmF5ICcgK1xuICAgICAgJ0Zsb2F0NjRBcnJheSBJbnQxNkFycmF5IEludDMyQXJyYXkgSW50OEFycmF5IFVpbnQxNkFycmF5IFVpbnQzMkFycmF5ICcgK1xuICAgICAgJ1VpbnQ4QXJyYXkgVWludDhDbGFtcGVkQXJyYXkgQXJyYXlCdWZmZXIgRGF0YVZpZXcgSlNPTiBJbnRsIGFyZ3VtZW50cyByZXF1aXJlICcgK1xuICAgICAgJ21vZHVsZSBjb25zb2xlIHdpbmRvdyBkb2N1bWVudCBTeW1ib2wgU2V0IE1hcCBXZWFrU2V0IFdlYWtNYXAgUHJveHkgUmVmbGVjdCAnICtcbiAgICAgICdCZWhhdmlvciBib29sIGNvbG9yIGNvb3JkaW5hdGUgZGF0ZSBkb3VibGUgZW51bWVyYXRpb24gZm9udCBnZW9jaXJjbGUgZ2VvcmVjdGFuZ2xlICcgK1xuICAgICAgJ2dlb3NoYXBlIGludCBsaXN0IG1hdHJpeDR4NCBwYXJlbnQgcG9pbnQgcXVhdGVybmlvbiByZWFsIHJlY3QgJyArXG4gICAgICAnc2l6ZSBzdHJpbmcgdXJsIHZhcmlhbnQgdmVjdG9yMmQgdmVjdG9yM2QgdmVjdG9yNGQgJyArXG4gICAgICAnUHJvbWlzZSdcbiAgfTtcblxuICBjb25zdCBRTUxfSURFTlRfUkUgPSAnW2EtekEtWl9dW2EtekEtWjAtOVxcXFwuX10qJztcblxuICAvLyBJc29sYXRlIHByb3BlcnR5IHN0YXRlbWVudHMuIEVuZHMgYXQgYSA6LCA9LCA7LCAsLCBhIGNvbW1lbnQgb3IgZW5kIG9mIGxpbmUuXG4gIC8vIFVzZSBwcm9wZXJ0eSBjbGFzcy5cbiAgY29uc3QgUFJPUEVSVFkgPSB7XG4gICAgY2xhc3NOYW1lOiAna2V5d29yZCcsXG4gICAgYmVnaW46ICdcXFxcYnByb3BlcnR5XFxcXGInLFxuICAgIHN0YXJ0czoge1xuICAgICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICAgIGVuZDogJyg6fD18O3wsfC8vfC9cXFxcKnwkKScsXG4gICAgICByZXR1cm5FbmQ6IHRydWVcbiAgICB9XG4gIH07XG5cbiAgLy8gSXNvbGF0ZSBzaWduYWwgc3RhdGVtZW50cy4gRW5kcyBhdCBhICkgYSBjb21tZW50IG9yIGVuZCBvZiBsaW5lLlxuICAvLyBVc2UgcHJvcGVydHkgY2xhc3MuXG4gIGNvbnN0IFNJR05BTCA9IHtcbiAgICBjbGFzc05hbWU6ICdrZXl3b3JkJyxcbiAgICBiZWdpbjogJ1xcXFxic2lnbmFsXFxcXGInLFxuICAgIHN0YXJ0czoge1xuICAgICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICAgIGVuZDogJyhcXFxcKHw6fD18O3wsfC8vfC9cXFxcKnwkKScsXG4gICAgICByZXR1cm5FbmQ6IHRydWVcbiAgICB9XG4gIH07XG5cbiAgLy8gaWQ6IGlzIHNwZWNpYWwgaW4gUU1MLiBXaGVuIHdlIHNlZSBpZDogd2Ugd2FudCB0byBtYXJrIHRoZSBpZDogYXMgYXR0cmlidXRlIGFuZFxuICAvLyBlbXBoYXNpemUgdGhlIHRva2VuIGZvbGxvd2luZy5cbiAgY29uc3QgSURfSUQgPSB7XG4gICAgY2xhc3NOYW1lOiAnYXR0cmlidXRlJyxcbiAgICBiZWdpbjogJ1xcXFxiaWRcXFxccyo6JyxcbiAgICBzdGFydHM6IHtcbiAgICAgIGNsYXNzTmFtZTogJ3N0cmluZycsXG4gICAgICBlbmQ6IFFNTF9JREVOVF9SRSxcbiAgICAgIHJldHVybkVuZDogZmFsc2VcbiAgICB9XG4gIH07XG5cbiAgLy8gRmluZCBRTUwgb2JqZWN0IGF0dHJpYnV0ZS4gQW4gYXR0cmlidXRlIGlzIGEgUU1MIGlkZW50aWZpZXIgZm9sbG93ZWQgYnkgOi5cbiAgLy8gVW5mb3J0dW5hdGVseSBpdCdzIGhhcmQgdG8ga25vdyB3aGVyZSBpdCBlbmRzLCBhcyBpdCBtYXkgY29udGFpbiBzY2FsYXJzLFxuICAvLyBvYmplY3RzLCBvYmplY3QgZGVmaW5pdGlvbnMsIG9yIGphdmFzY3JpcHQuIFRoZSB0cnVlIGVuZCBpcyBlaXRoZXIgd2hlbiB0aGUgcGFyZW50XG4gIC8vIGVuZHMgb3IgdGhlIG5leHQgYXR0cmlidXRlIGlzIGRldGVjdGVkLlxuICBjb25zdCBRTUxfQVRUUklCVVRFID0ge1xuICAgIGJlZ2luOiBRTUxfSURFTlRfUkUgKyAnXFxcXHMqOicsXG4gICAgcmV0dXJuQmVnaW46IHRydWUsXG4gICAgY29udGFpbnM6IFtcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnYXR0cmlidXRlJyxcbiAgICAgICAgYmVnaW46IFFNTF9JREVOVF9SRSxcbiAgICAgICAgZW5kOiAnXFxcXHMqOicsXG4gICAgICAgIGV4Y2x1ZGVFbmQ6IHRydWUsXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfVxuICAgIF0sXG4gICAgcmVsZXZhbmNlOiAwXG4gIH07XG5cbiAgLy8gRmluZCBRTUwgb2JqZWN0LiBBIFFNTCBvYmplY3QgaXMgYSBRTUwgaWRlbnRpZmllciBmb2xsb3dlZCBieSB7IGFuZCBlbmRzIGF0IHRoZSBtYXRjaGluZyB9LlxuICAvLyBBbGwgd2UgcmVhbGx5IGNhcmUgYWJvdXQgaXMgZmluZGluZyBJREVOVCBmb2xsb3dlZCBieSB7IGFuZCBqdXN0IG1hcmsgdXAgdGhlIElERU5UIGFuZCBpZ25vcmUgdGhlIHsuXG4gIGNvbnN0IFFNTF9PQkpFQ1QgPSB7XG4gICAgYmVnaW46IGNvbmNhdChRTUxfSURFTlRfUkUsIC9cXHMqXFx7LyksXG4gICAgZW5kOiAvXFx7LyxcbiAgICByZXR1cm5CZWdpbjogdHJ1ZSxcbiAgICByZWxldmFuY2U6IDAsXG4gICAgY29udGFpbnM6IFtcbiAgICAgIGhsanMuaW5oZXJpdChobGpzLlRJVExFX01PREUsIHtcbiAgICAgICAgYmVnaW46IFFNTF9JREVOVF9SRVxuICAgICAgfSlcbiAgICBdXG4gIH07XG5cbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnUU1MJyxcbiAgICBhbGlhc2VzOiBbICdxdCcgXSxcbiAgICBjYXNlX2luc2Vuc2l0aXZlOiBmYWxzZSxcbiAgICBrZXl3b3JkczogS0VZV09SRFMsXG4gICAgY29udGFpbnM6IFtcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnbWV0YScsXG4gICAgICAgIGJlZ2luOiAvXlxccypbJ1wiXXVzZSAoc3RyaWN0fGFzbSlbJ1wiXS9cbiAgICAgIH0sXG4gICAgICBobGpzLkFQT1NfU1RSSU5HX01PREUsXG4gICAgICBobGpzLlFVT1RFX1NUUklOR19NT0RFLFxuICAgICAgeyAvLyB0ZW1wbGF0ZSBzdHJpbmdcbiAgICAgICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICAgICAgYmVnaW46ICdgJyxcbiAgICAgICAgZW5kOiAnYCcsXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgaGxqcy5CQUNLU0xBU0hfRVNDQVBFLFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGNsYXNzTmFtZTogJ3N1YnN0JyxcbiAgICAgICAgICAgIGJlZ2luOiAnXFxcXCRcXFxceycsXG4gICAgICAgICAgICBlbmQ6ICdcXFxcfSdcbiAgICAgICAgICB9XG4gICAgICAgIF1cbiAgICAgIH0sXG4gICAgICBobGpzLkNfTElORV9DT01NRU5UX01PREUsXG4gICAgICBobGpzLkNfQkxPQ0tfQ09NTUVOVF9NT0RFLFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdudW1iZXInLFxuICAgICAgICB2YXJpYW50czogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiAnXFxcXGIoMFtiQl1bMDFdKyknXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbjogJ1xcXFxiKDBbb09dWzAtN10rKSdcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiBobGpzLkNfTlVNQkVSX1JFXG4gICAgICAgICAgfVxuICAgICAgICBdLFxuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH0sXG4gICAgICB7IC8vIFwidmFsdWVcIiBjb250YWluZXJcbiAgICAgICAgYmVnaW46ICcoJyArIGhsanMuUkVfU1RBUlRFUlNfUkUgKyAnfFxcXFxiKGNhc2V8cmV0dXJufHRocm93KVxcXFxiKVxcXFxzKicsXG4gICAgICAgIGtleXdvcmRzOiAncmV0dXJuIHRocm93IGNhc2UnLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIGhsanMuQ19MSU5FX0NPTU1FTlRfTU9ERSxcbiAgICAgICAgICBobGpzLkNfQkxPQ0tfQ09NTUVOVF9NT0RFLFxuICAgICAgICAgIGhsanMuUkVHRVhQX01PREUsXG4gICAgICAgICAgeyAvLyBFNFggLyBKU1hcbiAgICAgICAgICAgIGJlZ2luOiAvPC8sXG4gICAgICAgICAgICBlbmQ6IC8+XFxzKlspO1xcXV0vLFxuICAgICAgICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgICAgICAgc3ViTGFuZ3VhZ2U6ICd4bWwnXG4gICAgICAgICAgfVxuICAgICAgICBdLFxuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH0sXG4gICAgICBTSUdOQUwsXG4gICAgICBQUk9QRVJUWSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnZnVuY3Rpb24nLFxuICAgICAgICBiZWdpbktleXdvcmRzOiAnZnVuY3Rpb24nLFxuICAgICAgICBlbmQ6IC9cXHsvLFxuICAgICAgICBleGNsdWRlRW5kOiB0cnVlLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIGhsanMuaW5oZXJpdChobGpzLlRJVExFX01PREUsIHtcbiAgICAgICAgICAgIGJlZ2luOiAvW0EtWmEteiRfXVswLTlBLVphLXokX10qL1xuICAgICAgICAgIH0pLFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGNsYXNzTmFtZTogJ3BhcmFtcycsXG4gICAgICAgICAgICBiZWdpbjogL1xcKC8sXG4gICAgICAgICAgICBlbmQ6IC9cXCkvLFxuICAgICAgICAgICAgZXhjbHVkZUJlZ2luOiB0cnVlLFxuICAgICAgICAgICAgZXhjbHVkZUVuZDogdHJ1ZSxcbiAgICAgICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgICAgIGhsanMuQ19MSU5FX0NPTU1FTlRfTU9ERSxcbiAgICAgICAgICAgICAgaGxqcy5DX0JMT0NLX0NPTU1FTlRfTU9ERVxuICAgICAgICAgICAgXVxuICAgICAgICAgIH1cbiAgICAgICAgXSxcbiAgICAgICAgaWxsZWdhbDogL1xcW3wlL1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgLy8gaGFjazogcHJldmVudHMgZGV0ZWN0aW9uIG9mIGtleXdvcmRzIGFmdGVyIGRvdHNcbiAgICAgICAgYmVnaW46ICdcXFxcLicgKyBobGpzLklERU5UX1JFLFxuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH0sXG4gICAgICBJRF9JRCxcbiAgICAgIFFNTF9BVFRSSUJVVEUsXG4gICAgICBRTUxfT0JKRUNUXG4gICAgXSxcbiAgICBpbGxlZ2FsOiAvIy9cbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBxbWw7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=