(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_scheme"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/scheme.js":
/*!*************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/scheme.js ***!
  \*************************************************************************************************/
/***/ ((module) => {

/*
Language: Scheme
Description: Scheme is a programming language in the Lisp family.
             (keywords based on http://community.schemewiki.org/?scheme-keywords)
Author: JP Verkamp <me@jverkamp.com>
Contributors: Ivan Sagalaev <maniac@softwaremaniacs.org>
Origin: clojure.js
Website: http://community.schemewiki.org/?what-is-scheme
Category: lisp
*/

function scheme(hljs) {
  const SCHEME_IDENT_RE = '[^\\(\\)\\[\\]\\{\\}",\'`;#|\\\\\\s]+';
  const SCHEME_SIMPLE_NUMBER_RE = '(-|\\+)?\\d+([./]\\d+)?';
  const SCHEME_COMPLEX_NUMBER_RE = SCHEME_SIMPLE_NUMBER_RE + '[+\\-]' + SCHEME_SIMPLE_NUMBER_RE + 'i';
  const KEYWORDS = {
    $pattern: SCHEME_IDENT_RE,
    'builtin-name':
      'case-lambda call/cc class define-class exit-handler field import ' +
      'inherit init-field interface let*-values let-values let/ec mixin ' +
      'opt-lambda override protect provide public rename require ' +
      'require-for-syntax syntax syntax-case syntax-error unit/sig unless ' +
      'when with-syntax and begin call-with-current-continuation ' +
      'call-with-input-file call-with-output-file case cond define ' +
      'define-syntax delay do dynamic-wind else for-each if lambda let let* ' +
      'let-syntax letrec letrec-syntax map or syntax-rules \' * + , ,@ - ... / ' +
      '; < <= = => > >= ` abs acos angle append apply asin assoc assq assv atan ' +
      'boolean? caar cadr call-with-input-file call-with-output-file ' +
      'call-with-values car cdddar cddddr cdr ceiling char->integer ' +
      'char-alphabetic? char-ci<=? char-ci<? char-ci=? char-ci>=? char-ci>? ' +
      'char-downcase char-lower-case? char-numeric? char-ready? char-upcase ' +
      'char-upper-case? char-whitespace? char<=? char<? char=? char>=? char>? ' +
      'char? close-input-port close-output-port complex? cons cos ' +
      'current-input-port current-output-port denominator display eof-object? ' +
      'eq? equal? eqv? eval even? exact->inexact exact? exp expt floor ' +
      'force gcd imag-part inexact->exact inexact? input-port? integer->char ' +
      'integer? interaction-environment lcm length list list->string ' +
      'list->vector list-ref list-tail list? load log magnitude make-polar ' +
      'make-rectangular make-string make-vector max member memq memv min ' +
      'modulo negative? newline not null-environment null? number->string ' +
      'number? numerator odd? open-input-file open-output-file output-port? ' +
      'pair? peek-char port? positive? procedure? quasiquote quote quotient ' +
      'rational? rationalize read read-char real-part real? remainder reverse ' +
      'round scheme-report-environment set! set-car! set-cdr! sin sqrt string ' +
      'string->list string->number string->symbol string-append string-ci<=? ' +
      'string-ci<? string-ci=? string-ci>=? string-ci>? string-copy ' +
      'string-fill! string-length string-ref string-set! string<=? string<? ' +
      'string=? string>=? string>? string? substring symbol->string symbol? ' +
      'tan transcript-off transcript-on truncate values vector ' +
      'vector->list vector-fill! vector-length vector-ref vector-set! ' +
      'with-input-from-file with-output-to-file write write-char zero?'
  };

  const LITERAL = {
    className: 'literal',
    begin: '(#t|#f|#\\\\' + SCHEME_IDENT_RE + '|#\\\\.)'
  };

  const NUMBER = {
    className: 'number',
    variants: [
      {
        begin: SCHEME_SIMPLE_NUMBER_RE,
        relevance: 0
      },
      {
        begin: SCHEME_COMPLEX_NUMBER_RE,
        relevance: 0
      },
      {
        begin: '#b[0-1]+(/[0-1]+)?'
      },
      {
        begin: '#o[0-7]+(/[0-7]+)?'
      },
      {
        begin: '#x[0-9a-f]+(/[0-9a-f]+)?'
      }
    ]
  };

  const STRING = hljs.QUOTE_STRING_MODE;

  const COMMENT_MODES = [
    hljs.COMMENT(
      ';',
      '$',
      {
        relevance: 0
      }
    ),
    hljs.COMMENT('#\\|', '\\|#')
  ];

  const IDENT = {
    begin: SCHEME_IDENT_RE,
    relevance: 0
  };

  const QUOTED_IDENT = {
    className: 'symbol',
    begin: '\'' + SCHEME_IDENT_RE
  };

  const BODY = {
    endsWithParent: true,
    relevance: 0
  };

  const QUOTED_LIST = {
    variants: [
      {
        begin: /'/
      },
      {
        begin: '`'
      }
    ],
    contains: [
      {
        begin: '\\(',
        end: '\\)',
        contains: [
          'self',
          LITERAL,
          STRING,
          NUMBER,
          IDENT,
          QUOTED_IDENT
        ]
      }
    ]
  };

  const NAME = {
    className: 'name',
    relevance: 0,
    begin: SCHEME_IDENT_RE,
    keywords: KEYWORDS
  };

  const LAMBDA = {
    begin: /lambda/,
    endsWithParent: true,
    returnBegin: true,
    contains: [
      NAME,
      {
        endsParent: true,
        variants: [
          {
            begin: /\(/,
            end: /\)/
          },
          {
            begin: /\[/,
            end: /\]/
          }
        ],
        contains: [ IDENT ]
      }
    ]
  };

  const LIST = {
    variants: [
      {
        begin: '\\(',
        end: '\\)'
      },
      {
        begin: '\\[',
        end: '\\]'
      }
    ],
    contains: [
      LAMBDA,
      NAME,
      BODY
    ]
  };

  BODY.contains = [
    LITERAL,
    NUMBER,
    STRING,
    IDENT,
    QUOTED_IDENT,
    QUOTED_LIST,
    LIST
  ].concat(COMMENT_MODES);

  return {
    name: 'Scheme',
    illegal: /\S/,
    contains: [
      hljs.SHEBANG(),
      NUMBER,
      STRING,
      QUOTED_IDENT,
      QUOTED_LIST,
      LIST
    ].concat(COMMENT_MODES)
  };
}

module.exports = scheme;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfc2NoZW1lLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0EsNENBQTRDLEdBQUcsTUFBTTtBQUNyRDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFNBQVM7QUFDVDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBOztBQUVBO0FBQ0E7QUFDQSxRQUFRO0FBQ1I7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFdBQVc7QUFDWDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvc2NoZW1lLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogU2NoZW1lXG5EZXNjcmlwdGlvbjogU2NoZW1lIGlzIGEgcHJvZ3JhbW1pbmcgbGFuZ3VhZ2UgaW4gdGhlIExpc3AgZmFtaWx5LlxuICAgICAgICAgICAgIChrZXl3b3JkcyBiYXNlZCBvbiBodHRwOi8vY29tbXVuaXR5LnNjaGVtZXdpa2kub3JnLz9zY2hlbWUta2V5d29yZHMpXG5BdXRob3I6IEpQIFZlcmthbXAgPG1lQGp2ZXJrYW1wLmNvbT5cbkNvbnRyaWJ1dG9yczogSXZhbiBTYWdhbGFldiA8bWFuaWFjQHNvZnR3YXJlbWFuaWFjcy5vcmc+XG5PcmlnaW46IGNsb2p1cmUuanNcbldlYnNpdGU6IGh0dHA6Ly9jb21tdW5pdHkuc2NoZW1ld2lraS5vcmcvP3doYXQtaXMtc2NoZW1lXG5DYXRlZ29yeTogbGlzcFxuKi9cblxuZnVuY3Rpb24gc2NoZW1lKGhsanMpIHtcbiAgY29uc3QgU0NIRU1FX0lERU5UX1JFID0gJ1teXFxcXChcXFxcKVxcXFxbXFxcXF1cXFxce1xcXFx9XCIsXFwnYDsjfFxcXFxcXFxcXFxcXHNdKyc7XG4gIGNvbnN0IFNDSEVNRV9TSU1QTEVfTlVNQkVSX1JFID0gJygtfFxcXFwrKT9cXFxcZCsoWy4vXVxcXFxkKyk/JztcbiAgY29uc3QgU0NIRU1FX0NPTVBMRVhfTlVNQkVSX1JFID0gU0NIRU1FX1NJTVBMRV9OVU1CRVJfUkUgKyAnWytcXFxcLV0nICsgU0NIRU1FX1NJTVBMRV9OVU1CRVJfUkUgKyAnaSc7XG4gIGNvbnN0IEtFWVdPUkRTID0ge1xuICAgICRwYXR0ZXJuOiBTQ0hFTUVfSURFTlRfUkUsXG4gICAgJ2J1aWx0aW4tbmFtZSc6XG4gICAgICAnY2FzZS1sYW1iZGEgY2FsbC9jYyBjbGFzcyBkZWZpbmUtY2xhc3MgZXhpdC1oYW5kbGVyIGZpZWxkIGltcG9ydCAnICtcbiAgICAgICdpbmhlcml0IGluaXQtZmllbGQgaW50ZXJmYWNlIGxldCotdmFsdWVzIGxldC12YWx1ZXMgbGV0L2VjIG1peGluICcgK1xuICAgICAgJ29wdC1sYW1iZGEgb3ZlcnJpZGUgcHJvdGVjdCBwcm92aWRlIHB1YmxpYyByZW5hbWUgcmVxdWlyZSAnICtcbiAgICAgICdyZXF1aXJlLWZvci1zeW50YXggc3ludGF4IHN5bnRheC1jYXNlIHN5bnRheC1lcnJvciB1bml0L3NpZyB1bmxlc3MgJyArXG4gICAgICAnd2hlbiB3aXRoLXN5bnRheCBhbmQgYmVnaW4gY2FsbC13aXRoLWN1cnJlbnQtY29udGludWF0aW9uICcgK1xuICAgICAgJ2NhbGwtd2l0aC1pbnB1dC1maWxlIGNhbGwtd2l0aC1vdXRwdXQtZmlsZSBjYXNlIGNvbmQgZGVmaW5lICcgK1xuICAgICAgJ2RlZmluZS1zeW50YXggZGVsYXkgZG8gZHluYW1pYy13aW5kIGVsc2UgZm9yLWVhY2ggaWYgbGFtYmRhIGxldCBsZXQqICcgK1xuICAgICAgJ2xldC1zeW50YXggbGV0cmVjIGxldHJlYy1zeW50YXggbWFwIG9yIHN5bnRheC1ydWxlcyBcXCcgKiArICwgLEAgLSAuLi4gLyAnICtcbiAgICAgICc7IDwgPD0gPSA9PiA+ID49IGAgYWJzIGFjb3MgYW5nbGUgYXBwZW5kIGFwcGx5IGFzaW4gYXNzb2MgYXNzcSBhc3N2IGF0YW4gJyArXG4gICAgICAnYm9vbGVhbj8gY2FhciBjYWRyIGNhbGwtd2l0aC1pbnB1dC1maWxlIGNhbGwtd2l0aC1vdXRwdXQtZmlsZSAnICtcbiAgICAgICdjYWxsLXdpdGgtdmFsdWVzIGNhciBjZGRkYXIgY2RkZGRyIGNkciBjZWlsaW5nIGNoYXItPmludGVnZXIgJyArXG4gICAgICAnY2hhci1hbHBoYWJldGljPyBjaGFyLWNpPD0/IGNoYXItY2k8PyBjaGFyLWNpPT8gY2hhci1jaT49PyBjaGFyLWNpPj8gJyArXG4gICAgICAnY2hhci1kb3duY2FzZSBjaGFyLWxvd2VyLWNhc2U/IGNoYXItbnVtZXJpYz8gY2hhci1yZWFkeT8gY2hhci11cGNhc2UgJyArXG4gICAgICAnY2hhci11cHBlci1jYXNlPyBjaGFyLXdoaXRlc3BhY2U/IGNoYXI8PT8gY2hhcjw/IGNoYXI9PyBjaGFyPj0/IGNoYXI+PyAnICtcbiAgICAgICdjaGFyPyBjbG9zZS1pbnB1dC1wb3J0IGNsb3NlLW91dHB1dC1wb3J0IGNvbXBsZXg/IGNvbnMgY29zICcgK1xuICAgICAgJ2N1cnJlbnQtaW5wdXQtcG9ydCBjdXJyZW50LW91dHB1dC1wb3J0IGRlbm9taW5hdG9yIGRpc3BsYXkgZW9mLW9iamVjdD8gJyArXG4gICAgICAnZXE/IGVxdWFsPyBlcXY/IGV2YWwgZXZlbj8gZXhhY3QtPmluZXhhY3QgZXhhY3Q/IGV4cCBleHB0IGZsb29yICcgK1xuICAgICAgJ2ZvcmNlIGdjZCBpbWFnLXBhcnQgaW5leGFjdC0+ZXhhY3QgaW5leGFjdD8gaW5wdXQtcG9ydD8gaW50ZWdlci0+Y2hhciAnICtcbiAgICAgICdpbnRlZ2VyPyBpbnRlcmFjdGlvbi1lbnZpcm9ubWVudCBsY20gbGVuZ3RoIGxpc3QgbGlzdC0+c3RyaW5nICcgK1xuICAgICAgJ2xpc3QtPnZlY3RvciBsaXN0LXJlZiBsaXN0LXRhaWwgbGlzdD8gbG9hZCBsb2cgbWFnbml0dWRlIG1ha2UtcG9sYXIgJyArXG4gICAgICAnbWFrZS1yZWN0YW5ndWxhciBtYWtlLXN0cmluZyBtYWtlLXZlY3RvciBtYXggbWVtYmVyIG1lbXEgbWVtdiBtaW4gJyArXG4gICAgICAnbW9kdWxvIG5lZ2F0aXZlPyBuZXdsaW5lIG5vdCBudWxsLWVudmlyb25tZW50IG51bGw/IG51bWJlci0+c3RyaW5nICcgK1xuICAgICAgJ251bWJlcj8gbnVtZXJhdG9yIG9kZD8gb3Blbi1pbnB1dC1maWxlIG9wZW4tb3V0cHV0LWZpbGUgb3V0cHV0LXBvcnQ/ICcgK1xuICAgICAgJ3BhaXI/IHBlZWstY2hhciBwb3J0PyBwb3NpdGl2ZT8gcHJvY2VkdXJlPyBxdWFzaXF1b3RlIHF1b3RlIHF1b3RpZW50ICcgK1xuICAgICAgJ3JhdGlvbmFsPyByYXRpb25hbGl6ZSByZWFkIHJlYWQtY2hhciByZWFsLXBhcnQgcmVhbD8gcmVtYWluZGVyIHJldmVyc2UgJyArXG4gICAgICAncm91bmQgc2NoZW1lLXJlcG9ydC1lbnZpcm9ubWVudCBzZXQhIHNldC1jYXIhIHNldC1jZHIhIHNpbiBzcXJ0IHN0cmluZyAnICtcbiAgICAgICdzdHJpbmctPmxpc3Qgc3RyaW5nLT5udW1iZXIgc3RyaW5nLT5zeW1ib2wgc3RyaW5nLWFwcGVuZCBzdHJpbmctY2k8PT8gJyArXG4gICAgICAnc3RyaW5nLWNpPD8gc3RyaW5nLWNpPT8gc3RyaW5nLWNpPj0/IHN0cmluZy1jaT4/IHN0cmluZy1jb3B5ICcgK1xuICAgICAgJ3N0cmluZy1maWxsISBzdHJpbmctbGVuZ3RoIHN0cmluZy1yZWYgc3RyaW5nLXNldCEgc3RyaW5nPD0/IHN0cmluZzw/ICcgK1xuICAgICAgJ3N0cmluZz0/IHN0cmluZz49PyBzdHJpbmc+PyBzdHJpbmc/IHN1YnN0cmluZyBzeW1ib2wtPnN0cmluZyBzeW1ib2w/ICcgK1xuICAgICAgJ3RhbiB0cmFuc2NyaXB0LW9mZiB0cmFuc2NyaXB0LW9uIHRydW5jYXRlIHZhbHVlcyB2ZWN0b3IgJyArXG4gICAgICAndmVjdG9yLT5saXN0IHZlY3Rvci1maWxsISB2ZWN0b3ItbGVuZ3RoIHZlY3Rvci1yZWYgdmVjdG9yLXNldCEgJyArXG4gICAgICAnd2l0aC1pbnB1dC1mcm9tLWZpbGUgd2l0aC1vdXRwdXQtdG8tZmlsZSB3cml0ZSB3cml0ZS1jaGFyIHplcm8/J1xuICB9O1xuXG4gIGNvbnN0IExJVEVSQUwgPSB7XG4gICAgY2xhc3NOYW1lOiAnbGl0ZXJhbCcsXG4gICAgYmVnaW46ICcoI3R8I2Z8I1xcXFxcXFxcJyArIFNDSEVNRV9JREVOVF9SRSArICd8I1xcXFxcXFxcLiknXG4gIH07XG5cbiAgY29uc3QgTlVNQkVSID0ge1xuICAgIGNsYXNzTmFtZTogJ251bWJlcicsXG4gICAgdmFyaWFudHM6IFtcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IFNDSEVNRV9TSU1QTEVfTlVNQkVSX1JFLFxuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiBTQ0hFTUVfQ09NUExFWF9OVU1CRVJfUkUsXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICcjYlswLTFdKygvWzAtMV0rKT8nXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogJyNvWzAtN10rKC9bMC03XSspPydcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnI3hbMC05YS1mXSsoL1swLTlhLWZdKyk/J1xuICAgICAgfVxuICAgIF1cbiAgfTtcblxuICBjb25zdCBTVFJJTkcgPSBobGpzLlFVT1RFX1NUUklOR19NT0RFO1xuXG4gIGNvbnN0IENPTU1FTlRfTU9ERVMgPSBbXG4gICAgaGxqcy5DT01NRU5UKFxuICAgICAgJzsnLFxuICAgICAgJyQnLFxuICAgICAge1xuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH1cbiAgICApLFxuICAgIGhsanMuQ09NTUVOVCgnI1xcXFx8JywgJ1xcXFx8IycpXG4gIF07XG5cbiAgY29uc3QgSURFTlQgPSB7XG4gICAgYmVnaW46IFNDSEVNRV9JREVOVF9SRSxcbiAgICByZWxldmFuY2U6IDBcbiAgfTtcblxuICBjb25zdCBRVU9URURfSURFTlQgPSB7XG4gICAgY2xhc3NOYW1lOiAnc3ltYm9sJyxcbiAgICBiZWdpbjogJ1xcJycgKyBTQ0hFTUVfSURFTlRfUkVcbiAgfTtcblxuICBjb25zdCBCT0RZID0ge1xuICAgIGVuZHNXaXRoUGFyZW50OiB0cnVlLFxuICAgIHJlbGV2YW5jZTogMFxuICB9O1xuXG4gIGNvbnN0IFFVT1RFRF9MSVNUID0ge1xuICAgIHZhcmlhbnRzOiBbXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAvJy9cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnYCdcbiAgICAgIH1cbiAgICBdLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnXFxcXCgnLFxuICAgICAgICBlbmQ6ICdcXFxcKScsXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgJ3NlbGYnLFxuICAgICAgICAgIExJVEVSQUwsXG4gICAgICAgICAgU1RSSU5HLFxuICAgICAgICAgIE5VTUJFUixcbiAgICAgICAgICBJREVOVCxcbiAgICAgICAgICBRVU9URURfSURFTlRcbiAgICAgICAgXVxuICAgICAgfVxuICAgIF1cbiAgfTtcblxuICBjb25zdCBOQU1FID0ge1xuICAgIGNsYXNzTmFtZTogJ25hbWUnLFxuICAgIHJlbGV2YW5jZTogMCxcbiAgICBiZWdpbjogU0NIRU1FX0lERU5UX1JFLFxuICAgIGtleXdvcmRzOiBLRVlXT1JEU1xuICB9O1xuXG4gIGNvbnN0IExBTUJEQSA9IHtcbiAgICBiZWdpbjogL2xhbWJkYS8sXG4gICAgZW5kc1dpdGhQYXJlbnQ6IHRydWUsXG4gICAgcmV0dXJuQmVnaW46IHRydWUsXG4gICAgY29udGFpbnM6IFtcbiAgICAgIE5BTUUsXG4gICAgICB7XG4gICAgICAgIGVuZHNQYXJlbnQ6IHRydWUsXG4gICAgICAgIHZhcmlhbnRzOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgYmVnaW46IC9cXCgvLFxuICAgICAgICAgICAgZW5kOiAvXFwpL1xuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgYmVnaW46IC9cXFsvLFxuICAgICAgICAgICAgZW5kOiAvXFxdL1xuICAgICAgICAgIH1cbiAgICAgICAgXSxcbiAgICAgICAgY29udGFpbnM6IFsgSURFTlQgXVxuICAgICAgfVxuICAgIF1cbiAgfTtcblxuICBjb25zdCBMSVNUID0ge1xuICAgIHZhcmlhbnRzOiBbXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnXFxcXCgnLFxuICAgICAgICBlbmQ6ICdcXFxcKSdcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnXFxcXFsnLFxuICAgICAgICBlbmQ6ICdcXFxcXSdcbiAgICAgIH1cbiAgICBdLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBMQU1CREEsXG4gICAgICBOQU1FLFxuICAgICAgQk9EWVxuICAgIF1cbiAgfTtcblxuICBCT0RZLmNvbnRhaW5zID0gW1xuICAgIExJVEVSQUwsXG4gICAgTlVNQkVSLFxuICAgIFNUUklORyxcbiAgICBJREVOVCxcbiAgICBRVU9URURfSURFTlQsXG4gICAgUVVPVEVEX0xJU1QsXG4gICAgTElTVFxuICBdLmNvbmNhdChDT01NRU5UX01PREVTKTtcblxuICByZXR1cm4ge1xuICAgIG5hbWU6ICdTY2hlbWUnLFxuICAgIGlsbGVnYWw6IC9cXFMvLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBobGpzLlNIRUJBTkcoKSxcbiAgICAgIE5VTUJFUixcbiAgICAgIFNUUklORyxcbiAgICAgIFFVT1RFRF9JREVOVCxcbiAgICAgIFFVT1RFRF9MSVNULFxuICAgICAgTElTVFxuICAgIF0uY29uY2F0KENPTU1FTlRfTU9ERVMpXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gc2NoZW1lO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9