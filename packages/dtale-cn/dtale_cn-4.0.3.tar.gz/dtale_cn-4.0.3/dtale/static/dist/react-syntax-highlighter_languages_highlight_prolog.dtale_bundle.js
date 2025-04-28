(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_prolog"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/prolog.js":
/*!*************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/prolog.js ***!
  \*************************************************************************************************/
/***/ ((module) => {

/*
Language: Prolog
Description: Prolog is a general purpose logic programming language associated with artificial intelligence and computational linguistics.
Author: Raivo Laanemets <raivo@infdot.com>
Website: https://en.wikipedia.org/wiki/Prolog
*/

function prolog(hljs) {
  const ATOM = {

    begin: /[a-z][A-Za-z0-9_]*/,
    relevance: 0
  };

  const VAR = {

    className: 'symbol',
    variants: [
      {
        begin: /[A-Z][a-zA-Z0-9_]*/
      },
      {
        begin: /_[A-Za-z0-9_]*/
      }
    ],
    relevance: 0
  };

  const PARENTED = {

    begin: /\(/,
    end: /\)/,
    relevance: 0
  };

  const LIST = {

    begin: /\[/,
    end: /\]/
  };

  const LINE_COMMENT = {

    className: 'comment',
    begin: /%/,
    end: /$/,
    contains: [ hljs.PHRASAL_WORDS_MODE ]
  };

  const BACKTICK_STRING = {

    className: 'string',
    begin: /`/,
    end: /`/,
    contains: [ hljs.BACKSLASH_ESCAPE ]
  };

  const CHAR_CODE = {
    className: 'string', // 0'a etc.
    begin: /0'(\\'|.)/
  };

  const SPACE_CODE = {
    className: 'string',
    begin: /0'\\s/ // 0'\s
  };

  const PRED_OP = { // relevance booster
    begin: /:-/
  };

  const inner = [

    ATOM,
    VAR,
    PARENTED,
    PRED_OP,
    LIST,
    LINE_COMMENT,
    hljs.C_BLOCK_COMMENT_MODE,
    hljs.QUOTE_STRING_MODE,
    hljs.APOS_STRING_MODE,
    BACKTICK_STRING,
    CHAR_CODE,
    SPACE_CODE,
    hljs.C_NUMBER_MODE
  ];

  PARENTED.contains = inner;
  LIST.contains = inner;

  return {
    name: 'Prolog',
    contains: inner.concat([
      { // relevance booster
        begin: /\.$/
      }
    ])
  };
}

module.exports = prolog;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfcHJvbG9nLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTs7QUFFQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7O0FBRUE7QUFDQTtBQUNBOztBQUVBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQSxvQkFBb0I7QUFDcEI7QUFDQTs7QUFFQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0EsUUFBUTtBQUNSO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL3Byb2xvZy5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKlxuTGFuZ3VhZ2U6IFByb2xvZ1xuRGVzY3JpcHRpb246IFByb2xvZyBpcyBhIGdlbmVyYWwgcHVycG9zZSBsb2dpYyBwcm9ncmFtbWluZyBsYW5ndWFnZSBhc3NvY2lhdGVkIHdpdGggYXJ0aWZpY2lhbCBpbnRlbGxpZ2VuY2UgYW5kIGNvbXB1dGF0aW9uYWwgbGluZ3Vpc3RpY3MuXG5BdXRob3I6IFJhaXZvIExhYW5lbWV0cyA8cmFpdm9AaW5mZG90LmNvbT5cbldlYnNpdGU6IGh0dHBzOi8vZW4ud2lraXBlZGlhLm9yZy93aWtpL1Byb2xvZ1xuKi9cblxuZnVuY3Rpb24gcHJvbG9nKGhsanMpIHtcbiAgY29uc3QgQVRPTSA9IHtcblxuICAgIGJlZ2luOiAvW2Etel1bQS1aYS16MC05X10qLyxcbiAgICByZWxldmFuY2U6IDBcbiAgfTtcblxuICBjb25zdCBWQVIgPSB7XG5cbiAgICBjbGFzc05hbWU6ICdzeW1ib2wnLFxuICAgIHZhcmlhbnRzOiBbXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAvW0EtWl1bYS16QS1aMC05X10qL1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC9fW0EtWmEtejAtOV9dKi9cbiAgICAgIH1cbiAgICBdLFxuICAgIHJlbGV2YW5jZTogMFxuICB9O1xuXG4gIGNvbnN0IFBBUkVOVEVEID0ge1xuXG4gICAgYmVnaW46IC9cXCgvLFxuICAgIGVuZDogL1xcKS8sXG4gICAgcmVsZXZhbmNlOiAwXG4gIH07XG5cbiAgY29uc3QgTElTVCA9IHtcblxuICAgIGJlZ2luOiAvXFxbLyxcbiAgICBlbmQ6IC9cXF0vXG4gIH07XG5cbiAgY29uc3QgTElORV9DT01NRU5UID0ge1xuXG4gICAgY2xhc3NOYW1lOiAnY29tbWVudCcsXG4gICAgYmVnaW46IC8lLyxcbiAgICBlbmQ6IC8kLyxcbiAgICBjb250YWluczogWyBobGpzLlBIUkFTQUxfV09SRFNfTU9ERSBdXG4gIH07XG5cbiAgY29uc3QgQkFDS1RJQ0tfU1RSSU5HID0ge1xuXG4gICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICBiZWdpbjogL2AvLFxuICAgIGVuZDogL2AvLFxuICAgIGNvbnRhaW5zOiBbIGhsanMuQkFDS1NMQVNIX0VTQ0FQRSBdXG4gIH07XG5cbiAgY29uc3QgQ0hBUl9DT0RFID0ge1xuICAgIGNsYXNzTmFtZTogJ3N0cmluZycsIC8vIDAnYSBldGMuXG4gICAgYmVnaW46IC8wJyhcXFxcJ3wuKS9cbiAgfTtcblxuICBjb25zdCBTUEFDRV9DT0RFID0ge1xuICAgIGNsYXNzTmFtZTogJ3N0cmluZycsXG4gICAgYmVnaW46IC8wJ1xcXFxzLyAvLyAwJ1xcc1xuICB9O1xuXG4gIGNvbnN0IFBSRURfT1AgPSB7IC8vIHJlbGV2YW5jZSBib29zdGVyXG4gICAgYmVnaW46IC86LS9cbiAgfTtcblxuICBjb25zdCBpbm5lciA9IFtcblxuICAgIEFUT00sXG4gICAgVkFSLFxuICAgIFBBUkVOVEVELFxuICAgIFBSRURfT1AsXG4gICAgTElTVCxcbiAgICBMSU5FX0NPTU1FTlQsXG4gICAgaGxqcy5DX0JMT0NLX0NPTU1FTlRfTU9ERSxcbiAgICBobGpzLlFVT1RFX1NUUklOR19NT0RFLFxuICAgIGhsanMuQVBPU19TVFJJTkdfTU9ERSxcbiAgICBCQUNLVElDS19TVFJJTkcsXG4gICAgQ0hBUl9DT0RFLFxuICAgIFNQQUNFX0NPREUsXG4gICAgaGxqcy5DX05VTUJFUl9NT0RFXG4gIF07XG5cbiAgUEFSRU5URUQuY29udGFpbnMgPSBpbm5lcjtcbiAgTElTVC5jb250YWlucyA9IGlubmVyO1xuXG4gIHJldHVybiB7XG4gICAgbmFtZTogJ1Byb2xvZycsXG4gICAgY29udGFpbnM6IGlubmVyLmNvbmNhdChbXG4gICAgICB7IC8vIHJlbGV2YW5jZSBib29zdGVyXG4gICAgICAgIGJlZ2luOiAvXFwuJC9cbiAgICAgIH1cbiAgICBdKVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IHByb2xvZztcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==