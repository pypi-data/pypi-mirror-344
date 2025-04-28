(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_asciidoc"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/asciidoc.js":
/*!***************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/asciidoc.js ***!
  \***************************************************************************************************/
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
Language: AsciiDoc
Requires: xml.js
Author: Dan Allen <dan.j.allen@gmail.com>
Website: http://asciidoc.org
Description: A semantic, text-based document format that can be exported to HTML, DocBook and other backends.
Category: markup
*/

/** @type LanguageFn */
function asciidoc(hljs) {
  const HORIZONTAL_RULE = {
    begin: '^\'{3,}[ \\t]*$',
    relevance: 10
  };
  const ESCAPED_FORMATTING = [
    // escaped constrained formatting marks (i.e., \* \_ or \`)
    {
      begin: /\\[*_`]/
    },
    // escaped unconstrained formatting marks (i.e., \\** \\__ or \\``)
    // must ignore until the next formatting marks
    // this rule might not be 100% compliant with Asciidoctor 2.0 but we are entering undefined behavior territory...
    {
      begin: /\\\\\*{2}[^\n]*?\*{2}/
    },
    {
      begin: /\\\\_{2}[^\n]*_{2}/
    },
    {
      begin: /\\\\`{2}[^\n]*`{2}/
    },
    // guard: constrained formatting mark may not be preceded by ":", ";" or
    // "}". match these so the constrained rule doesn't see them
    {
      begin: /[:;}][*_`](?![*_`])/
    }
  ];
  const STRONG = [
    // inline unconstrained strong (single line)
    {
      className: 'strong',
      begin: /\*{2}([^\n]+?)\*{2}/
    },
    // inline unconstrained strong (multi-line)
    {
      className: 'strong',
      begin: concat(
        /\*\*/,
        /((\*(?!\*)|\\[^\n]|[^*\n\\])+\n)+/,
        /(\*(?!\*)|\\[^\n]|[^*\n\\])*/,
        /\*\*/
      ),
      relevance: 0
    },
    // inline constrained strong (single line)
    {
      className: 'strong',
      // must not precede or follow a word character
      begin: /\B\*(\S|\S[^\n]*?\S)\*(?!\w)/
    },
    // inline constrained strong (multi-line)
    {
      className: 'strong',
      // must not precede or follow a word character
      begin: /\*[^\s]([^\n]+\n)+([^\n]+)\*/
    }
  ];
  const EMPHASIS = [
    // inline unconstrained emphasis (single line)
    {
      className: 'emphasis',
      begin: /_{2}([^\n]+?)_{2}/
    },
    // inline unconstrained emphasis (multi-line)
    {
      className: 'emphasis',
      begin: concat(
        /__/,
        /((_(?!_)|\\[^\n]|[^_\n\\])+\n)+/,
        /(_(?!_)|\\[^\n]|[^_\n\\])*/,
        /__/
      ),
      relevance: 0
    },
    // inline constrained emphasis (single line)
    {
      className: 'emphasis',
      // must not precede or follow a word character
      begin: /\b_(\S|\S[^\n]*?\S)_(?!\w)/
    },
    // inline constrained emphasis (multi-line)
    {
      className: 'emphasis',
      // must not precede or follow a word character
      begin: /_[^\s]([^\n]+\n)+([^\n]+)_/
    },
    // inline constrained emphasis using single quote (legacy)
    {
      className: 'emphasis',
      // must not follow a word character or be followed by a single quote or space
      begin: '\\B\'(?![\'\\s])',
      end: '(\\n{2}|\')',
      // allow escaped single quote followed by word char
      contains: [{
        begin: '\\\\\'\\w',
        relevance: 0
      }],
      relevance: 0
    }
  ];
  const ADMONITION = {
    className: 'symbol',
    begin: '^(NOTE|TIP|IMPORTANT|WARNING|CAUTION):\\s+',
    relevance: 10
  };
  const BULLET_LIST = {
    className: 'bullet',
    begin: '^(\\*+|-+|\\.+|[^\\n]+?::)\\s+'
  };

  return {
    name: 'AsciiDoc',
    aliases: ['adoc'],
    contains: [
      // block comment
      hljs.COMMENT(
        '^/{4,}\\n',
        '\\n/{4,}$',
        // can also be done as...
        // '^/{4,}$',
        // '^/{4,}$',
        {
          relevance: 10
        }
      ),
      // line comment
      hljs.COMMENT(
        '^//',
        '$',
        {
          relevance: 0
        }
      ),
      // title
      {
        className: 'title',
        begin: '^\\.\\w.*$'
      },
      // example, admonition & sidebar blocks
      {
        begin: '^[=\\*]{4,}\\n',
        end: '\\n^[=\\*]{4,}$',
        relevance: 10
      },
      // headings
      {
        className: 'section',
        relevance: 10,
        variants: [
          {
            begin: '^(={1,6})[ \t].+?([ \t]\\1)?$'
          },
          {
            begin: '^[^\\[\\]\\n]+?\\n[=\\-~\\^\\+]{2,}$'
          }
        ]
      },
      // document attributes
      {
        className: 'meta',
        begin: '^:.+?:',
        end: '\\s',
        excludeEnd: true,
        relevance: 10
      },
      // block attributes
      {
        className: 'meta',
        begin: '^\\[.+?\\]$',
        relevance: 0
      },
      // quoteblocks
      {
        className: 'quote',
        begin: '^_{4,}\\n',
        end: '\\n_{4,}$',
        relevance: 10
      },
      // listing and literal blocks
      {
        className: 'code',
        begin: '^[\\-\\.]{4,}\\n',
        end: '\\n[\\-\\.]{4,}$',
        relevance: 10
      },
      // passthrough blocks
      {
        begin: '^\\+{4,}\\n',
        end: '\\n\\+{4,}$',
        contains: [{
          begin: '<',
          end: '>',
          subLanguage: 'xml',
          relevance: 0
        }],
        relevance: 10
      },

      BULLET_LIST,
      ADMONITION,
      ...ESCAPED_FORMATTING,
      ...STRONG,
      ...EMPHASIS,

      // inline smart quotes
      {
        className: 'string',
        variants: [
          {
            begin: "``.+?''"
          },
          {
            begin: "`.+?'"
          }
        ]
      },
      // inline unconstrained emphasis
      {
        className: 'code',
        begin: /`{2}/,
        end: /(\n{2}|`{2})/
      },
      // inline code snippets (TODO should get same treatment as strong and emphasis)
      {
        className: 'code',
        begin: '(`.+?`|\\+.+?\\+)',
        relevance: 0
      },
      // indented literal block
      {
        className: 'code',
        begin: '^[ \\t]',
        end: '$',
        relevance: 0
      },
      HORIZONTAL_RULE,
      // images and links
      {
        begin: '(link:)?(http|https|ftp|file|irc|image:?):\\S+?\\[[^[]*?\\]',
        returnBegin: true,
        contains: [
          {
            begin: '(link|image:?):',
            relevance: 0
          },
          {
            className: 'link',
            begin: '\\w',
            end: '[^\\[]+',
            relevance: 0
          },
          {
            className: 'string',
            begin: '\\[',
            end: '\\]',
            excludeBegin: true,
            excludeEnd: true,
            relevance: 0
          }
        ],
        relevance: 10
      }
    ]
  };
}

