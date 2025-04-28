(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_protobuf"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/protobuf.js":
/*!***************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/protobuf.js ***!
  \***************************************************************************************************/
/***/ ((module) => {

/*
Language: Protocol Buffers
Author: Dan Tao <daniel.tao@gmail.com>
Description: Protocol buffer message definition format
Website: https://developers.google.com/protocol-buffers/docs/proto3
Category: protocols
*/

function protobuf(hljs) {
  return {
    name: 'Protocol Buffers',
    keywords: {
      keyword: 'package import option optional required repeated group oneof',
      built_in: 'double float int32 int64 uint32 uint64 sint32 sint64 ' +
        'fixed32 fixed64 sfixed32 sfixed64 bool string bytes',
      literal: 'true false'
    },
    contains: [
      hljs.QUOTE_STRING_MODE,
      hljs.NUMBER_MODE,
      hljs.C_LINE_COMMENT_MODE,
      hljs.C_BLOCK_COMMENT_MODE,
      {
        className: 'class',
        beginKeywords: 'message enum service', end: /\{/,
        illegal: /\n/,
        contains: [
          hljs.inherit(hljs.TITLE_MODE, {
            starts: {endsWithParent: true, excludeEnd: true} // hack: eating everything after the first title
          })
        ]
      },
      {
        className: 'function',
        beginKeywords: 'rpc',
        end: /[{;]/, excludeEnd: true,
        keywords: 'rpc returns'
      },
      { // match enum items (relevance)
        // BLAH = ...;
        begin: /^\s*[A-Z_]+(?=\s*=[^\n]+;$)/
      }
    ]
  };
}

module.exports = protobuf;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfcHJvdG9idWYuZHRhbGVfYnVuZGxlLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLHVEQUF1RDtBQUN2RDtBQUNBO0FBQ0E7QUFDQSxxQkFBcUIsd0NBQXdDO0FBQzdELFdBQVc7QUFDWDtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSxpQkFBaUI7QUFDakI7QUFDQSxPQUFPO0FBQ1AsUUFBUTtBQUNSO0FBQ0EseUNBQXlDO0FBQ3pDO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9wcm90b2J1Zi5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKlxuTGFuZ3VhZ2U6IFByb3RvY29sIEJ1ZmZlcnNcbkF1dGhvcjogRGFuIFRhbyA8ZGFuaWVsLnRhb0BnbWFpbC5jb20+XG5EZXNjcmlwdGlvbjogUHJvdG9jb2wgYnVmZmVyIG1lc3NhZ2UgZGVmaW5pdGlvbiBmb3JtYXRcbldlYnNpdGU6IGh0dHBzOi8vZGV2ZWxvcGVycy5nb29nbGUuY29tL3Byb3RvY29sLWJ1ZmZlcnMvZG9jcy9wcm90bzNcbkNhdGVnb3J5OiBwcm90b2NvbHNcbiovXG5cbmZ1bmN0aW9uIHByb3RvYnVmKGhsanMpIHtcbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnUHJvdG9jb2wgQnVmZmVycycsXG4gICAga2V5d29yZHM6IHtcbiAgICAgIGtleXdvcmQ6ICdwYWNrYWdlIGltcG9ydCBvcHRpb24gb3B0aW9uYWwgcmVxdWlyZWQgcmVwZWF0ZWQgZ3JvdXAgb25lb2YnLFxuICAgICAgYnVpbHRfaW46ICdkb3VibGUgZmxvYXQgaW50MzIgaW50NjQgdWludDMyIHVpbnQ2NCBzaW50MzIgc2ludDY0ICcgK1xuICAgICAgICAnZml4ZWQzMiBmaXhlZDY0IHNmaXhlZDMyIHNmaXhlZDY0IGJvb2wgc3RyaW5nIGJ5dGVzJyxcbiAgICAgIGxpdGVyYWw6ICd0cnVlIGZhbHNlJ1xuICAgIH0sXG4gICAgY29udGFpbnM6IFtcbiAgICAgIGhsanMuUVVPVEVfU1RSSU5HX01PREUsXG4gICAgICBobGpzLk5VTUJFUl9NT0RFLFxuICAgICAgaGxqcy5DX0xJTkVfQ09NTUVOVF9NT0RFLFxuICAgICAgaGxqcy5DX0JMT0NLX0NPTU1FTlRfTU9ERSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnY2xhc3MnLFxuICAgICAgICBiZWdpbktleXdvcmRzOiAnbWVzc2FnZSBlbnVtIHNlcnZpY2UnLCBlbmQ6IC9cXHsvLFxuICAgICAgICBpbGxlZ2FsOiAvXFxuLyxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICBobGpzLmluaGVyaXQoaGxqcy5USVRMRV9NT0RFLCB7XG4gICAgICAgICAgICBzdGFydHM6IHtlbmRzV2l0aFBhcmVudDogdHJ1ZSwgZXhjbHVkZUVuZDogdHJ1ZX0gLy8gaGFjazogZWF0aW5nIGV2ZXJ5dGhpbmcgYWZ0ZXIgdGhlIGZpcnN0IHRpdGxlXG4gICAgICAgICAgfSlcbiAgICAgICAgXVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnZnVuY3Rpb24nLFxuICAgICAgICBiZWdpbktleXdvcmRzOiAncnBjJyxcbiAgICAgICAgZW5kOiAvW3s7XS8sIGV4Y2x1ZGVFbmQ6IHRydWUsXG4gICAgICAgIGtleXdvcmRzOiAncnBjIHJldHVybnMnXG4gICAgICB9LFxuICAgICAgeyAvLyBtYXRjaCBlbnVtIGl0ZW1zIChyZWxldmFuY2UpXG4gICAgICAgIC8vIEJMQUggPSAuLi47XG4gICAgICAgIGJlZ2luOiAvXlxccypbQS1aX10rKD89XFxzKj1bXlxcbl0rOyQpL1xuICAgICAgfVxuICAgIF1cbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBwcm90b2J1ZjtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==