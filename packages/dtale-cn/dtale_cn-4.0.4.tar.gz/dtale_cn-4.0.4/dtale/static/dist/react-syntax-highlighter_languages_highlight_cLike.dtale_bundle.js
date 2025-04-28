(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_cLike"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/c-like.js":
/*!*************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/c-like.js ***!
  \*************************************************************************************************/
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
Language: C++
Category: common, system
Website: https://isocpp.org
*/

/** @type LanguageFn */
function cPlusPlus(hljs) {
  // added for historic reasons because `hljs.C_LINE_COMMENT_MODE` does
  // not include such support nor can we be sure all the grammars depending
  // on it would desire this behavior
  const C_LINE_COMMENT_MODE = hljs.COMMENT('//', '$', {
    contains: [
      {
        begin: /\\\n/
      }
    ]
  });
  const DECLTYPE_AUTO_RE = 'decltype\\(auto\\)';
  const NAMESPACE_RE = '[a-zA-Z_]\\w*::';
  const TEMPLATE_ARGUMENT_RE = '<[^<>]+>';
  const FUNCTION_TYPE_RE = '(' +
    DECLTYPE_AUTO_RE + '|' +
    optional(NAMESPACE_RE) +
    '[a-zA-Z_]\\w*' + optional(TEMPLATE_ARGUMENT_RE) +
  ')';
  const CPP_PRIMITIVE_TYPES = {
    className: 'keyword',
    begin: '\\b[a-z\\d_]*_t\\b'
  };

  // https://en.cppreference.com/w/cpp/language/escape
  // \\ \x \xFF \u2837 \u00323747 \374
  const CHARACTER_ESCAPES = '\\\\(x[0-9A-Fa-f]{2}|u[0-9A-Fa-f]{4,8}|[0-7]{3}|\\S)';
  const STRINGS = {
    className: 'string',
    variants: [
      {
        begin: '(u8?|U|L)?"',
        end: '"',
        illegal: '\\n',
        contains: [ hljs.BACKSLASH_ESCAPE ]
      },
      {
        begin: '(u8?|U|L)?\'(' + CHARACTER_ESCAPES + "|.)",
        end: '\'',
        illegal: '.'
      },
      hljs.END_SAME_AS_BEGIN({
        begin: /(?:u8?|U|L)?R"([^()\\ ]{0,16})\(/,
        end: /\)([^()\\ ]{0,16})"/
      })
    ]
  };

  const NUMBERS = {
    className: 'number',
    variants: [
      {
        begin: '\\b(0b[01\']+)'
      },
      {
        begin: '(-?)\\b([\\d\']+(\\.[\\d\']*)?|\\.[\\d\']+)((ll|LL|l|L)(u|U)?|(u|U)(ll|LL|l|L)?|f|F|b|B)'
      },
      {
        begin: '(-?)(\\b0[xX][a-fA-F0-9\']+|(\\b[\\d\']+(\\.[\\d\']*)?|\\.[\\d\']+)([eE][-+]?[\\d\']+)?)'
      }
    ],
    relevance: 0
  };

  const PREPROCESSOR = {
    className: 'meta',
    begin: /#\s*[a-z]+\b/,
    end: /$/,
    keywords: {
      'meta-keyword':
        'if else elif endif define undef warning error line ' +
        'pragma _Pragma ifdef ifndef include'
    },
    contains: [
      {
        begin: /\\\n/,
        relevance: 0
      },
      hljs.inherit(STRINGS, {
        className: 'meta-string'
      }),
      {
        className: 'meta-string',
        begin: /<.*?>/
      },
      C_LINE_COMMENT_MODE,
      hljs.C_BLOCK_COMMENT_MODE
    ]
  };

  const TITLE_MODE = {
    className: 'title',
    begin: optional(NAMESPACE_RE) + hljs.IDENT_RE,
    relevance: 0
  };

  const FUNCTION_TITLE = optional(NAMESPACE_RE) + hljs.IDENT_RE + '\\s*\\(';

  const COMMON_CPP_HINTS = [
    'asin',
    'atan2',
    'atan',
    'calloc',
    'ceil',
    'cosh',
    'cos',
    'exit',
    'exp',
    'fabs',
    'floor',
    'fmod',
    'fprintf',
    'fputs',
    'free',
    'frexp',
    'auto_ptr',
    'deque',
    'list',
    'queue',
    'stack',
    'vector',
    'map',
    'set',
    'pair',
    'bitset',
    'multiset',
    'multimap',
    'unordered_set',
    'fscanf',
    'future',
    'isalnum',
    'isalpha',
    'iscntrl',
    'isdigit',
    'isgraph',
    'islower',
    'isprint',
    'ispunct',
    'isspace',
    'isupper',
    'isxdigit',
    'tolower',
    'toupper',
    'labs',
    'ldexp',
    'log10',
    'log',
    'malloc',
    'realloc',
    'memchr',
    'memcmp',
    'memcpy',
    'memset',
    'modf',
    'pow',
    'printf',
    'putchar',
    'puts',
    'scanf',
    'sinh',
    'sin',
    'snprintf',
    'sprintf',
    'sqrt',
    'sscanf',
    'strcat',
    'strchr',
    'strcmp',
    'strcpy',
    'strcspn',
    'strlen',
    'strncat',
    'strncmp',
    'strncpy',
    'strpbrk',
    'strrchr',
    'strspn',
    'strstr',
    'tanh',
    'tan',
    'unordered_map',
    'unordered_multiset',
    'unordered_multimap',
    'priority_queue',
    'make_pair',
    'array',
    'shared_ptr',
    'abort',
    'terminate',
    'abs',
    'acos',
    'vfprintf',
    'vprintf',
    'vsprintf',
    'endl',
    'initializer_list',
    'unique_ptr',
    'complex',
    'imaginary',
    'std',
    'string',
    'wstring',
    'cin',
    'cout',
    'cerr',
    'clog',
    'stdin',
    'stdout',
    'stderr',
    'stringstream',
    'istringstream',
    'ostringstream'
  ];

  const CPP_KEYWORDS = {
    keyword: 'int float while private char char8_t char16_t char32_t catch import module export virtual operator sizeof ' +
      'dynamic_cast|10 typedef const_cast|10 const for static_cast|10 union namespace ' +
      'unsigned long volatile static protected bool template mutable if public friend ' +
      'do goto auto void enum else break extern using asm case typeid wchar_t ' +
      'short reinterpret_cast|10 default double register explicit signed typename try this ' +
      'switch continue inline delete alignas alignof constexpr consteval constinit decltype ' +
      'concept co_await co_return co_yield requires ' +
      'noexcept static_assert thread_local restrict final override ' +
      'atomic_bool atomic_char atomic_schar ' +
      'atomic_uchar atomic_short atomic_ushort atomic_int atomic_uint atomic_long atomic_ulong atomic_llong ' +
      'atomic_ullong new throw return ' +
      'and and_eq bitand bitor compl not not_eq or or_eq xor xor_eq',
    built_in: '_Bool _Complex _Imaginary',
    _relevance_hints: COMMON_CPP_HINTS,
    literal: 'true false nullptr NULL'
  };

  const FUNCTION_DISPATCH = {
    className: "function.dispatch",
    relevance: 0,
    keywords: CPP_KEYWORDS,
    begin: concat(
      /\b/,
      /(?!decltype)/,
      /(?!if)/,
      /(?!for)/,
      /(?!while)/,
      hljs.IDENT_RE,
      lookahead(/\s*\(/))
  };

  const EXPRESSION_CONTAINS = [
    FUNCTION_DISPATCH,
    PREPROCESSOR,
    CPP_PRIMITIVE_TYPES,
    C_LINE_COMMENT_MODE,
    hljs.C_BLOCK_COMMENT_MODE,
    NUMBERS,
    STRINGS
  ];


  const EXPRESSION_CONTEXT = {
    // This mode covers expression context where we can't expect a function
    // definition and shouldn't highlight anything that looks like one:
    // `return some()`, `else if()`, `(x*sum(1, 2))`
    variants: [
      {
        begin: /=/,
        end: /;/
      },
      {
        begin: /\(/,
        end: /\)/
      },
      {
        beginKeywords: 'new throw return else',
        end: /;/
      }
    ],
    keywords: CPP_KEYWORDS,
    contains: EXPRESSION_CONTAINS.concat([
      {
        begin: /\(/,
        end: /\)/,
        keywords: CPP_KEYWORDS,
        contains: EXPRESSION_CONTAINS.concat([ 'self' ]),
        relevance: 0
      }
    ]),
    relevance: 0
  };

  const FUNCTION_DECLARATION = {
    className: 'function',
    begin: '(' + FUNCTION_TYPE_RE + '[\\*&\\s]+)+' + FUNCTION_TITLE,
    returnBegin: true,
    end: /[{;=]/,
    excludeEnd: true,
    keywords: CPP_KEYWORDS,
    illegal: /[^\w\s\*&:<>.]/,
    contains: [
      { // to prevent it from being confused as the function title
        begin: DECLTYPE_AUTO_RE,
        keywords: CPP_KEYWORDS,
        relevance: 0
      },
      {
        begin: FUNCTION_TITLE,
        returnBegin: true,
        contains: [ TITLE_MODE ],
        relevance: 0
      },
      // needed because we do not have look-behind on the below rule
      // to prevent it from grabbing the final : in a :: pair
      {
        begin: /::/,
        relevance: 0
      },
      // initializers
      {
        begin: /:/,
        endsWithParent: true,
        contains: [
          STRINGS,
          NUMBERS
        ]
      },
      {
        className: 'params',
        begin: /\(/,
        end: /\)/,
        keywords: CPP_KEYWORDS,
        relevance: 0,
        contains: [
          C_LINE_COMMENT_MODE,
          hljs.C_BLOCK_COMMENT_MODE,
          STRINGS,
          NUMBERS,
          CPP_PRIMITIVE_TYPES,
          // Count matching parentheses.
          {
            begin: /\(/,
            end: /\)/,
            keywords: CPP_KEYWORDS,
            relevance: 0,
            contains: [
              'self',
              C_LINE_COMMENT_MODE,
              hljs.C_BLOCK_COMMENT_MODE,
              STRINGS,
              NUMBERS,
              CPP_PRIMITIVE_TYPES
            ]
          }
        ]
      },
      CPP_PRIMITIVE_TYPES,
      C_LINE_COMMENT_MODE,
      hljs.C_BLOCK_COMMENT_MODE,
      PREPROCESSOR
    ]
  };

  return {
    name: 'C++',
    aliases: [
      'cc',
      'c++',
      'h++',
      'hpp',
      'hh',
      'hxx',
      'cxx'
    ],
    keywords: CPP_KEYWORDS,
    illegal: '</',
    classNameAliases: {
      "function.dispatch": "built_in"
    },
    contains: [].concat(
      EXPRESSION_CONTEXT,
      FUNCTION_DECLARATION,
      FUNCTION_DISPATCH,
      EXPRESSION_CONTAINS,
      [
        PREPROCESSOR,
        { // containers: ie, `vector <int> rooms (9);`
          begin: '\\b(deque|list|queue|priority_queue|pair|stack|vector|map|set|bitset|multiset|multimap|unordered_map|unordered_set|unordered_multiset|unordered_multimap|array)\\s*<',
          end: '>',
          keywords: CPP_KEYWORDS,
          contains: [
            'self',
            CPP_PRIMITIVE_TYPES
          ]
        },
        {
          begin: hljs.IDENT_RE + '::',
          keywords: CPP_KEYWORDS
        },
        {
          className: 'class',
          beginKeywords: 'enum class struct union',
          end: /[{;:<>=]/,
          contains: [
            {
              beginKeywords: "final class struct"
            },
            hljs.TITLE_MODE
          ]
        }
      ]),
    exports: {
      preprocessor: PREPROCESSOR,
      strings: STRINGS,
      keywords: CPP_KEYWORDS
    }
  };
}

/*
Language: C-like (deprecated, use C and C++ instead)
Author: Ivan Sagalaev <maniac@softwaremaniacs.org>
Contributors: Evgeny Stepanischev <imbolk@gmail.com>, Zaven Muradyan <megalivoithos@gmail.com>, Roel Deckers <admin@codingcat.nl>, Sam Wu <samsam2310@gmail.com>, Jordi Petit <jordi.petit@gmail.com>, Pieter Vantorre <pietervantorre@gmail.com>, Google Inc. (David Benjamin) <davidben@google.com>
*/

/** @type LanguageFn */
function cLike(hljs) {
  const lang = cPlusPlus(hljs);

  const C_ALIASES = [
    "c",
    "h"
  ];

  const CPP_ALIASES = [
    'cc',
    'c++',
    'h++',
    'hpp',
    'hh',
    'hxx',
    'cxx'
  ];

  lang.disableAutodetect = true;
  lang.aliases = [];
  // support users only loading c-like (legacy)
  if (!hljs.getLanguage("c")) lang.aliases.push(...C_ALIASES);
  if (!hljs.getLanguage("cpp")) lang.aliases.push(...CPP_ALIASES);

  // if c and cpp are loaded after then they will reclaim these
  // aliases for themselves

  return lang;
}

module.exports = cLike;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfY0xpa2UuZHRhbGVfYnVuZGxlLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7O0FBQUE7QUFDQSxXQUFXLFFBQVE7QUFDbkIsYUFBYTtBQUNiOztBQUVBO0FBQ0EsV0FBVyxrQkFBa0I7QUFDN0IsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7O0FBRUE7QUFDQSxXQUFXLGtCQUFrQjtBQUM3QixhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQSxXQUFXLGtCQUFrQjtBQUM3QixhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQSxXQUFXLHVCQUF1QjtBQUNsQyxhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxHQUFHO0FBQ0g7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQSwrQ0FBK0MsRUFBRSxjQUFjLElBQUksT0FBTyxFQUFFO0FBQzVFO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQSx3Q0FBd0MsS0FBSztBQUM3QywwQkFBMEIsS0FBSztBQUMvQixPQUFPO0FBQ1A7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7O0FBR0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxlQUFlO0FBQ2YsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0EsZUFBZTtBQUNmO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQSxhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7QUFDQSxRQUFRO0FBQ1I7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxVQUFVLDJDQUEyQztBQUNyRDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFNBQVM7QUFDVDtBQUNBO0FBQ0E7QUFDQSxTQUFTO0FBQ1Q7QUFDQTtBQUNBO0FBQ0EsbUJBQW1CO0FBQ25CO0FBQ0E7QUFDQTtBQUNBLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7O0FBRUE7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvYy1saWtlLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qKlxuICogQHBhcmFtIHtzdHJpbmd9IHZhbHVlXG4gKiBAcmV0dXJucyB7UmVnRXhwfVxuICogKi9cblxuLyoqXG4gKiBAcGFyYW0ge1JlZ0V4cCB8IHN0cmluZyB9IHJlXG4gKiBAcmV0dXJucyB7c3RyaW5nfVxuICovXG5mdW5jdGlvbiBzb3VyY2UocmUpIHtcbiAgaWYgKCFyZSkgcmV0dXJuIG51bGw7XG4gIGlmICh0eXBlb2YgcmUgPT09IFwic3RyaW5nXCIpIHJldHVybiByZTtcblxuICByZXR1cm4gcmUuc291cmNlO1xufVxuXG4vKipcbiAqIEBwYXJhbSB7UmVnRXhwIHwgc3RyaW5nIH0gcmVcbiAqIEByZXR1cm5zIHtzdHJpbmd9XG4gKi9cbmZ1bmN0aW9uIGxvb2thaGVhZChyZSkge1xuICByZXR1cm4gY29uY2F0KCcoPz0nLCByZSwgJyknKTtcbn1cblxuLyoqXG4gKiBAcGFyYW0ge1JlZ0V4cCB8IHN0cmluZyB9IHJlXG4gKiBAcmV0dXJucyB7c3RyaW5nfVxuICovXG5mdW5jdGlvbiBvcHRpb25hbChyZSkge1xuICByZXR1cm4gY29uY2F0KCcoJywgcmUsICcpPycpO1xufVxuXG4vKipcbiAqIEBwYXJhbSB7Li4uKFJlZ0V4cCB8IHN0cmluZykgfSBhcmdzXG4gKiBAcmV0dXJucyB7c3RyaW5nfVxuICovXG5mdW5jdGlvbiBjb25jYXQoLi4uYXJncykge1xuICBjb25zdCBqb2luZWQgPSBhcmdzLm1hcCgoeCkgPT4gc291cmNlKHgpKS5qb2luKFwiXCIpO1xuICByZXR1cm4gam9pbmVkO1xufVxuXG4vKlxuTGFuZ3VhZ2U6IEMrK1xuQ2F0ZWdvcnk6IGNvbW1vbiwgc3lzdGVtXG5XZWJzaXRlOiBodHRwczovL2lzb2NwcC5vcmdcbiovXG5cbi8qKiBAdHlwZSBMYW5ndWFnZUZuICovXG5mdW5jdGlvbiBjUGx1c1BsdXMoaGxqcykge1xuICAvLyBhZGRlZCBmb3IgaGlzdG9yaWMgcmVhc29ucyBiZWNhdXNlIGBobGpzLkNfTElORV9DT01NRU5UX01PREVgIGRvZXNcbiAgLy8gbm90IGluY2x1ZGUgc3VjaCBzdXBwb3J0IG5vciBjYW4gd2UgYmUgc3VyZSBhbGwgdGhlIGdyYW1tYXJzIGRlcGVuZGluZ1xuICAvLyBvbiBpdCB3b3VsZCBkZXNpcmUgdGhpcyBiZWhhdmlvclxuICBjb25zdCBDX0xJTkVfQ09NTUVOVF9NT0RFID0gaGxqcy5DT01NRU5UKCcvLycsICckJywge1xuICAgIGNvbnRhaW5zOiBbXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAvXFxcXFxcbi9cbiAgICAgIH1cbiAgICBdXG4gIH0pO1xuICBjb25zdCBERUNMVFlQRV9BVVRPX1JFID0gJ2RlY2x0eXBlXFxcXChhdXRvXFxcXCknO1xuICBjb25zdCBOQU1FU1BBQ0VfUkUgPSAnW2EtekEtWl9dXFxcXHcqOjonO1xuICBjb25zdCBURU1QTEFURV9BUkdVTUVOVF9SRSA9ICc8W148Pl0rPic7XG4gIGNvbnN0IEZVTkNUSU9OX1RZUEVfUkUgPSAnKCcgK1xuICAgIERFQ0xUWVBFX0FVVE9fUkUgKyAnfCcgK1xuICAgIG9wdGlvbmFsKE5BTUVTUEFDRV9SRSkgK1xuICAgICdbYS16QS1aX11cXFxcdyonICsgb3B0aW9uYWwoVEVNUExBVEVfQVJHVU1FTlRfUkUpICtcbiAgJyknO1xuICBjb25zdCBDUFBfUFJJTUlUSVZFX1RZUEVTID0ge1xuICAgIGNsYXNzTmFtZTogJ2tleXdvcmQnLFxuICAgIGJlZ2luOiAnXFxcXGJbYS16XFxcXGRfXSpfdFxcXFxiJ1xuICB9O1xuXG4gIC8vIGh0dHBzOi8vZW4uY3BwcmVmZXJlbmNlLmNvbS93L2NwcC9sYW5ndWFnZS9lc2NhcGVcbiAgLy8gXFxcXCBcXHggXFx4RkYgXFx1MjgzNyBcXHUwMDMyMzc0NyBcXDM3NFxuICBjb25zdCBDSEFSQUNURVJfRVNDQVBFUyA9ICdcXFxcXFxcXCh4WzAtOUEtRmEtZl17Mn18dVswLTlBLUZhLWZdezQsOH18WzAtN117M318XFxcXFMpJztcbiAgY29uc3QgU1RSSU5HUyA9IHtcbiAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgIHZhcmlhbnRzOiBbXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnKHU4P3xVfEwpP1wiJyxcbiAgICAgICAgZW5kOiAnXCInLFxuICAgICAgICBpbGxlZ2FsOiAnXFxcXG4nLFxuICAgICAgICBjb250YWluczogWyBobGpzLkJBQ0tTTEFTSF9FU0NBUEUgXVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICcodTg/fFV8TCk/XFwnKCcgKyBDSEFSQUNURVJfRVNDQVBFUyArIFwifC4pXCIsXG4gICAgICAgIGVuZDogJ1xcJycsXG4gICAgICAgIGlsbGVnYWw6ICcuJ1xuICAgICAgfSxcbiAgICAgIGhsanMuRU5EX1NBTUVfQVNfQkVHSU4oe1xuICAgICAgICBiZWdpbjogLyg/OnU4P3xVfEwpP1JcIihbXigpXFxcXCBdezAsMTZ9KVxcKC8sXG4gICAgICAgIGVuZDogL1xcKShbXigpXFxcXCBdezAsMTZ9KVwiL1xuICAgICAgfSlcbiAgICBdXG4gIH07XG5cbiAgY29uc3QgTlVNQkVSUyA9IHtcbiAgICBjbGFzc05hbWU6ICdudW1iZXInLFxuICAgIHZhcmlhbnRzOiBbXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnXFxcXGIoMGJbMDFcXCddKyknXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogJygtPylcXFxcYihbXFxcXGRcXCddKyhcXFxcLltcXFxcZFxcJ10qKT98XFxcXC5bXFxcXGRcXCddKykoKGxsfExMfGx8TCkodXxVKT98KHV8VSkobGx8TEx8bHxMKT98ZnxGfGJ8QiknXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogJygtPykoXFxcXGIwW3hYXVthLWZBLUYwLTlcXCddK3woXFxcXGJbXFxcXGRcXCddKyhcXFxcLltcXFxcZFxcJ10qKT98XFxcXC5bXFxcXGRcXCddKykoW2VFXVstK10/W1xcXFxkXFwnXSspPyknXG4gICAgICB9XG4gICAgXSxcbiAgICByZWxldmFuY2U6IDBcbiAgfTtcblxuICBjb25zdCBQUkVQUk9DRVNTT1IgPSB7XG4gICAgY2xhc3NOYW1lOiAnbWV0YScsXG4gICAgYmVnaW46IC8jXFxzKlthLXpdK1xcYi8sXG4gICAgZW5kOiAvJC8sXG4gICAga2V5d29yZHM6IHtcbiAgICAgICdtZXRhLWtleXdvcmQnOlxuICAgICAgICAnaWYgZWxzZSBlbGlmIGVuZGlmIGRlZmluZSB1bmRlZiB3YXJuaW5nIGVycm9yIGxpbmUgJyArXG4gICAgICAgICdwcmFnbWEgX1ByYWdtYSBpZmRlZiBpZm5kZWYgaW5jbHVkZSdcbiAgICB9LFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAvXFxcXFxcbi8sXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfSxcbiAgICAgIGhsanMuaW5oZXJpdChTVFJJTkdTLCB7XG4gICAgICAgIGNsYXNzTmFtZTogJ21ldGEtc3RyaW5nJ1xuICAgICAgfSksXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ21ldGEtc3RyaW5nJyxcbiAgICAgICAgYmVnaW46IC88Lio/Pi9cbiAgICAgIH0sXG4gICAgICBDX0xJTkVfQ09NTUVOVF9NT0RFLFxuICAgICAgaGxqcy5DX0JMT0NLX0NPTU1FTlRfTU9ERVxuICAgIF1cbiAgfTtcblxuICBjb25zdCBUSVRMRV9NT0RFID0ge1xuICAgIGNsYXNzTmFtZTogJ3RpdGxlJyxcbiAgICBiZWdpbjogb3B0aW9uYWwoTkFNRVNQQUNFX1JFKSArIGhsanMuSURFTlRfUkUsXG4gICAgcmVsZXZhbmNlOiAwXG4gIH07XG5cbiAgY29uc3QgRlVOQ1RJT05fVElUTEUgPSBvcHRpb25hbChOQU1FU1BBQ0VfUkUpICsgaGxqcy5JREVOVF9SRSArICdcXFxccypcXFxcKCc7XG5cbiAgY29uc3QgQ09NTU9OX0NQUF9ISU5UUyA9IFtcbiAgICAnYXNpbicsXG4gICAgJ2F0YW4yJyxcbiAgICAnYXRhbicsXG4gICAgJ2NhbGxvYycsXG4gICAgJ2NlaWwnLFxuICAgICdjb3NoJyxcbiAgICAnY29zJyxcbiAgICAnZXhpdCcsXG4gICAgJ2V4cCcsXG4gICAgJ2ZhYnMnLFxuICAgICdmbG9vcicsXG4gICAgJ2Ztb2QnLFxuICAgICdmcHJpbnRmJyxcbiAgICAnZnB1dHMnLFxuICAgICdmcmVlJyxcbiAgICAnZnJleHAnLFxuICAgICdhdXRvX3B0cicsXG4gICAgJ2RlcXVlJyxcbiAgICAnbGlzdCcsXG4gICAgJ3F1ZXVlJyxcbiAgICAnc3RhY2snLFxuICAgICd2ZWN0b3InLFxuICAgICdtYXAnLFxuICAgICdzZXQnLFxuICAgICdwYWlyJyxcbiAgICAnYml0c2V0JyxcbiAgICAnbXVsdGlzZXQnLFxuICAgICdtdWx0aW1hcCcsXG4gICAgJ3Vub3JkZXJlZF9zZXQnLFxuICAgICdmc2NhbmYnLFxuICAgICdmdXR1cmUnLFxuICAgICdpc2FsbnVtJyxcbiAgICAnaXNhbHBoYScsXG4gICAgJ2lzY250cmwnLFxuICAgICdpc2RpZ2l0JyxcbiAgICAnaXNncmFwaCcsXG4gICAgJ2lzbG93ZXInLFxuICAgICdpc3ByaW50JyxcbiAgICAnaXNwdW5jdCcsXG4gICAgJ2lzc3BhY2UnLFxuICAgICdpc3VwcGVyJyxcbiAgICAnaXN4ZGlnaXQnLFxuICAgICd0b2xvd2VyJyxcbiAgICAndG91cHBlcicsXG4gICAgJ2xhYnMnLFxuICAgICdsZGV4cCcsXG4gICAgJ2xvZzEwJyxcbiAgICAnbG9nJyxcbiAgICAnbWFsbG9jJyxcbiAgICAncmVhbGxvYycsXG4gICAgJ21lbWNocicsXG4gICAgJ21lbWNtcCcsXG4gICAgJ21lbWNweScsXG4gICAgJ21lbXNldCcsXG4gICAgJ21vZGYnLFxuICAgICdwb3cnLFxuICAgICdwcmludGYnLFxuICAgICdwdXRjaGFyJyxcbiAgICAncHV0cycsXG4gICAgJ3NjYW5mJyxcbiAgICAnc2luaCcsXG4gICAgJ3NpbicsXG4gICAgJ3NucHJpbnRmJyxcbiAgICAnc3ByaW50ZicsXG4gICAgJ3NxcnQnLFxuICAgICdzc2NhbmYnLFxuICAgICdzdHJjYXQnLFxuICAgICdzdHJjaHInLFxuICAgICdzdHJjbXAnLFxuICAgICdzdHJjcHknLFxuICAgICdzdHJjc3BuJyxcbiAgICAnc3RybGVuJyxcbiAgICAnc3RybmNhdCcsXG4gICAgJ3N0cm5jbXAnLFxuICAgICdzdHJuY3B5JyxcbiAgICAnc3RycGJyaycsXG4gICAgJ3N0cnJjaHInLFxuICAgICdzdHJzcG4nLFxuICAgICdzdHJzdHInLFxuICAgICd0YW5oJyxcbiAgICAndGFuJyxcbiAgICAndW5vcmRlcmVkX21hcCcsXG4gICAgJ3Vub3JkZXJlZF9tdWx0aXNldCcsXG4gICAgJ3Vub3JkZXJlZF9tdWx0aW1hcCcsXG4gICAgJ3ByaW9yaXR5X3F1ZXVlJyxcbiAgICAnbWFrZV9wYWlyJyxcbiAgICAnYXJyYXknLFxuICAgICdzaGFyZWRfcHRyJyxcbiAgICAnYWJvcnQnLFxuICAgICd0ZXJtaW5hdGUnLFxuICAgICdhYnMnLFxuICAgICdhY29zJyxcbiAgICAndmZwcmludGYnLFxuICAgICd2cHJpbnRmJyxcbiAgICAndnNwcmludGYnLFxuICAgICdlbmRsJyxcbiAgICAnaW5pdGlhbGl6ZXJfbGlzdCcsXG4gICAgJ3VuaXF1ZV9wdHInLFxuICAgICdjb21wbGV4JyxcbiAgICAnaW1hZ2luYXJ5JyxcbiAgICAnc3RkJyxcbiAgICAnc3RyaW5nJyxcbiAgICAnd3N0cmluZycsXG4gICAgJ2NpbicsXG4gICAgJ2NvdXQnLFxuICAgICdjZXJyJyxcbiAgICAnY2xvZycsXG4gICAgJ3N0ZGluJyxcbiAgICAnc3Rkb3V0JyxcbiAgICAnc3RkZXJyJyxcbiAgICAnc3RyaW5nc3RyZWFtJyxcbiAgICAnaXN0cmluZ3N0cmVhbScsXG4gICAgJ29zdHJpbmdzdHJlYW0nXG4gIF07XG5cbiAgY29uc3QgQ1BQX0tFWVdPUkRTID0ge1xuICAgIGtleXdvcmQ6ICdpbnQgZmxvYXQgd2hpbGUgcHJpdmF0ZSBjaGFyIGNoYXI4X3QgY2hhcjE2X3QgY2hhcjMyX3QgY2F0Y2ggaW1wb3J0IG1vZHVsZSBleHBvcnQgdmlydHVhbCBvcGVyYXRvciBzaXplb2YgJyArXG4gICAgICAnZHluYW1pY19jYXN0fDEwIHR5cGVkZWYgY29uc3RfY2FzdHwxMCBjb25zdCBmb3Igc3RhdGljX2Nhc3R8MTAgdW5pb24gbmFtZXNwYWNlICcgK1xuICAgICAgJ3Vuc2lnbmVkIGxvbmcgdm9sYXRpbGUgc3RhdGljIHByb3RlY3RlZCBib29sIHRlbXBsYXRlIG11dGFibGUgaWYgcHVibGljIGZyaWVuZCAnICtcbiAgICAgICdkbyBnb3RvIGF1dG8gdm9pZCBlbnVtIGVsc2UgYnJlYWsgZXh0ZXJuIHVzaW5nIGFzbSBjYXNlIHR5cGVpZCB3Y2hhcl90ICcgK1xuICAgICAgJ3Nob3J0IHJlaW50ZXJwcmV0X2Nhc3R8MTAgZGVmYXVsdCBkb3VibGUgcmVnaXN0ZXIgZXhwbGljaXQgc2lnbmVkIHR5cGVuYW1lIHRyeSB0aGlzICcgK1xuICAgICAgJ3N3aXRjaCBjb250aW51ZSBpbmxpbmUgZGVsZXRlIGFsaWduYXMgYWxpZ25vZiBjb25zdGV4cHIgY29uc3RldmFsIGNvbnN0aW5pdCBkZWNsdHlwZSAnICtcbiAgICAgICdjb25jZXB0IGNvX2F3YWl0IGNvX3JldHVybiBjb195aWVsZCByZXF1aXJlcyAnICtcbiAgICAgICdub2V4Y2VwdCBzdGF0aWNfYXNzZXJ0IHRocmVhZF9sb2NhbCByZXN0cmljdCBmaW5hbCBvdmVycmlkZSAnICtcbiAgICAgICdhdG9taWNfYm9vbCBhdG9taWNfY2hhciBhdG9taWNfc2NoYXIgJyArXG4gICAgICAnYXRvbWljX3VjaGFyIGF0b21pY19zaG9ydCBhdG9taWNfdXNob3J0IGF0b21pY19pbnQgYXRvbWljX3VpbnQgYXRvbWljX2xvbmcgYXRvbWljX3Vsb25nIGF0b21pY19sbG9uZyAnICtcbiAgICAgICdhdG9taWNfdWxsb25nIG5ldyB0aHJvdyByZXR1cm4gJyArXG4gICAgICAnYW5kIGFuZF9lcSBiaXRhbmQgYml0b3IgY29tcGwgbm90IG5vdF9lcSBvciBvcl9lcSB4b3IgeG9yX2VxJyxcbiAgICBidWlsdF9pbjogJ19Cb29sIF9Db21wbGV4IF9JbWFnaW5hcnknLFxuICAgIF9yZWxldmFuY2VfaGludHM6IENPTU1PTl9DUFBfSElOVFMsXG4gICAgbGl0ZXJhbDogJ3RydWUgZmFsc2UgbnVsbHB0ciBOVUxMJ1xuICB9O1xuXG4gIGNvbnN0IEZVTkNUSU9OX0RJU1BBVENIID0ge1xuICAgIGNsYXNzTmFtZTogXCJmdW5jdGlvbi5kaXNwYXRjaFwiLFxuICAgIHJlbGV2YW5jZTogMCxcbiAgICBrZXl3b3JkczogQ1BQX0tFWVdPUkRTLFxuICAgIGJlZ2luOiBjb25jYXQoXG4gICAgICAvXFxiLyxcbiAgICAgIC8oPyFkZWNsdHlwZSkvLFxuICAgICAgLyg/IWlmKS8sXG4gICAgICAvKD8hZm9yKS8sXG4gICAgICAvKD8hd2hpbGUpLyxcbiAgICAgIGhsanMuSURFTlRfUkUsXG4gICAgICBsb29rYWhlYWQoL1xccypcXCgvKSlcbiAgfTtcblxuICBjb25zdCBFWFBSRVNTSU9OX0NPTlRBSU5TID0gW1xuICAgIEZVTkNUSU9OX0RJU1BBVENILFxuICAgIFBSRVBST0NFU1NPUixcbiAgICBDUFBfUFJJTUlUSVZFX1RZUEVTLFxuICAgIENfTElORV9DT01NRU5UX01PREUsXG4gICAgaGxqcy5DX0JMT0NLX0NPTU1FTlRfTU9ERSxcbiAgICBOVU1CRVJTLFxuICAgIFNUUklOR1NcbiAgXTtcblxuXG4gIGNvbnN0IEVYUFJFU1NJT05fQ09OVEVYVCA9IHtcbiAgICAvLyBUaGlzIG1vZGUgY292ZXJzIGV4cHJlc3Npb24gY29udGV4dCB3aGVyZSB3ZSBjYW4ndCBleHBlY3QgYSBmdW5jdGlvblxuICAgIC8vIGRlZmluaXRpb24gYW5kIHNob3VsZG4ndCBoaWdobGlnaHQgYW55dGhpbmcgdGhhdCBsb29rcyBsaWtlIG9uZTpcbiAgICAvLyBgcmV0dXJuIHNvbWUoKWAsIGBlbHNlIGlmKClgLCBgKHgqc3VtKDEsIDIpKWBcbiAgICB2YXJpYW50czogW1xuICAgICAge1xuICAgICAgICBiZWdpbjogLz0vLFxuICAgICAgICBlbmQ6IC87L1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC9cXCgvLFxuICAgICAgICBlbmQ6IC9cXCkvXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbktleXdvcmRzOiAnbmV3IHRocm93IHJldHVybiBlbHNlJyxcbiAgICAgICAgZW5kOiAvOy9cbiAgICAgIH1cbiAgICBdLFxuICAgIGtleXdvcmRzOiBDUFBfS0VZV09SRFMsXG4gICAgY29udGFpbnM6IEVYUFJFU1NJT05fQ09OVEFJTlMuY29uY2F0KFtcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC9cXCgvLFxuICAgICAgICBlbmQ6IC9cXCkvLFxuICAgICAgICBrZXl3b3JkczogQ1BQX0tFWVdPUkRTLFxuICAgICAgICBjb250YWluczogRVhQUkVTU0lPTl9DT05UQUlOUy5jb25jYXQoWyAnc2VsZicgXSksXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfVxuICAgIF0pLFxuICAgIHJlbGV2YW5jZTogMFxuICB9O1xuXG4gIGNvbnN0IEZVTkNUSU9OX0RFQ0xBUkFUSU9OID0ge1xuICAgIGNsYXNzTmFtZTogJ2Z1bmN0aW9uJyxcbiAgICBiZWdpbjogJygnICsgRlVOQ1RJT05fVFlQRV9SRSArICdbXFxcXComXFxcXHNdKykrJyArIEZVTkNUSU9OX1RJVExFLFxuICAgIHJldHVybkJlZ2luOiB0cnVlLFxuICAgIGVuZDogL1t7Oz1dLyxcbiAgICBleGNsdWRlRW5kOiB0cnVlLFxuICAgIGtleXdvcmRzOiBDUFBfS0VZV09SRFMsXG4gICAgaWxsZWdhbDogL1teXFx3XFxzXFwqJjo8Pi5dLyxcbiAgICBjb250YWluczogW1xuICAgICAgeyAvLyB0byBwcmV2ZW50IGl0IGZyb20gYmVpbmcgY29uZnVzZWQgYXMgdGhlIGZ1bmN0aW9uIHRpdGxlXG4gICAgICAgIGJlZ2luOiBERUNMVFlQRV9BVVRPX1JFLFxuICAgICAgICBrZXl3b3JkczogQ1BQX0tFWVdPUkRTLFxuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiBGVU5DVElPTl9USVRMRSxcbiAgICAgICAgcmV0dXJuQmVnaW46IHRydWUsXG4gICAgICAgIGNvbnRhaW5zOiBbIFRJVExFX01PREUgXSxcbiAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICB9LFxuICAgICAgLy8gbmVlZGVkIGJlY2F1c2Ugd2UgZG8gbm90IGhhdmUgbG9vay1iZWhpbmQgb24gdGhlIGJlbG93IHJ1bGVcbiAgICAgIC8vIHRvIHByZXZlbnQgaXQgZnJvbSBncmFiYmluZyB0aGUgZmluYWwgOiBpbiBhIDo6IHBhaXJcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC86Oi8sXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfSxcbiAgICAgIC8vIGluaXRpYWxpemVyc1xuICAgICAge1xuICAgICAgICBiZWdpbjogLzovLFxuICAgICAgICBlbmRzV2l0aFBhcmVudDogdHJ1ZSxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICBTVFJJTkdTLFxuICAgICAgICAgIE5VTUJFUlNcbiAgICAgICAgXVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAncGFyYW1zJyxcbiAgICAgICAgYmVnaW46IC9cXCgvLFxuICAgICAgICBlbmQ6IC9cXCkvLFxuICAgICAgICBrZXl3b3JkczogQ1BQX0tFWVdPUkRTLFxuICAgICAgICByZWxldmFuY2U6IDAsXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgQ19MSU5FX0NPTU1FTlRfTU9ERSxcbiAgICAgICAgICBobGpzLkNfQkxPQ0tfQ09NTUVOVF9NT0RFLFxuICAgICAgICAgIFNUUklOR1MsXG4gICAgICAgICAgTlVNQkVSUyxcbiAgICAgICAgICBDUFBfUFJJTUlUSVZFX1RZUEVTLFxuICAgICAgICAgIC8vIENvdW50IG1hdGNoaW5nIHBhcmVudGhlc2VzLlxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiAvXFwoLyxcbiAgICAgICAgICAgIGVuZDogL1xcKS8sXG4gICAgICAgICAgICBrZXl3b3JkczogQ1BQX0tFWVdPUkRTLFxuICAgICAgICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICAgICAgJ3NlbGYnLFxuICAgICAgICAgICAgICBDX0xJTkVfQ09NTUVOVF9NT0RFLFxuICAgICAgICAgICAgICBobGpzLkNfQkxPQ0tfQ09NTUVOVF9NT0RFLFxuICAgICAgICAgICAgICBTVFJJTkdTLFxuICAgICAgICAgICAgICBOVU1CRVJTLFxuICAgICAgICAgICAgICBDUFBfUFJJTUlUSVZFX1RZUEVTXG4gICAgICAgICAgICBdXG4gICAgICAgICAgfVxuICAgICAgICBdXG4gICAgICB9LFxuICAgICAgQ1BQX1BSSU1JVElWRV9UWVBFUyxcbiAgICAgIENfTElORV9DT01NRU5UX01PREUsXG4gICAgICBobGpzLkNfQkxPQ0tfQ09NTUVOVF9NT0RFLFxuICAgICAgUFJFUFJPQ0VTU09SXG4gICAgXVxuICB9O1xuXG4gIHJldHVybiB7XG4gICAgbmFtZTogJ0MrKycsXG4gICAgYWxpYXNlczogW1xuICAgICAgJ2NjJyxcbiAgICAgICdjKysnLFxuICAgICAgJ2grKycsXG4gICAgICAnaHBwJyxcbiAgICAgICdoaCcsXG4gICAgICAnaHh4JyxcbiAgICAgICdjeHgnXG4gICAgXSxcbiAgICBrZXl3b3JkczogQ1BQX0tFWVdPUkRTLFxuICAgIGlsbGVnYWw6ICc8LycsXG4gICAgY2xhc3NOYW1lQWxpYXNlczoge1xuICAgICAgXCJmdW5jdGlvbi5kaXNwYXRjaFwiOiBcImJ1aWx0X2luXCJcbiAgICB9LFxuICAgIGNvbnRhaW5zOiBbXS5jb25jYXQoXG4gICAgICBFWFBSRVNTSU9OX0NPTlRFWFQsXG4gICAgICBGVU5DVElPTl9ERUNMQVJBVElPTixcbiAgICAgIEZVTkNUSU9OX0RJU1BBVENILFxuICAgICAgRVhQUkVTU0lPTl9DT05UQUlOUyxcbiAgICAgIFtcbiAgICAgICAgUFJFUFJPQ0VTU09SLFxuICAgICAgICB7IC8vIGNvbnRhaW5lcnM6IGllLCBgdmVjdG9yIDxpbnQ+IHJvb21zICg5KTtgXG4gICAgICAgICAgYmVnaW46ICdcXFxcYihkZXF1ZXxsaXN0fHF1ZXVlfHByaW9yaXR5X3F1ZXVlfHBhaXJ8c3RhY2t8dmVjdG9yfG1hcHxzZXR8Yml0c2V0fG11bHRpc2V0fG11bHRpbWFwfHVub3JkZXJlZF9tYXB8dW5vcmRlcmVkX3NldHx1bm9yZGVyZWRfbXVsdGlzZXR8dW5vcmRlcmVkX211bHRpbWFwfGFycmF5KVxcXFxzKjwnLFxuICAgICAgICAgIGVuZDogJz4nLFxuICAgICAgICAgIGtleXdvcmRzOiBDUFBfS0VZV09SRFMsXG4gICAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICAgICdzZWxmJyxcbiAgICAgICAgICAgIENQUF9QUklNSVRJVkVfVFlQRVNcbiAgICAgICAgICBdXG4gICAgICAgIH0sXG4gICAgICAgIHtcbiAgICAgICAgICBiZWdpbjogaGxqcy5JREVOVF9SRSArICc6OicsXG4gICAgICAgICAga2V5d29yZHM6IENQUF9LRVlXT1JEU1xuICAgICAgICB9LFxuICAgICAgICB7XG4gICAgICAgICAgY2xhc3NOYW1lOiAnY2xhc3MnLFxuICAgICAgICAgIGJlZ2luS2V5d29yZHM6ICdlbnVtIGNsYXNzIHN0cnVjdCB1bmlvbicsXG4gICAgICAgICAgZW5kOiAvW3s7Ojw+PV0vLFxuICAgICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgICB7XG4gICAgICAgICAgICAgIGJlZ2luS2V5d29yZHM6IFwiZmluYWwgY2xhc3Mgc3RydWN0XCJcbiAgICAgICAgICAgIH0sXG4gICAgICAgICAgICBobGpzLlRJVExFX01PREVcbiAgICAgICAgICBdXG4gICAgICAgIH1cbiAgICAgIF0pLFxuICAgIGV4cG9ydHM6IHtcbiAgICAgIHByZXByb2Nlc3NvcjogUFJFUFJPQ0VTU09SLFxuICAgICAgc3RyaW5nczogU1RSSU5HUyxcbiAgICAgIGtleXdvcmRzOiBDUFBfS0VZV09SRFNcbiAgICB9XG4gIH07XG59XG5cbi8qXG5MYW5ndWFnZTogQy1saWtlIChkZXByZWNhdGVkLCB1c2UgQyBhbmQgQysrIGluc3RlYWQpXG5BdXRob3I6IEl2YW4gU2FnYWxhZXYgPG1hbmlhY0Bzb2Z0d2FyZW1hbmlhY3Mub3JnPlxuQ29udHJpYnV0b3JzOiBFdmdlbnkgU3RlcGFuaXNjaGV2IDxpbWJvbGtAZ21haWwuY29tPiwgWmF2ZW4gTXVyYWR5YW4gPG1lZ2FsaXZvaXRob3NAZ21haWwuY29tPiwgUm9lbCBEZWNrZXJzIDxhZG1pbkBjb2RpbmdjYXQubmw+LCBTYW0gV3UgPHNhbXNhbTIzMTBAZ21haWwuY29tPiwgSm9yZGkgUGV0aXQgPGpvcmRpLnBldGl0QGdtYWlsLmNvbT4sIFBpZXRlciBWYW50b3JyZSA8cGlldGVydmFudG9ycmVAZ21haWwuY29tPiwgR29vZ2xlIEluYy4gKERhdmlkIEJlbmphbWluKSA8ZGF2aWRiZW5AZ29vZ2xlLmNvbT5cbiovXG5cbi8qKiBAdHlwZSBMYW5ndWFnZUZuICovXG5mdW5jdGlvbiBjTGlrZShobGpzKSB7XG4gIGNvbnN0IGxhbmcgPSBjUGx1c1BsdXMoaGxqcyk7XG5cbiAgY29uc3QgQ19BTElBU0VTID0gW1xuICAgIFwiY1wiLFxuICAgIFwiaFwiXG4gIF07XG5cbiAgY29uc3QgQ1BQX0FMSUFTRVMgPSBbXG4gICAgJ2NjJyxcbiAgICAnYysrJyxcbiAgICAnaCsrJyxcbiAgICAnaHBwJyxcbiAgICAnaGgnLFxuICAgICdoeHgnLFxuICAgICdjeHgnXG4gIF07XG5cbiAgbGFuZy5kaXNhYmxlQXV0b2RldGVjdCA9IHRydWU7XG4gIGxhbmcuYWxpYXNlcyA9IFtdO1xuICAvLyBzdXBwb3J0IHVzZXJzIG9ubHkgbG9hZGluZyBjLWxpa2UgKGxlZ2FjeSlcbiAgaWYgKCFobGpzLmdldExhbmd1YWdlKFwiY1wiKSkgbGFuZy5hbGlhc2VzLnB1c2goLi4uQ19BTElBU0VTKTtcbiAgaWYgKCFobGpzLmdldExhbmd1YWdlKFwiY3BwXCIpKSBsYW5nLmFsaWFzZXMucHVzaCguLi5DUFBfQUxJQVNFUyk7XG5cbiAgLy8gaWYgYyBhbmQgY3BwIGFyZSBsb2FkZWQgYWZ0ZXIgdGhlbiB0aGV5IHdpbGwgcmVjbGFpbSB0aGVzZVxuICAvLyBhbGlhc2VzIGZvciB0aGVtc2VsdmVzXG5cbiAgcmV0dXJuIGxhbmc7XG59XG5cbm1vZHVsZS5leHBvcnRzID0gY0xpa2U7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=