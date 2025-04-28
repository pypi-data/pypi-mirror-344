(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_gherkin"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/gherkin.js":
/*!**************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/gherkin.js ***!
  \**************************************************************************************************/
/***/ ((module) => {

/*
 Language: Gherkin
 Author: Sam Pikesley (@pikesley) <sam.pikesley@theodi.org>
 Description: Gherkin is the format for cucumber specifications. It is a domain specific language which helps you to describe business behavior without the need to go into detail of implementation.
 Website: https://cucumber.io/docs/gherkin/
 */

function gherkin(hljs) {
  return {
    name: 'Gherkin',
    aliases: ['feature'],
    keywords: 'Feature Background Ability Business\ Need Scenario Scenarios Scenario\ Outline Scenario\ Template Examples Given And Then But When',
    contains: [
      {
        className: 'symbol',
        begin: '\\*',
        relevance: 0
      },
      {
        className: 'meta',
        begin: '@[^@\\s]+'
      },
      {
        begin: '\\|',
        end: '\\|\\w*$',
        contains: [
          {
            className: 'string',
            begin: '[^|]+'
          }
        ]
      },
      {
        className: 'variable',
        begin: '<',
        end: '>'
      },
      hljs.HASH_COMMENT_MODE,
      {
        className: 'string',
        begin: '"""',
        end: '"""'
      },
      hljs.QUOTE_STRING_MODE
    ]
  };
}

module.exports = gherkin;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfZ2hlcmtpbi5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9naGVya2luLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG4gTGFuZ3VhZ2U6IEdoZXJraW5cbiBBdXRob3I6IFNhbSBQaWtlc2xleSAoQHBpa2VzbGV5KSA8c2FtLnBpa2VzbGV5QHRoZW9kaS5vcmc+XG4gRGVzY3JpcHRpb246IEdoZXJraW4gaXMgdGhlIGZvcm1hdCBmb3IgY3VjdW1iZXIgc3BlY2lmaWNhdGlvbnMuIEl0IGlzIGEgZG9tYWluIHNwZWNpZmljIGxhbmd1YWdlIHdoaWNoIGhlbHBzIHlvdSB0byBkZXNjcmliZSBidXNpbmVzcyBiZWhhdmlvciB3aXRob3V0IHRoZSBuZWVkIHRvIGdvIGludG8gZGV0YWlsIG9mIGltcGxlbWVudGF0aW9uLlxuIFdlYnNpdGU6IGh0dHBzOi8vY3VjdW1iZXIuaW8vZG9jcy9naGVya2luL1xuICovXG5cbmZ1bmN0aW9uIGdoZXJraW4oaGxqcykge1xuICByZXR1cm4ge1xuICAgIG5hbWU6ICdHaGVya2luJyxcbiAgICBhbGlhc2VzOiBbJ2ZlYXR1cmUnXSxcbiAgICBrZXl3b3JkczogJ0ZlYXR1cmUgQmFja2dyb3VuZCBBYmlsaXR5IEJ1c2luZXNzXFwgTmVlZCBTY2VuYXJpbyBTY2VuYXJpb3MgU2NlbmFyaW9cXCBPdXRsaW5lIFNjZW5hcmlvXFwgVGVtcGxhdGUgRXhhbXBsZXMgR2l2ZW4gQW5kIFRoZW4gQnV0IFdoZW4nLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3N5bWJvbCcsXG4gICAgICAgIGJlZ2luOiAnXFxcXConLFxuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ21ldGEnLFxuICAgICAgICBiZWdpbjogJ0BbXkBcXFxcc10rJ1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICdcXFxcfCcsXG4gICAgICAgIGVuZDogJ1xcXFx8XFxcXHcqJCcsXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICAgICAgICAgIGJlZ2luOiAnW158XSsnXG4gICAgICAgICAgfVxuICAgICAgICBdXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICd2YXJpYWJsZScsXG4gICAgICAgIGJlZ2luOiAnPCcsXG4gICAgICAgIGVuZDogJz4nXG4gICAgICB9LFxuICAgICAgaGxqcy5IQVNIX0NPTU1FTlRfTU9ERSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICAgICAgYmVnaW46ICdcIlwiXCInLFxuICAgICAgICBlbmQ6ICdcIlwiXCInXG4gICAgICB9LFxuICAgICAgaGxqcy5RVU9URV9TVFJJTkdfTU9ERVxuICAgIF1cbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBnaGVya2luO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9