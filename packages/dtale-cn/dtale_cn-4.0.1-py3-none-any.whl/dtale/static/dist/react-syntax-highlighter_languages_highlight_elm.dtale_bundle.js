(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_elm"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/elm.js":
/*!**********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/elm.js ***!
  \**********************************************************************************************/
/***/ ((module) => {

/*
Language: Elm
Author: Janis Voigtlaender <janis.voigtlaender@gmail.com>
Website: https://elm-lang.org
Category: functional
*/

/** @type LanguageFn */
function elm(hljs) {
  const COMMENT = {
    variants: [
      hljs.COMMENT('--', '$'),
      hljs.COMMENT(
        /\{-/,
        /-\}/,
        {
          contains: ['self']
        }
      )
    ]
  };

  const CONSTRUCTOR = {
    className: 'type',
    begin: '\\b[A-Z][\\w\']*', // TODO: other constructors (built-in, infix).
    relevance: 0
  };

  const LIST = {
    begin: '\\(',
    end: '\\)',
    illegal: '"',
    contains: [
      {
        className: 'type',
        begin: '\\b[A-Z][\\w]*(\\((\\.\\.|,|\\w+)\\))?'
      },
      COMMENT
    ]
  };

  const RECORD = {
    begin: /\{/,
    end: /\}/,
    contains: LIST.contains
  };

  const CHARACTER = {
    className: 'string',
    begin: '\'\\\\?.',
    end: '\'',
    illegal: '.'
  };

  return {
    name: 'Elm',
    keywords:
      'let in if then else case of where module import exposing ' +
      'type alias as infix infixl infixr port effect command subscription',
    contains: [

      // Top-level constructions.

      {
        beginKeywords: 'port effect module',
        end: 'exposing',
        keywords: 'port effect module where command subscription exposing',
        contains: [
          LIST,
          COMMENT
        ],
        illegal: '\\W\\.|;'
      },
      {
        begin: 'import',
        end: '$',
        keywords: 'import as exposing',
        contains: [
          LIST,
          COMMENT
        ],
        illegal: '\\W\\.|;'
      },
      {
        begin: 'type',
        end: '$',
        keywords: 'type alias',
        contains: [
          CONSTRUCTOR,
          LIST,
          RECORD,
          COMMENT
        ]
      },
      {
        beginKeywords: 'infix infixl infixr',
        end: '$',
        contains: [
          hljs.C_NUMBER_MODE,
          COMMENT
        ]
      },
      {
        begin: 'port',
        end: '$',
        keywords: 'port',
        contains: [COMMENT]
      },

      // Literals and names.

      CHARACTER,
      hljs.QUOTE_STRING_MODE,
      hljs.C_NUMBER_MODE,
      CONSTRUCTOR,
      hljs.inherit(hljs.TITLE_MODE, {
        begin: '^[_a-z][\\w\']*'
      }),
      COMMENT,

      {
        begin: '->|<-'
      } // No markup, relevance booster
    ],
    illegal: /;/
  };
}

module.exports = elm;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfZWxtLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1gsWUFBWTtBQUNaO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBOztBQUVBO0FBQ0EsY0FBYztBQUNkLFlBQVk7QUFDWjtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLDBCQUEwQjtBQUMxQixPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLDBCQUEwQjtBQUMxQixPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87O0FBRVA7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQOztBQUVBO0FBQ0E7QUFDQSxRQUFRO0FBQ1I7QUFDQSxlQUFlO0FBQ2Y7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvZWxtLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogRWxtXG5BdXRob3I6IEphbmlzIFZvaWd0bGFlbmRlciA8amFuaXMudm9pZ3RsYWVuZGVyQGdtYWlsLmNvbT5cbldlYnNpdGU6IGh0dHBzOi8vZWxtLWxhbmcub3JnXG5DYXRlZ29yeTogZnVuY3Rpb25hbFxuKi9cblxuLyoqIEB0eXBlIExhbmd1YWdlRm4gKi9cbmZ1bmN0aW9uIGVsbShobGpzKSB7XG4gIGNvbnN0IENPTU1FTlQgPSB7XG4gICAgdmFyaWFudHM6IFtcbiAgICAgIGhsanMuQ09NTUVOVCgnLS0nLCAnJCcpLFxuICAgICAgaGxqcy5DT01NRU5UKFxuICAgICAgICAvXFx7LS8sXG4gICAgICAgIC8tXFx9LyxcbiAgICAgICAge1xuICAgICAgICAgIGNvbnRhaW5zOiBbJ3NlbGYnXVxuICAgICAgICB9XG4gICAgICApXG4gICAgXVxuICB9O1xuXG4gIGNvbnN0IENPTlNUUlVDVE9SID0ge1xuICAgIGNsYXNzTmFtZTogJ3R5cGUnLFxuICAgIGJlZ2luOiAnXFxcXGJbQS1aXVtcXFxcd1xcJ10qJywgLy8gVE9ETzogb3RoZXIgY29uc3RydWN0b3JzIChidWlsdC1pbiwgaW5maXgpLlxuICAgIHJlbGV2YW5jZTogMFxuICB9O1xuXG4gIGNvbnN0IExJU1QgPSB7XG4gICAgYmVnaW46ICdcXFxcKCcsXG4gICAgZW5kOiAnXFxcXCknLFxuICAgIGlsbGVnYWw6ICdcIicsXG4gICAgY29udGFpbnM6IFtcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAndHlwZScsXG4gICAgICAgIGJlZ2luOiAnXFxcXGJbQS1aXVtcXFxcd10qKFxcXFwoKFxcXFwuXFxcXC58LHxcXFxcdyspXFxcXCkpPydcbiAgICAgIH0sXG4gICAgICBDT01NRU5UXG4gICAgXVxuICB9O1xuXG4gIGNvbnN0IFJFQ09SRCA9IHtcbiAgICBiZWdpbjogL1xcey8sXG4gICAgZW5kOiAvXFx9LyxcbiAgICBjb250YWluczogTElTVC5jb250YWluc1xuICB9O1xuXG4gIGNvbnN0IENIQVJBQ1RFUiA9IHtcbiAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgIGJlZ2luOiAnXFwnXFxcXFxcXFw/LicsXG4gICAgZW5kOiAnXFwnJyxcbiAgICBpbGxlZ2FsOiAnLidcbiAgfTtcblxuICByZXR1cm4ge1xuICAgIG5hbWU6ICdFbG0nLFxuICAgIGtleXdvcmRzOlxuICAgICAgJ2xldCBpbiBpZiB0aGVuIGVsc2UgY2FzZSBvZiB3aGVyZSBtb2R1bGUgaW1wb3J0IGV4cG9zaW5nICcgK1xuICAgICAgJ3R5cGUgYWxpYXMgYXMgaW5maXggaW5maXhsIGluZml4ciBwb3J0IGVmZmVjdCBjb21tYW5kIHN1YnNjcmlwdGlvbicsXG4gICAgY29udGFpbnM6IFtcblxuICAgICAgLy8gVG9wLWxldmVsIGNvbnN0cnVjdGlvbnMuXG5cbiAgICAgIHtcbiAgICAgICAgYmVnaW5LZXl3b3JkczogJ3BvcnQgZWZmZWN0IG1vZHVsZScsXG4gICAgICAgIGVuZDogJ2V4cG9zaW5nJyxcbiAgICAgICAga2V5d29yZHM6ICdwb3J0IGVmZmVjdCBtb2R1bGUgd2hlcmUgY29tbWFuZCBzdWJzY3JpcHRpb24gZXhwb3NpbmcnLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIExJU1QsXG4gICAgICAgICAgQ09NTUVOVFxuICAgICAgICBdLFxuICAgICAgICBpbGxlZ2FsOiAnXFxcXFdcXFxcLnw7J1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICdpbXBvcnQnLFxuICAgICAgICBlbmQ6ICckJyxcbiAgICAgICAga2V5d29yZHM6ICdpbXBvcnQgYXMgZXhwb3NpbmcnLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIExJU1QsXG4gICAgICAgICAgQ09NTUVOVFxuICAgICAgICBdLFxuICAgICAgICBpbGxlZ2FsOiAnXFxcXFdcXFxcLnw7J1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICd0eXBlJyxcbiAgICAgICAgZW5kOiAnJCcsXG4gICAgICAgIGtleXdvcmRzOiAndHlwZSBhbGlhcycsXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgQ09OU1RSVUNUT1IsXG4gICAgICAgICAgTElTVCxcbiAgICAgICAgICBSRUNPUkQsXG4gICAgICAgICAgQ09NTUVOVFxuICAgICAgICBdXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbktleXdvcmRzOiAnaW5maXggaW5maXhsIGluZml4cicsXG4gICAgICAgIGVuZDogJyQnLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIGhsanMuQ19OVU1CRVJfTU9ERSxcbiAgICAgICAgICBDT01NRU5UXG4gICAgICAgIF1cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAncG9ydCcsXG4gICAgICAgIGVuZDogJyQnLFxuICAgICAgICBrZXl3b3JkczogJ3BvcnQnLFxuICAgICAgICBjb250YWluczogW0NPTU1FTlRdXG4gICAgICB9LFxuXG4gICAgICAvLyBMaXRlcmFscyBhbmQgbmFtZXMuXG5cbiAgICAgIENIQVJBQ1RFUixcbiAgICAgIGhsanMuUVVPVEVfU1RSSU5HX01PREUsXG4gICAgICBobGpzLkNfTlVNQkVSX01PREUsXG4gICAgICBDT05TVFJVQ1RPUixcbiAgICAgIGhsanMuaW5oZXJpdChobGpzLlRJVExFX01PREUsIHtcbiAgICAgICAgYmVnaW46ICdeW19hLXpdW1xcXFx3XFwnXSonXG4gICAgICB9KSxcbiAgICAgIENPTU1FTlQsXG5cbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICctPnw8LSdcbiAgICAgIH0gLy8gTm8gbWFya3VwLCByZWxldmFuY2UgYm9vc3RlclxuICAgIF0sXG4gICAgaWxsZWdhbDogLzsvXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gZWxtO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9