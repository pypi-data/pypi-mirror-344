(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_ruby"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/ruby.js":
/*!***********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/ruby.js ***!
  \***********************************************************************************************/
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

/*
Language: Ruby
Description: Ruby is a dynamic, open source programming language with a focus on simplicity and productivity.
Website: https://www.ruby-lang.org/
Author: Anton Kovalyov <anton@kovalyov.net>
Contributors: Peter Leonov <gojpeg@yandex.ru>, Vasily Polovnyov <vast@whiteants.net>, Loren Segal <lsegal@soen.ca>, Pascal Hurni <phi@ruby-reactive.org>, Cedric Sohrauer <sohrauer@googlemail.com>
Category: common
*/

function ruby(hljs) {
  const RUBY_METHOD_RE = '([a-zA-Z_]\\w*[!?=]?|[-+~]@|<<|>>|=~|===?|<=>|[<>]=?|\\*\\*|[-/+%^&*~`|]|\\[\\]=?)';
  const RUBY_KEYWORDS = {
    keyword:
      'and then defined module in return redo if BEGIN retry end for self when ' +
      'next until do begin unless END rescue else break undef not super class case ' +
      'require yield alias while ensure elsif or include attr_reader attr_writer attr_accessor ' +
      '__FILE__',
    built_in: 'proc lambda',
    literal:
      'true false nil'
  };
  const YARDOCTAG = {
    className: 'doctag',
    begin: '@[A-Za-z]+'
  };
  const IRB_OBJECT = {
    begin: '#<',
    end: '>'
  };
  const COMMENT_MODES = [
    hljs.COMMENT(
      '#',
      '$',
      {
        contains: [ YARDOCTAG ]
      }
    ),
    hljs.COMMENT(
      '^=begin',
      '^=end',
      {
        contains: [ YARDOCTAG ],
        relevance: 10
      }
    ),
    hljs.COMMENT('^__END__', '\\n$')
  ];
  const SUBST = {
    className: 'subst',
    begin: /#\{/,
    end: /\}/,
    keywords: RUBY_KEYWORDS
  };
  const STRING = {
    className: 'string',
    contains: [
      hljs.BACKSLASH_ESCAPE,
      SUBST
    ],
    variants: [
      {
        begin: /'/,
        end: /'/
      },
      {
        begin: /"/,
        end: /"/
      },
      {
        begin: /`/,
        end: /`/
      },
      {
        begin: /%[qQwWx]?\(/,
        end: /\)/
      },
      {
        begin: /%[qQwWx]?\[/,
        end: /\]/
      },
      {
        begin: /%[qQwWx]?\{/,
        end: /\}/
      },
      {
        begin: /%[qQwWx]?</,
        end: />/
      },
      {
        begin: /%[qQwWx]?\//,
        end: /\//
      },
      {
        begin: /%[qQwWx]?%/,
        end: /%/
      },
      {
        begin: /%[qQwWx]?-/,
        end: /-/
      },
      {
        begin: /%[qQwWx]?\|/,
        end: /\|/
      },
      // in the following expressions, \B in the beginning suppresses recognition of ?-sequences
      // where ? is the last character of a preceding identifier, as in: `func?4`
      {
        begin: /\B\?(\\\d{1,3})/
      },
      {
        begin: /\B\?(\\x[A-Fa-f0-9]{1,2})/
      },
      {
        begin: /\B\?(\\u\{?[A-Fa-f0-9]{1,6}\}?)/
      },
      {
        begin: /\B\?(\\M-\\C-|\\M-\\c|\\c\\M-|\\M-|\\C-\\M-)[\x20-\x7e]/
      },
      {
        begin: /\B\?\\(c|C-)[\x20-\x7e]/
      },
      {
        begin: /\B\?\\?\S/
      },
      { // heredocs
        begin: /<<[-~]?'?(\w+)\n(?:[^\n]*\n)*?\s*\1\b/,
        returnBegin: true,
        contains: [
          {
            begin: /<<[-~]?'?/
          },
          hljs.END_SAME_AS_BEGIN({
            begin: /(\w+)/,
            end: /(\w+)/,
            contains: [
              hljs.BACKSLASH_ESCAPE,
              SUBST
            ]
          })
        ]
      }
    ]
  };

  // Ruby syntax is underdocumented, but this grammar seems to be accurate
  // as of version 2.7.2 (confirmed with (irb and `Ripper.sexp(...)`)
  // https://docs.ruby-lang.org/en/2.7.0/doc/syntax/literals_rdoc.html#label-Numbers
  const decimal = '[1-9](_?[0-9])*|0';
  const digits = '[0-9](_?[0-9])*';
  const NUMBER = {
    className: 'number',
    relevance: 0,
    variants: [
      // decimal integer/float, optionally exponential or rational, optionally imaginary
      {
        begin: `\\b(${decimal})(\\.(${digits}))?([eE][+-]?(${digits})|r)?i?\\b`
      },

      // explicit decimal/binary/octal/hexadecimal integer,
      // optionally rational and/or imaginary
      {
        begin: "\\b0[dD][0-9](_?[0-9])*r?i?\\b"
      },
      {
        begin: "\\b0[bB][0-1](_?[0-1])*r?i?\\b"
      },
      {
        begin: "\\b0[oO][0-7](_?[0-7])*r?i?\\b"
      },
      {
        begin: "\\b0[xX][0-9a-fA-F](_?[0-9a-fA-F])*r?i?\\b"
      },

      // 0-prefixed implicit octal integer, optionally rational and/or imaginary
      {
        begin: "\\b0(_?[0-7])+r?i?\\b"
      }
    ]
  };

  const PARAMS = {
    className: 'params',
    begin: '\\(',
    end: '\\)',
    endsParent: true,
    keywords: RUBY_KEYWORDS
  };

  const RUBY_DEFAULT_CONTAINS = [
    STRING,
    {
      className: 'class',
      beginKeywords: 'class module',
      end: '$|;',
      illegal: /=/,
      contains: [
        hljs.inherit(hljs.TITLE_MODE, {
          begin: '[A-Za-z_]\\w*(::\\w+)*(\\?|!)?'
        }),
        {
          begin: '<\\s*',
          contains: [
            {
              begin: '(' + hljs.IDENT_RE + '::)?' + hljs.IDENT_RE,
              // we already get points for <, we don't need poitns
              // for the name also
              relevance: 0
            }
          ]
        }
      ].concat(COMMENT_MODES)
    },
    {
      className: 'function',
      // def method_name(
      // def method_name;
      // def method_name (end of line)
      begin: concat(/def\s+/, lookahead(RUBY_METHOD_RE + "\\s*(\\(|;|$)")),
      relevance: 0, // relevance comes from kewords
      keywords: "def",
      end: '$|;',
      contains: [
        hljs.inherit(hljs.TITLE_MODE, {
          begin: RUBY_METHOD_RE
        }),
        PARAMS
      ].concat(COMMENT_MODES)
    },
    {
      // swallow namespace qualifiers before symbols
      begin: hljs.IDENT_RE + '::'
    },
    {
      className: 'symbol',
      begin: hljs.UNDERSCORE_IDENT_RE + '(!|\\?)?:',
      relevance: 0
    },
    {
      className: 'symbol',
      begin: ':(?!\\s)',
      contains: [
        STRING,
        {
          begin: RUBY_METHOD_RE
        }
      ],
      relevance: 0
    },
    NUMBER,
    {
      // negative-look forward attemps to prevent false matches like:
      // @ident@ or $ident$ that might indicate this is not ruby at all
      className: "variable",
      begin: '(\\$\\W)|((\\$|@@?)(\\w+))(?=[^@$?])' + `(?![A-Za-z])(?![@$?'])`
    },
    {
      className: 'params',
      begin: /\|/,
      end: /\|/,
      relevance: 0, // this could be a lot of things (in other languages) other than params
      keywords: RUBY_KEYWORDS
    },
    { // regexp container
      begin: '(' + hljs.RE_STARTERS_RE + '|unless)\\s*',
      keywords: 'unless',
      contains: [
        {
          className: 'regexp',
          contains: [
            hljs.BACKSLASH_ESCAPE,
            SUBST
          ],
          illegal: /\n/,
          variants: [
            {
              begin: '/',
              end: '/[a-z]*'
            },
            {
              begin: /%r\{/,
              end: /\}[a-z]*/
            },
            {
              begin: '%r\\(',
              end: '\\)[a-z]*'
            },
            {
              begin: '%r!',
              end: '![a-z]*'
            },
            {
              begin: '%r\\[',
              end: '\\][a-z]*'
            }
          ]
        }
      ].concat(IRB_OBJECT, COMMENT_MODES),
      relevance: 0
    }
  ].concat(IRB_OBJECT, COMMENT_MODES);

  SUBST.contains = RUBY_DEFAULT_CONTAINS;
  PARAMS.contains = RUBY_DEFAULT_CONTAINS;

  // >>
  // ?>
  const SIMPLE_PROMPT = "[>?]>";
  // irb(main):001:0>
  const DEFAULT_PROMPT = "[\\w#]+\\(\\w+\\):\\d+:\\d+>";
  const RVM_PROMPT = "(\\w+-)?\\d+\\.\\d+\\.\\d+(p\\d+)?[^\\d][^>]+>";

  const IRB_DEFAULT = [
    {
      begin: /^\s*=>/,
      starts: {
        end: '$',
        contains: RUBY_DEFAULT_CONTAINS
      }
    },
    {
      className: 'meta',
      begin: '^(' + SIMPLE_PROMPT + "|" + DEFAULT_PROMPT + '|' + RVM_PROMPT + ')(?=[ ])',
      starts: {
        end: '$',
        contains: RUBY_DEFAULT_CONTAINS
      }
    }
  ];

  COMMENT_MODES.unshift(IRB_OBJECT);

  return {
    name: 'Ruby',
    aliases: [
      'rb',
      'gemspec',
      'podspec',
      'thor',
      'irb'
    ],
    keywords: RUBY_KEYWORDS,
    illegal: /\/\*/,
    contains: [
      hljs.SHEBANG({
        binary: "ruby"
      })
    ]
      .concat(IRB_DEFAULT)
      .concat(COMMENT_MODES)
      .concat(RUBY_DEFAULT_CONTAINS)
  };
}

