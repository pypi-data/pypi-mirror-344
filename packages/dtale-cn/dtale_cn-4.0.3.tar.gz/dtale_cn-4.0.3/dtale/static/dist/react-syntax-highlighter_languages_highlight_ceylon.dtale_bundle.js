(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_ceylon"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/ceylon.js":
/*!*************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/ceylon.js ***!
  \*************************************************************************************************/
/***/ ((module) => {

/*
Language: Ceylon
Author: Lucas Werkmeister <mail@lucaswerkmeister.de>
Website: https://ceylon-lang.org
*/

/** @type LanguageFn */
function ceylon(hljs) {
  // 2.3. Identifiers and keywords
  const KEYWORDS =
    'assembly module package import alias class interface object given value ' +
    'assign void function new of extends satisfies abstracts in out return ' +
    'break continue throw assert dynamic if else switch case for while try ' +
    'catch finally then let this outer super is exists nonempty';
  // 7.4.1 Declaration Modifiers
  const DECLARATION_MODIFIERS =
    'shared abstract formal default actual variable late native deprecated ' +
    'final sealed annotation suppressWarnings small';
  // 7.4.2 Documentation
  const DOCUMENTATION =
    'doc by license see throws tagged';
  const SUBST = {
    className: 'subst',
    excludeBegin: true,
    excludeEnd: true,
    begin: /``/,
    end: /``/,
    keywords: KEYWORDS,
    relevance: 10
  };
  const EXPRESSIONS = [
    {
      // verbatim string
      className: 'string',
      begin: '"""',
      end: '"""',
      relevance: 10
    },
    {
      // string literal or template
      className: 'string',
      begin: '"',
      end: '"',
      contains: [SUBST]
    },
    {
      // character literal
      className: 'string',
      begin: "'",
      end: "'"
    },
    {
      // numeric literal
      className: 'number',
      begin: '#[0-9a-fA-F_]+|\\$[01_]+|[0-9_]+(?:\\.[0-9_](?:[eE][+-]?\\d+)?)?[kMGTPmunpf]?',
      relevance: 0
    }
  ];
  SUBST.contains = EXPRESSIONS;

  return {
    name: 'Ceylon',
    keywords: {
      keyword: KEYWORDS + ' ' + DECLARATION_MODIFIERS,
      meta: DOCUMENTATION
    },
    illegal: '\\$[^01]|#[^0-9a-fA-F]',
    contains: [
      hljs.C_LINE_COMMENT_MODE,
      hljs.COMMENT('/\\*', '\\*/', {
        contains: ['self']
      }),
      {
        // compiler annotation
        className: 'meta',
        begin: '@[a-z]\\w*(?::"[^"]*")?'
      }
    ].concat(EXPRESSIONS)
  };
}

module.exports = ceylon;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfY2V5bG9uLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvY2V5bG9uLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogQ2V5bG9uXG5BdXRob3I6IEx1Y2FzIFdlcmttZWlzdGVyIDxtYWlsQGx1Y2Fzd2Vya21laXN0ZXIuZGU+XG5XZWJzaXRlOiBodHRwczovL2NleWxvbi1sYW5nLm9yZ1xuKi9cblxuLyoqIEB0eXBlIExhbmd1YWdlRm4gKi9cbmZ1bmN0aW9uIGNleWxvbihobGpzKSB7XG4gIC8vIDIuMy4gSWRlbnRpZmllcnMgYW5kIGtleXdvcmRzXG4gIGNvbnN0IEtFWVdPUkRTID1cbiAgICAnYXNzZW1ibHkgbW9kdWxlIHBhY2thZ2UgaW1wb3J0IGFsaWFzIGNsYXNzIGludGVyZmFjZSBvYmplY3QgZ2l2ZW4gdmFsdWUgJyArXG4gICAgJ2Fzc2lnbiB2b2lkIGZ1bmN0aW9uIG5ldyBvZiBleHRlbmRzIHNhdGlzZmllcyBhYnN0cmFjdHMgaW4gb3V0IHJldHVybiAnICtcbiAgICAnYnJlYWsgY29udGludWUgdGhyb3cgYXNzZXJ0IGR5bmFtaWMgaWYgZWxzZSBzd2l0Y2ggY2FzZSBmb3Igd2hpbGUgdHJ5ICcgK1xuICAgICdjYXRjaCBmaW5hbGx5IHRoZW4gbGV0IHRoaXMgb3V0ZXIgc3VwZXIgaXMgZXhpc3RzIG5vbmVtcHR5JztcbiAgLy8gNy40LjEgRGVjbGFyYXRpb24gTW9kaWZpZXJzXG4gIGNvbnN0IERFQ0xBUkFUSU9OX01PRElGSUVSUyA9XG4gICAgJ3NoYXJlZCBhYnN0cmFjdCBmb3JtYWwgZGVmYXVsdCBhY3R1YWwgdmFyaWFibGUgbGF0ZSBuYXRpdmUgZGVwcmVjYXRlZCAnICtcbiAgICAnZmluYWwgc2VhbGVkIGFubm90YXRpb24gc3VwcHJlc3NXYXJuaW5ncyBzbWFsbCc7XG4gIC8vIDcuNC4yIERvY3VtZW50YXRpb25cbiAgY29uc3QgRE9DVU1FTlRBVElPTiA9XG4gICAgJ2RvYyBieSBsaWNlbnNlIHNlZSB0aHJvd3MgdGFnZ2VkJztcbiAgY29uc3QgU1VCU1QgPSB7XG4gICAgY2xhc3NOYW1lOiAnc3Vic3QnLFxuICAgIGV4Y2x1ZGVCZWdpbjogdHJ1ZSxcbiAgICBleGNsdWRlRW5kOiB0cnVlLFxuICAgIGJlZ2luOiAvYGAvLFxuICAgIGVuZDogL2BgLyxcbiAgICBrZXl3b3JkczogS0VZV09SRFMsXG4gICAgcmVsZXZhbmNlOiAxMFxuICB9O1xuICBjb25zdCBFWFBSRVNTSU9OUyA9IFtcbiAgICB7XG4gICAgICAvLyB2ZXJiYXRpbSBzdHJpbmdcbiAgICAgIGNsYXNzTmFtZTogJ3N0cmluZycsXG4gICAgICBiZWdpbjogJ1wiXCJcIicsXG4gICAgICBlbmQ6ICdcIlwiXCInLFxuICAgICAgcmVsZXZhbmNlOiAxMFxuICAgIH0sXG4gICAge1xuICAgICAgLy8gc3RyaW5nIGxpdGVyYWwgb3IgdGVtcGxhdGVcbiAgICAgIGNsYXNzTmFtZTogJ3N0cmluZycsXG4gICAgICBiZWdpbjogJ1wiJyxcbiAgICAgIGVuZDogJ1wiJyxcbiAgICAgIGNvbnRhaW5zOiBbU1VCU1RdXG4gICAgfSxcbiAgICB7XG4gICAgICAvLyBjaGFyYWN0ZXIgbGl0ZXJhbFxuICAgICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICAgIGJlZ2luOiBcIidcIixcbiAgICAgIGVuZDogXCInXCJcbiAgICB9LFxuICAgIHtcbiAgICAgIC8vIG51bWVyaWMgbGl0ZXJhbFxuICAgICAgY2xhc3NOYW1lOiAnbnVtYmVyJyxcbiAgICAgIGJlZ2luOiAnI1swLTlhLWZBLUZfXSt8XFxcXCRbMDFfXSt8WzAtOV9dKyg/OlxcXFwuWzAtOV9dKD86W2VFXVsrLV0/XFxcXGQrKT8pP1trTUdUUG11bnBmXT8nLFxuICAgICAgcmVsZXZhbmNlOiAwXG4gICAgfVxuICBdO1xuICBTVUJTVC5jb250YWlucyA9IEVYUFJFU1NJT05TO1xuXG4gIHJldHVybiB7XG4gICAgbmFtZTogJ0NleWxvbicsXG4gICAga2V5d29yZHM6IHtcbiAgICAgIGtleXdvcmQ6IEtFWVdPUkRTICsgJyAnICsgREVDTEFSQVRJT05fTU9ESUZJRVJTLFxuICAgICAgbWV0YTogRE9DVU1FTlRBVElPTlxuICAgIH0sXG4gICAgaWxsZWdhbDogJ1xcXFwkW14wMV18I1teMC05YS1mQS1GXScsXG4gICAgY29udGFpbnM6IFtcbiAgICAgIGhsanMuQ19MSU5FX0NPTU1FTlRfTU9ERSxcbiAgICAgIGhsanMuQ09NTUVOVCgnL1xcXFwqJywgJ1xcXFwqLycsIHtcbiAgICAgICAgY29udGFpbnM6IFsnc2VsZiddXG4gICAgICB9KSxcbiAgICAgIHtcbiAgICAgICAgLy8gY29tcGlsZXIgYW5ub3RhdGlvblxuICAgICAgICBjbGFzc05hbWU6ICdtZXRhJyxcbiAgICAgICAgYmVnaW46ICdAW2Etel1cXFxcdyooPzo6XCJbXlwiXSpcIik/J1xuICAgICAgfVxuICAgIF0uY29uY2F0KEVYUFJFU1NJT05TKVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IGNleWxvbjtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==