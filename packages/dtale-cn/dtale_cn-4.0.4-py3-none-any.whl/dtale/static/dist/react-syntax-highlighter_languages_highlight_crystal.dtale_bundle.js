(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_crystal"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/crystal.js":
/*!**************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/crystal.js ***!
  \**************************************************************************************************/
/***/ ((module) => {

/*
Language: Crystal
Author: TSUYUSATO Kitsune <make.just.on@gmail.com>
Website: https://crystal-lang.org
*/

/** @type LanguageFn */
function crystal(hljs) {
  const INT_SUFFIX = '(_?[ui](8|16|32|64|128))?';
  const FLOAT_SUFFIX = '(_?f(32|64))?';
  const CRYSTAL_IDENT_RE = '[a-zA-Z_]\\w*[!?=]?';
  const CRYSTAL_METHOD_RE = '[a-zA-Z_]\\w*[!?=]?|[-+~]@|<<|>>|[=!]~|===?|<=>|[<>]=?|\\*\\*|[-/+%^&*~|]|//|//=|&[-+*]=?|&\\*\\*|\\[\\][=?]?';
  const CRYSTAL_PATH_RE = '[A-Za-z_]\\w*(::\\w+)*(\\?|!)?';
  const CRYSTAL_KEYWORDS = {
    $pattern: CRYSTAL_IDENT_RE,
    keyword:
      'abstract alias annotation as as? asm begin break case class def do else elsif end ensure enum extend for fun if ' +
      'include instance_sizeof is_a? lib macro module next nil? of out pointerof private protected rescue responds_to? ' +
      'return require select self sizeof struct super then type typeof union uninitialized unless until verbatim when while with yield ' +
      '__DIR__ __END_LINE__ __FILE__ __LINE__',
    literal: 'false nil true'
  };
  const SUBST = {
    className: 'subst',
    begin: /#\{/,
    end: /\}/,
    keywords: CRYSTAL_KEYWORDS
  };
  const EXPANSION = {
    className: 'template-variable',
    variants: [
      {
        begin: '\\{\\{',
        end: '\\}\\}'
      },
      {
        begin: '\\{%',
        end: '%\\}'
      }
    ],
    keywords: CRYSTAL_KEYWORDS
  };

  function recursiveParen(begin, end) {
    const
        contains = [
          {
            begin: begin,
            end: end
          }
        ];
    contains[0].contains = contains;
    return contains;
  }
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
        begin: '%[Qwi]?\\(',
        end: '\\)',
        contains: recursiveParen('\\(', '\\)')
      },
      {
        begin: '%[Qwi]?\\[',
        end: '\\]',
        contains: recursiveParen('\\[', '\\]')
      },
      {
        begin: '%[Qwi]?\\{',
        end: /\}/,
        contains: recursiveParen(/\{/, /\}/)
      },
      {
        begin: '%[Qwi]?<',
        end: '>',
        contains: recursiveParen('<', '>')
      },
      {
        begin: '%[Qwi]?\\|',
        end: '\\|'
      },
      {
        begin: /<<-\w+$/,
        end: /^\s*\w+$/
      }
    ],
    relevance: 0
  };
  const Q_STRING = {
    className: 'string',
    variants: [
      {
        begin: '%q\\(',
        end: '\\)',
        contains: recursiveParen('\\(', '\\)')
      },
      {
        begin: '%q\\[',
        end: '\\]',
        contains: recursiveParen('\\[', '\\]')
      },
      {
        begin: '%q\\{',
        end: /\}/,
        contains: recursiveParen(/\{/, /\}/)
      },
      {
        begin: '%q<',
        end: '>',
        contains: recursiveParen('<', '>')
      },
      {
        begin: '%q\\|',
        end: '\\|'
      },
      {
        begin: /<<-'\w+'$/,
        end: /^\s*\w+$/
      }
    ],
    relevance: 0
  };
  const REGEXP = {
    begin: '(?!%\\})(' + hljs.RE_STARTERS_RE + '|\\n|\\b(case|if|select|unless|until|when|while)\\b)\\s*',
    keywords: 'case if select unless until when while',
    contains: [
      {
        className: 'regexp',
        contains: [
          hljs.BACKSLASH_ESCAPE,
          SUBST
        ],
        variants: [
          {
            begin: '//[a-z]*',
            relevance: 0
          },
          {
            begin: '/(?!\\/)',
            end: '/[a-z]*'
          }
        ]
      }
    ],
    relevance: 0
  };
  const REGEXP2 = {
    className: 'regexp',
    contains: [
      hljs.BACKSLASH_ESCAPE,
      SUBST
    ],
    variants: [
      {
        begin: '%r\\(',
        end: '\\)',
        contains: recursiveParen('\\(', '\\)')
      },
      {
        begin: '%r\\[',
        end: '\\]',
        contains: recursiveParen('\\[', '\\]')
      },
      {
        begin: '%r\\{',
        end: /\}/,
        contains: recursiveParen(/\{/, /\}/)
      },
      {
        begin: '%r<',
        end: '>',
        contains: recursiveParen('<', '>')
      },
      {
        begin: '%r\\|',
        end: '\\|'
      }
    ],
    relevance: 0
  };
  const ATTRIBUTE = {
    className: 'meta',
    begin: '@\\[',
    end: '\\]',
    contains: [
      hljs.inherit(hljs.QUOTE_STRING_MODE, {
        className: 'meta-string'
      })
    ]
  };
  const CRYSTAL_DEFAULT_CONTAINS = [
    EXPANSION,
    STRING,
    Q_STRING,
    REGEXP2,
    REGEXP,
    ATTRIBUTE,
    hljs.HASH_COMMENT_MODE,
    {
      className: 'class',
      beginKeywords: 'class module struct',
      end: '$|;',
      illegal: /=/,
      contains: [
        hljs.HASH_COMMENT_MODE,
        hljs.inherit(hljs.TITLE_MODE, {
          begin: CRYSTAL_PATH_RE
        }),
        { // relevance booster for inheritance
          begin: '<'
        }
      ]
    },
    {
      className: 'class',
      beginKeywords: 'lib enum union',
      end: '$|;',
      illegal: /=/,
      contains: [
        hljs.HASH_COMMENT_MODE,
        hljs.inherit(hljs.TITLE_MODE, {
          begin: CRYSTAL_PATH_RE
        })
      ]
    },
    {
      beginKeywords: 'annotation',
      end: '$|;',
      illegal: /=/,
      contains: [
        hljs.HASH_COMMENT_MODE,
        hljs.inherit(hljs.TITLE_MODE, {
          begin: CRYSTAL_PATH_RE
        })
      ],
      relevance: 2
    },
    {
      className: 'function',
      beginKeywords: 'def',
      end: /\B\b/,
      contains: [
        hljs.inherit(hljs.TITLE_MODE, {
          begin: CRYSTAL_METHOD_RE,
          endsParent: true
        })
      ]
    },
    {
      className: 'function',
      beginKeywords: 'fun macro',
      end: /\B\b/,
      contains: [
        hljs.inherit(hljs.TITLE_MODE, {
          begin: CRYSTAL_METHOD_RE,
          endsParent: true
        })
      ],
      relevance: 2
    },
    {
      className: 'symbol',
      begin: hljs.UNDERSCORE_IDENT_RE + '(!|\\?)?:',
      relevance: 0
    },
    {
      className: 'symbol',
      begin: ':',
      contains: [
        STRING,
        {
          begin: CRYSTAL_METHOD_RE
        }
      ],
      relevance: 0
    },
    {
      className: 'number',
      variants: [
        {
          begin: '\\b0b([01_]+)' + INT_SUFFIX
        },
        {
          begin: '\\b0o([0-7_]+)' + INT_SUFFIX
        },
        {
          begin: '\\b0x([A-Fa-f0-9_]+)' + INT_SUFFIX
        },
        {
          begin: '\\b([1-9][0-9_]*[0-9]|[0-9])(\\.[0-9][0-9_]*)?([eE]_?[-+]?[0-9_]*)?' + FLOAT_SUFFIX + '(?!_)'
        },
        {
          begin: '\\b([1-9][0-9_]*|0)' + INT_SUFFIX
        }
      ],
      relevance: 0
    }
  ];
  SUBST.contains = CRYSTAL_DEFAULT_CONTAINS;
  EXPANSION.contains = CRYSTAL_DEFAULT_CONTAINS.slice(1); // without EXPANSION

  return {
    name: 'Crystal',
    aliases: [ 'cr' ],
    keywords: CRYSTAL_KEYWORDS,
    contains: CRYSTAL_DEFAULT_CONTAINS
  };
}

