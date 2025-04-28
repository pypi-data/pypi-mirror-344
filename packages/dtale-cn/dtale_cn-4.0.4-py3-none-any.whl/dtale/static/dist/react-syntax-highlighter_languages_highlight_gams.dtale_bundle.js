(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_gams"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/gams.js":
/*!***********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/gams.js ***!
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
 * @param {RegExp | string } re
 * @returns {string}
 */
function anyNumberOfTimes(re) {
  return concat('(', re, ')*');
}

/**
 * @param {...(RegExp | string) } args
 * @returns {string}
 */
function concat(...args) {
  const joined = args.map((x) => source(x)).join("");
  return joined;
}

/** @type LanguageFn */
function gams(hljs) {
  const KEYWORDS = {
    keyword:
      'abort acronym acronyms alias all and assign binary card diag display ' +
      'else eq file files for free ge gt if integer le loop lt maximizing ' +
      'minimizing model models ne negative no not option options or ord ' +
      'positive prod put putpage puttl repeat sameas semicont semiint smax ' +
      'smin solve sos1 sos2 sum system table then until using while xor yes',
    literal:
      'eps inf na',
    built_in:
      'abs arccos arcsin arctan arctan2 Beta betaReg binomial ceil centropy ' +
      'cos cosh cvPower div div0 eDist entropy errorf execSeed exp fact ' +
      'floor frac gamma gammaReg log logBeta logGamma log10 log2 mapVal max ' +
      'min mod ncpCM ncpF ncpVUpow ncpVUsin normal pi poly power ' +
      'randBinomial randLinear randTriangle round rPower sigmoid sign ' +
      'signPower sin sinh slexp sllog10 slrec sqexp sqlog10 sqr sqrec sqrt ' +
      'tan tanh trunc uniform uniformInt vcPower bool_and bool_eqv bool_imp ' +
      'bool_not bool_or bool_xor ifThen rel_eq rel_ge rel_gt rel_le rel_lt ' +
      'rel_ne gday gdow ghour gleap gmillisec gminute gmonth gsecond gyear ' +
      'jdate jnow jstart jtime errorLevel execError gamsRelease gamsVersion ' +
      'handleCollect handleDelete handleStatus handleSubmit heapFree ' +
      'heapLimit heapSize jobHandle jobKill jobStatus jobTerminate ' +
      'licenseLevel licenseStatus maxExecError sleep timeClose timeComp ' +
      'timeElapsed timeExec timeStart'
  };
  const PARAMS = {
    className: 'params',
    begin: /\(/,
    end: /\)/,
    excludeBegin: true,
    excludeEnd: true
  };
  const SYMBOLS = {
    className: 'symbol',
    variants: [
      {
        begin: /=[lgenxc]=/
      },
      {
        begin: /\$/
      }
    ]
  };
  const QSTR = { // One-line quoted comment string
    className: 'comment',
    variants: [
      {
        begin: '\'',
        end: '\''
      },
      {
        begin: '"',
        end: '"'
      }
    ],
    illegal: '\\n',
    contains: [hljs.BACKSLASH_ESCAPE]
  };
  const ASSIGNMENT = {
    begin: '/',
    end: '/',
    keywords: KEYWORDS,
    contains: [
      QSTR,
      hljs.C_LINE_COMMENT_MODE,
      hljs.C_BLOCK_COMMENT_MODE,
      hljs.QUOTE_STRING_MODE,
      hljs.APOS_STRING_MODE,
      hljs.C_NUMBER_MODE
    ]
  };
  const COMMENT_WORD = /[a-z0-9&#*=?@\\><:,()$[\]_.{}!+%^-]+/;
  const DESCTEXT = { // Parameter/set/variable description text
    begin: /[a-z][a-z0-9_]*(\([a-z0-9_, ]*\))?[ \t]+/,
    excludeBegin: true,
    end: '$',
    endsWithParent: true,
    contains: [
      QSTR,
      ASSIGNMENT,
      {
        className: 'comment',
        // one comment word, then possibly more
        begin: concat(
          COMMENT_WORD,
          // [ ] because \s would be too broad (matching newlines)
          anyNumberOfTimes(concat(/[ ]+/, COMMENT_WORD))
        ),
        relevance: 0
      }
    ]
  };

  return {
    name: 'GAMS',
    aliases: ['gms'],
    case_insensitive: true,
    keywords: KEYWORDS,
    contains: [
      hljs.COMMENT(/^\$ontext/, /^\$offtext/),
      {
        className: 'meta',
        begin: '^\\$[a-z0-9]+',
        end: '$',
        returnBegin: true,
        contains: [
          {
            className: 'meta-keyword',
            begin: '^\\$[a-z0-9]+'
          }
        ]
      },
      hljs.COMMENT('^\\*', '$'),
      hljs.C_LINE_COMMENT_MODE,
      hljs.C_BLOCK_COMMENT_MODE,
      hljs.QUOTE_STRING_MODE,
      hljs.APOS_STRING_MODE,
      // Declarations
      {
        beginKeywords:
          'set sets parameter parameters variable variables ' +
          'scalar scalars equation equations',
        end: ';',
        contains: [
          hljs.COMMENT('^\\*', '$'),
          hljs.C_LINE_COMMENT_MODE,
          hljs.C_BLOCK_COMMENT_MODE,
          hljs.QUOTE_STRING_MODE,
          hljs.APOS_STRING_MODE,
          ASSIGNMENT,
          DESCTEXT
        ]
      },
      { // table environment
        beginKeywords: 'table',
        end: ';',
        returnBegin: true,
        contains: [
          { // table header row
            beginKeywords: 'table',
            end: '$',
            contains: [DESCTEXT]
          },
          hljs.COMMENT('^\\*', '$'),
          hljs.C_LINE_COMMENT_MODE,
          hljs.C_BLOCK_COMMENT_MODE,
          hljs.QUOTE_STRING_MODE,
          hljs.APOS_STRING_MODE,
          hljs.C_NUMBER_MODE
          // Table does not contain DESCTEXT or ASSIGNMENT
        ]
      },
      // Function definitions
      {
        className: 'function',
        begin: /^[a-z][a-z0-9_,\-+' ()$]+\.{2}/,
        returnBegin: true,
        contains: [
          { // Function title
            className: 'title',
            begin: /^[a-z0-9_]+/
          },
          PARAMS,
          SYMBOLS
        ]
      },
      hljs.C_NUMBER_MODE,
      SYMBOLS
    ]
  };
}

module.exports = gams;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfZ2Ftcy5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBLFdBQVcsUUFBUTtBQUNuQixhQUFhO0FBQ2I7O0FBRUE7QUFDQSxXQUFXLGtCQUFrQjtBQUM3QixhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTs7QUFFQTtBQUNBLFdBQVcsa0JBQWtCO0FBQzdCLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBLFdBQVcsdUJBQXVCO0FBQ2xDLGFBQWE7QUFDYjtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsaUJBQWlCO0FBQ2pCO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EscURBQXFEO0FBQ3JELHFCQUFxQjtBQUNyQjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxlQUFlO0FBQ2Y7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQLFFBQVE7QUFDUjtBQUNBLGVBQWU7QUFDZjtBQUNBO0FBQ0EsWUFBWTtBQUNaO0FBQ0E7QUFDQTtBQUNBLFdBQVc7QUFDWDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLDRDQUE0QyxFQUFFO0FBQzlDO0FBQ0E7QUFDQSxZQUFZO0FBQ1o7QUFDQTtBQUNBLFdBQVc7QUFDWDtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvZ2Ftcy5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKipcbiAqIEBwYXJhbSB7c3RyaW5nfSB2YWx1ZVxuICogQHJldHVybnMge1JlZ0V4cH1cbiAqICovXG5cbi8qKlxuICogQHBhcmFtIHtSZWdFeHAgfCBzdHJpbmcgfSByZVxuICogQHJldHVybnMge3N0cmluZ31cbiAqL1xuZnVuY3Rpb24gc291cmNlKHJlKSB7XG4gIGlmICghcmUpIHJldHVybiBudWxsO1xuICBpZiAodHlwZW9mIHJlID09PSBcInN0cmluZ1wiKSByZXR1cm4gcmU7XG5cbiAgcmV0dXJuIHJlLnNvdXJjZTtcbn1cblxuLyoqXG4gKiBAcGFyYW0ge1JlZ0V4cCB8IHN0cmluZyB9IHJlXG4gKiBAcmV0dXJucyB7c3RyaW5nfVxuICovXG5mdW5jdGlvbiBhbnlOdW1iZXJPZlRpbWVzKHJlKSB7XG4gIHJldHVybiBjb25jYXQoJygnLCByZSwgJykqJyk7XG59XG5cbi8qKlxuICogQHBhcmFtIHsuLi4oUmVnRXhwIHwgc3RyaW5nKSB9IGFyZ3NcbiAqIEByZXR1cm5zIHtzdHJpbmd9XG4gKi9cbmZ1bmN0aW9uIGNvbmNhdCguLi5hcmdzKSB7XG4gIGNvbnN0IGpvaW5lZCA9IGFyZ3MubWFwKCh4KSA9PiBzb3VyY2UoeCkpLmpvaW4oXCJcIik7XG4gIHJldHVybiBqb2luZWQ7XG59XG5cbi8qKiBAdHlwZSBMYW5ndWFnZUZuICovXG5mdW5jdGlvbiBnYW1zKGhsanMpIHtcbiAgY29uc3QgS0VZV09SRFMgPSB7XG4gICAga2V5d29yZDpcbiAgICAgICdhYm9ydCBhY3JvbnltIGFjcm9ueW1zIGFsaWFzIGFsbCBhbmQgYXNzaWduIGJpbmFyeSBjYXJkIGRpYWcgZGlzcGxheSAnICtcbiAgICAgICdlbHNlIGVxIGZpbGUgZmlsZXMgZm9yIGZyZWUgZ2UgZ3QgaWYgaW50ZWdlciBsZSBsb29wIGx0IG1heGltaXppbmcgJyArXG4gICAgICAnbWluaW1pemluZyBtb2RlbCBtb2RlbHMgbmUgbmVnYXRpdmUgbm8gbm90IG9wdGlvbiBvcHRpb25zIG9yIG9yZCAnICtcbiAgICAgICdwb3NpdGl2ZSBwcm9kIHB1dCBwdXRwYWdlIHB1dHRsIHJlcGVhdCBzYW1lYXMgc2VtaWNvbnQgc2VtaWludCBzbWF4ICcgK1xuICAgICAgJ3NtaW4gc29sdmUgc29zMSBzb3MyIHN1bSBzeXN0ZW0gdGFibGUgdGhlbiB1bnRpbCB1c2luZyB3aGlsZSB4b3IgeWVzJyxcbiAgICBsaXRlcmFsOlxuICAgICAgJ2VwcyBpbmYgbmEnLFxuICAgIGJ1aWx0X2luOlxuICAgICAgJ2FicyBhcmNjb3MgYXJjc2luIGFyY3RhbiBhcmN0YW4yIEJldGEgYmV0YVJlZyBiaW5vbWlhbCBjZWlsIGNlbnRyb3B5ICcgK1xuICAgICAgJ2NvcyBjb3NoIGN2UG93ZXIgZGl2IGRpdjAgZURpc3QgZW50cm9weSBlcnJvcmYgZXhlY1NlZWQgZXhwIGZhY3QgJyArXG4gICAgICAnZmxvb3IgZnJhYyBnYW1tYSBnYW1tYVJlZyBsb2cgbG9nQmV0YSBsb2dHYW1tYSBsb2cxMCBsb2cyIG1hcFZhbCBtYXggJyArXG4gICAgICAnbWluIG1vZCBuY3BDTSBuY3BGIG5jcFZVcG93IG5jcFZVc2luIG5vcm1hbCBwaSBwb2x5IHBvd2VyICcgK1xuICAgICAgJ3JhbmRCaW5vbWlhbCByYW5kTGluZWFyIHJhbmRUcmlhbmdsZSByb3VuZCByUG93ZXIgc2lnbW9pZCBzaWduICcgK1xuICAgICAgJ3NpZ25Qb3dlciBzaW4gc2luaCBzbGV4cCBzbGxvZzEwIHNscmVjIHNxZXhwIHNxbG9nMTAgc3FyIHNxcmVjIHNxcnQgJyArXG4gICAgICAndGFuIHRhbmggdHJ1bmMgdW5pZm9ybSB1bmlmb3JtSW50IHZjUG93ZXIgYm9vbF9hbmQgYm9vbF9lcXYgYm9vbF9pbXAgJyArXG4gICAgICAnYm9vbF9ub3QgYm9vbF9vciBib29sX3hvciBpZlRoZW4gcmVsX2VxIHJlbF9nZSByZWxfZ3QgcmVsX2xlIHJlbF9sdCAnICtcbiAgICAgICdyZWxfbmUgZ2RheSBnZG93IGdob3VyIGdsZWFwIGdtaWxsaXNlYyBnbWludXRlIGdtb250aCBnc2Vjb25kIGd5ZWFyICcgK1xuICAgICAgJ2pkYXRlIGpub3cganN0YXJ0IGp0aW1lIGVycm9yTGV2ZWwgZXhlY0Vycm9yIGdhbXNSZWxlYXNlIGdhbXNWZXJzaW9uICcgK1xuICAgICAgJ2hhbmRsZUNvbGxlY3QgaGFuZGxlRGVsZXRlIGhhbmRsZVN0YXR1cyBoYW5kbGVTdWJtaXQgaGVhcEZyZWUgJyArXG4gICAgICAnaGVhcExpbWl0IGhlYXBTaXplIGpvYkhhbmRsZSBqb2JLaWxsIGpvYlN0YXR1cyBqb2JUZXJtaW5hdGUgJyArXG4gICAgICAnbGljZW5zZUxldmVsIGxpY2Vuc2VTdGF0dXMgbWF4RXhlY0Vycm9yIHNsZWVwIHRpbWVDbG9zZSB0aW1lQ29tcCAnICtcbiAgICAgICd0aW1lRWxhcHNlZCB0aW1lRXhlYyB0aW1lU3RhcnQnXG4gIH07XG4gIGNvbnN0IFBBUkFNUyA9IHtcbiAgICBjbGFzc05hbWU6ICdwYXJhbXMnLFxuICAgIGJlZ2luOiAvXFwoLyxcbiAgICBlbmQ6IC9cXCkvLFxuICAgIGV4Y2x1ZGVCZWdpbjogdHJ1ZSxcbiAgICBleGNsdWRlRW5kOiB0cnVlXG4gIH07XG4gIGNvbnN0IFNZTUJPTFMgPSB7XG4gICAgY2xhc3NOYW1lOiAnc3ltYm9sJyxcbiAgICB2YXJpYW50czogW1xuICAgICAge1xuICAgICAgICBiZWdpbjogLz1bbGdlbnhjXT0vXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogL1xcJC9cbiAgICAgIH1cbiAgICBdXG4gIH07XG4gIGNvbnN0IFFTVFIgPSB7IC8vIE9uZS1saW5lIHF1b3RlZCBjb21tZW50IHN0cmluZ1xuICAgIGNsYXNzTmFtZTogJ2NvbW1lbnQnLFxuICAgIHZhcmlhbnRzOiBbXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnXFwnJyxcbiAgICAgICAgZW5kOiAnXFwnJ1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICdcIicsXG4gICAgICAgIGVuZDogJ1wiJ1xuICAgICAgfVxuICAgIF0sXG4gICAgaWxsZWdhbDogJ1xcXFxuJyxcbiAgICBjb250YWluczogW2hsanMuQkFDS1NMQVNIX0VTQ0FQRV1cbiAgfTtcbiAgY29uc3QgQVNTSUdOTUVOVCA9IHtcbiAgICBiZWdpbjogJy8nLFxuICAgIGVuZDogJy8nLFxuICAgIGtleXdvcmRzOiBLRVlXT1JEUyxcbiAgICBjb250YWluczogW1xuICAgICAgUVNUUixcbiAgICAgIGhsanMuQ19MSU5FX0NPTU1FTlRfTU9ERSxcbiAgICAgIGhsanMuQ19CTE9DS19DT01NRU5UX01PREUsXG4gICAgICBobGpzLlFVT1RFX1NUUklOR19NT0RFLFxuICAgICAgaGxqcy5BUE9TX1NUUklOR19NT0RFLFxuICAgICAgaGxqcy5DX05VTUJFUl9NT0RFXG4gICAgXVxuICB9O1xuICBjb25zdCBDT01NRU5UX1dPUkQgPSAvW2EtejAtOSYjKj0/QFxcXFw+PDosKCkkW1xcXV8ue30hKyVeLV0rLztcbiAgY29uc3QgREVTQ1RFWFQgPSB7IC8vIFBhcmFtZXRlci9zZXQvdmFyaWFibGUgZGVzY3JpcHRpb24gdGV4dFxuICAgIGJlZ2luOiAvW2Etel1bYS16MC05X10qKFxcKFthLXowLTlfLCBdKlxcKSk/WyBcXHRdKy8sXG4gICAgZXhjbHVkZUJlZ2luOiB0cnVlLFxuICAgIGVuZDogJyQnLFxuICAgIGVuZHNXaXRoUGFyZW50OiB0cnVlLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBRU1RSLFxuICAgICAgQVNTSUdOTUVOVCxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnY29tbWVudCcsXG4gICAgICAgIC8vIG9uZSBjb21tZW50IHdvcmQsIHRoZW4gcG9zc2libHkgbW9yZVxuICAgICAgICBiZWdpbjogY29uY2F0KFxuICAgICAgICAgIENPTU1FTlRfV09SRCxcbiAgICAgICAgICAvLyBbIF0gYmVjYXVzZSBcXHMgd291bGQgYmUgdG9vIGJyb2FkIChtYXRjaGluZyBuZXdsaW5lcylcbiAgICAgICAgICBhbnlOdW1iZXJPZlRpbWVzKGNvbmNhdCgvWyBdKy8sIENPTU1FTlRfV09SRCkpXG4gICAgICAgICksXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfVxuICAgIF1cbiAgfTtcblxuICByZXR1cm4ge1xuICAgIG5hbWU6ICdHQU1TJyxcbiAgICBhbGlhc2VzOiBbJ2dtcyddLFxuICAgIGNhc2VfaW5zZW5zaXRpdmU6IHRydWUsXG4gICAga2V5d29yZHM6IEtFWVdPUkRTLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBobGpzLkNPTU1FTlQoL15cXCRvbnRleHQvLCAvXlxcJG9mZnRleHQvKSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnbWV0YScsXG4gICAgICAgIGJlZ2luOiAnXlxcXFwkW2EtejAtOV0rJyxcbiAgICAgICAgZW5kOiAnJCcsXG4gICAgICAgIHJldHVybkJlZ2luOiB0cnVlLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIGNsYXNzTmFtZTogJ21ldGEta2V5d29yZCcsXG4gICAgICAgICAgICBiZWdpbjogJ15cXFxcJFthLXowLTldKydcbiAgICAgICAgICB9XG4gICAgICAgIF1cbiAgICAgIH0sXG4gICAgICBobGpzLkNPTU1FTlQoJ15cXFxcKicsICckJyksXG4gICAgICBobGpzLkNfTElORV9DT01NRU5UX01PREUsXG4gICAgICBobGpzLkNfQkxPQ0tfQ09NTUVOVF9NT0RFLFxuICAgICAgaGxqcy5RVU9URV9TVFJJTkdfTU9ERSxcbiAgICAgIGhsanMuQVBPU19TVFJJTkdfTU9ERSxcbiAgICAgIC8vIERlY2xhcmF0aW9uc1xuICAgICAge1xuICAgICAgICBiZWdpbktleXdvcmRzOlxuICAgICAgICAgICdzZXQgc2V0cyBwYXJhbWV0ZXIgcGFyYW1ldGVycyB2YXJpYWJsZSB2YXJpYWJsZXMgJyArXG4gICAgICAgICAgJ3NjYWxhciBzY2FsYXJzIGVxdWF0aW9uIGVxdWF0aW9ucycsXG4gICAgICAgIGVuZDogJzsnLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIGhsanMuQ09NTUVOVCgnXlxcXFwqJywgJyQnKSxcbiAgICAgICAgICBobGpzLkNfTElORV9DT01NRU5UX01PREUsXG4gICAgICAgICAgaGxqcy5DX0JMT0NLX0NPTU1FTlRfTU9ERSxcbiAgICAgICAgICBobGpzLlFVT1RFX1NUUklOR19NT0RFLFxuICAgICAgICAgIGhsanMuQVBPU19TVFJJTkdfTU9ERSxcbiAgICAgICAgICBBU1NJR05NRU5ULFxuICAgICAgICAgIERFU0NURVhUXG4gICAgICAgIF1cbiAgICAgIH0sXG4gICAgICB7IC8vIHRhYmxlIGVudmlyb25tZW50XG4gICAgICAgIGJlZ2luS2V5d29yZHM6ICd0YWJsZScsXG4gICAgICAgIGVuZDogJzsnLFxuICAgICAgICByZXR1cm5CZWdpbjogdHJ1ZSxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICB7IC8vIHRhYmxlIGhlYWRlciByb3dcbiAgICAgICAgICAgIGJlZ2luS2V5d29yZHM6ICd0YWJsZScsXG4gICAgICAgICAgICBlbmQ6ICckJyxcbiAgICAgICAgICAgIGNvbnRhaW5zOiBbREVTQ1RFWFRdXG4gICAgICAgICAgfSxcbiAgICAgICAgICBobGpzLkNPTU1FTlQoJ15cXFxcKicsICckJyksXG4gICAgICAgICAgaGxqcy5DX0xJTkVfQ09NTUVOVF9NT0RFLFxuICAgICAgICAgIGhsanMuQ19CTE9DS19DT01NRU5UX01PREUsXG4gICAgICAgICAgaGxqcy5RVU9URV9TVFJJTkdfTU9ERSxcbiAgICAgICAgICBobGpzLkFQT1NfU1RSSU5HX01PREUsXG4gICAgICAgICAgaGxqcy5DX05VTUJFUl9NT0RFXG4gICAgICAgICAgLy8gVGFibGUgZG9lcyBub3QgY29udGFpbiBERVNDVEVYVCBvciBBU1NJR05NRU5UXG4gICAgICAgIF1cbiAgICAgIH0sXG4gICAgICAvLyBGdW5jdGlvbiBkZWZpbml0aW9uc1xuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdmdW5jdGlvbicsXG4gICAgICAgIGJlZ2luOiAvXlthLXpdW2EtejAtOV8sXFwtKycgKCkkXStcXC57Mn0vLFxuICAgICAgICByZXR1cm5CZWdpbjogdHJ1ZSxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICB7IC8vIEZ1bmN0aW9uIHRpdGxlXG4gICAgICAgICAgICBjbGFzc05hbWU6ICd0aXRsZScsXG4gICAgICAgICAgICBiZWdpbjogL15bYS16MC05X10rL1xuICAgICAgICAgIH0sXG4gICAgICAgICAgUEFSQU1TLFxuICAgICAgICAgIFNZTUJPTFNcbiAgICAgICAgXVxuICAgICAgfSxcbiAgICAgIGhsanMuQ19OVU1CRVJfTU9ERSxcbiAgICAgIFNZTUJPTFNcbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gZ2FtcztcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==