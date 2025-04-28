(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_mojolicious"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/mojolicious.js":
/*!******************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/mojolicious.js ***!
  \******************************************************************************************************/
/***/ ((module) => {

/*
Language: Mojolicious
Requires: xml.js, perl.js
Author: Dotan Dimet <dotan@corky.net>
Description: Mojolicious .ep (Embedded Perl) templates
Website: https://mojolicious.org
Category: template
*/
function mojolicious(hljs) {
  return {
    name: 'Mojolicious',
    subLanguage: 'xml',
    contains: [
      {
        className: 'meta',
        begin: '^__(END|DATA)__$'
      },
      // mojolicious line
      {
        begin: "^\\s*%{1,2}={0,2}",
        end: '$',
        subLanguage: 'perl'
      },
      // mojolicious block
      {
        begin: "<%{1,2}={0,2}",
        end: "={0,1}%>",
        subLanguage: 'perl',
        excludeBegin: true,
        excludeEnd: true
      }
    ]
  };
}

module.exports = mojolicious;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfbW9qb2xpY2lvdXMuZHRhbGVfYnVuZGxlLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBLHVCQUF1QixJQUFJLEVBQUUsSUFBSTtBQUNqQztBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQSxtQkFBbUIsSUFBSSxFQUFFLElBQUk7QUFDN0IsZ0JBQWdCLElBQUk7QUFDcEI7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL21vam9saWNpb3VzLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogTW9qb2xpY2lvdXNcblJlcXVpcmVzOiB4bWwuanMsIHBlcmwuanNcbkF1dGhvcjogRG90YW4gRGltZXQgPGRvdGFuQGNvcmt5Lm5ldD5cbkRlc2NyaXB0aW9uOiBNb2pvbGljaW91cyAuZXAgKEVtYmVkZGVkIFBlcmwpIHRlbXBsYXRlc1xuV2Vic2l0ZTogaHR0cHM6Ly9tb2pvbGljaW91cy5vcmdcbkNhdGVnb3J5OiB0ZW1wbGF0ZVxuKi9cbmZ1bmN0aW9uIG1vam9saWNpb3VzKGhsanMpIHtcbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnTW9qb2xpY2lvdXMnLFxuICAgIHN1Ykxhbmd1YWdlOiAneG1sJyxcbiAgICBjb250YWluczogW1xuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdtZXRhJyxcbiAgICAgICAgYmVnaW46ICdeX18oRU5EfERBVEEpX18kJ1xuICAgICAgfSxcbiAgICAgIC8vIG1vam9saWNpb3VzIGxpbmVcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IFwiXlxcXFxzKiV7MSwyfT17MCwyfVwiLFxuICAgICAgICBlbmQ6ICckJyxcbiAgICAgICAgc3ViTGFuZ3VhZ2U6ICdwZXJsJ1xuICAgICAgfSxcbiAgICAgIC8vIG1vam9saWNpb3VzIGJsb2NrXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiBcIjwlezEsMn09ezAsMn1cIixcbiAgICAgICAgZW5kOiBcIj17MCwxfSU+XCIsXG4gICAgICAgIHN1Ykxhbmd1YWdlOiAncGVybCcsXG4gICAgICAgIGV4Y2x1ZGVCZWdpbjogdHJ1ZSxcbiAgICAgICAgZXhjbHVkZUVuZDogdHJ1ZVxuICAgICAgfVxuICAgIF1cbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBtb2pvbGljaW91cztcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==