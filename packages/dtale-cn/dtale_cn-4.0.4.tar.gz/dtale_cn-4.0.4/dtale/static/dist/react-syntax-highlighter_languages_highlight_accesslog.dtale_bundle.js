(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_accesslog"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/accesslog.js":
/*!****************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/accesslog.js ***!
  \****************************************************************************************************/
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

/**
 * Any of the passed expresssions may match
 *
 * Creates a huge this | this | that | that match
 * @param {(RegExp | string)[] } args
 * @returns {string}
 */
function either(...args) {
  const joined = '(' + args.map((x) => source(x)).join("|") + ")";
  return joined;
}

/*
 Language: Apache Access Log
 Author: Oleg Efimov <efimovov@gmail.com>
 Description: Apache/Nginx Access Logs
 Website: https://httpd.apache.org/docs/2.4/logs.html#accesslog
 Audit: 2020
 */

/** @type LanguageFn */
function accesslog(_hljs) {
  // https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
  const HTTP_VERBS = [
    "GET",
    "POST",
    "HEAD",
    "PUT",
    "DELETE",
    "CONNECT",
    "OPTIONS",
    "PATCH",
    "TRACE"
  ];
  return {
    name: 'Apache Access Log',
    contains: [
      // IP
      {
        className: 'number',
        begin: /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(:\d{1,5})?\b/,
        relevance: 5
      },
      // Other numbers
      {
        className: 'number',
        begin: /\b\d+\b/,
        relevance: 0
      },
      // Requests
      {
        className: 'string',
        begin: concat(/"/, either(...HTTP_VERBS)),
        end: /"/,
        keywords: HTTP_VERBS,
        illegal: /\n/,
        relevance: 5,
        contains: [
          {
            begin: /HTTP\/[12]\.\d'/,
            relevance: 5
          }
        ]
      },
      // Dates
      {
        className: 'string',
        // dates must have a certain length, this prevents matching
        // simple array accesses a[123] and [] and other common patterns
        // found in other languages
        begin: /\[\d[^\]\n]{8,}\]/,
        illegal: /\n/,
        relevance: 1
      },
      {
        className: 'string',
        begin: /\[/,
        end: /\]/,
        illegal: /\n/,
        relevance: 0
      },
      // User agent / relevance boost
      {
        className: 'string',
        begin: /"Mozilla\/\d\.\d \(/,
        end: /"/,
        illegal: /\n/,
        relevance: 3
      },
      // Strings
      {
        className: 'string',
        begin: /"/,
        end: /"/,
        illegal: /\n/,
        relevance: 0
      }
    ]
  };
}

module.exports = accesslog;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfYWNjZXNzbG9nLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0EsV0FBVyxRQUFRO0FBQ25CLGFBQWE7QUFDYjs7QUFFQTtBQUNBLFdBQVcsa0JBQWtCO0FBQzdCLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBOztBQUVBO0FBQ0EsV0FBVyx1QkFBdUI7QUFDbEMsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXLHNCQUFzQjtBQUNqQyxhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0Esb0JBQW9CLElBQUksS0FBSyxJQUFJLEtBQUssSUFBSSxLQUFLLElBQUksS0FBSyxJQUFJO0FBQzVEO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSw0QkFBNEIsR0FBRztBQUMvQjtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9hY2Nlc3Nsb2cuanMiXSwic291cmNlc0NvbnRlbnQiOlsiLyoqXG4gKiBAcGFyYW0ge3N0cmluZ30gdmFsdWVcbiAqIEByZXR1cm5zIHtSZWdFeHB9XG4gKiAqL1xuXG4vKipcbiAqIEBwYXJhbSB7UmVnRXhwIHwgc3RyaW5nIH0gcmVcbiAqIEByZXR1cm5zIHtzdHJpbmd9XG4gKi9cbmZ1bmN0aW9uIHNvdXJjZShyZSkge1xuICBpZiAoIXJlKSByZXR1cm4gbnVsbDtcbiAgaWYgKHR5cGVvZiByZSA9PT0gXCJzdHJpbmdcIikgcmV0dXJuIHJlO1xuXG4gIHJldHVybiByZS5zb3VyY2U7XG59XG5cbi8qKlxuICogQHBhcmFtIHsuLi4oUmVnRXhwIHwgc3RyaW5nKSB9IGFyZ3NcbiAqIEByZXR1cm5zIHtzdHJpbmd9XG4gKi9cbmZ1bmN0aW9uIGNvbmNhdCguLi5hcmdzKSB7XG4gIGNvbnN0IGpvaW5lZCA9IGFyZ3MubWFwKCh4KSA9PiBzb3VyY2UoeCkpLmpvaW4oXCJcIik7XG4gIHJldHVybiBqb2luZWQ7XG59XG5cbi8qKlxuICogQW55IG9mIHRoZSBwYXNzZWQgZXhwcmVzc3Npb25zIG1heSBtYXRjaFxuICpcbiAqIENyZWF0ZXMgYSBodWdlIHRoaXMgfCB0aGlzIHwgdGhhdCB8IHRoYXQgbWF0Y2hcbiAqIEBwYXJhbSB7KFJlZ0V4cCB8IHN0cmluZylbXSB9IGFyZ3NcbiAqIEByZXR1cm5zIHtzdHJpbmd9XG4gKi9cbmZ1bmN0aW9uIGVpdGhlciguLi5hcmdzKSB7XG4gIGNvbnN0IGpvaW5lZCA9ICcoJyArIGFyZ3MubWFwKCh4KSA9PiBzb3VyY2UoeCkpLmpvaW4oXCJ8XCIpICsgXCIpXCI7XG4gIHJldHVybiBqb2luZWQ7XG59XG5cbi8qXG4gTGFuZ3VhZ2U6IEFwYWNoZSBBY2Nlc3MgTG9nXG4gQXV0aG9yOiBPbGVnIEVmaW1vdiA8ZWZpbW92b3ZAZ21haWwuY29tPlxuIERlc2NyaXB0aW9uOiBBcGFjaGUvTmdpbnggQWNjZXNzIExvZ3NcbiBXZWJzaXRlOiBodHRwczovL2h0dHBkLmFwYWNoZS5vcmcvZG9jcy8yLjQvbG9ncy5odG1sI2FjY2Vzc2xvZ1xuIEF1ZGl0OiAyMDIwXG4gKi9cblxuLyoqIEB0eXBlIExhbmd1YWdlRm4gKi9cbmZ1bmN0aW9uIGFjY2Vzc2xvZyhfaGxqcykge1xuICAvLyBodHRwczovL2RldmVsb3Blci5tb3ppbGxhLm9yZy9lbi1VUy9kb2NzL1dlYi9IVFRQL01ldGhvZHNcbiAgY29uc3QgSFRUUF9WRVJCUyA9IFtcbiAgICBcIkdFVFwiLFxuICAgIFwiUE9TVFwiLFxuICAgIFwiSEVBRFwiLFxuICAgIFwiUFVUXCIsXG4gICAgXCJERUxFVEVcIixcbiAgICBcIkNPTk5FQ1RcIixcbiAgICBcIk9QVElPTlNcIixcbiAgICBcIlBBVENIXCIsXG4gICAgXCJUUkFDRVwiXG4gIF07XG4gIHJldHVybiB7XG4gICAgbmFtZTogJ0FwYWNoZSBBY2Nlc3MgTG9nJyxcbiAgICBjb250YWluczogW1xuICAgICAgLy8gSVBcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnbnVtYmVyJyxcbiAgICAgICAgYmVnaW46IC9eXFxkezEsM31cXC5cXGR7MSwzfVxcLlxcZHsxLDN9XFwuXFxkezEsM30oOlxcZHsxLDV9KT9cXGIvLFxuICAgICAgICByZWxldmFuY2U6IDVcbiAgICAgIH0sXG4gICAgICAvLyBPdGhlciBudW1iZXJzXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ251bWJlcicsXG4gICAgICAgIGJlZ2luOiAvXFxiXFxkK1xcYi8sXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfSxcbiAgICAgIC8vIFJlcXVlc3RzXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3N0cmluZycsXG4gICAgICAgIGJlZ2luOiBjb25jYXQoL1wiLywgZWl0aGVyKC4uLkhUVFBfVkVSQlMpKSxcbiAgICAgICAgZW5kOiAvXCIvLFxuICAgICAgICBrZXl3b3JkczogSFRUUF9WRVJCUyxcbiAgICAgICAgaWxsZWdhbDogL1xcbi8sXG4gICAgICAgIHJlbGV2YW5jZTogNSxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbjogL0hUVFBcXC9bMTJdXFwuXFxkJy8sXG4gICAgICAgICAgICByZWxldmFuY2U6IDVcbiAgICAgICAgICB9XG4gICAgICAgIF1cbiAgICAgIH0sXG4gICAgICAvLyBEYXRlc1xuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgICAgICAvLyBkYXRlcyBtdXN0IGhhdmUgYSBjZXJ0YWluIGxlbmd0aCwgdGhpcyBwcmV2ZW50cyBtYXRjaGluZ1xuICAgICAgICAvLyBzaW1wbGUgYXJyYXkgYWNjZXNzZXMgYVsxMjNdIGFuZCBbXSBhbmQgb3RoZXIgY29tbW9uIHBhdHRlcm5zXG4gICAgICAgIC8vIGZvdW5kIGluIG90aGVyIGxhbmd1YWdlc1xuICAgICAgICBiZWdpbjogL1xcW1xcZFteXFxdXFxuXXs4LH1cXF0vLFxuICAgICAgICBpbGxlZ2FsOiAvXFxuLyxcbiAgICAgICAgcmVsZXZhbmNlOiAxXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgICAgICBiZWdpbjogL1xcWy8sXG4gICAgICAgIGVuZDogL1xcXS8sXG4gICAgICAgIGlsbGVnYWw6IC9cXG4vLFxuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH0sXG4gICAgICAvLyBVc2VyIGFnZW50IC8gcmVsZXZhbmNlIGJvb3N0XG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3N0cmluZycsXG4gICAgICAgIGJlZ2luOiAvXCJNb3ppbGxhXFwvXFxkXFwuXFxkIFxcKC8sXG4gICAgICAgIGVuZDogL1wiLyxcbiAgICAgICAgaWxsZWdhbDogL1xcbi8sXG4gICAgICAgIHJlbGV2YW5jZTogM1xuICAgICAgfSxcbiAgICAgIC8vIFN0cmluZ3NcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICAgICAgYmVnaW46IC9cIi8sXG4gICAgICAgIGVuZDogL1wiLyxcbiAgICAgICAgaWxsZWdhbDogL1xcbi8sXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfVxuICAgIF1cbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBhY2Nlc3Nsb2c7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=