(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_objectivec"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/objectivec.js":
/*!*****************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/objectivec.js ***!
  \*****************************************************************************************************/
/***/ ((module) => {

/*
Language: Objective-C
Author: Valerii Hiora <valerii.hiora@gmail.com>
Contributors: Angel G. Olloqui <angelgarcia.mail@gmail.com>, Matt Diephouse <matt@diephouse.com>, Andrew Farmer <ahfarmer@gmail.com>, Minh Nguyễn <mxn@1ec5.org>
Website: https://developer.apple.com/documentation/objectivec
Category: common
*/

function objectivec(hljs) {
  const API_CLASS = {
    className: 'built_in',
    begin: '\\b(AV|CA|CF|CG|CI|CL|CM|CN|CT|MK|MP|MTK|MTL|NS|SCN|SK|UI|WK|XC)\\w+'
  };
  const IDENTIFIER_RE = /[a-zA-Z@][a-zA-Z0-9_]*/;
  const OBJC_KEYWORDS = {
    $pattern: IDENTIFIER_RE,
    keyword:
      'int float while char export sizeof typedef const struct for union ' +
      'unsigned long volatile static bool mutable if do return goto void ' +
      'enum else break extern asm case short default double register explicit ' +
      'signed typename this switch continue wchar_t inline readonly assign ' +
      'readwrite self @synchronized id typeof ' +
      'nonatomic super unichar IBOutlet IBAction strong weak copy ' +
      'in out inout bycopy byref oneway __strong __weak __block __autoreleasing ' +
      '@private @protected @public @try @property @end @throw @catch @finally ' +
      '@autoreleasepool @synthesize @dynamic @selector @optional @required ' +
      '@encode @package @import @defs @compatibility_alias ' +
      '__bridge __bridge_transfer __bridge_retained __bridge_retain ' +
      '__covariant __contravariant __kindof ' +
      '_Nonnull _Nullable _Null_unspecified ' +
      '__FUNCTION__ __PRETTY_FUNCTION__ __attribute__ ' +
      'getter setter retain unsafe_unretained ' +
      'nonnull nullable null_unspecified null_resettable class instancetype ' +
      'NS_DESIGNATED_INITIALIZER NS_UNAVAILABLE NS_REQUIRES_SUPER ' +
      'NS_RETURNS_INNER_POINTER NS_INLINE NS_AVAILABLE NS_DEPRECATED ' +
      'NS_ENUM NS_OPTIONS NS_SWIFT_UNAVAILABLE ' +
      'NS_ASSUME_NONNULL_BEGIN NS_ASSUME_NONNULL_END ' +
      'NS_REFINED_FOR_SWIFT NS_SWIFT_NAME NS_SWIFT_NOTHROW ' +
      'NS_DURING NS_HANDLER NS_ENDHANDLER NS_VALUERETURN NS_VOIDRETURN',
    literal:
      'false true FALSE TRUE nil YES NO NULL',
    built_in:
      'BOOL dispatch_once_t dispatch_queue_t dispatch_sync dispatch_async dispatch_once'
  };
  const CLASS_KEYWORDS = {
    $pattern: IDENTIFIER_RE,
    keyword: '@interface @class @protocol @implementation'
  };
  return {
    name: 'Objective-C',
    aliases: [
      'mm',
      'objc',
      'obj-c',
      'obj-c++',
      'objective-c++'
    ],
    keywords: OBJC_KEYWORDS,
    illegal: '</',
    contains: [
      API_CLASS,
      hljs.C_LINE_COMMENT_MODE,
      hljs.C_BLOCK_COMMENT_MODE,
      hljs.C_NUMBER_MODE,
      hljs.QUOTE_STRING_MODE,
      hljs.APOS_STRING_MODE,
      {
        className: 'string',
        variants: [
          {
            begin: '@"',
            end: '"',
            illegal: '\\n',
            contains: [ hljs.BACKSLASH_ESCAPE ]
          }
        ]
      },
      {
        className: 'meta',
        begin: /#\s*[a-z]+\b/,
        end: /$/,
        keywords: {
          'meta-keyword':
            'if else elif endif define undef warning error line ' +
            'pragma ifdef ifndef include'
        },
        contains: [
          {
            begin: /\\\n/,
            relevance: 0
          },
          hljs.inherit(hljs.QUOTE_STRING_MODE, {
            className: 'meta-string'
          }),
          {
            className: 'meta-string',
            begin: /<.*?>/,
            end: /$/,
            illegal: '\\n'
          },
          hljs.C_LINE_COMMENT_MODE,
          hljs.C_BLOCK_COMMENT_MODE
        ]
      },
      {
        className: 'class',
        begin: '(' + CLASS_KEYWORDS.keyword.split(' ').join('|') + ')\\b',
        end: /(\{|$)/,
        excludeEnd: true,
        keywords: CLASS_KEYWORDS,
        contains: [ hljs.UNDERSCORE_TITLE_MODE ]
      },
      {
        begin: '\\.' + hljs.UNDERSCORE_IDENT_RE,
        relevance: 0
      }
    ]
  };
}

module.exports = objectivec;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfb2JqZWN0aXZlYy5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxTQUFTO0FBQ1Q7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQTtBQUNBLFdBQVc7QUFDWDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsV0FBVztBQUNYO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSxpQkFBaUI7QUFDakI7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9vYmplY3RpdmVjLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogT2JqZWN0aXZlLUNcbkF1dGhvcjogVmFsZXJpaSBIaW9yYSA8dmFsZXJpaS5oaW9yYUBnbWFpbC5jb20+XG5Db250cmlidXRvcnM6IEFuZ2VsIEcuIE9sbG9xdWkgPGFuZ2VsZ2FyY2lhLm1haWxAZ21haWwuY29tPiwgTWF0dCBEaWVwaG91c2UgPG1hdHRAZGllcGhvdXNlLmNvbT4sIEFuZHJldyBGYXJtZXIgPGFoZmFybWVyQGdtYWlsLmNvbT4sIE1pbmggTmd1eeG7hW4gPG14bkAxZWM1Lm9yZz5cbldlYnNpdGU6IGh0dHBzOi8vZGV2ZWxvcGVyLmFwcGxlLmNvbS9kb2N1bWVudGF0aW9uL29iamVjdGl2ZWNcbkNhdGVnb3J5OiBjb21tb25cbiovXG5cbmZ1bmN0aW9uIG9iamVjdGl2ZWMoaGxqcykge1xuICBjb25zdCBBUElfQ0xBU1MgPSB7XG4gICAgY2xhc3NOYW1lOiAnYnVpbHRfaW4nLFxuICAgIGJlZ2luOiAnXFxcXGIoQVZ8Q0F8Q0Z8Q0d8Q0l8Q0x8Q018Q058Q1R8TUt8TVB8TVRLfE1UTHxOU3xTQ058U0t8VUl8V0t8WEMpXFxcXHcrJ1xuICB9O1xuICBjb25zdCBJREVOVElGSUVSX1JFID0gL1thLXpBLVpAXVthLXpBLVowLTlfXSovO1xuICBjb25zdCBPQkpDX0tFWVdPUkRTID0ge1xuICAgICRwYXR0ZXJuOiBJREVOVElGSUVSX1JFLFxuICAgIGtleXdvcmQ6XG4gICAgICAnaW50IGZsb2F0IHdoaWxlIGNoYXIgZXhwb3J0IHNpemVvZiB0eXBlZGVmIGNvbnN0IHN0cnVjdCBmb3IgdW5pb24gJyArXG4gICAgICAndW5zaWduZWQgbG9uZyB2b2xhdGlsZSBzdGF0aWMgYm9vbCBtdXRhYmxlIGlmIGRvIHJldHVybiBnb3RvIHZvaWQgJyArXG4gICAgICAnZW51bSBlbHNlIGJyZWFrIGV4dGVybiBhc20gY2FzZSBzaG9ydCBkZWZhdWx0IGRvdWJsZSByZWdpc3RlciBleHBsaWNpdCAnICtcbiAgICAgICdzaWduZWQgdHlwZW5hbWUgdGhpcyBzd2l0Y2ggY29udGludWUgd2NoYXJfdCBpbmxpbmUgcmVhZG9ubHkgYXNzaWduICcgK1xuICAgICAgJ3JlYWR3cml0ZSBzZWxmIEBzeW5jaHJvbml6ZWQgaWQgdHlwZW9mICcgK1xuICAgICAgJ25vbmF0b21pYyBzdXBlciB1bmljaGFyIElCT3V0bGV0IElCQWN0aW9uIHN0cm9uZyB3ZWFrIGNvcHkgJyArXG4gICAgICAnaW4gb3V0IGlub3V0IGJ5Y29weSBieXJlZiBvbmV3YXkgX19zdHJvbmcgX193ZWFrIF9fYmxvY2sgX19hdXRvcmVsZWFzaW5nICcgK1xuICAgICAgJ0Bwcml2YXRlIEBwcm90ZWN0ZWQgQHB1YmxpYyBAdHJ5IEBwcm9wZXJ0eSBAZW5kIEB0aHJvdyBAY2F0Y2ggQGZpbmFsbHkgJyArXG4gICAgICAnQGF1dG9yZWxlYXNlcG9vbCBAc3ludGhlc2l6ZSBAZHluYW1pYyBAc2VsZWN0b3IgQG9wdGlvbmFsIEByZXF1aXJlZCAnICtcbiAgICAgICdAZW5jb2RlIEBwYWNrYWdlIEBpbXBvcnQgQGRlZnMgQGNvbXBhdGliaWxpdHlfYWxpYXMgJyArXG4gICAgICAnX19icmlkZ2UgX19icmlkZ2VfdHJhbnNmZXIgX19icmlkZ2VfcmV0YWluZWQgX19icmlkZ2VfcmV0YWluICcgK1xuICAgICAgJ19fY292YXJpYW50IF9fY29udHJhdmFyaWFudCBfX2tpbmRvZiAnICtcbiAgICAgICdfTm9ubnVsbCBfTnVsbGFibGUgX051bGxfdW5zcGVjaWZpZWQgJyArXG4gICAgICAnX19GVU5DVElPTl9fIF9fUFJFVFRZX0ZVTkNUSU9OX18gX19hdHRyaWJ1dGVfXyAnICtcbiAgICAgICdnZXR0ZXIgc2V0dGVyIHJldGFpbiB1bnNhZmVfdW5yZXRhaW5lZCAnICtcbiAgICAgICdub25udWxsIG51bGxhYmxlIG51bGxfdW5zcGVjaWZpZWQgbnVsbF9yZXNldHRhYmxlIGNsYXNzIGluc3RhbmNldHlwZSAnICtcbiAgICAgICdOU19ERVNJR05BVEVEX0lOSVRJQUxJWkVSIE5TX1VOQVZBSUxBQkxFIE5TX1JFUVVJUkVTX1NVUEVSICcgK1xuICAgICAgJ05TX1JFVFVSTlNfSU5ORVJfUE9JTlRFUiBOU19JTkxJTkUgTlNfQVZBSUxBQkxFIE5TX0RFUFJFQ0FURUQgJyArXG4gICAgICAnTlNfRU5VTSBOU19PUFRJT05TIE5TX1NXSUZUX1VOQVZBSUxBQkxFICcgK1xuICAgICAgJ05TX0FTU1VNRV9OT05OVUxMX0JFR0lOIE5TX0FTU1VNRV9OT05OVUxMX0VORCAnICtcbiAgICAgICdOU19SRUZJTkVEX0ZPUl9TV0lGVCBOU19TV0lGVF9OQU1FIE5TX1NXSUZUX05PVEhST1cgJyArXG4gICAgICAnTlNfRFVSSU5HIE5TX0hBTkRMRVIgTlNfRU5ESEFORExFUiBOU19WQUxVRVJFVFVSTiBOU19WT0lEUkVUVVJOJyxcbiAgICBsaXRlcmFsOlxuICAgICAgJ2ZhbHNlIHRydWUgRkFMU0UgVFJVRSBuaWwgWUVTIE5PIE5VTEwnLFxuICAgIGJ1aWx0X2luOlxuICAgICAgJ0JPT0wgZGlzcGF0Y2hfb25jZV90IGRpc3BhdGNoX3F1ZXVlX3QgZGlzcGF0Y2hfc3luYyBkaXNwYXRjaF9hc3luYyBkaXNwYXRjaF9vbmNlJ1xuICB9O1xuICBjb25zdCBDTEFTU19LRVlXT1JEUyA9IHtcbiAgICAkcGF0dGVybjogSURFTlRJRklFUl9SRSxcbiAgICBrZXl3b3JkOiAnQGludGVyZmFjZSBAY2xhc3MgQHByb3RvY29sIEBpbXBsZW1lbnRhdGlvbidcbiAgfTtcbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnT2JqZWN0aXZlLUMnLFxuICAgIGFsaWFzZXM6IFtcbiAgICAgICdtbScsXG4gICAgICAnb2JqYycsXG4gICAgICAnb2JqLWMnLFxuICAgICAgJ29iai1jKysnLFxuICAgICAgJ29iamVjdGl2ZS1jKysnXG4gICAgXSxcbiAgICBrZXl3b3JkczogT0JKQ19LRVlXT1JEUyxcbiAgICBpbGxlZ2FsOiAnPC8nLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBBUElfQ0xBU1MsXG4gICAgICBobGpzLkNfTElORV9DT01NRU5UX01PREUsXG4gICAgICBobGpzLkNfQkxPQ0tfQ09NTUVOVF9NT0RFLFxuICAgICAgaGxqcy5DX05VTUJFUl9NT0RFLFxuICAgICAgaGxqcy5RVU9URV9TVFJJTkdfTU9ERSxcbiAgICAgIGhsanMuQVBPU19TVFJJTkdfTU9ERSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICAgICAgdmFyaWFudHM6IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbjogJ0BcIicsXG4gICAgICAgICAgICBlbmQ6ICdcIicsXG4gICAgICAgICAgICBpbGxlZ2FsOiAnXFxcXG4nLFxuICAgICAgICAgICAgY29udGFpbnM6IFsgaGxqcy5CQUNLU0xBU0hfRVNDQVBFIF1cbiAgICAgICAgICB9XG4gICAgICAgIF1cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ21ldGEnLFxuICAgICAgICBiZWdpbjogLyNcXHMqW2Etel0rXFxiLyxcbiAgICAgICAgZW5kOiAvJC8sXG4gICAgICAgIGtleXdvcmRzOiB7XG4gICAgICAgICAgJ21ldGEta2V5d29yZCc6XG4gICAgICAgICAgICAnaWYgZWxzZSBlbGlmIGVuZGlmIGRlZmluZSB1bmRlZiB3YXJuaW5nIGVycm9yIGxpbmUgJyArXG4gICAgICAgICAgICAncHJhZ21hIGlmZGVmIGlmbmRlZiBpbmNsdWRlJ1xuICAgICAgICB9LFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiAvXFxcXFxcbi8sXG4gICAgICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgICAgICB9LFxuICAgICAgICAgIGhsanMuaW5oZXJpdChobGpzLlFVT1RFX1NUUklOR19NT0RFLCB7XG4gICAgICAgICAgICBjbGFzc05hbWU6ICdtZXRhLXN0cmluZydcbiAgICAgICAgICB9KSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICBjbGFzc05hbWU6ICdtZXRhLXN0cmluZycsXG4gICAgICAgICAgICBiZWdpbjogLzwuKj8+LyxcbiAgICAgICAgICAgIGVuZDogLyQvLFxuICAgICAgICAgICAgaWxsZWdhbDogJ1xcXFxuJ1xuICAgICAgICAgIH0sXG4gICAgICAgICAgaGxqcy5DX0xJTkVfQ09NTUVOVF9NT0RFLFxuICAgICAgICAgIGhsanMuQ19CTE9DS19DT01NRU5UX01PREVcbiAgICAgICAgXVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnY2xhc3MnLFxuICAgICAgICBiZWdpbjogJygnICsgQ0xBU1NfS0VZV09SRFMua2V5d29yZC5zcGxpdCgnICcpLmpvaW4oJ3wnKSArICcpXFxcXGInLFxuICAgICAgICBlbmQ6IC8oXFx7fCQpLyxcbiAgICAgICAgZXhjbHVkZUVuZDogdHJ1ZSxcbiAgICAgICAga2V5d29yZHM6IENMQVNTX0tFWVdPUkRTLFxuICAgICAgICBjb250YWluczogWyBobGpzLlVOREVSU0NPUkVfVElUTEVfTU9ERSBdXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogJ1xcXFwuJyArIGhsanMuVU5ERVJTQ09SRV9JREVOVF9SRSxcbiAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICB9XG4gICAgXVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IG9iamVjdGl2ZWM7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=