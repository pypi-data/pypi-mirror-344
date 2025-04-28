(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_apache"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/apache.js":
/*!*************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/apache.js ***!
  \*************************************************************************************************/
/***/ ((module) => {

/*
Language: Apache config
Author: Ruslan Keba <rukeba@gmail.com>
Contributors: Ivan Sagalaev <maniac@softwaremaniacs.org>
Website: https://httpd.apache.org
Description: language definition for Apache configuration files (httpd.conf & .htaccess)
Category: common, config
Audit: 2020
*/

/** @type LanguageFn */
function apache(hljs) {
  const NUMBER_REF = {
    className: 'number',
    begin: /[$%]\d+/
  };
  const NUMBER = {
    className: 'number',
    begin: /\d+/
  };
  const IP_ADDRESS = {
    className: "number",
    begin: /\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(:\d{1,5})?/
  };
  const PORT_NUMBER = {
    className: "number",
    begin: /:\d{1,5}/
  };
  return {
    name: 'Apache config',
    aliases: [ 'apacheconf' ],
    case_insensitive: true,
    contains: [
      hljs.HASH_COMMENT_MODE,
      {
        className: 'section',
        begin: /<\/?/,
        end: />/,
        contains: [
          IP_ADDRESS,
          PORT_NUMBER,
          // low relevance prevents us from claming XML/HTML where this rule would
          // match strings inside of XML tags
          hljs.inherit(hljs.QUOTE_STRING_MODE, { relevance: 0 })
        ]
      },
      {
        className: 'attribute',
        begin: /\w+/,
        relevance: 0,
        // keywords aren’t needed for highlighting per se, they only boost relevance
        // for a very generally defined mode (starts with a word, ends with line-end
        keywords: {
          nomarkup:
            'order deny allow setenv rewriterule rewriteengine rewritecond documentroot ' +
            'sethandler errordocument loadmodule options header listen serverroot ' +
            'servername'
        },
        starts: {
          end: /$/,
          relevance: 0,
          keywords: { literal: 'on off all deny allow' },
          contains: [
            {
              className: 'meta',
              begin: /\s\[/,
              end: /\]$/
            },
            {
              className: 'variable',
              begin: /[\$%]\{/,
              end: /\}/,
              contains: [
                'self',
                NUMBER_REF
              ]
            },
            IP_ADDRESS,
            NUMBER,
            hljs.QUOTE_STRING_MODE
          ]
        }
      }
    ],
    illegal: /\S/
  };
}

module.exports = apache;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfYXBhY2hlLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxlQUFlLElBQUksS0FBSyxJQUFJLEtBQUssSUFBSSxLQUFLLElBQUksS0FBSyxJQUFJO0FBQ3ZEO0FBQ0E7QUFDQTtBQUNBLGdCQUFnQixJQUFJO0FBQ3BCO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsaURBQWlELGNBQWM7QUFDL0Q7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFNBQVM7QUFDVDtBQUNBO0FBQ0E7QUFDQSxzQkFBc0Isa0NBQWtDO0FBQ3hEO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxhQUFhO0FBQ2I7QUFDQTtBQUNBLDZCQUE2QjtBQUM3QixzQkFBc0I7QUFDdEI7QUFDQTtBQUNBO0FBQ0E7QUFDQSxhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL2FwYWNoZS5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKlxuTGFuZ3VhZ2U6IEFwYWNoZSBjb25maWdcbkF1dGhvcjogUnVzbGFuIEtlYmEgPHJ1a2ViYUBnbWFpbC5jb20+XG5Db250cmlidXRvcnM6IEl2YW4gU2FnYWxhZXYgPG1hbmlhY0Bzb2Z0d2FyZW1hbmlhY3Mub3JnPlxuV2Vic2l0ZTogaHR0cHM6Ly9odHRwZC5hcGFjaGUub3JnXG5EZXNjcmlwdGlvbjogbGFuZ3VhZ2UgZGVmaW5pdGlvbiBmb3IgQXBhY2hlIGNvbmZpZ3VyYXRpb24gZmlsZXMgKGh0dHBkLmNvbmYgJiAuaHRhY2Nlc3MpXG5DYXRlZ29yeTogY29tbW9uLCBjb25maWdcbkF1ZGl0OiAyMDIwXG4qL1xuXG4vKiogQHR5cGUgTGFuZ3VhZ2VGbiAqL1xuZnVuY3Rpb24gYXBhY2hlKGhsanMpIHtcbiAgY29uc3QgTlVNQkVSX1JFRiA9IHtcbiAgICBjbGFzc05hbWU6ICdudW1iZXInLFxuICAgIGJlZ2luOiAvWyQlXVxcZCsvXG4gIH07XG4gIGNvbnN0IE5VTUJFUiA9IHtcbiAgICBjbGFzc05hbWU6ICdudW1iZXInLFxuICAgIGJlZ2luOiAvXFxkKy9cbiAgfTtcbiAgY29uc3QgSVBfQUREUkVTUyA9IHtcbiAgICBjbGFzc05hbWU6IFwibnVtYmVyXCIsXG4gICAgYmVnaW46IC9cXGR7MSwzfVxcLlxcZHsxLDN9XFwuXFxkezEsM31cXC5cXGR7MSwzfSg6XFxkezEsNX0pPy9cbiAgfTtcbiAgY29uc3QgUE9SVF9OVU1CRVIgPSB7XG4gICAgY2xhc3NOYW1lOiBcIm51bWJlclwiLFxuICAgIGJlZ2luOiAvOlxcZHsxLDV9L1xuICB9O1xuICByZXR1cm4ge1xuICAgIG5hbWU6ICdBcGFjaGUgY29uZmlnJyxcbiAgICBhbGlhc2VzOiBbICdhcGFjaGVjb25mJyBdLFxuICAgIGNhc2VfaW5zZW5zaXRpdmU6IHRydWUsXG4gICAgY29udGFpbnM6IFtcbiAgICAgIGhsanMuSEFTSF9DT01NRU5UX01PREUsXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3NlY3Rpb24nLFxuICAgICAgICBiZWdpbjogLzxcXC8/LyxcbiAgICAgICAgZW5kOiAvPi8sXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgSVBfQUREUkVTUyxcbiAgICAgICAgICBQT1JUX05VTUJFUixcbiAgICAgICAgICAvLyBsb3cgcmVsZXZhbmNlIHByZXZlbnRzIHVzIGZyb20gY2xhbWluZyBYTUwvSFRNTCB3aGVyZSB0aGlzIHJ1bGUgd291bGRcbiAgICAgICAgICAvLyBtYXRjaCBzdHJpbmdzIGluc2lkZSBvZiBYTUwgdGFnc1xuICAgICAgICAgIGhsanMuaW5oZXJpdChobGpzLlFVT1RFX1NUUklOR19NT0RFLCB7IHJlbGV2YW5jZTogMCB9KVxuICAgICAgICBdXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdhdHRyaWJ1dGUnLFxuICAgICAgICBiZWdpbjogL1xcdysvLFxuICAgICAgICByZWxldmFuY2U6IDAsXG4gICAgICAgIC8vIGtleXdvcmRzIGFyZW7igJl0IG5lZWRlZCBmb3IgaGlnaGxpZ2h0aW5nIHBlciBzZSwgdGhleSBvbmx5IGJvb3N0IHJlbGV2YW5jZVxuICAgICAgICAvLyBmb3IgYSB2ZXJ5IGdlbmVyYWxseSBkZWZpbmVkIG1vZGUgKHN0YXJ0cyB3aXRoIGEgd29yZCwgZW5kcyB3aXRoIGxpbmUtZW5kXG4gICAgICAgIGtleXdvcmRzOiB7XG4gICAgICAgICAgbm9tYXJrdXA6XG4gICAgICAgICAgICAnb3JkZXIgZGVueSBhbGxvdyBzZXRlbnYgcmV3cml0ZXJ1bGUgcmV3cml0ZWVuZ2luZSByZXdyaXRlY29uZCBkb2N1bWVudHJvb3QgJyArXG4gICAgICAgICAgICAnc2V0aGFuZGxlciBlcnJvcmRvY3VtZW50IGxvYWRtb2R1bGUgb3B0aW9ucyBoZWFkZXIgbGlzdGVuIHNlcnZlcnJvb3QgJyArXG4gICAgICAgICAgICAnc2VydmVybmFtZSdcbiAgICAgICAgfSxcbiAgICAgICAgc3RhcnRzOiB7XG4gICAgICAgICAgZW5kOiAvJC8sXG4gICAgICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgICAgIGtleXdvcmRzOiB7IGxpdGVyYWw6ICdvbiBvZmYgYWxsIGRlbnkgYWxsb3cnIH0sXG4gICAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgY2xhc3NOYW1lOiAnbWV0YScsXG4gICAgICAgICAgICAgIGJlZ2luOiAvXFxzXFxbLyxcbiAgICAgICAgICAgICAgZW5kOiAvXFxdJC9cbiAgICAgICAgICAgIH0sXG4gICAgICAgICAgICB7XG4gICAgICAgICAgICAgIGNsYXNzTmFtZTogJ3ZhcmlhYmxlJyxcbiAgICAgICAgICAgICAgYmVnaW46IC9bXFwkJV1cXHsvLFxuICAgICAgICAgICAgICBlbmQ6IC9cXH0vLFxuICAgICAgICAgICAgICBjb250YWluczogW1xuICAgICAgICAgICAgICAgICdzZWxmJyxcbiAgICAgICAgICAgICAgICBOVU1CRVJfUkVGXG4gICAgICAgICAgICAgIF1cbiAgICAgICAgICAgIH0sXG4gICAgICAgICAgICBJUF9BRERSRVNTLFxuICAgICAgICAgICAgTlVNQkVSLFxuICAgICAgICAgICAgaGxqcy5RVU9URV9TVFJJTkdfTU9ERVxuICAgICAgICAgIF1cbiAgICAgICAgfVxuICAgICAgfVxuICAgIF0sXG4gICAgaWxsZWdhbDogL1xcUy9cbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBhcGFjaGU7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=