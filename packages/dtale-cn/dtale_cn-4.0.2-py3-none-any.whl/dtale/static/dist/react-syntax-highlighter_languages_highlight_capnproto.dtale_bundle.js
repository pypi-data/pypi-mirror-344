(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_capnproto"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/capnproto.js":
/*!****************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/capnproto.js ***!
  \****************************************************************************************************/
/***/ ((module) => {

/*
Language: Cap’n Proto
Author: Oleg Efimov <efimovov@gmail.com>
Description: Cap’n Proto message definition format
Website: https://capnproto.org/capnp-tool.html
Category: protocols
*/

/** @type LanguageFn */
function capnproto(hljs) {
  return {
    name: 'Cap’n Proto',
    aliases: ['capnp'],
    keywords: {
      keyword:
        'struct enum interface union group import using const annotation extends in of on as with from fixed',
      built_in:
        'Void Bool Int8 Int16 Int32 Int64 UInt8 UInt16 UInt32 UInt64 Float32 Float64 ' +
        'Text Data AnyPointer AnyStruct Capability List',
      literal:
        'true false'
    },
    contains: [
      hljs.QUOTE_STRING_MODE,
      hljs.NUMBER_MODE,
      hljs.HASH_COMMENT_MODE,
      {
        className: 'meta',
        begin: /@0x[\w\d]{16};/,
        illegal: /\n/
      },
      {
        className: 'symbol',
        begin: /@\d+\b/
      },
      {
        className: 'class',
        beginKeywords: 'struct enum',
        end: /\{/,
        illegal: /\n/,
        contains: [hljs.inherit(hljs.TITLE_MODE, {
          starts: {
            endsWithParent: true,
            excludeEnd: true
          } // hack: eating everything after the first title
        })]
      },
      {
        className: 'class',
        beginKeywords: 'interface',
        end: /\{/,
        illegal: /\n/,
        contains: [hljs.inherit(hljs.TITLE_MODE, {
          starts: {
            endsWithParent: true,
            excludeEnd: true
          } // hack: eating everything after the first title
        })]
      }
    ]
  };
}

module.exports = capnproto;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfY2FwbnByb3RvLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLDBCQUEwQixJQUFJO0FBQzlCO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSxnQkFBZ0I7QUFDaEI7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFlBQVk7QUFDWixTQUFTO0FBQ1QsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLGdCQUFnQjtBQUNoQjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsWUFBWTtBQUNaLFNBQVM7QUFDVDtBQUNBO0FBQ0E7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvY2FwbnByb3RvLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogQ2Fw4oCZbiBQcm90b1xuQXV0aG9yOiBPbGVnIEVmaW1vdiA8ZWZpbW92b3ZAZ21haWwuY29tPlxuRGVzY3JpcHRpb246IENhcOKAmW4gUHJvdG8gbWVzc2FnZSBkZWZpbml0aW9uIGZvcm1hdFxuV2Vic2l0ZTogaHR0cHM6Ly9jYXBucHJvdG8ub3JnL2NhcG5wLXRvb2wuaHRtbFxuQ2F0ZWdvcnk6IHByb3RvY29sc1xuKi9cblxuLyoqIEB0eXBlIExhbmd1YWdlRm4gKi9cbmZ1bmN0aW9uIGNhcG5wcm90byhobGpzKSB7XG4gIHJldHVybiB7XG4gICAgbmFtZTogJ0NhcOKAmW4gUHJvdG8nLFxuICAgIGFsaWFzZXM6IFsnY2FwbnAnXSxcbiAgICBrZXl3b3Jkczoge1xuICAgICAga2V5d29yZDpcbiAgICAgICAgJ3N0cnVjdCBlbnVtIGludGVyZmFjZSB1bmlvbiBncm91cCBpbXBvcnQgdXNpbmcgY29uc3QgYW5ub3RhdGlvbiBleHRlbmRzIGluIG9mIG9uIGFzIHdpdGggZnJvbSBmaXhlZCcsXG4gICAgICBidWlsdF9pbjpcbiAgICAgICAgJ1ZvaWQgQm9vbCBJbnQ4IEludDE2IEludDMyIEludDY0IFVJbnQ4IFVJbnQxNiBVSW50MzIgVUludDY0IEZsb2F0MzIgRmxvYXQ2NCAnICtcbiAgICAgICAgJ1RleHQgRGF0YSBBbnlQb2ludGVyIEFueVN0cnVjdCBDYXBhYmlsaXR5IExpc3QnLFxuICAgICAgbGl0ZXJhbDpcbiAgICAgICAgJ3RydWUgZmFsc2UnXG4gICAgfSxcbiAgICBjb250YWluczogW1xuICAgICAgaGxqcy5RVU9URV9TVFJJTkdfTU9ERSxcbiAgICAgIGhsanMuTlVNQkVSX01PREUsXG4gICAgICBobGpzLkhBU0hfQ09NTUVOVF9NT0RFLFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdtZXRhJyxcbiAgICAgICAgYmVnaW46IC9AMHhbXFx3XFxkXXsxNn07LyxcbiAgICAgICAgaWxsZWdhbDogL1xcbi9cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3N5bWJvbCcsXG4gICAgICAgIGJlZ2luOiAvQFxcZCtcXGIvXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdjbGFzcycsXG4gICAgICAgIGJlZ2luS2V5d29yZHM6ICdzdHJ1Y3QgZW51bScsXG4gICAgICAgIGVuZDogL1xcey8sXG4gICAgICAgIGlsbGVnYWw6IC9cXG4vLFxuICAgICAgICBjb250YWluczogW2hsanMuaW5oZXJpdChobGpzLlRJVExFX01PREUsIHtcbiAgICAgICAgICBzdGFydHM6IHtcbiAgICAgICAgICAgIGVuZHNXaXRoUGFyZW50OiB0cnVlLFxuICAgICAgICAgICAgZXhjbHVkZUVuZDogdHJ1ZVxuICAgICAgICAgIH0gLy8gaGFjazogZWF0aW5nIGV2ZXJ5dGhpbmcgYWZ0ZXIgdGhlIGZpcnN0IHRpdGxlXG4gICAgICAgIH0pXVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnY2xhc3MnLFxuICAgICAgICBiZWdpbktleXdvcmRzOiAnaW50ZXJmYWNlJyxcbiAgICAgICAgZW5kOiAvXFx7LyxcbiAgICAgICAgaWxsZWdhbDogL1xcbi8sXG4gICAgICAgIGNvbnRhaW5zOiBbaGxqcy5pbmhlcml0KGhsanMuVElUTEVfTU9ERSwge1xuICAgICAgICAgIHN0YXJ0czoge1xuICAgICAgICAgICAgZW5kc1dpdGhQYXJlbnQ6IHRydWUsXG4gICAgICAgICAgICBleGNsdWRlRW5kOiB0cnVlXG4gICAgICAgICAgfSAvLyBoYWNrOiBlYXRpbmcgZXZlcnl0aGluZyBhZnRlciB0aGUgZmlyc3QgdGl0bGVcbiAgICAgICAgfSldXG4gICAgICB9XG4gICAgXVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IGNhcG5wcm90bztcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==