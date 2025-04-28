(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_csharp"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/csharp.js":
/*!*************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/csharp.js ***!
  \*************************************************************************************************/
/***/ ((module) => {

/*
Language: C#
Author: Jason Diamond <jason@diamond.name>
Contributor: Nicolas LLOBERA <nllobera@gmail.com>, Pieter Vantorre <pietervantorre@gmail.com>, David Pine <david.pine@microsoft.com>
Website: https://docs.microsoft.com/en-us/dotnet/csharp/
Category: common
*/

/** @type LanguageFn */
function csharp(hljs) {
  const BUILT_IN_KEYWORDS = [
    'bool',
    'byte',
    'char',
    'decimal',
    'delegate',
    'double',
    'dynamic',
    'enum',
    'float',
    'int',
    'long',
    'nint',
    'nuint',
    'object',
    'sbyte',
    'short',
    'string',
    'ulong',
    'uint',
    'ushort'
  ];
  const FUNCTION_MODIFIERS = [
    'public',
    'private',
    'protected',
    'static',
    'internal',
    'protected',
    'abstract',
    'async',
    'extern',
    'override',
    'unsafe',
    'virtual',
    'new',
    'sealed',
    'partial'
  ];
  const LITERAL_KEYWORDS = [
    'default',
    'false',
    'null',
    'true'
  ];
  const NORMAL_KEYWORDS = [
    'abstract',
    'as',
    'base',
    'break',
    'case',
    'class',
    'const',
    'continue',
    'do',
    'else',
    'event',
    'explicit',
    'extern',
    'finally',
    'fixed',
    'for',
    'foreach',
    'goto',
    'if',
    'implicit',
    'in',
    'interface',
    'internal',
    'is',
    'lock',
    'namespace',
    'new',
    'operator',
    'out',
    'override',
    'params',
    'private',
    'protected',
    'public',
    'readonly',
    'record',
    'ref',
    'return',
    'sealed',
    'sizeof',
    'stackalloc',
    'static',
    'struct',
    'switch',
    'this',
    'throw',
    'try',
    'typeof',
    'unchecked',
    'unsafe',
    'using',
    'virtual',
    'void',
    'volatile',
    'while'
  ];
  const CONTEXTUAL_KEYWORDS = [
    'add',
    'alias',
    'and',
    'ascending',
    'async',
    'await',
    'by',
    'descending',
    'equals',
    'from',
    'get',
    'global',
    'group',
    'init',
    'into',
    'join',
    'let',
    'nameof',
    'not',
    'notnull',
    'on',
    'or',
    'orderby',
    'partial',
    'remove',
    'select',
    'set',
    'unmanaged',
    'value|0',
    'var',
    'when',
    'where',
    'with',
    'yield'
  ];

  const KEYWORDS = {
    keyword: NORMAL_KEYWORDS.concat(CONTEXTUAL_KEYWORDS),
    built_in: BUILT_IN_KEYWORDS,
    literal: LITERAL_KEYWORDS
  };
  const TITLE_MODE = hljs.inherit(hljs.TITLE_MODE, {
    begin: '[a-zA-Z](\\.?\\w)*'
  });
  const NUMBERS = {
    className: 'number',
    variants: [
      {
        begin: '\\b(0b[01\']+)'
      },
      {
        begin: '(-?)\\b([\\d\']+(\\.[\\d\']*)?|\\.[\\d\']+)(u|U|l|L|ul|UL|f|F|b|B)'
      },
      {
        begin: '(-?)(\\b0[xX][a-fA-F0-9\']+|(\\b[\\d\']+(\\.[\\d\']*)?|\\.[\\d\']+)([eE][-+]?[\\d\']+)?)'
      }
    ],
    relevance: 0
  };
  const VERBATIM_STRING = {
    className: 'string',
    begin: '@"',
    end: '"',
    contains: [
      {
        begin: '""'
      }
    ]
  };
  const VERBATIM_STRING_NO_LF = hljs.inherit(VERBATIM_STRING, {
    illegal: /\n/
  });
  const SUBST = {
    className: 'subst',
    begin: /\{/,
    end: /\}/,
    keywords: KEYWORDS
  };
  const SUBST_NO_LF = hljs.inherit(SUBST, {
    illegal: /\n/
  });
  const INTERPOLATED_STRING = {
    className: 'string',
    begin: /\$"/,
    end: '"',
    illegal: /\n/,
    contains: [
      {
        begin: /\{\{/
      },
      {
        begin: /\}\}/
      },
      hljs.BACKSLASH_ESCAPE,
      SUBST_NO_LF
    ]
  };
  const INTERPOLATED_VERBATIM_STRING = {
    className: 'string',
    begin: /\$@"/,
    end: '"',
    contains: [
      {
        begin: /\{\{/
      },
      {
        begin: /\}\}/
      },
      {
        begin: '""'
      },
      SUBST
    ]
  };
  const INTERPOLATED_VERBATIM_STRING_NO_LF = hljs.inherit(INTERPOLATED_VERBATIM_STRING, {
    illegal: /\n/,
    contains: [
      {
        begin: /\{\{/
      },
      {
        begin: /\}\}/
      },
      {
        begin: '""'
      },
      SUBST_NO_LF
    ]
  });
  SUBST.contains = [
    INTERPOLATED_VERBATIM_STRING,
    INTERPOLATED_STRING,
    VERBATIM_STRING,
    hljs.APOS_STRING_MODE,
    hljs.QUOTE_STRING_MODE,
    NUMBERS,
    hljs.C_BLOCK_COMMENT_MODE
  ];
  SUBST_NO_LF.contains = [
    INTERPOLATED_VERBATIM_STRING_NO_LF,
    INTERPOLATED_STRING,
    VERBATIM_STRING_NO_LF,
    hljs.APOS_STRING_MODE,
    hljs.QUOTE_STRING_MODE,
    NUMBERS,
    hljs.inherit(hljs.C_BLOCK_COMMENT_MODE, {
      illegal: /\n/
    })
  ];
  const STRING = {
    variants: [
      INTERPOLATED_VERBATIM_STRING,
      INTERPOLATED_STRING,
      VERBATIM_STRING,
      hljs.APOS_STRING_MODE,
      hljs.QUOTE_STRING_MODE
    ]
  };

  const GENERIC_MODIFIER = {
    begin: "<",
    end: ">",
    contains: [
      {
        beginKeywords: "in out"
      },
      TITLE_MODE
    ]
  };
  const TYPE_IDENT_RE = hljs.IDENT_RE + '(<' + hljs.IDENT_RE + '(\\s*,\\s*' + hljs.IDENT_RE + ')*>)?(\\[\\])?';
  const AT_IDENTIFIER = {
    // prevents expressions like `@class` from incorrect flagging
    // `class` as a keyword
    begin: "@" + hljs.IDENT_RE,
    relevance: 0
  };

  return {
    name: 'C#',
    aliases: [
      'cs',
      'c#'
    ],
    keywords: KEYWORDS,
    illegal: /::/,
    contains: [
      hljs.COMMENT(
        '///',
        '$',
        {
          returnBegin: true,
          contains: [
            {
              className: 'doctag',
              variants: [
                {
                  begin: '///',
                  relevance: 0
                },
                {
                  begin: '<!--|-->'
                },
                {
                  begin: '</?',
                  end: '>'
                }
              ]
            }
          ]
        }
      ),
      hljs.C_LINE_COMMENT_MODE,
      hljs.C_BLOCK_COMMENT_MODE,
      {
        className: 'meta',
        begin: '#',
        end: '$',
        keywords: {
          'meta-keyword': 'if else elif endif define undef warning error line region endregion pragma checksum'
        }
      },
      STRING,
      NUMBERS,
      {
        beginKeywords: 'class interface',
        relevance: 0,
        end: /[{;=]/,
        illegal: /[^\s:,]/,
        contains: [
          {
            beginKeywords: "where class"
          },
          TITLE_MODE,
          GENERIC_MODIFIER,
          hljs.C_LINE_COMMENT_MODE,
          hljs.C_BLOCK_COMMENT_MODE
        ]
      },
      {
        beginKeywords: 'namespace',
        relevance: 0,
        end: /[{;=]/,
        illegal: /[^\s:]/,
        contains: [
          TITLE_MODE,
          hljs.C_LINE_COMMENT_MODE,
          hljs.C_BLOCK_COMMENT_MODE
        ]
      },
      {
        beginKeywords: 'record',
        relevance: 0,
        end: /[{;=]/,
        illegal: /[^\s:]/,
        contains: [
          TITLE_MODE,
          GENERIC_MODIFIER,
          hljs.C_LINE_COMMENT_MODE,
          hljs.C_BLOCK_COMMENT_MODE
        ]
      },
      {
        // [Attributes("")]
        className: 'meta',
        begin: '^\\s*\\[',
        excludeBegin: true,
        end: '\\]',
        excludeEnd: true,
        contains: [
          {
            className: 'meta-string',
            begin: /"/,
            end: /"/
          }
        ]
      },
      {
        // Expression keywords prevent 'keyword Name(...)' from being
        // recognized as a function definition
        beginKeywords: 'new return throw await else',
        relevance: 0
      },
      {
        className: 'function',
        begin: '(' + TYPE_IDENT_RE + '\\s+)+' + hljs.IDENT_RE + '\\s*(<.+>\\s*)?\\(',
        returnBegin: true,
        end: /\s*[{;=]/,
        excludeEnd: true,
        keywords: KEYWORDS,
        contains: [
          // prevents these from being highlighted `title`
          {
            beginKeywords: FUNCTION_MODIFIERS.join(" "),
            relevance: 0
          },
          {
            begin: hljs.IDENT_RE + '\\s*(<.+>\\s*)?\\(',
            returnBegin: true,
            contains: [
              hljs.TITLE_MODE,
              GENERIC_MODIFIER
            ],
            relevance: 0
          },
          {
            className: 'params',
            begin: /\(/,
            end: /\)/,
            excludeBegin: true,
            excludeEnd: true,
            keywords: KEYWORDS,
            relevance: 0,
            contains: [
              STRING,
              NUMBERS,
              hljs.C_BLOCK_COMMENT_MODE
            ]
          },
          hljs.C_LINE_COMMENT_MODE,
          hljs.C_BLOCK_COMMENT_MODE
        ]
      },
      AT_IDENTIFIER
    ]
  };
}

module.exports = csharp;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfY3NoYXJwLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxHQUFHO0FBQ0g7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEdBQUc7QUFDSDtBQUNBO0FBQ0EsY0FBYztBQUNkLFlBQVk7QUFDWjtBQUNBO0FBQ0E7QUFDQTtBQUNBLEdBQUc7QUFDSDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLGtCQUFrQixFQUFFO0FBQ3BCLE9BQU87QUFDUDtBQUNBLGtCQUFrQixFQUFFO0FBQ3BCLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLGtCQUFrQixFQUFFO0FBQ3BCLE9BQU87QUFDUDtBQUNBLGtCQUFrQixFQUFFO0FBQ3BCLE9BQU87QUFDUDtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0Esa0JBQWtCLEVBQUU7QUFDcEIsT0FBTztBQUNQO0FBQ0Esa0JBQWtCLEVBQUU7QUFDcEIsT0FBTztBQUNQO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBLEdBQUc7QUFDSDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLGlCQUFpQjtBQUNqQjtBQUNBO0FBQ0EsaUJBQWlCO0FBQ2pCO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsaUJBQWlCO0FBQ2pCO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsV0FBVztBQUNYO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0EsaUJBQWlCO0FBQ2pCO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSxpQkFBaUI7QUFDakI7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0Esb0JBQW9CO0FBQ3BCO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsV0FBVztBQUNYO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9jc2hhcnAuanMiXSwic291cmNlc0NvbnRlbnQiOlsiLypcbkxhbmd1YWdlOiBDI1xuQXV0aG9yOiBKYXNvbiBEaWFtb25kIDxqYXNvbkBkaWFtb25kLm5hbWU+XG5Db250cmlidXRvcjogTmljb2xhcyBMTE9CRVJBIDxubGxvYmVyYUBnbWFpbC5jb20+LCBQaWV0ZXIgVmFudG9ycmUgPHBpZXRlcnZhbnRvcnJlQGdtYWlsLmNvbT4sIERhdmlkIFBpbmUgPGRhdmlkLnBpbmVAbWljcm9zb2Z0LmNvbT5cbldlYnNpdGU6IGh0dHBzOi8vZG9jcy5taWNyb3NvZnQuY29tL2VuLXVzL2RvdG5ldC9jc2hhcnAvXG5DYXRlZ29yeTogY29tbW9uXG4qL1xuXG4vKiogQHR5cGUgTGFuZ3VhZ2VGbiAqL1xuZnVuY3Rpb24gY3NoYXJwKGhsanMpIHtcbiAgY29uc3QgQlVJTFRfSU5fS0VZV09SRFMgPSBbXG4gICAgJ2Jvb2wnLFxuICAgICdieXRlJyxcbiAgICAnY2hhcicsXG4gICAgJ2RlY2ltYWwnLFxuICAgICdkZWxlZ2F0ZScsXG4gICAgJ2RvdWJsZScsXG4gICAgJ2R5bmFtaWMnLFxuICAgICdlbnVtJyxcbiAgICAnZmxvYXQnLFxuICAgICdpbnQnLFxuICAgICdsb25nJyxcbiAgICAnbmludCcsXG4gICAgJ251aW50JyxcbiAgICAnb2JqZWN0JyxcbiAgICAnc2J5dGUnLFxuICAgICdzaG9ydCcsXG4gICAgJ3N0cmluZycsXG4gICAgJ3Vsb25nJyxcbiAgICAndWludCcsXG4gICAgJ3VzaG9ydCdcbiAgXTtcbiAgY29uc3QgRlVOQ1RJT05fTU9ESUZJRVJTID0gW1xuICAgICdwdWJsaWMnLFxuICAgICdwcml2YXRlJyxcbiAgICAncHJvdGVjdGVkJyxcbiAgICAnc3RhdGljJyxcbiAgICAnaW50ZXJuYWwnLFxuICAgICdwcm90ZWN0ZWQnLFxuICAgICdhYnN0cmFjdCcsXG4gICAgJ2FzeW5jJyxcbiAgICAnZXh0ZXJuJyxcbiAgICAnb3ZlcnJpZGUnLFxuICAgICd1bnNhZmUnLFxuICAgICd2aXJ0dWFsJyxcbiAgICAnbmV3JyxcbiAgICAnc2VhbGVkJyxcbiAgICAncGFydGlhbCdcbiAgXTtcbiAgY29uc3QgTElURVJBTF9LRVlXT1JEUyA9IFtcbiAgICAnZGVmYXVsdCcsXG4gICAgJ2ZhbHNlJyxcbiAgICAnbnVsbCcsXG4gICAgJ3RydWUnXG4gIF07XG4gIGNvbnN0IE5PUk1BTF9LRVlXT1JEUyA9IFtcbiAgICAnYWJzdHJhY3QnLFxuICAgICdhcycsXG4gICAgJ2Jhc2UnLFxuICAgICdicmVhaycsXG4gICAgJ2Nhc2UnLFxuICAgICdjbGFzcycsXG4gICAgJ2NvbnN0JyxcbiAgICAnY29udGludWUnLFxuICAgICdkbycsXG4gICAgJ2Vsc2UnLFxuICAgICdldmVudCcsXG4gICAgJ2V4cGxpY2l0JyxcbiAgICAnZXh0ZXJuJyxcbiAgICAnZmluYWxseScsXG4gICAgJ2ZpeGVkJyxcbiAgICAnZm9yJyxcbiAgICAnZm9yZWFjaCcsXG4gICAgJ2dvdG8nLFxuICAgICdpZicsXG4gICAgJ2ltcGxpY2l0JyxcbiAgICAnaW4nLFxuICAgICdpbnRlcmZhY2UnLFxuICAgICdpbnRlcm5hbCcsXG4gICAgJ2lzJyxcbiAgICAnbG9jaycsXG4gICAgJ25hbWVzcGFjZScsXG4gICAgJ25ldycsXG4gICAgJ29wZXJhdG9yJyxcbiAgICAnb3V0JyxcbiAgICAnb3ZlcnJpZGUnLFxuICAgICdwYXJhbXMnLFxuICAgICdwcml2YXRlJyxcbiAgICAncHJvdGVjdGVkJyxcbiAgICAncHVibGljJyxcbiAgICAncmVhZG9ubHknLFxuICAgICdyZWNvcmQnLFxuICAgICdyZWYnLFxuICAgICdyZXR1cm4nLFxuICAgICdzZWFsZWQnLFxuICAgICdzaXplb2YnLFxuICAgICdzdGFja2FsbG9jJyxcbiAgICAnc3RhdGljJyxcbiAgICAnc3RydWN0JyxcbiAgICAnc3dpdGNoJyxcbiAgICAndGhpcycsXG4gICAgJ3Rocm93JyxcbiAgICAndHJ5JyxcbiAgICAndHlwZW9mJyxcbiAgICAndW5jaGVja2VkJyxcbiAgICAndW5zYWZlJyxcbiAgICAndXNpbmcnLFxuICAgICd2aXJ0dWFsJyxcbiAgICAndm9pZCcsXG4gICAgJ3ZvbGF0aWxlJyxcbiAgICAnd2hpbGUnXG4gIF07XG4gIGNvbnN0IENPTlRFWFRVQUxfS0VZV09SRFMgPSBbXG4gICAgJ2FkZCcsXG4gICAgJ2FsaWFzJyxcbiAgICAnYW5kJyxcbiAgICAnYXNjZW5kaW5nJyxcbiAgICAnYXN5bmMnLFxuICAgICdhd2FpdCcsXG4gICAgJ2J5JyxcbiAgICAnZGVzY2VuZGluZycsXG4gICAgJ2VxdWFscycsXG4gICAgJ2Zyb20nLFxuICAgICdnZXQnLFxuICAgICdnbG9iYWwnLFxuICAgICdncm91cCcsXG4gICAgJ2luaXQnLFxuICAgICdpbnRvJyxcbiAgICAnam9pbicsXG4gICAgJ2xldCcsXG4gICAgJ25hbWVvZicsXG4gICAgJ25vdCcsXG4gICAgJ25vdG51bGwnLFxuICAgICdvbicsXG4gICAgJ29yJyxcbiAgICAnb3JkZXJieScsXG4gICAgJ3BhcnRpYWwnLFxuICAgICdyZW1vdmUnLFxuICAgICdzZWxlY3QnLFxuICAgICdzZXQnLFxuICAgICd1bm1hbmFnZWQnLFxuICAgICd2YWx1ZXwwJyxcbiAgICAndmFyJyxcbiAgICAnd2hlbicsXG4gICAgJ3doZXJlJyxcbiAgICAnd2l0aCcsXG4gICAgJ3lpZWxkJ1xuICBdO1xuXG4gIGNvbnN0IEtFWVdPUkRTID0ge1xuICAgIGtleXdvcmQ6IE5PUk1BTF9LRVlXT1JEUy5jb25jYXQoQ09OVEVYVFVBTF9LRVlXT1JEUyksXG4gICAgYnVpbHRfaW46IEJVSUxUX0lOX0tFWVdPUkRTLFxuICAgIGxpdGVyYWw6IExJVEVSQUxfS0VZV09SRFNcbiAgfTtcbiAgY29uc3QgVElUTEVfTU9ERSA9IGhsanMuaW5oZXJpdChobGpzLlRJVExFX01PREUsIHtcbiAgICBiZWdpbjogJ1thLXpBLVpdKFxcXFwuP1xcXFx3KSonXG4gIH0pO1xuICBjb25zdCBOVU1CRVJTID0ge1xuICAgIGNsYXNzTmFtZTogJ251bWJlcicsXG4gICAgdmFyaWFudHM6IFtcbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICdcXFxcYigwYlswMVxcJ10rKSdcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnKC0/KVxcXFxiKFtcXFxcZFxcJ10rKFxcXFwuW1xcXFxkXFwnXSopP3xcXFxcLltcXFxcZFxcJ10rKSh1fFV8bHxMfHVsfFVMfGZ8RnxifEIpJ1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICcoLT8pKFxcXFxiMFt4WF1bYS1mQS1GMC05XFwnXSt8KFxcXFxiW1xcXFxkXFwnXSsoXFxcXC5bXFxcXGRcXCddKik/fFxcXFwuW1xcXFxkXFwnXSspKFtlRV1bLStdP1tcXFxcZFxcJ10rKT8pJ1xuICAgICAgfVxuICAgIF0sXG4gICAgcmVsZXZhbmNlOiAwXG4gIH07XG4gIGNvbnN0IFZFUkJBVElNX1NUUklORyA9IHtcbiAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgIGJlZ2luOiAnQFwiJyxcbiAgICBlbmQ6ICdcIicsXG4gICAgY29udGFpbnM6IFtcbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICdcIlwiJ1xuICAgICAgfVxuICAgIF1cbiAgfTtcbiAgY29uc3QgVkVSQkFUSU1fU1RSSU5HX05PX0xGID0gaGxqcy5pbmhlcml0KFZFUkJBVElNX1NUUklORywge1xuICAgIGlsbGVnYWw6IC9cXG4vXG4gIH0pO1xuICBjb25zdCBTVUJTVCA9IHtcbiAgICBjbGFzc05hbWU6ICdzdWJzdCcsXG4gICAgYmVnaW46IC9cXHsvLFxuICAgIGVuZDogL1xcfS8sXG4gICAga2V5d29yZHM6IEtFWVdPUkRTXG4gIH07XG4gIGNvbnN0IFNVQlNUX05PX0xGID0gaGxqcy5pbmhlcml0KFNVQlNULCB7XG4gICAgaWxsZWdhbDogL1xcbi9cbiAgfSk7XG4gIGNvbnN0IElOVEVSUE9MQVRFRF9TVFJJTkcgPSB7XG4gICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICBiZWdpbjogL1xcJFwiLyxcbiAgICBlbmQ6ICdcIicsXG4gICAgaWxsZWdhbDogL1xcbi8sXG4gICAgY29udGFpbnM6IFtcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC9cXHtcXHsvXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogL1xcfVxcfS9cbiAgICAgIH0sXG4gICAgICBobGpzLkJBQ0tTTEFTSF9FU0NBUEUsXG4gICAgICBTVUJTVF9OT19MRlxuICAgIF1cbiAgfTtcbiAgY29uc3QgSU5URVJQT0xBVEVEX1ZFUkJBVElNX1NUUklORyA9IHtcbiAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgIGJlZ2luOiAvXFwkQFwiLyxcbiAgICBlbmQ6ICdcIicsXG4gICAgY29udGFpbnM6IFtcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC9cXHtcXHsvXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogL1xcfVxcfS9cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnXCJcIidcbiAgICAgIH0sXG4gICAgICBTVUJTVFxuICAgIF1cbiAgfTtcbiAgY29uc3QgSU5URVJQT0xBVEVEX1ZFUkJBVElNX1NUUklOR19OT19MRiA9IGhsanMuaW5oZXJpdChJTlRFUlBPTEFURURfVkVSQkFUSU1fU1RSSU5HLCB7XG4gICAgaWxsZWdhbDogL1xcbi8sXG4gICAgY29udGFpbnM6IFtcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC9cXHtcXHsvXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogL1xcfVxcfS9cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnXCJcIidcbiAgICAgIH0sXG4gICAgICBTVUJTVF9OT19MRlxuICAgIF1cbiAgfSk7XG4gIFNVQlNULmNvbnRhaW5zID0gW1xuICAgIElOVEVSUE9MQVRFRF9WRVJCQVRJTV9TVFJJTkcsXG4gICAgSU5URVJQT0xBVEVEX1NUUklORyxcbiAgICBWRVJCQVRJTV9TVFJJTkcsXG4gICAgaGxqcy5BUE9TX1NUUklOR19NT0RFLFxuICAgIGhsanMuUVVPVEVfU1RSSU5HX01PREUsXG4gICAgTlVNQkVSUyxcbiAgICBobGpzLkNfQkxPQ0tfQ09NTUVOVF9NT0RFXG4gIF07XG4gIFNVQlNUX05PX0xGLmNvbnRhaW5zID0gW1xuICAgIElOVEVSUE9MQVRFRF9WRVJCQVRJTV9TVFJJTkdfTk9fTEYsXG4gICAgSU5URVJQT0xBVEVEX1NUUklORyxcbiAgICBWRVJCQVRJTV9TVFJJTkdfTk9fTEYsXG4gICAgaGxqcy5BUE9TX1NUUklOR19NT0RFLFxuICAgIGhsanMuUVVPVEVfU1RSSU5HX01PREUsXG4gICAgTlVNQkVSUyxcbiAgICBobGpzLmluaGVyaXQoaGxqcy5DX0JMT0NLX0NPTU1FTlRfTU9ERSwge1xuICAgICAgaWxsZWdhbDogL1xcbi9cbiAgICB9KVxuICBdO1xuICBjb25zdCBTVFJJTkcgPSB7XG4gICAgdmFyaWFudHM6IFtcbiAgICAgIElOVEVSUE9MQVRFRF9WRVJCQVRJTV9TVFJJTkcsXG4gICAgICBJTlRFUlBPTEFURURfU1RSSU5HLFxuICAgICAgVkVSQkFUSU1fU1RSSU5HLFxuICAgICAgaGxqcy5BUE9TX1NUUklOR19NT0RFLFxuICAgICAgaGxqcy5RVU9URV9TVFJJTkdfTU9ERVxuICAgIF1cbiAgfTtcblxuICBjb25zdCBHRU5FUklDX01PRElGSUVSID0ge1xuICAgIGJlZ2luOiBcIjxcIixcbiAgICBlbmQ6IFwiPlwiLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICB7XG4gICAgICAgIGJlZ2luS2V5d29yZHM6IFwiaW4gb3V0XCJcbiAgICAgIH0sXG4gICAgICBUSVRMRV9NT0RFXG4gICAgXVxuICB9O1xuICBjb25zdCBUWVBFX0lERU5UX1JFID0gaGxqcy5JREVOVF9SRSArICcoPCcgKyBobGpzLklERU5UX1JFICsgJyhcXFxccyosXFxcXHMqJyArIGhsanMuSURFTlRfUkUgKyAnKSo+KT8oXFxcXFtcXFxcXSk/JztcbiAgY29uc3QgQVRfSURFTlRJRklFUiA9IHtcbiAgICAvLyBwcmV2ZW50cyBleHByZXNzaW9ucyBsaWtlIGBAY2xhc3NgIGZyb20gaW5jb3JyZWN0IGZsYWdnaW5nXG4gICAgLy8gYGNsYXNzYCBhcyBhIGtleXdvcmRcbiAgICBiZWdpbjogXCJAXCIgKyBobGpzLklERU5UX1JFLFxuICAgIHJlbGV2YW5jZTogMFxuICB9O1xuXG4gIHJldHVybiB7XG4gICAgbmFtZTogJ0MjJyxcbiAgICBhbGlhc2VzOiBbXG4gICAgICAnY3MnLFxuICAgICAgJ2MjJ1xuICAgIF0sXG4gICAga2V5d29yZHM6IEtFWVdPUkRTLFxuICAgIGlsbGVnYWw6IC86Oi8sXG4gICAgY29udGFpbnM6IFtcbiAgICAgIGhsanMuQ09NTUVOVChcbiAgICAgICAgJy8vLycsXG4gICAgICAgICckJyxcbiAgICAgICAge1xuICAgICAgICAgIHJldHVybkJlZ2luOiB0cnVlLFxuICAgICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgICB7XG4gICAgICAgICAgICAgIGNsYXNzTmFtZTogJ2RvY3RhZycsXG4gICAgICAgICAgICAgIHZhcmlhbnRzOiBbXG4gICAgICAgICAgICAgICAge1xuICAgICAgICAgICAgICAgICAgYmVnaW46ICcvLy8nLFxuICAgICAgICAgICAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICAgICAgICAgICAgfSxcbiAgICAgICAgICAgICAgICB7XG4gICAgICAgICAgICAgICAgICBiZWdpbjogJzwhLS18LS0+J1xuICAgICAgICAgICAgICAgIH0sXG4gICAgICAgICAgICAgICAge1xuICAgICAgICAgICAgICAgICAgYmVnaW46ICc8Lz8nLFxuICAgICAgICAgICAgICAgICAgZW5kOiAnPidcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgIF1cbiAgICAgICAgICAgIH1cbiAgICAgICAgICBdXG4gICAgICAgIH1cbiAgICAgICksXG4gICAgICBobGpzLkNfTElORV9DT01NRU5UX01PREUsXG4gICAgICBobGpzLkNfQkxPQ0tfQ09NTUVOVF9NT0RFLFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdtZXRhJyxcbiAgICAgICAgYmVnaW46ICcjJyxcbiAgICAgICAgZW5kOiAnJCcsXG4gICAgICAgIGtleXdvcmRzOiB7XG4gICAgICAgICAgJ21ldGEta2V5d29yZCc6ICdpZiBlbHNlIGVsaWYgZW5kaWYgZGVmaW5lIHVuZGVmIHdhcm5pbmcgZXJyb3IgbGluZSByZWdpb24gZW5kcmVnaW9uIHByYWdtYSBjaGVja3N1bSdcbiAgICAgICAgfVxuICAgICAgfSxcbiAgICAgIFNUUklORyxcbiAgICAgIE5VTUJFUlMsXG4gICAgICB7XG4gICAgICAgIGJlZ2luS2V5d29yZHM6ICdjbGFzcyBpbnRlcmZhY2UnLFxuICAgICAgICByZWxldmFuY2U6IDAsXG4gICAgICAgIGVuZDogL1t7Oz1dLyxcbiAgICAgICAgaWxsZWdhbDogL1teXFxzOixdLyxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbktleXdvcmRzOiBcIndoZXJlIGNsYXNzXCJcbiAgICAgICAgICB9LFxuICAgICAgICAgIFRJVExFX01PREUsXG4gICAgICAgICAgR0VORVJJQ19NT0RJRklFUixcbiAgICAgICAgICBobGpzLkNfTElORV9DT01NRU5UX01PREUsXG4gICAgICAgICAgaGxqcy5DX0JMT0NLX0NPTU1FTlRfTU9ERVxuICAgICAgICBdXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbktleXdvcmRzOiAnbmFtZXNwYWNlJyxcbiAgICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgICBlbmQ6IC9bezs9XS8sXG4gICAgICAgIGlsbGVnYWw6IC9bXlxcczpdLyxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICBUSVRMRV9NT0RFLFxuICAgICAgICAgIGhsanMuQ19MSU5FX0NPTU1FTlRfTU9ERSxcbiAgICAgICAgICBobGpzLkNfQkxPQ0tfQ09NTUVOVF9NT0RFXG4gICAgICAgIF1cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luS2V5d29yZHM6ICdyZWNvcmQnLFxuICAgICAgICByZWxldmFuY2U6IDAsXG4gICAgICAgIGVuZDogL1t7Oz1dLyxcbiAgICAgICAgaWxsZWdhbDogL1teXFxzOl0vLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIFRJVExFX01PREUsXG4gICAgICAgICAgR0VORVJJQ19NT0RJRklFUixcbiAgICAgICAgICBobGpzLkNfTElORV9DT01NRU5UX01PREUsXG4gICAgICAgICAgaGxqcy5DX0JMT0NLX0NPTU1FTlRfTU9ERVxuICAgICAgICBdXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICAvLyBbQXR0cmlidXRlcyhcIlwiKV1cbiAgICAgICAgY2xhc3NOYW1lOiAnbWV0YScsXG4gICAgICAgIGJlZ2luOiAnXlxcXFxzKlxcXFxbJyxcbiAgICAgICAgZXhjbHVkZUJlZ2luOiB0cnVlLFxuICAgICAgICBlbmQ6ICdcXFxcXScsXG4gICAgICAgIGV4Y2x1ZGVFbmQ6IHRydWUsXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgY2xhc3NOYW1lOiAnbWV0YS1zdHJpbmcnLFxuICAgICAgICAgICAgYmVnaW46IC9cIi8sXG4gICAgICAgICAgICBlbmQ6IC9cIi9cbiAgICAgICAgICB9XG4gICAgICAgIF1cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIC8vIEV4cHJlc3Npb24ga2V5d29yZHMgcHJldmVudCAna2V5d29yZCBOYW1lKC4uLiknIGZyb20gYmVpbmdcbiAgICAgICAgLy8gcmVjb2duaXplZCBhcyBhIGZ1bmN0aW9uIGRlZmluaXRpb25cbiAgICAgICAgYmVnaW5LZXl3b3JkczogJ25ldyByZXR1cm4gdGhyb3cgYXdhaXQgZWxzZScsXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnZnVuY3Rpb24nLFxuICAgICAgICBiZWdpbjogJygnICsgVFlQRV9JREVOVF9SRSArICdcXFxccyspKycgKyBobGpzLklERU5UX1JFICsgJ1xcXFxzKig8Lis+XFxcXHMqKT9cXFxcKCcsXG4gICAgICAgIHJldHVybkJlZ2luOiB0cnVlLFxuICAgICAgICBlbmQ6IC9cXHMqW3s7PV0vLFxuICAgICAgICBleGNsdWRlRW5kOiB0cnVlLFxuICAgICAgICBrZXl3b3JkczogS0VZV09SRFMsXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgLy8gcHJldmVudHMgdGhlc2UgZnJvbSBiZWluZyBoaWdobGlnaHRlZCBgdGl0bGVgXG4gICAgICAgICAge1xuICAgICAgICAgICAgYmVnaW5LZXl3b3JkczogRlVOQ1RJT05fTU9ESUZJRVJTLmpvaW4oXCIgXCIpLFxuICAgICAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbjogaGxqcy5JREVOVF9SRSArICdcXFxccyooPC4rPlxcXFxzKik/XFxcXCgnLFxuICAgICAgICAgICAgcmV0dXJuQmVnaW46IHRydWUsXG4gICAgICAgICAgICBjb250YWluczogW1xuICAgICAgICAgICAgICBobGpzLlRJVExFX01PREUsXG4gICAgICAgICAgICAgIEdFTkVSSUNfTU9ESUZJRVJcbiAgICAgICAgICAgIF0sXG4gICAgICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGNsYXNzTmFtZTogJ3BhcmFtcycsXG4gICAgICAgICAgICBiZWdpbjogL1xcKC8sXG4gICAgICAgICAgICBlbmQ6IC9cXCkvLFxuICAgICAgICAgICAgZXhjbHVkZUJlZ2luOiB0cnVlLFxuICAgICAgICAgICAgZXhjbHVkZUVuZDogdHJ1ZSxcbiAgICAgICAgICAgIGtleXdvcmRzOiBLRVlXT1JEUyxcbiAgICAgICAgICAgIHJlbGV2YW5jZTogMCxcbiAgICAgICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgICAgIFNUUklORyxcbiAgICAgICAgICAgICAgTlVNQkVSUyxcbiAgICAgICAgICAgICAgaGxqcy5DX0JMT0NLX0NPTU1FTlRfTU9ERVxuICAgICAgICAgICAgXVxuICAgICAgICAgIH0sXG4gICAgICAgICAgaGxqcy5DX0xJTkVfQ09NTUVOVF9NT0RFLFxuICAgICAgICAgIGhsanMuQ19CTE9DS19DT01NRU5UX01PREVcbiAgICAgICAgXVxuICAgICAgfSxcbiAgICAgIEFUX0lERU5USUZJRVJcbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gY3NoYXJwO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9