module.exports = asciidoc;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfYXNjaWlkb2MuZHRhbGVfYnVuZGxlLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7O0FBQUE7QUFDQSxXQUFXLFFBQVE7QUFDbkIsYUFBYTtBQUNiOztBQUVBO0FBQ0EsV0FBVyxrQkFBa0I7QUFDN0IsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7O0FBRUE7QUFDQSxXQUFXLHVCQUF1QjtBQUNsQyxhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBLGdCQUFnQixHQUFHO0FBQ25CO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7QUFDQTtBQUNBLHFCQUFxQixFQUFFLFVBQVUsRUFBRTtBQUNuQyxLQUFLO0FBQ0w7QUFDQSxvQkFBb0IsRUFBRSxRQUFRLEVBQUU7QUFDaEMsS0FBSztBQUNMO0FBQ0Esb0JBQW9CLEVBQUUsUUFBUSxFQUFFO0FBQ2hDLEtBQUs7QUFDTCx3RUFBd0U7QUFDeEUsU0FBUztBQUNUO0FBQ0Esa0JBQWtCO0FBQ2xCO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLGlCQUFpQixFQUFFLFlBQVksRUFBRTtBQUNqQyxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsZ0JBQWdCLEVBQUUsV0FBVyxFQUFFO0FBQy9CLEtBQUs7QUFDTDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLGlCQUFpQixFQUFFO0FBQ25CO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxZQUFZLEdBQUc7QUFDZixjQUFjLEdBQUc7QUFDakI7QUFDQSxlQUFlLEdBQUc7QUFDbEIsZUFBZSxHQUFHO0FBQ2xCO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQSx3QkFBd0IsR0FBRztBQUMzQix5QkFBeUIsR0FBRztBQUM1QjtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSx3QkFBd0IsSUFBSTtBQUM1QixXQUFXO0FBQ1g7QUFDQSxvREFBb0QsR0FBRztBQUN2RDtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0EsbUJBQW1CLEdBQUc7QUFDdEIsbUJBQW1CLEdBQUc7QUFDdEI7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0EsMEJBQTBCLEdBQUc7QUFDN0IsMEJBQTBCLEdBQUc7QUFDN0I7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBLHFCQUFxQixHQUFHO0FBQ3hCLHFCQUFxQixHQUFHO0FBQ3hCO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxTQUFTO0FBQ1Q7QUFDQSxPQUFPOztBQUVQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsV0FBVztBQUNYO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLGtCQUFrQixFQUFFO0FBQ3BCLGtCQUFrQixFQUFFLEdBQUcsRUFBRTtBQUN6QixPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsV0FBVztBQUNYO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvYXNjaWlkb2MuanMiXSwic291cmNlc0NvbnRlbnQiOlsiLyoqXG4gKiBAcGFyYW0ge3N0cmluZ30gdmFsdWVcbiAqIEByZXR1cm5zIHtSZWdFeHB9XG4gKiAqL1xuXG4vKipcbiAqIEBwYXJhbSB7UmVnRXhwIHwgc3RyaW5nIH0gcmVcbiAqIEByZXR1cm5zIHtzdHJpbmd9XG4gKi9cbmZ1bmN0aW9uIHNvdXJjZShyZSkge1xuICBpZiAoIXJlKSByZXR1cm4gbnVsbDtcbiAgaWYgKHR5cGVvZiByZSA9PT0gXCJzdHJpbmdcIikgcmV0dXJuIHJlO1xuXG4gIHJldHVybiByZS5zb3VyY2U7XG59XG5cbi8qKlxuICogQHBhcmFtIHsuLi4oUmVnRXhwIHwgc3RyaW5nKSB9IGFyZ3NcbiAqIEByZXR1cm5zIHtzdHJpbmd9XG4gKi9cbmZ1bmN0aW9uIGNvbmNhdCguLi5hcmdzKSB7XG4gIGNvbnN0IGpvaW5lZCA9IGFyZ3MubWFwKCh4KSA9PiBzb3VyY2UoeCkpLmpvaW4oXCJcIik7XG4gIHJldHVybiBqb2luZWQ7XG59XG5cbi8qXG5MYW5ndWFnZTogQXNjaWlEb2NcblJlcXVpcmVzOiB4bWwuanNcbkF1dGhvcjogRGFuIEFsbGVuIDxkYW4uai5hbGxlbkBnbWFpbC5jb20+XG5XZWJzaXRlOiBodHRwOi8vYXNjaWlkb2Mub3JnXG5EZXNjcmlwdGlvbjogQSBzZW1hbnRpYywgdGV4dC1iYXNlZCBkb2N1bWVudCBmb3JtYXQgdGhhdCBjYW4gYmUgZXhwb3J0ZWQgdG8gSFRNTCwgRG9jQm9vayBhbmQgb3RoZXIgYmFja2VuZHMuXG5DYXRlZ29yeTogbWFya3VwXG4qL1xuXG4vKiogQHR5cGUgTGFuZ3VhZ2VGbiAqL1xuZnVuY3Rpb24gYXNjaWlkb2MoaGxqcykge1xuICBjb25zdCBIT1JJWk9OVEFMX1JVTEUgPSB7XG4gICAgYmVnaW46ICdeXFwnezMsfVsgXFxcXHRdKiQnLFxuICAgIHJlbGV2YW5jZTogMTBcbiAgfTtcbiAgY29uc3QgRVNDQVBFRF9GT1JNQVRUSU5HID0gW1xuICAgIC8vIGVzY2FwZWQgY29uc3RyYWluZWQgZm9ybWF0dGluZyBtYXJrcyAoaS5lLiwgXFwqIFxcXyBvciBcXGApXG4gICAge1xuICAgICAgYmVnaW46IC9cXFxcWypfYF0vXG4gICAgfSxcbiAgICAvLyBlc2NhcGVkIHVuY29uc3RyYWluZWQgZm9ybWF0dGluZyBtYXJrcyAoaS5lLiwgXFxcXCoqIFxcXFxfXyBvciBcXFxcYGApXG4gICAgLy8gbXVzdCBpZ25vcmUgdW50aWwgdGhlIG5leHQgZm9ybWF0dGluZyBtYXJrc1xuICAgIC8vIHRoaXMgcnVsZSBtaWdodCBub3QgYmUgMTAwJSBjb21wbGlhbnQgd2l0aCBBc2NpaWRvY3RvciAyLjAgYnV0IHdlIGFyZSBlbnRlcmluZyB1bmRlZmluZWQgYmVoYXZpb3IgdGVycml0b3J5Li4uXG4gICAge1xuICAgICAgYmVnaW46IC9cXFxcXFxcXFxcKnsyfVteXFxuXSo/XFwqezJ9L1xuICAgIH0sXG4gICAge1xuICAgICAgYmVnaW46IC9cXFxcXFxcXF97Mn1bXlxcbl0qX3syfS9cbiAgICB9LFxuICAgIHtcbiAgICAgIGJlZ2luOiAvXFxcXFxcXFxgezJ9W15cXG5dKmB7Mn0vXG4gICAgfSxcbiAgICAvLyBndWFyZDogY29uc3RyYWluZWQgZm9ybWF0dGluZyBtYXJrIG1heSBub3QgYmUgcHJlY2VkZWQgYnkgXCI6XCIsIFwiO1wiIG9yXG4gICAgLy8gXCJ9XCIuIG1hdGNoIHRoZXNlIHNvIHRoZSBjb25zdHJhaW5lZCBydWxlIGRvZXNuJ3Qgc2VlIHRoZW1cbiAgICB7XG4gICAgICBiZWdpbjogL1s6O31dWypfYF0oPyFbKl9gXSkvXG4gICAgfVxuICBdO1xuICBjb25zdCBTVFJPTkcgPSBbXG4gICAgLy8gaW5saW5lIHVuY29uc3RyYWluZWQgc3Ryb25nIChzaW5nbGUgbGluZSlcbiAgICB7XG4gICAgICBjbGFzc05hbWU6ICdzdHJvbmcnLFxuICAgICAgYmVnaW46IC9cXCp7Mn0oW15cXG5dKz8pXFwqezJ9L1xuICAgIH0sXG4gICAgLy8gaW5saW5lIHVuY29uc3RyYWluZWQgc3Ryb25nIChtdWx0aS1saW5lKVxuICAgIHtcbiAgICAgIGNsYXNzTmFtZTogJ3N0cm9uZycsXG4gICAgICBiZWdpbjogY29uY2F0KFxuICAgICAgICAvXFwqXFwqLyxcbiAgICAgICAgLygoXFwqKD8hXFwqKXxcXFxcW15cXG5dfFteKlxcblxcXFxdKStcXG4pKy8sXG4gICAgICAgIC8oXFwqKD8hXFwqKXxcXFxcW15cXG5dfFteKlxcblxcXFxdKSovLFxuICAgICAgICAvXFwqXFwqL1xuICAgICAgKSxcbiAgICAgIHJlbGV2YW5jZTogMFxuICAgIH0sXG4gICAgLy8gaW5saW5lIGNvbnN0cmFpbmVkIHN0cm9uZyAoc2luZ2xlIGxpbmUpXG4gICAge1xuICAgICAgY2xhc3NOYW1lOiAnc3Ryb25nJyxcbiAgICAgIC8vIG11c3Qgbm90IHByZWNlZGUgb3IgZm9sbG93IGEgd29yZCBjaGFyYWN0ZXJcbiAgICAgIGJlZ2luOiAvXFxCXFwqKFxcU3xcXFNbXlxcbl0qP1xcUylcXCooPyFcXHcpL1xuICAgIH0sXG4gICAgLy8gaW5saW5lIGNvbnN0cmFpbmVkIHN0cm9uZyAobXVsdGktbGluZSlcbiAgICB7XG4gICAgICBjbGFzc05hbWU6ICdzdHJvbmcnLFxuICAgICAgLy8gbXVzdCBub3QgcHJlY2VkZSBvciBmb2xsb3cgYSB3b3JkIGNoYXJhY3RlclxuICAgICAgYmVnaW46IC9cXCpbXlxcc10oW15cXG5dK1xcbikrKFteXFxuXSspXFwqL1xuICAgIH1cbiAgXTtcbiAgY29uc3QgRU1QSEFTSVMgPSBbXG4gICAgLy8gaW5saW5lIHVuY29uc3RyYWluZWQgZW1waGFzaXMgKHNpbmdsZSBsaW5lKVxuICAgIHtcbiAgICAgIGNsYXNzTmFtZTogJ2VtcGhhc2lzJyxcbiAgICAgIGJlZ2luOiAvX3syfShbXlxcbl0rPylfezJ9L1xuICAgIH0sXG4gICAgLy8gaW5saW5lIHVuY29uc3RyYWluZWQgZW1waGFzaXMgKG11bHRpLWxpbmUpXG4gICAge1xuICAgICAgY2xhc3NOYW1lOiAnZW1waGFzaXMnLFxuICAgICAgYmVnaW46IGNvbmNhdChcbiAgICAgICAgL19fLyxcbiAgICAgICAgLygoXyg/IV8pfFxcXFxbXlxcbl18W15fXFxuXFxcXF0pK1xcbikrLyxcbiAgICAgICAgLyhfKD8hXyl8XFxcXFteXFxuXXxbXl9cXG5cXFxcXSkqLyxcbiAgICAgICAgL19fL1xuICAgICAgKSxcbiAgICAgIHJlbGV2YW5jZTogMFxuICAgIH0sXG4gICAgLy8gaW5saW5lIGNvbnN0cmFpbmVkIGVtcGhhc2lzIChzaW5nbGUgbGluZSlcbiAgICB7XG4gICAgICBjbGFzc05hbWU6ICdlbXBoYXNpcycsXG4gICAgICAvLyBtdXN0IG5vdCBwcmVjZWRlIG9yIGZvbGxvdyBhIHdvcmQgY2hhcmFjdGVyXG4gICAgICBiZWdpbjogL1xcYl8oXFxTfFxcU1teXFxuXSo/XFxTKV8oPyFcXHcpL1xuICAgIH0sXG4gICAgLy8gaW5saW5lIGNvbnN0cmFpbmVkIGVtcGhhc2lzIChtdWx0aS1saW5lKVxuICAgIHtcbiAgICAgIGNsYXNzTmFtZTogJ2VtcGhhc2lzJyxcbiAgICAgIC8vIG11c3Qgbm90IHByZWNlZGUgb3IgZm9sbG93IGEgd29yZCBjaGFyYWN0ZXJcbiAgICAgIGJlZ2luOiAvX1teXFxzXShbXlxcbl0rXFxuKSsoW15cXG5dKylfL1xuICAgIH0sXG4gICAgLy8gaW5saW5lIGNvbnN0cmFpbmVkIGVtcGhhc2lzIHVzaW5nIHNpbmdsZSBxdW90ZSAobGVnYWN5KVxuICAgIHtcbiAgICAgIGNsYXNzTmFtZTogJ2VtcGhhc2lzJyxcbiAgICAgIC8vIG11c3Qgbm90IGZvbGxvdyBhIHdvcmQgY2hhcmFjdGVyIG9yIGJlIGZvbGxvd2VkIGJ5IGEgc2luZ2xlIHF1b3RlIG9yIHNwYWNlXG4gICAgICBiZWdpbjogJ1xcXFxCXFwnKD8hW1xcJ1xcXFxzXSknLFxuICAgICAgZW5kOiAnKFxcXFxuezJ9fFxcJyknLFxuICAgICAgLy8gYWxsb3cgZXNjYXBlZCBzaW5nbGUgcXVvdGUgZm9sbG93ZWQgYnkgd29yZCBjaGFyXG4gICAgICBjb250YWluczogW3tcbiAgICAgICAgYmVnaW46ICdcXFxcXFxcXFxcJ1xcXFx3JyxcbiAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICB9XSxcbiAgICAgIHJlbGV2YW5jZTogMFxuICAgIH1cbiAgXTtcbiAgY29uc3QgQURNT05JVElPTiA9IHtcbiAgICBjbGFzc05hbWU6ICdzeW1ib2wnLFxuICAgIGJlZ2luOiAnXihOT1RFfFRJUHxJTVBPUlRBTlR8V0FSTklOR3xDQVVUSU9OKTpcXFxccysnLFxuICAgIHJlbGV2YW5jZTogMTBcbiAgfTtcbiAgY29uc3QgQlVMTEVUX0xJU1QgPSB7XG4gICAgY2xhc3NOYW1lOiAnYnVsbGV0JyxcbiAgICBiZWdpbjogJ14oXFxcXCorfC0rfFxcXFwuK3xbXlxcXFxuXSs/OjopXFxcXHMrJ1xuICB9O1xuXG4gIHJldHVybiB7XG4gICAgbmFtZTogJ0FzY2lpRG9jJyxcbiAgICBhbGlhc2VzOiBbJ2Fkb2MnXSxcbiAgICBjb250YWluczogW1xuICAgICAgLy8gYmxvY2sgY29tbWVudFxuICAgICAgaGxqcy5DT01NRU5UKFxuICAgICAgICAnXi97NCx9XFxcXG4nLFxuICAgICAgICAnXFxcXG4vezQsfSQnLFxuICAgICAgICAvLyBjYW4gYWxzbyBiZSBkb25lIGFzLi4uXG4gICAgICAgIC8vICdeL3s0LH0kJyxcbiAgICAgICAgLy8gJ14vezQsfSQnLFxuICAgICAgICB7XG4gICAgICAgICAgcmVsZXZhbmNlOiAxMFxuICAgICAgICB9XG4gICAgICApLFxuICAgICAgLy8gbGluZSBjb21tZW50XG4gICAgICBobGpzLkNPTU1FTlQoXG4gICAgICAgICdeLy8nLFxuICAgICAgICAnJCcsXG4gICAgICAgIHtcbiAgICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgICAgfVxuICAgICAgKSxcbiAgICAgIC8vIHRpdGxlXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3RpdGxlJyxcbiAgICAgICAgYmVnaW46ICdeXFxcXC5cXFxcdy4qJCdcbiAgICAgIH0sXG4gICAgICAvLyBleGFtcGxlLCBhZG1vbml0aW9uICYgc2lkZWJhciBibG9ja3NcbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICdeWz1cXFxcKl17NCx9XFxcXG4nLFxuICAgICAgICBlbmQ6ICdcXFxcbl5bPVxcXFwqXXs0LH0kJyxcbiAgICAgICAgcmVsZXZhbmNlOiAxMFxuICAgICAgfSxcbiAgICAgIC8vIGhlYWRpbmdzXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3NlY3Rpb24nLFxuICAgICAgICByZWxldmFuY2U6IDEwLFxuICAgICAgICB2YXJpYW50czogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiAnXig9ezEsNn0pWyBcXHRdLis/KFsgXFx0XVxcXFwxKT8kJ1xuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgYmVnaW46ICdeW15cXFxcW1xcXFxdXFxcXG5dKz9cXFxcbls9XFxcXC1+XFxcXF5cXFxcK117Mix9JCdcbiAgICAgICAgICB9XG4gICAgICAgIF1cbiAgICAgIH0sXG4gICAgICAvLyBkb2N1bWVudCBhdHRyaWJ1dGVzXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ21ldGEnLFxuICAgICAgICBiZWdpbjogJ146Lis/OicsXG4gICAgICAgIGVuZDogJ1xcXFxzJyxcbiAgICAgICAgZXhjbHVkZUVuZDogdHJ1ZSxcbiAgICAgICAgcmVsZXZhbmNlOiAxMFxuICAgICAgfSxcbiAgICAgIC8vIGJsb2NrIGF0dHJpYnV0ZXNcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnbWV0YScsXG4gICAgICAgIGJlZ2luOiAnXlxcXFxbLis/XFxcXF0kJyxcbiAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICB9LFxuICAgICAgLy8gcXVvdGVibG9ja3NcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAncXVvdGUnLFxuICAgICAgICBiZWdpbjogJ15fezQsfVxcXFxuJyxcbiAgICAgICAgZW5kOiAnXFxcXG5fezQsfSQnLFxuICAgICAgICByZWxldmFuY2U6IDEwXG4gICAgICB9LFxuICAgICAgLy8gbGlzdGluZyBhbmQgbGl0ZXJhbCBibG9ja3NcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnY29kZScsXG4gICAgICAgIGJlZ2luOiAnXltcXFxcLVxcXFwuXXs0LH1cXFxcbicsXG4gICAgICAgIGVuZDogJ1xcXFxuW1xcXFwtXFxcXC5dezQsfSQnLFxuICAgICAgICByZWxldmFuY2U6IDEwXG4gICAgICB9LFxuICAgICAgLy8gcGFzc3Rocm91Z2ggYmxvY2tzXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnXlxcXFwrezQsfVxcXFxuJyxcbiAgICAgICAgZW5kOiAnXFxcXG5cXFxcK3s0LH0kJyxcbiAgICAgICAgY29udGFpbnM6IFt7XG4gICAgICAgICAgYmVnaW46ICc8JyxcbiAgICAgICAgICBlbmQ6ICc+JyxcbiAgICAgICAgICBzdWJMYW5ndWFnZTogJ3htbCcsXG4gICAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICAgIH1dLFxuICAgICAgICByZWxldmFuY2U6IDEwXG4gICAgICB9LFxuXG4gICAgICBCVUxMRVRfTElTVCxcbiAgICAgIEFETU9OSVRJT04sXG4gICAgICAuLi5FU0NBUEVEX0ZPUk1BVFRJTkcsXG4gICAgICAuLi5TVFJPTkcsXG4gICAgICAuLi5FTVBIQVNJUyxcblxuICAgICAgLy8gaW5saW5lIHNtYXJ0IHF1b3Rlc1xuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgICAgICB2YXJpYW50czogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiBcImBgLis/JydcIlxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgYmVnaW46IFwiYC4rPydcIlxuICAgICAgICAgIH1cbiAgICAgICAgXVxuICAgICAgfSxcbiAgICAgIC8vIGlubGluZSB1bmNvbnN0cmFpbmVkIGVtcGhhc2lzXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ2NvZGUnLFxuICAgICAgICBiZWdpbjogL2B7Mn0vLFxuICAgICAgICBlbmQ6IC8oXFxuezJ9fGB7Mn0pL1xuICAgICAgfSxcbiAgICAgIC8vIGlubGluZSBjb2RlIHNuaXBwZXRzIChUT0RPIHNob3VsZCBnZXQgc2FtZSB0cmVhdG1lbnQgYXMgc3Ryb25nIGFuZCBlbXBoYXNpcylcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnY29kZScsXG4gICAgICAgIGJlZ2luOiAnKGAuKz9gfFxcXFwrLis/XFxcXCspJyxcbiAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICB9LFxuICAgICAgLy8gaW5kZW50ZWQgbGl0ZXJhbCBibG9ja1xuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdjb2RlJyxcbiAgICAgICAgYmVnaW46ICdeWyBcXFxcdF0nLFxuICAgICAgICBlbmQ6ICckJyxcbiAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICB9LFxuICAgICAgSE9SSVpPTlRBTF9SVUxFLFxuICAgICAgLy8gaW1hZ2VzIGFuZCBsaW5rc1xuICAgICAge1xuICAgICAgICBiZWdpbjogJyhsaW5rOik/KGh0dHB8aHR0cHN8ZnRwfGZpbGV8aXJjfGltYWdlOj8pOlxcXFxTKz9cXFxcW1teW10qP1xcXFxdJyxcbiAgICAgICAgcmV0dXJuQmVnaW46IHRydWUsXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgYmVnaW46ICcobGlua3xpbWFnZTo/KTonLFxuICAgICAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICBjbGFzc05hbWU6ICdsaW5rJyxcbiAgICAgICAgICAgIGJlZ2luOiAnXFxcXHcnLFxuICAgICAgICAgICAgZW5kOiAnW15cXFxcW10rJyxcbiAgICAgICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICAgICAgICAgIGJlZ2luOiAnXFxcXFsnLFxuICAgICAgICAgICAgZW5kOiAnXFxcXF0nLFxuICAgICAgICAgICAgZXhjbHVkZUJlZ2luOiB0cnVlLFxuICAgICAgICAgICAgZXhjbHVkZUVuZDogdHJ1ZSxcbiAgICAgICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgICAgIH1cbiAgICAgICAgXSxcbiAgICAgICAgcmVsZXZhbmNlOiAxMFxuICAgICAgfVxuICAgIF1cbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBhc2NpaWRvYztcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==