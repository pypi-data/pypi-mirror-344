(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_rust"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/rust.js":
/*!***********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/rust.js ***!
  \***********************************************************************************************/
/***/ ((module) => {

/*
Language: Rust
Author: Andrey Vlasovskikh <andrey.vlasovskikh@gmail.com>
Contributors: Roman Shmatov <romanshmatov@gmail.com>, Kasper Andersen <kma_untrusted@protonmail.com>
Website: https://www.rust-lang.org
Category: common, system
*/

function rust(hljs) {
  const NUM_SUFFIX = '([ui](8|16|32|64|128|size)|f(32|64))\?';
  const KEYWORDS =
    'abstract as async await become box break const continue crate do dyn ' +
    'else enum extern false final fn for if impl in let loop macro match mod ' +
    'move mut override priv pub ref return self Self static struct super ' +
    'trait true try type typeof unsafe unsized use virtual where while yield';
  const BUILTINS =
    // functions
    'drop ' +
    // types
    'i8 i16 i32 i64 i128 isize ' +
    'u8 u16 u32 u64 u128 usize ' +
    'f32 f64 ' +
    'str char bool ' +
    'Box Option Result String Vec ' +
    // traits
    'Copy Send Sized Sync Drop Fn FnMut FnOnce ToOwned Clone Debug ' +
    'PartialEq PartialOrd Eq Ord AsRef AsMut Into From Default Iterator ' +
    'Extend IntoIterator DoubleEndedIterator ExactSizeIterator ' +
    'SliceConcatExt ToString ' +
    // macros
    'assert! assert_eq! bitflags! bytes! cfg! col! concat! concat_idents! ' +
    'debug_assert! debug_assert_eq! env! panic! file! format! format_args! ' +
    'include_bin! include_str! line! local_data_key! module_path! ' +
    'option_env! print! println! select! stringify! try! unimplemented! ' +
    'unreachable! vec! write! writeln! macro_rules! assert_ne! debug_assert_ne!';
  return {
    name: 'Rust',
    aliases: [ 'rs' ],
    keywords: {
      $pattern: hljs.IDENT_RE + '!?',
      keyword:
        KEYWORDS,
      literal:
        'true false Some None Ok Err',
      built_in:
        BUILTINS
    },
    illegal: '</',
    contains: [
      hljs.C_LINE_COMMENT_MODE,
      hljs.COMMENT('/\\*', '\\*/', {
        contains: [ 'self' ]
      }),
      hljs.inherit(hljs.QUOTE_STRING_MODE, {
        begin: /b?"/,
        illegal: null
      }),
      {
        className: 'string',
        variants: [
          {
            begin: /r(#*)"(.|\n)*?"\1(?!#)/
          },
          {
            begin: /b?'\\?(x\w{2}|u\w{4}|U\w{8}|.)'/
          }
        ]
      },
      {
        className: 'symbol',
        begin: /'[a-zA-Z_][a-zA-Z0-9_]*/
      },
      {
        className: 'number',
        variants: [
          {
            begin: '\\b0b([01_]+)' + NUM_SUFFIX
          },
          {
            begin: '\\b0o([0-7_]+)' + NUM_SUFFIX
          },
          {
            begin: '\\b0x([A-Fa-f0-9_]+)' + NUM_SUFFIX
          },
          {
            begin: '\\b(\\d[\\d_]*(\\.[0-9_]+)?([eE][+-]?[0-9_]+)?)' +
                   NUM_SUFFIX
          }
        ],
        relevance: 0
      },
      {
        className: 'function',
        beginKeywords: 'fn',
        end: '(\\(|<)',
        excludeEnd: true,
        contains: [ hljs.UNDERSCORE_TITLE_MODE ]
      },
      {
        className: 'meta',
        begin: '#!?\\[',
        end: '\\]',
        contains: [
          {
            className: 'meta-string',
            begin: /"/,
            end: /"/
          }
        ]
      },
      {
        className: 'class',
        beginKeywords: 'type',
        end: ';',
        contains: [
          hljs.inherit(hljs.UNDERSCORE_TITLE_MODE, {
            endsParent: true
          })
        ],
        illegal: '\\S'
      },
      {
        className: 'class',
        beginKeywords: 'trait enum struct union',
        end: /\{/,
        contains: [
          hljs.inherit(hljs.UNDERSCORE_TITLE_MODE, {
            endsParent: true
          })
        ],
        illegal: '[\\w\\d]'
      },
      {
        begin: hljs.IDENT_RE + '::',
        keywords: {
          built_in: BUILTINS
        }
      },
      {
        begin: '->'
      }
    ]
  };
}

module.exports = rust;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfcnVzdC5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQSwrQkFBK0IsRUFBRSxLQUFLLEVBQUUsS0FBSyxFQUFFO0FBQy9DO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQTtBQUNBLFdBQVc7QUFDWDtBQUNBO0FBQ0EsV0FBVztBQUNYO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSxlQUFlO0FBQ2Y7QUFDQTtBQUNBO0FBQ0EsV0FBVztBQUNYO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0EsZ0JBQWdCO0FBQ2hCO0FBQ0E7QUFDQTtBQUNBLFdBQVc7QUFDWDtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9ydXN0LmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogUnVzdFxuQXV0aG9yOiBBbmRyZXkgVmxhc292c2tpa2ggPGFuZHJleS52bGFzb3Zza2lraEBnbWFpbC5jb20+XG5Db250cmlidXRvcnM6IFJvbWFuIFNobWF0b3YgPHJvbWFuc2htYXRvdkBnbWFpbC5jb20+LCBLYXNwZXIgQW5kZXJzZW4gPGttYV91bnRydXN0ZWRAcHJvdG9ubWFpbC5jb20+XG5XZWJzaXRlOiBodHRwczovL3d3dy5ydXN0LWxhbmcub3JnXG5DYXRlZ29yeTogY29tbW9uLCBzeXN0ZW1cbiovXG5cbmZ1bmN0aW9uIHJ1c3QoaGxqcykge1xuICBjb25zdCBOVU1fU1VGRklYID0gJyhbdWldKDh8MTZ8MzJ8NjR8MTI4fHNpemUpfGYoMzJ8NjQpKVxcPyc7XG4gIGNvbnN0IEtFWVdPUkRTID1cbiAgICAnYWJzdHJhY3QgYXMgYXN5bmMgYXdhaXQgYmVjb21lIGJveCBicmVhayBjb25zdCBjb250aW51ZSBjcmF0ZSBkbyBkeW4gJyArXG4gICAgJ2Vsc2UgZW51bSBleHRlcm4gZmFsc2UgZmluYWwgZm4gZm9yIGlmIGltcGwgaW4gbGV0IGxvb3AgbWFjcm8gbWF0Y2ggbW9kICcgK1xuICAgICdtb3ZlIG11dCBvdmVycmlkZSBwcml2IHB1YiByZWYgcmV0dXJuIHNlbGYgU2VsZiBzdGF0aWMgc3RydWN0IHN1cGVyICcgK1xuICAgICd0cmFpdCB0cnVlIHRyeSB0eXBlIHR5cGVvZiB1bnNhZmUgdW5zaXplZCB1c2UgdmlydHVhbCB3aGVyZSB3aGlsZSB5aWVsZCc7XG4gIGNvbnN0IEJVSUxUSU5TID1cbiAgICAvLyBmdW5jdGlvbnNcbiAgICAnZHJvcCAnICtcbiAgICAvLyB0eXBlc1xuICAgICdpOCBpMTYgaTMyIGk2NCBpMTI4IGlzaXplICcgK1xuICAgICd1OCB1MTYgdTMyIHU2NCB1MTI4IHVzaXplICcgK1xuICAgICdmMzIgZjY0ICcgK1xuICAgICdzdHIgY2hhciBib29sICcgK1xuICAgICdCb3ggT3B0aW9uIFJlc3VsdCBTdHJpbmcgVmVjICcgK1xuICAgIC8vIHRyYWl0c1xuICAgICdDb3B5IFNlbmQgU2l6ZWQgU3luYyBEcm9wIEZuIEZuTXV0IEZuT25jZSBUb093bmVkIENsb25lIERlYnVnICcgK1xuICAgICdQYXJ0aWFsRXEgUGFydGlhbE9yZCBFcSBPcmQgQXNSZWYgQXNNdXQgSW50byBGcm9tIERlZmF1bHQgSXRlcmF0b3IgJyArXG4gICAgJ0V4dGVuZCBJbnRvSXRlcmF0b3IgRG91YmxlRW5kZWRJdGVyYXRvciBFeGFjdFNpemVJdGVyYXRvciAnICtcbiAgICAnU2xpY2VDb25jYXRFeHQgVG9TdHJpbmcgJyArXG4gICAgLy8gbWFjcm9zXG4gICAgJ2Fzc2VydCEgYXNzZXJ0X2VxISBiaXRmbGFncyEgYnl0ZXMhIGNmZyEgY29sISBjb25jYXQhIGNvbmNhdF9pZGVudHMhICcgK1xuICAgICdkZWJ1Z19hc3NlcnQhIGRlYnVnX2Fzc2VydF9lcSEgZW52ISBwYW5pYyEgZmlsZSEgZm9ybWF0ISBmb3JtYXRfYXJncyEgJyArXG4gICAgJ2luY2x1ZGVfYmluISBpbmNsdWRlX3N0ciEgbGluZSEgbG9jYWxfZGF0YV9rZXkhIG1vZHVsZV9wYXRoISAnICtcbiAgICAnb3B0aW9uX2VudiEgcHJpbnQhIHByaW50bG4hIHNlbGVjdCEgc3RyaW5naWZ5ISB0cnkhIHVuaW1wbGVtZW50ZWQhICcgK1xuICAgICd1bnJlYWNoYWJsZSEgdmVjISB3cml0ZSEgd3JpdGVsbiEgbWFjcm9fcnVsZXMhIGFzc2VydF9uZSEgZGVidWdfYXNzZXJ0X25lISc7XG4gIHJldHVybiB7XG4gICAgbmFtZTogJ1J1c3QnLFxuICAgIGFsaWFzZXM6IFsgJ3JzJyBdLFxuICAgIGtleXdvcmRzOiB7XG4gICAgICAkcGF0dGVybjogaGxqcy5JREVOVF9SRSArICchPycsXG4gICAgICBrZXl3b3JkOlxuICAgICAgICBLRVlXT1JEUyxcbiAgICAgIGxpdGVyYWw6XG4gICAgICAgICd0cnVlIGZhbHNlIFNvbWUgTm9uZSBPayBFcnInLFxuICAgICAgYnVpbHRfaW46XG4gICAgICAgIEJVSUxUSU5TXG4gICAgfSxcbiAgICBpbGxlZ2FsOiAnPC8nLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBobGpzLkNfTElORV9DT01NRU5UX01PREUsXG4gICAgICBobGpzLkNPTU1FTlQoJy9cXFxcKicsICdcXFxcKi8nLCB7XG4gICAgICAgIGNvbnRhaW5zOiBbICdzZWxmJyBdXG4gICAgICB9KSxcbiAgICAgIGhsanMuaW5oZXJpdChobGpzLlFVT1RFX1NUUklOR19NT0RFLCB7XG4gICAgICAgIGJlZ2luOiAvYj9cIi8sXG4gICAgICAgIGlsbGVnYWw6IG51bGxcbiAgICAgIH0pLFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgICAgICB2YXJpYW50czogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiAvcigjKilcIigufFxcbikqP1wiXFwxKD8hIykvXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbjogL2I/J1xcXFw/KHhcXHd7Mn18dVxcd3s0fXxVXFx3ezh9fC4pJy9cbiAgICAgICAgICB9XG4gICAgICAgIF1cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3N5bWJvbCcsXG4gICAgICAgIGJlZ2luOiAvJ1thLXpBLVpfXVthLXpBLVowLTlfXSovXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdudW1iZXInLFxuICAgICAgICB2YXJpYW50czogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiAnXFxcXGIwYihbMDFfXSspJyArIE5VTV9TVUZGSVhcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiAnXFxcXGIwbyhbMC03X10rKScgKyBOVU1fU1VGRklYXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbjogJ1xcXFxiMHgoW0EtRmEtZjAtOV9dKyknICsgTlVNX1NVRkZJWFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgYmVnaW46ICdcXFxcYihcXFxcZFtcXFxcZF9dKihcXFxcLlswLTlfXSspPyhbZUVdWystXT9bMC05X10rKT8pJyArXG4gICAgICAgICAgICAgICAgICAgTlVNX1NVRkZJWFxuICAgICAgICAgIH1cbiAgICAgICAgXSxcbiAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdmdW5jdGlvbicsXG4gICAgICAgIGJlZ2luS2V5d29yZHM6ICdmbicsXG4gICAgICAgIGVuZDogJyhcXFxcKHw8KScsXG4gICAgICAgIGV4Y2x1ZGVFbmQ6IHRydWUsXG4gICAgICAgIGNvbnRhaW5zOiBbIGhsanMuVU5ERVJTQ09SRV9USVRMRV9NT0RFIF1cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ21ldGEnLFxuICAgICAgICBiZWdpbjogJyMhP1xcXFxbJyxcbiAgICAgICAgZW5kOiAnXFxcXF0nLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIGNsYXNzTmFtZTogJ21ldGEtc3RyaW5nJyxcbiAgICAgICAgICAgIGJlZ2luOiAvXCIvLFxuICAgICAgICAgICAgZW5kOiAvXCIvXG4gICAgICAgICAgfVxuICAgICAgICBdXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdjbGFzcycsXG4gICAgICAgIGJlZ2luS2V5d29yZHM6ICd0eXBlJyxcbiAgICAgICAgZW5kOiAnOycsXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgaGxqcy5pbmhlcml0KGhsanMuVU5ERVJTQ09SRV9USVRMRV9NT0RFLCB7XG4gICAgICAgICAgICBlbmRzUGFyZW50OiB0cnVlXG4gICAgICAgICAgfSlcbiAgICAgICAgXSxcbiAgICAgICAgaWxsZWdhbDogJ1xcXFxTJ1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnY2xhc3MnLFxuICAgICAgICBiZWdpbktleXdvcmRzOiAndHJhaXQgZW51bSBzdHJ1Y3QgdW5pb24nLFxuICAgICAgICBlbmQ6IC9cXHsvLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIGhsanMuaW5oZXJpdChobGpzLlVOREVSU0NPUkVfVElUTEVfTU9ERSwge1xuICAgICAgICAgICAgZW5kc1BhcmVudDogdHJ1ZVxuICAgICAgICAgIH0pXG4gICAgICAgIF0sXG4gICAgICAgIGlsbGVnYWw6ICdbXFxcXHdcXFxcZF0nXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogaGxqcy5JREVOVF9SRSArICc6OicsXG4gICAgICAgIGtleXdvcmRzOiB7XG4gICAgICAgICAgYnVpbHRfaW46IEJVSUxUSU5TXG4gICAgICAgIH1cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnLT4nXG4gICAgICB9XG4gICAgXVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IHJ1c3Q7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=