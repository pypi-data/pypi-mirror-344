(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_coffeescript"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/coffeescript.js":
/*!*******************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/coffeescript.js ***!
  \*******************************************************************************************************/
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
Language: CoffeeScript
Author: Dmytrii Nagirniak <dnagir@gmail.com>
Contributors: Oleg Efimov <efimovov@gmail.com>, Cédric Néhémie <cedric.nehemie@gmail.com>
Description: CoffeeScript is a programming language that transcompiles to JavaScript. For info about language see http://coffeescript.org/
Category: common, scripting
Website: https://coffeescript.org
*/

/** @type LanguageFn */
function coffeescript(hljs) {
  const COFFEE_BUILT_INS = [
    'npm',
    'print'
  ];
  const COFFEE_LITERALS = [
    'yes',
    'no',
    'on',
    'off'
  ];
  const COFFEE_KEYWORDS = [
    'then',
    'unless',
    'until',
    'loop',
    'by',
    'when',
    'and',
    'or',
    'is',
    'isnt',
    'not'
  ];
  const NOT_VALID_KEYWORDS = [
    "var",
    "const",
    "let",
    "function",
    "static"
  ];
  const excluding = (list) =>
    (kw) => !list.includes(kw);
  const KEYWORDS$1 = {
    keyword: KEYWORDS.concat(COFFEE_KEYWORDS).filter(excluding(NOT_VALID_KEYWORDS)),
    literal: LITERALS.concat(COFFEE_LITERALS),
    built_in: BUILT_INS.concat(COFFEE_BUILT_INS)
  };
  const JS_IDENT_RE = '[A-Za-z$_][0-9A-Za-z$_]*';
  const SUBST = {
    className: 'subst',
    begin: /#\{/,
    end: /\}/,
    keywords: KEYWORDS$1
  };
  const EXPRESSIONS = [
    hljs.BINARY_NUMBER_MODE,
    hljs.inherit(hljs.C_NUMBER_MODE, {
      starts: {
        end: '(\\s*/)?',
        relevance: 0
      }
    }), // a number tries to eat the following slash to prevent treating it as a regexp
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
            SUBST
          ]
        },
        {
          begin: /"/,
          end: /"/,
          contains: [
            hljs.BACKSLASH_ESCAPE,
            SUBST
          ]
        }
      ]
    },
    {
      className: 'regexp',
      variants: [
        {
          begin: '///',
          end: '///',
          contains: [
            SUBST,
            hljs.HASH_COMMENT_MODE
          ]
        },
        {
          begin: '//[gim]{0,3}(?=\\W)',
          relevance: 0
        },
        {
          // regex can't start with space to parse x / 2 / 3 as two divisions
          // regex can't start with *, and it supports an "illegal" in the main mode
          begin: /\/(?![ *]).*?(?![\\]).\/[gim]{0,3}(?=\W)/
        }
      ]
    },
    {
      begin: '@' + JS_IDENT_RE // relevance booster
    },
    {
      subLanguage: 'javascript',
      excludeBegin: true,
      excludeEnd: true,
      variants: [
        {
          begin: '```',
          end: '```'
        },
        {
          begin: '`',
          end: '`'
        }
      ]
    }
  ];
  SUBST.contains = EXPRESSIONS;

  const TITLE = hljs.inherit(hljs.TITLE_MODE, {
    begin: JS_IDENT_RE
  });
  const POSSIBLE_PARAMS_RE = '(\\(.*\\)\\s*)?\\B[-=]>';
  const PARAMS = {
    className: 'params',
    begin: '\\([^\\(]',
    returnBegin: true,
    /* We need another contained nameless mode to not have every nested
    pair of parens to be called "params" */
    contains: [{
      begin: /\(/,
      end: /\)/,
      keywords: KEYWORDS$1,
      contains: ['self'].concat(EXPRESSIONS)
    }]
  };

  return {
    name: 'CoffeeScript',
    aliases: [
      'coffee',
      'cson',
      'iced'
    ],
    keywords: KEYWORDS$1,
    illegal: /\/\*/,
    contains: EXPRESSIONS.concat([
      hljs.COMMENT('###', '###'),
      hljs.HASH_COMMENT_MODE,
      {
        className: 'function',
        begin: '^\\s*' + JS_IDENT_RE + '\\s*=\\s*' + POSSIBLE_PARAMS_RE,
        end: '[-=]>',
        returnBegin: true,
        contains: [
          TITLE,
          PARAMS
        ]
      },
      {
        // anonymous function start
        begin: /[:\(,=]\s*/,
        relevance: 0,
        contains: [{
          className: 'function',
          begin: POSSIBLE_PARAMS_RE,
          end: '[-=]>',
          returnBegin: true,
          contains: [PARAMS]
        }]
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

module.exports = coffeescript;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfY29mZmVlc2NyaXB0LmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxlQUFlO0FBQ2YsWUFBWTtBQUNaO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFNBQVM7QUFDVDtBQUNBO0FBQ0E7QUFDQTtBQUNBLFNBQVM7QUFDVDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFNBQVM7QUFDVDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxTQUFTO0FBQ1Q7QUFDQSwwQkFBMEIsSUFBSTtBQUM5QjtBQUNBLFNBQVM7QUFDVDtBQUNBO0FBQ0E7QUFDQSxnREFBZ0QsSUFBSTtBQUNwRDtBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFNBQVM7QUFDVDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQSxHQUFHO0FBQ0g7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFNBQVM7QUFDVCxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFdBQVc7QUFDWDtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9jb2ZmZWVzY3JpcHQuanMiXSwic291cmNlc0NvbnRlbnQiOlsiY29uc3QgS0VZV09SRFMgPSBbXG4gIFwiYXNcIiwgLy8gZm9yIGV4cG9ydHNcbiAgXCJpblwiLFxuICBcIm9mXCIsXG4gIFwiaWZcIixcbiAgXCJmb3JcIixcbiAgXCJ3aGlsZVwiLFxuICBcImZpbmFsbHlcIixcbiAgXCJ2YXJcIixcbiAgXCJuZXdcIixcbiAgXCJmdW5jdGlvblwiLFxuICBcImRvXCIsXG4gIFwicmV0dXJuXCIsXG4gIFwidm9pZFwiLFxuICBcImVsc2VcIixcbiAgXCJicmVha1wiLFxuICBcImNhdGNoXCIsXG4gIFwiaW5zdGFuY2VvZlwiLFxuICBcIndpdGhcIixcbiAgXCJ0aHJvd1wiLFxuICBcImNhc2VcIixcbiAgXCJkZWZhdWx0XCIsXG4gIFwidHJ5XCIsXG4gIFwic3dpdGNoXCIsXG4gIFwiY29udGludWVcIixcbiAgXCJ0eXBlb2ZcIixcbiAgXCJkZWxldGVcIixcbiAgXCJsZXRcIixcbiAgXCJ5aWVsZFwiLFxuICBcImNvbnN0XCIsXG4gIFwiY2xhc3NcIixcbiAgLy8gSlMgaGFuZGxlcyB0aGVzZSB3aXRoIGEgc3BlY2lhbCBydWxlXG4gIC8vIFwiZ2V0XCIsXG4gIC8vIFwic2V0XCIsXG4gIFwiZGVidWdnZXJcIixcbiAgXCJhc3luY1wiLFxuICBcImF3YWl0XCIsXG4gIFwic3RhdGljXCIsXG4gIFwiaW1wb3J0XCIsXG4gIFwiZnJvbVwiLFxuICBcImV4cG9ydFwiLFxuICBcImV4dGVuZHNcIlxuXTtcbmNvbnN0IExJVEVSQUxTID0gW1xuICBcInRydWVcIixcbiAgXCJmYWxzZVwiLFxuICBcIm51bGxcIixcbiAgXCJ1bmRlZmluZWRcIixcbiAgXCJOYU5cIixcbiAgXCJJbmZpbml0eVwiXG5dO1xuXG5jb25zdCBUWVBFUyA9IFtcbiAgXCJJbnRsXCIsXG4gIFwiRGF0YVZpZXdcIixcbiAgXCJOdW1iZXJcIixcbiAgXCJNYXRoXCIsXG4gIFwiRGF0ZVwiLFxuICBcIlN0cmluZ1wiLFxuICBcIlJlZ0V4cFwiLFxuICBcIk9iamVjdFwiLFxuICBcIkZ1bmN0aW9uXCIsXG4gIFwiQm9vbGVhblwiLFxuICBcIkVycm9yXCIsXG4gIFwiU3ltYm9sXCIsXG4gIFwiU2V0XCIsXG4gIFwiTWFwXCIsXG4gIFwiV2Vha1NldFwiLFxuICBcIldlYWtNYXBcIixcbiAgXCJQcm94eVwiLFxuICBcIlJlZmxlY3RcIixcbiAgXCJKU09OXCIsXG4gIFwiUHJvbWlzZVwiLFxuICBcIkZsb2F0NjRBcnJheVwiLFxuICBcIkludDE2QXJyYXlcIixcbiAgXCJJbnQzMkFycmF5XCIsXG4gIFwiSW50OEFycmF5XCIsXG4gIFwiVWludDE2QXJyYXlcIixcbiAgXCJVaW50MzJBcnJheVwiLFxuICBcIkZsb2F0MzJBcnJheVwiLFxuICBcIkFycmF5XCIsXG4gIFwiVWludDhBcnJheVwiLFxuICBcIlVpbnQ4Q2xhbXBlZEFycmF5XCIsXG4gIFwiQXJyYXlCdWZmZXJcIixcbiAgXCJCaWdJbnQ2NEFycmF5XCIsXG4gIFwiQmlnVWludDY0QXJyYXlcIixcbiAgXCJCaWdJbnRcIlxuXTtcblxuY29uc3QgRVJST1JfVFlQRVMgPSBbXG4gIFwiRXZhbEVycm9yXCIsXG4gIFwiSW50ZXJuYWxFcnJvclwiLFxuICBcIlJhbmdlRXJyb3JcIixcbiAgXCJSZWZlcmVuY2VFcnJvclwiLFxuICBcIlN5bnRheEVycm9yXCIsXG4gIFwiVHlwZUVycm9yXCIsXG4gIFwiVVJJRXJyb3JcIlxuXTtcblxuY29uc3QgQlVJTFRfSU5fR0xPQkFMUyA9IFtcbiAgXCJzZXRJbnRlcnZhbFwiLFxuICBcInNldFRpbWVvdXRcIixcbiAgXCJjbGVhckludGVydmFsXCIsXG4gIFwiY2xlYXJUaW1lb3V0XCIsXG5cbiAgXCJyZXF1aXJlXCIsXG4gIFwiZXhwb3J0c1wiLFxuXG4gIFwiZXZhbFwiLFxuICBcImlzRmluaXRlXCIsXG4gIFwiaXNOYU5cIixcbiAgXCJwYXJzZUZsb2F0XCIsXG4gIFwicGFyc2VJbnRcIixcbiAgXCJkZWNvZGVVUklcIixcbiAgXCJkZWNvZGVVUklDb21wb25lbnRcIixcbiAgXCJlbmNvZGVVUklcIixcbiAgXCJlbmNvZGVVUklDb21wb25lbnRcIixcbiAgXCJlc2NhcGVcIixcbiAgXCJ1bmVzY2FwZVwiXG5dO1xuXG5jb25zdCBCVUlMVF9JTl9WQVJJQUJMRVMgPSBbXG4gIFwiYXJndW1lbnRzXCIsXG4gIFwidGhpc1wiLFxuICBcInN1cGVyXCIsXG4gIFwiY29uc29sZVwiLFxuICBcIndpbmRvd1wiLFxuICBcImRvY3VtZW50XCIsXG4gIFwibG9jYWxTdG9yYWdlXCIsXG4gIFwibW9kdWxlXCIsXG4gIFwiZ2xvYmFsXCIgLy8gTm9kZS5qc1xuXTtcblxuY29uc3QgQlVJTFRfSU5TID0gW10uY29uY2F0KFxuICBCVUlMVF9JTl9HTE9CQUxTLFxuICBCVUlMVF9JTl9WQVJJQUJMRVMsXG4gIFRZUEVTLFxuICBFUlJPUl9UWVBFU1xuKTtcblxuLypcbkxhbmd1YWdlOiBDb2ZmZWVTY3JpcHRcbkF1dGhvcjogRG15dHJpaSBOYWdpcm5pYWsgPGRuYWdpckBnbWFpbC5jb20+XG5Db250cmlidXRvcnM6IE9sZWcgRWZpbW92IDxlZmltb3ZvdkBnbWFpbC5jb20+LCBDw6lkcmljIE7DqWjDqW1pZSA8Y2VkcmljLm5laGVtaWVAZ21haWwuY29tPlxuRGVzY3JpcHRpb246IENvZmZlZVNjcmlwdCBpcyBhIHByb2dyYW1taW5nIGxhbmd1YWdlIHRoYXQgdHJhbnNjb21waWxlcyB0byBKYXZhU2NyaXB0LiBGb3IgaW5mbyBhYm91dCBsYW5ndWFnZSBzZWUgaHR0cDovL2NvZmZlZXNjcmlwdC5vcmcvXG5DYXRlZ29yeTogY29tbW9uLCBzY3JpcHRpbmdcbldlYnNpdGU6IGh0dHBzOi8vY29mZmVlc2NyaXB0Lm9yZ1xuKi9cblxuLyoqIEB0eXBlIExhbmd1YWdlRm4gKi9cbmZ1bmN0aW9uIGNvZmZlZXNjcmlwdChobGpzKSB7XG4gIGNvbnN0IENPRkZFRV9CVUlMVF9JTlMgPSBbXG4gICAgJ25wbScsXG4gICAgJ3ByaW50J1xuICBdO1xuICBjb25zdCBDT0ZGRUVfTElURVJBTFMgPSBbXG4gICAgJ3llcycsXG4gICAgJ25vJyxcbiAgICAnb24nLFxuICAgICdvZmYnXG4gIF07XG4gIGNvbnN0IENPRkZFRV9LRVlXT1JEUyA9IFtcbiAgICAndGhlbicsXG4gICAgJ3VubGVzcycsXG4gICAgJ3VudGlsJyxcbiAgICAnbG9vcCcsXG4gICAgJ2J5JyxcbiAgICAnd2hlbicsXG4gICAgJ2FuZCcsXG4gICAgJ29yJyxcbiAgICAnaXMnLFxuICAgICdpc250JyxcbiAgICAnbm90J1xuICBdO1xuICBjb25zdCBOT1RfVkFMSURfS0VZV09SRFMgPSBbXG4gICAgXCJ2YXJcIixcbiAgICBcImNvbnN0XCIsXG4gICAgXCJsZXRcIixcbiAgICBcImZ1bmN0aW9uXCIsXG4gICAgXCJzdGF0aWNcIlxuICBdO1xuICBjb25zdCBleGNsdWRpbmcgPSAobGlzdCkgPT5cbiAgICAoa3cpID0+ICFsaXN0LmluY2x1ZGVzKGt3KTtcbiAgY29uc3QgS0VZV09SRFMkMSA9IHtcbiAgICBrZXl3b3JkOiBLRVlXT1JEUy5jb25jYXQoQ09GRkVFX0tFWVdPUkRTKS5maWx0ZXIoZXhjbHVkaW5nKE5PVF9WQUxJRF9LRVlXT1JEUykpLFxuICAgIGxpdGVyYWw6IExJVEVSQUxTLmNvbmNhdChDT0ZGRUVfTElURVJBTFMpLFxuICAgIGJ1aWx0X2luOiBCVUlMVF9JTlMuY29uY2F0KENPRkZFRV9CVUlMVF9JTlMpXG4gIH07XG4gIGNvbnN0IEpTX0lERU5UX1JFID0gJ1tBLVphLXokX11bMC05QS1aYS16JF9dKic7XG4gIGNvbnN0IFNVQlNUID0ge1xuICAgIGNsYXNzTmFtZTogJ3N1YnN0JyxcbiAgICBiZWdpbjogLyNcXHsvLFxuICAgIGVuZDogL1xcfS8sXG4gICAga2V5d29yZHM6IEtFWVdPUkRTJDFcbiAgfTtcbiAgY29uc3QgRVhQUkVTU0lPTlMgPSBbXG4gICAgaGxqcy5CSU5BUllfTlVNQkVSX01PREUsXG4gICAgaGxqcy5pbmhlcml0KGhsanMuQ19OVU1CRVJfTU9ERSwge1xuICAgICAgc3RhcnRzOiB7XG4gICAgICAgIGVuZDogJyhcXFxccyovKT8nLFxuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH1cbiAgICB9KSwgLy8gYSBudW1iZXIgdHJpZXMgdG8gZWF0IHRoZSBmb2xsb3dpbmcgc2xhc2ggdG8gcHJldmVudCB0cmVhdGluZyBpdCBhcyBhIHJlZ2V4cFxuICAgIHtcbiAgICAgIGNsYXNzTmFtZTogJ3N0cmluZycsXG4gICAgICB2YXJpYW50czogW1xuICAgICAgICB7XG4gICAgICAgICAgYmVnaW46IC8nJycvLFxuICAgICAgICAgIGVuZDogLycnJy8sXG4gICAgICAgICAgY29udGFpbnM6IFtobGpzLkJBQ0tTTEFTSF9FU0NBUEVdXG4gICAgICAgIH0sXG4gICAgICAgIHtcbiAgICAgICAgICBiZWdpbjogLycvLFxuICAgICAgICAgIGVuZDogLycvLFxuICAgICAgICAgIGNvbnRhaW5zOiBbaGxqcy5CQUNLU0xBU0hfRVNDQVBFXVxuICAgICAgICB9LFxuICAgICAgICB7XG4gICAgICAgICAgYmVnaW46IC9cIlwiXCIvLFxuICAgICAgICAgIGVuZDogL1wiXCJcIi8sXG4gICAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICAgIGhsanMuQkFDS1NMQVNIX0VTQ0FQRSxcbiAgICAgICAgICAgIFNVQlNUXG4gICAgICAgICAgXVxuICAgICAgICB9LFxuICAgICAgICB7XG4gICAgICAgICAgYmVnaW46IC9cIi8sXG4gICAgICAgICAgZW5kOiAvXCIvLFxuICAgICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgICBobGpzLkJBQ0tTTEFTSF9FU0NBUEUsXG4gICAgICAgICAgICBTVUJTVFxuICAgICAgICAgIF1cbiAgICAgICAgfVxuICAgICAgXVxuICAgIH0sXG4gICAge1xuICAgICAgY2xhc3NOYW1lOiAncmVnZXhwJyxcbiAgICAgIHZhcmlhbnRzOiBbXG4gICAgICAgIHtcbiAgICAgICAgICBiZWdpbjogJy8vLycsXG4gICAgICAgICAgZW5kOiAnLy8vJyxcbiAgICAgICAgICBjb250YWluczogW1xuICAgICAgICAgICAgU1VCU1QsXG4gICAgICAgICAgICBobGpzLkhBU0hfQ09NTUVOVF9NT0RFXG4gICAgICAgICAgXVxuICAgICAgICB9LFxuICAgICAgICB7XG4gICAgICAgICAgYmVnaW46ICcvL1tnaW1dezAsM30oPz1cXFxcVyknLFxuICAgICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgICB9LFxuICAgICAgICB7XG4gICAgICAgICAgLy8gcmVnZXggY2FuJ3Qgc3RhcnQgd2l0aCBzcGFjZSB0byBwYXJzZSB4IC8gMiAvIDMgYXMgdHdvIGRpdmlzaW9uc1xuICAgICAgICAgIC8vIHJlZ2V4IGNhbid0IHN0YXJ0IHdpdGggKiwgYW5kIGl0IHN1cHBvcnRzIGFuIFwiaWxsZWdhbFwiIGluIHRoZSBtYWluIG1vZGVcbiAgICAgICAgICBiZWdpbjogL1xcLyg/IVsgKl0pLio/KD8hW1xcXFxdKS5cXC9bZ2ltXXswLDN9KD89XFxXKS9cbiAgICAgICAgfVxuICAgICAgXVxuICAgIH0sXG4gICAge1xuICAgICAgYmVnaW46ICdAJyArIEpTX0lERU5UX1JFIC8vIHJlbGV2YW5jZSBib29zdGVyXG4gICAgfSxcbiAgICB7XG4gICAgICBzdWJMYW5ndWFnZTogJ2phdmFzY3JpcHQnLFxuICAgICAgZXhjbHVkZUJlZ2luOiB0cnVlLFxuICAgICAgZXhjbHVkZUVuZDogdHJ1ZSxcbiAgICAgIHZhcmlhbnRzOiBbXG4gICAgICAgIHtcbiAgICAgICAgICBiZWdpbjogJ2BgYCcsXG4gICAgICAgICAgZW5kOiAnYGBgJ1xuICAgICAgICB9LFxuICAgICAgICB7XG4gICAgICAgICAgYmVnaW46ICdgJyxcbiAgICAgICAgICBlbmQ6ICdgJ1xuICAgICAgICB9XG4gICAgICBdXG4gICAgfVxuICBdO1xuICBTVUJTVC5jb250YWlucyA9IEVYUFJFU1NJT05TO1xuXG4gIGNvbnN0IFRJVExFID0gaGxqcy5pbmhlcml0KGhsanMuVElUTEVfTU9ERSwge1xuICAgIGJlZ2luOiBKU19JREVOVF9SRVxuICB9KTtcbiAgY29uc3QgUE9TU0lCTEVfUEFSQU1TX1JFID0gJyhcXFxcKC4qXFxcXClcXFxccyopP1xcXFxCWy09XT4nO1xuICBjb25zdCBQQVJBTVMgPSB7XG4gICAgY2xhc3NOYW1lOiAncGFyYW1zJyxcbiAgICBiZWdpbjogJ1xcXFwoW15cXFxcKF0nLFxuICAgIHJldHVybkJlZ2luOiB0cnVlLFxuICAgIC8qIFdlIG5lZWQgYW5vdGhlciBjb250YWluZWQgbmFtZWxlc3MgbW9kZSB0byBub3QgaGF2ZSBldmVyeSBuZXN0ZWRcbiAgICBwYWlyIG9mIHBhcmVucyB0byBiZSBjYWxsZWQgXCJwYXJhbXNcIiAqL1xuICAgIGNvbnRhaW5zOiBbe1xuICAgICAgYmVnaW46IC9cXCgvLFxuICAgICAgZW5kOiAvXFwpLyxcbiAgICAgIGtleXdvcmRzOiBLRVlXT1JEUyQxLFxuICAgICAgY29udGFpbnM6IFsnc2VsZiddLmNvbmNhdChFWFBSRVNTSU9OUylcbiAgICB9XVxuICB9O1xuXG4gIHJldHVybiB7XG4gICAgbmFtZTogJ0NvZmZlZVNjcmlwdCcsXG4gICAgYWxpYXNlczogW1xuICAgICAgJ2NvZmZlZScsXG4gICAgICAnY3NvbicsXG4gICAgICAnaWNlZCdcbiAgICBdLFxuICAgIGtleXdvcmRzOiBLRVlXT1JEUyQxLFxuICAgIGlsbGVnYWw6IC9cXC9cXCovLFxuICAgIGNvbnRhaW5zOiBFWFBSRVNTSU9OUy5jb25jYXQoW1xuICAgICAgaGxqcy5DT01NRU5UKCcjIyMnLCAnIyMjJyksXG4gICAgICBobGpzLkhBU0hfQ09NTUVOVF9NT0RFLFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdmdW5jdGlvbicsXG4gICAgICAgIGJlZ2luOiAnXlxcXFxzKicgKyBKU19JREVOVF9SRSArICdcXFxccyo9XFxcXHMqJyArIFBPU1NJQkxFX1BBUkFNU19SRSxcbiAgICAgICAgZW5kOiAnWy09XT4nLFxuICAgICAgICByZXR1cm5CZWdpbjogdHJ1ZSxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICBUSVRMRSxcbiAgICAgICAgICBQQVJBTVNcbiAgICAgICAgXVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgLy8gYW5vbnltb3VzIGZ1bmN0aW9uIHN0YXJ0XG4gICAgICAgIGJlZ2luOiAvWzpcXCgsPV1cXHMqLyxcbiAgICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgICBjb250YWluczogW3tcbiAgICAgICAgICBjbGFzc05hbWU6ICdmdW5jdGlvbicsXG4gICAgICAgICAgYmVnaW46IFBPU1NJQkxFX1BBUkFNU19SRSxcbiAgICAgICAgICBlbmQ6ICdbLT1dPicsXG4gICAgICAgICAgcmV0dXJuQmVnaW46IHRydWUsXG4gICAgICAgICAgY29udGFpbnM6IFtQQVJBTVNdXG4gICAgICAgIH1dXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdjbGFzcycsXG4gICAgICAgIGJlZ2luS2V5d29yZHM6ICdjbGFzcycsXG4gICAgICAgIGVuZDogJyQnLFxuICAgICAgICBpbGxlZ2FsOiAvWzo9XCJcXFtcXF1dLyxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbktleXdvcmRzOiAnZXh0ZW5kcycsXG4gICAgICAgICAgICBlbmRzV2l0aFBhcmVudDogdHJ1ZSxcbiAgICAgICAgICAgIGlsbGVnYWw6IC9bOj1cIlxcW1xcXV0vLFxuICAgICAgICAgICAgY29udGFpbnM6IFtUSVRMRV1cbiAgICAgICAgICB9LFxuICAgICAgICAgIFRJVExFXG4gICAgICAgIF1cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiBKU19JREVOVF9SRSArICc6JyxcbiAgICAgICAgZW5kOiAnOicsXG4gICAgICAgIHJldHVybkJlZ2luOiB0cnVlLFxuICAgICAgICByZXR1cm5FbmQ6IHRydWUsXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfVxuICAgIF0pXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gY29mZmVlc2NyaXB0O1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9