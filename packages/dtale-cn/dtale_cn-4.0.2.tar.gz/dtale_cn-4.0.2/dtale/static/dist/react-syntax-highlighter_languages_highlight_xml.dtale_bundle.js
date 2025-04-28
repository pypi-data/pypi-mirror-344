(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_xml"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/xml.js":
/*!**********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/xml.js ***!
  \**********************************************************************************************/
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
 * @param {RegExp | string } re
 * @returns {string}
 */
function lookahead(re) {
  return concat('(?=', re, ')');
}

/**
 * @param {RegExp | string } re
 * @returns {string}
 */
function optional(re) {
  return concat('(', re, ')?');
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
Language: HTML, XML
Website: https://www.w3.org/XML/
Category: common
Audit: 2020
*/

/** @type LanguageFn */
function xml(hljs) {
  // Element names can contain letters, digits, hyphens, underscores, and periods
  const TAG_NAME_RE = concat(/[A-Z_]/, optional(/[A-Z0-9_.-]*:/), /[A-Z0-9_.-]*/);
  const XML_IDENT_RE = /[A-Za-z0-9._:-]+/;
  const XML_ENTITIES = {
    className: 'symbol',
    begin: /&[a-z]+;|&#[0-9]+;|&#x[a-f0-9]+;/
  };
  const XML_META_KEYWORDS = {
    begin: /\s/,
    contains: [
      {
        className: 'meta-keyword',
        begin: /#?[a-z_][a-z1-9_-]+/,
        illegal: /\n/
      }
    ]
  };
  const XML_META_PAR_KEYWORDS = hljs.inherit(XML_META_KEYWORDS, {
    begin: /\(/,
    end: /\)/
  });
  const APOS_META_STRING_MODE = hljs.inherit(hljs.APOS_STRING_MODE, {
    className: 'meta-string'
  });
  const QUOTE_META_STRING_MODE = hljs.inherit(hljs.QUOTE_STRING_MODE, {
    className: 'meta-string'
  });
  const TAG_INTERNALS = {
    endsWithParent: true,
    illegal: /</,
    relevance: 0,
    contains: [
      {
        className: 'attr',
        begin: XML_IDENT_RE,
        relevance: 0
      },
      {
        begin: /=\s*/,
        relevance: 0,
        contains: [
          {
            className: 'string',
            endsParent: true,
            variants: [
              {
                begin: /"/,
                end: /"/,
                contains: [ XML_ENTITIES ]
              },
              {
                begin: /'/,
                end: /'/,
                contains: [ XML_ENTITIES ]
              },
              {
                begin: /[^\s"'=<>`]+/
              }
            ]
          }
        ]
      }
    ]
  };
  return {
    name: 'HTML, XML',
    aliases: [
      'html',
      'xhtml',
      'rss',
      'atom',
      'xjb',
      'xsd',
      'xsl',
      'plist',
      'wsf',
      'svg'
    ],
    case_insensitive: true,
    contains: [
      {
        className: 'meta',
        begin: /<![a-z]/,
        end: />/,
        relevance: 10,
        contains: [
          XML_META_KEYWORDS,
          QUOTE_META_STRING_MODE,
          APOS_META_STRING_MODE,
          XML_META_PAR_KEYWORDS,
          {
            begin: /\[/,
            end: /\]/,
            contains: [
              {
                className: 'meta',
                begin: /<![a-z]/,
                end: />/,
                contains: [
                  XML_META_KEYWORDS,
                  XML_META_PAR_KEYWORDS,
                  QUOTE_META_STRING_MODE,
                  APOS_META_STRING_MODE
                ]
              }
            ]
          }
        ]
      },
      hljs.COMMENT(
        /<!--/,
        /-->/,
        {
          relevance: 10
        }
      ),
      {
        begin: /<!\[CDATA\[/,
        end: /\]\]>/,
        relevance: 10
      },
      XML_ENTITIES,
      {
        className: 'meta',
        begin: /<\?xml/,
        end: /\?>/,
        relevance: 10
      },
      {
        className: 'tag',
        /*
        The lookahead pattern (?=...) ensures that 'begin' only matches
        '<style' as a single word, followed by a whitespace or an
        ending braket. The '$' is needed for the lexeme to be recognized
        by hljs.subMode() that tests lexemes outside the stream.
        */
        begin: /<style(?=\s|>)/,
        end: />/,
        keywords: {
          name: 'style'
        },
        contains: [ TAG_INTERNALS ],
        starts: {
          end: /<\/style>/,
          returnEnd: true,
          subLanguage: [
            'css',
            'xml'
          ]
        }
      },
      {
        className: 'tag',
        // See the comment in the <style tag about the lookahead pattern
        begin: /<script(?=\s|>)/,
        end: />/,
        keywords: {
          name: 'script'
        },
        contains: [ TAG_INTERNALS ],
        starts: {
          end: /<\/script>/,
          returnEnd: true,
          subLanguage: [
            'javascript',
            'handlebars',
            'xml'
          ]
        }
      },
      // we need this for now for jSX
      {
        className: 'tag',
        begin: /<>|<\/>/
      },
      // open tag
      {
        className: 'tag',
        begin: concat(
          /</,
          lookahead(concat(
            TAG_NAME_RE,
            // <tag/>
            // <tag>
            // <tag ...
            either(/\/>/, />/, /\s/)
          ))
        ),
        end: /\/?>/,
        contains: [
          {
            className: 'name',
            begin: TAG_NAME_RE,
            relevance: 0,
            starts: TAG_INTERNALS
          }
        ]
      },
      // close tag
      {
        className: 'tag',
        begin: concat(
          /<\//,
          lookahead(concat(
            TAG_NAME_RE, />/
          ))
        ),
        contains: [
          {
            className: 'name',
            begin: TAG_NAME_RE,
            relevance: 0
          },
          {
            begin: />/,
            relevance: 0,
            endsParent: true
          }
        ]
      }
    ]
  };
}

module.exports = xml;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfeG1sLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0EsV0FBVyxRQUFRO0FBQ25CLGFBQWE7QUFDYjs7QUFFQTtBQUNBLFdBQVcsa0JBQWtCO0FBQzdCLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBOztBQUVBO0FBQ0EsV0FBVyxrQkFBa0I7QUFDN0IsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0EsV0FBVyxrQkFBa0I7QUFDN0IsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0EsV0FBVyx1QkFBdUI7QUFDbEMsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXLHNCQUFzQjtBQUNqQyxhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxvQkFBb0IsVUFBVSxjQUFjO0FBQzVDO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxHQUFHO0FBQ0g7QUFDQTtBQUNBLEdBQUc7QUFDSDtBQUNBO0FBQ0EsR0FBRztBQUNIO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxlQUFlO0FBQ2Y7QUFDQTtBQUNBO0FBQ0E7QUFDQSxlQUFlO0FBQ2Y7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxTQUFTO0FBQ1Q7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsU0FBUztBQUNUO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL3htbC5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKipcbiAqIEBwYXJhbSB7c3RyaW5nfSB2YWx1ZVxuICogQHJldHVybnMge1JlZ0V4cH1cbiAqICovXG5cbi8qKlxuICogQHBhcmFtIHtSZWdFeHAgfCBzdHJpbmcgfSByZVxuICogQHJldHVybnMge3N0cmluZ31cbiAqL1xuZnVuY3Rpb24gc291cmNlKHJlKSB7XG4gIGlmICghcmUpIHJldHVybiBudWxsO1xuICBpZiAodHlwZW9mIHJlID09PSBcInN0cmluZ1wiKSByZXR1cm4gcmU7XG5cbiAgcmV0dXJuIHJlLnNvdXJjZTtcbn1cblxuLyoqXG4gKiBAcGFyYW0ge1JlZ0V4cCB8IHN0cmluZyB9IHJlXG4gKiBAcmV0dXJucyB7c3RyaW5nfVxuICovXG5mdW5jdGlvbiBsb29rYWhlYWQocmUpIHtcbiAgcmV0dXJuIGNvbmNhdCgnKD89JywgcmUsICcpJyk7XG59XG5cbi8qKlxuICogQHBhcmFtIHtSZWdFeHAgfCBzdHJpbmcgfSByZVxuICogQHJldHVybnMge3N0cmluZ31cbiAqL1xuZnVuY3Rpb24gb3B0aW9uYWwocmUpIHtcbiAgcmV0dXJuIGNvbmNhdCgnKCcsIHJlLCAnKT8nKTtcbn1cblxuLyoqXG4gKiBAcGFyYW0gey4uLihSZWdFeHAgfCBzdHJpbmcpIH0gYXJnc1xuICogQHJldHVybnMge3N0cmluZ31cbiAqL1xuZnVuY3Rpb24gY29uY2F0KC4uLmFyZ3MpIHtcbiAgY29uc3Qgam9pbmVkID0gYXJncy5tYXAoKHgpID0+IHNvdXJjZSh4KSkuam9pbihcIlwiKTtcbiAgcmV0dXJuIGpvaW5lZDtcbn1cblxuLyoqXG4gKiBBbnkgb2YgdGhlIHBhc3NlZCBleHByZXNzc2lvbnMgbWF5IG1hdGNoXG4gKlxuICogQ3JlYXRlcyBhIGh1Z2UgdGhpcyB8IHRoaXMgfCB0aGF0IHwgdGhhdCBtYXRjaFxuICogQHBhcmFtIHsoUmVnRXhwIHwgc3RyaW5nKVtdIH0gYXJnc1xuICogQHJldHVybnMge3N0cmluZ31cbiAqL1xuZnVuY3Rpb24gZWl0aGVyKC4uLmFyZ3MpIHtcbiAgY29uc3Qgam9pbmVkID0gJygnICsgYXJncy5tYXAoKHgpID0+IHNvdXJjZSh4KSkuam9pbihcInxcIikgKyBcIilcIjtcbiAgcmV0dXJuIGpvaW5lZDtcbn1cblxuLypcbkxhbmd1YWdlOiBIVE1MLCBYTUxcbldlYnNpdGU6IGh0dHBzOi8vd3d3LnczLm9yZy9YTUwvXG5DYXRlZ29yeTogY29tbW9uXG5BdWRpdDogMjAyMFxuKi9cblxuLyoqIEB0eXBlIExhbmd1YWdlRm4gKi9cbmZ1bmN0aW9uIHhtbChobGpzKSB7XG4gIC8vIEVsZW1lbnQgbmFtZXMgY2FuIGNvbnRhaW4gbGV0dGVycywgZGlnaXRzLCBoeXBoZW5zLCB1bmRlcnNjb3JlcywgYW5kIHBlcmlvZHNcbiAgY29uc3QgVEFHX05BTUVfUkUgPSBjb25jYXQoL1tBLVpfXS8sIG9wdGlvbmFsKC9bQS1aMC05Xy4tXSo6LyksIC9bQS1aMC05Xy4tXSovKTtcbiAgY29uc3QgWE1MX0lERU5UX1JFID0gL1tBLVphLXowLTkuXzotXSsvO1xuICBjb25zdCBYTUxfRU5USVRJRVMgPSB7XG4gICAgY2xhc3NOYW1lOiAnc3ltYm9sJyxcbiAgICBiZWdpbjogLyZbYS16XSs7fCYjWzAtOV0rO3wmI3hbYS1mMC05XSs7L1xuICB9O1xuICBjb25zdCBYTUxfTUVUQV9LRVlXT1JEUyA9IHtcbiAgICBiZWdpbjogL1xccy8sXG4gICAgY29udGFpbnM6IFtcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnbWV0YS1rZXl3b3JkJyxcbiAgICAgICAgYmVnaW46IC8jP1thLXpfXVthLXoxLTlfLV0rLyxcbiAgICAgICAgaWxsZWdhbDogL1xcbi9cbiAgICAgIH1cbiAgICBdXG4gIH07XG4gIGNvbnN0IFhNTF9NRVRBX1BBUl9LRVlXT1JEUyA9IGhsanMuaW5oZXJpdChYTUxfTUVUQV9LRVlXT1JEUywge1xuICAgIGJlZ2luOiAvXFwoLyxcbiAgICBlbmQ6IC9cXCkvXG4gIH0pO1xuICBjb25zdCBBUE9TX01FVEFfU1RSSU5HX01PREUgPSBobGpzLmluaGVyaXQoaGxqcy5BUE9TX1NUUklOR19NT0RFLCB7XG4gICAgY2xhc3NOYW1lOiAnbWV0YS1zdHJpbmcnXG4gIH0pO1xuICBjb25zdCBRVU9URV9NRVRBX1NUUklOR19NT0RFID0gaGxqcy5pbmhlcml0KGhsanMuUVVPVEVfU1RSSU5HX01PREUsIHtcbiAgICBjbGFzc05hbWU6ICdtZXRhLXN0cmluZydcbiAgfSk7XG4gIGNvbnN0IFRBR19JTlRFUk5BTFMgPSB7XG4gICAgZW5kc1dpdGhQYXJlbnQ6IHRydWUsXG4gICAgaWxsZWdhbDogLzwvLFxuICAgIHJlbGV2YW5jZTogMCxcbiAgICBjb250YWluczogW1xuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdhdHRyJyxcbiAgICAgICAgYmVnaW46IFhNTF9JREVOVF9SRSxcbiAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogLz1cXHMqLyxcbiAgICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIGNsYXNzTmFtZTogJ3N0cmluZycsXG4gICAgICAgICAgICBlbmRzUGFyZW50OiB0cnVlLFxuICAgICAgICAgICAgdmFyaWFudHM6IFtcbiAgICAgICAgICAgICAge1xuICAgICAgICAgICAgICAgIGJlZ2luOiAvXCIvLFxuICAgICAgICAgICAgICAgIGVuZDogL1wiLyxcbiAgICAgICAgICAgICAgICBjb250YWluczogWyBYTUxfRU5USVRJRVMgXVxuICAgICAgICAgICAgICB9LFxuICAgICAgICAgICAgICB7XG4gICAgICAgICAgICAgICAgYmVnaW46IC8nLyxcbiAgICAgICAgICAgICAgICBlbmQ6IC8nLyxcbiAgICAgICAgICAgICAgICBjb250YWluczogWyBYTUxfRU5USVRJRVMgXVxuICAgICAgICAgICAgICB9LFxuICAgICAgICAgICAgICB7XG4gICAgICAgICAgICAgICAgYmVnaW46IC9bXlxcc1wiJz08PmBdKy9cbiAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgXVxuICAgICAgICAgIH1cbiAgICAgICAgXVxuICAgICAgfVxuICAgIF1cbiAgfTtcbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnSFRNTCwgWE1MJyxcbiAgICBhbGlhc2VzOiBbXG4gICAgICAnaHRtbCcsXG4gICAgICAneGh0bWwnLFxuICAgICAgJ3JzcycsXG4gICAgICAnYXRvbScsXG4gICAgICAneGpiJyxcbiAgICAgICd4c2QnLFxuICAgICAgJ3hzbCcsXG4gICAgICAncGxpc3QnLFxuICAgICAgJ3dzZicsXG4gICAgICAnc3ZnJ1xuICAgIF0sXG4gICAgY2FzZV9pbnNlbnNpdGl2ZTogdHJ1ZSxcbiAgICBjb250YWluczogW1xuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdtZXRhJyxcbiAgICAgICAgYmVnaW46IC88IVthLXpdLyxcbiAgICAgICAgZW5kOiAvPi8sXG4gICAgICAgIHJlbGV2YW5jZTogMTAsXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgWE1MX01FVEFfS0VZV09SRFMsXG4gICAgICAgICAgUVVPVEVfTUVUQV9TVFJJTkdfTU9ERSxcbiAgICAgICAgICBBUE9TX01FVEFfU1RSSU5HX01PREUsXG4gICAgICAgICAgWE1MX01FVEFfUEFSX0tFWVdPUkRTLFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiAvXFxbLyxcbiAgICAgICAgICAgIGVuZDogL1xcXS8sXG4gICAgICAgICAgICBjb250YWluczogW1xuICAgICAgICAgICAgICB7XG4gICAgICAgICAgICAgICAgY2xhc3NOYW1lOiAnbWV0YScsXG4gICAgICAgICAgICAgICAgYmVnaW46IC88IVthLXpdLyxcbiAgICAgICAgICAgICAgICBlbmQ6IC8+LyxcbiAgICAgICAgICAgICAgICBjb250YWluczogW1xuICAgICAgICAgICAgICAgICAgWE1MX01FVEFfS0VZV09SRFMsXG4gICAgICAgICAgICAgICAgICBYTUxfTUVUQV9QQVJfS0VZV09SRFMsXG4gICAgICAgICAgICAgICAgICBRVU9URV9NRVRBX1NUUklOR19NT0RFLFxuICAgICAgICAgICAgICAgICAgQVBPU19NRVRBX1NUUklOR19NT0RFXG4gICAgICAgICAgICAgICAgXVxuICAgICAgICAgICAgICB9XG4gICAgICAgICAgICBdXG4gICAgICAgICAgfVxuICAgICAgICBdXG4gICAgICB9LFxuICAgICAgaGxqcy5DT01NRU5UKFxuICAgICAgICAvPCEtLS8sXG4gICAgICAgIC8tLT4vLFxuICAgICAgICB7XG4gICAgICAgICAgcmVsZXZhbmNlOiAxMFxuICAgICAgICB9XG4gICAgICApLFxuICAgICAge1xuICAgICAgICBiZWdpbjogLzwhXFxbQ0RBVEFcXFsvLFxuICAgICAgICBlbmQ6IC9cXF1cXF0+LyxcbiAgICAgICAgcmVsZXZhbmNlOiAxMFxuICAgICAgfSxcbiAgICAgIFhNTF9FTlRJVElFUyxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnbWV0YScsXG4gICAgICAgIGJlZ2luOiAvPFxcP3htbC8sXG4gICAgICAgIGVuZDogL1xcPz4vLFxuICAgICAgICByZWxldmFuY2U6IDEwXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICd0YWcnLFxuICAgICAgICAvKlxuICAgICAgICBUaGUgbG9va2FoZWFkIHBhdHRlcm4gKD89Li4uKSBlbnN1cmVzIHRoYXQgJ2JlZ2luJyBvbmx5IG1hdGNoZXNcbiAgICAgICAgJzxzdHlsZScgYXMgYSBzaW5nbGUgd29yZCwgZm9sbG93ZWQgYnkgYSB3aGl0ZXNwYWNlIG9yIGFuXG4gICAgICAgIGVuZGluZyBicmFrZXQuIFRoZSAnJCcgaXMgbmVlZGVkIGZvciB0aGUgbGV4ZW1lIHRvIGJlIHJlY29nbml6ZWRcbiAgICAgICAgYnkgaGxqcy5zdWJNb2RlKCkgdGhhdCB0ZXN0cyBsZXhlbWVzIG91dHNpZGUgdGhlIHN0cmVhbS5cbiAgICAgICAgKi9cbiAgICAgICAgYmVnaW46IC88c3R5bGUoPz1cXHN8PikvLFxuICAgICAgICBlbmQ6IC8+LyxcbiAgICAgICAga2V5d29yZHM6IHtcbiAgICAgICAgICBuYW1lOiAnc3R5bGUnXG4gICAgICAgIH0sXG4gICAgICAgIGNvbnRhaW5zOiBbIFRBR19JTlRFUk5BTFMgXSxcbiAgICAgICAgc3RhcnRzOiB7XG4gICAgICAgICAgZW5kOiAvPFxcL3N0eWxlPi8sXG4gICAgICAgICAgcmV0dXJuRW5kOiB0cnVlLFxuICAgICAgICAgIHN1Ykxhbmd1YWdlOiBbXG4gICAgICAgICAgICAnY3NzJyxcbiAgICAgICAgICAgICd4bWwnXG4gICAgICAgICAgXVxuICAgICAgICB9XG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICd0YWcnLFxuICAgICAgICAvLyBTZWUgdGhlIGNvbW1lbnQgaW4gdGhlIDxzdHlsZSB0YWcgYWJvdXQgdGhlIGxvb2thaGVhZCBwYXR0ZXJuXG4gICAgICAgIGJlZ2luOiAvPHNjcmlwdCg/PVxcc3w+KS8sXG4gICAgICAgIGVuZDogLz4vLFxuICAgICAgICBrZXl3b3Jkczoge1xuICAgICAgICAgIG5hbWU6ICdzY3JpcHQnXG4gICAgICAgIH0sXG4gICAgICAgIGNvbnRhaW5zOiBbIFRBR19JTlRFUk5BTFMgXSxcbiAgICAgICAgc3RhcnRzOiB7XG4gICAgICAgICAgZW5kOiAvPFxcL3NjcmlwdD4vLFxuICAgICAgICAgIHJldHVybkVuZDogdHJ1ZSxcbiAgICAgICAgICBzdWJMYW5ndWFnZTogW1xuICAgICAgICAgICAgJ2phdmFzY3JpcHQnLFxuICAgICAgICAgICAgJ2hhbmRsZWJhcnMnLFxuICAgICAgICAgICAgJ3htbCdcbiAgICAgICAgICBdXG4gICAgICAgIH1cbiAgICAgIH0sXG4gICAgICAvLyB3ZSBuZWVkIHRoaXMgZm9yIG5vdyBmb3IgalNYXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3RhZycsXG4gICAgICAgIGJlZ2luOiAvPD58PFxcLz4vXG4gICAgICB9LFxuICAgICAgLy8gb3BlbiB0YWdcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAndGFnJyxcbiAgICAgICAgYmVnaW46IGNvbmNhdChcbiAgICAgICAgICAvPC8sXG4gICAgICAgICAgbG9va2FoZWFkKGNvbmNhdChcbiAgICAgICAgICAgIFRBR19OQU1FX1JFLFxuICAgICAgICAgICAgLy8gPHRhZy8+XG4gICAgICAgICAgICAvLyA8dGFnPlxuICAgICAgICAgICAgLy8gPHRhZyAuLi5cbiAgICAgICAgICAgIGVpdGhlcigvXFwvPi8sIC8+LywgL1xccy8pXG4gICAgICAgICAgKSlcbiAgICAgICAgKSxcbiAgICAgICAgZW5kOiAvXFwvPz4vLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIGNsYXNzTmFtZTogJ25hbWUnLFxuICAgICAgICAgICAgYmVnaW46IFRBR19OQU1FX1JFLFxuICAgICAgICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgICAgICAgc3RhcnRzOiBUQUdfSU5URVJOQUxTXG4gICAgICAgICAgfVxuICAgICAgICBdXG4gICAgICB9LFxuICAgICAgLy8gY2xvc2UgdGFnXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3RhZycsXG4gICAgICAgIGJlZ2luOiBjb25jYXQoXG4gICAgICAgICAgLzxcXC8vLFxuICAgICAgICAgIGxvb2thaGVhZChjb25jYXQoXG4gICAgICAgICAgICBUQUdfTkFNRV9SRSwgLz4vXG4gICAgICAgICAgKSlcbiAgICAgICAgKSxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBjbGFzc05hbWU6ICduYW1lJyxcbiAgICAgICAgICAgIGJlZ2luOiBUQUdfTkFNRV9SRSxcbiAgICAgICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgYmVnaW46IC8+LyxcbiAgICAgICAgICAgIHJlbGV2YW5jZTogMCxcbiAgICAgICAgICAgIGVuZHNQYXJlbnQ6IHRydWVcbiAgICAgICAgICB9XG4gICAgICAgIF1cbiAgICAgIH1cbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0geG1sO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9