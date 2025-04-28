(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_golo"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/golo.js":
/*!***********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/golo.js ***!
  \***********************************************************************************************/
/***/ ((module) => {

/*
Language: Golo
Author: Philippe Charriere <ph.charriere@gmail.com>
Description: a lightweight dynamic language for the JVM
Website: http://golo-lang.org/
*/

function golo(hljs) {
  return {
    name: 'Golo',
    keywords: {
      keyword:
          'println readln print import module function local return let var ' +
          'while for foreach times in case when match with break continue ' +
          'augment augmentation each find filter reduce ' +
          'if then else otherwise try catch finally raise throw orIfNull ' +
          'DynamicObject|10 DynamicVariable struct Observable map set vector list array',
      literal:
          'true false null'
    },
    contains: [
      hljs.HASH_COMMENT_MODE,
      hljs.QUOTE_STRING_MODE,
      hljs.C_NUMBER_MODE,
      {
        className: 'meta',
        begin: '@[A-Za-z]+'
      }
    ]
  };
}

module.exports = golo;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfZ29sby5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL2dvbG8uanMiXSwic291cmNlc0NvbnRlbnQiOlsiLypcbkxhbmd1YWdlOiBHb2xvXG5BdXRob3I6IFBoaWxpcHBlIENoYXJyaWVyZSA8cGguY2hhcnJpZXJlQGdtYWlsLmNvbT5cbkRlc2NyaXB0aW9uOiBhIGxpZ2h0d2VpZ2h0IGR5bmFtaWMgbGFuZ3VhZ2UgZm9yIHRoZSBKVk1cbldlYnNpdGU6IGh0dHA6Ly9nb2xvLWxhbmcub3JnL1xuKi9cblxuZnVuY3Rpb24gZ29sbyhobGpzKSB7XG4gIHJldHVybiB7XG4gICAgbmFtZTogJ0dvbG8nLFxuICAgIGtleXdvcmRzOiB7XG4gICAgICBrZXl3b3JkOlxuICAgICAgICAgICdwcmludGxuIHJlYWRsbiBwcmludCBpbXBvcnQgbW9kdWxlIGZ1bmN0aW9uIGxvY2FsIHJldHVybiBsZXQgdmFyICcgK1xuICAgICAgICAgICd3aGlsZSBmb3IgZm9yZWFjaCB0aW1lcyBpbiBjYXNlIHdoZW4gbWF0Y2ggd2l0aCBicmVhayBjb250aW51ZSAnICtcbiAgICAgICAgICAnYXVnbWVudCBhdWdtZW50YXRpb24gZWFjaCBmaW5kIGZpbHRlciByZWR1Y2UgJyArXG4gICAgICAgICAgJ2lmIHRoZW4gZWxzZSBvdGhlcndpc2UgdHJ5IGNhdGNoIGZpbmFsbHkgcmFpc2UgdGhyb3cgb3JJZk51bGwgJyArXG4gICAgICAgICAgJ0R5bmFtaWNPYmplY3R8MTAgRHluYW1pY1ZhcmlhYmxlIHN0cnVjdCBPYnNlcnZhYmxlIG1hcCBzZXQgdmVjdG9yIGxpc3QgYXJyYXknLFxuICAgICAgbGl0ZXJhbDpcbiAgICAgICAgICAndHJ1ZSBmYWxzZSBudWxsJ1xuICAgIH0sXG4gICAgY29udGFpbnM6IFtcbiAgICAgIGhsanMuSEFTSF9DT01NRU5UX01PREUsXG4gICAgICBobGpzLlFVT1RFX1NUUklOR19NT0RFLFxuICAgICAgaGxqcy5DX05VTUJFUl9NT0RFLFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdtZXRhJyxcbiAgICAgICAgYmVnaW46ICdAW0EtWmEtel0rJ1xuICAgICAgfVxuICAgIF1cbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBnb2xvO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9