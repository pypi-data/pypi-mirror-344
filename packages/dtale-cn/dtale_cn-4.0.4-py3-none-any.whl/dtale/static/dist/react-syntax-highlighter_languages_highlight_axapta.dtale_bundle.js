(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_axapta"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/axapta.js":
/*!*************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/axapta.js ***!
  \*************************************************************************************************/
/***/ ((module) => {

/*
Language: Microsoft X++
Description: X++ is a language used in Microsoft Dynamics 365, Dynamics AX, and Axapta.
Author: Dmitri Roudakov <dmitri@roudakov.ru>
Website: https://dynamics.microsoft.com/en-us/ax-overview/
Category: enterprise
*/

/** @type LanguageFn */
function axapta(hljs) {
  const BUILT_IN_KEYWORDS = [
    'anytype',
    'boolean',
    'byte',
    'char',
    'container',
    'date',
    'double',
    'enum',
    'guid',
    'int',
    'int64',
    'long',
    'real',
    'short',
    'str',
    'utcdatetime',
    'var'
  ];

  const LITERAL_KEYWORDS = [
    'default',
    'false',
    'null',
    'true'
  ];

  const NORMAL_KEYWORDS = [
    'abstract',
    'as',
    'asc',
    'avg',
    'break',
    'breakpoint',
    'by',
    'byref',
    'case',
    'catch',
    'changecompany',
    'class',
    'client',
    'client',
    'common',
    'const',
    'continue',
    'count',
    'crosscompany',
    'delegate',
    'delete_from',
    'desc',
    'display',
    'div',
    'do',
    'edit',
    'else',
    'eventhandler',
    'exists',
    'extends',
    'final',
    'finally',
    'firstfast',
    'firstonly',
    'firstonly1',
    'firstonly10',
    'firstonly100',
    'firstonly1000',
    'flush',
    'for',
    'forceliterals',
    'forcenestedloop',
    'forceplaceholders',
    'forceselectorder',
    'forupdate',
    'from',
    'generateonly',
    'group',
    'hint',
    'if',
    'implements',
    'in',
    'index',
    'insert_recordset',
    'interface',
    'internal',
    'is',
    'join',
    'like',
    'maxof',
    'minof',
    'mod',
    'namespace',
    'new',
    'next',
    'nofetch',
    'notexists',
    'optimisticlock',
    'order',
    'outer',
    'pessimisticlock',
    'print',
    'private',
    'protected',
    'public',
    'readonly',
    'repeatableread',
    'retry',
    'return',
    'reverse',
    'select',
    'server',
    'setting',
    'static',
    'sum',
    'super',
    'switch',
    'this',
    'throw',
    'try',
    'ttsabort',
    'ttsbegin',
    'ttscommit',
    'unchecked',
    'update_recordset',
    'using',
    'validtimestate',
    'void',
    'where',
    'while'
  ];

  const KEYWORDS = {
    keyword: NORMAL_KEYWORDS,
    built_in: BUILT_IN_KEYWORDS,
    literal: LITERAL_KEYWORDS
  };

  return {
    name: 'X++',
    aliases: ['x++'],
    keywords: KEYWORDS,
    contains: [
      hljs.C_LINE_COMMENT_MODE,
      hljs.C_BLOCK_COMMENT_MODE,
      hljs.APOS_STRING_MODE,
      hljs.QUOTE_STRING_MODE,
      hljs.C_NUMBER_MODE,
      {
        className: 'meta',
        begin: '#',
        end: '$'
      },
      {
        className: 'class',
        beginKeywords: 'class interface',
        end: /\{/,
        excludeEnd: true,
        illegal: ':',
        contains: [
          {
            beginKeywords: 'extends implements'
          },
          hljs.UNDERSCORE_TITLE_MODE
        ]
      }
    ]
  };
}

module.exports = axapta;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfYXhhcHRhLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSxnQkFBZ0I7QUFDaEI7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFdBQVc7QUFDWDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL2F4YXB0YS5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKlxuTGFuZ3VhZ2U6IE1pY3Jvc29mdCBYKytcbkRlc2NyaXB0aW9uOiBYKysgaXMgYSBsYW5ndWFnZSB1c2VkIGluIE1pY3Jvc29mdCBEeW5hbWljcyAzNjUsIER5bmFtaWNzIEFYLCBhbmQgQXhhcHRhLlxuQXV0aG9yOiBEbWl0cmkgUm91ZGFrb3YgPGRtaXRyaUByb3VkYWtvdi5ydT5cbldlYnNpdGU6IGh0dHBzOi8vZHluYW1pY3MubWljcm9zb2Z0LmNvbS9lbi11cy9heC1vdmVydmlldy9cbkNhdGVnb3J5OiBlbnRlcnByaXNlXG4qL1xuXG4vKiogQHR5cGUgTGFuZ3VhZ2VGbiAqL1xuZnVuY3Rpb24gYXhhcHRhKGhsanMpIHtcbiAgY29uc3QgQlVJTFRfSU5fS0VZV09SRFMgPSBbXG4gICAgJ2FueXR5cGUnLFxuICAgICdib29sZWFuJyxcbiAgICAnYnl0ZScsXG4gICAgJ2NoYXInLFxuICAgICdjb250YWluZXInLFxuICAgICdkYXRlJyxcbiAgICAnZG91YmxlJyxcbiAgICAnZW51bScsXG4gICAgJ2d1aWQnLFxuICAgICdpbnQnLFxuICAgICdpbnQ2NCcsXG4gICAgJ2xvbmcnLFxuICAgICdyZWFsJyxcbiAgICAnc2hvcnQnLFxuICAgICdzdHInLFxuICAgICd1dGNkYXRldGltZScsXG4gICAgJ3ZhcidcbiAgXTtcblxuICBjb25zdCBMSVRFUkFMX0tFWVdPUkRTID0gW1xuICAgICdkZWZhdWx0JyxcbiAgICAnZmFsc2UnLFxuICAgICdudWxsJyxcbiAgICAndHJ1ZSdcbiAgXTtcblxuICBjb25zdCBOT1JNQUxfS0VZV09SRFMgPSBbXG4gICAgJ2Fic3RyYWN0JyxcbiAgICAnYXMnLFxuICAgICdhc2MnLFxuICAgICdhdmcnLFxuICAgICdicmVhaycsXG4gICAgJ2JyZWFrcG9pbnQnLFxuICAgICdieScsXG4gICAgJ2J5cmVmJyxcbiAgICAnY2FzZScsXG4gICAgJ2NhdGNoJyxcbiAgICAnY2hhbmdlY29tcGFueScsXG4gICAgJ2NsYXNzJyxcbiAgICAnY2xpZW50JyxcbiAgICAnY2xpZW50JyxcbiAgICAnY29tbW9uJyxcbiAgICAnY29uc3QnLFxuICAgICdjb250aW51ZScsXG4gICAgJ2NvdW50JyxcbiAgICAnY3Jvc3Njb21wYW55JyxcbiAgICAnZGVsZWdhdGUnLFxuICAgICdkZWxldGVfZnJvbScsXG4gICAgJ2Rlc2MnLFxuICAgICdkaXNwbGF5JyxcbiAgICAnZGl2JyxcbiAgICAnZG8nLFxuICAgICdlZGl0JyxcbiAgICAnZWxzZScsXG4gICAgJ2V2ZW50aGFuZGxlcicsXG4gICAgJ2V4aXN0cycsXG4gICAgJ2V4dGVuZHMnLFxuICAgICdmaW5hbCcsXG4gICAgJ2ZpbmFsbHknLFxuICAgICdmaXJzdGZhc3QnLFxuICAgICdmaXJzdG9ubHknLFxuICAgICdmaXJzdG9ubHkxJyxcbiAgICAnZmlyc3Rvbmx5MTAnLFxuICAgICdmaXJzdG9ubHkxMDAnLFxuICAgICdmaXJzdG9ubHkxMDAwJyxcbiAgICAnZmx1c2gnLFxuICAgICdmb3InLFxuICAgICdmb3JjZWxpdGVyYWxzJyxcbiAgICAnZm9yY2VuZXN0ZWRsb29wJyxcbiAgICAnZm9yY2VwbGFjZWhvbGRlcnMnLFxuICAgICdmb3JjZXNlbGVjdG9yZGVyJyxcbiAgICAnZm9ydXBkYXRlJyxcbiAgICAnZnJvbScsXG4gICAgJ2dlbmVyYXRlb25seScsXG4gICAgJ2dyb3VwJyxcbiAgICAnaGludCcsXG4gICAgJ2lmJyxcbiAgICAnaW1wbGVtZW50cycsXG4gICAgJ2luJyxcbiAgICAnaW5kZXgnLFxuICAgICdpbnNlcnRfcmVjb3Jkc2V0JyxcbiAgICAnaW50ZXJmYWNlJyxcbiAgICAnaW50ZXJuYWwnLFxuICAgICdpcycsXG4gICAgJ2pvaW4nLFxuICAgICdsaWtlJyxcbiAgICAnbWF4b2YnLFxuICAgICdtaW5vZicsXG4gICAgJ21vZCcsXG4gICAgJ25hbWVzcGFjZScsXG4gICAgJ25ldycsXG4gICAgJ25leHQnLFxuICAgICdub2ZldGNoJyxcbiAgICAnbm90ZXhpc3RzJyxcbiAgICAnb3B0aW1pc3RpY2xvY2snLFxuICAgICdvcmRlcicsXG4gICAgJ291dGVyJyxcbiAgICAncGVzc2ltaXN0aWNsb2NrJyxcbiAgICAncHJpbnQnLFxuICAgICdwcml2YXRlJyxcbiAgICAncHJvdGVjdGVkJyxcbiAgICAncHVibGljJyxcbiAgICAncmVhZG9ubHknLFxuICAgICdyZXBlYXRhYmxlcmVhZCcsXG4gICAgJ3JldHJ5JyxcbiAgICAncmV0dXJuJyxcbiAgICAncmV2ZXJzZScsXG4gICAgJ3NlbGVjdCcsXG4gICAgJ3NlcnZlcicsXG4gICAgJ3NldHRpbmcnLFxuICAgICdzdGF0aWMnLFxuICAgICdzdW0nLFxuICAgICdzdXBlcicsXG4gICAgJ3N3aXRjaCcsXG4gICAgJ3RoaXMnLFxuICAgICd0aHJvdycsXG4gICAgJ3RyeScsXG4gICAgJ3R0c2Fib3J0JyxcbiAgICAndHRzYmVnaW4nLFxuICAgICd0dHNjb21taXQnLFxuICAgICd1bmNoZWNrZWQnLFxuICAgICd1cGRhdGVfcmVjb3Jkc2V0JyxcbiAgICAndXNpbmcnLFxuICAgICd2YWxpZHRpbWVzdGF0ZScsXG4gICAgJ3ZvaWQnLFxuICAgICd3aGVyZScsXG4gICAgJ3doaWxlJ1xuICBdO1xuXG4gIGNvbnN0IEtFWVdPUkRTID0ge1xuICAgIGtleXdvcmQ6IE5PUk1BTF9LRVlXT1JEUyxcbiAgICBidWlsdF9pbjogQlVJTFRfSU5fS0VZV09SRFMsXG4gICAgbGl0ZXJhbDogTElURVJBTF9LRVlXT1JEU1xuICB9O1xuXG4gIHJldHVybiB7XG4gICAgbmFtZTogJ1grKycsXG4gICAgYWxpYXNlczogWyd4KysnXSxcbiAgICBrZXl3b3JkczogS0VZV09SRFMsXG4gICAgY29udGFpbnM6IFtcbiAgICAgIGhsanMuQ19MSU5FX0NPTU1FTlRfTU9ERSxcbiAgICAgIGhsanMuQ19CTE9DS19DT01NRU5UX01PREUsXG4gICAgICBobGpzLkFQT1NfU1RSSU5HX01PREUsXG4gICAgICBobGpzLlFVT1RFX1NUUklOR19NT0RFLFxuICAgICAgaGxqcy5DX05VTUJFUl9NT0RFLFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdtZXRhJyxcbiAgICAgICAgYmVnaW46ICcjJyxcbiAgICAgICAgZW5kOiAnJCdcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ2NsYXNzJyxcbiAgICAgICAgYmVnaW5LZXl3b3JkczogJ2NsYXNzIGludGVyZmFjZScsXG4gICAgICAgIGVuZDogL1xcey8sXG4gICAgICAgIGV4Y2x1ZGVFbmQ6IHRydWUsXG4gICAgICAgIGlsbGVnYWw6ICc6JyxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbktleXdvcmRzOiAnZXh0ZW5kcyBpbXBsZW1lbnRzJ1xuICAgICAgICAgIH0sXG4gICAgICAgICAgaGxqcy5VTkRFUlNDT1JFX1RJVExFX01PREVcbiAgICAgICAgXVxuICAgICAgfVxuICAgIF1cbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBheGFwdGE7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=