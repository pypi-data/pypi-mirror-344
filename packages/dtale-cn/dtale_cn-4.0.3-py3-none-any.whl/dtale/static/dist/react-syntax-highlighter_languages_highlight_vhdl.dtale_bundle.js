(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_vhdl"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/vhdl.js":
/*!***********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/vhdl.js ***!
  \***********************************************************************************************/
/***/ ((module) => {

/*
Language: VHDL
Author: Igor Kalnitsky <igor@kalnitsky.org>
Contributors: Daniel C.K. Kho <daniel.kho@tauhop.com>, Guillaume Savaton <guillaume.savaton@eseo.fr>
Description: VHDL is a hardware description language used in electronic design automation to describe digital and mixed-signal systems.
Website: https://en.wikipedia.org/wiki/VHDL
*/

function vhdl(hljs) {
  // Regular expression for VHDL numeric literals.

  // Decimal literal:
  const INTEGER_RE = '\\d(_|\\d)*';
  const EXPONENT_RE = '[eE][-+]?' + INTEGER_RE;
  const DECIMAL_LITERAL_RE = INTEGER_RE + '(\\.' + INTEGER_RE + ')?' + '(' + EXPONENT_RE + ')?';
  // Based literal:
  const BASED_INTEGER_RE = '\\w+';
  const BASED_LITERAL_RE = INTEGER_RE + '#' + BASED_INTEGER_RE + '(\\.' + BASED_INTEGER_RE + ')?' + '#' + '(' + EXPONENT_RE + ')?';

  const NUMBER_RE = '\\b(' + BASED_LITERAL_RE + '|' + DECIMAL_LITERAL_RE + ')';

  return {
    name: 'VHDL',
    case_insensitive: true,
    keywords: {
      keyword:
        'abs access after alias all and architecture array assert assume assume_guarantee attribute ' +
        'begin block body buffer bus case component configuration constant context cover disconnect ' +
        'downto default else elsif end entity exit fairness file for force function generate ' +
        'generic group guarded if impure in inertial inout is label library linkage literal ' +
        'loop map mod nand new next nor not null of on open or others out package parameter port ' +
        'postponed procedure process property protected pure range record register reject ' +
        'release rem report restrict restrict_guarantee return rol ror select sequence ' +
        'severity shared signal sla sll sra srl strong subtype then to transport type ' +
        'unaffected units until use variable view vmode vprop vunit wait when while with xnor xor',
      built_in:
        'boolean bit character ' +
        'integer time delay_length natural positive ' +
        'string bit_vector file_open_kind file_open_status ' +
        'std_logic std_logic_vector unsigned signed boolean_vector integer_vector ' +
        'std_ulogic std_ulogic_vector unresolved_unsigned u_unsigned unresolved_signed u_signed ' +
        'real_vector time_vector',
      literal:
        'false true note warning error failure ' + // severity_level
        'line text side width' // textio
    },
    illegal: /\{/,
    contains: [
      hljs.C_BLOCK_COMMENT_MODE, // VHDL-2008 block commenting.
      hljs.COMMENT('--', '$'),
      hljs.QUOTE_STRING_MODE,
      {
        className: 'number',
        begin: NUMBER_RE,
        relevance: 0
      },
      {
        className: 'string',
        begin: '\'(U|X|0|1|Z|W|L|H|-)\'',
        contains: [ hljs.BACKSLASH_ESCAPE ]
      },
      {
        className: 'symbol',
        begin: '\'[A-Za-z](_?[A-Za-z0-9])*',
        contains: [ hljs.BACKSLASH_ESCAPE ]
      }
    ]
  };
}

module.exports = vhdl;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfdmhkbC5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTCxnQkFBZ0I7QUFDaEI7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy92aGRsLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogVkhETFxuQXV0aG9yOiBJZ29yIEthbG5pdHNreSA8aWdvckBrYWxuaXRza3kub3JnPlxuQ29udHJpYnV0b3JzOiBEYW5pZWwgQy5LLiBLaG8gPGRhbmllbC5raG9AdGF1aG9wLmNvbT4sIEd1aWxsYXVtZSBTYXZhdG9uIDxndWlsbGF1bWUuc2F2YXRvbkBlc2VvLmZyPlxuRGVzY3JpcHRpb246IFZIREwgaXMgYSBoYXJkd2FyZSBkZXNjcmlwdGlvbiBsYW5ndWFnZSB1c2VkIGluIGVsZWN0cm9uaWMgZGVzaWduIGF1dG9tYXRpb24gdG8gZGVzY3JpYmUgZGlnaXRhbCBhbmQgbWl4ZWQtc2lnbmFsIHN5c3RlbXMuXG5XZWJzaXRlOiBodHRwczovL2VuLndpa2lwZWRpYS5vcmcvd2lraS9WSERMXG4qL1xuXG5mdW5jdGlvbiB2aGRsKGhsanMpIHtcbiAgLy8gUmVndWxhciBleHByZXNzaW9uIGZvciBWSERMIG51bWVyaWMgbGl0ZXJhbHMuXG5cbiAgLy8gRGVjaW1hbCBsaXRlcmFsOlxuICBjb25zdCBJTlRFR0VSX1JFID0gJ1xcXFxkKF98XFxcXGQpKic7XG4gIGNvbnN0IEVYUE9ORU5UX1JFID0gJ1tlRV1bLStdPycgKyBJTlRFR0VSX1JFO1xuICBjb25zdCBERUNJTUFMX0xJVEVSQUxfUkUgPSBJTlRFR0VSX1JFICsgJyhcXFxcLicgKyBJTlRFR0VSX1JFICsgJyk/JyArICcoJyArIEVYUE9ORU5UX1JFICsgJyk/JztcbiAgLy8gQmFzZWQgbGl0ZXJhbDpcbiAgY29uc3QgQkFTRURfSU5URUdFUl9SRSA9ICdcXFxcdysnO1xuICBjb25zdCBCQVNFRF9MSVRFUkFMX1JFID0gSU5URUdFUl9SRSArICcjJyArIEJBU0VEX0lOVEVHRVJfUkUgKyAnKFxcXFwuJyArIEJBU0VEX0lOVEVHRVJfUkUgKyAnKT8nICsgJyMnICsgJygnICsgRVhQT05FTlRfUkUgKyAnKT8nO1xuXG4gIGNvbnN0IE5VTUJFUl9SRSA9ICdcXFxcYignICsgQkFTRURfTElURVJBTF9SRSArICd8JyArIERFQ0lNQUxfTElURVJBTF9SRSArICcpJztcblxuICByZXR1cm4ge1xuICAgIG5hbWU6ICdWSERMJyxcbiAgICBjYXNlX2luc2Vuc2l0aXZlOiB0cnVlLFxuICAgIGtleXdvcmRzOiB7XG4gICAgICBrZXl3b3JkOlxuICAgICAgICAnYWJzIGFjY2VzcyBhZnRlciBhbGlhcyBhbGwgYW5kIGFyY2hpdGVjdHVyZSBhcnJheSBhc3NlcnQgYXNzdW1lIGFzc3VtZV9ndWFyYW50ZWUgYXR0cmlidXRlICcgK1xuICAgICAgICAnYmVnaW4gYmxvY2sgYm9keSBidWZmZXIgYnVzIGNhc2UgY29tcG9uZW50IGNvbmZpZ3VyYXRpb24gY29uc3RhbnQgY29udGV4dCBjb3ZlciBkaXNjb25uZWN0ICcgK1xuICAgICAgICAnZG93bnRvIGRlZmF1bHQgZWxzZSBlbHNpZiBlbmQgZW50aXR5IGV4aXQgZmFpcm5lc3MgZmlsZSBmb3IgZm9yY2UgZnVuY3Rpb24gZ2VuZXJhdGUgJyArXG4gICAgICAgICdnZW5lcmljIGdyb3VwIGd1YXJkZWQgaWYgaW1wdXJlIGluIGluZXJ0aWFsIGlub3V0IGlzIGxhYmVsIGxpYnJhcnkgbGlua2FnZSBsaXRlcmFsICcgK1xuICAgICAgICAnbG9vcCBtYXAgbW9kIG5hbmQgbmV3IG5leHQgbm9yIG5vdCBudWxsIG9mIG9uIG9wZW4gb3Igb3RoZXJzIG91dCBwYWNrYWdlIHBhcmFtZXRlciBwb3J0ICcgK1xuICAgICAgICAncG9zdHBvbmVkIHByb2NlZHVyZSBwcm9jZXNzIHByb3BlcnR5IHByb3RlY3RlZCBwdXJlIHJhbmdlIHJlY29yZCByZWdpc3RlciByZWplY3QgJyArXG4gICAgICAgICdyZWxlYXNlIHJlbSByZXBvcnQgcmVzdHJpY3QgcmVzdHJpY3RfZ3VhcmFudGVlIHJldHVybiByb2wgcm9yIHNlbGVjdCBzZXF1ZW5jZSAnICtcbiAgICAgICAgJ3NldmVyaXR5IHNoYXJlZCBzaWduYWwgc2xhIHNsbCBzcmEgc3JsIHN0cm9uZyBzdWJ0eXBlIHRoZW4gdG8gdHJhbnNwb3J0IHR5cGUgJyArXG4gICAgICAgICd1bmFmZmVjdGVkIHVuaXRzIHVudGlsIHVzZSB2YXJpYWJsZSB2aWV3IHZtb2RlIHZwcm9wIHZ1bml0IHdhaXQgd2hlbiB3aGlsZSB3aXRoIHhub3IgeG9yJyxcbiAgICAgIGJ1aWx0X2luOlxuICAgICAgICAnYm9vbGVhbiBiaXQgY2hhcmFjdGVyICcgK1xuICAgICAgICAnaW50ZWdlciB0aW1lIGRlbGF5X2xlbmd0aCBuYXR1cmFsIHBvc2l0aXZlICcgK1xuICAgICAgICAnc3RyaW5nIGJpdF92ZWN0b3IgZmlsZV9vcGVuX2tpbmQgZmlsZV9vcGVuX3N0YXR1cyAnICtcbiAgICAgICAgJ3N0ZF9sb2dpYyBzdGRfbG9naWNfdmVjdG9yIHVuc2lnbmVkIHNpZ25lZCBib29sZWFuX3ZlY3RvciBpbnRlZ2VyX3ZlY3RvciAnICtcbiAgICAgICAgJ3N0ZF91bG9naWMgc3RkX3Vsb2dpY192ZWN0b3IgdW5yZXNvbHZlZF91bnNpZ25lZCB1X3Vuc2lnbmVkIHVucmVzb2x2ZWRfc2lnbmVkIHVfc2lnbmVkICcgK1xuICAgICAgICAncmVhbF92ZWN0b3IgdGltZV92ZWN0b3InLFxuICAgICAgbGl0ZXJhbDpcbiAgICAgICAgJ2ZhbHNlIHRydWUgbm90ZSB3YXJuaW5nIGVycm9yIGZhaWx1cmUgJyArIC8vIHNldmVyaXR5X2xldmVsXG4gICAgICAgICdsaW5lIHRleHQgc2lkZSB3aWR0aCcgLy8gdGV4dGlvXG4gICAgfSxcbiAgICBpbGxlZ2FsOiAvXFx7LyxcbiAgICBjb250YWluczogW1xuICAgICAgaGxqcy5DX0JMT0NLX0NPTU1FTlRfTU9ERSwgLy8gVkhETC0yMDA4IGJsb2NrIGNvbW1lbnRpbmcuXG4gICAgICBobGpzLkNPTU1FTlQoJy0tJywgJyQnKSxcbiAgICAgIGhsanMuUVVPVEVfU1RSSU5HX01PREUsXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ251bWJlcicsXG4gICAgICAgIGJlZ2luOiBOVU1CRVJfUkUsXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICAgICAgYmVnaW46ICdcXCcoVXxYfDB8MXxafFd8THxIfC0pXFwnJyxcbiAgICAgICAgY29udGFpbnM6IFsgaGxqcy5CQUNLU0xBU0hfRVNDQVBFIF1cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3N5bWJvbCcsXG4gICAgICAgIGJlZ2luOiAnXFwnW0EtWmEtel0oXz9bQS1aYS16MC05XSkqJyxcbiAgICAgICAgY29udGFpbnM6IFsgaGxqcy5CQUNLU0xBU0hfRVNDQVBFIF1cbiAgICAgIH1cbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gdmhkbDtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==