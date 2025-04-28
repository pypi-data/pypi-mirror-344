(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_reasonml"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/reasonml.js":
/*!***************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/reasonml.js ***!
  \***************************************************************************************************/
/***/ ((module) => {

/*
Language: ReasonML
Description: Reason lets you write simple, fast and quality type safe code while leveraging both the JavaScript & OCaml ecosystems.
Website: https://reasonml.github.io
Author: Gidi Meir Morris <oss@gidi.io>
Category: functional
*/
function reasonml(hljs) {
  function orReValues(ops) {
    return ops
      .map(function(op) {
        return op
          .split('')
          .map(function(char) {
            return '\\' + char;
          })
          .join('');
      })
      .join('|');
  }

  const RE_IDENT = '~?[a-z$_][0-9a-zA-Z$_]*';
  const RE_MODULE_IDENT = '`?[A-Z$_][0-9a-zA-Z$_]*';

  const RE_PARAM_TYPEPARAM = '\'?[a-z$_][0-9a-z$_]*';
  const RE_PARAM_TYPE = '\\s*:\\s*[a-z$_][0-9a-z$_]*(\\(\\s*(' + RE_PARAM_TYPEPARAM + '\\s*(,' + RE_PARAM_TYPEPARAM + '\\s*)*)?\\))?';
  const RE_PARAM = RE_IDENT + '(' + RE_PARAM_TYPE + '){0,2}';
  const RE_OPERATOR = "(" + orReValues([
    '||',
    '++',
    '**',
    '+.',
    '*',
    '/',
    '*.',
    '/.',
    '...'
  ]) + "|\\|>|&&|==|===)";
  const RE_OPERATOR_SPACED = "\\s+" + RE_OPERATOR + "\\s+";

  const KEYWORDS = {
    keyword:
      'and as asr assert begin class constraint do done downto else end exception external ' +
      'for fun function functor if in include inherit initializer ' +
      'land lazy let lor lsl lsr lxor match method mod module mutable new nonrec ' +
      'object of open or private rec sig struct then to try type val virtual when while with',
    built_in:
      'array bool bytes char exn|5 float int int32 int64 list lazy_t|5 nativeint|5 ref string unit ',
    literal:
      'true false'
  };

  const RE_NUMBER = '\\b(0[xX][a-fA-F0-9_]+[Lln]?|' +
    '0[oO][0-7_]+[Lln]?|' +
    '0[bB][01_]+[Lln]?|' +
    '[0-9][0-9_]*([Lln]|(\\.[0-9_]*)?([eE][-+]?[0-9_]+)?)?)';

  const NUMBER_MODE = {
    className: 'number',
    relevance: 0,
    variants: [
      {
        begin: RE_NUMBER
      },
      {
        begin: '\\(-' + RE_NUMBER + '\\)'
      }
    ]
  };

  const OPERATOR_MODE = {
    className: 'operator',
    relevance: 0,
    begin: RE_OPERATOR
  };
  const LIST_CONTENTS_MODES = [
    {
      className: 'identifier',
      relevance: 0,
      begin: RE_IDENT
    },
    OPERATOR_MODE,
    NUMBER_MODE
  ];

  const MODULE_ACCESS_CONTENTS = [
    hljs.QUOTE_STRING_MODE,
    OPERATOR_MODE,
    {
      className: 'module',
      begin: "\\b" + RE_MODULE_IDENT,
      returnBegin: true,
      end: "\.",
      contains: [
        {
          className: 'identifier',
          begin: RE_MODULE_IDENT,
          relevance: 0
        }
      ]
    }
  ];

  const PARAMS_CONTENTS = [
    {
      className: 'module',
      begin: "\\b" + RE_MODULE_IDENT,
      returnBegin: true,
      end: "\.",
      relevance: 0,
      contains: [
        {
          className: 'identifier',
          begin: RE_MODULE_IDENT,
          relevance: 0
        }
      ]
    }
  ];

  const PARAMS_MODE = {
    begin: RE_IDENT,
    end: '(,|\\n|\\))',
    relevance: 0,
    contains: [
      OPERATOR_MODE,
      {
        className: 'typing',
        begin: ':',
        end: '(,|\\n)',
        returnBegin: true,
        relevance: 0,
        contains: PARAMS_CONTENTS
      }
    ]
  };

  const FUNCTION_BLOCK_MODE = {
    className: 'function',
    relevance: 0,
    keywords: KEYWORDS,
    variants: [
      {
        begin: '\\s(\\(\\.?.*?\\)|' + RE_IDENT + ')\\s*=>',
        end: '\\s*=>',
        returnBegin: true,
        relevance: 0,
        contains: [
          {
            className: 'params',
            variants: [
              {
                begin: RE_IDENT
              },
              {
                begin: RE_PARAM
              },
              {
                begin: /\(\s*\)/
              }
            ]
          }
        ]
      },
      {
        begin: '\\s\\(\\.?[^;\\|]*\\)\\s*=>',
        end: '\\s=>',
        returnBegin: true,
        relevance: 0,
        contains: [
          {
            className: 'params',
            relevance: 0,
            variants: [ PARAMS_MODE ]
          }
        ]
      },
      {
        begin: '\\(\\.\\s' + RE_IDENT + '\\)\\s*=>'
      }
    ]
  };
  MODULE_ACCESS_CONTENTS.push(FUNCTION_BLOCK_MODE);

  const CONSTRUCTOR_MODE = {
    className: 'constructor',
    begin: RE_MODULE_IDENT + '\\(',
    end: '\\)',
    illegal: '\\n',
    keywords: KEYWORDS,
    contains: [
      hljs.QUOTE_STRING_MODE,
      OPERATOR_MODE,
      {
        className: 'params',
        begin: '\\b' + RE_IDENT
      }
    ]
  };

  const PATTERN_MATCH_BLOCK_MODE = {
    className: 'pattern-match',
    begin: '\\|',
    returnBegin: true,
    keywords: KEYWORDS,
    end: '=>',
    relevance: 0,
    contains: [
      CONSTRUCTOR_MODE,
      OPERATOR_MODE,
      {
        relevance: 0,
        className: 'constructor',
        begin: RE_MODULE_IDENT
      }
    ]
  };

  const MODULE_ACCESS_MODE = {
    className: 'module-access',
    keywords: KEYWORDS,
    returnBegin: true,
    variants: [
      {
        begin: "\\b(" + RE_MODULE_IDENT + "\\.)+" + RE_IDENT
      },
      {
        begin: "\\b(" + RE_MODULE_IDENT + "\\.)+\\(",
        end: "\\)",
        returnBegin: true,
        contains: [
          FUNCTION_BLOCK_MODE,
          {
            begin: '\\(',
            end: '\\)',
            skip: true
          }
        ].concat(MODULE_ACCESS_CONTENTS)
      },
      {
        begin: "\\b(" + RE_MODULE_IDENT + "\\.)+\\{",
        end: /\}/
      }
    ],
    contains: MODULE_ACCESS_CONTENTS
  };

  PARAMS_CONTENTS.push(MODULE_ACCESS_MODE);

  return {
    name: 'ReasonML',
    aliases: [ 're' ],
    keywords: KEYWORDS,
    illegal: '(:-|:=|\\$\\{|\\+=)',
    contains: [
      hljs.COMMENT('/\\*', '\\*/', {
        illegal: '^(#,\\/\\/)'
      }),
      {
        className: 'character',
        begin: '\'(\\\\[^\']+|[^\'])\'',
        illegal: '\\n',
        relevance: 0
      },
      hljs.QUOTE_STRING_MODE,
      {
        className: 'literal',
        begin: '\\(\\)',
        relevance: 0
      },
      {
        className: 'literal',
        begin: '\\[\\|',
        end: '\\|\\]',
        relevance: 0,
        contains: LIST_CONTENTS_MODES
      },
      {
        className: 'literal',
        begin: '\\[',
        end: '\\]',
        relevance: 0,
        contains: LIST_CONTENTS_MODES
      },
      CONSTRUCTOR_MODE,
      {
        className: 'operator',
        begin: RE_OPERATOR_SPACED,
        illegal: '-->',
        relevance: 0
      },
      NUMBER_MODE,
      hljs.C_LINE_COMMENT_MODE,
      PATTERN_MATCH_BLOCK_MODE,
      FUNCTION_BLOCK_MODE,
      {
        className: 'module-def',
        begin: "\\bmodule\\s+" + RE_IDENT + "\\s+" + RE_MODULE_IDENT + "\\s+=\\s+\\{",
        end: /\}/,
        returnBegin: true,
        keywords: KEYWORDS,
        relevance: 0,
        contains: [
          {
            className: 'module',
            relevance: 0,
            begin: RE_MODULE_IDENT
          },
          {
            begin: /\{/,
            end: /\}/,
            skip: true
          }
        ].concat(MODULE_ACCESS_CONTENTS)
      },
      MODULE_ACCESS_MODE
    ]
  };
}

module.exports = reasonml;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfcmVhc29ubWwuZHRhbGVfYnVuZGxlLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsV0FBVztBQUNYO0FBQ0EsT0FBTztBQUNQO0FBQ0E7O0FBRUE7QUFDQTs7QUFFQTtBQUNBO0FBQ0EsdURBQXVELElBQUk7QUFDM0Q7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxlQUFlO0FBQ2Y7QUFDQTtBQUNBLGVBQWU7QUFDZjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQSw2QkFBNkI7QUFDN0I7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBLG1EQUFtRDtBQUNuRCxnQkFBZ0I7QUFDaEI7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQSwyQkFBMkI7QUFDM0I7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxvRkFBb0Y7QUFDcEYsZ0JBQWdCO0FBQ2hCO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQSxzQkFBc0I7QUFDdEIsb0JBQW9CO0FBQ3BCO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvcmVhc29ubWwuanMiXSwic291cmNlc0NvbnRlbnQiOlsiLypcbkxhbmd1YWdlOiBSZWFzb25NTFxuRGVzY3JpcHRpb246IFJlYXNvbiBsZXRzIHlvdSB3cml0ZSBzaW1wbGUsIGZhc3QgYW5kIHF1YWxpdHkgdHlwZSBzYWZlIGNvZGUgd2hpbGUgbGV2ZXJhZ2luZyBib3RoIHRoZSBKYXZhU2NyaXB0ICYgT0NhbWwgZWNvc3lzdGVtcy5cbldlYnNpdGU6IGh0dHBzOi8vcmVhc29ubWwuZ2l0aHViLmlvXG5BdXRob3I6IEdpZGkgTWVpciBNb3JyaXMgPG9zc0BnaWRpLmlvPlxuQ2F0ZWdvcnk6IGZ1bmN0aW9uYWxcbiovXG5mdW5jdGlvbiByZWFzb25tbChobGpzKSB7XG4gIGZ1bmN0aW9uIG9yUmVWYWx1ZXMob3BzKSB7XG4gICAgcmV0dXJuIG9wc1xuICAgICAgLm1hcChmdW5jdGlvbihvcCkge1xuICAgICAgICByZXR1cm4gb3BcbiAgICAgICAgICAuc3BsaXQoJycpXG4gICAgICAgICAgLm1hcChmdW5jdGlvbihjaGFyKSB7XG4gICAgICAgICAgICByZXR1cm4gJ1xcXFwnICsgY2hhcjtcbiAgICAgICAgICB9KVxuICAgICAgICAgIC5qb2luKCcnKTtcbiAgICAgIH0pXG4gICAgICAuam9pbignfCcpO1xuICB9XG5cbiAgY29uc3QgUkVfSURFTlQgPSAnfj9bYS16JF9dWzAtOWEtekEtWiRfXSonO1xuICBjb25zdCBSRV9NT0RVTEVfSURFTlQgPSAnYD9bQS1aJF9dWzAtOWEtekEtWiRfXSonO1xuXG4gIGNvbnN0IFJFX1BBUkFNX1RZUEVQQVJBTSA9ICdcXCc/W2EteiRfXVswLTlhLXokX10qJztcbiAgY29uc3QgUkVfUEFSQU1fVFlQRSA9ICdcXFxccyo6XFxcXHMqW2EteiRfXVswLTlhLXokX10qKFxcXFwoXFxcXHMqKCcgKyBSRV9QQVJBTV9UWVBFUEFSQU0gKyAnXFxcXHMqKCwnICsgUkVfUEFSQU1fVFlQRVBBUkFNICsgJ1xcXFxzKikqKT9cXFxcKSk/JztcbiAgY29uc3QgUkVfUEFSQU0gPSBSRV9JREVOVCArICcoJyArIFJFX1BBUkFNX1RZUEUgKyAnKXswLDJ9JztcbiAgY29uc3QgUkVfT1BFUkFUT1IgPSBcIihcIiArIG9yUmVWYWx1ZXMoW1xuICAgICd8fCcsXG4gICAgJysrJyxcbiAgICAnKionLFxuICAgICcrLicsXG4gICAgJyonLFxuICAgICcvJyxcbiAgICAnKi4nLFxuICAgICcvLicsXG4gICAgJy4uLidcbiAgXSkgKyBcInxcXFxcfD58JiZ8PT18PT09KVwiO1xuICBjb25zdCBSRV9PUEVSQVRPUl9TUEFDRUQgPSBcIlxcXFxzK1wiICsgUkVfT1BFUkFUT1IgKyBcIlxcXFxzK1wiO1xuXG4gIGNvbnN0IEtFWVdPUkRTID0ge1xuICAgIGtleXdvcmQ6XG4gICAgICAnYW5kIGFzIGFzciBhc3NlcnQgYmVnaW4gY2xhc3MgY29uc3RyYWludCBkbyBkb25lIGRvd250byBlbHNlIGVuZCBleGNlcHRpb24gZXh0ZXJuYWwgJyArXG4gICAgICAnZm9yIGZ1biBmdW5jdGlvbiBmdW5jdG9yIGlmIGluIGluY2x1ZGUgaW5oZXJpdCBpbml0aWFsaXplciAnICtcbiAgICAgICdsYW5kIGxhenkgbGV0IGxvciBsc2wgbHNyIGx4b3IgbWF0Y2ggbWV0aG9kIG1vZCBtb2R1bGUgbXV0YWJsZSBuZXcgbm9ucmVjICcgK1xuICAgICAgJ29iamVjdCBvZiBvcGVuIG9yIHByaXZhdGUgcmVjIHNpZyBzdHJ1Y3QgdGhlbiB0byB0cnkgdHlwZSB2YWwgdmlydHVhbCB3aGVuIHdoaWxlIHdpdGgnLFxuICAgIGJ1aWx0X2luOlxuICAgICAgJ2FycmF5IGJvb2wgYnl0ZXMgY2hhciBleG58NSBmbG9hdCBpbnQgaW50MzIgaW50NjQgbGlzdCBsYXp5X3R8NSBuYXRpdmVpbnR8NSByZWYgc3RyaW5nIHVuaXQgJyxcbiAgICBsaXRlcmFsOlxuICAgICAgJ3RydWUgZmFsc2UnXG4gIH07XG5cbiAgY29uc3QgUkVfTlVNQkVSID0gJ1xcXFxiKDBbeFhdW2EtZkEtRjAtOV9dK1tMbG5dP3wnICtcbiAgICAnMFtvT11bMC03X10rW0xsbl0/fCcgK1xuICAgICcwW2JCXVswMV9dK1tMbG5dP3wnICtcbiAgICAnWzAtOV1bMC05X10qKFtMbG5dfChcXFxcLlswLTlfXSopPyhbZUVdWy0rXT9bMC05X10rKT8pPyknO1xuXG4gIGNvbnN0IE5VTUJFUl9NT0RFID0ge1xuICAgIGNsYXNzTmFtZTogJ251bWJlcicsXG4gICAgcmVsZXZhbmNlOiAwLFxuICAgIHZhcmlhbnRzOiBbXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiBSRV9OVU1CRVJcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnXFxcXCgtJyArIFJFX05VTUJFUiArICdcXFxcKSdcbiAgICAgIH1cbiAgICBdXG4gIH07XG5cbiAgY29uc3QgT1BFUkFUT1JfTU9ERSA9IHtcbiAgICBjbGFzc05hbWU6ICdvcGVyYXRvcicsXG4gICAgcmVsZXZhbmNlOiAwLFxuICAgIGJlZ2luOiBSRV9PUEVSQVRPUlxuICB9O1xuICBjb25zdCBMSVNUX0NPTlRFTlRTX01PREVTID0gW1xuICAgIHtcbiAgICAgIGNsYXNzTmFtZTogJ2lkZW50aWZpZXInLFxuICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgYmVnaW46IFJFX0lERU5UXG4gICAgfSxcbiAgICBPUEVSQVRPUl9NT0RFLFxuICAgIE5VTUJFUl9NT0RFXG4gIF07XG5cbiAgY29uc3QgTU9EVUxFX0FDQ0VTU19DT05URU5UUyA9IFtcbiAgICBobGpzLlFVT1RFX1NUUklOR19NT0RFLFxuICAgIE9QRVJBVE9SX01PREUsXG4gICAge1xuICAgICAgY2xhc3NOYW1lOiAnbW9kdWxlJyxcbiAgICAgIGJlZ2luOiBcIlxcXFxiXCIgKyBSRV9NT0RVTEVfSURFTlQsXG4gICAgICByZXR1cm5CZWdpbjogdHJ1ZSxcbiAgICAgIGVuZDogXCJcXC5cIixcbiAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgIHtcbiAgICAgICAgICBjbGFzc05hbWU6ICdpZGVudGlmaWVyJyxcbiAgICAgICAgICBiZWdpbjogUkVfTU9EVUxFX0lERU5ULFxuICAgICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgICB9XG4gICAgICBdXG4gICAgfVxuICBdO1xuXG4gIGNvbnN0IFBBUkFNU19DT05URU5UUyA9IFtcbiAgICB7XG4gICAgICBjbGFzc05hbWU6ICdtb2R1bGUnLFxuICAgICAgYmVnaW46IFwiXFxcXGJcIiArIFJFX01PRFVMRV9JREVOVCxcbiAgICAgIHJldHVybkJlZ2luOiB0cnVlLFxuICAgICAgZW5kOiBcIlxcLlwiLFxuICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgY29udGFpbnM6IFtcbiAgICAgICAge1xuICAgICAgICAgIGNsYXNzTmFtZTogJ2lkZW50aWZpZXInLFxuICAgICAgICAgIGJlZ2luOiBSRV9NT0RVTEVfSURFTlQsXG4gICAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICAgIH1cbiAgICAgIF1cbiAgICB9XG4gIF07XG5cbiAgY29uc3QgUEFSQU1TX01PREUgPSB7XG4gICAgYmVnaW46IFJFX0lERU5ULFxuICAgIGVuZDogJygsfFxcXFxufFxcXFwpKScsXG4gICAgcmVsZXZhbmNlOiAwLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBPUEVSQVRPUl9NT0RFLFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICd0eXBpbmcnLFxuICAgICAgICBiZWdpbjogJzonLFxuICAgICAgICBlbmQ6ICcoLHxcXFxcbiknLFxuICAgICAgICByZXR1cm5CZWdpbjogdHJ1ZSxcbiAgICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgICBjb250YWluczogUEFSQU1TX0NPTlRFTlRTXG4gICAgICB9XG4gICAgXVxuICB9O1xuXG4gIGNvbnN0IEZVTkNUSU9OX0JMT0NLX01PREUgPSB7XG4gICAgY2xhc3NOYW1lOiAnZnVuY3Rpb24nLFxuICAgIHJlbGV2YW5jZTogMCxcbiAgICBrZXl3b3JkczogS0VZV09SRFMsXG4gICAgdmFyaWFudHM6IFtcbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICdcXFxccyhcXFxcKFxcXFwuPy4qP1xcXFwpfCcgKyBSRV9JREVOVCArICcpXFxcXHMqPT4nLFxuICAgICAgICBlbmQ6ICdcXFxccyo9PicsXG4gICAgICAgIHJldHVybkJlZ2luOiB0cnVlLFxuICAgICAgICByZWxldmFuY2U6IDAsXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgY2xhc3NOYW1lOiAncGFyYW1zJyxcbiAgICAgICAgICAgIHZhcmlhbnRzOiBbXG4gICAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgICBiZWdpbjogUkVfSURFTlRcbiAgICAgICAgICAgICAgfSxcbiAgICAgICAgICAgICAge1xuICAgICAgICAgICAgICAgIGJlZ2luOiBSRV9QQVJBTVxuICAgICAgICAgICAgICB9LFxuICAgICAgICAgICAgICB7XG4gICAgICAgICAgICAgICAgYmVnaW46IC9cXChcXHMqXFwpL1xuICAgICAgICAgICAgICB9XG4gICAgICAgICAgICBdXG4gICAgICAgICAgfVxuICAgICAgICBdXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogJ1xcXFxzXFxcXChcXFxcLj9bXjtcXFxcfF0qXFxcXClcXFxccyo9PicsXG4gICAgICAgIGVuZDogJ1xcXFxzPT4nLFxuICAgICAgICByZXR1cm5CZWdpbjogdHJ1ZSxcbiAgICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIGNsYXNzTmFtZTogJ3BhcmFtcycsXG4gICAgICAgICAgICByZWxldmFuY2U6IDAsXG4gICAgICAgICAgICB2YXJpYW50czogWyBQQVJBTVNfTU9ERSBdXG4gICAgICAgICAgfVxuICAgICAgICBdXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogJ1xcXFwoXFxcXC5cXFxccycgKyBSRV9JREVOVCArICdcXFxcKVxcXFxzKj0+J1xuICAgICAgfVxuICAgIF1cbiAgfTtcbiAgTU9EVUxFX0FDQ0VTU19DT05URU5UUy5wdXNoKEZVTkNUSU9OX0JMT0NLX01PREUpO1xuXG4gIGNvbnN0IENPTlNUUlVDVE9SX01PREUgPSB7XG4gICAgY2xhc3NOYW1lOiAnY29uc3RydWN0b3InLFxuICAgIGJlZ2luOiBSRV9NT0RVTEVfSURFTlQgKyAnXFxcXCgnLFxuICAgIGVuZDogJ1xcXFwpJyxcbiAgICBpbGxlZ2FsOiAnXFxcXG4nLFxuICAgIGtleXdvcmRzOiBLRVlXT1JEUyxcbiAgICBjb250YWluczogW1xuICAgICAgaGxqcy5RVU9URV9TVFJJTkdfTU9ERSxcbiAgICAgIE9QRVJBVE9SX01PREUsXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3BhcmFtcycsXG4gICAgICAgIGJlZ2luOiAnXFxcXGInICsgUkVfSURFTlRcbiAgICAgIH1cbiAgICBdXG4gIH07XG5cbiAgY29uc3QgUEFUVEVSTl9NQVRDSF9CTE9DS19NT0RFID0ge1xuICAgIGNsYXNzTmFtZTogJ3BhdHRlcm4tbWF0Y2gnLFxuICAgIGJlZ2luOiAnXFxcXHwnLFxuICAgIHJldHVybkJlZ2luOiB0cnVlLFxuICAgIGtleXdvcmRzOiBLRVlXT1JEUyxcbiAgICBlbmQ6ICc9PicsXG4gICAgcmVsZXZhbmNlOiAwLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBDT05TVFJVQ1RPUl9NT0RFLFxuICAgICAgT1BFUkFUT1JfTU9ERSxcbiAgICAgIHtcbiAgICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgICBjbGFzc05hbWU6ICdjb25zdHJ1Y3RvcicsXG4gICAgICAgIGJlZ2luOiBSRV9NT0RVTEVfSURFTlRcbiAgICAgIH1cbiAgICBdXG4gIH07XG5cbiAgY29uc3QgTU9EVUxFX0FDQ0VTU19NT0RFID0ge1xuICAgIGNsYXNzTmFtZTogJ21vZHVsZS1hY2Nlc3MnLFxuICAgIGtleXdvcmRzOiBLRVlXT1JEUyxcbiAgICByZXR1cm5CZWdpbjogdHJ1ZSxcbiAgICB2YXJpYW50czogW1xuICAgICAge1xuICAgICAgICBiZWdpbjogXCJcXFxcYihcIiArIFJFX01PRFVMRV9JREVOVCArIFwiXFxcXC4pK1wiICsgUkVfSURFTlRcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiBcIlxcXFxiKFwiICsgUkVfTU9EVUxFX0lERU5UICsgXCJcXFxcLikrXFxcXChcIixcbiAgICAgICAgZW5kOiBcIlxcXFwpXCIsXG4gICAgICAgIHJldHVybkJlZ2luOiB0cnVlLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIEZVTkNUSU9OX0JMT0NLX01PREUsXG4gICAgICAgICAge1xuICAgICAgICAgICAgYmVnaW46ICdcXFxcKCcsXG4gICAgICAgICAgICBlbmQ6ICdcXFxcKScsXG4gICAgICAgICAgICBza2lwOiB0cnVlXG4gICAgICAgICAgfVxuICAgICAgICBdLmNvbmNhdChNT0RVTEVfQUNDRVNTX0NPTlRFTlRTKVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IFwiXFxcXGIoXCIgKyBSRV9NT0RVTEVfSURFTlQgKyBcIlxcXFwuKStcXFxce1wiLFxuICAgICAgICBlbmQ6IC9cXH0vXG4gICAgICB9XG4gICAgXSxcbiAgICBjb250YWluczogTU9EVUxFX0FDQ0VTU19DT05URU5UU1xuICB9O1xuXG4gIFBBUkFNU19DT05URU5UUy5wdXNoKE1PRFVMRV9BQ0NFU1NfTU9ERSk7XG5cbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnUmVhc29uTUwnLFxuICAgIGFsaWFzZXM6IFsgJ3JlJyBdLFxuICAgIGtleXdvcmRzOiBLRVlXT1JEUyxcbiAgICBpbGxlZ2FsOiAnKDotfDo9fFxcXFwkXFxcXHt8XFxcXCs9KScsXG4gICAgY29udGFpbnM6IFtcbiAgICAgIGhsanMuQ09NTUVOVCgnL1xcXFwqJywgJ1xcXFwqLycsIHtcbiAgICAgICAgaWxsZWdhbDogJ14oIyxcXFxcL1xcXFwvKSdcbiAgICAgIH0pLFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdjaGFyYWN0ZXInLFxuICAgICAgICBiZWdpbjogJ1xcJyhcXFxcXFxcXFteXFwnXSt8W15cXCddKVxcJycsXG4gICAgICAgIGlsbGVnYWw6ICdcXFxcbicsXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfSxcbiAgICAgIGhsanMuUVVPVEVfU1RSSU5HX01PREUsXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ2xpdGVyYWwnLFxuICAgICAgICBiZWdpbjogJ1xcXFwoXFxcXCknLFxuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ2xpdGVyYWwnLFxuICAgICAgICBiZWdpbjogJ1xcXFxbXFxcXHwnLFxuICAgICAgICBlbmQ6ICdcXFxcfFxcXFxdJyxcbiAgICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgICBjb250YWluczogTElTVF9DT05URU5UU19NT0RFU1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnbGl0ZXJhbCcsXG4gICAgICAgIGJlZ2luOiAnXFxcXFsnLFxuICAgICAgICBlbmQ6ICdcXFxcXScsXG4gICAgICAgIHJlbGV2YW5jZTogMCxcbiAgICAgICAgY29udGFpbnM6IExJU1RfQ09OVEVOVFNfTU9ERVNcbiAgICAgIH0sXG4gICAgICBDT05TVFJVQ1RPUl9NT0RFLFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdvcGVyYXRvcicsXG4gICAgICAgIGJlZ2luOiBSRV9PUEVSQVRPUl9TUEFDRUQsXG4gICAgICAgIGlsbGVnYWw6ICctLT4nLFxuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH0sXG4gICAgICBOVU1CRVJfTU9ERSxcbiAgICAgIGhsanMuQ19MSU5FX0NPTU1FTlRfTU9ERSxcbiAgICAgIFBBVFRFUk5fTUFUQ0hfQkxPQ0tfTU9ERSxcbiAgICAgIEZVTkNUSU9OX0JMT0NLX01PREUsXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ21vZHVsZS1kZWYnLFxuICAgICAgICBiZWdpbjogXCJcXFxcYm1vZHVsZVxcXFxzK1wiICsgUkVfSURFTlQgKyBcIlxcXFxzK1wiICsgUkVfTU9EVUxFX0lERU5UICsgXCJcXFxccys9XFxcXHMrXFxcXHtcIixcbiAgICAgICAgZW5kOiAvXFx9LyxcbiAgICAgICAgcmV0dXJuQmVnaW46IHRydWUsXG4gICAgICAgIGtleXdvcmRzOiBLRVlXT1JEUyxcbiAgICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIGNsYXNzTmFtZTogJ21vZHVsZScsXG4gICAgICAgICAgICByZWxldmFuY2U6IDAsXG4gICAgICAgICAgICBiZWdpbjogUkVfTU9EVUxFX0lERU5UXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbjogL1xcey8sXG4gICAgICAgICAgICBlbmQ6IC9cXH0vLFxuICAgICAgICAgICAgc2tpcDogdHJ1ZVxuICAgICAgICAgIH1cbiAgICAgICAgXS5jb25jYXQoTU9EVUxFX0FDQ0VTU19DT05URU5UUylcbiAgICAgIH0sXG4gICAgICBNT0RVTEVfQUNDRVNTX01PREVcbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gcmVhc29ubWw7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=