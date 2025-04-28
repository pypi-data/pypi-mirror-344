(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_dart"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/dart.js":
/*!***********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/dart.js ***!
  \***********************************************************************************************/
/***/ ((module) => {

/*
Language: Dart
Requires: markdown.js
Author: Maxim Dikun <dikmax@gmail.com>
Description: Dart a modern, object-oriented language developed by Google. For more information see https://www.dartlang.org/
Website: https://dart.dev
Category: scripting
*/

/** @type LanguageFn */
function dart(hljs) {
  const SUBST = {
    className: 'subst',
    variants: [{
      begin: '\\$[A-Za-z0-9_]+'
    }]
  };

  const BRACED_SUBST = {
    className: 'subst',
    variants: [{
      begin: /\$\{/,
      end: /\}/
    }],
    keywords: 'true false null this is new super'
  };

  const STRING = {
    className: 'string',
    variants: [
      {
        begin: 'r\'\'\'',
        end: '\'\'\''
      },
      {
        begin: 'r"""',
        end: '"""'
      },
      {
        begin: 'r\'',
        end: '\'',
        illegal: '\\n'
      },
      {
        begin: 'r"',
        end: '"',
        illegal: '\\n'
      },
      {
        begin: '\'\'\'',
        end: '\'\'\'',
        contains: [
          hljs.BACKSLASH_ESCAPE,
          SUBST,
          BRACED_SUBST
        ]
      },
      {
        begin: '"""',
        end: '"""',
        contains: [
          hljs.BACKSLASH_ESCAPE,
          SUBST,
          BRACED_SUBST
        ]
      },
      {
        begin: '\'',
        end: '\'',
        illegal: '\\n',
        contains: [
          hljs.BACKSLASH_ESCAPE,
          SUBST,
          BRACED_SUBST
        ]
      },
      {
        begin: '"',
        end: '"',
        illegal: '\\n',
        contains: [
          hljs.BACKSLASH_ESCAPE,
          SUBST,
          BRACED_SUBST
        ]
      }
    ]
  };
  BRACED_SUBST.contains = [
    hljs.C_NUMBER_MODE,
    STRING
  ];

  const BUILT_IN_TYPES = [
    // dart:core
    'Comparable',
    'DateTime',
    'Duration',
    'Function',
    'Iterable',
    'Iterator',
    'List',
    'Map',
    'Match',
    'Object',
    'Pattern',
    'RegExp',
    'Set',
    'Stopwatch',
    'String',
    'StringBuffer',
    'StringSink',
    'Symbol',
    'Type',
    'Uri',
    'bool',
    'double',
    'int',
    'num',
    // dart:html
    'Element',
    'ElementList'
  ];
  const NULLABLE_BUILT_IN_TYPES = BUILT_IN_TYPES.map((e) => `${e}?`);

  const KEYWORDS = {
    keyword: 'abstract as assert async await break case catch class const continue covariant default deferred do ' +
      'dynamic else enum export extends extension external factory false final finally for Function get hide if ' +
      'implements import in inferface is late library mixin new null on operator part required rethrow return set ' +
      'show static super switch sync this throw true try typedef var void while with yield',
    built_in:
      BUILT_IN_TYPES
        .concat(NULLABLE_BUILT_IN_TYPES)
        .concat([
          // dart:core
          'Never',
          'Null',
          'dynamic',
          'print',
          // dart:html
          'document',
          'querySelector',
          'querySelectorAll',
          'window'
        ]),
    $pattern: /[A-Za-z][A-Za-z0-9_]*\??/
  };

  return {
    name: 'Dart',
    keywords: KEYWORDS,
    contains: [
      STRING,
      hljs.COMMENT(
        /\/\*\*(?!\/)/,
        /\*\//,
        {
          subLanguage: 'markdown',
          relevance: 0
        }
      ),
      hljs.COMMENT(
        /\/{3,} ?/,
        /$/, {
          contains: [{
            subLanguage: 'markdown',
            begin: '.',
            end: '$',
            relevance: 0
          }]
        }
      ),
      hljs.C_LINE_COMMENT_MODE,
      hljs.C_BLOCK_COMMENT_MODE,
      {
        className: 'class',
        beginKeywords: 'class interface',
        end: /\{/,
        excludeEnd: true,
        contains: [
          {
            beginKeywords: 'extends implements'
          },
          hljs.UNDERSCORE_TITLE_MODE
        ]
      },
      hljs.C_NUMBER_MODE,
      {
        className: 'meta',
        begin: '@[A-Za-z]+'
      },
      {
        begin: '=>' // No markup, just a relevance booster
      }
    ]
  };
}

module.exports = dart;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfZGFydC5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDs7QUFFQTtBQUNBO0FBQ0E7QUFDQSxrQkFBa0I7QUFDbEIsY0FBYztBQUNkLEtBQUs7QUFDTDtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSwrREFBK0QsRUFBRTs7QUFFakU7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFlBQVksSUFBSTtBQUNoQjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxnQkFBZ0I7QUFDaEI7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL2RhcnQuanMiXSwic291cmNlc0NvbnRlbnQiOlsiLypcbkxhbmd1YWdlOiBEYXJ0XG5SZXF1aXJlczogbWFya2Rvd24uanNcbkF1dGhvcjogTWF4aW0gRGlrdW4gPGRpa21heEBnbWFpbC5jb20+XG5EZXNjcmlwdGlvbjogRGFydCBhIG1vZGVybiwgb2JqZWN0LW9yaWVudGVkIGxhbmd1YWdlIGRldmVsb3BlZCBieSBHb29nbGUuIEZvciBtb3JlIGluZm9ybWF0aW9uIHNlZSBodHRwczovL3d3dy5kYXJ0bGFuZy5vcmcvXG5XZWJzaXRlOiBodHRwczovL2RhcnQuZGV2XG5DYXRlZ29yeTogc2NyaXB0aW5nXG4qL1xuXG4vKiogQHR5cGUgTGFuZ3VhZ2VGbiAqL1xuZnVuY3Rpb24gZGFydChobGpzKSB7XG4gIGNvbnN0IFNVQlNUID0ge1xuICAgIGNsYXNzTmFtZTogJ3N1YnN0JyxcbiAgICB2YXJpYW50czogW3tcbiAgICAgIGJlZ2luOiAnXFxcXCRbQS1aYS16MC05X10rJ1xuICAgIH1dXG4gIH07XG5cbiAgY29uc3QgQlJBQ0VEX1NVQlNUID0ge1xuICAgIGNsYXNzTmFtZTogJ3N1YnN0JyxcbiAgICB2YXJpYW50czogW3tcbiAgICAgIGJlZ2luOiAvXFwkXFx7LyxcbiAgICAgIGVuZDogL1xcfS9cbiAgICB9XSxcbiAgICBrZXl3b3JkczogJ3RydWUgZmFsc2UgbnVsbCB0aGlzIGlzIG5ldyBzdXBlcidcbiAgfTtcblxuICBjb25zdCBTVFJJTkcgPSB7XG4gICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICB2YXJpYW50czogW1xuICAgICAge1xuICAgICAgICBiZWdpbjogJ3JcXCdcXCdcXCcnLFxuICAgICAgICBlbmQ6ICdcXCdcXCdcXCcnXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogJ3JcIlwiXCInLFxuICAgICAgICBlbmQ6ICdcIlwiXCInXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogJ3JcXCcnLFxuICAgICAgICBlbmQ6ICdcXCcnLFxuICAgICAgICBpbGxlZ2FsOiAnXFxcXG4nXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogJ3JcIicsXG4gICAgICAgIGVuZDogJ1wiJyxcbiAgICAgICAgaWxsZWdhbDogJ1xcXFxuJ1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICdcXCdcXCdcXCcnLFxuICAgICAgICBlbmQ6ICdcXCdcXCdcXCcnLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIGhsanMuQkFDS1NMQVNIX0VTQ0FQRSxcbiAgICAgICAgICBTVUJTVCxcbiAgICAgICAgICBCUkFDRURfU1VCU1RcbiAgICAgICAgXVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICdcIlwiXCInLFxuICAgICAgICBlbmQ6ICdcIlwiXCInLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIGhsanMuQkFDS1NMQVNIX0VTQ0FQRSxcbiAgICAgICAgICBTVUJTVCxcbiAgICAgICAgICBCUkFDRURfU1VCU1RcbiAgICAgICAgXVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICdcXCcnLFxuICAgICAgICBlbmQ6ICdcXCcnLFxuICAgICAgICBpbGxlZ2FsOiAnXFxcXG4nLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIGhsanMuQkFDS1NMQVNIX0VTQ0FQRSxcbiAgICAgICAgICBTVUJTVCxcbiAgICAgICAgICBCUkFDRURfU1VCU1RcbiAgICAgICAgXVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICdcIicsXG4gICAgICAgIGVuZDogJ1wiJyxcbiAgICAgICAgaWxsZWdhbDogJ1xcXFxuJyxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICBobGpzLkJBQ0tTTEFTSF9FU0NBUEUsXG4gICAgICAgICAgU1VCU1QsXG4gICAgICAgICAgQlJBQ0VEX1NVQlNUXG4gICAgICAgIF1cbiAgICAgIH1cbiAgICBdXG4gIH07XG4gIEJSQUNFRF9TVUJTVC5jb250YWlucyA9IFtcbiAgICBobGpzLkNfTlVNQkVSX01PREUsXG4gICAgU1RSSU5HXG4gIF07XG5cbiAgY29uc3QgQlVJTFRfSU5fVFlQRVMgPSBbXG4gICAgLy8gZGFydDpjb3JlXG4gICAgJ0NvbXBhcmFibGUnLFxuICAgICdEYXRlVGltZScsXG4gICAgJ0R1cmF0aW9uJyxcbiAgICAnRnVuY3Rpb24nLFxuICAgICdJdGVyYWJsZScsXG4gICAgJ0l0ZXJhdG9yJyxcbiAgICAnTGlzdCcsXG4gICAgJ01hcCcsXG4gICAgJ01hdGNoJyxcbiAgICAnT2JqZWN0JyxcbiAgICAnUGF0dGVybicsXG4gICAgJ1JlZ0V4cCcsXG4gICAgJ1NldCcsXG4gICAgJ1N0b3B3YXRjaCcsXG4gICAgJ1N0cmluZycsXG4gICAgJ1N0cmluZ0J1ZmZlcicsXG4gICAgJ1N0cmluZ1NpbmsnLFxuICAgICdTeW1ib2wnLFxuICAgICdUeXBlJyxcbiAgICAnVXJpJyxcbiAgICAnYm9vbCcsXG4gICAgJ2RvdWJsZScsXG4gICAgJ2ludCcsXG4gICAgJ251bScsXG4gICAgLy8gZGFydDpodG1sXG4gICAgJ0VsZW1lbnQnLFxuICAgICdFbGVtZW50TGlzdCdcbiAgXTtcbiAgY29uc3QgTlVMTEFCTEVfQlVJTFRfSU5fVFlQRVMgPSBCVUlMVF9JTl9UWVBFUy5tYXAoKGUpID0+IGAke2V9P2ApO1xuXG4gIGNvbnN0IEtFWVdPUkRTID0ge1xuICAgIGtleXdvcmQ6ICdhYnN0cmFjdCBhcyBhc3NlcnQgYXN5bmMgYXdhaXQgYnJlYWsgY2FzZSBjYXRjaCBjbGFzcyBjb25zdCBjb250aW51ZSBjb3ZhcmlhbnQgZGVmYXVsdCBkZWZlcnJlZCBkbyAnICtcbiAgICAgICdkeW5hbWljIGVsc2UgZW51bSBleHBvcnQgZXh0ZW5kcyBleHRlbnNpb24gZXh0ZXJuYWwgZmFjdG9yeSBmYWxzZSBmaW5hbCBmaW5hbGx5IGZvciBGdW5jdGlvbiBnZXQgaGlkZSBpZiAnICtcbiAgICAgICdpbXBsZW1lbnRzIGltcG9ydCBpbiBpbmZlcmZhY2UgaXMgbGF0ZSBsaWJyYXJ5IG1peGluIG5ldyBudWxsIG9uIG9wZXJhdG9yIHBhcnQgcmVxdWlyZWQgcmV0aHJvdyByZXR1cm4gc2V0ICcgK1xuICAgICAgJ3Nob3cgc3RhdGljIHN1cGVyIHN3aXRjaCBzeW5jIHRoaXMgdGhyb3cgdHJ1ZSB0cnkgdHlwZWRlZiB2YXIgdm9pZCB3aGlsZSB3aXRoIHlpZWxkJyxcbiAgICBidWlsdF9pbjpcbiAgICAgIEJVSUxUX0lOX1RZUEVTXG4gICAgICAgIC5jb25jYXQoTlVMTEFCTEVfQlVJTFRfSU5fVFlQRVMpXG4gICAgICAgIC5jb25jYXQoW1xuICAgICAgICAgIC8vIGRhcnQ6Y29yZVxuICAgICAgICAgICdOZXZlcicsXG4gICAgICAgICAgJ051bGwnLFxuICAgICAgICAgICdkeW5hbWljJyxcbiAgICAgICAgICAncHJpbnQnLFxuICAgICAgICAgIC8vIGRhcnQ6aHRtbFxuICAgICAgICAgICdkb2N1bWVudCcsXG4gICAgICAgICAgJ3F1ZXJ5U2VsZWN0b3InLFxuICAgICAgICAgICdxdWVyeVNlbGVjdG9yQWxsJyxcbiAgICAgICAgICAnd2luZG93J1xuICAgICAgICBdKSxcbiAgICAkcGF0dGVybjogL1tBLVphLXpdW0EtWmEtejAtOV9dKlxcPz8vXG4gIH07XG5cbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnRGFydCcsXG4gICAga2V5d29yZHM6IEtFWVdPUkRTLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBTVFJJTkcsXG4gICAgICBobGpzLkNPTU1FTlQoXG4gICAgICAgIC9cXC9cXCpcXCooPyFcXC8pLyxcbiAgICAgICAgL1xcKlxcLy8sXG4gICAgICAgIHtcbiAgICAgICAgICBzdWJMYW5ndWFnZTogJ21hcmtkb3duJyxcbiAgICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgICAgfVxuICAgICAgKSxcbiAgICAgIGhsanMuQ09NTUVOVChcbiAgICAgICAgL1xcL3szLH0gPy8sXG4gICAgICAgIC8kLywge1xuICAgICAgICAgIGNvbnRhaW5zOiBbe1xuICAgICAgICAgICAgc3ViTGFuZ3VhZ2U6ICdtYXJrZG93bicsXG4gICAgICAgICAgICBiZWdpbjogJy4nLFxuICAgICAgICAgICAgZW5kOiAnJCcsXG4gICAgICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgICAgICB9XVxuICAgICAgICB9XG4gICAgICApLFxuICAgICAgaGxqcy5DX0xJTkVfQ09NTUVOVF9NT0RFLFxuICAgICAgaGxqcy5DX0JMT0NLX0NPTU1FTlRfTU9ERSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnY2xhc3MnLFxuICAgICAgICBiZWdpbktleXdvcmRzOiAnY2xhc3MgaW50ZXJmYWNlJyxcbiAgICAgICAgZW5kOiAvXFx7LyxcbiAgICAgICAgZXhjbHVkZUVuZDogdHJ1ZSxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbktleXdvcmRzOiAnZXh0ZW5kcyBpbXBsZW1lbnRzJ1xuICAgICAgICAgIH0sXG4gICAgICAgICAgaGxqcy5VTkRFUlNDT1JFX1RJVExFX01PREVcbiAgICAgICAgXVxuICAgICAgfSxcbiAgICAgIGhsanMuQ19OVU1CRVJfTU9ERSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnbWV0YScsXG4gICAgICAgIGJlZ2luOiAnQFtBLVphLXpdKydcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnPT4nIC8vIE5vIG1hcmt1cCwganVzdCBhIHJlbGV2YW5jZSBib29zdGVyXG4gICAgICB9XG4gICAgXVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IGRhcnQ7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=