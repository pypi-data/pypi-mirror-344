(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_livescript"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/livescript.js":
/*!*****************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/livescript.js ***!
  \*****************************************************************************************************/
/***/ ((module) => {

const KEYWORDS = [
  "as", // for exports
  "in",
  "of",
  "if",
  "for",
  "while",
  "finally",
  "var",
  "new",
  "function",
  "do",
  "return",
  "void",
  "else",
  "break",
  "catch",
  "instanceof",
  "with",
  "throw",
  "case",
  "default",
  "try",
  "switch",
  "continue",
  "typeof",
  "delete",
  "let",
  "yield",
  "const",
  "class",
  // JS handles these with a special rule
  // "get",
  // "set",
  "debugger",
  "async",
  "await",
  "static",
  "import",
  "from",
  "export",
  "extends"
];
const LITERALS = [
  "true",
  "false",
  "null",
  "undefined",
  "NaN",
  "Infinity"
];

const TYPES = [
  "Intl",
  "DataView",
  "Number",
  "Math",
  "Date",
  "String",
  "RegExp",
  "Object",
  "Function",
  "Boolean",
  "Error",
  "Symbol",
  "Set",
  "Map",
  "WeakSet",
  "WeakMap",
  "Proxy",
  "Reflect",
  "JSON",
  "Promise",
  "Float64Array",
  "Int16Array",
  "Int32Array",
  "Int8Array",
  "Uint16Array",
  "Uint32Array",
  "Float32Array",
  "Array",
  "Uint8Array",
  "Uint8ClampedArray",
  "ArrayBuffer",
  "BigInt64Array",
  "BigUint64Array",
  "BigInt"
];

const ERROR_TYPES = [
  "EvalError",
  "InternalError",
  "RangeError",
  "ReferenceError",
  "SyntaxError",
  "TypeError",
  "URIError"
];

const BUILT_IN_GLOBALS = [
  "setInterval",
  "setTimeout",
  "clearInterval",
  "clearTimeout",

  "require",
  "exports",

  "eval",
  "isFinite",
  "isNaN",
  "parseFloat",
  "parseInt",
  "decodeURI",
  "decodeURIComponent",
  "encodeURI",
  "encodeURIComponent",
  "escape",
  "unescape"
];

const BUILT_IN_VARIABLES = [
  "arguments",
  "this",
  "super",
  "console",
  "window",
  "document",
  "localStorage",
  "module",
  "global" // Node.js
];

const BUILT_INS = [].concat(
  BUILT_IN_GLOBALS,
  BUILT_IN_VARIABLES,
  TYPES,
  ERROR_TYPES
);

/*
Language: LiveScript
Author: Taneli Vatanen <taneli.vatanen@gmail.com>
Contributors: Jen Evers-Corvina <jen@sevvie.net>
Origin: coffeescript.js
Description: LiveScript is a programming language that transcompiles to JavaScript. For info about language see http://livescript.net/
Website: https://livescript.net
Category: scripting
*/

function livescript(hljs) {
  const LIVESCRIPT_BUILT_INS = [
    'npm',
    'print'
  ];
  const LIVESCRIPT_LITERALS = [
    'yes',
    'no',
    'on',
    'off',
    'it',
    'that',
    'void'
  ];
  const LIVESCRIPT_KEYWORDS = [
    'then',
    'unless',
    'until',
    'loop',
    'of',
    'by',
    'when',
    'and',
    'or',
    'is',
    'isnt',
    'not',
    'it',
    'that',
    'otherwise',
    'from',
    'to',
    'til',
    'fallthrough',
    'case',
    'enum',
    'native',
    'list',
    'map',
    '__hasProp',
    '__extends',
    '__slice',
    '__bind',
    '__indexOf'
  ];
  const KEYWORDS$1 = {
    keyword: KEYWORDS.concat(LIVESCRIPT_KEYWORDS),
    literal: LITERALS.concat(LIVESCRIPT_LITERALS),
    built_in: BUILT_INS.concat(LIVESCRIPT_BUILT_INS)
  };
  const JS_IDENT_RE = '[A-Za-z$_](?:-[0-9A-Za-z$_]|[0-9A-Za-z$_])*';
  const TITLE = hljs.inherit(hljs.TITLE_MODE, {
    begin: JS_IDENT_RE
  });
  const SUBST = {
    className: 'subst',
    begin: /#\{/,
    end: /\}/,
    keywords: KEYWORDS$1
  };
  const SUBST_SIMPLE = {
    className: 'subst',
    begin: /#[A-Za-z$_]/,
    end: /(?:-[0-9A-Za-z$_]|[0-9A-Za-z$_])*/,
    keywords: KEYWORDS$1
  };
  const EXPRESSIONS = [
    hljs.BINARY_NUMBER_MODE,
    {
      className: 'number',
      begin: '(\\b0[xX][a-fA-F0-9_]+)|(\\b\\d(\\d|_\\d)*(\\.(\\d(\\d|_\\d)*)?)?(_*[eE]([-+]\\d(_\\d|\\d)*)?)?[_a-z]*)',
      relevance: 0,
      starts: {
        end: '(\\s*/)?',
        relevance: 0
      } // a number tries to eat the following slash to prevent treating it as a regexp
    },
    {
      className: 'string',
      variants: [
        {
          begin: /'''/,
          end: /'''/,
          contains: [hljs.BACKSLASH_ESCAPE]
        },
        {
          begin: /'/,
          end: /'/,
          contains: [hljs.BACKSLASH_ESCAPE]
        },
        {
          begin: /"""/,
          end: /"""/,
          contains: [
            hljs.BACKSLASH_ESCAPE,
            SUBST,
            SUBST_SIMPLE
          ]
        },
        {
          begin: /"/,
          end: /"/,
          contains: [
            hljs.BACKSLASH_ESCAPE,
            SUBST,
            SUBST_SIMPLE
          ]
        },
        {
          begin: /\\/,
          end: /(\s|$)/,
          excludeEnd: true
        }
      ]
    },
    {
      className: 'regexp',
      variants: [
        {
          begin: '//',
          end: '//[gim]*',
          contains: [
            SUBST,
            hljs.HASH_COMMENT_MODE
          ]
        },
        {
          // regex can't start with space to parse x / 2 / 3 as two divisions
          // regex can't start with *, and it supports an "illegal" in the main mode
          begin: /\/(?![ *])(\\.|[^\\\n])*?\/[gim]*(?=\W)/
        }
      ]
    },
    {
      begin: '@' + JS_IDENT_RE
    },
    {
      begin: '``',
      end: '``',
      excludeBegin: true,
      excludeEnd: true,
      subLanguage: 'javascript'
    }
  ];
  SUBST.contains = EXPRESSIONS;

  const PARAMS = {
    className: 'params',
    begin: '\\(',
    returnBegin: true,
    /* We need another contained nameless mode to not have every nested
    pair of parens to be called "params" */
    contains: [
      {
        begin: /\(/,
        end: /\)/,
        keywords: KEYWORDS$1,
        contains: ['self'].concat(EXPRESSIONS)
      }
    ]
  };

  const SYMBOLS = {
    begin: '(#=>|=>|\\|>>|-?->|!->)'
  };

  return {
    name: 'LiveScript',
    aliases: ['ls'],
    keywords: KEYWORDS$1,
    illegal: /\/\*/,
    contains: EXPRESSIONS.concat([
      hljs.COMMENT('\\/\\*', '\\*\\/'),
      hljs.HASH_COMMENT_MODE,
      SYMBOLS, // relevance booster
      {
        className: 'function',
        contains: [
          TITLE,
          PARAMS
        ],
        returnBegin: true,
        variants: [
          {
            begin: '(' + JS_IDENT_RE + '\\s*(?:=|:=)\\s*)?(\\(.*\\)\\s*)?\\B->\\*?',
            end: '->\\*?'
          },
          {
            begin: '(' + JS_IDENT_RE + '\\s*(?:=|:=)\\s*)?!?(\\(.*\\)\\s*)?\\B[-~]{1,2}>\\*?',
            end: '[-~]{1,2}>\\*?'
          },
          {
            begin: '(' + JS_IDENT_RE + '\\s*(?:=|:=)\\s*)?(\\(.*\\)\\s*)?\\B!?[-~]{1,2}>\\*?',
            end: '!?[-~]{1,2}>\\*?'
          }
        ]
      },
      {
        className: 'class',
        beginKeywords: 'class',
        end: '$',
        illegal: /[:="\[\]]/,
        contains: [
          {
            beginKeywords: 'extends',
            endsWithParent: true,
            illegal: /[:="\[\]]/,
            contains: [TITLE]
          },
          TITLE
        ]
      },
      {
        begin: JS_IDENT_RE + ':',
        end: ':',
        returnBegin: true,
        returnEnd: true,
        relevance: 0
      }
    ])
  };
}

module.exports = livescript;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfbGl2ZXNjcmlwdC5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsR0FBRztBQUNIO0FBQ0E7QUFDQSxlQUFlO0FBQ2YsWUFBWTtBQUNaO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxRQUFRO0FBQ1IsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsU0FBUztBQUNUO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsU0FBUztBQUNUO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxTQUFTO0FBQ1Q7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFNBQVM7QUFDVDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxTQUFTO0FBQ1Q7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFdBQVc7QUFDWDtBQUNBLG1GQUFtRixJQUFJO0FBQ3ZGLHVCQUF1QixJQUFJO0FBQzNCLFdBQVc7QUFDWDtBQUNBLG1GQUFtRixJQUFJO0FBQ3ZGLHlCQUF5QixJQUFJO0FBQzdCO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFdBQVc7QUFDWDtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9saXZlc2NyaXB0LmpzIl0sInNvdXJjZXNDb250ZW50IjpbImNvbnN0IEtFWVdPUkRTID0gW1xuICBcImFzXCIsIC8vIGZvciBleHBvcnRzXG4gIFwiaW5cIixcbiAgXCJvZlwiLFxuICBcImlmXCIsXG4gIFwiZm9yXCIsXG4gIFwid2hpbGVcIixcbiAgXCJmaW5hbGx5XCIsXG4gIFwidmFyXCIsXG4gIFwibmV3XCIsXG4gIFwiZnVuY3Rpb25cIixcbiAgXCJkb1wiLFxuICBcInJldHVyblwiLFxuICBcInZvaWRcIixcbiAgXCJlbHNlXCIsXG4gIFwiYnJlYWtcIixcbiAgXCJjYXRjaFwiLFxuICBcImluc3RhbmNlb2ZcIixcbiAgXCJ3aXRoXCIsXG4gIFwidGhyb3dcIixcbiAgXCJjYXNlXCIsXG4gIFwiZGVmYXVsdFwiLFxuICBcInRyeVwiLFxuICBcInN3aXRjaFwiLFxuICBcImNvbnRpbnVlXCIsXG4gIFwidHlwZW9mXCIsXG4gIFwiZGVsZXRlXCIsXG4gIFwibGV0XCIsXG4gIFwieWllbGRcIixcbiAgXCJjb25zdFwiLFxuICBcImNsYXNzXCIsXG4gIC8vIEpTIGhhbmRsZXMgdGhlc2Ugd2l0aCBhIHNwZWNpYWwgcnVsZVxuICAvLyBcImdldFwiLFxuICAvLyBcInNldFwiLFxuICBcImRlYnVnZ2VyXCIsXG4gIFwiYXN5bmNcIixcbiAgXCJhd2FpdFwiLFxuICBcInN0YXRpY1wiLFxuICBcImltcG9ydFwiLFxuICBcImZyb21cIixcbiAgXCJleHBvcnRcIixcbiAgXCJleHRlbmRzXCJcbl07XG5jb25zdCBMSVRFUkFMUyA9IFtcbiAgXCJ0cnVlXCIsXG4gIFwiZmFsc2VcIixcbiAgXCJudWxsXCIsXG4gIFwidW5kZWZpbmVkXCIsXG4gIFwiTmFOXCIsXG4gIFwiSW5maW5pdHlcIlxuXTtcblxuY29uc3QgVFlQRVMgPSBbXG4gIFwiSW50bFwiLFxuICBcIkRhdGFWaWV3XCIsXG4gIFwiTnVtYmVyXCIsXG4gIFwiTWF0aFwiLFxuICBcIkRhdGVcIixcbiAgXCJTdHJpbmdcIixcbiAgXCJSZWdFeHBcIixcbiAgXCJPYmplY3RcIixcbiAgXCJGdW5jdGlvblwiLFxuICBcIkJvb2xlYW5cIixcbiAgXCJFcnJvclwiLFxuICBcIlN5bWJvbFwiLFxuICBcIlNldFwiLFxuICBcIk1hcFwiLFxuICBcIldlYWtTZXRcIixcbiAgXCJXZWFrTWFwXCIsXG4gIFwiUHJveHlcIixcbiAgXCJSZWZsZWN0XCIsXG4gIFwiSlNPTlwiLFxuICBcIlByb21pc2VcIixcbiAgXCJGbG9hdDY0QXJyYXlcIixcbiAgXCJJbnQxNkFycmF5XCIsXG4gIFwiSW50MzJBcnJheVwiLFxuICBcIkludDhBcnJheVwiLFxuICBcIlVpbnQxNkFycmF5XCIsXG4gIFwiVWludDMyQXJyYXlcIixcbiAgXCJGbG9hdDMyQXJyYXlcIixcbiAgXCJBcnJheVwiLFxuICBcIlVpbnQ4QXJyYXlcIixcbiAgXCJVaW50OENsYW1wZWRBcnJheVwiLFxuICBcIkFycmF5QnVmZmVyXCIsXG4gIFwiQmlnSW50NjRBcnJheVwiLFxuICBcIkJpZ1VpbnQ2NEFycmF5XCIsXG4gIFwiQmlnSW50XCJcbl07XG5cbmNvbnN0IEVSUk9SX1RZUEVTID0gW1xuICBcIkV2YWxFcnJvclwiLFxuICBcIkludGVybmFsRXJyb3JcIixcbiAgXCJSYW5nZUVycm9yXCIsXG4gIFwiUmVmZXJlbmNlRXJyb3JcIixcbiAgXCJTeW50YXhFcnJvclwiLFxuICBcIlR5cGVFcnJvclwiLFxuICBcIlVSSUVycm9yXCJcbl07XG5cbmNvbnN0IEJVSUxUX0lOX0dMT0JBTFMgPSBbXG4gIFwic2V0SW50ZXJ2YWxcIixcbiAgXCJzZXRUaW1lb3V0XCIsXG4gIFwiY2xlYXJJbnRlcnZhbFwiLFxuICBcImNsZWFyVGltZW91dFwiLFxuXG4gIFwicmVxdWlyZVwiLFxuICBcImV4cG9ydHNcIixcblxuICBcImV2YWxcIixcbiAgXCJpc0Zpbml0ZVwiLFxuICBcImlzTmFOXCIsXG4gIFwicGFyc2VGbG9hdFwiLFxuICBcInBhcnNlSW50XCIsXG4gIFwiZGVjb2RlVVJJXCIsXG4gIFwiZGVjb2RlVVJJQ29tcG9uZW50XCIsXG4gIFwiZW5jb2RlVVJJXCIsXG4gIFwiZW5jb2RlVVJJQ29tcG9uZW50XCIsXG4gIFwiZXNjYXBlXCIsXG4gIFwidW5lc2NhcGVcIlxuXTtcblxuY29uc3QgQlVJTFRfSU5fVkFSSUFCTEVTID0gW1xuICBcImFyZ3VtZW50c1wiLFxuICBcInRoaXNcIixcbiAgXCJzdXBlclwiLFxuICBcImNvbnNvbGVcIixcbiAgXCJ3aW5kb3dcIixcbiAgXCJkb2N1bWVudFwiLFxuICBcImxvY2FsU3RvcmFnZVwiLFxuICBcIm1vZHVsZVwiLFxuICBcImdsb2JhbFwiIC8vIE5vZGUuanNcbl07XG5cbmNvbnN0IEJVSUxUX0lOUyA9IFtdLmNvbmNhdChcbiAgQlVJTFRfSU5fR0xPQkFMUyxcbiAgQlVJTFRfSU5fVkFSSUFCTEVTLFxuICBUWVBFUyxcbiAgRVJST1JfVFlQRVNcbik7XG5cbi8qXG5MYW5ndWFnZTogTGl2ZVNjcmlwdFxuQXV0aG9yOiBUYW5lbGkgVmF0YW5lbiA8dGFuZWxpLnZhdGFuZW5AZ21haWwuY29tPlxuQ29udHJpYnV0b3JzOiBKZW4gRXZlcnMtQ29ydmluYSA8amVuQHNldnZpZS5uZXQ+XG5PcmlnaW46IGNvZmZlZXNjcmlwdC5qc1xuRGVzY3JpcHRpb246IExpdmVTY3JpcHQgaXMgYSBwcm9ncmFtbWluZyBsYW5ndWFnZSB0aGF0IHRyYW5zY29tcGlsZXMgdG8gSmF2YVNjcmlwdC4gRm9yIGluZm8gYWJvdXQgbGFuZ3VhZ2Ugc2VlIGh0dHA6Ly9saXZlc2NyaXB0Lm5ldC9cbldlYnNpdGU6IGh0dHBzOi8vbGl2ZXNjcmlwdC5uZXRcbkNhdGVnb3J5OiBzY3JpcHRpbmdcbiovXG5cbmZ1bmN0aW9uIGxpdmVzY3JpcHQoaGxqcykge1xuICBjb25zdCBMSVZFU0NSSVBUX0JVSUxUX0lOUyA9IFtcbiAgICAnbnBtJyxcbiAgICAncHJpbnQnXG4gIF07XG4gIGNvbnN0IExJVkVTQ1JJUFRfTElURVJBTFMgPSBbXG4gICAgJ3llcycsXG4gICAgJ25vJyxcbiAgICAnb24nLFxuICAgICdvZmYnLFxuICAgICdpdCcsXG4gICAgJ3RoYXQnLFxuICAgICd2b2lkJ1xuICBdO1xuICBjb25zdCBMSVZFU0NSSVBUX0tFWVdPUkRTID0gW1xuICAgICd0aGVuJyxcbiAgICAndW5sZXNzJyxcbiAgICAndW50aWwnLFxuICAgICdsb29wJyxcbiAgICAnb2YnLFxuICAgICdieScsXG4gICAgJ3doZW4nLFxuICAgICdhbmQnLFxuICAgICdvcicsXG4gICAgJ2lzJyxcbiAgICAnaXNudCcsXG4gICAgJ25vdCcsXG4gICAgJ2l0JyxcbiAgICAndGhhdCcsXG4gICAgJ290aGVyd2lzZScsXG4gICAgJ2Zyb20nLFxuICAgICd0bycsXG4gICAgJ3RpbCcsXG4gICAgJ2ZhbGx0aHJvdWdoJyxcbiAgICAnY2FzZScsXG4gICAgJ2VudW0nLFxuICAgICduYXRpdmUnLFxuICAgICdsaXN0JyxcbiAgICAnbWFwJyxcbiAgICAnX19oYXNQcm9wJyxcbiAgICAnX19leHRlbmRzJyxcbiAgICAnX19zbGljZScsXG4gICAgJ19fYmluZCcsXG4gICAgJ19faW5kZXhPZidcbiAgXTtcbiAgY29uc3QgS0VZV09SRFMkMSA9IHtcbiAgICBrZXl3b3JkOiBLRVlXT1JEUy5jb25jYXQoTElWRVNDUklQVF9LRVlXT1JEUyksXG4gICAgbGl0ZXJhbDogTElURVJBTFMuY29uY2F0KExJVkVTQ1JJUFRfTElURVJBTFMpLFxuICAgIGJ1aWx0X2luOiBCVUlMVF9JTlMuY29uY2F0KExJVkVTQ1JJUFRfQlVJTFRfSU5TKVxuICB9O1xuICBjb25zdCBKU19JREVOVF9SRSA9ICdbQS1aYS16JF9dKD86LVswLTlBLVphLXokX118WzAtOUEtWmEteiRfXSkqJztcbiAgY29uc3QgVElUTEUgPSBobGpzLmluaGVyaXQoaGxqcy5USVRMRV9NT0RFLCB7XG4gICAgYmVnaW46IEpTX0lERU5UX1JFXG4gIH0pO1xuICBjb25zdCBTVUJTVCA9IHtcbiAgICBjbGFzc05hbWU6ICdzdWJzdCcsXG4gICAgYmVnaW46IC8jXFx7LyxcbiAgICBlbmQ6IC9cXH0vLFxuICAgIGtleXdvcmRzOiBLRVlXT1JEUyQxXG4gIH07XG4gIGNvbnN0IFNVQlNUX1NJTVBMRSA9IHtcbiAgICBjbGFzc05hbWU6ICdzdWJzdCcsXG4gICAgYmVnaW46IC8jW0EtWmEteiRfXS8sXG4gICAgZW5kOiAvKD86LVswLTlBLVphLXokX118WzAtOUEtWmEteiRfXSkqLyxcbiAgICBrZXl3b3JkczogS0VZV09SRFMkMVxuICB9O1xuICBjb25zdCBFWFBSRVNTSU9OUyA9IFtcbiAgICBobGpzLkJJTkFSWV9OVU1CRVJfTU9ERSxcbiAgICB7XG4gICAgICBjbGFzc05hbWU6ICdudW1iZXInLFxuICAgICAgYmVnaW46ICcoXFxcXGIwW3hYXVthLWZBLUYwLTlfXSspfChcXFxcYlxcXFxkKFxcXFxkfF9cXFxcZCkqKFxcXFwuKFxcXFxkKFxcXFxkfF9cXFxcZCkqKT8pPyhfKltlRV0oWy0rXVxcXFxkKF9cXFxcZHxcXFxcZCkqKT8pP1tfYS16XSopJyxcbiAgICAgIHJlbGV2YW5jZTogMCxcbiAgICAgIHN0YXJ0czoge1xuICAgICAgICBlbmQ6ICcoXFxcXHMqLyk/JyxcbiAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICB9IC8vIGEgbnVtYmVyIHRyaWVzIHRvIGVhdCB0aGUgZm9sbG93aW5nIHNsYXNoIHRvIHByZXZlbnQgdHJlYXRpbmcgaXQgYXMgYSByZWdleHBcbiAgICB9LFxuICAgIHtcbiAgICAgIGNsYXNzTmFtZTogJ3N0cmluZycsXG4gICAgICB2YXJpYW50czogW1xuICAgICAgICB7XG4gICAgICAgICAgYmVnaW46IC8nJycvLFxuICAgICAgICAgIGVuZDogLycnJy8sXG4gICAgICAgICAgY29udGFpbnM6IFtobGpzLkJBQ0tTTEFTSF9FU0NBUEVdXG4gICAgICAgIH0sXG4gICAgICAgIHtcbiAgICAgICAgICBiZWdpbjogLycvLFxuICAgICAgICAgIGVuZDogLycvLFxuICAgICAgICAgIGNvbnRhaW5zOiBbaGxqcy5CQUNLU0xBU0hfRVNDQVBFXVxuICAgICAgICB9LFxuICAgICAgICB7XG4gICAgICAgICAgYmVnaW46IC9cIlwiXCIvLFxuICAgICAgICAgIGVuZDogL1wiXCJcIi8sXG4gICAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICAgIGhsanMuQkFDS1NMQVNIX0VTQ0FQRSxcbiAgICAgICAgICAgIFNVQlNULFxuICAgICAgICAgICAgU1VCU1RfU0lNUExFXG4gICAgICAgICAgXVxuICAgICAgICB9LFxuICAgICAgICB7XG4gICAgICAgICAgYmVnaW46IC9cIi8sXG4gICAgICAgICAgZW5kOiAvXCIvLFxuICAgICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgICBobGpzLkJBQ0tTTEFTSF9FU0NBUEUsXG4gICAgICAgICAgICBTVUJTVCxcbiAgICAgICAgICAgIFNVQlNUX1NJTVBMRVxuICAgICAgICAgIF1cbiAgICAgICAgfSxcbiAgICAgICAge1xuICAgICAgICAgIGJlZ2luOiAvXFxcXC8sXG4gICAgICAgICAgZW5kOiAvKFxcc3wkKS8sXG4gICAgICAgICAgZXhjbHVkZUVuZDogdHJ1ZVxuICAgICAgICB9XG4gICAgICBdXG4gICAgfSxcbiAgICB7XG4gICAgICBjbGFzc05hbWU6ICdyZWdleHAnLFxuICAgICAgdmFyaWFudHM6IFtcbiAgICAgICAge1xuICAgICAgICAgIGJlZ2luOiAnLy8nLFxuICAgICAgICAgIGVuZDogJy8vW2dpbV0qJyxcbiAgICAgICAgICBjb250YWluczogW1xuICAgICAgICAgICAgU1VCU1QsXG4gICAgICAgICAgICBobGpzLkhBU0hfQ09NTUVOVF9NT0RFXG4gICAgICAgICAgXVxuICAgICAgICB9LFxuICAgICAgICB7XG4gICAgICAgICAgLy8gcmVnZXggY2FuJ3Qgc3RhcnQgd2l0aCBzcGFjZSB0byBwYXJzZSB4IC8gMiAvIDMgYXMgdHdvIGRpdmlzaW9uc1xuICAgICAgICAgIC8vIHJlZ2V4IGNhbid0IHN0YXJ0IHdpdGggKiwgYW5kIGl0IHN1cHBvcnRzIGFuIFwiaWxsZWdhbFwiIGluIHRoZSBtYWluIG1vZGVcbiAgICAgICAgICBiZWdpbjogL1xcLyg/IVsgKl0pKFxcXFwufFteXFxcXFxcbl0pKj9cXC9bZ2ltXSooPz1cXFcpL1xuICAgICAgICB9XG4gICAgICBdXG4gICAgfSxcbiAgICB7XG4gICAgICBiZWdpbjogJ0AnICsgSlNfSURFTlRfUkVcbiAgICB9LFxuICAgIHtcbiAgICAgIGJlZ2luOiAnYGAnLFxuICAgICAgZW5kOiAnYGAnLFxuICAgICAgZXhjbHVkZUJlZ2luOiB0cnVlLFxuICAgICAgZXhjbHVkZUVuZDogdHJ1ZSxcbiAgICAgIHN1Ykxhbmd1YWdlOiAnamF2YXNjcmlwdCdcbiAgICB9XG4gIF07XG4gIFNVQlNULmNvbnRhaW5zID0gRVhQUkVTU0lPTlM7XG5cbiAgY29uc3QgUEFSQU1TID0ge1xuICAgIGNsYXNzTmFtZTogJ3BhcmFtcycsXG4gICAgYmVnaW46ICdcXFxcKCcsXG4gICAgcmV0dXJuQmVnaW46IHRydWUsXG4gICAgLyogV2UgbmVlZCBhbm90aGVyIGNvbnRhaW5lZCBuYW1lbGVzcyBtb2RlIHRvIG5vdCBoYXZlIGV2ZXJ5IG5lc3RlZFxuICAgIHBhaXIgb2YgcGFyZW5zIHRvIGJlIGNhbGxlZCBcInBhcmFtc1wiICovXG4gICAgY29udGFpbnM6IFtcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC9cXCgvLFxuICAgICAgICBlbmQ6IC9cXCkvLFxuICAgICAgICBrZXl3b3JkczogS0VZV09SRFMkMSxcbiAgICAgICAgY29udGFpbnM6IFsnc2VsZiddLmNvbmNhdChFWFBSRVNTSU9OUylcbiAgICAgIH1cbiAgICBdXG4gIH07XG5cbiAgY29uc3QgU1lNQk9MUyA9IHtcbiAgICBiZWdpbjogJygjPT58PT58XFxcXHw+PnwtPy0+fCEtPiknXG4gIH07XG5cbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnTGl2ZVNjcmlwdCcsXG4gICAgYWxpYXNlczogWydscyddLFxuICAgIGtleXdvcmRzOiBLRVlXT1JEUyQxLFxuICAgIGlsbGVnYWw6IC9cXC9cXCovLFxuICAgIGNvbnRhaW5zOiBFWFBSRVNTSU9OUy5jb25jYXQoW1xuICAgICAgaGxqcy5DT01NRU5UKCdcXFxcL1xcXFwqJywgJ1xcXFwqXFxcXC8nKSxcbiAgICAgIGhsanMuSEFTSF9DT01NRU5UX01PREUsXG4gICAgICBTWU1CT0xTLCAvLyByZWxldmFuY2UgYm9vc3RlclxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdmdW5jdGlvbicsXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgVElUTEUsXG4gICAgICAgICAgUEFSQU1TXG4gICAgICAgIF0sXG4gICAgICAgIHJldHVybkJlZ2luOiB0cnVlLFxuICAgICAgICB2YXJpYW50czogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiAnKCcgKyBKU19JREVOVF9SRSArICdcXFxccyooPzo9fDo9KVxcXFxzKik/KFxcXFwoLipcXFxcKVxcXFxzKik/XFxcXEItPlxcXFwqPycsXG4gICAgICAgICAgICBlbmQ6ICctPlxcXFwqPydcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiAnKCcgKyBKU19JREVOVF9SRSArICdcXFxccyooPzo9fDo9KVxcXFxzKik/IT8oXFxcXCguKlxcXFwpXFxcXHMqKT9cXFxcQlstfl17MSwyfT5cXFxcKj8nLFxuICAgICAgICAgICAgZW5kOiAnWy1+XXsxLDJ9PlxcXFwqPydcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiAnKCcgKyBKU19JREVOVF9SRSArICdcXFxccyooPzo9fDo9KVxcXFxzKik/KFxcXFwoLipcXFxcKVxcXFxzKik/XFxcXEIhP1stfl17MSwyfT5cXFxcKj8nLFxuICAgICAgICAgICAgZW5kOiAnIT9bLX5dezEsMn0+XFxcXCo/J1xuICAgICAgICAgIH1cbiAgICAgICAgXVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnY2xhc3MnLFxuICAgICAgICBiZWdpbktleXdvcmRzOiAnY2xhc3MnLFxuICAgICAgICBlbmQ6ICckJyxcbiAgICAgICAgaWxsZWdhbDogL1s6PVwiXFxbXFxdXS8sXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgYmVnaW5LZXl3b3JkczogJ2V4dGVuZHMnLFxuICAgICAgICAgICAgZW5kc1dpdGhQYXJlbnQ6IHRydWUsXG4gICAgICAgICAgICBpbGxlZ2FsOiAvWzo9XCJcXFtcXF1dLyxcbiAgICAgICAgICAgIGNvbnRhaW5zOiBbVElUTEVdXG4gICAgICAgICAgfSxcbiAgICAgICAgICBUSVRMRVxuICAgICAgICBdXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogSlNfSURFTlRfUkUgKyAnOicsXG4gICAgICAgIGVuZDogJzonLFxuICAgICAgICByZXR1cm5CZWdpbjogdHJ1ZSxcbiAgICAgICAgcmV0dXJuRW5kOiB0cnVlLFxuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH1cbiAgICBdKVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IGxpdmVzY3JpcHQ7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=