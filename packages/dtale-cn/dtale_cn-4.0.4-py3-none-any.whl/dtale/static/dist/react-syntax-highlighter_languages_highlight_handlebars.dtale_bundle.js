(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_handlebars"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/handlebars.js":
/*!*****************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/handlebars.js ***!
  \*****************************************************************************************************/
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
function anyNumberOfTimes(re) {
  return concat('(', re, ')*');
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
Language: Handlebars
Requires: xml.js
Author: Robin Ward <robin.ward@gmail.com>
Description: Matcher for Handlebars as well as EmberJS additions.
Website: https://handlebarsjs.com
Category: template
*/

function handlebars(hljs) {
  const BUILT_INS = {
    'builtin-name': [
      'action',
      'bindattr',
      'collection',
      'component',
      'concat',
      'debugger',
      'each',
      'each-in',
      'get',
      'hash',
      'if',
      'in',
      'input',
      'link-to',
      'loc',
      'log',
      'lookup',
      'mut',
      'outlet',
      'partial',
      'query-params',
      'render',
      'template',
      'textarea',
      'unbound',
      'unless',
      'view',
      'with',
      'yield'
    ]
  };

  const LITERALS = {
    literal: [
      'true',
      'false',
      'undefined',
      'null'
    ]
  };

  // as defined in https://handlebarsjs.com/guide/expressions.html#literal-segments
  // this regex matches literal segments like ' abc ' or [ abc ] as well as helpers and paths
  // like a/b, ./abc/cde, and abc.bcd

  const DOUBLE_QUOTED_ID_REGEX = /""|"[^"]+"/;
  const SINGLE_QUOTED_ID_REGEX = /''|'[^']+'/;
  const BRACKET_QUOTED_ID_REGEX = /\[\]|\[[^\]]+\]/;
  const PLAIN_ID_REGEX = /[^\s!"#%&'()*+,.\/;<=>@\[\\\]^`{|}~]+/;
  const PATH_DELIMITER_REGEX = /(\.|\/)/;
  const ANY_ID = either(
    DOUBLE_QUOTED_ID_REGEX,
    SINGLE_QUOTED_ID_REGEX,
    BRACKET_QUOTED_ID_REGEX,
    PLAIN_ID_REGEX
    );

  const IDENTIFIER_REGEX = concat(
    optional(/\.|\.\/|\//), // relative or absolute path
    ANY_ID,
    anyNumberOfTimes(concat(
      PATH_DELIMITER_REGEX,
      ANY_ID
    ))
  );

  // identifier followed by a equal-sign (without the equal sign)
  const HASH_PARAM_REGEX = concat(
    '(',
    BRACKET_QUOTED_ID_REGEX, '|',
    PLAIN_ID_REGEX,
    ')(?==)'
  );

  const HELPER_NAME_OR_PATH_EXPRESSION = {
    begin: IDENTIFIER_REGEX,
    lexemes: /[\w.\/]+/
  };

  const HELPER_PARAMETER = hljs.inherit(HELPER_NAME_OR_PATH_EXPRESSION, {
    keywords: LITERALS
  });

  const SUB_EXPRESSION = {
    begin: /\(/,
    end: /\)/
    // the "contains" is added below when all necessary sub-modes are defined
  };

  const HASH = {
    // fka "attribute-assignment", parameters of the form 'key=value'
    className: 'attr',
    begin: HASH_PARAM_REGEX,
    relevance: 0,
    starts: {
      begin: /=/,
      end: /=/,
      starts: {
        contains: [
          hljs.NUMBER_MODE,
          hljs.QUOTE_STRING_MODE,
          hljs.APOS_STRING_MODE,
          HELPER_PARAMETER,
          SUB_EXPRESSION
        ]
      }
    }
  };

  const BLOCK_PARAMS = {
    // parameters of the form '{{#with x as | y |}}...{{/with}}'
    begin: /as\s+\|/,
    keywords: {
      keyword: 'as'
    },
    end: /\|/,
    contains: [
      {
        // define sub-mode in order to prevent highlighting of block-parameter named "as"
        begin: /\w+/
      }
    ]
  };

  const HELPER_PARAMETERS = {
    contains: [
      hljs.NUMBER_MODE,
      hljs.QUOTE_STRING_MODE,
      hljs.APOS_STRING_MODE,
      BLOCK_PARAMS,
      HASH,
      HELPER_PARAMETER,
      SUB_EXPRESSION
    ],
    returnEnd: true
    // the property "end" is defined through inheritance when the mode is used. If depends
    // on the surrounding mode, but "endsWithParent" does not work here (i.e. it includes the
    // end-token of the surrounding mode)
  };

  const SUB_EXPRESSION_CONTENTS = hljs.inherit(HELPER_NAME_OR_PATH_EXPRESSION, {
    className: 'name',
    keywords: BUILT_INS,
    starts: hljs.inherit(HELPER_PARAMETERS, {
      end: /\)/
    })
  });

  SUB_EXPRESSION.contains = [SUB_EXPRESSION_CONTENTS];

  const OPENING_BLOCK_MUSTACHE_CONTENTS = hljs.inherit(HELPER_NAME_OR_PATH_EXPRESSION, {
    keywords: BUILT_INS,
    className: 'name',
    starts: hljs.inherit(HELPER_PARAMETERS, {
      end: /\}\}/
    })
  });

  const CLOSING_BLOCK_MUSTACHE_CONTENTS = hljs.inherit(HELPER_NAME_OR_PATH_EXPRESSION, {
    keywords: BUILT_INS,
    className: 'name'
  });

  const BASIC_MUSTACHE_CONTENTS = hljs.inherit(HELPER_NAME_OR_PATH_EXPRESSION, {
    className: 'name',
    keywords: BUILT_INS,
    starts: hljs.inherit(HELPER_PARAMETERS, {
      end: /\}\}/
    })
  });

  const ESCAPE_MUSTACHE_WITH_PRECEEDING_BACKSLASH = {
    begin: /\\\{\{/,
    skip: true
  };
  const PREVENT_ESCAPE_WITH_ANOTHER_PRECEEDING_BACKSLASH = {
    begin: /\\\\(?=\{\{)/,
    skip: true
  };

  return {
    name: 'Handlebars',
    aliases: [
      'hbs',
      'html.hbs',
      'html.handlebars',
      'htmlbars'
    ],
    case_insensitive: true,
    subLanguage: 'xml',
    contains: [
      ESCAPE_MUSTACHE_WITH_PRECEEDING_BACKSLASH,
      PREVENT_ESCAPE_WITH_ANOTHER_PRECEEDING_BACKSLASH,
      hljs.COMMENT(/\{\{!--/, /--\}\}/),
      hljs.COMMENT(/\{\{!/, /\}\}/),
      {
        // open raw block "{{{{raw}}}} content not evaluated {{{{/raw}}}}"
        className: 'template-tag',
        begin: /\{\{\{\{(?!\/)/,
        end: /\}\}\}\}/,
        contains: [OPENING_BLOCK_MUSTACHE_CONTENTS],
        starts: {
          end: /\{\{\{\{\//,
          returnEnd: true,
          subLanguage: 'xml'
        }
      },
      {
        // close raw block
        className: 'template-tag',
        begin: /\{\{\{\{\//,
        end: /\}\}\}\}/,
        contains: [CLOSING_BLOCK_MUSTACHE_CONTENTS]
      },
      {
        // open block statement
        className: 'template-tag',
        begin: /\{\{#/,
        end: /\}\}/,
        contains: [OPENING_BLOCK_MUSTACHE_CONTENTS]
      },
      {
        className: 'template-tag',
        begin: /\{\{(?=else\}\})/,
        end: /\}\}/,
        keywords: 'else'
      },
      {
        className: 'template-tag',
        begin: /\{\{(?=else if)/,
        end: /\}\}/,
        keywords: 'else if'
      },
      {
        // closing block statement
        className: 'template-tag',
        begin: /\{\{\//,
        end: /\}\}/,
        contains: [CLOSING_BLOCK_MUSTACHE_CONTENTS]
      },
      {
        // template variable or helper-call that is NOT html-escaped
        className: 'template-variable',
        begin: /\{\{\{/,
        end: /\}\}\}/,
        contains: [BASIC_MUSTACHE_CONTENTS]
      },
      {
        // template variable or helper-call that is html-escaped
        className: 'template-variable',
        begin: /\{\{/,
        end: /\}\}/,
        contains: [BASIC_MUSTACHE_CONTENTS]
      }
    ]
  };
}

module.exports = handlebars;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfaGFuZGxlYmFycy5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBLFdBQVcsUUFBUTtBQUNuQixhQUFhO0FBQ2I7O0FBRUE7QUFDQSxXQUFXLGtCQUFrQjtBQUM3QixhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTs7QUFFQTtBQUNBLFdBQVcsa0JBQWtCO0FBQzdCLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBLFdBQVcsa0JBQWtCO0FBQzdCLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBLFdBQVcsdUJBQXVCO0FBQ2xDLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsV0FBVyxzQkFBc0I7QUFDakMsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQSw2Q0FBNkMsYUFBYSxFQUFFO0FBQzVEO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBLEdBQUc7O0FBRUg7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBLGlDQUFpQyxrQkFBa0IsS0FBSyxPQUFPO0FBQy9EO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMLEdBQUc7O0FBRUg7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQSxjQUFjLEVBQUU7QUFDaEIsS0FBSztBQUNMLEdBQUc7O0FBRUg7QUFDQTtBQUNBO0FBQ0EsR0FBRzs7QUFFSDtBQUNBO0FBQ0E7QUFDQTtBQUNBLGNBQWMsRUFBRTtBQUNoQixLQUFLO0FBQ0wsR0FBRzs7QUFFSDtBQUNBLGdCQUFnQixFQUFFO0FBQ2xCO0FBQ0E7QUFDQTtBQUNBLHFCQUFxQixFQUFFO0FBQ3ZCO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxzQkFBc0IsRUFBRSxXQUFXLEVBQUU7QUFDckMsc0JBQXNCLEVBQUUsT0FBTyxFQUFFO0FBQ2pDO0FBQ0EsK0JBQStCLFFBQVEsMEJBQTBCLFFBQVE7QUFDekU7QUFDQSxrQkFBa0IsRUFBRSxFQUFFLEVBQUU7QUFDeEIsZ0JBQWdCLEVBQUUsRUFBRSxFQUFFO0FBQ3RCO0FBQ0E7QUFDQSxrQkFBa0IsRUFBRSxFQUFFLEVBQUU7QUFDeEI7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLGtCQUFrQixFQUFFLEVBQUUsRUFBRTtBQUN4QixnQkFBZ0IsRUFBRSxFQUFFLEVBQUU7QUFDdEI7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0Esa0JBQWtCLEVBQUU7QUFDcEIsZ0JBQWdCLEVBQUU7QUFDbEI7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBLGtCQUFrQixFQUFFLFNBQVMsRUFBRTtBQUMvQixnQkFBZ0IsRUFBRTtBQUNsQjtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0Esa0JBQWtCLEVBQUU7QUFDcEIsZ0JBQWdCLEVBQUU7QUFDbEI7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0Esa0JBQWtCLEVBQUU7QUFDcEIsZ0JBQWdCLEVBQUU7QUFDbEI7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0Esa0JBQWtCLEVBQUUsRUFBRTtBQUN0QixnQkFBZ0IsRUFBRSxFQUFFO0FBQ3BCO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLGtCQUFrQixFQUFFO0FBQ3BCLGdCQUFnQixFQUFFO0FBQ2xCO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL2hhbmRsZWJhcnMuanMiXSwic291cmNlc0NvbnRlbnQiOlsiLyoqXG4gKiBAcGFyYW0ge3N0cmluZ30gdmFsdWVcbiAqIEByZXR1cm5zIHtSZWdFeHB9XG4gKiAqL1xuXG4vKipcbiAqIEBwYXJhbSB7UmVnRXhwIHwgc3RyaW5nIH0gcmVcbiAqIEByZXR1cm5zIHtzdHJpbmd9XG4gKi9cbmZ1bmN0aW9uIHNvdXJjZShyZSkge1xuICBpZiAoIXJlKSByZXR1cm4gbnVsbDtcbiAgaWYgKHR5cGVvZiByZSA9PT0gXCJzdHJpbmdcIikgcmV0dXJuIHJlO1xuXG4gIHJldHVybiByZS5zb3VyY2U7XG59XG5cbi8qKlxuICogQHBhcmFtIHtSZWdFeHAgfCBzdHJpbmcgfSByZVxuICogQHJldHVybnMge3N0cmluZ31cbiAqL1xuZnVuY3Rpb24gYW55TnVtYmVyT2ZUaW1lcyhyZSkge1xuICByZXR1cm4gY29uY2F0KCcoJywgcmUsICcpKicpO1xufVxuXG4vKipcbiAqIEBwYXJhbSB7UmVnRXhwIHwgc3RyaW5nIH0gcmVcbiAqIEByZXR1cm5zIHtzdHJpbmd9XG4gKi9cbmZ1bmN0aW9uIG9wdGlvbmFsKHJlKSB7XG4gIHJldHVybiBjb25jYXQoJygnLCByZSwgJyk/Jyk7XG59XG5cbi8qKlxuICogQHBhcmFtIHsuLi4oUmVnRXhwIHwgc3RyaW5nKSB9IGFyZ3NcbiAqIEByZXR1cm5zIHtzdHJpbmd9XG4gKi9cbmZ1bmN0aW9uIGNvbmNhdCguLi5hcmdzKSB7XG4gIGNvbnN0IGpvaW5lZCA9IGFyZ3MubWFwKCh4KSA9PiBzb3VyY2UoeCkpLmpvaW4oXCJcIik7XG4gIHJldHVybiBqb2luZWQ7XG59XG5cbi8qKlxuICogQW55IG9mIHRoZSBwYXNzZWQgZXhwcmVzc3Npb25zIG1heSBtYXRjaFxuICpcbiAqIENyZWF0ZXMgYSBodWdlIHRoaXMgfCB0aGlzIHwgdGhhdCB8IHRoYXQgbWF0Y2hcbiAqIEBwYXJhbSB7KFJlZ0V4cCB8IHN0cmluZylbXSB9IGFyZ3NcbiAqIEByZXR1cm5zIHtzdHJpbmd9XG4gKi9cbmZ1bmN0aW9uIGVpdGhlciguLi5hcmdzKSB7XG4gIGNvbnN0IGpvaW5lZCA9ICcoJyArIGFyZ3MubWFwKCh4KSA9PiBzb3VyY2UoeCkpLmpvaW4oXCJ8XCIpICsgXCIpXCI7XG4gIHJldHVybiBqb2luZWQ7XG59XG5cbi8qXG5MYW5ndWFnZTogSGFuZGxlYmFyc1xuUmVxdWlyZXM6IHhtbC5qc1xuQXV0aG9yOiBSb2JpbiBXYXJkIDxyb2Jpbi53YXJkQGdtYWlsLmNvbT5cbkRlc2NyaXB0aW9uOiBNYXRjaGVyIGZvciBIYW5kbGViYXJzIGFzIHdlbGwgYXMgRW1iZXJKUyBhZGRpdGlvbnMuXG5XZWJzaXRlOiBodHRwczovL2hhbmRsZWJhcnNqcy5jb21cbkNhdGVnb3J5OiB0ZW1wbGF0ZVxuKi9cblxuZnVuY3Rpb24gaGFuZGxlYmFycyhobGpzKSB7XG4gIGNvbnN0IEJVSUxUX0lOUyA9IHtcbiAgICAnYnVpbHRpbi1uYW1lJzogW1xuICAgICAgJ2FjdGlvbicsXG4gICAgICAnYmluZGF0dHInLFxuICAgICAgJ2NvbGxlY3Rpb24nLFxuICAgICAgJ2NvbXBvbmVudCcsXG4gICAgICAnY29uY2F0JyxcbiAgICAgICdkZWJ1Z2dlcicsXG4gICAgICAnZWFjaCcsXG4gICAgICAnZWFjaC1pbicsXG4gICAgICAnZ2V0JyxcbiAgICAgICdoYXNoJyxcbiAgICAgICdpZicsXG4gICAgICAnaW4nLFxuICAgICAgJ2lucHV0JyxcbiAgICAgICdsaW5rLXRvJyxcbiAgICAgICdsb2MnLFxuICAgICAgJ2xvZycsXG4gICAgICAnbG9va3VwJyxcbiAgICAgICdtdXQnLFxuICAgICAgJ291dGxldCcsXG4gICAgICAncGFydGlhbCcsXG4gICAgICAncXVlcnktcGFyYW1zJyxcbiAgICAgICdyZW5kZXInLFxuICAgICAgJ3RlbXBsYXRlJyxcbiAgICAgICd0ZXh0YXJlYScsXG4gICAgICAndW5ib3VuZCcsXG4gICAgICAndW5sZXNzJyxcbiAgICAgICd2aWV3JyxcbiAgICAgICd3aXRoJyxcbiAgICAgICd5aWVsZCdcbiAgICBdXG4gIH07XG5cbiAgY29uc3QgTElURVJBTFMgPSB7XG4gICAgbGl0ZXJhbDogW1xuICAgICAgJ3RydWUnLFxuICAgICAgJ2ZhbHNlJyxcbiAgICAgICd1bmRlZmluZWQnLFxuICAgICAgJ251bGwnXG4gICAgXVxuICB9O1xuXG4gIC8vIGFzIGRlZmluZWQgaW4gaHR0cHM6Ly9oYW5kbGViYXJzanMuY29tL2d1aWRlL2V4cHJlc3Npb25zLmh0bWwjbGl0ZXJhbC1zZWdtZW50c1xuICAvLyB0aGlzIHJlZ2V4IG1hdGNoZXMgbGl0ZXJhbCBzZWdtZW50cyBsaWtlICcgYWJjICcgb3IgWyBhYmMgXSBhcyB3ZWxsIGFzIGhlbHBlcnMgYW5kIHBhdGhzXG4gIC8vIGxpa2UgYS9iLCAuL2FiYy9jZGUsIGFuZCBhYmMuYmNkXG5cbiAgY29uc3QgRE9VQkxFX1FVT1RFRF9JRF9SRUdFWCA9IC9cIlwifFwiW15cIl0rXCIvO1xuICBjb25zdCBTSU5HTEVfUVVPVEVEX0lEX1JFR0VYID0gLycnfCdbXiddKycvO1xuICBjb25zdCBCUkFDS0VUX1FVT1RFRF9JRF9SRUdFWCA9IC9cXFtcXF18XFxbW15cXF1dK1xcXS87XG4gIGNvbnN0IFBMQUlOX0lEX1JFR0VYID0gL1teXFxzIVwiIyUmJygpKissLlxcLzs8PT5AXFxbXFxcXFxcXV5ge3x9fl0rLztcbiAgY29uc3QgUEFUSF9ERUxJTUlURVJfUkVHRVggPSAvKFxcLnxcXC8pLztcbiAgY29uc3QgQU5ZX0lEID0gZWl0aGVyKFxuICAgIERPVUJMRV9RVU9URURfSURfUkVHRVgsXG4gICAgU0lOR0xFX1FVT1RFRF9JRF9SRUdFWCxcbiAgICBCUkFDS0VUX1FVT1RFRF9JRF9SRUdFWCxcbiAgICBQTEFJTl9JRF9SRUdFWFxuICAgICk7XG5cbiAgY29uc3QgSURFTlRJRklFUl9SRUdFWCA9IGNvbmNhdChcbiAgICBvcHRpb25hbCgvXFwufFxcLlxcL3xcXC8vKSwgLy8gcmVsYXRpdmUgb3IgYWJzb2x1dGUgcGF0aFxuICAgIEFOWV9JRCxcbiAgICBhbnlOdW1iZXJPZlRpbWVzKGNvbmNhdChcbiAgICAgIFBBVEhfREVMSU1JVEVSX1JFR0VYLFxuICAgICAgQU5ZX0lEXG4gICAgKSlcbiAgKTtcblxuICAvLyBpZGVudGlmaWVyIGZvbGxvd2VkIGJ5IGEgZXF1YWwtc2lnbiAod2l0aG91dCB0aGUgZXF1YWwgc2lnbilcbiAgY29uc3QgSEFTSF9QQVJBTV9SRUdFWCA9IGNvbmNhdChcbiAgICAnKCcsXG4gICAgQlJBQ0tFVF9RVU9URURfSURfUkVHRVgsICd8JyxcbiAgICBQTEFJTl9JRF9SRUdFWCxcbiAgICAnKSg/PT0pJ1xuICApO1xuXG4gIGNvbnN0IEhFTFBFUl9OQU1FX09SX1BBVEhfRVhQUkVTU0lPTiA9IHtcbiAgICBiZWdpbjogSURFTlRJRklFUl9SRUdFWCxcbiAgICBsZXhlbWVzOiAvW1xcdy5cXC9dKy9cbiAgfTtcblxuICBjb25zdCBIRUxQRVJfUEFSQU1FVEVSID0gaGxqcy5pbmhlcml0KEhFTFBFUl9OQU1FX09SX1BBVEhfRVhQUkVTU0lPTiwge1xuICAgIGtleXdvcmRzOiBMSVRFUkFMU1xuICB9KTtcblxuICBjb25zdCBTVUJfRVhQUkVTU0lPTiA9IHtcbiAgICBiZWdpbjogL1xcKC8sXG4gICAgZW5kOiAvXFwpL1xuICAgIC8vIHRoZSBcImNvbnRhaW5zXCIgaXMgYWRkZWQgYmVsb3cgd2hlbiBhbGwgbmVjZXNzYXJ5IHN1Yi1tb2RlcyBhcmUgZGVmaW5lZFxuICB9O1xuXG4gIGNvbnN0IEhBU0ggPSB7XG4gICAgLy8gZmthIFwiYXR0cmlidXRlLWFzc2lnbm1lbnRcIiwgcGFyYW1ldGVycyBvZiB0aGUgZm9ybSAna2V5PXZhbHVlJ1xuICAgIGNsYXNzTmFtZTogJ2F0dHInLFxuICAgIGJlZ2luOiBIQVNIX1BBUkFNX1JFR0VYLFxuICAgIHJlbGV2YW5jZTogMCxcbiAgICBzdGFydHM6IHtcbiAgICAgIGJlZ2luOiAvPS8sXG4gICAgICBlbmQ6IC89LyxcbiAgICAgIHN0YXJ0czoge1xuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIGhsanMuTlVNQkVSX01PREUsXG4gICAgICAgICAgaGxqcy5RVU9URV9TVFJJTkdfTU9ERSxcbiAgICAgICAgICBobGpzLkFQT1NfU1RSSU5HX01PREUsXG4gICAgICAgICAgSEVMUEVSX1BBUkFNRVRFUixcbiAgICAgICAgICBTVUJfRVhQUkVTU0lPTlxuICAgICAgICBdXG4gICAgICB9XG4gICAgfVxuICB9O1xuXG4gIGNvbnN0IEJMT0NLX1BBUkFNUyA9IHtcbiAgICAvLyBwYXJhbWV0ZXJzIG9mIHRoZSBmb3JtICd7eyN3aXRoIHggYXMgfCB5IHx9fS4uLnt7L3dpdGh9fSdcbiAgICBiZWdpbjogL2FzXFxzK1xcfC8sXG4gICAga2V5d29yZHM6IHtcbiAgICAgIGtleXdvcmQ6ICdhcydcbiAgICB9LFxuICAgIGVuZDogL1xcfC8sXG4gICAgY29udGFpbnM6IFtcbiAgICAgIHtcbiAgICAgICAgLy8gZGVmaW5lIHN1Yi1tb2RlIGluIG9yZGVyIHRvIHByZXZlbnQgaGlnaGxpZ2h0aW5nIG9mIGJsb2NrLXBhcmFtZXRlciBuYW1lZCBcImFzXCJcbiAgICAgICAgYmVnaW46IC9cXHcrL1xuICAgICAgfVxuICAgIF1cbiAgfTtcblxuICBjb25zdCBIRUxQRVJfUEFSQU1FVEVSUyA9IHtcbiAgICBjb250YWluczogW1xuICAgICAgaGxqcy5OVU1CRVJfTU9ERSxcbiAgICAgIGhsanMuUVVPVEVfU1RSSU5HX01PREUsXG4gICAgICBobGpzLkFQT1NfU1RSSU5HX01PREUsXG4gICAgICBCTE9DS19QQVJBTVMsXG4gICAgICBIQVNILFxuICAgICAgSEVMUEVSX1BBUkFNRVRFUixcbiAgICAgIFNVQl9FWFBSRVNTSU9OXG4gICAgXSxcbiAgICByZXR1cm5FbmQ6IHRydWVcbiAgICAvLyB0aGUgcHJvcGVydHkgXCJlbmRcIiBpcyBkZWZpbmVkIHRocm91Z2ggaW5oZXJpdGFuY2Ugd2hlbiB0aGUgbW9kZSBpcyB1c2VkLiBJZiBkZXBlbmRzXG4gICAgLy8gb24gdGhlIHN1cnJvdW5kaW5nIG1vZGUsIGJ1dCBcImVuZHNXaXRoUGFyZW50XCIgZG9lcyBub3Qgd29yayBoZXJlIChpLmUuIGl0IGluY2x1ZGVzIHRoZVxuICAgIC8vIGVuZC10b2tlbiBvZiB0aGUgc3Vycm91bmRpbmcgbW9kZSlcbiAgfTtcblxuICBjb25zdCBTVUJfRVhQUkVTU0lPTl9DT05URU5UUyA9IGhsanMuaW5oZXJpdChIRUxQRVJfTkFNRV9PUl9QQVRIX0VYUFJFU1NJT04sIHtcbiAgICBjbGFzc05hbWU6ICduYW1lJyxcbiAgICBrZXl3b3JkczogQlVJTFRfSU5TLFxuICAgIHN0YXJ0czogaGxqcy5pbmhlcml0KEhFTFBFUl9QQVJBTUVURVJTLCB7XG4gICAgICBlbmQ6IC9cXCkvXG4gICAgfSlcbiAgfSk7XG5cbiAgU1VCX0VYUFJFU1NJT04uY29udGFpbnMgPSBbU1VCX0VYUFJFU1NJT05fQ09OVEVOVFNdO1xuXG4gIGNvbnN0IE9QRU5JTkdfQkxPQ0tfTVVTVEFDSEVfQ09OVEVOVFMgPSBobGpzLmluaGVyaXQoSEVMUEVSX05BTUVfT1JfUEFUSF9FWFBSRVNTSU9OLCB7XG4gICAga2V5d29yZHM6IEJVSUxUX0lOUyxcbiAgICBjbGFzc05hbWU6ICduYW1lJyxcbiAgICBzdGFydHM6IGhsanMuaW5oZXJpdChIRUxQRVJfUEFSQU1FVEVSUywge1xuICAgICAgZW5kOiAvXFx9XFx9L1xuICAgIH0pXG4gIH0pO1xuXG4gIGNvbnN0IENMT1NJTkdfQkxPQ0tfTVVTVEFDSEVfQ09OVEVOVFMgPSBobGpzLmluaGVyaXQoSEVMUEVSX05BTUVfT1JfUEFUSF9FWFBSRVNTSU9OLCB7XG4gICAga2V5d29yZHM6IEJVSUxUX0lOUyxcbiAgICBjbGFzc05hbWU6ICduYW1lJ1xuICB9KTtcblxuICBjb25zdCBCQVNJQ19NVVNUQUNIRV9DT05URU5UUyA9IGhsanMuaW5oZXJpdChIRUxQRVJfTkFNRV9PUl9QQVRIX0VYUFJFU1NJT04sIHtcbiAgICBjbGFzc05hbWU6ICduYW1lJyxcbiAgICBrZXl3b3JkczogQlVJTFRfSU5TLFxuICAgIHN0YXJ0czogaGxqcy5pbmhlcml0KEhFTFBFUl9QQVJBTUVURVJTLCB7XG4gICAgICBlbmQ6IC9cXH1cXH0vXG4gICAgfSlcbiAgfSk7XG5cbiAgY29uc3QgRVNDQVBFX01VU1RBQ0hFX1dJVEhfUFJFQ0VFRElOR19CQUNLU0xBU0ggPSB7XG4gICAgYmVnaW46IC9cXFxcXFx7XFx7LyxcbiAgICBza2lwOiB0cnVlXG4gIH07XG4gIGNvbnN0IFBSRVZFTlRfRVNDQVBFX1dJVEhfQU5PVEhFUl9QUkVDRUVESU5HX0JBQ0tTTEFTSCA9IHtcbiAgICBiZWdpbjogL1xcXFxcXFxcKD89XFx7XFx7KS8sXG4gICAgc2tpcDogdHJ1ZVxuICB9O1xuXG4gIHJldHVybiB7XG4gICAgbmFtZTogJ0hhbmRsZWJhcnMnLFxuICAgIGFsaWFzZXM6IFtcbiAgICAgICdoYnMnLFxuICAgICAgJ2h0bWwuaGJzJyxcbiAgICAgICdodG1sLmhhbmRsZWJhcnMnLFxuICAgICAgJ2h0bWxiYXJzJ1xuICAgIF0sXG4gICAgY2FzZV9pbnNlbnNpdGl2ZTogdHJ1ZSxcbiAgICBzdWJMYW5ndWFnZTogJ3htbCcsXG4gICAgY29udGFpbnM6IFtcbiAgICAgIEVTQ0FQRV9NVVNUQUNIRV9XSVRIX1BSRUNFRURJTkdfQkFDS1NMQVNILFxuICAgICAgUFJFVkVOVF9FU0NBUEVfV0lUSF9BTk9USEVSX1BSRUNFRURJTkdfQkFDS1NMQVNILFxuICAgICAgaGxqcy5DT01NRU5UKC9cXHtcXHshLS0vLCAvLS1cXH1cXH0vKSxcbiAgICAgIGhsanMuQ09NTUVOVCgvXFx7XFx7IS8sIC9cXH1cXH0vKSxcbiAgICAgIHtcbiAgICAgICAgLy8gb3BlbiByYXcgYmxvY2sgXCJ7e3t7cmF3fX19fSBjb250ZW50IG5vdCBldmFsdWF0ZWQge3t7ey9yYXd9fX19XCJcbiAgICAgICAgY2xhc3NOYW1lOiAndGVtcGxhdGUtdGFnJyxcbiAgICAgICAgYmVnaW46IC9cXHtcXHtcXHtcXHsoPyFcXC8pLyxcbiAgICAgICAgZW5kOiAvXFx9XFx9XFx9XFx9LyxcbiAgICAgICAgY29udGFpbnM6IFtPUEVOSU5HX0JMT0NLX01VU1RBQ0hFX0NPTlRFTlRTXSxcbiAgICAgICAgc3RhcnRzOiB7XG4gICAgICAgICAgZW5kOiAvXFx7XFx7XFx7XFx7XFwvLyxcbiAgICAgICAgICByZXR1cm5FbmQ6IHRydWUsXG4gICAgICAgICAgc3ViTGFuZ3VhZ2U6ICd4bWwnXG4gICAgICAgIH1cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIC8vIGNsb3NlIHJhdyBibG9ja1xuICAgICAgICBjbGFzc05hbWU6ICd0ZW1wbGF0ZS10YWcnLFxuICAgICAgICBiZWdpbjogL1xce1xce1xce1xce1xcLy8sXG4gICAgICAgIGVuZDogL1xcfVxcfVxcfVxcfS8sXG4gICAgICAgIGNvbnRhaW5zOiBbQ0xPU0lOR19CTE9DS19NVVNUQUNIRV9DT05URU5UU11cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIC8vIG9wZW4gYmxvY2sgc3RhdGVtZW50XG4gICAgICAgIGNsYXNzTmFtZTogJ3RlbXBsYXRlLXRhZycsXG4gICAgICAgIGJlZ2luOiAvXFx7XFx7Iy8sXG4gICAgICAgIGVuZDogL1xcfVxcfS8sXG4gICAgICAgIGNvbnRhaW5zOiBbT1BFTklOR19CTE9DS19NVVNUQUNIRV9DT05URU5UU11cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3RlbXBsYXRlLXRhZycsXG4gICAgICAgIGJlZ2luOiAvXFx7XFx7KD89ZWxzZVxcfVxcfSkvLFxuICAgICAgICBlbmQ6IC9cXH1cXH0vLFxuICAgICAgICBrZXl3b3JkczogJ2Vsc2UnXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICd0ZW1wbGF0ZS10YWcnLFxuICAgICAgICBiZWdpbjogL1xce1xceyg/PWVsc2UgaWYpLyxcbiAgICAgICAgZW5kOiAvXFx9XFx9LyxcbiAgICAgICAga2V5d29yZHM6ICdlbHNlIGlmJ1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgLy8gY2xvc2luZyBibG9jayBzdGF0ZW1lbnRcbiAgICAgICAgY2xhc3NOYW1lOiAndGVtcGxhdGUtdGFnJyxcbiAgICAgICAgYmVnaW46IC9cXHtcXHtcXC8vLFxuICAgICAgICBlbmQ6IC9cXH1cXH0vLFxuICAgICAgICBjb250YWluczogW0NMT1NJTkdfQkxPQ0tfTVVTVEFDSEVfQ09OVEVOVFNdXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICAvLyB0ZW1wbGF0ZSB2YXJpYWJsZSBvciBoZWxwZXItY2FsbCB0aGF0IGlzIE5PVCBodG1sLWVzY2FwZWRcbiAgICAgICAgY2xhc3NOYW1lOiAndGVtcGxhdGUtdmFyaWFibGUnLFxuICAgICAgICBiZWdpbjogL1xce1xce1xcey8sXG4gICAgICAgIGVuZDogL1xcfVxcfVxcfS8sXG4gICAgICAgIGNvbnRhaW5zOiBbQkFTSUNfTVVTVEFDSEVfQ09OVEVOVFNdXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICAvLyB0ZW1wbGF0ZSB2YXJpYWJsZSBvciBoZWxwZXItY2FsbCB0aGF0IGlzIGh0bWwtZXNjYXBlZFxuICAgICAgICBjbGFzc05hbWU6ICd0ZW1wbGF0ZS12YXJpYWJsZScsXG4gICAgICAgIGJlZ2luOiAvXFx7XFx7LyxcbiAgICAgICAgZW5kOiAvXFx9XFx9LyxcbiAgICAgICAgY29udGFpbnM6IFtCQVNJQ19NVVNUQUNIRV9DT05URU5UU11cbiAgICAgIH1cbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gaGFuZGxlYmFycztcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==