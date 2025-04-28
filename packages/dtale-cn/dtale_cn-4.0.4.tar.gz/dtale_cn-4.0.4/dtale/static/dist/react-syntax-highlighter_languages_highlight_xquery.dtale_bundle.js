(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_xquery"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/xquery.js":
/*!*************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/xquery.js ***!
  \*************************************************************************************************/
/***/ ((module) => {

/*
Language: XQuery
Author: Dirk Kirsten <dk@basex.org>
Contributor: Duncan Paterson
Description: Supports XQuery 3.1 including XQuery Update 3, so also XPath (as it is a superset)
Refactored to process xml constructor syntax and function-bodies. Added missing data-types, xpath operands, inbuilt functions, and query prologs
Website: https://www.w3.org/XML/Query/
Category: functional
Audit: 2020
*/

/** @type LanguageFn */
function xquery(_hljs) {
  // see https://www.w3.org/TR/xquery/#id-terminal-delimitation
  const KEYWORDS =
    'module schema namespace boundary-space preserve no-preserve strip default collation base-uri ordering context decimal-format decimal-separator copy-namespaces empty-sequence except exponent-separator external grouping-separator inherit no-inherit lax minus-sign per-mille percent schema-attribute schema-element strict unordered zero-digit ' +
    'declare import option function validate variable ' +
    'for at in let where order group by return if then else ' +
    'tumbling sliding window start when only end previous next stable ' +
    'ascending descending allowing empty greatest least some every satisfies switch case typeswitch try catch ' +
    'and or to union intersect instance of treat as castable cast map array ' +
    'delete insert into replace value rename copy modify update';

  // Node Types (sorted by inheritance)
  // atomic types (sorted by inheritance)
  const TYPE =
    'item document-node node attribute document element comment namespace namespace-node processing-instruction text construction ' +
    'xs:anyAtomicType xs:untypedAtomic xs:duration xs:time xs:decimal xs:float xs:double xs:gYearMonth xs:gYear xs:gMonthDay xs:gMonth xs:gDay xs:boolean xs:base64Binary xs:hexBinary xs:anyURI xs:QName xs:NOTATION xs:dateTime xs:dateTimeStamp xs:date xs:string xs:normalizedString xs:token xs:language xs:NMTOKEN xs:Name xs:NCName xs:ID xs:IDREF xs:ENTITY xs:integer xs:nonPositiveInteger xs:negativeInteger xs:long xs:int xs:short xs:byte xs:nonNegativeInteger xs:unisignedLong xs:unsignedInt xs:unsignedShort xs:unsignedByte xs:positiveInteger xs:yearMonthDuration xs:dayTimeDuration';

  const LITERAL =
    'eq ne lt le gt ge is ' +
    'self:: child:: descendant:: descendant-or-self:: attribute:: following:: following-sibling:: parent:: ancestor:: ancestor-or-self:: preceding:: preceding-sibling:: ' +
    'NaN';

  // functions (TODO: find regex for op: without breaking build)
  const BUILT_IN = {
    className: 'built_in',
    variants: [
      {
        begin: /\barray:/,
        end: /(?:append|filter|flatten|fold-(?:left|right)|for-each(?:-pair)?|get|head|insert-before|join|put|remove|reverse|size|sort|subarray|tail)\b/
      },
      {
        begin: /\bmap:/,
        end: /(?:contains|entry|find|for-each|get|keys|merge|put|remove|size)\b/
      },
      {
        begin: /\bmath:/,
        end: /(?:a(?:cos|sin|tan[2]?)|cos|exp(?:10)?|log(?:10)?|pi|pow|sin|sqrt|tan)\b/
      },
      {
        begin: /\bop:/,
        end: /\(/,
        excludeEnd: true
      },
      {
        begin: /\bfn:/,
        end: /\(/,
        excludeEnd: true
      },
      // do not highlight inbuilt strings as variable or xml element names
      {
        begin: /[^</$:'"-]\b(?:abs|accumulator-(?:after|before)|adjust-(?:date(?:Time)?|time)-to-timezone|analyze-string|apply|available-(?:environment-variables|system-properties)|avg|base-uri|boolean|ceiling|codepoints?-(?:equal|to-string)|collation-key|collection|compare|concat|contains(?:-token)?|copy-of|count|current(?:-)?(?:date(?:Time)?|time|group(?:ing-key)?|output-uri|merge-(?:group|key))?data|dateTime|days?-from-(?:date(?:Time)?|duration)|deep-equal|default-(?:collation|language)|distinct-values|document(?:-uri)?|doc(?:-available)?|element-(?:available|with-id)|empty|encode-for-uri|ends-with|environment-variable|error|escape-html-uri|exactly-one|exists|false|filter|floor|fold-(?:left|right)|for-each(?:-pair)?|format-(?:date(?:Time)?|time|integer|number)|function-(?:arity|available|lookup|name)|generate-id|has-children|head|hours-from-(?:dateTime|duration|time)|id(?:ref)?|implicit-timezone|in-scope-prefixes|index-of|innermost|insert-before|iri-to-uri|json-(?:doc|to-xml)|key|lang|last|load-xquery-module|local-name(?:-from-QName)?|(?:lower|upper)-case|matches|max|minutes-from-(?:dateTime|duration|time)|min|months?-from-(?:date(?:Time)?|duration)|name(?:space-uri-?(?:for-prefix|from-QName)?)?|nilled|node-name|normalize-(?:space|unicode)|not|number|one-or-more|outermost|parse-(?:ietf-date|json)|path|position|(?:prefix-from-)?QName|random-number-generator|regex-group|remove|replace|resolve-(?:QName|uri)|reverse|root|round(?:-half-to-even)?|seconds-from-(?:dateTime|duration|time)|snapshot|sort|starts-with|static-base-uri|stream-available|string-?(?:join|length|to-codepoints)?|subsequence|substring-?(?:after|before)?|sum|system-property|tail|timezone-from-(?:date(?:Time)?|time)|tokenize|trace|trans(?:form|late)|true|type-available|unordered|unparsed-(?:entity|text)?-?(?:public-id|uri|available|lines)?|uri-collection|xml-to-json|years?-from-(?:date(?:Time)?|duration)|zero-or-one)\b/
      },
      {
        begin: /\blocal:/,
        end: /\(/,
        excludeEnd: true
      },
      {
        begin: /\bzip:/,
        end: /(?:zip-file|(?:xml|html|text|binary)-entry| (?:update-)?entries)\b/
      },
      {
        begin: /\b(?:util|db|functx|app|xdmp|xmldb):/,
        end: /\(/,
        excludeEnd: true
      }
    ]
  };

  const TITLE = {
    className: 'title',
    begin: /\bxquery version "[13]\.[01]"\s?(?:encoding ".+")?/,
    end: /;/
  };

  const VAR = {
    className: 'variable',
    begin: /[$][\w\-:]+/
  };

  const NUMBER = {
    className: 'number',
    begin: /(\b0[0-7_]+)|(\b0x[0-9a-fA-F_]+)|(\b[1-9][0-9_]*(\.[0-9_]+)?)|[0_]\b/,
    relevance: 0
  };

  const STRING = {
    className: 'string',
    variants: [
      {
        begin: /"/,
        end: /"/,
        contains: [
          {
            begin: /""/,
            relevance: 0
          }
        ]
      },
      {
        begin: /'/,
        end: /'/,
        contains: [
          {
            begin: /''/,
            relevance: 0
          }
        ]
      }
    ]
  };

  const ANNOTATION = {
    className: 'meta',
    begin: /%[\w\-:]+/
  };

  const COMMENT = {
    className: 'comment',
    begin: /\(:/,
    end: /:\)/,
    relevance: 10,
    contains: [
      {
        className: 'doctag',
        begin: /@\w+/
      }
    ]
  };

  // see https://www.w3.org/TR/xquery/#id-computedConstructors
  // mocha: computed_inbuilt
  // see https://www.regexpal.com/?fam=99749
  const COMPUTED = {
    beginKeywords: 'element attribute comment document processing-instruction',
    end: /\{/,
    excludeEnd: true
  };

  // mocha: direct_method
  const DIRECT = {
    begin: /<([\w._:-]+)(\s+\S*=('|").*('|"))?>/,
    end: /(\/[\w._:-]+>)/,
    subLanguage: 'xml',
    contains: [
      {
        begin: /\{/,
        end: /\}/,
        subLanguage: 'xquery'
      },
      'self'
    ]
  };

  const CONTAINS = [
    VAR,
    BUILT_IN,
    STRING,
    NUMBER,
    COMMENT,
    ANNOTATION,
    TITLE,
    COMPUTED,
    DIRECT
  ];

  return {
    name: 'XQuery',
    aliases: [
      'xpath',
      'xq'
    ],
    case_insensitive: false,
    illegal: /(proc)|(abstract)|(extends)|(until)|(#)/,
    keywords: {
      $pattern: /[a-zA-Z$][a-zA-Z0-9_:-]*/,
      keyword: KEYWORDS,
      type: TYPE,
      literal: LITERAL
    },
    contains: CONTAINS
  };
}

module.exports = xquery;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfeHF1ZXJ5LmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0EsV0FBVztBQUNYOztBQUVBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFlBQVk7QUFDWjtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0Esa0JBQWtCO0FBQ2xCLGdCQUFnQjtBQUNoQjtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL3hxdWVyeS5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKlxuTGFuZ3VhZ2U6IFhRdWVyeVxuQXV0aG9yOiBEaXJrIEtpcnN0ZW4gPGRrQGJhc2V4Lm9yZz5cbkNvbnRyaWJ1dG9yOiBEdW5jYW4gUGF0ZXJzb25cbkRlc2NyaXB0aW9uOiBTdXBwb3J0cyBYUXVlcnkgMy4xIGluY2x1ZGluZyBYUXVlcnkgVXBkYXRlIDMsIHNvIGFsc28gWFBhdGggKGFzIGl0IGlzIGEgc3VwZXJzZXQpXG5SZWZhY3RvcmVkIHRvIHByb2Nlc3MgeG1sIGNvbnN0cnVjdG9yIHN5bnRheCBhbmQgZnVuY3Rpb24tYm9kaWVzLiBBZGRlZCBtaXNzaW5nIGRhdGEtdHlwZXMsIHhwYXRoIG9wZXJhbmRzLCBpbmJ1aWx0IGZ1bmN0aW9ucywgYW5kIHF1ZXJ5IHByb2xvZ3NcbldlYnNpdGU6IGh0dHBzOi8vd3d3LnczLm9yZy9YTUwvUXVlcnkvXG5DYXRlZ29yeTogZnVuY3Rpb25hbFxuQXVkaXQ6IDIwMjBcbiovXG5cbi8qKiBAdHlwZSBMYW5ndWFnZUZuICovXG5mdW5jdGlvbiB4cXVlcnkoX2hsanMpIHtcbiAgLy8gc2VlIGh0dHBzOi8vd3d3LnczLm9yZy9UUi94cXVlcnkvI2lkLXRlcm1pbmFsLWRlbGltaXRhdGlvblxuICBjb25zdCBLRVlXT1JEUyA9XG4gICAgJ21vZHVsZSBzY2hlbWEgbmFtZXNwYWNlIGJvdW5kYXJ5LXNwYWNlIHByZXNlcnZlIG5vLXByZXNlcnZlIHN0cmlwIGRlZmF1bHQgY29sbGF0aW9uIGJhc2UtdXJpIG9yZGVyaW5nIGNvbnRleHQgZGVjaW1hbC1mb3JtYXQgZGVjaW1hbC1zZXBhcmF0b3IgY29weS1uYW1lc3BhY2VzIGVtcHR5LXNlcXVlbmNlIGV4Y2VwdCBleHBvbmVudC1zZXBhcmF0b3IgZXh0ZXJuYWwgZ3JvdXBpbmctc2VwYXJhdG9yIGluaGVyaXQgbm8taW5oZXJpdCBsYXggbWludXMtc2lnbiBwZXItbWlsbGUgcGVyY2VudCBzY2hlbWEtYXR0cmlidXRlIHNjaGVtYS1lbGVtZW50IHN0cmljdCB1bm9yZGVyZWQgemVyby1kaWdpdCAnICtcbiAgICAnZGVjbGFyZSBpbXBvcnQgb3B0aW9uIGZ1bmN0aW9uIHZhbGlkYXRlIHZhcmlhYmxlICcgK1xuICAgICdmb3IgYXQgaW4gbGV0IHdoZXJlIG9yZGVyIGdyb3VwIGJ5IHJldHVybiBpZiB0aGVuIGVsc2UgJyArXG4gICAgJ3R1bWJsaW5nIHNsaWRpbmcgd2luZG93IHN0YXJ0IHdoZW4gb25seSBlbmQgcHJldmlvdXMgbmV4dCBzdGFibGUgJyArXG4gICAgJ2FzY2VuZGluZyBkZXNjZW5kaW5nIGFsbG93aW5nIGVtcHR5IGdyZWF0ZXN0IGxlYXN0IHNvbWUgZXZlcnkgc2F0aXNmaWVzIHN3aXRjaCBjYXNlIHR5cGVzd2l0Y2ggdHJ5IGNhdGNoICcgK1xuICAgICdhbmQgb3IgdG8gdW5pb24gaW50ZXJzZWN0IGluc3RhbmNlIG9mIHRyZWF0IGFzIGNhc3RhYmxlIGNhc3QgbWFwIGFycmF5ICcgK1xuICAgICdkZWxldGUgaW5zZXJ0IGludG8gcmVwbGFjZSB2YWx1ZSByZW5hbWUgY29weSBtb2RpZnkgdXBkYXRlJztcblxuICAvLyBOb2RlIFR5cGVzIChzb3J0ZWQgYnkgaW5oZXJpdGFuY2UpXG4gIC8vIGF0b21pYyB0eXBlcyAoc29ydGVkIGJ5IGluaGVyaXRhbmNlKVxuICBjb25zdCBUWVBFID1cbiAgICAnaXRlbSBkb2N1bWVudC1ub2RlIG5vZGUgYXR0cmlidXRlIGRvY3VtZW50IGVsZW1lbnQgY29tbWVudCBuYW1lc3BhY2UgbmFtZXNwYWNlLW5vZGUgcHJvY2Vzc2luZy1pbnN0cnVjdGlvbiB0ZXh0IGNvbnN0cnVjdGlvbiAnICtcbiAgICAneHM6YW55QXRvbWljVHlwZSB4czp1bnR5cGVkQXRvbWljIHhzOmR1cmF0aW9uIHhzOnRpbWUgeHM6ZGVjaW1hbCB4czpmbG9hdCB4czpkb3VibGUgeHM6Z1llYXJNb250aCB4czpnWWVhciB4czpnTW9udGhEYXkgeHM6Z01vbnRoIHhzOmdEYXkgeHM6Ym9vbGVhbiB4czpiYXNlNjRCaW5hcnkgeHM6aGV4QmluYXJ5IHhzOmFueVVSSSB4czpRTmFtZSB4czpOT1RBVElPTiB4czpkYXRlVGltZSB4czpkYXRlVGltZVN0YW1wIHhzOmRhdGUgeHM6c3RyaW5nIHhzOm5vcm1hbGl6ZWRTdHJpbmcgeHM6dG9rZW4geHM6bGFuZ3VhZ2UgeHM6Tk1UT0tFTiB4czpOYW1lIHhzOk5DTmFtZSB4czpJRCB4czpJRFJFRiB4czpFTlRJVFkgeHM6aW50ZWdlciB4czpub25Qb3NpdGl2ZUludGVnZXIgeHM6bmVnYXRpdmVJbnRlZ2VyIHhzOmxvbmcgeHM6aW50IHhzOnNob3J0IHhzOmJ5dGUgeHM6bm9uTmVnYXRpdmVJbnRlZ2VyIHhzOnVuaXNpZ25lZExvbmcgeHM6dW5zaWduZWRJbnQgeHM6dW5zaWduZWRTaG9ydCB4czp1bnNpZ25lZEJ5dGUgeHM6cG9zaXRpdmVJbnRlZ2VyIHhzOnllYXJNb250aER1cmF0aW9uIHhzOmRheVRpbWVEdXJhdGlvbic7XG5cbiAgY29uc3QgTElURVJBTCA9XG4gICAgJ2VxIG5lIGx0IGxlIGd0IGdlIGlzICcgK1xuICAgICdzZWxmOjogY2hpbGQ6OiBkZXNjZW5kYW50OjogZGVzY2VuZGFudC1vci1zZWxmOjogYXR0cmlidXRlOjogZm9sbG93aW5nOjogZm9sbG93aW5nLXNpYmxpbmc6OiBwYXJlbnQ6OiBhbmNlc3Rvcjo6IGFuY2VzdG9yLW9yLXNlbGY6OiBwcmVjZWRpbmc6OiBwcmVjZWRpbmctc2libGluZzo6ICcgK1xuICAgICdOYU4nO1xuXG4gIC8vIGZ1bmN0aW9ucyAoVE9ETzogZmluZCByZWdleCBmb3Igb3A6IHdpdGhvdXQgYnJlYWtpbmcgYnVpbGQpXG4gIGNvbnN0IEJVSUxUX0lOID0ge1xuICAgIGNsYXNzTmFtZTogJ2J1aWx0X2luJyxcbiAgICB2YXJpYW50czogW1xuICAgICAge1xuICAgICAgICBiZWdpbjogL1xcYmFycmF5Oi8sXG4gICAgICAgIGVuZDogLyg/OmFwcGVuZHxmaWx0ZXJ8ZmxhdHRlbnxmb2xkLSg/OmxlZnR8cmlnaHQpfGZvci1lYWNoKD86LXBhaXIpP3xnZXR8aGVhZHxpbnNlcnQtYmVmb3JlfGpvaW58cHV0fHJlbW92ZXxyZXZlcnNlfHNpemV8c29ydHxzdWJhcnJheXx0YWlsKVxcYi9cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAvXFxibWFwOi8sXG4gICAgICAgIGVuZDogLyg/OmNvbnRhaW5zfGVudHJ5fGZpbmR8Zm9yLWVhY2h8Z2V0fGtleXN8bWVyZ2V8cHV0fHJlbW92ZXxzaXplKVxcYi9cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAvXFxibWF0aDovLFxuICAgICAgICBlbmQ6IC8oPzphKD86Y29zfHNpbnx0YW5bMl0/KXxjb3N8ZXhwKD86MTApP3xsb2coPzoxMCk/fHBpfHBvd3xzaW58c3FydHx0YW4pXFxiL1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC9cXGJvcDovLFxuICAgICAgICBlbmQ6IC9cXCgvLFxuICAgICAgICBleGNsdWRlRW5kOiB0cnVlXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogL1xcYmZuOi8sXG4gICAgICAgIGVuZDogL1xcKC8sXG4gICAgICAgIGV4Y2x1ZGVFbmQ6IHRydWVcbiAgICAgIH0sXG4gICAgICAvLyBkbyBub3QgaGlnaGxpZ2h0IGluYnVpbHQgc3RyaW5ncyBhcyB2YXJpYWJsZSBvciB4bWwgZWxlbWVudCBuYW1lc1xuICAgICAge1xuICAgICAgICBiZWdpbjogL1tePC8kOidcIi1dXFxiKD86YWJzfGFjY3VtdWxhdG9yLSg/OmFmdGVyfGJlZm9yZSl8YWRqdXN0LSg/OmRhdGUoPzpUaW1lKT98dGltZSktdG8tdGltZXpvbmV8YW5hbHl6ZS1zdHJpbmd8YXBwbHl8YXZhaWxhYmxlLSg/OmVudmlyb25tZW50LXZhcmlhYmxlc3xzeXN0ZW0tcHJvcGVydGllcyl8YXZnfGJhc2UtdXJpfGJvb2xlYW58Y2VpbGluZ3xjb2RlcG9pbnRzPy0oPzplcXVhbHx0by1zdHJpbmcpfGNvbGxhdGlvbi1rZXl8Y29sbGVjdGlvbnxjb21wYXJlfGNvbmNhdHxjb250YWlucyg/Oi10b2tlbik/fGNvcHktb2Z8Y291bnR8Y3VycmVudCg/Oi0pPyg/OmRhdGUoPzpUaW1lKT98dGltZXxncm91cCg/OmluZy1rZXkpP3xvdXRwdXQtdXJpfG1lcmdlLSg/Omdyb3VwfGtleSkpP2RhdGF8ZGF0ZVRpbWV8ZGF5cz8tZnJvbS0oPzpkYXRlKD86VGltZSk/fGR1cmF0aW9uKXxkZWVwLWVxdWFsfGRlZmF1bHQtKD86Y29sbGF0aW9ufGxhbmd1YWdlKXxkaXN0aW5jdC12YWx1ZXN8ZG9jdW1lbnQoPzotdXJpKT98ZG9jKD86LWF2YWlsYWJsZSk/fGVsZW1lbnQtKD86YXZhaWxhYmxlfHdpdGgtaWQpfGVtcHR5fGVuY29kZS1mb3ItdXJpfGVuZHMtd2l0aHxlbnZpcm9ubWVudC12YXJpYWJsZXxlcnJvcnxlc2NhcGUtaHRtbC11cml8ZXhhY3RseS1vbmV8ZXhpc3RzfGZhbHNlfGZpbHRlcnxmbG9vcnxmb2xkLSg/OmxlZnR8cmlnaHQpfGZvci1lYWNoKD86LXBhaXIpP3xmb3JtYXQtKD86ZGF0ZSg/OlRpbWUpP3x0aW1lfGludGVnZXJ8bnVtYmVyKXxmdW5jdGlvbi0oPzphcml0eXxhdmFpbGFibGV8bG9va3VwfG5hbWUpfGdlbmVyYXRlLWlkfGhhcy1jaGlsZHJlbnxoZWFkfGhvdXJzLWZyb20tKD86ZGF0ZVRpbWV8ZHVyYXRpb258dGltZSl8aWQoPzpyZWYpP3xpbXBsaWNpdC10aW1lem9uZXxpbi1zY29wZS1wcmVmaXhlc3xpbmRleC1vZnxpbm5lcm1vc3R8aW5zZXJ0LWJlZm9yZXxpcmktdG8tdXJpfGpzb24tKD86ZG9jfHRvLXhtbCl8a2V5fGxhbmd8bGFzdHxsb2FkLXhxdWVyeS1tb2R1bGV8bG9jYWwtbmFtZSg/Oi1mcm9tLVFOYW1lKT98KD86bG93ZXJ8dXBwZXIpLWNhc2V8bWF0Y2hlc3xtYXh8bWludXRlcy1mcm9tLSg/OmRhdGVUaW1lfGR1cmF0aW9ufHRpbWUpfG1pbnxtb250aHM/LWZyb20tKD86ZGF0ZSg/OlRpbWUpP3xkdXJhdGlvbil8bmFtZSg/OnNwYWNlLXVyaS0/KD86Zm9yLXByZWZpeHxmcm9tLVFOYW1lKT8pP3xuaWxsZWR8bm9kZS1uYW1lfG5vcm1hbGl6ZS0oPzpzcGFjZXx1bmljb2RlKXxub3R8bnVtYmVyfG9uZS1vci1tb3JlfG91dGVybW9zdHxwYXJzZS0oPzppZXRmLWRhdGV8anNvbil8cGF0aHxwb3NpdGlvbnwoPzpwcmVmaXgtZnJvbS0pP1FOYW1lfHJhbmRvbS1udW1iZXItZ2VuZXJhdG9yfHJlZ2V4LWdyb3VwfHJlbW92ZXxyZXBsYWNlfHJlc29sdmUtKD86UU5hbWV8dXJpKXxyZXZlcnNlfHJvb3R8cm91bmQoPzotaGFsZi10by1ldmVuKT98c2Vjb25kcy1mcm9tLSg/OmRhdGVUaW1lfGR1cmF0aW9ufHRpbWUpfHNuYXBzaG90fHNvcnR8c3RhcnRzLXdpdGh8c3RhdGljLWJhc2UtdXJpfHN0cmVhbS1hdmFpbGFibGV8c3RyaW5nLT8oPzpqb2lufGxlbmd0aHx0by1jb2RlcG9pbnRzKT98c3Vic2VxdWVuY2V8c3Vic3RyaW5nLT8oPzphZnRlcnxiZWZvcmUpP3xzdW18c3lzdGVtLXByb3BlcnR5fHRhaWx8dGltZXpvbmUtZnJvbS0oPzpkYXRlKD86VGltZSk/fHRpbWUpfHRva2VuaXplfHRyYWNlfHRyYW5zKD86Zm9ybXxsYXRlKXx0cnVlfHR5cGUtYXZhaWxhYmxlfHVub3JkZXJlZHx1bnBhcnNlZC0oPzplbnRpdHl8dGV4dCk/LT8oPzpwdWJsaWMtaWR8dXJpfGF2YWlsYWJsZXxsaW5lcyk/fHVyaS1jb2xsZWN0aW9ufHhtbC10by1qc29ufHllYXJzPy1mcm9tLSg/OmRhdGUoPzpUaW1lKT98ZHVyYXRpb24pfHplcm8tb3Itb25lKVxcYi9cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAvXFxibG9jYWw6LyxcbiAgICAgICAgZW5kOiAvXFwoLyxcbiAgICAgICAgZXhjbHVkZUVuZDogdHJ1ZVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC9cXGJ6aXA6LyxcbiAgICAgICAgZW5kOiAvKD86emlwLWZpbGV8KD86eG1sfGh0bWx8dGV4dHxiaW5hcnkpLWVudHJ5fCAoPzp1cGRhdGUtKT9lbnRyaWVzKVxcYi9cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAvXFxiKD86dXRpbHxkYnxmdW5jdHh8YXBwfHhkbXB8eG1sZGIpOi8sXG4gICAgICAgIGVuZDogL1xcKC8sXG4gICAgICAgIGV4Y2x1ZGVFbmQ6IHRydWVcbiAgICAgIH1cbiAgICBdXG4gIH07XG5cbiAgY29uc3QgVElUTEUgPSB7XG4gICAgY2xhc3NOYW1lOiAndGl0bGUnLFxuICAgIGJlZ2luOiAvXFxieHF1ZXJ5IHZlcnNpb24gXCJbMTNdXFwuWzAxXVwiXFxzPyg/OmVuY29kaW5nIFwiLitcIik/LyxcbiAgICBlbmQ6IC87L1xuICB9O1xuXG4gIGNvbnN0IFZBUiA9IHtcbiAgICBjbGFzc05hbWU6ICd2YXJpYWJsZScsXG4gICAgYmVnaW46IC9bJF1bXFx3XFwtOl0rL1xuICB9O1xuXG4gIGNvbnN0IE5VTUJFUiA9IHtcbiAgICBjbGFzc05hbWU6ICdudW1iZXInLFxuICAgIGJlZ2luOiAvKFxcYjBbMC03X10rKXwoXFxiMHhbMC05YS1mQS1GX10rKXwoXFxiWzEtOV1bMC05X10qKFxcLlswLTlfXSspPyl8WzBfXVxcYi8sXG4gICAgcmVsZXZhbmNlOiAwXG4gIH07XG5cbiAgY29uc3QgU1RSSU5HID0ge1xuICAgIGNsYXNzTmFtZTogJ3N0cmluZycsXG4gICAgdmFyaWFudHM6IFtcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC9cIi8sXG4gICAgICAgIGVuZDogL1wiLyxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbjogL1wiXCIvLFxuICAgICAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICAgICAgfVxuICAgICAgICBdXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogLycvLFxuICAgICAgICBlbmQ6IC8nLyxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbjogLycnLyxcbiAgICAgICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgICAgIH1cbiAgICAgICAgXVxuICAgICAgfVxuICAgIF1cbiAgfTtcblxuICBjb25zdCBBTk5PVEFUSU9OID0ge1xuICAgIGNsYXNzTmFtZTogJ21ldGEnLFxuICAgIGJlZ2luOiAvJVtcXHdcXC06XSsvXG4gIH07XG5cbiAgY29uc3QgQ09NTUVOVCA9IHtcbiAgICBjbGFzc05hbWU6ICdjb21tZW50JyxcbiAgICBiZWdpbjogL1xcKDovLFxuICAgIGVuZDogLzpcXCkvLFxuICAgIHJlbGV2YW5jZTogMTAsXG4gICAgY29udGFpbnM6IFtcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnZG9jdGFnJyxcbiAgICAgICAgYmVnaW46IC9AXFx3Ky9cbiAgICAgIH1cbiAgICBdXG4gIH07XG5cbiAgLy8gc2VlIGh0dHBzOi8vd3d3LnczLm9yZy9UUi94cXVlcnkvI2lkLWNvbXB1dGVkQ29uc3RydWN0b3JzXG4gIC8vIG1vY2hhOiBjb21wdXRlZF9pbmJ1aWx0XG4gIC8vIHNlZSBodHRwczovL3d3dy5yZWdleHBhbC5jb20vP2ZhbT05OTc0OVxuICBjb25zdCBDT01QVVRFRCA9IHtcbiAgICBiZWdpbktleXdvcmRzOiAnZWxlbWVudCBhdHRyaWJ1dGUgY29tbWVudCBkb2N1bWVudCBwcm9jZXNzaW5nLWluc3RydWN0aW9uJyxcbiAgICBlbmQ6IC9cXHsvLFxuICAgIGV4Y2x1ZGVFbmQ6IHRydWVcbiAgfTtcblxuICAvLyBtb2NoYTogZGlyZWN0X21ldGhvZFxuICBjb25zdCBESVJFQ1QgPSB7XG4gICAgYmVnaW46IC88KFtcXHcuXzotXSspKFxccytcXFMqPSgnfFwiKS4qKCd8XCIpKT8+LyxcbiAgICBlbmQ6IC8oXFwvW1xcdy5fOi1dKz4pLyxcbiAgICBzdWJMYW5ndWFnZTogJ3htbCcsXG4gICAgY29udGFpbnM6IFtcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC9cXHsvLFxuICAgICAgICBlbmQ6IC9cXH0vLFxuICAgICAgICBzdWJMYW5ndWFnZTogJ3hxdWVyeSdcbiAgICAgIH0sXG4gICAgICAnc2VsZidcbiAgICBdXG4gIH07XG5cbiAgY29uc3QgQ09OVEFJTlMgPSBbXG4gICAgVkFSLFxuICAgIEJVSUxUX0lOLFxuICAgIFNUUklORyxcbiAgICBOVU1CRVIsXG4gICAgQ09NTUVOVCxcbiAgICBBTk5PVEFUSU9OLFxuICAgIFRJVExFLFxuICAgIENPTVBVVEVELFxuICAgIERJUkVDVFxuICBdO1xuXG4gIHJldHVybiB7XG4gICAgbmFtZTogJ1hRdWVyeScsXG4gICAgYWxpYXNlczogW1xuICAgICAgJ3hwYXRoJyxcbiAgICAgICd4cSdcbiAgICBdLFxuICAgIGNhc2VfaW5zZW5zaXRpdmU6IGZhbHNlLFxuICAgIGlsbGVnYWw6IC8ocHJvYyl8KGFic3RyYWN0KXwoZXh0ZW5kcyl8KHVudGlsKXwoIykvLFxuICAgIGtleXdvcmRzOiB7XG4gICAgICAkcGF0dGVybjogL1thLXpBLVokXVthLXpBLVowLTlfOi1dKi8sXG4gICAgICBrZXl3b3JkOiBLRVlXT1JEUyxcbiAgICAgIHR5cGU6IFRZUEUsXG4gICAgICBsaXRlcmFsOiBMSVRFUkFMXG4gICAgfSxcbiAgICBjb250YWluczogQ09OVEFJTlNcbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSB4cXVlcnk7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=