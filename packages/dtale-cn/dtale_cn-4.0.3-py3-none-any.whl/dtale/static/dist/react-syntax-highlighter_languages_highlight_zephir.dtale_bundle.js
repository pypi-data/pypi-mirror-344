(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_zephir"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/zephir.js":
/*!*************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/zephir.js ***!
  \*************************************************************************************************/
/***/ ((module) => {

/*
 Language: Zephir
 Description: Zephir, an open source, high-level language designed to ease the creation and maintainability of extensions for PHP with a focus on type and memory safety.
 Author: Oleg Efimov <efimovov@gmail.com>
 Website: https://zephir-lang.com/en
 Audit: 2020
 */

/** @type LanguageFn */
function zephir(hljs) {
  const STRING = {
    className: 'string',
    contains: [ hljs.BACKSLASH_ESCAPE ],
    variants: [
      hljs.inherit(hljs.APOS_STRING_MODE, {
        illegal: null
      }),
      hljs.inherit(hljs.QUOTE_STRING_MODE, {
        illegal: null
      })
    ]
  };
  const TITLE_MODE = hljs.UNDERSCORE_TITLE_MODE;
  const NUMBER = {
    variants: [
      hljs.BINARY_NUMBER_MODE,
      hljs.C_NUMBER_MODE
    ]
  };
  const KEYWORDS =
    // classes and objects
    'namespace class interface use extends ' +
    'function return ' +
    'abstract final public protected private static deprecated ' +
    // error handling
    'throw try catch Exception ' +
    // keyword-ish things their website does NOT seem to highlight (in their own snippets)
    // 'typeof fetch in ' +
    // operators/helpers
    'echo empty isset instanceof unset ' +
    // assignment/variables
    'let var new const self ' +
    // control
    'require ' +
    'if else elseif switch case default ' +
    'do while loop for continue break ' +
    'likely unlikely ' +
    // magic constants
    // https://github.com/phalcon/zephir/blob/master/Library/Expression/Constants.php
    '__LINE__ __FILE__ __DIR__ __FUNCTION__ __CLASS__ __TRAIT__ __METHOD__ __NAMESPACE__ ' +
    // types - https://docs.zephir-lang.com/0.12/en/types
    'array boolean float double integer object resource string ' +
    'char long unsigned bool int uint ulong uchar ' +
    // built-ins
    'true false null undefined';

  return {
    name: 'Zephir',
    aliases: [ 'zep' ],
    keywords: KEYWORDS,
    contains: [
      hljs.C_LINE_COMMENT_MODE,
      hljs.COMMENT(
        /\/\*/,
        /\*\//,
        {
          contains: [
            {
              className: 'doctag',
              begin: /@[A-Za-z]+/
            }
          ]
        }
      ),
      {
        className: 'string',
        begin: /<<<['"]?\w+['"]?$/,
        end: /^\w+;/,
        contains: [ hljs.BACKSLASH_ESCAPE ]
      },
      {
        // swallow composed identifiers to avoid parsing them as keywords
        begin: /(::|->)+[a-zA-Z_\x7f-\xff][a-zA-Z0-9_\x7f-\xff]*/
      },
      {
        className: 'function',
        beginKeywords: 'function fn',
        end: /[;{]/,
        excludeEnd: true,
        illegal: /\$|\[|%/,
        contains: [
          TITLE_MODE,
          {
            className: 'params',
            begin: /\(/,
            end: /\)/,
            keywords: KEYWORDS,
            contains: [
              'self',
              hljs.C_BLOCK_COMMENT_MODE,
              STRING,
              NUMBER
            ]
          }
        ]
      },
      {
        className: 'class',
        beginKeywords: 'class interface',
        end: /\{/,
        excludeEnd: true,
        illegal: /[:($"]/,
        contains: [
          {
            beginKeywords: 'extends implements'
          },
          TITLE_MODE
        ]
      },
      {
        beginKeywords: 'namespace',
        end: /;/,
        illegal: /[.']/,
        contains: [ TITLE_MODE ]
      },
      {
        beginKeywords: 'use',
        end: /;/,
        contains: [ TITLE_MODE ]
      },
      {
        begin: /=>/ // No markup, just a relevance booster
      },
      STRING,
      NUMBER
    ]
  };
}

module.exports = zephir;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfemVwaGlyLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLG1CQUFtQjtBQUNuQjtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0EsaUJBQWlCO0FBQ2pCO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0EsZ0JBQWdCO0FBQ2hCO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0EsZUFBZTtBQUNmO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBLGVBQWU7QUFDZjtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL3plcGhpci5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKlxuIExhbmd1YWdlOiBaZXBoaXJcbiBEZXNjcmlwdGlvbjogWmVwaGlyLCBhbiBvcGVuIHNvdXJjZSwgaGlnaC1sZXZlbCBsYW5ndWFnZSBkZXNpZ25lZCB0byBlYXNlIHRoZSBjcmVhdGlvbiBhbmQgbWFpbnRhaW5hYmlsaXR5IG9mIGV4dGVuc2lvbnMgZm9yIFBIUCB3aXRoIGEgZm9jdXMgb24gdHlwZSBhbmQgbWVtb3J5IHNhZmV0eS5cbiBBdXRob3I6IE9sZWcgRWZpbW92IDxlZmltb3ZvdkBnbWFpbC5jb20+XG4gV2Vic2l0ZTogaHR0cHM6Ly96ZXBoaXItbGFuZy5jb20vZW5cbiBBdWRpdDogMjAyMFxuICovXG5cbi8qKiBAdHlwZSBMYW5ndWFnZUZuICovXG5mdW5jdGlvbiB6ZXBoaXIoaGxqcykge1xuICBjb25zdCBTVFJJTkcgPSB7XG4gICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICBjb250YWluczogWyBobGpzLkJBQ0tTTEFTSF9FU0NBUEUgXSxcbiAgICB2YXJpYW50czogW1xuICAgICAgaGxqcy5pbmhlcml0KGhsanMuQVBPU19TVFJJTkdfTU9ERSwge1xuICAgICAgICBpbGxlZ2FsOiBudWxsXG4gICAgICB9KSxcbiAgICAgIGhsanMuaW5oZXJpdChobGpzLlFVT1RFX1NUUklOR19NT0RFLCB7XG4gICAgICAgIGlsbGVnYWw6IG51bGxcbiAgICAgIH0pXG4gICAgXVxuICB9O1xuICBjb25zdCBUSVRMRV9NT0RFID0gaGxqcy5VTkRFUlNDT1JFX1RJVExFX01PREU7XG4gIGNvbnN0IE5VTUJFUiA9IHtcbiAgICB2YXJpYW50czogW1xuICAgICAgaGxqcy5CSU5BUllfTlVNQkVSX01PREUsXG4gICAgICBobGpzLkNfTlVNQkVSX01PREVcbiAgICBdXG4gIH07XG4gIGNvbnN0IEtFWVdPUkRTID1cbiAgICAvLyBjbGFzc2VzIGFuZCBvYmplY3RzXG4gICAgJ25hbWVzcGFjZSBjbGFzcyBpbnRlcmZhY2UgdXNlIGV4dGVuZHMgJyArXG4gICAgJ2Z1bmN0aW9uIHJldHVybiAnICtcbiAgICAnYWJzdHJhY3QgZmluYWwgcHVibGljIHByb3RlY3RlZCBwcml2YXRlIHN0YXRpYyBkZXByZWNhdGVkICcgK1xuICAgIC8vIGVycm9yIGhhbmRsaW5nXG4gICAgJ3Rocm93IHRyeSBjYXRjaCBFeGNlcHRpb24gJyArXG4gICAgLy8ga2V5d29yZC1pc2ggdGhpbmdzIHRoZWlyIHdlYnNpdGUgZG9lcyBOT1Qgc2VlbSB0byBoaWdobGlnaHQgKGluIHRoZWlyIG93biBzbmlwcGV0cylcbiAgICAvLyAndHlwZW9mIGZldGNoIGluICcgK1xuICAgIC8vIG9wZXJhdG9ycy9oZWxwZXJzXG4gICAgJ2VjaG8gZW1wdHkgaXNzZXQgaW5zdGFuY2VvZiB1bnNldCAnICtcbiAgICAvLyBhc3NpZ25tZW50L3ZhcmlhYmxlc1xuICAgICdsZXQgdmFyIG5ldyBjb25zdCBzZWxmICcgK1xuICAgIC8vIGNvbnRyb2xcbiAgICAncmVxdWlyZSAnICtcbiAgICAnaWYgZWxzZSBlbHNlaWYgc3dpdGNoIGNhc2UgZGVmYXVsdCAnICtcbiAgICAnZG8gd2hpbGUgbG9vcCBmb3IgY29udGludWUgYnJlYWsgJyArXG4gICAgJ2xpa2VseSB1bmxpa2VseSAnICtcbiAgICAvLyBtYWdpYyBjb25zdGFudHNcbiAgICAvLyBodHRwczovL2dpdGh1Yi5jb20vcGhhbGNvbi96ZXBoaXIvYmxvYi9tYXN0ZXIvTGlicmFyeS9FeHByZXNzaW9uL0NvbnN0YW50cy5waHBcbiAgICAnX19MSU5FX18gX19GSUxFX18gX19ESVJfXyBfX0ZVTkNUSU9OX18gX19DTEFTU19fIF9fVFJBSVRfXyBfX01FVEhPRF9fIF9fTkFNRVNQQUNFX18gJyArXG4gICAgLy8gdHlwZXMgLSBodHRwczovL2RvY3MuemVwaGlyLWxhbmcuY29tLzAuMTIvZW4vdHlwZXNcbiAgICAnYXJyYXkgYm9vbGVhbiBmbG9hdCBkb3VibGUgaW50ZWdlciBvYmplY3QgcmVzb3VyY2Ugc3RyaW5nICcgK1xuICAgICdjaGFyIGxvbmcgdW5zaWduZWQgYm9vbCBpbnQgdWludCB1bG9uZyB1Y2hhciAnICtcbiAgICAvLyBidWlsdC1pbnNcbiAgICAndHJ1ZSBmYWxzZSBudWxsIHVuZGVmaW5lZCc7XG5cbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnWmVwaGlyJyxcbiAgICBhbGlhc2VzOiBbICd6ZXAnIF0sXG4gICAga2V5d29yZHM6IEtFWVdPUkRTLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBobGpzLkNfTElORV9DT01NRU5UX01PREUsXG4gICAgICBobGpzLkNPTU1FTlQoXG4gICAgICAgIC9cXC9cXCovLFxuICAgICAgICAvXFwqXFwvLyxcbiAgICAgICAge1xuICAgICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgICB7XG4gICAgICAgICAgICAgIGNsYXNzTmFtZTogJ2RvY3RhZycsXG4gICAgICAgICAgICAgIGJlZ2luOiAvQFtBLVphLXpdKy9cbiAgICAgICAgICAgIH1cbiAgICAgICAgICBdXG4gICAgICAgIH1cbiAgICAgICksXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3N0cmluZycsXG4gICAgICAgIGJlZ2luOiAvPDw8WydcIl0/XFx3K1snXCJdPyQvLFxuICAgICAgICBlbmQ6IC9eXFx3KzsvLFxuICAgICAgICBjb250YWluczogWyBobGpzLkJBQ0tTTEFTSF9FU0NBUEUgXVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgLy8gc3dhbGxvdyBjb21wb3NlZCBpZGVudGlmaWVycyB0byBhdm9pZCBwYXJzaW5nIHRoZW0gYXMga2V5d29yZHNcbiAgICAgICAgYmVnaW46IC8oOjp8LT4pK1thLXpBLVpfXFx4N2YtXFx4ZmZdW2EtekEtWjAtOV9cXHg3Zi1cXHhmZl0qL1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnZnVuY3Rpb24nLFxuICAgICAgICBiZWdpbktleXdvcmRzOiAnZnVuY3Rpb24gZm4nLFxuICAgICAgICBlbmQ6IC9bO3tdLyxcbiAgICAgICAgZXhjbHVkZUVuZDogdHJ1ZSxcbiAgICAgICAgaWxsZWdhbDogL1xcJHxcXFt8JS8sXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgVElUTEVfTU9ERSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICBjbGFzc05hbWU6ICdwYXJhbXMnLFxuICAgICAgICAgICAgYmVnaW46IC9cXCgvLFxuICAgICAgICAgICAgZW5kOiAvXFwpLyxcbiAgICAgICAgICAgIGtleXdvcmRzOiBLRVlXT1JEUyxcbiAgICAgICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgICAgICdzZWxmJyxcbiAgICAgICAgICAgICAgaGxqcy5DX0JMT0NLX0NPTU1FTlRfTU9ERSxcbiAgICAgICAgICAgICAgU1RSSU5HLFxuICAgICAgICAgICAgICBOVU1CRVJcbiAgICAgICAgICAgIF1cbiAgICAgICAgICB9XG4gICAgICAgIF1cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ2NsYXNzJyxcbiAgICAgICAgYmVnaW5LZXl3b3JkczogJ2NsYXNzIGludGVyZmFjZScsXG4gICAgICAgIGVuZDogL1xcey8sXG4gICAgICAgIGV4Y2x1ZGVFbmQ6IHRydWUsXG4gICAgICAgIGlsbGVnYWw6IC9bOigkXCJdLyxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbktleXdvcmRzOiAnZXh0ZW5kcyBpbXBsZW1lbnRzJ1xuICAgICAgICAgIH0sXG4gICAgICAgICAgVElUTEVfTU9ERVxuICAgICAgICBdXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbktleXdvcmRzOiAnbmFtZXNwYWNlJyxcbiAgICAgICAgZW5kOiAvOy8sXG4gICAgICAgIGlsbGVnYWw6IC9bLiddLyxcbiAgICAgICAgY29udGFpbnM6IFsgVElUTEVfTU9ERSBdXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbktleXdvcmRzOiAndXNlJyxcbiAgICAgICAgZW5kOiAvOy8sXG4gICAgICAgIGNvbnRhaW5zOiBbIFRJVExFX01PREUgXVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC89Pi8gLy8gTm8gbWFya3VwLCBqdXN0IGEgcmVsZXZhbmNlIGJvb3N0ZXJcbiAgICAgIH0sXG4gICAgICBTVFJJTkcsXG4gICAgICBOVU1CRVJcbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gemVwaGlyO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9