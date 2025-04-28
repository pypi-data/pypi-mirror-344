(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_htmlbars"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/htmlbars.js":
/*!***************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/htmlbars.js ***!
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

/*
 Language: HTMLBars (legacy)
 Requires: xml.js
 Description: Matcher for Handlebars as well as EmberJS additions.
 Website: https://github.com/tildeio/htmlbars
 Category: template
 */

function htmlbars(hljs) {
  const definition = handlebars(hljs);

  definition.name = "HTMLbars";

  // HACK: This lets handlebars do the auto-detection if it's been loaded (by
  // default the build script will load in alphabetical order) and if not (perhaps
  // an install is only using `htmlbars`, not `handlebars`) then this will still
  // allow HTMLBars to participate in the auto-detection

  // worse case someone will have HTMLbars and handlebars competing for the same
  // content and will need to change their setup to only require handlebars, but
  // I don't consider this a breaking change
  if (hljs.getLanguage("handlebars")) {
    definition.disableAutodetect = true;
  }

  return definition;
}

module.exports = htmlbars;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfaHRtbGJhcnMuZHRhbGVfYnVuZGxlLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7O0FBQUE7QUFDQSxXQUFXLFFBQVE7QUFDbkIsYUFBYTtBQUNiOztBQUVBO0FBQ0EsV0FBVyxrQkFBa0I7QUFDN0IsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7O0FBRUE7QUFDQSxXQUFXLGtCQUFrQjtBQUM3QixhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQSxXQUFXLGtCQUFrQjtBQUM3QixhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQSxXQUFXLHVCQUF1QjtBQUNsQyxhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFdBQVcsc0JBQXNCO0FBQ2pDLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0EsNkNBQTZDLGFBQWEsRUFBRTtBQUM1RDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQSxHQUFHOztBQUVIO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQSxpQ0FBaUMsa0JBQWtCLEtBQUssT0FBTztBQUMvRDtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTCxHQUFHOztBQUVIOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsY0FBYyxFQUFFO0FBQ2hCLEtBQUs7QUFDTCxHQUFHOztBQUVIO0FBQ0E7QUFDQTtBQUNBLEdBQUc7O0FBRUg7QUFDQTtBQUNBO0FBQ0E7QUFDQSxjQUFjLEVBQUU7QUFDaEIsS0FBSztBQUNMLEdBQUc7O0FBRUg7QUFDQSxnQkFBZ0IsRUFBRTtBQUNsQjtBQUNBO0FBQ0E7QUFDQSxxQkFBcUIsRUFBRTtBQUN2QjtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0Esc0JBQXNCLEVBQUUsV0FBVyxFQUFFO0FBQ3JDLHNCQUFzQixFQUFFLE9BQU8sRUFBRTtBQUNqQztBQUNBLCtCQUErQixRQUFRLDBCQUEwQixRQUFRO0FBQ3pFO0FBQ0Esa0JBQWtCLEVBQUUsRUFBRSxFQUFFO0FBQ3hCLGdCQUFnQixFQUFFLEVBQUUsRUFBRTtBQUN0QjtBQUNBO0FBQ0Esa0JBQWtCLEVBQUUsRUFBRSxFQUFFO0FBQ3hCO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSxrQkFBa0IsRUFBRSxFQUFFLEVBQUU7QUFDeEIsZ0JBQWdCLEVBQUUsRUFBRSxFQUFFO0FBQ3RCO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLGtCQUFrQixFQUFFO0FBQ3BCLGdCQUFnQixFQUFFO0FBQ2xCO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQSxrQkFBa0IsRUFBRSxTQUFTLEVBQUU7QUFDL0IsZ0JBQWdCLEVBQUU7QUFDbEI7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBLGtCQUFrQixFQUFFO0FBQ3BCLGdCQUFnQixFQUFFO0FBQ2xCO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLGtCQUFrQixFQUFFO0FBQ3BCLGdCQUFnQixFQUFFO0FBQ2xCO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLGtCQUFrQixFQUFFLEVBQUU7QUFDdEIsZ0JBQWdCLEVBQUUsRUFBRTtBQUNwQjtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSxrQkFBa0IsRUFBRTtBQUNwQixnQkFBZ0IsRUFBRTtBQUNsQjtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7O0FBRUE7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL2h0bWxiYXJzLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qKlxuICogQHBhcmFtIHtzdHJpbmd9IHZhbHVlXG4gKiBAcmV0dXJucyB7UmVnRXhwfVxuICogKi9cblxuLyoqXG4gKiBAcGFyYW0ge1JlZ0V4cCB8IHN0cmluZyB9IHJlXG4gKiBAcmV0dXJucyB7c3RyaW5nfVxuICovXG5mdW5jdGlvbiBzb3VyY2UocmUpIHtcbiAgaWYgKCFyZSkgcmV0dXJuIG51bGw7XG4gIGlmICh0eXBlb2YgcmUgPT09IFwic3RyaW5nXCIpIHJldHVybiByZTtcblxuICByZXR1cm4gcmUuc291cmNlO1xufVxuXG4vKipcbiAqIEBwYXJhbSB7UmVnRXhwIHwgc3RyaW5nIH0gcmVcbiAqIEByZXR1cm5zIHtzdHJpbmd9XG4gKi9cbmZ1bmN0aW9uIGFueU51bWJlck9mVGltZXMocmUpIHtcbiAgcmV0dXJuIGNvbmNhdCgnKCcsIHJlLCAnKSonKTtcbn1cblxuLyoqXG4gKiBAcGFyYW0ge1JlZ0V4cCB8IHN0cmluZyB9IHJlXG4gKiBAcmV0dXJucyB7c3RyaW5nfVxuICovXG5mdW5jdGlvbiBvcHRpb25hbChyZSkge1xuICByZXR1cm4gY29uY2F0KCcoJywgcmUsICcpPycpO1xufVxuXG4vKipcbiAqIEBwYXJhbSB7Li4uKFJlZ0V4cCB8IHN0cmluZykgfSBhcmdzXG4gKiBAcmV0dXJucyB7c3RyaW5nfVxuICovXG5mdW5jdGlvbiBjb25jYXQoLi4uYXJncykge1xuICBjb25zdCBqb2luZWQgPSBhcmdzLm1hcCgoeCkgPT4gc291cmNlKHgpKS5qb2luKFwiXCIpO1xuICByZXR1cm4gam9pbmVkO1xufVxuXG4vKipcbiAqIEFueSBvZiB0aGUgcGFzc2VkIGV4cHJlc3NzaW9ucyBtYXkgbWF0Y2hcbiAqXG4gKiBDcmVhdGVzIGEgaHVnZSB0aGlzIHwgdGhpcyB8IHRoYXQgfCB0aGF0IG1hdGNoXG4gKiBAcGFyYW0geyhSZWdFeHAgfCBzdHJpbmcpW10gfSBhcmdzXG4gKiBAcmV0dXJucyB7c3RyaW5nfVxuICovXG5mdW5jdGlvbiBlaXRoZXIoLi4uYXJncykge1xuICBjb25zdCBqb2luZWQgPSAnKCcgKyBhcmdzLm1hcCgoeCkgPT4gc291cmNlKHgpKS5qb2luKFwifFwiKSArIFwiKVwiO1xuICByZXR1cm4gam9pbmVkO1xufVxuXG4vKlxuTGFuZ3VhZ2U6IEhhbmRsZWJhcnNcblJlcXVpcmVzOiB4bWwuanNcbkF1dGhvcjogUm9iaW4gV2FyZCA8cm9iaW4ud2FyZEBnbWFpbC5jb20+XG5EZXNjcmlwdGlvbjogTWF0Y2hlciBmb3IgSGFuZGxlYmFycyBhcyB3ZWxsIGFzIEVtYmVySlMgYWRkaXRpb25zLlxuV2Vic2l0ZTogaHR0cHM6Ly9oYW5kbGViYXJzanMuY29tXG5DYXRlZ29yeTogdGVtcGxhdGVcbiovXG5cbmZ1bmN0aW9uIGhhbmRsZWJhcnMoaGxqcykge1xuICBjb25zdCBCVUlMVF9JTlMgPSB7XG4gICAgJ2J1aWx0aW4tbmFtZSc6IFtcbiAgICAgICdhY3Rpb24nLFxuICAgICAgJ2JpbmRhdHRyJyxcbiAgICAgICdjb2xsZWN0aW9uJyxcbiAgICAgICdjb21wb25lbnQnLFxuICAgICAgJ2NvbmNhdCcsXG4gICAgICAnZGVidWdnZXInLFxuICAgICAgJ2VhY2gnLFxuICAgICAgJ2VhY2gtaW4nLFxuICAgICAgJ2dldCcsXG4gICAgICAnaGFzaCcsXG4gICAgICAnaWYnLFxuICAgICAgJ2luJyxcbiAgICAgICdpbnB1dCcsXG4gICAgICAnbGluay10bycsXG4gICAgICAnbG9jJyxcbiAgICAgICdsb2cnLFxuICAgICAgJ2xvb2t1cCcsXG4gICAgICAnbXV0JyxcbiAgICAgICdvdXRsZXQnLFxuICAgICAgJ3BhcnRpYWwnLFxuICAgICAgJ3F1ZXJ5LXBhcmFtcycsXG4gICAgICAncmVuZGVyJyxcbiAgICAgICd0ZW1wbGF0ZScsXG4gICAgICAndGV4dGFyZWEnLFxuICAgICAgJ3VuYm91bmQnLFxuICAgICAgJ3VubGVzcycsXG4gICAgICAndmlldycsXG4gICAgICAnd2l0aCcsXG4gICAgICAneWllbGQnXG4gICAgXVxuICB9O1xuXG4gIGNvbnN0IExJVEVSQUxTID0ge1xuICAgIGxpdGVyYWw6IFtcbiAgICAgICd0cnVlJyxcbiAgICAgICdmYWxzZScsXG4gICAgICAndW5kZWZpbmVkJyxcbiAgICAgICdudWxsJ1xuICAgIF1cbiAgfTtcblxuICAvLyBhcyBkZWZpbmVkIGluIGh0dHBzOi8vaGFuZGxlYmFyc2pzLmNvbS9ndWlkZS9leHByZXNzaW9ucy5odG1sI2xpdGVyYWwtc2VnbWVudHNcbiAgLy8gdGhpcyByZWdleCBtYXRjaGVzIGxpdGVyYWwgc2VnbWVudHMgbGlrZSAnIGFiYyAnIG9yIFsgYWJjIF0gYXMgd2VsbCBhcyBoZWxwZXJzIGFuZCBwYXRoc1xuICAvLyBsaWtlIGEvYiwgLi9hYmMvY2RlLCBhbmQgYWJjLmJjZFxuXG4gIGNvbnN0IERPVUJMRV9RVU9URURfSURfUkVHRVggPSAvXCJcInxcIlteXCJdK1wiLztcbiAgY29uc3QgU0lOR0xFX1FVT1RFRF9JRF9SRUdFWCA9IC8nJ3wnW14nXSsnLztcbiAgY29uc3QgQlJBQ0tFVF9RVU9URURfSURfUkVHRVggPSAvXFxbXFxdfFxcW1teXFxdXStcXF0vO1xuICBjb25zdCBQTEFJTl9JRF9SRUdFWCA9IC9bXlxccyFcIiMlJicoKSorLC5cXC87PD0+QFxcW1xcXFxcXF1eYHt8fX5dKy87XG4gIGNvbnN0IFBBVEhfREVMSU1JVEVSX1JFR0VYID0gLyhcXC58XFwvKS87XG4gIGNvbnN0IEFOWV9JRCA9IGVpdGhlcihcbiAgICBET1VCTEVfUVVPVEVEX0lEX1JFR0VYLFxuICAgIFNJTkdMRV9RVU9URURfSURfUkVHRVgsXG4gICAgQlJBQ0tFVF9RVU9URURfSURfUkVHRVgsXG4gICAgUExBSU5fSURfUkVHRVhcbiAgICApO1xuXG4gIGNvbnN0IElERU5USUZJRVJfUkVHRVggPSBjb25jYXQoXG4gICAgb3B0aW9uYWwoL1xcLnxcXC5cXC98XFwvLyksIC8vIHJlbGF0aXZlIG9yIGFic29sdXRlIHBhdGhcbiAgICBBTllfSUQsXG4gICAgYW55TnVtYmVyT2ZUaW1lcyhjb25jYXQoXG4gICAgICBQQVRIX0RFTElNSVRFUl9SRUdFWCxcbiAgICAgIEFOWV9JRFxuICAgICkpXG4gICk7XG5cbiAgLy8gaWRlbnRpZmllciBmb2xsb3dlZCBieSBhIGVxdWFsLXNpZ24gKHdpdGhvdXQgdGhlIGVxdWFsIHNpZ24pXG4gIGNvbnN0IEhBU0hfUEFSQU1fUkVHRVggPSBjb25jYXQoXG4gICAgJygnLFxuICAgIEJSQUNLRVRfUVVPVEVEX0lEX1JFR0VYLCAnfCcsXG4gICAgUExBSU5fSURfUkVHRVgsXG4gICAgJykoPz09KSdcbiAgKTtcblxuICBjb25zdCBIRUxQRVJfTkFNRV9PUl9QQVRIX0VYUFJFU1NJT04gPSB7XG4gICAgYmVnaW46IElERU5USUZJRVJfUkVHRVgsXG4gICAgbGV4ZW1lczogL1tcXHcuXFwvXSsvXG4gIH07XG5cbiAgY29uc3QgSEVMUEVSX1BBUkFNRVRFUiA9IGhsanMuaW5oZXJpdChIRUxQRVJfTkFNRV9PUl9QQVRIX0VYUFJFU1NJT04sIHtcbiAgICBrZXl3b3JkczogTElURVJBTFNcbiAgfSk7XG5cbiAgY29uc3QgU1VCX0VYUFJFU1NJT04gPSB7XG4gICAgYmVnaW46IC9cXCgvLFxuICAgIGVuZDogL1xcKS9cbiAgICAvLyB0aGUgXCJjb250YWluc1wiIGlzIGFkZGVkIGJlbG93IHdoZW4gYWxsIG5lY2Vzc2FyeSBzdWItbW9kZXMgYXJlIGRlZmluZWRcbiAgfTtcblxuICBjb25zdCBIQVNIID0ge1xuICAgIC8vIGZrYSBcImF0dHJpYnV0ZS1hc3NpZ25tZW50XCIsIHBhcmFtZXRlcnMgb2YgdGhlIGZvcm0gJ2tleT12YWx1ZSdcbiAgICBjbGFzc05hbWU6ICdhdHRyJyxcbiAgICBiZWdpbjogSEFTSF9QQVJBTV9SRUdFWCxcbiAgICByZWxldmFuY2U6IDAsXG4gICAgc3RhcnRzOiB7XG4gICAgICBiZWdpbjogLz0vLFxuICAgICAgZW5kOiAvPS8sXG4gICAgICBzdGFydHM6IHtcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICBobGpzLk5VTUJFUl9NT0RFLFxuICAgICAgICAgIGhsanMuUVVPVEVfU1RSSU5HX01PREUsXG4gICAgICAgICAgaGxqcy5BUE9TX1NUUklOR19NT0RFLFxuICAgICAgICAgIEhFTFBFUl9QQVJBTUVURVIsXG4gICAgICAgICAgU1VCX0VYUFJFU1NJT05cbiAgICAgICAgXVxuICAgICAgfVxuICAgIH1cbiAgfTtcblxuICBjb25zdCBCTE9DS19QQVJBTVMgPSB7XG4gICAgLy8gcGFyYW1ldGVycyBvZiB0aGUgZm9ybSAne3sjd2l0aCB4IGFzIHwgeSB8fX0uLi57ey93aXRofX0nXG4gICAgYmVnaW46IC9hc1xccytcXHwvLFxuICAgIGtleXdvcmRzOiB7XG4gICAgICBrZXl3b3JkOiAnYXMnXG4gICAgfSxcbiAgICBlbmQ6IC9cXHwvLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICB7XG4gICAgICAgIC8vIGRlZmluZSBzdWItbW9kZSBpbiBvcmRlciB0byBwcmV2ZW50IGhpZ2hsaWdodGluZyBvZiBibG9jay1wYXJhbWV0ZXIgbmFtZWQgXCJhc1wiXG4gICAgICAgIGJlZ2luOiAvXFx3Ky9cbiAgICAgIH1cbiAgICBdXG4gIH07XG5cbiAgY29uc3QgSEVMUEVSX1BBUkFNRVRFUlMgPSB7XG4gICAgY29udGFpbnM6IFtcbiAgICAgIGhsanMuTlVNQkVSX01PREUsXG4gICAgICBobGpzLlFVT1RFX1NUUklOR19NT0RFLFxuICAgICAgaGxqcy5BUE9TX1NUUklOR19NT0RFLFxuICAgICAgQkxPQ0tfUEFSQU1TLFxuICAgICAgSEFTSCxcbiAgICAgIEhFTFBFUl9QQVJBTUVURVIsXG4gICAgICBTVUJfRVhQUkVTU0lPTlxuICAgIF0sXG4gICAgcmV0dXJuRW5kOiB0cnVlXG4gICAgLy8gdGhlIHByb3BlcnR5IFwiZW5kXCIgaXMgZGVmaW5lZCB0aHJvdWdoIGluaGVyaXRhbmNlIHdoZW4gdGhlIG1vZGUgaXMgdXNlZC4gSWYgZGVwZW5kc1xuICAgIC8vIG9uIHRoZSBzdXJyb3VuZGluZyBtb2RlLCBidXQgXCJlbmRzV2l0aFBhcmVudFwiIGRvZXMgbm90IHdvcmsgaGVyZSAoaS5lLiBpdCBpbmNsdWRlcyB0aGVcbiAgICAvLyBlbmQtdG9rZW4gb2YgdGhlIHN1cnJvdW5kaW5nIG1vZGUpXG4gIH07XG5cbiAgY29uc3QgU1VCX0VYUFJFU1NJT05fQ09OVEVOVFMgPSBobGpzLmluaGVyaXQoSEVMUEVSX05BTUVfT1JfUEFUSF9FWFBSRVNTSU9OLCB7XG4gICAgY2xhc3NOYW1lOiAnbmFtZScsXG4gICAga2V5d29yZHM6IEJVSUxUX0lOUyxcbiAgICBzdGFydHM6IGhsanMuaW5oZXJpdChIRUxQRVJfUEFSQU1FVEVSUywge1xuICAgICAgZW5kOiAvXFwpL1xuICAgIH0pXG4gIH0pO1xuXG4gIFNVQl9FWFBSRVNTSU9OLmNvbnRhaW5zID0gW1NVQl9FWFBSRVNTSU9OX0NPTlRFTlRTXTtcblxuICBjb25zdCBPUEVOSU5HX0JMT0NLX01VU1RBQ0hFX0NPTlRFTlRTID0gaGxqcy5pbmhlcml0KEhFTFBFUl9OQU1FX09SX1BBVEhfRVhQUkVTU0lPTiwge1xuICAgIGtleXdvcmRzOiBCVUlMVF9JTlMsXG4gICAgY2xhc3NOYW1lOiAnbmFtZScsXG4gICAgc3RhcnRzOiBobGpzLmluaGVyaXQoSEVMUEVSX1BBUkFNRVRFUlMsIHtcbiAgICAgIGVuZDogL1xcfVxcfS9cbiAgICB9KVxuICB9KTtcblxuICBjb25zdCBDTE9TSU5HX0JMT0NLX01VU1RBQ0hFX0NPTlRFTlRTID0gaGxqcy5pbmhlcml0KEhFTFBFUl9OQU1FX09SX1BBVEhfRVhQUkVTU0lPTiwge1xuICAgIGtleXdvcmRzOiBCVUlMVF9JTlMsXG4gICAgY2xhc3NOYW1lOiAnbmFtZSdcbiAgfSk7XG5cbiAgY29uc3QgQkFTSUNfTVVTVEFDSEVfQ09OVEVOVFMgPSBobGpzLmluaGVyaXQoSEVMUEVSX05BTUVfT1JfUEFUSF9FWFBSRVNTSU9OLCB7XG4gICAgY2xhc3NOYW1lOiAnbmFtZScsXG4gICAga2V5d29yZHM6IEJVSUxUX0lOUyxcbiAgICBzdGFydHM6IGhsanMuaW5oZXJpdChIRUxQRVJfUEFSQU1FVEVSUywge1xuICAgICAgZW5kOiAvXFx9XFx9L1xuICAgIH0pXG4gIH0pO1xuXG4gIGNvbnN0IEVTQ0FQRV9NVVNUQUNIRV9XSVRIX1BSRUNFRURJTkdfQkFDS1NMQVNIID0ge1xuICAgIGJlZ2luOiAvXFxcXFxce1xcey8sXG4gICAgc2tpcDogdHJ1ZVxuICB9O1xuICBjb25zdCBQUkVWRU5UX0VTQ0FQRV9XSVRIX0FOT1RIRVJfUFJFQ0VFRElOR19CQUNLU0xBU0ggPSB7XG4gICAgYmVnaW46IC9cXFxcXFxcXCg/PVxce1xceykvLFxuICAgIHNraXA6IHRydWVcbiAgfTtcblxuICByZXR1cm4ge1xuICAgIG5hbWU6ICdIYW5kbGViYXJzJyxcbiAgICBhbGlhc2VzOiBbXG4gICAgICAnaGJzJyxcbiAgICAgICdodG1sLmhicycsXG4gICAgICAnaHRtbC5oYW5kbGViYXJzJyxcbiAgICAgICdodG1sYmFycydcbiAgICBdLFxuICAgIGNhc2VfaW5zZW5zaXRpdmU6IHRydWUsXG4gICAgc3ViTGFuZ3VhZ2U6ICd4bWwnLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBFU0NBUEVfTVVTVEFDSEVfV0lUSF9QUkVDRUVESU5HX0JBQ0tTTEFTSCxcbiAgICAgIFBSRVZFTlRfRVNDQVBFX1dJVEhfQU5PVEhFUl9QUkVDRUVESU5HX0JBQ0tTTEFTSCxcbiAgICAgIGhsanMuQ09NTUVOVCgvXFx7XFx7IS0tLywgLy0tXFx9XFx9LyksXG4gICAgICBobGpzLkNPTU1FTlQoL1xce1xceyEvLCAvXFx9XFx9LyksXG4gICAgICB7XG4gICAgICAgIC8vIG9wZW4gcmF3IGJsb2NrIFwie3t7e3Jhd319fX0gY29udGVudCBub3QgZXZhbHVhdGVkIHt7e3svcmF3fX19fVwiXG4gICAgICAgIGNsYXNzTmFtZTogJ3RlbXBsYXRlLXRhZycsXG4gICAgICAgIGJlZ2luOiAvXFx7XFx7XFx7XFx7KD8hXFwvKS8sXG4gICAgICAgIGVuZDogL1xcfVxcfVxcfVxcfS8sXG4gICAgICAgIGNvbnRhaW5zOiBbT1BFTklOR19CTE9DS19NVVNUQUNIRV9DT05URU5UU10sXG4gICAgICAgIHN0YXJ0czoge1xuICAgICAgICAgIGVuZDogL1xce1xce1xce1xce1xcLy8sXG4gICAgICAgICAgcmV0dXJuRW5kOiB0cnVlLFxuICAgICAgICAgIHN1Ykxhbmd1YWdlOiAneG1sJ1xuICAgICAgICB9XG4gICAgICB9LFxuICAgICAge1xuICAgICAgICAvLyBjbG9zZSByYXcgYmxvY2tcbiAgICAgICAgY2xhc3NOYW1lOiAndGVtcGxhdGUtdGFnJyxcbiAgICAgICAgYmVnaW46IC9cXHtcXHtcXHtcXHtcXC8vLFxuICAgICAgICBlbmQ6IC9cXH1cXH1cXH1cXH0vLFxuICAgICAgICBjb250YWluczogW0NMT1NJTkdfQkxPQ0tfTVVTVEFDSEVfQ09OVEVOVFNdXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICAvLyBvcGVuIGJsb2NrIHN0YXRlbWVudFxuICAgICAgICBjbGFzc05hbWU6ICd0ZW1wbGF0ZS10YWcnLFxuICAgICAgICBiZWdpbjogL1xce1xceyMvLFxuICAgICAgICBlbmQ6IC9cXH1cXH0vLFxuICAgICAgICBjb250YWluczogW09QRU5JTkdfQkxPQ0tfTVVTVEFDSEVfQ09OVEVOVFNdXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICd0ZW1wbGF0ZS10YWcnLFxuICAgICAgICBiZWdpbjogL1xce1xceyg/PWVsc2VcXH1cXH0pLyxcbiAgICAgICAgZW5kOiAvXFx9XFx9LyxcbiAgICAgICAga2V5d29yZHM6ICdlbHNlJ1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAndGVtcGxhdGUtdGFnJyxcbiAgICAgICAgYmVnaW46IC9cXHtcXHsoPz1lbHNlIGlmKS8sXG4gICAgICAgIGVuZDogL1xcfVxcfS8sXG4gICAgICAgIGtleXdvcmRzOiAnZWxzZSBpZidcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIC8vIGNsb3NpbmcgYmxvY2sgc3RhdGVtZW50XG4gICAgICAgIGNsYXNzTmFtZTogJ3RlbXBsYXRlLXRhZycsXG4gICAgICAgIGJlZ2luOiAvXFx7XFx7XFwvLyxcbiAgICAgICAgZW5kOiAvXFx9XFx9LyxcbiAgICAgICAgY29udGFpbnM6IFtDTE9TSU5HX0JMT0NLX01VU1RBQ0hFX0NPTlRFTlRTXVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgLy8gdGVtcGxhdGUgdmFyaWFibGUgb3IgaGVscGVyLWNhbGwgdGhhdCBpcyBOT1QgaHRtbC1lc2NhcGVkXG4gICAgICAgIGNsYXNzTmFtZTogJ3RlbXBsYXRlLXZhcmlhYmxlJyxcbiAgICAgICAgYmVnaW46IC9cXHtcXHtcXHsvLFxuICAgICAgICBlbmQ6IC9cXH1cXH1cXH0vLFxuICAgICAgICBjb250YWluczogW0JBU0lDX01VU1RBQ0hFX0NPTlRFTlRTXVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgLy8gdGVtcGxhdGUgdmFyaWFibGUgb3IgaGVscGVyLWNhbGwgdGhhdCBpcyBodG1sLWVzY2FwZWRcbiAgICAgICAgY2xhc3NOYW1lOiAndGVtcGxhdGUtdmFyaWFibGUnLFxuICAgICAgICBiZWdpbjogL1xce1xcey8sXG4gICAgICAgIGVuZDogL1xcfVxcfS8sXG4gICAgICAgIGNvbnRhaW5zOiBbQkFTSUNfTVVTVEFDSEVfQ09OVEVOVFNdXG4gICAgICB9XG4gICAgXVxuICB9O1xufVxuXG4vKlxuIExhbmd1YWdlOiBIVE1MQmFycyAobGVnYWN5KVxuIFJlcXVpcmVzOiB4bWwuanNcbiBEZXNjcmlwdGlvbjogTWF0Y2hlciBmb3IgSGFuZGxlYmFycyBhcyB3ZWxsIGFzIEVtYmVySlMgYWRkaXRpb25zLlxuIFdlYnNpdGU6IGh0dHBzOi8vZ2l0aHViLmNvbS90aWxkZWlvL2h0bWxiYXJzXG4gQ2F0ZWdvcnk6IHRlbXBsYXRlXG4gKi9cblxuZnVuY3Rpb24gaHRtbGJhcnMoaGxqcykge1xuICBjb25zdCBkZWZpbml0aW9uID0gaGFuZGxlYmFycyhobGpzKTtcblxuICBkZWZpbml0aW9uLm5hbWUgPSBcIkhUTUxiYXJzXCI7XG5cbiAgLy8gSEFDSzogVGhpcyBsZXRzIGhhbmRsZWJhcnMgZG8gdGhlIGF1dG8tZGV0ZWN0aW9uIGlmIGl0J3MgYmVlbiBsb2FkZWQgKGJ5XG4gIC8vIGRlZmF1bHQgdGhlIGJ1aWxkIHNjcmlwdCB3aWxsIGxvYWQgaW4gYWxwaGFiZXRpY2FsIG9yZGVyKSBhbmQgaWYgbm90IChwZXJoYXBzXG4gIC8vIGFuIGluc3RhbGwgaXMgb25seSB1c2luZyBgaHRtbGJhcnNgLCBub3QgYGhhbmRsZWJhcnNgKSB0aGVuIHRoaXMgd2lsbCBzdGlsbFxuICAvLyBhbGxvdyBIVE1MQmFycyB0byBwYXJ0aWNpcGF0ZSBpbiB0aGUgYXV0by1kZXRlY3Rpb25cblxuICAvLyB3b3JzZSBjYXNlIHNvbWVvbmUgd2lsbCBoYXZlIEhUTUxiYXJzIGFuZCBoYW5kbGViYXJzIGNvbXBldGluZyBmb3IgdGhlIHNhbWVcbiAgLy8gY29udGVudCBhbmQgd2lsbCBuZWVkIHRvIGNoYW5nZSB0aGVpciBzZXR1cCB0byBvbmx5IHJlcXVpcmUgaGFuZGxlYmFycywgYnV0XG4gIC8vIEkgZG9uJ3QgY29uc2lkZXIgdGhpcyBhIGJyZWFraW5nIGNoYW5nZVxuICBpZiAoaGxqcy5nZXRMYW5ndWFnZShcImhhbmRsZWJhcnNcIikpIHtcbiAgICBkZWZpbml0aW9uLmRpc2FibGVBdXRvZGV0ZWN0ID0gdHJ1ZTtcbiAgfVxuXG4gIHJldHVybiBkZWZpbml0aW9uO1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IGh0bWxiYXJzO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9