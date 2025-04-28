(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_http"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/http.js":
/*!***********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/http.js ***!
  \***********************************************************************************************/
/***/ ((module) => {

/**
 * @param {string} value
 * @returns {RegExp}
 * */

/**
 * @param {RegExp | string } re
 * @returns {string}
 */
function source(re) {
  if (!re) return null;
  if (typeof re === "string") return re;

  return re.source;
}

/**
 * @param {...(RegExp | string) } args
 * @returns {string}
 */
function concat(...args) {
  const joined = args.map((x) => source(x)).join("");
  return joined;
}

/*
Language: HTTP
Description: HTTP request and response headers with automatic body highlighting
Author: Ivan Sagalaev <maniac@softwaremaniacs.org>
Category: common, protocols
Website: https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview
*/

function http(hljs) {
  const VERSION = 'HTTP/(2|1\\.[01])';
  const HEADER_NAME = /[A-Za-z][A-Za-z0-9-]*/;
  const HEADER = {
    className: 'attribute',
    begin: concat('^', HEADER_NAME, '(?=\\:\\s)'),
    starts: {
      contains: [
        {
          className: "punctuation",
          begin: /: /,
          relevance: 0,
          starts: {
            end: '$',
            relevance: 0
          }
        }
      ]
    }
  };
  const HEADERS_AND_BODY = [
    HEADER,
    {
      begin: '\\n\\n',
      starts: { subLanguage: [], endsWithParent: true }
    }
  ];

  return {
    name: 'HTTP',
    aliases: ['https'],
    illegal: /\S/,
    contains: [
      // response
      {
        begin: '^(?=' + VERSION + " \\d{3})",
        end: /$/,
        contains: [
          {
            className: "meta",
            begin: VERSION
          },
          {
            className: 'number', begin: '\\b\\d{3}\\b'
          }
        ],
        starts: {
          end: /\b\B/,
          illegal: /\S/,
          contains: HEADERS_AND_BODY
        }
      },
      // request
      {
        begin: '(?=^[A-Z]+ (.*?) ' + VERSION + '$)',
        end: /$/,
        contains: [
          {
            className: 'string',
            begin: ' ',
            end: ' ',
            excludeBegin: true,
            excludeEnd: true
          },
          {
            className: "meta",
            begin: VERSION
          },
          {
            className: 'keyword',
            begin: '[A-Z]+'
          }
        ],
        starts: {
          end: /\b\B/,
          illegal: /\S/,
          contains: HEADERS_AND_BODY
        }
      },
      // to allow headers to work even without a preamble
      hljs.inherit(HEADER, {
        relevance: 0
      })
    ]
  };
}

module.exports = http;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfaHR0cC5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBLFdBQVcsUUFBUTtBQUNuQixhQUFhO0FBQ2I7O0FBRUE7QUFDQSxXQUFXLGtCQUFrQjtBQUM3QixhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTs7QUFFQTtBQUNBLFdBQVcsdUJBQXVCO0FBQ2xDLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLGdCQUFnQjtBQUNoQjtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0Esd0NBQXdDLEVBQUU7QUFDMUM7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFdBQVc7QUFDWDtBQUNBLGdEQUFnRCxFQUFFO0FBQ2xEO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQTtBQUNBO0FBQ0EsV0FBVztBQUNYO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL2h0dHAuanMiXSwic291cmNlc0NvbnRlbnQiOlsiLyoqXG4gKiBAcGFyYW0ge3N0cmluZ30gdmFsdWVcbiAqIEByZXR1cm5zIHtSZWdFeHB9XG4gKiAqL1xuXG4vKipcbiAqIEBwYXJhbSB7UmVnRXhwIHwgc3RyaW5nIH0gcmVcbiAqIEByZXR1cm5zIHtzdHJpbmd9XG4gKi9cbmZ1bmN0aW9uIHNvdXJjZShyZSkge1xuICBpZiAoIXJlKSByZXR1cm4gbnVsbDtcbiAgaWYgKHR5cGVvZiByZSA9PT0gXCJzdHJpbmdcIikgcmV0dXJuIHJlO1xuXG4gIHJldHVybiByZS5zb3VyY2U7XG59XG5cbi8qKlxuICogQHBhcmFtIHsuLi4oUmVnRXhwIHwgc3RyaW5nKSB9IGFyZ3NcbiAqIEByZXR1cm5zIHtzdHJpbmd9XG4gKi9cbmZ1bmN0aW9uIGNvbmNhdCguLi5hcmdzKSB7XG4gIGNvbnN0IGpvaW5lZCA9IGFyZ3MubWFwKCh4KSA9PiBzb3VyY2UoeCkpLmpvaW4oXCJcIik7XG4gIHJldHVybiBqb2luZWQ7XG59XG5cbi8qXG5MYW5ndWFnZTogSFRUUFxuRGVzY3JpcHRpb246IEhUVFAgcmVxdWVzdCBhbmQgcmVzcG9uc2UgaGVhZGVycyB3aXRoIGF1dG9tYXRpYyBib2R5IGhpZ2hsaWdodGluZ1xuQXV0aG9yOiBJdmFuIFNhZ2FsYWV2IDxtYW5pYWNAc29mdHdhcmVtYW5pYWNzLm9yZz5cbkNhdGVnb3J5OiBjb21tb24sIHByb3RvY29sc1xuV2Vic2l0ZTogaHR0cHM6Ly9kZXZlbG9wZXIubW96aWxsYS5vcmcvZW4tVVMvZG9jcy9XZWIvSFRUUC9PdmVydmlld1xuKi9cblxuZnVuY3Rpb24gaHR0cChobGpzKSB7XG4gIGNvbnN0IFZFUlNJT04gPSAnSFRUUC8oMnwxXFxcXC5bMDFdKSc7XG4gIGNvbnN0IEhFQURFUl9OQU1FID0gL1tBLVphLXpdW0EtWmEtejAtOS1dKi87XG4gIGNvbnN0IEhFQURFUiA9IHtcbiAgICBjbGFzc05hbWU6ICdhdHRyaWJ1dGUnLFxuICAgIGJlZ2luOiBjb25jYXQoJ14nLCBIRUFERVJfTkFNRSwgJyg/PVxcXFw6XFxcXHMpJyksXG4gICAgc3RhcnRzOiB7XG4gICAgICBjb250YWluczogW1xuICAgICAgICB7XG4gICAgICAgICAgY2xhc3NOYW1lOiBcInB1bmN0dWF0aW9uXCIsXG4gICAgICAgICAgYmVnaW46IC86IC8sXG4gICAgICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgICAgIHN0YXJ0czoge1xuICAgICAgICAgICAgZW5kOiAnJCcsXG4gICAgICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgIF1cbiAgICB9XG4gIH07XG4gIGNvbnN0IEhFQURFUlNfQU5EX0JPRFkgPSBbXG4gICAgSEVBREVSLFxuICAgIHtcbiAgICAgIGJlZ2luOiAnXFxcXG5cXFxcbicsXG4gICAgICBzdGFydHM6IHsgc3ViTGFuZ3VhZ2U6IFtdLCBlbmRzV2l0aFBhcmVudDogdHJ1ZSB9XG4gICAgfVxuICBdO1xuXG4gIHJldHVybiB7XG4gICAgbmFtZTogJ0hUVFAnLFxuICAgIGFsaWFzZXM6IFsnaHR0cHMnXSxcbiAgICBpbGxlZ2FsOiAvXFxTLyxcbiAgICBjb250YWluczogW1xuICAgICAgLy8gcmVzcG9uc2VcbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICdeKD89JyArIFZFUlNJT04gKyBcIiBcXFxcZHszfSlcIixcbiAgICAgICAgZW5kOiAvJC8sXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgY2xhc3NOYW1lOiBcIm1ldGFcIixcbiAgICAgICAgICAgIGJlZ2luOiBWRVJTSU9OXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICBjbGFzc05hbWU6ICdudW1iZXInLCBiZWdpbjogJ1xcXFxiXFxcXGR7M31cXFxcYidcbiAgICAgICAgICB9XG4gICAgICAgIF0sXG4gICAgICAgIHN0YXJ0czoge1xuICAgICAgICAgIGVuZDogL1xcYlxcQi8sXG4gICAgICAgICAgaWxsZWdhbDogL1xcUy8sXG4gICAgICAgICAgY29udGFpbnM6IEhFQURFUlNfQU5EX0JPRFlcbiAgICAgICAgfVxuICAgICAgfSxcbiAgICAgIC8vIHJlcXVlc3RcbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICcoPz1eW0EtWl0rICguKj8pICcgKyBWRVJTSU9OICsgJyQpJyxcbiAgICAgICAgZW5kOiAvJC8sXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICAgICAgICAgIGJlZ2luOiAnICcsXG4gICAgICAgICAgICBlbmQ6ICcgJyxcbiAgICAgICAgICAgIGV4Y2x1ZGVCZWdpbjogdHJ1ZSxcbiAgICAgICAgICAgIGV4Y2x1ZGVFbmQ6IHRydWVcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGNsYXNzTmFtZTogXCJtZXRhXCIsXG4gICAgICAgICAgICBiZWdpbjogVkVSU0lPTlxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgY2xhc3NOYW1lOiAna2V5d29yZCcsXG4gICAgICAgICAgICBiZWdpbjogJ1tBLVpdKydcbiAgICAgICAgICB9XG4gICAgICAgIF0sXG4gICAgICAgIHN0YXJ0czoge1xuICAgICAgICAgIGVuZDogL1xcYlxcQi8sXG4gICAgICAgICAgaWxsZWdhbDogL1xcUy8sXG4gICAgICAgICAgY29udGFpbnM6IEhFQURFUlNfQU5EX0JPRFlcbiAgICAgICAgfVxuICAgICAgfSxcbiAgICAgIC8vIHRvIGFsbG93IGhlYWRlcnMgdG8gd29yayBldmVuIHdpdGhvdXQgYSBwcmVhbWJsZVxuICAgICAgaGxqcy5pbmhlcml0KEhFQURFUiwge1xuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH0pXG4gICAgXVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IGh0dHA7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=