module.exports = ruby;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfcnVieS5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBLFdBQVcsUUFBUTtBQUNuQixhQUFhO0FBQ2I7O0FBRUE7QUFDQSxXQUFXLGtCQUFrQjtBQUM3QixhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTs7QUFFQTtBQUNBLFdBQVcsa0JBQWtCO0FBQzdCLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBLFdBQVcsdUJBQXVCO0FBQ2xDLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxlQUFlO0FBQ2YsWUFBWTtBQUNaO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQSwyQkFBMkI7QUFDM0IsZ0JBQWdCO0FBQ2hCLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLDBCQUEwQixJQUFJO0FBQzlCLE9BQU87QUFDUDtBQUNBLG9DQUFvQyxJQUFJO0FBQ3hDLE9BQU87QUFDUDtBQUNBLDBCQUEwQixhQUFhLElBQUksRUFBRTtBQUM3QyxPQUFPO0FBQ1A7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQSxPQUFPO0FBQ1AsUUFBUTtBQUNSO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLHNCQUFzQixRQUFRLFFBQVEsT0FBTyxnQkFBZ0IsT0FBTztBQUNwRSxPQUFPOztBQUVQO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0EsT0FBTzs7QUFFUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLGVBQWU7QUFDZjtBQUNBO0FBQ0E7QUFDQTtBQUNBLFNBQVM7QUFDVDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLG9FQUFvRTtBQUNwRTtBQUNBO0FBQ0EsZUFBZTtBQUNmO0FBQ0E7QUFDQTtBQUNBLFNBQVM7QUFDVDtBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMLE1BQU07QUFDTjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsYUFBYTtBQUNiO0FBQ0EsMEJBQTBCO0FBQzFCLHNCQUFzQjtBQUN0QixhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0EsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL3J1YnkuanMiXSwic291cmNlc0NvbnRlbnQiOlsiLyoqXG4gKiBAcGFyYW0ge3N0cmluZ30gdmFsdWVcbiAqIEByZXR1cm5zIHtSZWdFeHB9XG4gKiAqL1xuXG4vKipcbiAqIEBwYXJhbSB7UmVnRXhwIHwgc3RyaW5nIH0gcmVcbiAqIEByZXR1cm5zIHtzdHJpbmd9XG4gKi9cbmZ1bmN0aW9uIHNvdXJjZShyZSkge1xuICBpZiAoIXJlKSByZXR1cm4gbnVsbDtcbiAgaWYgKHR5cGVvZiByZSA9PT0gXCJzdHJpbmdcIikgcmV0dXJuIHJlO1xuXG4gIHJldHVybiByZS5zb3VyY2U7XG59XG5cbi8qKlxuICogQHBhcmFtIHtSZWdFeHAgfCBzdHJpbmcgfSByZVxuICogQHJldHVybnMge3N0cmluZ31cbiAqL1xuZnVuY3Rpb24gbG9va2FoZWFkKHJlKSB7XG4gIHJldHVybiBjb25jYXQoJyg/PScsIHJlLCAnKScpO1xufVxuXG4vKipcbiAqIEBwYXJhbSB7Li4uKFJlZ0V4cCB8IHN0cmluZykgfSBhcmdzXG4gKiBAcmV0dXJucyB7c3RyaW5nfVxuICovXG5mdW5jdGlvbiBjb25jYXQoLi4uYXJncykge1xuICBjb25zdCBqb2luZWQgPSBhcmdzLm1hcCgoeCkgPT4gc291cmNlKHgpKS5qb2luKFwiXCIpO1xuICByZXR1cm4gam9pbmVkO1xufVxuXG4vKlxuTGFuZ3VhZ2U6IFJ1YnlcbkRlc2NyaXB0aW9uOiBSdWJ5IGlzIGEgZHluYW1pYywgb3BlbiBzb3VyY2UgcHJvZ3JhbW1pbmcgbGFuZ3VhZ2Ugd2l0aCBhIGZvY3VzIG9uIHNpbXBsaWNpdHkgYW5kIHByb2R1Y3Rpdml0eS5cbldlYnNpdGU6IGh0dHBzOi8vd3d3LnJ1YnktbGFuZy5vcmcvXG5BdXRob3I6IEFudG9uIEtvdmFseW92IDxhbnRvbkBrb3ZhbHlvdi5uZXQ+XG5Db250cmlidXRvcnM6IFBldGVyIExlb25vdiA8Z29qcGVnQHlhbmRleC5ydT4sIFZhc2lseSBQb2xvdm55b3YgPHZhc3RAd2hpdGVhbnRzLm5ldD4sIExvcmVuIFNlZ2FsIDxsc2VnYWxAc29lbi5jYT4sIFBhc2NhbCBIdXJuaSA8cGhpQHJ1YnktcmVhY3RpdmUub3JnPiwgQ2VkcmljIFNvaHJhdWVyIDxzb2hyYXVlckBnb29nbGVtYWlsLmNvbT5cbkNhdGVnb3J5OiBjb21tb25cbiovXG5cbmZ1bmN0aW9uIHJ1YnkoaGxqcykge1xuICBjb25zdCBSVUJZX01FVEhPRF9SRSA9ICcoW2EtekEtWl9dXFxcXHcqWyE/PV0/fFstK35dQHw8PHw+Pnw9fnw9PT0/fDw9PnxbPD5dPT98XFxcXCpcXFxcKnxbLS8rJV4mKn5gfF18XFxcXFtcXFxcXT0/KSc7XG4gIGNvbnN0IFJVQllfS0VZV09SRFMgPSB7XG4gICAga2V5d29yZDpcbiAgICAgICdhbmQgdGhlbiBkZWZpbmVkIG1vZHVsZSBpbiByZXR1cm4gcmVkbyBpZiBCRUdJTiByZXRyeSBlbmQgZm9yIHNlbGYgd2hlbiAnICtcbiAgICAgICduZXh0IHVudGlsIGRvIGJlZ2luIHVubGVzcyBFTkQgcmVzY3VlIGVsc2UgYnJlYWsgdW5kZWYgbm90IHN1cGVyIGNsYXNzIGNhc2UgJyArXG4gICAgICAncmVxdWlyZSB5aWVsZCBhbGlhcyB3aGlsZSBlbnN1cmUgZWxzaWYgb3IgaW5jbHVkZSBhdHRyX3JlYWRlciBhdHRyX3dyaXRlciBhdHRyX2FjY2Vzc29yICcgK1xuICAgICAgJ19fRklMRV9fJyxcbiAgICBidWlsdF9pbjogJ3Byb2MgbGFtYmRhJyxcbiAgICBsaXRlcmFsOlxuICAgICAgJ3RydWUgZmFsc2UgbmlsJ1xuICB9O1xuICBjb25zdCBZQVJET0NUQUcgPSB7XG4gICAgY2xhc3NOYW1lOiAnZG9jdGFnJyxcbiAgICBiZWdpbjogJ0BbQS1aYS16XSsnXG4gIH07XG4gIGNvbnN0IElSQl9PQkpFQ1QgPSB7XG4gICAgYmVnaW46ICcjPCcsXG4gICAgZW5kOiAnPidcbiAgfTtcbiAgY29uc3QgQ09NTUVOVF9NT0RFUyA9IFtcbiAgICBobGpzLkNPTU1FTlQoXG4gICAgICAnIycsXG4gICAgICAnJCcsXG4gICAgICB7XG4gICAgICAgIGNvbnRhaW5zOiBbIFlBUkRPQ1RBRyBdXG4gICAgICB9XG4gICAgKSxcbiAgICBobGpzLkNPTU1FTlQoXG4gICAgICAnXj1iZWdpbicsXG4gICAgICAnXj1lbmQnLFxuICAgICAge1xuICAgICAgICBjb250YWluczogWyBZQVJET0NUQUcgXSxcbiAgICAgICAgcmVsZXZhbmNlOiAxMFxuICAgICAgfVxuICAgICksXG4gICAgaGxqcy5DT01NRU5UKCdeX19FTkRfXycsICdcXFxcbiQnKVxuICBdO1xuICBjb25zdCBTVUJTVCA9IHtcbiAgICBjbGFzc05hbWU6ICdzdWJzdCcsXG4gICAgYmVnaW46IC8jXFx7LyxcbiAgICBlbmQ6IC9cXH0vLFxuICAgIGtleXdvcmRzOiBSVUJZX0tFWVdPUkRTXG4gIH07XG4gIGNvbnN0IFNUUklORyA9IHtcbiAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBobGpzLkJBQ0tTTEFTSF9FU0NBUEUsXG4gICAgICBTVUJTVFxuICAgIF0sXG4gICAgdmFyaWFudHM6IFtcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC8nLyxcbiAgICAgICAgZW5kOiAvJy9cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAvXCIvLFxuICAgICAgICBlbmQ6IC9cIi9cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAvYC8sXG4gICAgICAgIGVuZDogL2AvXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogLyVbcVF3V3hdP1xcKC8sXG4gICAgICAgIGVuZDogL1xcKS9cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAvJVtxUXdXeF0/XFxbLyxcbiAgICAgICAgZW5kOiAvXFxdL1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC8lW3FRd1d4XT9cXHsvLFxuICAgICAgICBlbmQ6IC9cXH0vXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogLyVbcVF3V3hdPzwvLFxuICAgICAgICBlbmQ6IC8+L1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC8lW3FRd1d4XT9cXC8vLFxuICAgICAgICBlbmQ6IC9cXC8vXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogLyVbcVF3V3hdPyUvLFxuICAgICAgICBlbmQ6IC8lL1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC8lW3FRd1d4XT8tLyxcbiAgICAgICAgZW5kOiAvLS9cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAvJVtxUXdXeF0/XFx8LyxcbiAgICAgICAgZW5kOiAvXFx8L1xuICAgICAgfSxcbiAgICAgIC8vIGluIHRoZSBmb2xsb3dpbmcgZXhwcmVzc2lvbnMsIFxcQiBpbiB0aGUgYmVnaW5uaW5nIHN1cHByZXNzZXMgcmVjb2duaXRpb24gb2YgPy1zZXF1ZW5jZXNcbiAgICAgIC8vIHdoZXJlID8gaXMgdGhlIGxhc3QgY2hhcmFjdGVyIG9mIGEgcHJlY2VkaW5nIGlkZW50aWZpZXIsIGFzIGluOiBgZnVuYz80YFxuICAgICAge1xuICAgICAgICBiZWdpbjogL1xcQlxcPyhcXFxcXFxkezEsM30pL1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC9cXEJcXD8oXFxcXHhbQS1GYS1mMC05XXsxLDJ9KS9cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAvXFxCXFw/KFxcXFx1XFx7P1tBLUZhLWYwLTldezEsNn1cXH0/KS9cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAvXFxCXFw/KFxcXFxNLVxcXFxDLXxcXFxcTS1cXFxcY3xcXFxcY1xcXFxNLXxcXFxcTS18XFxcXEMtXFxcXE0tKVtcXHgyMC1cXHg3ZV0vXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogL1xcQlxcP1xcXFwoY3xDLSlbXFx4MjAtXFx4N2VdL1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC9cXEJcXD9cXFxcP1xcUy9cbiAgICAgIH0sXG4gICAgICB7IC8vIGhlcmVkb2NzXG4gICAgICAgIGJlZ2luOiAvPDxbLX5dPyc/KFxcdyspXFxuKD86W15cXG5dKlxcbikqP1xccypcXDFcXGIvLFxuICAgICAgICByZXR1cm5CZWdpbjogdHJ1ZSxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbjogLzw8Wy1+XT8nPy9cbiAgICAgICAgICB9LFxuICAgICAgICAgIGhsanMuRU5EX1NBTUVfQVNfQkVHSU4oe1xuICAgICAgICAgICAgYmVnaW46IC8oXFx3KykvLFxuICAgICAgICAgICAgZW5kOiAvKFxcdyspLyxcbiAgICAgICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgICAgIGhsanMuQkFDS1NMQVNIX0VTQ0FQRSxcbiAgICAgICAgICAgICAgU1VCU1RcbiAgICAgICAgICAgIF1cbiAgICAgICAgICB9KVxuICAgICAgICBdXG4gICAgICB9XG4gICAgXVxuICB9O1xuXG4gIC8vIFJ1Ynkgc3ludGF4IGlzIHVuZGVyZG9jdW1lbnRlZCwgYnV0IHRoaXMgZ3JhbW1hciBzZWVtcyB0byBiZSBhY2N1cmF0ZVxuICAvLyBhcyBvZiB2ZXJzaW9uIDIuNy4yIChjb25maXJtZWQgd2l0aCAoaXJiIGFuZCBgUmlwcGVyLnNleHAoLi4uKWApXG4gIC8vIGh0dHBzOi8vZG9jcy5ydWJ5LWxhbmcub3JnL2VuLzIuNy4wL2RvYy9zeW50YXgvbGl0ZXJhbHNfcmRvYy5odG1sI2xhYmVsLU51bWJlcnNcbiAgY29uc3QgZGVjaW1hbCA9ICdbMS05XShfP1swLTldKSp8MCc7XG4gIGNvbnN0IGRpZ2l0cyA9ICdbMC05XShfP1swLTldKSonO1xuICBjb25zdCBOVU1CRVIgPSB7XG4gICAgY2xhc3NOYW1lOiAnbnVtYmVyJyxcbiAgICByZWxldmFuY2U6IDAsXG4gICAgdmFyaWFudHM6IFtcbiAgICAgIC8vIGRlY2ltYWwgaW50ZWdlci9mbG9hdCwgb3B0aW9uYWxseSBleHBvbmVudGlhbCBvciByYXRpb25hbCwgb3B0aW9uYWxseSBpbWFnaW5hcnlcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IGBcXFxcYigke2RlY2ltYWx9KShcXFxcLigke2RpZ2l0c30pKT8oW2VFXVsrLV0/KCR7ZGlnaXRzfSl8cik/aT9cXFxcYmBcbiAgICAgIH0sXG5cbiAgICAgIC8vIGV4cGxpY2l0IGRlY2ltYWwvYmluYXJ5L29jdGFsL2hleGFkZWNpbWFsIGludGVnZXIsXG4gICAgICAvLyBvcHRpb25hbGx5IHJhdGlvbmFsIGFuZC9vciBpbWFnaW5hcnlcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IFwiXFxcXGIwW2REXVswLTldKF8/WzAtOV0pKnI/aT9cXFxcYlwiXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogXCJcXFxcYjBbYkJdWzAtMV0oXz9bMC0xXSkqcj9pP1xcXFxiXCJcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiBcIlxcXFxiMFtvT11bMC03XShfP1swLTddKSpyP2k/XFxcXGJcIlxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IFwiXFxcXGIwW3hYXVswLTlhLWZBLUZdKF8/WzAtOWEtZkEtRl0pKnI/aT9cXFxcYlwiXG4gICAgICB9LFxuXG4gICAgICAvLyAwLXByZWZpeGVkIGltcGxpY2l0IG9jdGFsIGludGVnZXIsIG9wdGlvbmFsbHkgcmF0aW9uYWwgYW5kL29yIGltYWdpbmFyeVxuICAgICAge1xuICAgICAgICBiZWdpbjogXCJcXFxcYjAoXz9bMC03XSkrcj9pP1xcXFxiXCJcbiAgICAgIH1cbiAgICBdXG4gIH07XG5cbiAgY29uc3QgUEFSQU1TID0ge1xuICAgIGNsYXNzTmFtZTogJ3BhcmFtcycsXG4gICAgYmVnaW46ICdcXFxcKCcsXG4gICAgZW5kOiAnXFxcXCknLFxuICAgIGVuZHNQYXJlbnQ6IHRydWUsXG4gICAga2V5d29yZHM6IFJVQllfS0VZV09SRFNcbiAgfTtcblxuICBjb25zdCBSVUJZX0RFRkFVTFRfQ09OVEFJTlMgPSBbXG4gICAgU1RSSU5HLFxuICAgIHtcbiAgICAgIGNsYXNzTmFtZTogJ2NsYXNzJyxcbiAgICAgIGJlZ2luS2V5d29yZHM6ICdjbGFzcyBtb2R1bGUnLFxuICAgICAgZW5kOiAnJHw7JyxcbiAgICAgIGlsbGVnYWw6IC89LyxcbiAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgIGhsanMuaW5oZXJpdChobGpzLlRJVExFX01PREUsIHtcbiAgICAgICAgICBiZWdpbjogJ1tBLVphLXpfXVxcXFx3Kig6OlxcXFx3KykqKFxcXFw/fCEpPydcbiAgICAgICAgfSksXG4gICAgICAgIHtcbiAgICAgICAgICBiZWdpbjogJzxcXFxccyonLFxuICAgICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgICB7XG4gICAgICAgICAgICAgIGJlZ2luOiAnKCcgKyBobGpzLklERU5UX1JFICsgJzo6KT8nICsgaGxqcy5JREVOVF9SRSxcbiAgICAgICAgICAgICAgLy8gd2UgYWxyZWFkeSBnZXQgcG9pbnRzIGZvciA8LCB3ZSBkb24ndCBuZWVkIHBvaXRuc1xuICAgICAgICAgICAgICAvLyBmb3IgdGhlIG5hbWUgYWxzb1xuICAgICAgICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgICAgICAgIH1cbiAgICAgICAgICBdXG4gICAgICAgIH1cbiAgICAgIF0uY29uY2F0KENPTU1FTlRfTU9ERVMpXG4gICAgfSxcbiAgICB7XG4gICAgICBjbGFzc05hbWU6ICdmdW5jdGlvbicsXG4gICAgICAvLyBkZWYgbWV0aG9kX25hbWUoXG4gICAgICAvLyBkZWYgbWV0aG9kX25hbWU7XG4gICAgICAvLyBkZWYgbWV0aG9kX25hbWUgKGVuZCBvZiBsaW5lKVxuICAgICAgYmVnaW46IGNvbmNhdCgvZGVmXFxzKy8sIGxvb2thaGVhZChSVUJZX01FVEhPRF9SRSArIFwiXFxcXHMqKFxcXFwofDt8JClcIikpLFxuICAgICAgcmVsZXZhbmNlOiAwLCAvLyByZWxldmFuY2UgY29tZXMgZnJvbSBrZXdvcmRzXG4gICAgICBrZXl3b3JkczogXCJkZWZcIixcbiAgICAgIGVuZDogJyR8OycsXG4gICAgICBjb250YWluczogW1xuICAgICAgICBobGpzLmluaGVyaXQoaGxqcy5USVRMRV9NT0RFLCB7XG4gICAgICAgICAgYmVnaW46IFJVQllfTUVUSE9EX1JFXG4gICAgICAgIH0pLFxuICAgICAgICBQQVJBTVNcbiAgICAgIF0uY29uY2F0KENPTU1FTlRfTU9ERVMpXG4gICAgfSxcbiAgICB7XG4gICAgICAvLyBzd2FsbG93IG5hbWVzcGFjZSBxdWFsaWZpZXJzIGJlZm9yZSBzeW1ib2xzXG4gICAgICBiZWdpbjogaGxqcy5JREVOVF9SRSArICc6OidcbiAgICB9LFxuICAgIHtcbiAgICAgIGNsYXNzTmFtZTogJ3N5bWJvbCcsXG4gICAgICBiZWdpbjogaGxqcy5VTkRFUlNDT1JFX0lERU5UX1JFICsgJyghfFxcXFw/KT86JyxcbiAgICAgIHJlbGV2YW5jZTogMFxuICAgIH0sXG4gICAge1xuICAgICAgY2xhc3NOYW1lOiAnc3ltYm9sJyxcbiAgICAgIGJlZ2luOiAnOig/IVxcXFxzKScsXG4gICAgICBjb250YWluczogW1xuICAgICAgICBTVFJJTkcsXG4gICAgICAgIHtcbiAgICAgICAgICBiZWdpbjogUlVCWV9NRVRIT0RfUkVcbiAgICAgICAgfVxuICAgICAgXSxcbiAgICAgIHJlbGV2YW5jZTogMFxuICAgIH0sXG4gICAgTlVNQkVSLFxuICAgIHtcbiAgICAgIC8vIG5lZ2F0aXZlLWxvb2sgZm9yd2FyZCBhdHRlbXBzIHRvIHByZXZlbnQgZmFsc2UgbWF0Y2hlcyBsaWtlOlxuICAgICAgLy8gQGlkZW50QCBvciAkaWRlbnQkIHRoYXQgbWlnaHQgaW5kaWNhdGUgdGhpcyBpcyBub3QgcnVieSBhdCBhbGxcbiAgICAgIGNsYXNzTmFtZTogXCJ2YXJpYWJsZVwiLFxuICAgICAgYmVnaW46ICcoXFxcXCRcXFxcVyl8KChcXFxcJHxAQD8pKFxcXFx3KykpKD89W15AJD9dKScgKyBgKD8hW0EtWmEtel0pKD8hW0AkPyddKWBcbiAgICB9LFxuICAgIHtcbiAgICAgIGNsYXNzTmFtZTogJ3BhcmFtcycsXG4gICAgICBiZWdpbjogL1xcfC8sXG4gICAgICBlbmQ6IC9cXHwvLFxuICAgICAgcmVsZXZhbmNlOiAwLCAvLyB0aGlzIGNvdWxkIGJlIGEgbG90IG9mIHRoaW5ncyAoaW4gb3RoZXIgbGFuZ3VhZ2VzKSBvdGhlciB0aGFuIHBhcmFtc1xuICAgICAga2V5d29yZHM6IFJVQllfS0VZV09SRFNcbiAgICB9LFxuICAgIHsgLy8gcmVnZXhwIGNvbnRhaW5lclxuICAgICAgYmVnaW46ICcoJyArIGhsanMuUkVfU1RBUlRFUlNfUkUgKyAnfHVubGVzcylcXFxccyonLFxuICAgICAga2V5d29yZHM6ICd1bmxlc3MnLFxuICAgICAgY29udGFpbnM6IFtcbiAgICAgICAge1xuICAgICAgICAgIGNsYXNzTmFtZTogJ3JlZ2V4cCcsXG4gICAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICAgIGhsanMuQkFDS1NMQVNIX0VTQ0FQRSxcbiAgICAgICAgICAgIFNVQlNUXG4gICAgICAgICAgXSxcbiAgICAgICAgICBpbGxlZ2FsOiAvXFxuLyxcbiAgICAgICAgICB2YXJpYW50czogW1xuICAgICAgICAgICAge1xuICAgICAgICAgICAgICBiZWdpbjogJy8nLFxuICAgICAgICAgICAgICBlbmQ6ICcvW2Etel0qJ1xuICAgICAgICAgICAgfSxcbiAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgYmVnaW46IC8lclxcey8sXG4gICAgICAgICAgICAgIGVuZDogL1xcfVthLXpdKi9cbiAgICAgICAgICAgIH0sXG4gICAgICAgICAgICB7XG4gICAgICAgICAgICAgIGJlZ2luOiAnJXJcXFxcKCcsXG4gICAgICAgICAgICAgIGVuZDogJ1xcXFwpW2Etel0qJ1xuICAgICAgICAgICAgfSxcbiAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgYmVnaW46ICclciEnLFxuICAgICAgICAgICAgICBlbmQ6ICchW2Etel0qJ1xuICAgICAgICAgICAgfSxcbiAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgYmVnaW46ICclclxcXFxbJyxcbiAgICAgICAgICAgICAgZW5kOiAnXFxcXF1bYS16XSonXG4gICAgICAgICAgICB9XG4gICAgICAgICAgXVxuICAgICAgICB9XG4gICAgICBdLmNvbmNhdChJUkJfT0JKRUNULCBDT01NRU5UX01PREVTKSxcbiAgICAgIHJlbGV2YW5jZTogMFxuICAgIH1cbiAgXS5jb25jYXQoSVJCX09CSkVDVCwgQ09NTUVOVF9NT0RFUyk7XG5cbiAgU1VCU1QuY29udGFpbnMgPSBSVUJZX0RFRkFVTFRfQ09OVEFJTlM7XG4gIFBBUkFNUy5jb250YWlucyA9IFJVQllfREVGQVVMVF9DT05UQUlOUztcblxuICAvLyA+PlxuICAvLyA/PlxuICBjb25zdCBTSU1QTEVfUFJPTVBUID0gXCJbPj9dPlwiO1xuICAvLyBpcmIobWFpbik6MDAxOjA+XG4gIGNvbnN0IERFRkFVTFRfUFJPTVBUID0gXCJbXFxcXHcjXStcXFxcKFxcXFx3K1xcXFwpOlxcXFxkKzpcXFxcZCs+XCI7XG4gIGNvbnN0IFJWTV9QUk9NUFQgPSBcIihcXFxcdystKT9cXFxcZCtcXFxcLlxcXFxkK1xcXFwuXFxcXGQrKHBcXFxcZCspP1teXFxcXGRdW14+XSs+XCI7XG5cbiAgY29uc3QgSVJCX0RFRkFVTFQgPSBbXG4gICAge1xuICAgICAgYmVnaW46IC9eXFxzKj0+LyxcbiAgICAgIHN0YXJ0czoge1xuICAgICAgICBlbmQ6ICckJyxcbiAgICAgICAgY29udGFpbnM6IFJVQllfREVGQVVMVF9DT05UQUlOU1xuICAgICAgfVxuICAgIH0sXG4gICAge1xuICAgICAgY2xhc3NOYW1lOiAnbWV0YScsXG4gICAgICBiZWdpbjogJ14oJyArIFNJTVBMRV9QUk9NUFQgKyBcInxcIiArIERFRkFVTFRfUFJPTVBUICsgJ3wnICsgUlZNX1BST01QVCArICcpKD89WyBdKScsXG4gICAgICBzdGFydHM6IHtcbiAgICAgICAgZW5kOiAnJCcsXG4gICAgICAgIGNvbnRhaW5zOiBSVUJZX0RFRkFVTFRfQ09OVEFJTlNcbiAgICAgIH1cbiAgICB9XG4gIF07XG5cbiAgQ09NTUVOVF9NT0RFUy51bnNoaWZ0KElSQl9PQkpFQ1QpO1xuXG4gIHJldHVybiB7XG4gICAgbmFtZTogJ1J1YnknLFxuICAgIGFsaWFzZXM6IFtcbiAgICAgICdyYicsXG4gICAgICAnZ2Vtc3BlYycsXG4gICAgICAncG9kc3BlYycsXG4gICAgICAndGhvcicsXG4gICAgICAnaXJiJ1xuICAgIF0sXG4gICAga2V5d29yZHM6IFJVQllfS0VZV09SRFMsXG4gICAgaWxsZWdhbDogL1xcL1xcKi8sXG4gICAgY29udGFpbnM6IFtcbiAgICAgIGhsanMuU0hFQkFORyh7XG4gICAgICAgIGJpbmFyeTogXCJydWJ5XCJcbiAgICAgIH0pXG4gICAgXVxuICAgICAgLmNvbmNhdChJUkJfREVGQVVMVClcbiAgICAgIC5jb25jYXQoQ09NTUVOVF9NT0RFUylcbiAgICAgIC5jb25jYXQoUlVCWV9ERUZBVUxUX0NPTlRBSU5TKVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IHJ1Ynk7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=