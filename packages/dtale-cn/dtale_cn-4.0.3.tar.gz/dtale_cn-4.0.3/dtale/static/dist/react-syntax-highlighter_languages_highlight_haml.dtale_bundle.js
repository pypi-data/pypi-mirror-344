(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_haml"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/haml.js":
/*!***********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/haml.js ***!
  \***********************************************************************************************/
/***/ ((module) => {

/*
Language: HAML
Requires: ruby.js
Author: Dan Allen <dan.j.allen@gmail.com>
Website: http://haml.info
Category: template
*/

// TODO support filter tags like :javascript, support inline HTML
function haml(hljs) {
  return {
    name: 'HAML',
    case_insensitive: true,
    contains: [
      {
        className: 'meta',
        begin: '^!!!( (5|1\\.1|Strict|Frameset|Basic|Mobile|RDFa|XML\\b.*))?$',
        relevance: 10
      },
      // FIXME these comments should be allowed to span indented lines
      hljs.COMMENT(
        '^\\s*(!=#|=#|-#|/).*$',
        false,
        {
          relevance: 0
        }
      ),
      {
        begin: '^\\s*(-|=|!=)(?!#)',
        starts: {
          end: '\\n',
          subLanguage: 'ruby'
        }
      },
      {
        className: 'tag',
        begin: '^\\s*%',
        contains: [
          {
            className: 'selector-tag',
            begin: '\\w+'
          },
          {
            className: 'selector-id',
            begin: '#[\\w-]+'
          },
          {
            className: 'selector-class',
            begin: '\\.[\\w-]+'
          },
          {
            begin: /\{\s*/,
            end: /\s*\}/,
            contains: [
              {
                begin: ':\\w+\\s*=>',
                end: ',\\s+',
                returnBegin: true,
                endsWithParent: true,
                contains: [
                  {
                    className: 'attr',
                    begin: ':\\w+'
                  },
                  hljs.APOS_STRING_MODE,
                  hljs.QUOTE_STRING_MODE,
                  {
                    begin: '\\w+',
                    relevance: 0
                  }
                ]
              }
            ]
          },
          {
            begin: '\\(\\s*',
            end: '\\s*\\)',
            excludeEnd: true,
            contains: [
              {
                begin: '\\w+\\s*=',
                end: '\\s+',
                returnBegin: true,
                endsWithParent: true,
                contains: [
                  {
                    className: 'attr',
                    begin: '\\w+',
                    relevance: 0
                  },
                  hljs.APOS_STRING_MODE,
                  hljs.QUOTE_STRING_MODE,
                  {
                    begin: '\\w+',
                    relevance: 0
                  }
                ]
              }
            ]
          }
        ]
      },
      {
        begin: '^\\s*[=~]\\s*'
      },
      {
        begin: /#\{/,
        starts: {
          end: /\}/,
          subLanguage: 'ruby'
        }
      }
    ]
  };
}

module.exports = haml;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfaGFtbC5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsV0FBVztBQUNYO0FBQ0E7QUFDQTtBQUNBLFdBQVc7QUFDWDtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQSxzQkFBc0I7QUFDdEIsdUJBQXVCO0FBQ3ZCO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsbUJBQW1CO0FBQ25CO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFdBQVc7QUFDWDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxtQkFBbUI7QUFDbkI7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0EsbUJBQW1CO0FBQ25CO0FBQ0Esa0JBQWtCO0FBQ2xCO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvaGFtbC5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKlxuTGFuZ3VhZ2U6IEhBTUxcblJlcXVpcmVzOiBydWJ5LmpzXG5BdXRob3I6IERhbiBBbGxlbiA8ZGFuLmouYWxsZW5AZ21haWwuY29tPlxuV2Vic2l0ZTogaHR0cDovL2hhbWwuaW5mb1xuQ2F0ZWdvcnk6IHRlbXBsYXRlXG4qL1xuXG4vLyBUT0RPIHN1cHBvcnQgZmlsdGVyIHRhZ3MgbGlrZSA6amF2YXNjcmlwdCwgc3VwcG9ydCBpbmxpbmUgSFRNTFxuZnVuY3Rpb24gaGFtbChobGpzKSB7XG4gIHJldHVybiB7XG4gICAgbmFtZTogJ0hBTUwnLFxuICAgIGNhc2VfaW5zZW5zaXRpdmU6IHRydWUsXG4gICAgY29udGFpbnM6IFtcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnbWV0YScsXG4gICAgICAgIGJlZ2luOiAnXiEhISggKDV8MVxcXFwuMXxTdHJpY3R8RnJhbWVzZXR8QmFzaWN8TW9iaWxlfFJERmF8WE1MXFxcXGIuKikpPyQnLFxuICAgICAgICByZWxldmFuY2U6IDEwXG4gICAgICB9LFxuICAgICAgLy8gRklYTUUgdGhlc2UgY29tbWVudHMgc2hvdWxkIGJlIGFsbG93ZWQgdG8gc3BhbiBpbmRlbnRlZCBsaW5lc1xuICAgICAgaGxqcy5DT01NRU5UKFxuICAgICAgICAnXlxcXFxzKighPSN8PSN8LSN8LykuKiQnLFxuICAgICAgICBmYWxzZSxcbiAgICAgICAge1xuICAgICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgICB9XG4gICAgICApLFxuICAgICAge1xuICAgICAgICBiZWdpbjogJ15cXFxccyooLXw9fCE9KSg/ISMpJyxcbiAgICAgICAgc3RhcnRzOiB7XG4gICAgICAgICAgZW5kOiAnXFxcXG4nLFxuICAgICAgICAgIHN1Ykxhbmd1YWdlOiAncnVieSdcbiAgICAgICAgfVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAndGFnJyxcbiAgICAgICAgYmVnaW46ICdeXFxcXHMqJScsXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgY2xhc3NOYW1lOiAnc2VsZWN0b3ItdGFnJyxcbiAgICAgICAgICAgIGJlZ2luOiAnXFxcXHcrJ1xuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgY2xhc3NOYW1lOiAnc2VsZWN0b3ItaWQnLFxuICAgICAgICAgICAgYmVnaW46ICcjW1xcXFx3LV0rJ1xuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgY2xhc3NOYW1lOiAnc2VsZWN0b3ItY2xhc3MnLFxuICAgICAgICAgICAgYmVnaW46ICdcXFxcLltcXFxcdy1dKydcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiAvXFx7XFxzKi8sXG4gICAgICAgICAgICBlbmQ6IC9cXHMqXFx9LyxcbiAgICAgICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgICBiZWdpbjogJzpcXFxcdytcXFxccyo9PicsXG4gICAgICAgICAgICAgICAgZW5kOiAnLFxcXFxzKycsXG4gICAgICAgICAgICAgICAgcmV0dXJuQmVnaW46IHRydWUsXG4gICAgICAgICAgICAgICAgZW5kc1dpdGhQYXJlbnQ6IHRydWUsXG4gICAgICAgICAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgICAgICAgY2xhc3NOYW1lOiAnYXR0cicsXG4gICAgICAgICAgICAgICAgICAgIGJlZ2luOiAnOlxcXFx3KydcbiAgICAgICAgICAgICAgICAgIH0sXG4gICAgICAgICAgICAgICAgICBobGpzLkFQT1NfU1RSSU5HX01PREUsXG4gICAgICAgICAgICAgICAgICBobGpzLlFVT1RFX1NUUklOR19NT0RFLFxuICAgICAgICAgICAgICAgICAge1xuICAgICAgICAgICAgICAgICAgICBiZWdpbjogJ1xcXFx3KycsXG4gICAgICAgICAgICAgICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIF1cbiAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgXVxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgYmVnaW46ICdcXFxcKFxcXFxzKicsXG4gICAgICAgICAgICBlbmQ6ICdcXFxccypcXFxcKScsXG4gICAgICAgICAgICBleGNsdWRlRW5kOiB0cnVlLFxuICAgICAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICAgICAge1xuICAgICAgICAgICAgICAgIGJlZ2luOiAnXFxcXHcrXFxcXHMqPScsXG4gICAgICAgICAgICAgICAgZW5kOiAnXFxcXHMrJyxcbiAgICAgICAgICAgICAgICByZXR1cm5CZWdpbjogdHJ1ZSxcbiAgICAgICAgICAgICAgICBlbmRzV2l0aFBhcmVudDogdHJ1ZSxcbiAgICAgICAgICAgICAgICBjb250YWluczogW1xuICAgICAgICAgICAgICAgICAge1xuICAgICAgICAgICAgICAgICAgICBjbGFzc05hbWU6ICdhdHRyJyxcbiAgICAgICAgICAgICAgICAgICAgYmVnaW46ICdcXFxcdysnLFxuICAgICAgICAgICAgICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgICAgICAgICAgICAgIH0sXG4gICAgICAgICAgICAgICAgICBobGpzLkFQT1NfU1RSSU5HX01PREUsXG4gICAgICAgICAgICAgICAgICBobGpzLlFVT1RFX1NUUklOR19NT0RFLFxuICAgICAgICAgICAgICAgICAge1xuICAgICAgICAgICAgICAgICAgICBiZWdpbjogJ1xcXFx3KycsXG4gICAgICAgICAgICAgICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIF1cbiAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgXVxuICAgICAgICAgIH1cbiAgICAgICAgXVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICdeXFxcXHMqWz1+XVxcXFxzKidcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAvI1xcey8sXG4gICAgICAgIHN0YXJ0czoge1xuICAgICAgICAgIGVuZDogL1xcfS8sXG4gICAgICAgICAgc3ViTGFuZ3VhZ2U6ICdydWJ5J1xuICAgICAgICB9XG4gICAgICB9XG4gICAgXVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IGhhbWw7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=