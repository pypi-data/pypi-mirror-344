(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_dust"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/dust.js":
/*!***********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/dust.js ***!
  \***********************************************************************************************/
/***/ ((module) => {

/*
Language: Dust
Requires: xml.js
Author: Michael Allen <michael.allen@benefitfocus.com>
Description: Matcher for dust.js templates.
Website: https://www.dustjs.com
Category: template
*/

/** @type LanguageFn */
function dust(hljs) {
  const EXPRESSION_KEYWORDS = 'if eq ne lt lte gt gte select default math sep';
  return {
    name: 'Dust',
    aliases: ['dst'],
    case_insensitive: true,
    subLanguage: 'xml',
    contains: [
      {
        className: 'template-tag',
        begin: /\{[#\/]/,
        end: /\}/,
        illegal: /;/,
        contains: [{
          className: 'name',
          begin: /[a-zA-Z\.-]+/,
          starts: {
            endsWithParent: true,
            relevance: 0,
            contains: [hljs.QUOTE_STRING_MODE]
          }
        }]
      },
      {
        className: 'template-variable',
        begin: /\{/,
        end: /\}/,
        illegal: /;/,
        keywords: EXPRESSION_KEYWORDS
      }
    ]
  };
}

module.exports = dust;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfZHVzdC5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxrQkFBa0I7QUFDbEIsZ0JBQWdCO0FBQ2hCLG1CQUFtQjtBQUNuQjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsU0FBUztBQUNULE9BQU87QUFDUDtBQUNBO0FBQ0Esa0JBQWtCO0FBQ2xCLGdCQUFnQjtBQUNoQixtQkFBbUI7QUFDbkI7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvZHVzdC5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKlxuTGFuZ3VhZ2U6IER1c3RcblJlcXVpcmVzOiB4bWwuanNcbkF1dGhvcjogTWljaGFlbCBBbGxlbiA8bWljaGFlbC5hbGxlbkBiZW5lZml0Zm9jdXMuY29tPlxuRGVzY3JpcHRpb246IE1hdGNoZXIgZm9yIGR1c3QuanMgdGVtcGxhdGVzLlxuV2Vic2l0ZTogaHR0cHM6Ly93d3cuZHVzdGpzLmNvbVxuQ2F0ZWdvcnk6IHRlbXBsYXRlXG4qL1xuXG4vKiogQHR5cGUgTGFuZ3VhZ2VGbiAqL1xuZnVuY3Rpb24gZHVzdChobGpzKSB7XG4gIGNvbnN0IEVYUFJFU1NJT05fS0VZV09SRFMgPSAnaWYgZXEgbmUgbHQgbHRlIGd0IGd0ZSBzZWxlY3QgZGVmYXVsdCBtYXRoIHNlcCc7XG4gIHJldHVybiB7XG4gICAgbmFtZTogJ0R1c3QnLFxuICAgIGFsaWFzZXM6IFsnZHN0J10sXG4gICAgY2FzZV9pbnNlbnNpdGl2ZTogdHJ1ZSxcbiAgICBzdWJMYW5ndWFnZTogJ3htbCcsXG4gICAgY29udGFpbnM6IFtcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAndGVtcGxhdGUtdGFnJyxcbiAgICAgICAgYmVnaW46IC9cXHtbI1xcL10vLFxuICAgICAgICBlbmQ6IC9cXH0vLFxuICAgICAgICBpbGxlZ2FsOiAvOy8sXG4gICAgICAgIGNvbnRhaW5zOiBbe1xuICAgICAgICAgIGNsYXNzTmFtZTogJ25hbWUnLFxuICAgICAgICAgIGJlZ2luOiAvW2EtekEtWlxcLi1dKy8sXG4gICAgICAgICAgc3RhcnRzOiB7XG4gICAgICAgICAgICBlbmRzV2l0aFBhcmVudDogdHJ1ZSxcbiAgICAgICAgICAgIHJlbGV2YW5jZTogMCxcbiAgICAgICAgICAgIGNvbnRhaW5zOiBbaGxqcy5RVU9URV9TVFJJTkdfTU9ERV1cbiAgICAgICAgICB9XG4gICAgICAgIH1dXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICd0ZW1wbGF0ZS12YXJpYWJsZScsXG4gICAgICAgIGJlZ2luOiAvXFx7LyxcbiAgICAgICAgZW5kOiAvXFx9LyxcbiAgICAgICAgaWxsZWdhbDogLzsvLFxuICAgICAgICBrZXl3b3JkczogRVhQUkVTU0lPTl9LRVlXT1JEU1xuICAgICAgfVxuICAgIF1cbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBkdXN0O1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9