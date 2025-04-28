(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_ada"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/ada.js":
/*!**********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/ada.js ***!
  \**********************************************************************************************/
/***/ ((module) => {

/*
Language: Ada
Author: Lars Schulna <kartoffelbrei.mit.muskatnuss@gmail.org>
Description: Ada is a general-purpose programming language that has great support for saftey critical and real-time applications.
             It has been developed by the DoD and thus has been used in military and safety-critical applications (like civil aviation).
             The first version appeared in the 80s, but it's still actively developed today with
             the newest standard being Ada2012.
*/

// We try to support full Ada2012
//
// We highlight all appearances of types, keywords, literals (string, char, number, bool)
// and titles (user defined function/procedure/package)
// CSS classes are set accordingly
//
// Languages causing problems for language detection:
// xml (broken by Foo : Bar type), elm (broken by Foo : Bar type), vbscript-html (broken by body keyword)
// sql (ada default.txt has a lot of sql keywords)

/** @type LanguageFn */
function ada(hljs) {
  // Regular expression for Ada numeric literals.
  // stolen form the VHDL highlighter

  // Decimal literal:
  const INTEGER_RE = '\\d(_|\\d)*';
  const EXPONENT_RE = '[eE][-+]?' + INTEGER_RE;
  const DECIMAL_LITERAL_RE = INTEGER_RE + '(\\.' + INTEGER_RE + ')?' + '(' + EXPONENT_RE + ')?';

  // Based literal:
  const BASED_INTEGER_RE = '\\w+';
  const BASED_LITERAL_RE = INTEGER_RE + '#' + BASED_INTEGER_RE + '(\\.' + BASED_INTEGER_RE + ')?' + '#' + '(' + EXPONENT_RE + ')?';

  const NUMBER_RE = '\\b(' + BASED_LITERAL_RE + '|' + DECIMAL_LITERAL_RE + ')';

  // Identifier regex
  const ID_REGEX = '[A-Za-z](_?[A-Za-z0-9.])*';

  // bad chars, only allowed in literals
  const BAD_CHARS = `[]\\{\\}%#'"`;

  // Ada doesn't have block comments, only line comments
  const COMMENTS = hljs.COMMENT('--', '$');

  // variable declarations of the form
  // Foo : Bar := Baz;
  // where only Bar will be highlighted
  const VAR_DECLS = {
    // TODO: These spaces are not required by the Ada syntax
    // however, I have yet to see handwritten Ada code where
    // someone does not put spaces around :
    begin: '\\s+:\\s+',
    end: '\\s*(:=|;|\\)|=>|$)',
    // endsWithParent: true,
    // returnBegin: true,
    illegal: BAD_CHARS,
    contains: [
      {
        // workaround to avoid highlighting
        // named loops and declare blocks
        beginKeywords: 'loop for declare others',
        endsParent: true
      },
      {
        // properly highlight all modifiers
        className: 'keyword',
        beginKeywords: 'not null constant access function procedure in out aliased exception'
      },
      {
        className: 'type',
        begin: ID_REGEX,
        endsParent: true,
        relevance: 0
      }
    ]
  };

  return {
    name: 'Ada',
    case_insensitive: true,
    keywords: {
      keyword:
                'abort else new return abs elsif not reverse abstract end ' +
                'accept entry select access exception of separate aliased exit or some ' +
                'all others subtype and for out synchronized array function overriding ' +
                'at tagged generic package task begin goto pragma terminate ' +
                'body private then if procedure type case in protected constant interface ' +
                'is raise use declare range delay limited record when delta loop rem while ' +
                'digits renames with do mod requeue xor',
      literal:
                'True False'
    },
    contains: [
      COMMENTS,
      // strings "foobar"
      {
        className: 'string',
        begin: /"/,
        end: /"/,
        contains: [{
          begin: /""/,
          relevance: 0
        }]
      },
      // characters ''
      {
        // character literals always contain one char
        className: 'string',
        begin: /'.'/
      },
      {
        // number literals
        className: 'number',
        begin: NUMBER_RE,
        relevance: 0
      },
      {
        // Attributes
        className: 'symbol',
        begin: "'" + ID_REGEX
      },
      {
        // package definition, maybe inside generic
        className: 'title',
        begin: '(\\bwith\\s+)?(\\bprivate\\s+)?\\bpackage\\s+(\\bbody\\s+)?',
        end: '(is|$)',
        keywords: 'package body',
        excludeBegin: true,
        excludeEnd: true,
        illegal: BAD_CHARS
      },
      {
        // function/procedure declaration/definition
        // maybe inside generic
        begin: '(\\b(with|overriding)\\s+)?\\b(function|procedure)\\s+',
        end: '(\\bis|\\bwith|\\brenames|\\)\\s*;)',
        keywords: 'overriding function procedure with is renames return',
        // we need to re-match the 'function' keyword, so that
        // the title mode below matches only exactly once
        returnBegin: true,
        contains:
                [
                  COMMENTS,
                  {
                    // name of the function/procedure
                    className: 'title',
                    begin: '(\\bwith\\s+)?\\b(function|procedure)\\s+',
                    end: '(\\(|\\s+|$)',
                    excludeBegin: true,
                    excludeEnd: true,
                    illegal: BAD_CHARS
                  },
                  // 'self'
                  // // parameter types
                  VAR_DECLS,
                  {
                    // return type
                    className: 'type',
                    begin: '\\breturn\\s+',
                    end: '(\\s+|;|$)',
                    keywords: 'return',
                    excludeBegin: true,
                    excludeEnd: true,
                    // we are done with functions
                    endsParent: true,
                    illegal: BAD_CHARS

                  }
                ]
      },
      {
        // new type declarations
        // maybe inside generic
        className: 'type',
        begin: '\\b(sub)?type\\s+',
        end: '\\s+',
        keywords: 'type',
        excludeBegin: true,
        illegal: BAD_CHARS
      },

      // see comment above the definition
      VAR_DECLS

      // no markup
      // relevance boosters for small snippets
      // {begin: '\\s*=>\\s*'},
      // {begin: '\\s*:=\\s*'},
      // {begin: '\\s+:=\\s+'},
    ]
  };
}

module.exports = ada;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfYWRhLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTs7QUFFQTs7QUFFQTtBQUNBOztBQUVBO0FBQ0EsMEJBQTBCLEdBQUc7O0FBRTdCO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLG1CQUFtQjtBQUNuQjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsU0FBUztBQUNULE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsZ0RBQWdEO0FBQ2hEO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLG1CQUFtQjtBQUNuQjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLGlDQUFpQztBQUNqQztBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPOztBQUVQO0FBQ0E7O0FBRUE7QUFDQTtBQUNBLFVBQVUsb0JBQW9CO0FBQzlCLFVBQVUsb0JBQW9CO0FBQzlCLFVBQVUsb0JBQW9CO0FBQzlCO0FBQ0E7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvYWRhLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogQWRhXG5BdXRob3I6IExhcnMgU2NodWxuYSA8a2FydG9mZmVsYnJlaS5taXQubXVza2F0bnVzc0BnbWFpbC5vcmc+XG5EZXNjcmlwdGlvbjogQWRhIGlzIGEgZ2VuZXJhbC1wdXJwb3NlIHByb2dyYW1taW5nIGxhbmd1YWdlIHRoYXQgaGFzIGdyZWF0IHN1cHBvcnQgZm9yIHNhZnRleSBjcml0aWNhbCBhbmQgcmVhbC10aW1lIGFwcGxpY2F0aW9ucy5cbiAgICAgICAgICAgICBJdCBoYXMgYmVlbiBkZXZlbG9wZWQgYnkgdGhlIERvRCBhbmQgdGh1cyBoYXMgYmVlbiB1c2VkIGluIG1pbGl0YXJ5IGFuZCBzYWZldHktY3JpdGljYWwgYXBwbGljYXRpb25zIChsaWtlIGNpdmlsIGF2aWF0aW9uKS5cbiAgICAgICAgICAgICBUaGUgZmlyc3QgdmVyc2lvbiBhcHBlYXJlZCBpbiB0aGUgODBzLCBidXQgaXQncyBzdGlsbCBhY3RpdmVseSBkZXZlbG9wZWQgdG9kYXkgd2l0aFxuICAgICAgICAgICAgIHRoZSBuZXdlc3Qgc3RhbmRhcmQgYmVpbmcgQWRhMjAxMi5cbiovXG5cbi8vIFdlIHRyeSB0byBzdXBwb3J0IGZ1bGwgQWRhMjAxMlxuLy9cbi8vIFdlIGhpZ2hsaWdodCBhbGwgYXBwZWFyYW5jZXMgb2YgdHlwZXMsIGtleXdvcmRzLCBsaXRlcmFscyAoc3RyaW5nLCBjaGFyLCBudW1iZXIsIGJvb2wpXG4vLyBhbmQgdGl0bGVzICh1c2VyIGRlZmluZWQgZnVuY3Rpb24vcHJvY2VkdXJlL3BhY2thZ2UpXG4vLyBDU1MgY2xhc3NlcyBhcmUgc2V0IGFjY29yZGluZ2x5XG4vL1xuLy8gTGFuZ3VhZ2VzIGNhdXNpbmcgcHJvYmxlbXMgZm9yIGxhbmd1YWdlIGRldGVjdGlvbjpcbi8vIHhtbCAoYnJva2VuIGJ5IEZvbyA6IEJhciB0eXBlKSwgZWxtIChicm9rZW4gYnkgRm9vIDogQmFyIHR5cGUpLCB2YnNjcmlwdC1odG1sIChicm9rZW4gYnkgYm9keSBrZXl3b3JkKVxuLy8gc3FsIChhZGEgZGVmYXVsdC50eHQgaGFzIGEgbG90IG9mIHNxbCBrZXl3b3JkcylcblxuLyoqIEB0eXBlIExhbmd1YWdlRm4gKi9cbmZ1bmN0aW9uIGFkYShobGpzKSB7XG4gIC8vIFJlZ3VsYXIgZXhwcmVzc2lvbiBmb3IgQWRhIG51bWVyaWMgbGl0ZXJhbHMuXG4gIC8vIHN0b2xlbiBmb3JtIHRoZSBWSERMIGhpZ2hsaWdodGVyXG5cbiAgLy8gRGVjaW1hbCBsaXRlcmFsOlxuICBjb25zdCBJTlRFR0VSX1JFID0gJ1xcXFxkKF98XFxcXGQpKic7XG4gIGNvbnN0IEVYUE9ORU5UX1JFID0gJ1tlRV1bLStdPycgKyBJTlRFR0VSX1JFO1xuICBjb25zdCBERUNJTUFMX0xJVEVSQUxfUkUgPSBJTlRFR0VSX1JFICsgJyhcXFxcLicgKyBJTlRFR0VSX1JFICsgJyk/JyArICcoJyArIEVYUE9ORU5UX1JFICsgJyk/JztcblxuICAvLyBCYXNlZCBsaXRlcmFsOlxuICBjb25zdCBCQVNFRF9JTlRFR0VSX1JFID0gJ1xcXFx3Kyc7XG4gIGNvbnN0IEJBU0VEX0xJVEVSQUxfUkUgPSBJTlRFR0VSX1JFICsgJyMnICsgQkFTRURfSU5URUdFUl9SRSArICcoXFxcXC4nICsgQkFTRURfSU5URUdFUl9SRSArICcpPycgKyAnIycgKyAnKCcgKyBFWFBPTkVOVF9SRSArICcpPyc7XG5cbiAgY29uc3QgTlVNQkVSX1JFID0gJ1xcXFxiKCcgKyBCQVNFRF9MSVRFUkFMX1JFICsgJ3wnICsgREVDSU1BTF9MSVRFUkFMX1JFICsgJyknO1xuXG4gIC8vIElkZW50aWZpZXIgcmVnZXhcbiAgY29uc3QgSURfUkVHRVggPSAnW0EtWmEtel0oXz9bQS1aYS16MC05Ll0pKic7XG5cbiAgLy8gYmFkIGNoYXJzLCBvbmx5IGFsbG93ZWQgaW4gbGl0ZXJhbHNcbiAgY29uc3QgQkFEX0NIQVJTID0gYFtdXFxcXHtcXFxcfSUjJ1wiYDtcblxuICAvLyBBZGEgZG9lc24ndCBoYXZlIGJsb2NrIGNvbW1lbnRzLCBvbmx5IGxpbmUgY29tbWVudHNcbiAgY29uc3QgQ09NTUVOVFMgPSBobGpzLkNPTU1FTlQoJy0tJywgJyQnKTtcblxuICAvLyB2YXJpYWJsZSBkZWNsYXJhdGlvbnMgb2YgdGhlIGZvcm1cbiAgLy8gRm9vIDogQmFyIDo9IEJhejtcbiAgLy8gd2hlcmUgb25seSBCYXIgd2lsbCBiZSBoaWdobGlnaHRlZFxuICBjb25zdCBWQVJfREVDTFMgPSB7XG4gICAgLy8gVE9ETzogVGhlc2Ugc3BhY2VzIGFyZSBub3QgcmVxdWlyZWQgYnkgdGhlIEFkYSBzeW50YXhcbiAgICAvLyBob3dldmVyLCBJIGhhdmUgeWV0IHRvIHNlZSBoYW5kd3JpdHRlbiBBZGEgY29kZSB3aGVyZVxuICAgIC8vIHNvbWVvbmUgZG9lcyBub3QgcHV0IHNwYWNlcyBhcm91bmQgOlxuICAgIGJlZ2luOiAnXFxcXHMrOlxcXFxzKycsXG4gICAgZW5kOiAnXFxcXHMqKDo9fDt8XFxcXCl8PT58JCknLFxuICAgIC8vIGVuZHNXaXRoUGFyZW50OiB0cnVlLFxuICAgIC8vIHJldHVybkJlZ2luOiB0cnVlLFxuICAgIGlsbGVnYWw6IEJBRF9DSEFSUyxcbiAgICBjb250YWluczogW1xuICAgICAge1xuICAgICAgICAvLyB3b3JrYXJvdW5kIHRvIGF2b2lkIGhpZ2hsaWdodGluZ1xuICAgICAgICAvLyBuYW1lZCBsb29wcyBhbmQgZGVjbGFyZSBibG9ja3NcbiAgICAgICAgYmVnaW5LZXl3b3JkczogJ2xvb3AgZm9yIGRlY2xhcmUgb3RoZXJzJyxcbiAgICAgICAgZW5kc1BhcmVudDogdHJ1ZVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgLy8gcHJvcGVybHkgaGlnaGxpZ2h0IGFsbCBtb2RpZmllcnNcbiAgICAgICAgY2xhc3NOYW1lOiAna2V5d29yZCcsXG4gICAgICAgIGJlZ2luS2V5d29yZHM6ICdub3QgbnVsbCBjb25zdGFudCBhY2Nlc3MgZnVuY3Rpb24gcHJvY2VkdXJlIGluIG91dCBhbGlhc2VkIGV4Y2VwdGlvbidcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3R5cGUnLFxuICAgICAgICBiZWdpbjogSURfUkVHRVgsXG4gICAgICAgIGVuZHNQYXJlbnQ6IHRydWUsXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfVxuICAgIF1cbiAgfTtcblxuICByZXR1cm4ge1xuICAgIG5hbWU6ICdBZGEnLFxuICAgIGNhc2VfaW5zZW5zaXRpdmU6IHRydWUsXG4gICAga2V5d29yZHM6IHtcbiAgICAgIGtleXdvcmQ6XG4gICAgICAgICAgICAgICAgJ2Fib3J0IGVsc2UgbmV3IHJldHVybiBhYnMgZWxzaWYgbm90IHJldmVyc2UgYWJzdHJhY3QgZW5kICcgK1xuICAgICAgICAgICAgICAgICdhY2NlcHQgZW50cnkgc2VsZWN0IGFjY2VzcyBleGNlcHRpb24gb2Ygc2VwYXJhdGUgYWxpYXNlZCBleGl0IG9yIHNvbWUgJyArXG4gICAgICAgICAgICAgICAgJ2FsbCBvdGhlcnMgc3VidHlwZSBhbmQgZm9yIG91dCBzeW5jaHJvbml6ZWQgYXJyYXkgZnVuY3Rpb24gb3ZlcnJpZGluZyAnICtcbiAgICAgICAgICAgICAgICAnYXQgdGFnZ2VkIGdlbmVyaWMgcGFja2FnZSB0YXNrIGJlZ2luIGdvdG8gcHJhZ21hIHRlcm1pbmF0ZSAnICtcbiAgICAgICAgICAgICAgICAnYm9keSBwcml2YXRlIHRoZW4gaWYgcHJvY2VkdXJlIHR5cGUgY2FzZSBpbiBwcm90ZWN0ZWQgY29uc3RhbnQgaW50ZXJmYWNlICcgK1xuICAgICAgICAgICAgICAgICdpcyByYWlzZSB1c2UgZGVjbGFyZSByYW5nZSBkZWxheSBsaW1pdGVkIHJlY29yZCB3aGVuIGRlbHRhIGxvb3AgcmVtIHdoaWxlICcgK1xuICAgICAgICAgICAgICAgICdkaWdpdHMgcmVuYW1lcyB3aXRoIGRvIG1vZCByZXF1ZXVlIHhvcicsXG4gICAgICBsaXRlcmFsOlxuICAgICAgICAgICAgICAgICdUcnVlIEZhbHNlJ1xuICAgIH0sXG4gICAgY29udGFpbnM6IFtcbiAgICAgIENPTU1FTlRTLFxuICAgICAgLy8gc3RyaW5ncyBcImZvb2JhclwiXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3N0cmluZycsXG4gICAgICAgIGJlZ2luOiAvXCIvLFxuICAgICAgICBlbmQ6IC9cIi8sXG4gICAgICAgIGNvbnRhaW5zOiBbe1xuICAgICAgICAgIGJlZ2luOiAvXCJcIi8sXG4gICAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICAgIH1dXG4gICAgICB9LFxuICAgICAgLy8gY2hhcmFjdGVycyAnJ1xuICAgICAge1xuICAgICAgICAvLyBjaGFyYWN0ZXIgbGl0ZXJhbHMgYWx3YXlzIGNvbnRhaW4gb25lIGNoYXJcbiAgICAgICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICAgICAgYmVnaW46IC8nLicvXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICAvLyBudW1iZXIgbGl0ZXJhbHNcbiAgICAgICAgY2xhc3NOYW1lOiAnbnVtYmVyJyxcbiAgICAgICAgYmVnaW46IE5VTUJFUl9SRSxcbiAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICAvLyBBdHRyaWJ1dGVzXG4gICAgICAgIGNsYXNzTmFtZTogJ3N5bWJvbCcsXG4gICAgICAgIGJlZ2luOiBcIidcIiArIElEX1JFR0VYXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICAvLyBwYWNrYWdlIGRlZmluaXRpb24sIG1heWJlIGluc2lkZSBnZW5lcmljXG4gICAgICAgIGNsYXNzTmFtZTogJ3RpdGxlJyxcbiAgICAgICAgYmVnaW46ICcoXFxcXGJ3aXRoXFxcXHMrKT8oXFxcXGJwcml2YXRlXFxcXHMrKT9cXFxcYnBhY2thZ2VcXFxccysoXFxcXGJib2R5XFxcXHMrKT8nLFxuICAgICAgICBlbmQ6ICcoaXN8JCknLFxuICAgICAgICBrZXl3b3JkczogJ3BhY2thZ2UgYm9keScsXG4gICAgICAgIGV4Y2x1ZGVCZWdpbjogdHJ1ZSxcbiAgICAgICAgZXhjbHVkZUVuZDogdHJ1ZSxcbiAgICAgICAgaWxsZWdhbDogQkFEX0NIQVJTXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICAvLyBmdW5jdGlvbi9wcm9jZWR1cmUgZGVjbGFyYXRpb24vZGVmaW5pdGlvblxuICAgICAgICAvLyBtYXliZSBpbnNpZGUgZ2VuZXJpY1xuICAgICAgICBiZWdpbjogJyhcXFxcYih3aXRofG92ZXJyaWRpbmcpXFxcXHMrKT9cXFxcYihmdW5jdGlvbnxwcm9jZWR1cmUpXFxcXHMrJyxcbiAgICAgICAgZW5kOiAnKFxcXFxiaXN8XFxcXGJ3aXRofFxcXFxicmVuYW1lc3xcXFxcKVxcXFxzKjspJyxcbiAgICAgICAga2V5d29yZHM6ICdvdmVycmlkaW5nIGZ1bmN0aW9uIHByb2NlZHVyZSB3aXRoIGlzIHJlbmFtZXMgcmV0dXJuJyxcbiAgICAgICAgLy8gd2UgbmVlZCB0byByZS1tYXRjaCB0aGUgJ2Z1bmN0aW9uJyBrZXl3b3JkLCBzbyB0aGF0XG4gICAgICAgIC8vIHRoZSB0aXRsZSBtb2RlIGJlbG93IG1hdGNoZXMgb25seSBleGFjdGx5IG9uY2VcbiAgICAgICAgcmV0dXJuQmVnaW46IHRydWUsXG4gICAgICAgIGNvbnRhaW5zOlxuICAgICAgICAgICAgICAgIFtcbiAgICAgICAgICAgICAgICAgIENPTU1FTlRTLFxuICAgICAgICAgICAgICAgICAge1xuICAgICAgICAgICAgICAgICAgICAvLyBuYW1lIG9mIHRoZSBmdW5jdGlvbi9wcm9jZWR1cmVcbiAgICAgICAgICAgICAgICAgICAgY2xhc3NOYW1lOiAndGl0bGUnLFxuICAgICAgICAgICAgICAgICAgICBiZWdpbjogJyhcXFxcYndpdGhcXFxccyspP1xcXFxiKGZ1bmN0aW9ufHByb2NlZHVyZSlcXFxccysnLFxuICAgICAgICAgICAgICAgICAgICBlbmQ6ICcoXFxcXCh8XFxcXHMrfCQpJyxcbiAgICAgICAgICAgICAgICAgICAgZXhjbHVkZUJlZ2luOiB0cnVlLFxuICAgICAgICAgICAgICAgICAgICBleGNsdWRlRW5kOiB0cnVlLFxuICAgICAgICAgICAgICAgICAgICBpbGxlZ2FsOiBCQURfQ0hBUlNcbiAgICAgICAgICAgICAgICAgIH0sXG4gICAgICAgICAgICAgICAgICAvLyAnc2VsZidcbiAgICAgICAgICAgICAgICAgIC8vIC8vIHBhcmFtZXRlciB0eXBlc1xuICAgICAgICAgICAgICAgICAgVkFSX0RFQ0xTLFxuICAgICAgICAgICAgICAgICAge1xuICAgICAgICAgICAgICAgICAgICAvLyByZXR1cm4gdHlwZVxuICAgICAgICAgICAgICAgICAgICBjbGFzc05hbWU6ICd0eXBlJyxcbiAgICAgICAgICAgICAgICAgICAgYmVnaW46ICdcXFxcYnJldHVyblxcXFxzKycsXG4gICAgICAgICAgICAgICAgICAgIGVuZDogJyhcXFxccyt8O3wkKScsXG4gICAgICAgICAgICAgICAgICAgIGtleXdvcmRzOiAncmV0dXJuJyxcbiAgICAgICAgICAgICAgICAgICAgZXhjbHVkZUJlZ2luOiB0cnVlLFxuICAgICAgICAgICAgICAgICAgICBleGNsdWRlRW5kOiB0cnVlLFxuICAgICAgICAgICAgICAgICAgICAvLyB3ZSBhcmUgZG9uZSB3aXRoIGZ1bmN0aW9uc1xuICAgICAgICAgICAgICAgICAgICBlbmRzUGFyZW50OiB0cnVlLFxuICAgICAgICAgICAgICAgICAgICBpbGxlZ2FsOiBCQURfQ0hBUlNcblxuICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIF1cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIC8vIG5ldyB0eXBlIGRlY2xhcmF0aW9uc1xuICAgICAgICAvLyBtYXliZSBpbnNpZGUgZ2VuZXJpY1xuICAgICAgICBjbGFzc05hbWU6ICd0eXBlJyxcbiAgICAgICAgYmVnaW46ICdcXFxcYihzdWIpP3R5cGVcXFxccysnLFxuICAgICAgICBlbmQ6ICdcXFxccysnLFxuICAgICAgICBrZXl3b3JkczogJ3R5cGUnLFxuICAgICAgICBleGNsdWRlQmVnaW46IHRydWUsXG4gICAgICAgIGlsbGVnYWw6IEJBRF9DSEFSU1xuICAgICAgfSxcblxuICAgICAgLy8gc2VlIGNvbW1lbnQgYWJvdmUgdGhlIGRlZmluaXRpb25cbiAgICAgIFZBUl9ERUNMU1xuXG4gICAgICAvLyBubyBtYXJrdXBcbiAgICAgIC8vIHJlbGV2YW5jZSBib29zdGVycyBmb3Igc21hbGwgc25pcHBldHNcbiAgICAgIC8vIHtiZWdpbjogJ1xcXFxzKj0+XFxcXHMqJ30sXG4gICAgICAvLyB7YmVnaW46ICdcXFxccyo6PVxcXFxzKid9LFxuICAgICAgLy8ge2JlZ2luOiAnXFxcXHMrOj1cXFxccysnfSxcbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gYWRhO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9