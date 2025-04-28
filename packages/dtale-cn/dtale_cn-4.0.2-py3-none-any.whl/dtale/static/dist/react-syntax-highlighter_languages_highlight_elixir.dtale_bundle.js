(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_elixir"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/elixir.js":
/*!*************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/elixir.js ***!
  \*************************************************************************************************/
/***/ ((module) => {

/*
Language: Elixir
Author: Josh Adams <josh@isotope11.com>
Description: language definition for Elixir source code files (.ex and .exs).  Based on ruby language support.
Category: functional
Website: https://elixir-lang.org
*/

/** @type LanguageFn */
function elixir(hljs) {
  const ELIXIR_IDENT_RE = '[a-zA-Z_][a-zA-Z0-9_.]*(!|\\?)?';
  const ELIXIR_METHOD_RE = '[a-zA-Z_]\\w*[!?=]?|[-+~]@|<<|>>|=~|===?|<=>|[<>]=?|\\*\\*|[-/+%^&*~`|]|\\[\\]=?';
  const ELIXIR_KEYWORDS = {
    $pattern: ELIXIR_IDENT_RE,
    keyword: 'and false then defined module in return redo retry end for true self when ' +
    'next until do begin unless nil break not case cond alias while ensure or ' +
    'include use alias fn quote require import with|0'
  };
  const SUBST = {
    className: 'subst',
    begin: /#\{/,
    end: /\}/,
    keywords: ELIXIR_KEYWORDS
  };
  const NUMBER = {
    className: 'number',
    begin: '(\\b0o[0-7_]+)|(\\b0b[01_]+)|(\\b0x[0-9a-fA-F_]+)|(-?\\b[1-9][0-9_]*(\\.[0-9_]+([eE][-+]?[0-9]+)?)?)',
    relevance: 0
  };
  const SIGIL_DELIMITERS = '[/|([{<"\']';
  const LOWERCASE_SIGIL = {
    className: 'string',
    begin: '~[a-z]' + '(?=' + SIGIL_DELIMITERS + ')',
    contains: [
      {
        endsParent: true,
        contains: [
          {
            contains: [
              hljs.BACKSLASH_ESCAPE,
              SUBST
            ],
            variants: [
              {
                begin: /"/,
                end: /"/
              },
              {
                begin: /'/,
                end: /'/
              },
              {
                begin: /\//,
                end: /\//
              },
              {
                begin: /\|/,
                end: /\|/
              },
              {
                begin: /\(/,
                end: /\)/
              },
              {
                begin: /\[/,
                end: /\]/
              },
              {
                begin: /\{/,
                end: /\}/
              },
              {
                begin: /</,
                end: />/
              }
            ]
          }
        ]
      }
    ]
  };

  const UPCASE_SIGIL = {
    className: 'string',
    begin: '~[A-Z]' + '(?=' + SIGIL_DELIMITERS + ')',
    contains: [
      {
        begin: /"/,
        end: /"/
      },
      {
        begin: /'/,
        end: /'/
      },
      {
        begin: /\//,
        end: /\//
      },
      {
        begin: /\|/,
        end: /\|/
      },
      {
        begin: /\(/,
        end: /\)/
      },
      {
        begin: /\[/,
        end: /\]/
      },
      {
        begin: /\{/,
        end: /\}/
      },
      {
        begin: /</,
        end: />/
      }
    ]
  };

  const STRING = {
    className: 'string',
    contains: [
      hljs.BACKSLASH_ESCAPE,
      SUBST
    ],
    variants: [
      {
        begin: /"""/,
        end: /"""/
      },
      {
        begin: /'''/,
        end: /'''/
      },
      {
        begin: /~S"""/,
        end: /"""/,
        contains: [] // override default
      },
      {
        begin: /~S"/,
        end: /"/,
        contains: [] // override default
      },
      {
        begin: /~S'''/,
        end: /'''/,
        contains: [] // override default
      },
      {
        begin: /~S'/,
        end: /'/,
        contains: [] // override default
      },
      {
        begin: /'/,
        end: /'/
      },
      {
        begin: /"/,
        end: /"/
      }
    ]
  };
  const FUNCTION = {
    className: 'function',
    beginKeywords: 'def defp defmacro',
    end: /\B\b/, // the mode is ended by the title
    contains: [
      hljs.inherit(hljs.TITLE_MODE, {
        begin: ELIXIR_IDENT_RE,
        endsParent: true
      })
    ]
  };
  const CLASS = hljs.inherit(FUNCTION, {
    className: 'class',
    beginKeywords: 'defimpl defmodule defprotocol defrecord',
    end: /\bdo\b|$|;/
  });
  const ELIXIR_DEFAULT_CONTAINS = [
    STRING,
    UPCASE_SIGIL,
    LOWERCASE_SIGIL,
    hljs.HASH_COMMENT_MODE,
    CLASS,
    FUNCTION,
    {
      begin: '::'
    },
    {
      className: 'symbol',
      begin: ':(?![\\s:])',
      contains: [
        STRING,
        {
          begin: ELIXIR_METHOD_RE
        }
      ],
      relevance: 0
    },
    {
      className: 'symbol',
      begin: ELIXIR_IDENT_RE + ':(?!:)',
      relevance: 0
    },
    NUMBER,
    {
      className: 'variable',
      begin: '(\\$\\W)|((\\$|@@?)(\\w+))'
    },
    {
      begin: '->'
    },
    { // regexp container
      begin: '(' + hljs.RE_STARTERS_RE + ')\\s*',
      contains: [
        hljs.HASH_COMMENT_MODE,
        {
          // to prevent false regex triggers for the division function:
          // /:
          begin: /\/: (?=\d+\s*[,\]])/,
          relevance: 0,
          contains: [NUMBER]
        },
        {
          className: 'regexp',
          illegal: '\\n',
          contains: [
            hljs.BACKSLASH_ESCAPE,
            SUBST
          ],
          variants: [
            {
              begin: '/',
              end: '/[a-z]*'
            },
            {
              begin: '%r\\[',
              end: '\\][a-z]*'
            }
          ]
        }
      ],
      relevance: 0
    }
  ];
  SUBST.contains = ELIXIR_DEFAULT_CONTAINS;

  return {
    name: 'Elixir',
    keywords: ELIXIR_KEYWORDS,
    contains: ELIXIR_DEFAULT_CONTAINS
  };
}

module.exports = elixir;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfZWxpeGlyLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLGVBQWU7QUFDZixZQUFZO0FBQ1o7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxrQ0FBa0M7QUFDbEM7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxlQUFlO0FBQ2Y7QUFDQTtBQUNBO0FBQ0EsZUFBZTtBQUNmO0FBQ0E7QUFDQTtBQUNBLGVBQWU7QUFDZjtBQUNBO0FBQ0E7QUFDQSxlQUFlO0FBQ2Y7QUFDQTtBQUNBO0FBQ0EsZUFBZTtBQUNmO0FBQ0E7QUFDQTtBQUNBLGVBQWU7QUFDZjtBQUNBLDBCQUEwQjtBQUMxQix3QkFBd0I7QUFDeEIsZUFBZTtBQUNmO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQSxrQkFBa0I7QUFDbEIsZ0JBQWdCO0FBQ2hCLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxvQkFBb0I7QUFDcEIsR0FBRztBQUNIO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0EsS0FBSztBQUNMLE1BQU07QUFDTjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxTQUFTO0FBQ1Q7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvZWxpeGlyLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogRWxpeGlyXG5BdXRob3I6IEpvc2ggQWRhbXMgPGpvc2hAaXNvdG9wZTExLmNvbT5cbkRlc2NyaXB0aW9uOiBsYW5ndWFnZSBkZWZpbml0aW9uIGZvciBFbGl4aXIgc291cmNlIGNvZGUgZmlsZXMgKC5leCBhbmQgLmV4cykuICBCYXNlZCBvbiBydWJ5IGxhbmd1YWdlIHN1cHBvcnQuXG5DYXRlZ29yeTogZnVuY3Rpb25hbFxuV2Vic2l0ZTogaHR0cHM6Ly9lbGl4aXItbGFuZy5vcmdcbiovXG5cbi8qKiBAdHlwZSBMYW5ndWFnZUZuICovXG5mdW5jdGlvbiBlbGl4aXIoaGxqcykge1xuICBjb25zdCBFTElYSVJfSURFTlRfUkUgPSAnW2EtekEtWl9dW2EtekEtWjAtOV8uXSooIXxcXFxcPyk/JztcbiAgY29uc3QgRUxJWElSX01FVEhPRF9SRSA9ICdbYS16QS1aX11cXFxcdypbIT89XT98Wy0rfl1AfDw8fD4+fD1+fD09PT98PD0+fFs8Pl09P3xcXFxcKlxcXFwqfFstLyslXiYqfmB8XXxcXFxcW1xcXFxdPT8nO1xuICBjb25zdCBFTElYSVJfS0VZV09SRFMgPSB7XG4gICAgJHBhdHRlcm46IEVMSVhJUl9JREVOVF9SRSxcbiAgICBrZXl3b3JkOiAnYW5kIGZhbHNlIHRoZW4gZGVmaW5lZCBtb2R1bGUgaW4gcmV0dXJuIHJlZG8gcmV0cnkgZW5kIGZvciB0cnVlIHNlbGYgd2hlbiAnICtcbiAgICAnbmV4dCB1bnRpbCBkbyBiZWdpbiB1bmxlc3MgbmlsIGJyZWFrIG5vdCBjYXNlIGNvbmQgYWxpYXMgd2hpbGUgZW5zdXJlIG9yICcgK1xuICAgICdpbmNsdWRlIHVzZSBhbGlhcyBmbiBxdW90ZSByZXF1aXJlIGltcG9ydCB3aXRofDAnXG4gIH07XG4gIGNvbnN0IFNVQlNUID0ge1xuICAgIGNsYXNzTmFtZTogJ3N1YnN0JyxcbiAgICBiZWdpbjogLyNcXHsvLFxuICAgIGVuZDogL1xcfS8sXG4gICAga2V5d29yZHM6IEVMSVhJUl9LRVlXT1JEU1xuICB9O1xuICBjb25zdCBOVU1CRVIgPSB7XG4gICAgY2xhc3NOYW1lOiAnbnVtYmVyJyxcbiAgICBiZWdpbjogJyhcXFxcYjBvWzAtN19dKyl8KFxcXFxiMGJbMDFfXSspfChcXFxcYjB4WzAtOWEtZkEtRl9dKyl8KC0/XFxcXGJbMS05XVswLTlfXSooXFxcXC5bMC05X10rKFtlRV1bLStdP1swLTldKyk/KT8pJyxcbiAgICByZWxldmFuY2U6IDBcbiAgfTtcbiAgY29uc3QgU0lHSUxfREVMSU1JVEVSUyA9ICdbL3woW3s8XCJcXCddJztcbiAgY29uc3QgTE9XRVJDQVNFX1NJR0lMID0ge1xuICAgIGNsYXNzTmFtZTogJ3N0cmluZycsXG4gICAgYmVnaW46ICd+W2Etel0nICsgJyg/PScgKyBTSUdJTF9ERUxJTUlURVJTICsgJyknLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICB7XG4gICAgICAgIGVuZHNQYXJlbnQ6IHRydWUsXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICAgICAgaGxqcy5CQUNLU0xBU0hfRVNDQVBFLFxuICAgICAgICAgICAgICBTVUJTVFxuICAgICAgICAgICAgXSxcbiAgICAgICAgICAgIHZhcmlhbnRzOiBbXG4gICAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgICBiZWdpbjogL1wiLyxcbiAgICAgICAgICAgICAgICBlbmQ6IC9cIi9cbiAgICAgICAgICAgICAgfSxcbiAgICAgICAgICAgICAge1xuICAgICAgICAgICAgICAgIGJlZ2luOiAvJy8sXG4gICAgICAgICAgICAgICAgZW5kOiAvJy9cbiAgICAgICAgICAgICAgfSxcbiAgICAgICAgICAgICAge1xuICAgICAgICAgICAgICAgIGJlZ2luOiAvXFwvLyxcbiAgICAgICAgICAgICAgICBlbmQ6IC9cXC8vXG4gICAgICAgICAgICAgIH0sXG4gICAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgICBiZWdpbjogL1xcfC8sXG4gICAgICAgICAgICAgICAgZW5kOiAvXFx8L1xuICAgICAgICAgICAgICB9LFxuICAgICAgICAgICAgICB7XG4gICAgICAgICAgICAgICAgYmVnaW46IC9cXCgvLFxuICAgICAgICAgICAgICAgIGVuZDogL1xcKS9cbiAgICAgICAgICAgICAgfSxcbiAgICAgICAgICAgICAge1xuICAgICAgICAgICAgICAgIGJlZ2luOiAvXFxbLyxcbiAgICAgICAgICAgICAgICBlbmQ6IC9cXF0vXG4gICAgICAgICAgICAgIH0sXG4gICAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgICBiZWdpbjogL1xcey8sXG4gICAgICAgICAgICAgICAgZW5kOiAvXFx9L1xuICAgICAgICAgICAgICB9LFxuICAgICAgICAgICAgICB7XG4gICAgICAgICAgICAgICAgYmVnaW46IC88LyxcbiAgICAgICAgICAgICAgICBlbmQ6IC8+L1xuICAgICAgICAgICAgICB9XG4gICAgICAgICAgICBdXG4gICAgICAgICAgfVxuICAgICAgICBdXG4gICAgICB9XG4gICAgXVxuICB9O1xuXG4gIGNvbnN0IFVQQ0FTRV9TSUdJTCA9IHtcbiAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgIGJlZ2luOiAnfltBLVpdJyArICcoPz0nICsgU0lHSUxfREVMSU1JVEVSUyArICcpJyxcbiAgICBjb250YWluczogW1xuICAgICAge1xuICAgICAgICBiZWdpbjogL1wiLyxcbiAgICAgICAgZW5kOiAvXCIvXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogLycvLFxuICAgICAgICBlbmQ6IC8nL1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC9cXC8vLFxuICAgICAgICBlbmQ6IC9cXC8vXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogL1xcfC8sXG4gICAgICAgIGVuZDogL1xcfC9cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAvXFwoLyxcbiAgICAgICAgZW5kOiAvXFwpL1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC9cXFsvLFxuICAgICAgICBlbmQ6IC9cXF0vXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogL1xcey8sXG4gICAgICAgIGVuZDogL1xcfS9cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAvPC8sXG4gICAgICAgIGVuZDogLz4vXG4gICAgICB9XG4gICAgXVxuICB9O1xuXG4gIGNvbnN0IFNUUklORyA9IHtcbiAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBobGpzLkJBQ0tTTEFTSF9FU0NBUEUsXG4gICAgICBTVUJTVFxuICAgIF0sXG4gICAgdmFyaWFudHM6IFtcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC9cIlwiXCIvLFxuICAgICAgICBlbmQ6IC9cIlwiXCIvXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogLycnJy8sXG4gICAgICAgIGVuZDogLycnJy9cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAvflNcIlwiXCIvLFxuICAgICAgICBlbmQ6IC9cIlwiXCIvLFxuICAgICAgICBjb250YWluczogW10gLy8gb3ZlcnJpZGUgZGVmYXVsdFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC9+U1wiLyxcbiAgICAgICAgZW5kOiAvXCIvLFxuICAgICAgICBjb250YWluczogW10gLy8gb3ZlcnJpZGUgZGVmYXVsdFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC9+UycnJy8sXG4gICAgICAgIGVuZDogLycnJy8sXG4gICAgICAgIGNvbnRhaW5zOiBbXSAvLyBvdmVycmlkZSBkZWZhdWx0XG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogL35TJy8sXG4gICAgICAgIGVuZDogLycvLFxuICAgICAgICBjb250YWluczogW10gLy8gb3ZlcnJpZGUgZGVmYXVsdFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC8nLyxcbiAgICAgICAgZW5kOiAvJy9cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAvXCIvLFxuICAgICAgICBlbmQ6IC9cIi9cbiAgICAgIH1cbiAgICBdXG4gIH07XG4gIGNvbnN0IEZVTkNUSU9OID0ge1xuICAgIGNsYXNzTmFtZTogJ2Z1bmN0aW9uJyxcbiAgICBiZWdpbktleXdvcmRzOiAnZGVmIGRlZnAgZGVmbWFjcm8nLFxuICAgIGVuZDogL1xcQlxcYi8sIC8vIHRoZSBtb2RlIGlzIGVuZGVkIGJ5IHRoZSB0aXRsZVxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBobGpzLmluaGVyaXQoaGxqcy5USVRMRV9NT0RFLCB7XG4gICAgICAgIGJlZ2luOiBFTElYSVJfSURFTlRfUkUsXG4gICAgICAgIGVuZHNQYXJlbnQ6IHRydWVcbiAgICAgIH0pXG4gICAgXVxuICB9O1xuICBjb25zdCBDTEFTUyA9IGhsanMuaW5oZXJpdChGVU5DVElPTiwge1xuICAgIGNsYXNzTmFtZTogJ2NsYXNzJyxcbiAgICBiZWdpbktleXdvcmRzOiAnZGVmaW1wbCBkZWZtb2R1bGUgZGVmcHJvdG9jb2wgZGVmcmVjb3JkJyxcbiAgICBlbmQ6IC9cXGJkb1xcYnwkfDsvXG4gIH0pO1xuICBjb25zdCBFTElYSVJfREVGQVVMVF9DT05UQUlOUyA9IFtcbiAgICBTVFJJTkcsXG4gICAgVVBDQVNFX1NJR0lMLFxuICAgIExPV0VSQ0FTRV9TSUdJTCxcbiAgICBobGpzLkhBU0hfQ09NTUVOVF9NT0RFLFxuICAgIENMQVNTLFxuICAgIEZVTkNUSU9OLFxuICAgIHtcbiAgICAgIGJlZ2luOiAnOjonXG4gICAgfSxcbiAgICB7XG4gICAgICBjbGFzc05hbWU6ICdzeW1ib2wnLFxuICAgICAgYmVnaW46ICc6KD8hW1xcXFxzOl0pJyxcbiAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgIFNUUklORyxcbiAgICAgICAge1xuICAgICAgICAgIGJlZ2luOiBFTElYSVJfTUVUSE9EX1JFXG4gICAgICAgIH1cbiAgICAgIF0sXG4gICAgICByZWxldmFuY2U6IDBcbiAgICB9LFxuICAgIHtcbiAgICAgIGNsYXNzTmFtZTogJ3N5bWJvbCcsXG4gICAgICBiZWdpbjogRUxJWElSX0lERU5UX1JFICsgJzooPyE6KScsXG4gICAgICByZWxldmFuY2U6IDBcbiAgICB9LFxuICAgIE5VTUJFUixcbiAgICB7XG4gICAgICBjbGFzc05hbWU6ICd2YXJpYWJsZScsXG4gICAgICBiZWdpbjogJyhcXFxcJFxcXFxXKXwoKFxcXFwkfEBAPykoXFxcXHcrKSknXG4gICAgfSxcbiAgICB7XG4gICAgICBiZWdpbjogJy0+J1xuICAgIH0sXG4gICAgeyAvLyByZWdleHAgY29udGFpbmVyXG4gICAgICBiZWdpbjogJygnICsgaGxqcy5SRV9TVEFSVEVSU19SRSArICcpXFxcXHMqJyxcbiAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgIGhsanMuSEFTSF9DT01NRU5UX01PREUsXG4gICAgICAgIHtcbiAgICAgICAgICAvLyB0byBwcmV2ZW50IGZhbHNlIHJlZ2V4IHRyaWdnZXJzIGZvciB0aGUgZGl2aXNpb24gZnVuY3Rpb246XG4gICAgICAgICAgLy8gLzpcbiAgICAgICAgICBiZWdpbjogL1xcLzogKD89XFxkK1xccypbLFxcXV0pLyxcbiAgICAgICAgICByZWxldmFuY2U6IDAsXG4gICAgICAgICAgY29udGFpbnM6IFtOVU1CRVJdXG4gICAgICAgIH0sXG4gICAgICAgIHtcbiAgICAgICAgICBjbGFzc05hbWU6ICdyZWdleHAnLFxuICAgICAgICAgIGlsbGVnYWw6ICdcXFxcbicsXG4gICAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICAgIGhsanMuQkFDS1NMQVNIX0VTQ0FQRSxcbiAgICAgICAgICAgIFNVQlNUXG4gICAgICAgICAgXSxcbiAgICAgICAgICB2YXJpYW50czogW1xuICAgICAgICAgICAge1xuICAgICAgICAgICAgICBiZWdpbjogJy8nLFxuICAgICAgICAgICAgICBlbmQ6ICcvW2Etel0qJ1xuICAgICAgICAgICAgfSxcbiAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgYmVnaW46ICclclxcXFxbJyxcbiAgICAgICAgICAgICAgZW5kOiAnXFxcXF1bYS16XSonXG4gICAgICAgICAgICB9XG4gICAgICAgICAgXVxuICAgICAgICB9XG4gICAgICBdLFxuICAgICAgcmVsZXZhbmNlOiAwXG4gICAgfVxuICBdO1xuICBTVUJTVC5jb250YWlucyA9IEVMSVhJUl9ERUZBVUxUX0NPTlRBSU5TO1xuXG4gIHJldHVybiB7XG4gICAgbmFtZTogJ0VsaXhpcicsXG4gICAga2V5d29yZHM6IEVMSVhJUl9LRVlXT1JEUyxcbiAgICBjb250YWluczogRUxJWElSX0RFRkFVTFRfQ09OVEFJTlNcbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBlbGl4aXI7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=