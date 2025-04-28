(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_java"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/java.js":
/*!***********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/java.js ***!
  \***********************************************************************************************/
/***/ ((module) => {

// https://docs.oracle.com/javase/specs/jls/se15/html/jls-3.html#jls-3.10
var decimalDigits = '[0-9](_*[0-9])*';
var frac = `\\.(${decimalDigits})`;
var hexDigits = '[0-9a-fA-F](_*[0-9a-fA-F])*';
var NUMERIC = {
  className: 'number',
  variants: [
    // DecimalFloatingPointLiteral
    // including ExponentPart
    { begin: `(\\b(${decimalDigits})((${frac})|\\.)?|(${frac}))` +
      `[eE][+-]?(${decimalDigits})[fFdD]?\\b` },
    // excluding ExponentPart
    { begin: `\\b(${decimalDigits})((${frac})[fFdD]?\\b|\\.([fFdD]\\b)?)` },
    { begin: `(${frac})[fFdD]?\\b` },
    { begin: `\\b(${decimalDigits})[fFdD]\\b` },

    // HexadecimalFloatingPointLiteral
    { begin: `\\b0[xX]((${hexDigits})\\.?|(${hexDigits})?\\.(${hexDigits}))` +
      `[pP][+-]?(${decimalDigits})[fFdD]?\\b` },

    // DecimalIntegerLiteral
    { begin: '\\b(0|[1-9](_*[0-9])*)[lL]?\\b' },

    // HexIntegerLiteral
    { begin: `\\b0[xX](${hexDigits})[lL]?\\b` },

    // OctalIntegerLiteral
    { begin: '\\b0(_*[0-7])*[lL]?\\b' },

    // BinaryIntegerLiteral
    { begin: '\\b0[bB][01](_*[01])*[lL]?\\b' },
  ],
  relevance: 0
};

/*
Language: Java
Author: Vsevolod Solovyov <vsevolod.solovyov@gmail.com>
Category: common, enterprise
Website: https://www.java.com/
*/

function java(hljs) {
  var JAVA_IDENT_RE = '[\u00C0-\u02B8a-zA-Z_$][\u00C0-\u02B8a-zA-Z_$0-9]*';
  var GENERIC_IDENT_RE = JAVA_IDENT_RE + '(<' + JAVA_IDENT_RE + '(\\s*,\\s*' + JAVA_IDENT_RE + ')*>)?';
  var KEYWORDS = 'false synchronized int abstract float private char boolean var static null if const ' +
    'for true while long strictfp finally protected import native final void ' +
    'enum else break transient catch instanceof byte super volatile case assert short ' +
    'package default double public try this switch continue throws protected public private ' +
    'module requires exports do';

  var ANNOTATION = {
    className: 'meta',
    begin: '@' + JAVA_IDENT_RE,
    contains: [
      {
        begin: /\(/,
        end: /\)/,
        contains: ["self"] // allow nested () inside our annotation
      },
    ]
  };
  const NUMBER = NUMERIC;

  return {
    name: 'Java',
    aliases: ['jsp'],
    keywords: KEYWORDS,
    illegal: /<\/|#/,
    contains: [
      hljs.COMMENT(
        '/\\*\\*',
        '\\*/',
        {
          relevance: 0,
          contains: [
            {
              // eat up @'s in emails to prevent them to be recognized as doctags
              begin: /\w+@/, relevance: 0
            },
            {
              className: 'doctag',
              begin: '@[A-Za-z]+'
            }
          ]
        }
      ),
      // relevance boost
      {
        begin: /import java\.[a-z]+\./,
        keywords: "import",
        relevance: 2
      },
      hljs.C_LINE_COMMENT_MODE,
      hljs.C_BLOCK_COMMENT_MODE,
      hljs.APOS_STRING_MODE,
      hljs.QUOTE_STRING_MODE,
      {
        className: 'class',
        beginKeywords: 'class interface enum', end: /[{;=]/, excludeEnd: true,
        // TODO: can this be removed somehow?
        // an extra boost because Java is more popular than other languages with
        // this same syntax feature (this is just to preserve our tests passing
        // for now)
        relevance: 1,
        keywords: 'class interface enum',
        illegal: /[:"\[\]]/,
        contains: [
          { beginKeywords: 'extends implements' },
          hljs.UNDERSCORE_TITLE_MODE
        ]
      },
      {
        // Expression keywords prevent 'keyword Name(...)' from being
        // recognized as a function definition
        beginKeywords: 'new throw return else',
        relevance: 0
      },
      {
        className: 'class',
        begin: 'record\\s+' + hljs.UNDERSCORE_IDENT_RE + '\\s*\\(',
        returnBegin: true,
        excludeEnd: true,
        end: /[{;=]/,
        keywords: KEYWORDS,
        contains: [
          { beginKeywords: "record" },
          {
            begin: hljs.UNDERSCORE_IDENT_RE + '\\s*\\(',
            returnBegin: true,
            relevance: 0,
            contains: [hljs.UNDERSCORE_TITLE_MODE]
          },
          {
            className: 'params',
            begin: /\(/, end: /\)/,
            keywords: KEYWORDS,
            relevance: 0,
            contains: [
              hljs.C_BLOCK_COMMENT_MODE
            ]
          },
          hljs.C_LINE_COMMENT_MODE,
          hljs.C_BLOCK_COMMENT_MODE
        ]
      },
      {
        className: 'function',
        begin: '(' + GENERIC_IDENT_RE + '\\s+)+' + hljs.UNDERSCORE_IDENT_RE + '\\s*\\(', returnBegin: true, end: /[{;=]/,
        excludeEnd: true,
        keywords: KEYWORDS,
        contains: [
          {
            begin: hljs.UNDERSCORE_IDENT_RE + '\\s*\\(', returnBegin: true,
            relevance: 0,
            contains: [hljs.UNDERSCORE_TITLE_MODE]
          },
          {
            className: 'params',
            begin: /\(/, end: /\)/,
            keywords: KEYWORDS,
            relevance: 0,
            contains: [
              ANNOTATION,
              hljs.APOS_STRING_MODE,
              hljs.QUOTE_STRING_MODE,
              NUMBER,
              hljs.C_BLOCK_COMMENT_MODE
            ]
          },
          hljs.C_LINE_COMMENT_MODE,
          hljs.C_BLOCK_COMMENT_MODE
        ]
      },
      NUMBER,
      ANNOTATION
    ]
  };
}

module.exports = java;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfamF2YS5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0Esa0JBQWtCLGNBQWM7QUFDaEM7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsTUFBTSxlQUFlLGNBQWMsS0FBSyxLQUFLLFdBQVcsS0FBSztBQUM3RCxtQkFBbUIsY0FBYyxjQUFjO0FBQy9DO0FBQ0EsTUFBTSxjQUFjLGNBQWMsS0FBSyxLQUFLLCtCQUErQjtBQUMzRSxNQUFNLFdBQVcsS0FBSyxjQUFjO0FBQ3BDLE1BQU0sY0FBYyxjQUFjLGFBQWE7O0FBRS9DO0FBQ0EsTUFBTSxvQkFBb0IsVUFBVSxTQUFTLFVBQVUsUUFBUSxVQUFVO0FBQ3pFLG1CQUFtQixjQUFjLGNBQWM7O0FBRS9DO0FBQ0EsTUFBTSx5Q0FBeUM7O0FBRS9DO0FBQ0EsTUFBTSxtQkFBbUIsVUFBVSxZQUFZOztBQUUvQztBQUNBLE1BQU0saUNBQWlDOztBQUV2QztBQUNBLE1BQU0sd0NBQXdDO0FBQzlDO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLHdEQUF3RDtBQUN4RDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsWUFBWSxxQ0FBcUM7QUFDakQ7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxpQkFBaUI7QUFDakI7QUFDQTtBQUNBLFlBQVkseUJBQXlCO0FBQ3JDO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFdBQVc7QUFDWDtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBLHFIQUFxSDtBQUNySDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFdBQVc7QUFDWDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL2phdmEuanMiXSwic291cmNlc0NvbnRlbnQiOlsiLy8gaHR0cHM6Ly9kb2NzLm9yYWNsZS5jb20vamF2YXNlL3NwZWNzL2pscy9zZTE1L2h0bWwvamxzLTMuaHRtbCNqbHMtMy4xMFxudmFyIGRlY2ltYWxEaWdpdHMgPSAnWzAtOV0oXypbMC05XSkqJztcbnZhciBmcmFjID0gYFxcXFwuKCR7ZGVjaW1hbERpZ2l0c30pYDtcbnZhciBoZXhEaWdpdHMgPSAnWzAtOWEtZkEtRl0oXypbMC05YS1mQS1GXSkqJztcbnZhciBOVU1FUklDID0ge1xuICBjbGFzc05hbWU6ICdudW1iZXInLFxuICB2YXJpYW50czogW1xuICAgIC8vIERlY2ltYWxGbG9hdGluZ1BvaW50TGl0ZXJhbFxuICAgIC8vIGluY2x1ZGluZyBFeHBvbmVudFBhcnRcbiAgICB7IGJlZ2luOiBgKFxcXFxiKCR7ZGVjaW1hbERpZ2l0c30pKCgke2ZyYWN9KXxcXFxcLik/fCgke2ZyYWN9KSlgICtcbiAgICAgIGBbZUVdWystXT8oJHtkZWNpbWFsRGlnaXRzfSlbZkZkRF0/XFxcXGJgIH0sXG4gICAgLy8gZXhjbHVkaW5nIEV4cG9uZW50UGFydFxuICAgIHsgYmVnaW46IGBcXFxcYigke2RlY2ltYWxEaWdpdHN9KSgoJHtmcmFjfSlbZkZkRF0/XFxcXGJ8XFxcXC4oW2ZGZERdXFxcXGIpPylgIH0sXG4gICAgeyBiZWdpbjogYCgke2ZyYWN9KVtmRmREXT9cXFxcYmAgfSxcbiAgICB7IGJlZ2luOiBgXFxcXGIoJHtkZWNpbWFsRGlnaXRzfSlbZkZkRF1cXFxcYmAgfSxcblxuICAgIC8vIEhleGFkZWNpbWFsRmxvYXRpbmdQb2ludExpdGVyYWxcbiAgICB7IGJlZ2luOiBgXFxcXGIwW3hYXSgoJHtoZXhEaWdpdHN9KVxcXFwuP3woJHtoZXhEaWdpdHN9KT9cXFxcLigke2hleERpZ2l0c30pKWAgK1xuICAgICAgYFtwUF1bKy1dPygke2RlY2ltYWxEaWdpdHN9KVtmRmREXT9cXFxcYmAgfSxcblxuICAgIC8vIERlY2ltYWxJbnRlZ2VyTGl0ZXJhbFxuICAgIHsgYmVnaW46ICdcXFxcYigwfFsxLTldKF8qWzAtOV0pKilbbExdP1xcXFxiJyB9LFxuXG4gICAgLy8gSGV4SW50ZWdlckxpdGVyYWxcbiAgICB7IGJlZ2luOiBgXFxcXGIwW3hYXSgke2hleERpZ2l0c30pW2xMXT9cXFxcYmAgfSxcblxuICAgIC8vIE9jdGFsSW50ZWdlckxpdGVyYWxcbiAgICB7IGJlZ2luOiAnXFxcXGIwKF8qWzAtN10pKltsTF0/XFxcXGInIH0sXG5cbiAgICAvLyBCaW5hcnlJbnRlZ2VyTGl0ZXJhbFxuICAgIHsgYmVnaW46ICdcXFxcYjBbYkJdWzAxXShfKlswMV0pKltsTF0/XFxcXGInIH0sXG4gIF0sXG4gIHJlbGV2YW5jZTogMFxufTtcblxuLypcbkxhbmd1YWdlOiBKYXZhXG5BdXRob3I6IFZzZXZvbG9kIFNvbG92eW92IDx2c2V2b2xvZC5zb2xvdnlvdkBnbWFpbC5jb20+XG5DYXRlZ29yeTogY29tbW9uLCBlbnRlcnByaXNlXG5XZWJzaXRlOiBodHRwczovL3d3dy5qYXZhLmNvbS9cbiovXG5cbmZ1bmN0aW9uIGphdmEoaGxqcykge1xuICB2YXIgSkFWQV9JREVOVF9SRSA9ICdbXFx1MDBDMC1cXHUwMkI4YS16QS1aXyRdW1xcdTAwQzAtXFx1MDJCOGEtekEtWl8kMC05XSonO1xuICB2YXIgR0VORVJJQ19JREVOVF9SRSA9IEpBVkFfSURFTlRfUkUgKyAnKDwnICsgSkFWQV9JREVOVF9SRSArICcoXFxcXHMqLFxcXFxzKicgKyBKQVZBX0lERU5UX1JFICsgJykqPik/JztcbiAgdmFyIEtFWVdPUkRTID0gJ2ZhbHNlIHN5bmNocm9uaXplZCBpbnQgYWJzdHJhY3QgZmxvYXQgcHJpdmF0ZSBjaGFyIGJvb2xlYW4gdmFyIHN0YXRpYyBudWxsIGlmIGNvbnN0ICcgK1xuICAgICdmb3IgdHJ1ZSB3aGlsZSBsb25nIHN0cmljdGZwIGZpbmFsbHkgcHJvdGVjdGVkIGltcG9ydCBuYXRpdmUgZmluYWwgdm9pZCAnICtcbiAgICAnZW51bSBlbHNlIGJyZWFrIHRyYW5zaWVudCBjYXRjaCBpbnN0YW5jZW9mIGJ5dGUgc3VwZXIgdm9sYXRpbGUgY2FzZSBhc3NlcnQgc2hvcnQgJyArXG4gICAgJ3BhY2thZ2UgZGVmYXVsdCBkb3VibGUgcHVibGljIHRyeSB0aGlzIHN3aXRjaCBjb250aW51ZSB0aHJvd3MgcHJvdGVjdGVkIHB1YmxpYyBwcml2YXRlICcgK1xuICAgICdtb2R1bGUgcmVxdWlyZXMgZXhwb3J0cyBkbyc7XG5cbiAgdmFyIEFOTk9UQVRJT04gPSB7XG4gICAgY2xhc3NOYW1lOiAnbWV0YScsXG4gICAgYmVnaW46ICdAJyArIEpBVkFfSURFTlRfUkUsXG4gICAgY29udGFpbnM6IFtcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC9cXCgvLFxuICAgICAgICBlbmQ6IC9cXCkvLFxuICAgICAgICBjb250YWluczogW1wic2VsZlwiXSAvLyBhbGxvdyBuZXN0ZWQgKCkgaW5zaWRlIG91ciBhbm5vdGF0aW9uXG4gICAgICB9LFxuICAgIF1cbiAgfTtcbiAgY29uc3QgTlVNQkVSID0gTlVNRVJJQztcblxuICByZXR1cm4ge1xuICAgIG5hbWU6ICdKYXZhJyxcbiAgICBhbGlhc2VzOiBbJ2pzcCddLFxuICAgIGtleXdvcmRzOiBLRVlXT1JEUyxcbiAgICBpbGxlZ2FsOiAvPFxcL3wjLyxcbiAgICBjb250YWluczogW1xuICAgICAgaGxqcy5DT01NRU5UKFxuICAgICAgICAnL1xcXFwqXFxcXConLFxuICAgICAgICAnXFxcXCovJyxcbiAgICAgICAge1xuICAgICAgICAgIHJlbGV2YW5jZTogMCxcbiAgICAgICAgICBjb250YWluczogW1xuICAgICAgICAgICAge1xuICAgICAgICAgICAgICAvLyBlYXQgdXAgQCdzIGluIGVtYWlscyB0byBwcmV2ZW50IHRoZW0gdG8gYmUgcmVjb2duaXplZCBhcyBkb2N0YWdzXG4gICAgICAgICAgICAgIGJlZ2luOiAvXFx3K0AvLCByZWxldmFuY2U6IDBcbiAgICAgICAgICAgIH0sXG4gICAgICAgICAgICB7XG4gICAgICAgICAgICAgIGNsYXNzTmFtZTogJ2RvY3RhZycsXG4gICAgICAgICAgICAgIGJlZ2luOiAnQFtBLVphLXpdKydcbiAgICAgICAgICAgIH1cbiAgICAgICAgICBdXG4gICAgICAgIH1cbiAgICAgICksXG4gICAgICAvLyByZWxldmFuY2UgYm9vc3RcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC9pbXBvcnQgamF2YVxcLlthLXpdK1xcLi8sXG4gICAgICAgIGtleXdvcmRzOiBcImltcG9ydFwiLFxuICAgICAgICByZWxldmFuY2U6IDJcbiAgICAgIH0sXG4gICAgICBobGpzLkNfTElORV9DT01NRU5UX01PREUsXG4gICAgICBobGpzLkNfQkxPQ0tfQ09NTUVOVF9NT0RFLFxuICAgICAgaGxqcy5BUE9TX1NUUklOR19NT0RFLFxuICAgICAgaGxqcy5RVU9URV9TVFJJTkdfTU9ERSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnY2xhc3MnLFxuICAgICAgICBiZWdpbktleXdvcmRzOiAnY2xhc3MgaW50ZXJmYWNlIGVudW0nLCBlbmQ6IC9bezs9XS8sIGV4Y2x1ZGVFbmQ6IHRydWUsXG4gICAgICAgIC8vIFRPRE86IGNhbiB0aGlzIGJlIHJlbW92ZWQgc29tZWhvdz9cbiAgICAgICAgLy8gYW4gZXh0cmEgYm9vc3QgYmVjYXVzZSBKYXZhIGlzIG1vcmUgcG9wdWxhciB0aGFuIG90aGVyIGxhbmd1YWdlcyB3aXRoXG4gICAgICAgIC8vIHRoaXMgc2FtZSBzeW50YXggZmVhdHVyZSAodGhpcyBpcyBqdXN0IHRvIHByZXNlcnZlIG91ciB0ZXN0cyBwYXNzaW5nXG4gICAgICAgIC8vIGZvciBub3cpXG4gICAgICAgIHJlbGV2YW5jZTogMSxcbiAgICAgICAga2V5d29yZHM6ICdjbGFzcyBpbnRlcmZhY2UgZW51bScsXG4gICAgICAgIGlsbGVnYWw6IC9bOlwiXFxbXFxdXS8sXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgeyBiZWdpbktleXdvcmRzOiAnZXh0ZW5kcyBpbXBsZW1lbnRzJyB9LFxuICAgICAgICAgIGhsanMuVU5ERVJTQ09SRV9USVRMRV9NT0RFXG4gICAgICAgIF1cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIC8vIEV4cHJlc3Npb24ga2V5d29yZHMgcHJldmVudCAna2V5d29yZCBOYW1lKC4uLiknIGZyb20gYmVpbmdcbiAgICAgICAgLy8gcmVjb2duaXplZCBhcyBhIGZ1bmN0aW9uIGRlZmluaXRpb25cbiAgICAgICAgYmVnaW5LZXl3b3JkczogJ25ldyB0aHJvdyByZXR1cm4gZWxzZScsXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnY2xhc3MnLFxuICAgICAgICBiZWdpbjogJ3JlY29yZFxcXFxzKycgKyBobGpzLlVOREVSU0NPUkVfSURFTlRfUkUgKyAnXFxcXHMqXFxcXCgnLFxuICAgICAgICByZXR1cm5CZWdpbjogdHJ1ZSxcbiAgICAgICAgZXhjbHVkZUVuZDogdHJ1ZSxcbiAgICAgICAgZW5kOiAvW3s7PV0vLFxuICAgICAgICBrZXl3b3JkczogS0VZV09SRFMsXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgeyBiZWdpbktleXdvcmRzOiBcInJlY29yZFwiIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgYmVnaW46IGhsanMuVU5ERVJTQ09SRV9JREVOVF9SRSArICdcXFxccypcXFxcKCcsXG4gICAgICAgICAgICByZXR1cm5CZWdpbjogdHJ1ZSxcbiAgICAgICAgICAgIHJlbGV2YW5jZTogMCxcbiAgICAgICAgICAgIGNvbnRhaW5zOiBbaGxqcy5VTkRFUlNDT1JFX1RJVExFX01PREVdXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICBjbGFzc05hbWU6ICdwYXJhbXMnLFxuICAgICAgICAgICAgYmVnaW46IC9cXCgvLCBlbmQ6IC9cXCkvLFxuICAgICAgICAgICAga2V5d29yZHM6IEtFWVdPUkRTLFxuICAgICAgICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICAgICAgaGxqcy5DX0JMT0NLX0NPTU1FTlRfTU9ERVxuICAgICAgICAgICAgXVxuICAgICAgICAgIH0sXG4gICAgICAgICAgaGxqcy5DX0xJTkVfQ09NTUVOVF9NT0RFLFxuICAgICAgICAgIGhsanMuQ19CTE9DS19DT01NRU5UX01PREVcbiAgICAgICAgXVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnZnVuY3Rpb24nLFxuICAgICAgICBiZWdpbjogJygnICsgR0VORVJJQ19JREVOVF9SRSArICdcXFxccyspKycgKyBobGpzLlVOREVSU0NPUkVfSURFTlRfUkUgKyAnXFxcXHMqXFxcXCgnLCByZXR1cm5CZWdpbjogdHJ1ZSwgZW5kOiAvW3s7PV0vLFxuICAgICAgICBleGNsdWRlRW5kOiB0cnVlLFxuICAgICAgICBrZXl3b3JkczogS0VZV09SRFMsXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgYmVnaW46IGhsanMuVU5ERVJTQ09SRV9JREVOVF9SRSArICdcXFxccypcXFxcKCcsIHJldHVybkJlZ2luOiB0cnVlLFxuICAgICAgICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgICAgICAgY29udGFpbnM6IFtobGpzLlVOREVSU0NPUkVfVElUTEVfTU9ERV1cbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGNsYXNzTmFtZTogJ3BhcmFtcycsXG4gICAgICAgICAgICBiZWdpbjogL1xcKC8sIGVuZDogL1xcKS8sXG4gICAgICAgICAgICBrZXl3b3JkczogS0VZV09SRFMsXG4gICAgICAgICAgICByZWxldmFuY2U6IDAsXG4gICAgICAgICAgICBjb250YWluczogW1xuICAgICAgICAgICAgICBBTk5PVEFUSU9OLFxuICAgICAgICAgICAgICBobGpzLkFQT1NfU1RSSU5HX01PREUsXG4gICAgICAgICAgICAgIGhsanMuUVVPVEVfU1RSSU5HX01PREUsXG4gICAgICAgICAgICAgIE5VTUJFUixcbiAgICAgICAgICAgICAgaGxqcy5DX0JMT0NLX0NPTU1FTlRfTU9ERVxuICAgICAgICAgICAgXVxuICAgICAgICAgIH0sXG4gICAgICAgICAgaGxqcy5DX0xJTkVfQ09NTUVOVF9NT0RFLFxuICAgICAgICAgIGhsanMuQ19CTE9DS19DT01NRU5UX01PREVcbiAgICAgICAgXVxuICAgICAgfSxcbiAgICAgIE5VTUJFUixcbiAgICAgIEFOTk9UQVRJT05cbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gamF2YTtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==