module.exports = crystal;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfY3J5c3RhbC5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLGVBQWU7QUFDZixZQUFZO0FBQ1o7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsbUJBQW1CLEdBQUc7QUFDdEIsaUJBQWlCLEdBQUc7QUFDcEIsT0FBTztBQUNQO0FBQ0EsbUJBQW1CO0FBQ25CLGtCQUFrQjtBQUNsQjtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBLDBCQUEwQjtBQUMxQixnQkFBZ0I7QUFDaEIsb0NBQW9DLE1BQU07QUFDMUMsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0EscUJBQXFCO0FBQ3JCLGdCQUFnQjtBQUNoQixvQ0FBb0MsTUFBTTtBQUMxQyxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxtQkFBbUI7QUFDbkI7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsV0FBVztBQUNYO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQSxxQkFBcUI7QUFDckIsZ0JBQWdCO0FBQ2hCLG9DQUFvQyxNQUFNO0FBQzFDLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsZUFBZTtBQUNmO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxTQUFTO0FBQ1QsVUFBVTtBQUNWO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7QUFDQSxlQUFlO0FBQ2Y7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFNBQVM7QUFDVDtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0EsZUFBZTtBQUNmO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxTQUFTO0FBQ1Q7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsU0FBUztBQUNUO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxTQUFTO0FBQ1Q7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsU0FBUztBQUNUO0FBQ0E7QUFDQSxTQUFTO0FBQ1Q7QUFDQTtBQUNBLFNBQVM7QUFDVDtBQUNBO0FBQ0EsU0FBUztBQUNUO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSwwREFBMEQ7O0FBRTFEO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9jcnlzdGFsLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogQ3J5c3RhbFxuQXV0aG9yOiBUU1VZVVNBVE8gS2l0c3VuZSA8bWFrZS5qdXN0Lm9uQGdtYWlsLmNvbT5cbldlYnNpdGU6IGh0dHBzOi8vY3J5c3RhbC1sYW5nLm9yZ1xuKi9cblxuLyoqIEB0eXBlIExhbmd1YWdlRm4gKi9cbmZ1bmN0aW9uIGNyeXN0YWwoaGxqcykge1xuICBjb25zdCBJTlRfU1VGRklYID0gJyhfP1t1aV0oOHwxNnwzMnw2NHwxMjgpKT8nO1xuICBjb25zdCBGTE9BVF9TVUZGSVggPSAnKF8/ZigzMnw2NCkpPyc7XG4gIGNvbnN0IENSWVNUQUxfSURFTlRfUkUgPSAnW2EtekEtWl9dXFxcXHcqWyE/PV0/JztcbiAgY29uc3QgQ1JZU1RBTF9NRVRIT0RfUkUgPSAnW2EtekEtWl9dXFxcXHcqWyE/PV0/fFstK35dQHw8PHw+PnxbPSFdfnw9PT0/fDw9PnxbPD5dPT98XFxcXCpcXFxcKnxbLS8rJV4mKn58XXwvL3wvLz18JlstKypdPT98JlxcXFwqXFxcXCp8XFxcXFtcXFxcXVs9P10/JztcbiAgY29uc3QgQ1JZU1RBTF9QQVRIX1JFID0gJ1tBLVphLXpfXVxcXFx3Kig6OlxcXFx3KykqKFxcXFw/fCEpPyc7XG4gIGNvbnN0IENSWVNUQUxfS0VZV09SRFMgPSB7XG4gICAgJHBhdHRlcm46IENSWVNUQUxfSURFTlRfUkUsXG4gICAga2V5d29yZDpcbiAgICAgICdhYnN0cmFjdCBhbGlhcyBhbm5vdGF0aW9uIGFzIGFzPyBhc20gYmVnaW4gYnJlYWsgY2FzZSBjbGFzcyBkZWYgZG8gZWxzZSBlbHNpZiBlbmQgZW5zdXJlIGVudW0gZXh0ZW5kIGZvciBmdW4gaWYgJyArXG4gICAgICAnaW5jbHVkZSBpbnN0YW5jZV9zaXplb2YgaXNfYT8gbGliIG1hY3JvIG1vZHVsZSBuZXh0IG5pbD8gb2Ygb3V0IHBvaW50ZXJvZiBwcml2YXRlIHByb3RlY3RlZCByZXNjdWUgcmVzcG9uZHNfdG8/ICcgK1xuICAgICAgJ3JldHVybiByZXF1aXJlIHNlbGVjdCBzZWxmIHNpemVvZiBzdHJ1Y3Qgc3VwZXIgdGhlbiB0eXBlIHR5cGVvZiB1bmlvbiB1bmluaXRpYWxpemVkIHVubGVzcyB1bnRpbCB2ZXJiYXRpbSB3aGVuIHdoaWxlIHdpdGggeWllbGQgJyArXG4gICAgICAnX19ESVJfXyBfX0VORF9MSU5FX18gX19GSUxFX18gX19MSU5FX18nLFxuICAgIGxpdGVyYWw6ICdmYWxzZSBuaWwgdHJ1ZSdcbiAgfTtcbiAgY29uc3QgU1VCU1QgPSB7XG4gICAgY2xhc3NOYW1lOiAnc3Vic3QnLFxuICAgIGJlZ2luOiAvI1xcey8sXG4gICAgZW5kOiAvXFx9LyxcbiAgICBrZXl3b3JkczogQ1JZU1RBTF9LRVlXT1JEU1xuICB9O1xuICBjb25zdCBFWFBBTlNJT04gPSB7XG4gICAgY2xhc3NOYW1lOiAndGVtcGxhdGUtdmFyaWFibGUnLFxuICAgIHZhcmlhbnRzOiBbXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnXFxcXHtcXFxceycsXG4gICAgICAgIGVuZDogJ1xcXFx9XFxcXH0nXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogJ1xcXFx7JScsXG4gICAgICAgIGVuZDogJyVcXFxcfSdcbiAgICAgIH1cbiAgICBdLFxuICAgIGtleXdvcmRzOiBDUllTVEFMX0tFWVdPUkRTXG4gIH07XG5cbiAgZnVuY3Rpb24gcmVjdXJzaXZlUGFyZW4oYmVnaW4sIGVuZCkge1xuICAgIGNvbnN0XG4gICAgICAgIGNvbnRhaW5zID0gW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiBiZWdpbixcbiAgICAgICAgICAgIGVuZDogZW5kXG4gICAgICAgICAgfVxuICAgICAgICBdO1xuICAgIGNvbnRhaW5zWzBdLmNvbnRhaW5zID0gY29udGFpbnM7XG4gICAgcmV0dXJuIGNvbnRhaW5zO1xuICB9XG4gIGNvbnN0IFNUUklORyA9IHtcbiAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBobGpzLkJBQ0tTTEFTSF9FU0NBUEUsXG4gICAgICBTVUJTVFxuICAgIF0sXG4gICAgdmFyaWFudHM6IFtcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC8nLyxcbiAgICAgICAgZW5kOiAvJy9cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAvXCIvLFxuICAgICAgICBlbmQ6IC9cIi9cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAvYC8sXG4gICAgICAgIGVuZDogL2AvXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogJyVbUXdpXT9cXFxcKCcsXG4gICAgICAgIGVuZDogJ1xcXFwpJyxcbiAgICAgICAgY29udGFpbnM6IHJlY3Vyc2l2ZVBhcmVuKCdcXFxcKCcsICdcXFxcKScpXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogJyVbUXdpXT9cXFxcWycsXG4gICAgICAgIGVuZDogJ1xcXFxdJyxcbiAgICAgICAgY29udGFpbnM6IHJlY3Vyc2l2ZVBhcmVuKCdcXFxcWycsICdcXFxcXScpXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogJyVbUXdpXT9cXFxceycsXG4gICAgICAgIGVuZDogL1xcfS8sXG4gICAgICAgIGNvbnRhaW5zOiByZWN1cnNpdmVQYXJlbigvXFx7LywgL1xcfS8pXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogJyVbUXdpXT88JyxcbiAgICAgICAgZW5kOiAnPicsXG4gICAgICAgIGNvbnRhaW5zOiByZWN1cnNpdmVQYXJlbignPCcsICc+JylcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnJVtRd2ldP1xcXFx8JyxcbiAgICAgICAgZW5kOiAnXFxcXHwnXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogLzw8LVxcdyskLyxcbiAgICAgICAgZW5kOiAvXlxccypcXHcrJC9cbiAgICAgIH1cbiAgICBdLFxuICAgIHJlbGV2YW5jZTogMFxuICB9O1xuICBjb25zdCBRX1NUUklORyA9IHtcbiAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgIHZhcmlhbnRzOiBbXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnJXFcXFxcKCcsXG4gICAgICAgIGVuZDogJ1xcXFwpJyxcbiAgICAgICAgY29udGFpbnM6IHJlY3Vyc2l2ZVBhcmVuKCdcXFxcKCcsICdcXFxcKScpXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogJyVxXFxcXFsnLFxuICAgICAgICBlbmQ6ICdcXFxcXScsXG4gICAgICAgIGNvbnRhaW5zOiByZWN1cnNpdmVQYXJlbignXFxcXFsnLCAnXFxcXF0nKVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICclcVxcXFx7JyxcbiAgICAgICAgZW5kOiAvXFx9LyxcbiAgICAgICAgY29udGFpbnM6IHJlY3Vyc2l2ZVBhcmVuKC9cXHsvLCAvXFx9LylcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnJXE8JyxcbiAgICAgICAgZW5kOiAnPicsXG4gICAgICAgIGNvbnRhaW5zOiByZWN1cnNpdmVQYXJlbignPCcsICc+JylcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnJXFcXFxcfCcsXG4gICAgICAgIGVuZDogJ1xcXFx8J1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC88PC0nXFx3KyckLyxcbiAgICAgICAgZW5kOiAvXlxccypcXHcrJC9cbiAgICAgIH1cbiAgICBdLFxuICAgIHJlbGV2YW5jZTogMFxuICB9O1xuICBjb25zdCBSRUdFWFAgPSB7XG4gICAgYmVnaW46ICcoPyElXFxcXH0pKCcgKyBobGpzLlJFX1NUQVJURVJTX1JFICsgJ3xcXFxcbnxcXFxcYihjYXNlfGlmfHNlbGVjdHx1bmxlc3N8dW50aWx8d2hlbnx3aGlsZSlcXFxcYilcXFxccyonLFxuICAgIGtleXdvcmRzOiAnY2FzZSBpZiBzZWxlY3QgdW5sZXNzIHVudGlsIHdoZW4gd2hpbGUnLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3JlZ2V4cCcsXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgaGxqcy5CQUNLU0xBU0hfRVNDQVBFLFxuICAgICAgICAgIFNVQlNUXG4gICAgICAgIF0sXG4gICAgICAgIHZhcmlhbnRzOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgYmVnaW46ICcvL1thLXpdKicsXG4gICAgICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiAnLyg/IVxcXFwvKScsXG4gICAgICAgICAgICBlbmQ6ICcvW2Etel0qJ1xuICAgICAgICAgIH1cbiAgICAgICAgXVxuICAgICAgfVxuICAgIF0sXG4gICAgcmVsZXZhbmNlOiAwXG4gIH07XG4gIGNvbnN0IFJFR0VYUDIgPSB7XG4gICAgY2xhc3NOYW1lOiAncmVnZXhwJyxcbiAgICBjb250YWluczogW1xuICAgICAgaGxqcy5CQUNLU0xBU0hfRVNDQVBFLFxuICAgICAgU1VCU1RcbiAgICBdLFxuICAgIHZhcmlhbnRzOiBbXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnJXJcXFxcKCcsXG4gICAgICAgIGVuZDogJ1xcXFwpJyxcbiAgICAgICAgY29udGFpbnM6IHJlY3Vyc2l2ZVBhcmVuKCdcXFxcKCcsICdcXFxcKScpXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogJyVyXFxcXFsnLFxuICAgICAgICBlbmQ6ICdcXFxcXScsXG4gICAgICAgIGNvbnRhaW5zOiByZWN1cnNpdmVQYXJlbignXFxcXFsnLCAnXFxcXF0nKVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICclclxcXFx7JyxcbiAgICAgICAgZW5kOiAvXFx9LyxcbiAgICAgICAgY29udGFpbnM6IHJlY3Vyc2l2ZVBhcmVuKC9cXHsvLCAvXFx9LylcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnJXI8JyxcbiAgICAgICAgZW5kOiAnPicsXG4gICAgICAgIGNvbnRhaW5zOiByZWN1cnNpdmVQYXJlbignPCcsICc+JylcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnJXJcXFxcfCcsXG4gICAgICAgIGVuZDogJ1xcXFx8J1xuICAgICAgfVxuICAgIF0sXG4gICAgcmVsZXZhbmNlOiAwXG4gIH07XG4gIGNvbnN0IEFUVFJJQlVURSA9IHtcbiAgICBjbGFzc05hbWU6ICdtZXRhJyxcbiAgICBiZWdpbjogJ0BcXFxcWycsXG4gICAgZW5kOiAnXFxcXF0nLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBobGpzLmluaGVyaXQoaGxqcy5RVU9URV9TVFJJTkdfTU9ERSwge1xuICAgICAgICBjbGFzc05hbWU6ICdtZXRhLXN0cmluZydcbiAgICAgIH0pXG4gICAgXVxuICB9O1xuICBjb25zdCBDUllTVEFMX0RFRkFVTFRfQ09OVEFJTlMgPSBbXG4gICAgRVhQQU5TSU9OLFxuICAgIFNUUklORyxcbiAgICBRX1NUUklORyxcbiAgICBSRUdFWFAyLFxuICAgIFJFR0VYUCxcbiAgICBBVFRSSUJVVEUsXG4gICAgaGxqcy5IQVNIX0NPTU1FTlRfTU9ERSxcbiAgICB7XG4gICAgICBjbGFzc05hbWU6ICdjbGFzcycsXG4gICAgICBiZWdpbktleXdvcmRzOiAnY2xhc3MgbW9kdWxlIHN0cnVjdCcsXG4gICAgICBlbmQ6ICckfDsnLFxuICAgICAgaWxsZWdhbDogLz0vLFxuICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgaGxqcy5IQVNIX0NPTU1FTlRfTU9ERSxcbiAgICAgICAgaGxqcy5pbmhlcml0KGhsanMuVElUTEVfTU9ERSwge1xuICAgICAgICAgIGJlZ2luOiBDUllTVEFMX1BBVEhfUkVcbiAgICAgICAgfSksXG4gICAgICAgIHsgLy8gcmVsZXZhbmNlIGJvb3N0ZXIgZm9yIGluaGVyaXRhbmNlXG4gICAgICAgICAgYmVnaW46ICc8J1xuICAgICAgICB9XG4gICAgICBdXG4gICAgfSxcbiAgICB7XG4gICAgICBjbGFzc05hbWU6ICdjbGFzcycsXG4gICAgICBiZWdpbktleXdvcmRzOiAnbGliIGVudW0gdW5pb24nLFxuICAgICAgZW5kOiAnJHw7JyxcbiAgICAgIGlsbGVnYWw6IC89LyxcbiAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgIGhsanMuSEFTSF9DT01NRU5UX01PREUsXG4gICAgICAgIGhsanMuaW5oZXJpdChobGpzLlRJVExFX01PREUsIHtcbiAgICAgICAgICBiZWdpbjogQ1JZU1RBTF9QQVRIX1JFXG4gICAgICAgIH0pXG4gICAgICBdXG4gICAgfSxcbiAgICB7XG4gICAgICBiZWdpbktleXdvcmRzOiAnYW5ub3RhdGlvbicsXG4gICAgICBlbmQ6ICckfDsnLFxuICAgICAgaWxsZWdhbDogLz0vLFxuICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgaGxqcy5IQVNIX0NPTU1FTlRfTU9ERSxcbiAgICAgICAgaGxqcy5pbmhlcml0KGhsanMuVElUTEVfTU9ERSwge1xuICAgICAgICAgIGJlZ2luOiBDUllTVEFMX1BBVEhfUkVcbiAgICAgICAgfSlcbiAgICAgIF0sXG4gICAgICByZWxldmFuY2U6IDJcbiAgICB9LFxuICAgIHtcbiAgICAgIGNsYXNzTmFtZTogJ2Z1bmN0aW9uJyxcbiAgICAgIGJlZ2luS2V5d29yZHM6ICdkZWYnLFxuICAgICAgZW5kOiAvXFxCXFxiLyxcbiAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgIGhsanMuaW5oZXJpdChobGpzLlRJVExFX01PREUsIHtcbiAgICAgICAgICBiZWdpbjogQ1JZU1RBTF9NRVRIT0RfUkUsXG4gICAgICAgICAgZW5kc1BhcmVudDogdHJ1ZVxuICAgICAgICB9KVxuICAgICAgXVxuICAgIH0sXG4gICAge1xuICAgICAgY2xhc3NOYW1lOiAnZnVuY3Rpb24nLFxuICAgICAgYmVnaW5LZXl3b3JkczogJ2Z1biBtYWNybycsXG4gICAgICBlbmQ6IC9cXEJcXGIvLFxuICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgaGxqcy5pbmhlcml0KGhsanMuVElUTEVfTU9ERSwge1xuICAgICAgICAgIGJlZ2luOiBDUllTVEFMX01FVEhPRF9SRSxcbiAgICAgICAgICBlbmRzUGFyZW50OiB0cnVlXG4gICAgICAgIH0pXG4gICAgICBdLFxuICAgICAgcmVsZXZhbmNlOiAyXG4gICAgfSxcbiAgICB7XG4gICAgICBjbGFzc05hbWU6ICdzeW1ib2wnLFxuICAgICAgYmVnaW46IGhsanMuVU5ERVJTQ09SRV9JREVOVF9SRSArICcoIXxcXFxcPyk/OicsXG4gICAgICByZWxldmFuY2U6IDBcbiAgICB9LFxuICAgIHtcbiAgICAgIGNsYXNzTmFtZTogJ3N5bWJvbCcsXG4gICAgICBiZWdpbjogJzonLFxuICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgU1RSSU5HLFxuICAgICAgICB7XG4gICAgICAgICAgYmVnaW46IENSWVNUQUxfTUVUSE9EX1JFXG4gICAgICAgIH1cbiAgICAgIF0sXG4gICAgICByZWxldmFuY2U6IDBcbiAgICB9LFxuICAgIHtcbiAgICAgIGNsYXNzTmFtZTogJ251bWJlcicsXG4gICAgICB2YXJpYW50czogW1xuICAgICAgICB7XG4gICAgICAgICAgYmVnaW46ICdcXFxcYjBiKFswMV9dKyknICsgSU5UX1NVRkZJWFxuICAgICAgICB9LFxuICAgICAgICB7XG4gICAgICAgICAgYmVnaW46ICdcXFxcYjBvKFswLTdfXSspJyArIElOVF9TVUZGSVhcbiAgICAgICAgfSxcbiAgICAgICAge1xuICAgICAgICAgIGJlZ2luOiAnXFxcXGIweChbQS1GYS1mMC05X10rKScgKyBJTlRfU1VGRklYXG4gICAgICAgIH0sXG4gICAgICAgIHtcbiAgICAgICAgICBiZWdpbjogJ1xcXFxiKFsxLTldWzAtOV9dKlswLTldfFswLTldKShcXFxcLlswLTldWzAtOV9dKik/KFtlRV1fP1stK10/WzAtOV9dKik/JyArIEZMT0FUX1NVRkZJWCArICcoPyFfKSdcbiAgICAgICAgfSxcbiAgICAgICAge1xuICAgICAgICAgIGJlZ2luOiAnXFxcXGIoWzEtOV1bMC05X10qfDApJyArIElOVF9TVUZGSVhcbiAgICAgICAgfVxuICAgICAgXSxcbiAgICAgIHJlbGV2YW5jZTogMFxuICAgIH1cbiAgXTtcbiAgU1VCU1QuY29udGFpbnMgPSBDUllTVEFMX0RFRkFVTFRfQ09OVEFJTlM7XG4gIEVYUEFOU0lPTi5jb250YWlucyA9IENSWVNUQUxfREVGQVVMVF9DT05UQUlOUy5zbGljZSgxKTsgLy8gd2l0aG91dCBFWFBBTlNJT05cblxuICByZXR1cm4ge1xuICAgIG5hbWU6ICdDcnlzdGFsJyxcbiAgICBhbGlhc2VzOiBbICdjcicgXSxcbiAgICBrZXl3b3JkczogQ1JZU1RBTF9LRVlXT1JEUyxcbiAgICBjb250YWluczogQ1JZU1RBTF9ERUZBVUxUX0NPTlRBSU5TXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gY3J5c3RhbDtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==