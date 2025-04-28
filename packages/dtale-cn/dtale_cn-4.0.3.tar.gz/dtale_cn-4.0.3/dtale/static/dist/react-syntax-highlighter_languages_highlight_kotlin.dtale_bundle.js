(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_kotlin"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/kotlin.js":
/*!*************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/kotlin.js ***!
  \*************************************************************************************************/
/***/ ((module) => {

// https://docs.oracle.com/javase/specs/jls/se15/html/jls-3.html#jls-3.10
var decimalDigits = '[0-9](_*[0-9])*';
var frac = `\\.(${decimalDigits})`;
var hexDigits = '[0-9a-fA-F](_*[0-9a-fA-F])*';
var NUMERIC = {
  className: 'number',
  variants: [
    // DecimalFloatingPointLiteral
    // including ExponentPart
    { begin: `(\\b(${decimalDigits})((${frac})|\\.)?|(${frac}))` +
      `[eE][+-]?(${decimalDigits})[fFdD]?\\b` },
    // excluding ExponentPart
    { begin: `\\b(${decimalDigits})((${frac})[fFdD]?\\b|\\.([fFdD]\\b)?)` },
    { begin: `(${frac})[fFdD]?\\b` },
    { begin: `\\b(${decimalDigits})[fFdD]\\b` },

    // HexadecimalFloatingPointLiteral
    { begin: `\\b0[xX]((${hexDigits})\\.?|(${hexDigits})?\\.(${hexDigits}))` +
      `[pP][+-]?(${decimalDigits})[fFdD]?\\b` },

    // DecimalIntegerLiteral
    { begin: '\\b(0|[1-9](_*[0-9])*)[lL]?\\b' },

    // HexIntegerLiteral
    { begin: `\\b0[xX](${hexDigits})[lL]?\\b` },

    // OctalIntegerLiteral
    { begin: '\\b0(_*[0-7])*[lL]?\\b' },

    // BinaryIntegerLiteral
    { begin: '\\b0[bB][01](_*[01])*[lL]?\\b' },
  ],
  relevance: 0
};

/*
 Language: Kotlin
 Description: Kotlin is an OSS statically typed programming language that targets the JVM, Android, JavaScript and Native.
 Author: Sergey Mashkov <cy6erGn0m@gmail.com>
 Website: https://kotlinlang.org
 Category: common
 */

function kotlin(hljs) {
  const KEYWORDS = {
    keyword:
      'abstract as val var vararg get set class object open private protected public noinline ' +
      'crossinline dynamic final enum if else do while for when throw try catch finally ' +
      'import package is in fun override companion reified inline lateinit init ' +
      'interface annotation data sealed internal infix operator out by constructor super ' +
      'tailrec where const inner suspend typealias external expect actual',
    built_in:
      'Byte Short Char Int Long Boolean Float Double Void Unit Nothing',
    literal:
      'true false null'
  };
  const KEYWORDS_WITH_LABEL = {
    className: 'keyword',
    begin: /\b(break|continue|return|this)\b/,
    starts: {
      contains: [
        {
          className: 'symbol',
          begin: /@\w+/
        }
      ]
    }
  };
  const LABEL = {
    className: 'symbol',
    begin: hljs.UNDERSCORE_IDENT_RE + '@'
  };

  // for string templates
  const SUBST = {
    className: 'subst',
    begin: /\$\{/,
    end: /\}/,
    contains: [ hljs.C_NUMBER_MODE ]
  };
  const VARIABLE = {
    className: 'variable',
    begin: '\\$' + hljs.UNDERSCORE_IDENT_RE
  };
  const STRING = {
    className: 'string',
    variants: [
      {
        begin: '"""',
        end: '"""(?=[^"])',
        contains: [
          VARIABLE,
          SUBST
        ]
      },
      // Can't use built-in modes easily, as we want to use STRING in the meta
      // context as 'meta-string' and there's no syntax to remove explicitly set
      // classNames in built-in modes.
      {
        begin: '\'',
        end: '\'',
        illegal: /\n/,
        contains: [ hljs.BACKSLASH_ESCAPE ]
      },
      {
        begin: '"',
        end: '"',
        illegal: /\n/,
        contains: [
          hljs.BACKSLASH_ESCAPE,
          VARIABLE,
          SUBST
        ]
      }
    ]
  };
  SUBST.contains.push(STRING);

  const ANNOTATION_USE_SITE = {
    className: 'meta',
    begin: '@(?:file|property|field|get|set|receiver|param|setparam|delegate)\\s*:(?:\\s*' + hljs.UNDERSCORE_IDENT_RE + ')?'
  };
  const ANNOTATION = {
    className: 'meta',
    begin: '@' + hljs.UNDERSCORE_IDENT_RE,
    contains: [
      {
        begin: /\(/,
        end: /\)/,
        contains: [
          hljs.inherit(STRING, {
            className: 'meta-string'
          })
        ]
      }
    ]
  };

  // https://kotlinlang.org/docs/reference/whatsnew11.html#underscores-in-numeric-literals
  // According to the doc above, the number mode of kotlin is the same as java 8,
  // so the code below is copied from java.js
  const KOTLIN_NUMBER_MODE = NUMERIC;
  const KOTLIN_NESTED_COMMENT = hljs.COMMENT(
    '/\\*', '\\*/',
    {
      contains: [ hljs.C_BLOCK_COMMENT_MODE ]
    }
  );
  const KOTLIN_PAREN_TYPE = {
    variants: [
      {
        className: 'type',
        begin: hljs.UNDERSCORE_IDENT_RE
      },
      {
        begin: /\(/,
        end: /\)/,
        contains: [] // defined later
      }
    ]
  };
  const KOTLIN_PAREN_TYPE2 = KOTLIN_PAREN_TYPE;
  KOTLIN_PAREN_TYPE2.variants[1].contains = [ KOTLIN_PAREN_TYPE ];
  KOTLIN_PAREN_TYPE.variants[1].contains = [ KOTLIN_PAREN_TYPE2 ];

  return {
    name: 'Kotlin',
    aliases: [ 'kt', 'kts' ],
    keywords: KEYWORDS,
    contains: [
      hljs.COMMENT(
        '/\\*\\*',
        '\\*/',
        {
          relevance: 0,
          contains: [
            {
              className: 'doctag',
              begin: '@[A-Za-z]+'
            }
          ]
        }
      ),
      hljs.C_LINE_COMMENT_MODE,
      KOTLIN_NESTED_COMMENT,
      KEYWORDS_WITH_LABEL,
      LABEL,
      ANNOTATION_USE_SITE,
      ANNOTATION,
      {
        className: 'function',
        beginKeywords: 'fun',
        end: '[(]|$',
        returnBegin: true,
        excludeEnd: true,
        keywords: KEYWORDS,
        relevance: 5,
        contains: [
          {
            begin: hljs.UNDERSCORE_IDENT_RE + '\\s*\\(',
            returnBegin: true,
            relevance: 0,
            contains: [ hljs.UNDERSCORE_TITLE_MODE ]
          },
          {
            className: 'type',
            begin: /</,
            end: />/,
            keywords: 'reified',
            relevance: 0
          },
          {
            className: 'params',
            begin: /\(/,
            end: /\)/,
            endsParent: true,
            keywords: KEYWORDS,
            relevance: 0,
            contains: [
              {
                begin: /:/,
                end: /[=,\/]/,
                endsWithParent: true,
                contains: [
                  KOTLIN_PAREN_TYPE,
                  hljs.C_LINE_COMMENT_MODE,
                  KOTLIN_NESTED_COMMENT
                ],
                relevance: 0
              },
              hljs.C_LINE_COMMENT_MODE,
              KOTLIN_NESTED_COMMENT,
              ANNOTATION_USE_SITE,
              ANNOTATION,
              STRING,
              hljs.C_NUMBER_MODE
            ]
          },
          KOTLIN_NESTED_COMMENT
        ]
      },
      {
        className: 'class',
        beginKeywords: 'class interface trait', // remove 'trait' when removed from KEYWORDS
        end: /[:\{(]|$/,
        excludeEnd: true,
        illegal: 'extends implements',
        contains: [
          {
            beginKeywords: 'public protected internal private constructor'
          },
          hljs.UNDERSCORE_TITLE_MODE,
          {
            className: 'type',
            begin: /</,
            end: />/,
            excludeBegin: true,
            excludeEnd: true,
            relevance: 0
          },
          {
            className: 'type',
            begin: /[,:]\s*/,
            end: /[<\(,]|$/,
            excludeBegin: true,
            returnEnd: true
          },
          ANNOTATION_USE_SITE,
          ANNOTATION
        ]
      },
      STRING,
      {
        className: 'meta',
        begin: "^#!/usr/bin/env",
        end: '$',
        illegal: '\n'
      },
      KOTLIN_NUMBER_MODE
    ]
  };
}

module.exports = kotlin;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfa290bGluLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQSxrQkFBa0IsY0FBYztBQUNoQztBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxNQUFNLGVBQWUsY0FBYyxLQUFLLEtBQUssV0FBVyxLQUFLO0FBQzdELG1CQUFtQixjQUFjLGNBQWM7QUFDL0M7QUFDQSxNQUFNLGNBQWMsY0FBYyxLQUFLLEtBQUssK0JBQStCO0FBQzNFLE1BQU0sV0FBVyxLQUFLLGNBQWM7QUFDcEMsTUFBTSxjQUFjLGNBQWMsYUFBYTs7QUFFL0M7QUFDQSxNQUFNLG9CQUFvQixVQUFVLFNBQVMsVUFBVSxRQUFRLFVBQVU7QUFDekUsbUJBQW1CLGNBQWMsY0FBYzs7QUFFL0M7QUFDQSxNQUFNLHlDQUF5Qzs7QUFFL0M7QUFDQSxNQUFNLG1CQUFtQixVQUFVLFlBQVk7O0FBRS9DO0FBQ0EsTUFBTSxpQ0FBaUM7O0FBRXZDO0FBQ0EsTUFBTSx3Q0FBd0M7QUFDOUM7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0EsZ0JBQWdCO0FBQ2hCLFlBQVk7QUFDWjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsV0FBVztBQUNYO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLGVBQWU7QUFDZjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFdBQVc7QUFDWDtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLGtCQUFrQjtBQUNsQjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsV0FBVztBQUNYO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsV0FBVztBQUNYO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL2tvdGxpbi5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvLyBodHRwczovL2RvY3Mub3JhY2xlLmNvbS9qYXZhc2Uvc3BlY3MvamxzL3NlMTUvaHRtbC9qbHMtMy5odG1sI2pscy0zLjEwXG52YXIgZGVjaW1hbERpZ2l0cyA9ICdbMC05XShfKlswLTldKSonO1xudmFyIGZyYWMgPSBgXFxcXC4oJHtkZWNpbWFsRGlnaXRzfSlgO1xudmFyIGhleERpZ2l0cyA9ICdbMC05YS1mQS1GXShfKlswLTlhLWZBLUZdKSonO1xudmFyIE5VTUVSSUMgPSB7XG4gIGNsYXNzTmFtZTogJ251bWJlcicsXG4gIHZhcmlhbnRzOiBbXG4gICAgLy8gRGVjaW1hbEZsb2F0aW5nUG9pbnRMaXRlcmFsXG4gICAgLy8gaW5jbHVkaW5nIEV4cG9uZW50UGFydFxuICAgIHsgYmVnaW46IGAoXFxcXGIoJHtkZWNpbWFsRGlnaXRzfSkoKCR7ZnJhY30pfFxcXFwuKT98KCR7ZnJhY30pKWAgK1xuICAgICAgYFtlRV1bKy1dPygke2RlY2ltYWxEaWdpdHN9KVtmRmREXT9cXFxcYmAgfSxcbiAgICAvLyBleGNsdWRpbmcgRXhwb25lbnRQYXJ0XG4gICAgeyBiZWdpbjogYFxcXFxiKCR7ZGVjaW1hbERpZ2l0c30pKCgke2ZyYWN9KVtmRmREXT9cXFxcYnxcXFxcLihbZkZkRF1cXFxcYik/KWAgfSxcbiAgICB7IGJlZ2luOiBgKCR7ZnJhY30pW2ZGZERdP1xcXFxiYCB9LFxuICAgIHsgYmVnaW46IGBcXFxcYigke2RlY2ltYWxEaWdpdHN9KVtmRmREXVxcXFxiYCB9LFxuXG4gICAgLy8gSGV4YWRlY2ltYWxGbG9hdGluZ1BvaW50TGl0ZXJhbFxuICAgIHsgYmVnaW46IGBcXFxcYjBbeFhdKCgke2hleERpZ2l0c30pXFxcXC4/fCgke2hleERpZ2l0c30pP1xcXFwuKCR7aGV4RGlnaXRzfSkpYCArXG4gICAgICBgW3BQXVsrLV0/KCR7ZGVjaW1hbERpZ2l0c30pW2ZGZERdP1xcXFxiYCB9LFxuXG4gICAgLy8gRGVjaW1hbEludGVnZXJMaXRlcmFsXG4gICAgeyBiZWdpbjogJ1xcXFxiKDB8WzEtOV0oXypbMC05XSkqKVtsTF0/XFxcXGInIH0sXG5cbiAgICAvLyBIZXhJbnRlZ2VyTGl0ZXJhbFxuICAgIHsgYmVnaW46IGBcXFxcYjBbeFhdKCR7aGV4RGlnaXRzfSlbbExdP1xcXFxiYCB9LFxuXG4gICAgLy8gT2N0YWxJbnRlZ2VyTGl0ZXJhbFxuICAgIHsgYmVnaW46ICdcXFxcYjAoXypbMC03XSkqW2xMXT9cXFxcYicgfSxcblxuICAgIC8vIEJpbmFyeUludGVnZXJMaXRlcmFsXG4gICAgeyBiZWdpbjogJ1xcXFxiMFtiQl1bMDFdKF8qWzAxXSkqW2xMXT9cXFxcYicgfSxcbiAgXSxcbiAgcmVsZXZhbmNlOiAwXG59O1xuXG4vKlxuIExhbmd1YWdlOiBLb3RsaW5cbiBEZXNjcmlwdGlvbjogS290bGluIGlzIGFuIE9TUyBzdGF0aWNhbGx5IHR5cGVkIHByb2dyYW1taW5nIGxhbmd1YWdlIHRoYXQgdGFyZ2V0cyB0aGUgSlZNLCBBbmRyb2lkLCBKYXZhU2NyaXB0IGFuZCBOYXRpdmUuXG4gQXV0aG9yOiBTZXJnZXkgTWFzaGtvdiA8Y3k2ZXJHbjBtQGdtYWlsLmNvbT5cbiBXZWJzaXRlOiBodHRwczovL2tvdGxpbmxhbmcub3JnXG4gQ2F0ZWdvcnk6IGNvbW1vblxuICovXG5cbmZ1bmN0aW9uIGtvdGxpbihobGpzKSB7XG4gIGNvbnN0IEtFWVdPUkRTID0ge1xuICAgIGtleXdvcmQ6XG4gICAgICAnYWJzdHJhY3QgYXMgdmFsIHZhciB2YXJhcmcgZ2V0IHNldCBjbGFzcyBvYmplY3Qgb3BlbiBwcml2YXRlIHByb3RlY3RlZCBwdWJsaWMgbm9pbmxpbmUgJyArXG4gICAgICAnY3Jvc3NpbmxpbmUgZHluYW1pYyBmaW5hbCBlbnVtIGlmIGVsc2UgZG8gd2hpbGUgZm9yIHdoZW4gdGhyb3cgdHJ5IGNhdGNoIGZpbmFsbHkgJyArXG4gICAgICAnaW1wb3J0IHBhY2thZ2UgaXMgaW4gZnVuIG92ZXJyaWRlIGNvbXBhbmlvbiByZWlmaWVkIGlubGluZSBsYXRlaW5pdCBpbml0ICcgK1xuICAgICAgJ2ludGVyZmFjZSBhbm5vdGF0aW9uIGRhdGEgc2VhbGVkIGludGVybmFsIGluZml4IG9wZXJhdG9yIG91dCBieSBjb25zdHJ1Y3RvciBzdXBlciAnICtcbiAgICAgICd0YWlscmVjIHdoZXJlIGNvbnN0IGlubmVyIHN1c3BlbmQgdHlwZWFsaWFzIGV4dGVybmFsIGV4cGVjdCBhY3R1YWwnLFxuICAgIGJ1aWx0X2luOlxuICAgICAgJ0J5dGUgU2hvcnQgQ2hhciBJbnQgTG9uZyBCb29sZWFuIEZsb2F0IERvdWJsZSBWb2lkIFVuaXQgTm90aGluZycsXG4gICAgbGl0ZXJhbDpcbiAgICAgICd0cnVlIGZhbHNlIG51bGwnXG4gIH07XG4gIGNvbnN0IEtFWVdPUkRTX1dJVEhfTEFCRUwgPSB7XG4gICAgY2xhc3NOYW1lOiAna2V5d29yZCcsXG4gICAgYmVnaW46IC9cXGIoYnJlYWt8Y29udGludWV8cmV0dXJufHRoaXMpXFxiLyxcbiAgICBzdGFydHM6IHtcbiAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgIHtcbiAgICAgICAgICBjbGFzc05hbWU6ICdzeW1ib2wnLFxuICAgICAgICAgIGJlZ2luOiAvQFxcdysvXG4gICAgICAgIH1cbiAgICAgIF1cbiAgICB9XG4gIH07XG4gIGNvbnN0IExBQkVMID0ge1xuICAgIGNsYXNzTmFtZTogJ3N5bWJvbCcsXG4gICAgYmVnaW46IGhsanMuVU5ERVJTQ09SRV9JREVOVF9SRSArICdAJ1xuICB9O1xuXG4gIC8vIGZvciBzdHJpbmcgdGVtcGxhdGVzXG4gIGNvbnN0IFNVQlNUID0ge1xuICAgIGNsYXNzTmFtZTogJ3N1YnN0JyxcbiAgICBiZWdpbjogL1xcJFxcey8sXG4gICAgZW5kOiAvXFx9LyxcbiAgICBjb250YWluczogWyBobGpzLkNfTlVNQkVSX01PREUgXVxuICB9O1xuICBjb25zdCBWQVJJQUJMRSA9IHtcbiAgICBjbGFzc05hbWU6ICd2YXJpYWJsZScsXG4gICAgYmVnaW46ICdcXFxcJCcgKyBobGpzLlVOREVSU0NPUkVfSURFTlRfUkVcbiAgfTtcbiAgY29uc3QgU1RSSU5HID0ge1xuICAgIGNsYXNzTmFtZTogJ3N0cmluZycsXG4gICAgdmFyaWFudHM6IFtcbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICdcIlwiXCInLFxuICAgICAgICBlbmQ6ICdcIlwiXCIoPz1bXlwiXSknLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIFZBUklBQkxFLFxuICAgICAgICAgIFNVQlNUXG4gICAgICAgIF1cbiAgICAgIH0sXG4gICAgICAvLyBDYW4ndCB1c2UgYnVpbHQtaW4gbW9kZXMgZWFzaWx5LCBhcyB3ZSB3YW50IHRvIHVzZSBTVFJJTkcgaW4gdGhlIG1ldGFcbiAgICAgIC8vIGNvbnRleHQgYXMgJ21ldGEtc3RyaW5nJyBhbmQgdGhlcmUncyBubyBzeW50YXggdG8gcmVtb3ZlIGV4cGxpY2l0bHkgc2V0XG4gICAgICAvLyBjbGFzc05hbWVzIGluIGJ1aWx0LWluIG1vZGVzLlxuICAgICAge1xuICAgICAgICBiZWdpbjogJ1xcJycsXG4gICAgICAgIGVuZDogJ1xcJycsXG4gICAgICAgIGlsbGVnYWw6IC9cXG4vLFxuICAgICAgICBjb250YWluczogWyBobGpzLkJBQ0tTTEFTSF9FU0NBUEUgXVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICdcIicsXG4gICAgICAgIGVuZDogJ1wiJyxcbiAgICAgICAgaWxsZWdhbDogL1xcbi8sXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgaGxqcy5CQUNLU0xBU0hfRVNDQVBFLFxuICAgICAgICAgIFZBUklBQkxFLFxuICAgICAgICAgIFNVQlNUXG4gICAgICAgIF1cbiAgICAgIH1cbiAgICBdXG4gIH07XG4gIFNVQlNULmNvbnRhaW5zLnB1c2goU1RSSU5HKTtcblxuICBjb25zdCBBTk5PVEFUSU9OX1VTRV9TSVRFID0ge1xuICAgIGNsYXNzTmFtZTogJ21ldGEnLFxuICAgIGJlZ2luOiAnQCg/OmZpbGV8cHJvcGVydHl8ZmllbGR8Z2V0fHNldHxyZWNlaXZlcnxwYXJhbXxzZXRwYXJhbXxkZWxlZ2F0ZSlcXFxccyo6KD86XFxcXHMqJyArIGhsanMuVU5ERVJTQ09SRV9JREVOVF9SRSArICcpPydcbiAgfTtcbiAgY29uc3QgQU5OT1RBVElPTiA9IHtcbiAgICBjbGFzc05hbWU6ICdtZXRhJyxcbiAgICBiZWdpbjogJ0AnICsgaGxqcy5VTkRFUlNDT1JFX0lERU5UX1JFLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAvXFwoLyxcbiAgICAgICAgZW5kOiAvXFwpLyxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICBobGpzLmluaGVyaXQoU1RSSU5HLCB7XG4gICAgICAgICAgICBjbGFzc05hbWU6ICdtZXRhLXN0cmluZydcbiAgICAgICAgICB9KVxuICAgICAgICBdXG4gICAgICB9XG4gICAgXVxuICB9O1xuXG4gIC8vIGh0dHBzOi8va290bGlubGFuZy5vcmcvZG9jcy9yZWZlcmVuY2Uvd2hhdHNuZXcxMS5odG1sI3VuZGVyc2NvcmVzLWluLW51bWVyaWMtbGl0ZXJhbHNcbiAgLy8gQWNjb3JkaW5nIHRvIHRoZSBkb2MgYWJvdmUsIHRoZSBudW1iZXIgbW9kZSBvZiBrb3RsaW4gaXMgdGhlIHNhbWUgYXMgamF2YSA4LFxuICAvLyBzbyB0aGUgY29kZSBiZWxvdyBpcyBjb3BpZWQgZnJvbSBqYXZhLmpzXG4gIGNvbnN0IEtPVExJTl9OVU1CRVJfTU9ERSA9IE5VTUVSSUM7XG4gIGNvbnN0IEtPVExJTl9ORVNURURfQ09NTUVOVCA9IGhsanMuQ09NTUVOVChcbiAgICAnL1xcXFwqJywgJ1xcXFwqLycsXG4gICAge1xuICAgICAgY29udGFpbnM6IFsgaGxqcy5DX0JMT0NLX0NPTU1FTlRfTU9ERSBdXG4gICAgfVxuICApO1xuICBjb25zdCBLT1RMSU5fUEFSRU5fVFlQRSA9IHtcbiAgICB2YXJpYW50czogW1xuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICd0eXBlJyxcbiAgICAgICAgYmVnaW46IGhsanMuVU5ERVJTQ09SRV9JREVOVF9SRVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC9cXCgvLFxuICAgICAgICBlbmQ6IC9cXCkvLFxuICAgICAgICBjb250YWluczogW10gLy8gZGVmaW5lZCBsYXRlclxuICAgICAgfVxuICAgIF1cbiAgfTtcbiAgY29uc3QgS09UTElOX1BBUkVOX1RZUEUyID0gS09UTElOX1BBUkVOX1RZUEU7XG4gIEtPVExJTl9QQVJFTl9UWVBFMi52YXJpYW50c1sxXS5jb250YWlucyA9IFsgS09UTElOX1BBUkVOX1RZUEUgXTtcbiAgS09UTElOX1BBUkVOX1RZUEUudmFyaWFudHNbMV0uY29udGFpbnMgPSBbIEtPVExJTl9QQVJFTl9UWVBFMiBdO1xuXG4gIHJldHVybiB7XG4gICAgbmFtZTogJ0tvdGxpbicsXG4gICAgYWxpYXNlczogWyAna3QnLCAna3RzJyBdLFxuICAgIGtleXdvcmRzOiBLRVlXT1JEUyxcbiAgICBjb250YWluczogW1xuICAgICAgaGxqcy5DT01NRU5UKFxuICAgICAgICAnL1xcXFwqXFxcXConLFxuICAgICAgICAnXFxcXCovJyxcbiAgICAgICAge1xuICAgICAgICAgIHJlbGV2YW5jZTogMCxcbiAgICAgICAgICBjb250YWluczogW1xuICAgICAgICAgICAge1xuICAgICAgICAgICAgICBjbGFzc05hbWU6ICdkb2N0YWcnLFxuICAgICAgICAgICAgICBiZWdpbjogJ0BbQS1aYS16XSsnXG4gICAgICAgICAgICB9XG4gICAgICAgICAgXVxuICAgICAgICB9XG4gICAgICApLFxuICAgICAgaGxqcy5DX0xJTkVfQ09NTUVOVF9NT0RFLFxuICAgICAgS09UTElOX05FU1RFRF9DT01NRU5ULFxuICAgICAgS0VZV09SRFNfV0lUSF9MQUJFTCxcbiAgICAgIExBQkVMLFxuICAgICAgQU5OT1RBVElPTl9VU0VfU0lURSxcbiAgICAgIEFOTk9UQVRJT04sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ2Z1bmN0aW9uJyxcbiAgICAgICAgYmVnaW5LZXl3b3JkczogJ2Z1bicsXG4gICAgICAgIGVuZDogJ1soXXwkJyxcbiAgICAgICAgcmV0dXJuQmVnaW46IHRydWUsXG4gICAgICAgIGV4Y2x1ZGVFbmQ6IHRydWUsXG4gICAgICAgIGtleXdvcmRzOiBLRVlXT1JEUyxcbiAgICAgICAgcmVsZXZhbmNlOiA1LFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiBobGpzLlVOREVSU0NPUkVfSURFTlRfUkUgKyAnXFxcXHMqXFxcXCgnLFxuICAgICAgICAgICAgcmV0dXJuQmVnaW46IHRydWUsXG4gICAgICAgICAgICByZWxldmFuY2U6IDAsXG4gICAgICAgICAgICBjb250YWluczogWyBobGpzLlVOREVSU0NPUkVfVElUTEVfTU9ERSBdXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICBjbGFzc05hbWU6ICd0eXBlJyxcbiAgICAgICAgICAgIGJlZ2luOiAvPC8sXG4gICAgICAgICAgICBlbmQ6IC8+LyxcbiAgICAgICAgICAgIGtleXdvcmRzOiAncmVpZmllZCcsXG4gICAgICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGNsYXNzTmFtZTogJ3BhcmFtcycsXG4gICAgICAgICAgICBiZWdpbjogL1xcKC8sXG4gICAgICAgICAgICBlbmQ6IC9cXCkvLFxuICAgICAgICAgICAgZW5kc1BhcmVudDogdHJ1ZSxcbiAgICAgICAgICAgIGtleXdvcmRzOiBLRVlXT1JEUyxcbiAgICAgICAgICAgIHJlbGV2YW5jZTogMCxcbiAgICAgICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgICBiZWdpbjogLzovLFxuICAgICAgICAgICAgICAgIGVuZDogL1s9LFxcL10vLFxuICAgICAgICAgICAgICAgIGVuZHNXaXRoUGFyZW50OiB0cnVlLFxuICAgICAgICAgICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgICAgICAgICBLT1RMSU5fUEFSRU5fVFlQRSxcbiAgICAgICAgICAgICAgICAgIGhsanMuQ19MSU5FX0NPTU1FTlRfTU9ERSxcbiAgICAgICAgICAgICAgICAgIEtPVExJTl9ORVNURURfQ09NTUVOVFxuICAgICAgICAgICAgICAgIF0sXG4gICAgICAgICAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICAgICAgICAgIH0sXG4gICAgICAgICAgICAgIGhsanMuQ19MSU5FX0NPTU1FTlRfTU9ERSxcbiAgICAgICAgICAgICAgS09UTElOX05FU1RFRF9DT01NRU5ULFxuICAgICAgICAgICAgICBBTk5PVEFUSU9OX1VTRV9TSVRFLFxuICAgICAgICAgICAgICBBTk5PVEFUSU9OLFxuICAgICAgICAgICAgICBTVFJJTkcsXG4gICAgICAgICAgICAgIGhsanMuQ19OVU1CRVJfTU9ERVxuICAgICAgICAgICAgXVxuICAgICAgICAgIH0sXG4gICAgICAgICAgS09UTElOX05FU1RFRF9DT01NRU5UXG4gICAgICAgIF1cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ2NsYXNzJyxcbiAgICAgICAgYmVnaW5LZXl3b3JkczogJ2NsYXNzIGludGVyZmFjZSB0cmFpdCcsIC8vIHJlbW92ZSAndHJhaXQnIHdoZW4gcmVtb3ZlZCBmcm9tIEtFWVdPUkRTXG4gICAgICAgIGVuZDogL1s6XFx7KF18JC8sXG4gICAgICAgIGV4Y2x1ZGVFbmQ6IHRydWUsXG4gICAgICAgIGlsbGVnYWw6ICdleHRlbmRzIGltcGxlbWVudHMnLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luS2V5d29yZHM6ICdwdWJsaWMgcHJvdGVjdGVkIGludGVybmFsIHByaXZhdGUgY29uc3RydWN0b3InXG4gICAgICAgICAgfSxcbiAgICAgICAgICBobGpzLlVOREVSU0NPUkVfVElUTEVfTU9ERSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICBjbGFzc05hbWU6ICd0eXBlJyxcbiAgICAgICAgICAgIGJlZ2luOiAvPC8sXG4gICAgICAgICAgICBlbmQ6IC8+LyxcbiAgICAgICAgICAgIGV4Y2x1ZGVCZWdpbjogdHJ1ZSxcbiAgICAgICAgICAgIGV4Y2x1ZGVFbmQ6IHRydWUsXG4gICAgICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGNsYXNzTmFtZTogJ3R5cGUnLFxuICAgICAgICAgICAgYmVnaW46IC9bLDpdXFxzKi8sXG4gICAgICAgICAgICBlbmQ6IC9bPFxcKCxdfCQvLFxuICAgICAgICAgICAgZXhjbHVkZUJlZ2luOiB0cnVlLFxuICAgICAgICAgICAgcmV0dXJuRW5kOiB0cnVlXG4gICAgICAgICAgfSxcbiAgICAgICAgICBBTk5PVEFUSU9OX1VTRV9TSVRFLFxuICAgICAgICAgIEFOTk9UQVRJT05cbiAgICAgICAgXVxuICAgICAgfSxcbiAgICAgIFNUUklORyxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnbWV0YScsXG4gICAgICAgIGJlZ2luOiBcIl4jIS91c3IvYmluL2VudlwiLFxuICAgICAgICBlbmQ6ICckJyxcbiAgICAgICAgaWxsZWdhbDogJ1xcbidcbiAgICAgIH0sXG4gICAgICBLT1RMSU5fTlVNQkVSX01PREVcbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0ga290bGluO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9