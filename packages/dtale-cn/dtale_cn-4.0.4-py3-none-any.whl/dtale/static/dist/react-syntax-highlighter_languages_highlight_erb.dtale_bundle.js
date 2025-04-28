(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_erb"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/erb.js":
/*!**********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/erb.js ***!
  \**********************************************************************************************/
/***/ ((module) => {

/*
Language: ERB (Embedded Ruby)
Requires: xml.js, ruby.js
Author: Lucas Mazza <lucastmazza@gmail.com>
Contributors: Kassio Borges <kassioborgesm@gmail.com>
Description: "Bridge" language defining fragments of Ruby in HTML within <% .. %>
Website: https://ruby-doc.org/stdlib-2.6.5/libdoc/erb/rdoc/ERB.html
Category: template
*/

/** @type LanguageFn */
function erb(hljs) {
  return {
    name: 'ERB',
    subLanguage: 'xml',
    contains: [
      hljs.COMMENT('<%#', '%>'),
      {
        begin: '<%[%=-]?',
        end: '[%-]?%>',
        subLanguage: 'ruby',
        excludeBegin: true,
        excludeEnd: true
      }
    ]
  };
}

module.exports = erb;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfZXJiLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9lcmIuanMiXSwic291cmNlc0NvbnRlbnQiOlsiLypcbkxhbmd1YWdlOiBFUkIgKEVtYmVkZGVkIFJ1YnkpXG5SZXF1aXJlczogeG1sLmpzLCBydWJ5LmpzXG5BdXRob3I6IEx1Y2FzIE1henphIDxsdWNhc3RtYXp6YUBnbWFpbC5jb20+XG5Db250cmlidXRvcnM6IEthc3NpbyBCb3JnZXMgPGthc3Npb2Jvcmdlc21AZ21haWwuY29tPlxuRGVzY3JpcHRpb246IFwiQnJpZGdlXCIgbGFuZ3VhZ2UgZGVmaW5pbmcgZnJhZ21lbnRzIG9mIFJ1YnkgaW4gSFRNTCB3aXRoaW4gPCUgLi4gJT5cbldlYnNpdGU6IGh0dHBzOi8vcnVieS1kb2Mub3JnL3N0ZGxpYi0yLjYuNS9saWJkb2MvZXJiL3Jkb2MvRVJCLmh0bWxcbkNhdGVnb3J5OiB0ZW1wbGF0ZVxuKi9cblxuLyoqIEB0eXBlIExhbmd1YWdlRm4gKi9cbmZ1bmN0aW9uIGVyYihobGpzKSB7XG4gIHJldHVybiB7XG4gICAgbmFtZTogJ0VSQicsXG4gICAgc3ViTGFuZ3VhZ2U6ICd4bWwnLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBobGpzLkNPTU1FTlQoJzwlIycsICclPicpLFxuICAgICAge1xuICAgICAgICBiZWdpbjogJzwlWyU9LV0/JyxcbiAgICAgICAgZW5kOiAnWyUtXT8lPicsXG4gICAgICAgIHN1Ykxhbmd1YWdlOiAncnVieScsXG4gICAgICAgIGV4Y2x1ZGVCZWdpbjogdHJ1ZSxcbiAgICAgICAgZXhjbHVkZUVuZDogdHJ1ZVxuICAgICAgfVxuICAgIF1cbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBlcmI7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=