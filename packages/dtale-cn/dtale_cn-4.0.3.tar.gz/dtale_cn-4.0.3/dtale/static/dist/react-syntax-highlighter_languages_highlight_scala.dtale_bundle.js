(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_scala"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/scala.js":
/*!************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/scala.js ***!
  \************************************************************************************************/
/***/ ((module) => {

/*
Language: Scala
Category: functional
Author: Jan Berkel <jan.berkel@gmail.com>
Contributors: Erik Osheim <d_m@plastic-idolatry.com>
Website: https://www.scala-lang.org
*/

function scala(hljs) {
  const ANNOTATION = {
    className: 'meta',
    begin: '@[A-Za-z]+'
  };

  // used in strings for escaping/interpolation/substitution
  const SUBST = {
    className: 'subst',
    variants: [
      {
        begin: '\\$[A-Za-z0-9_]+'
      },
      {
        begin: /\$\{/,
        end: /\}/
      }
    ]
  };

  const STRING = {
    className: 'string',
    variants: [
      {
        begin: '"""',
        end: '"""'
      },
      {
        begin: '"',
        end: '"',
        illegal: '\\n',
        contains: [ hljs.BACKSLASH_ESCAPE ]
      },
      {
        begin: '[a-z]+"',
        end: '"',
        illegal: '\\n',
        contains: [
          hljs.BACKSLASH_ESCAPE,
          SUBST
        ]
      },
      {
        className: 'string',
        begin: '[a-z]+"""',
        end: '"""',
        contains: [ SUBST ],
        relevance: 10
      }
    ]

  };

  const SYMBOL = {
    className: 'symbol',
    begin: '\'\\w[\\w\\d_]*(?!\')'
  };

  const TYPE = {
    className: 'type',
    begin: '\\b[A-Z][A-Za-z0-9_]*',
    relevance: 0
  };

  const NAME = {
    className: 'title',
    begin: /[^0-9\n\t "'(),.`{}\[\]:;][^\n\t "'(),.`{}\[\]:;]+|[^0-9\n\t "'(),.`{}\[\]:;=]/,
    relevance: 0
  };

  const CLASS = {
    className: 'class',
    beginKeywords: 'class object trait type',
    end: /[:={\[\n;]/,
    excludeEnd: true,
    contains: [
      hljs.C_LINE_COMMENT_MODE,
      hljs.C_BLOCK_COMMENT_MODE,
      {
        beginKeywords: 'extends with',
        relevance: 10
      },
      {
        begin: /\[/,
        end: /\]/,
        excludeBegin: true,
        excludeEnd: true,
        relevance: 0,
        contains: [ TYPE ]
      },
      {
        className: 'params',
        begin: /\(/,
        end: /\)/,
        excludeBegin: true,
        excludeEnd: true,
        relevance: 0,
        contains: [ TYPE ]
      },
      NAME
    ]
  };

  const METHOD = {
    className: 'function',
    beginKeywords: 'def',
    end: /[:={\[(\n;]/,
    excludeEnd: true,
    contains: [ NAME ]
  };

  return {
    name: 'Scala',
    keywords: {
      literal: 'true false null',
      keyword: 'type yield lazy override def with val var sealed abstract private trait object if forSome for while throw finally protected extends import final return else break new catch super class case package default try this match continue throws implicit'
    },
    contains: [
      hljs.C_LINE_COMMENT_MODE,
      hljs.C_BLOCK_COMMENT_MODE,
      STRING,
      SYMBOL,
      TYPE,
      METHOD,
      CLASS,
      hljs.C_NUMBER_MODE,
      ANNOTATION
    ]
  };
}

module.exports = scala;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfc2NhbGEuZHRhbGVfYnVuZGxlLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQSxvQkFBb0I7QUFDcEIsZ0JBQWdCO0FBQ2hCO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0EsK0JBQStCLE1BQU0saUJBQWlCLE1BQU0sc0JBQXNCLE1BQU07QUFDeEY7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQSxjQUFjLEtBQUs7QUFDbkI7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0EsY0FBYyxNQUFNO0FBQ3BCO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9zY2FsYS5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKlxuTGFuZ3VhZ2U6IFNjYWxhXG5DYXRlZ29yeTogZnVuY3Rpb25hbFxuQXV0aG9yOiBKYW4gQmVya2VsIDxqYW4uYmVya2VsQGdtYWlsLmNvbT5cbkNvbnRyaWJ1dG9yczogRXJpayBPc2hlaW0gPGRfbUBwbGFzdGljLWlkb2xhdHJ5LmNvbT5cbldlYnNpdGU6IGh0dHBzOi8vd3d3LnNjYWxhLWxhbmcub3JnXG4qL1xuXG5mdW5jdGlvbiBzY2FsYShobGpzKSB7XG4gIGNvbnN0IEFOTk9UQVRJT04gPSB7XG4gICAgY2xhc3NOYW1lOiAnbWV0YScsXG4gICAgYmVnaW46ICdAW0EtWmEtel0rJ1xuICB9O1xuXG4gIC8vIHVzZWQgaW4gc3RyaW5ncyBmb3IgZXNjYXBpbmcvaW50ZXJwb2xhdGlvbi9zdWJzdGl0dXRpb25cbiAgY29uc3QgU1VCU1QgPSB7XG4gICAgY2xhc3NOYW1lOiAnc3Vic3QnLFxuICAgIHZhcmlhbnRzOiBbXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnXFxcXCRbQS1aYS16MC05X10rJ1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC9cXCRcXHsvLFxuICAgICAgICBlbmQ6IC9cXH0vXG4gICAgICB9XG4gICAgXVxuICB9O1xuXG4gIGNvbnN0IFNUUklORyA9IHtcbiAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgIHZhcmlhbnRzOiBbXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnXCJcIlwiJyxcbiAgICAgICAgZW5kOiAnXCJcIlwiJ1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICdcIicsXG4gICAgICAgIGVuZDogJ1wiJyxcbiAgICAgICAgaWxsZWdhbDogJ1xcXFxuJyxcbiAgICAgICAgY29udGFpbnM6IFsgaGxqcy5CQUNLU0xBU0hfRVNDQVBFIF1cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnW2Etel0rXCInLFxuICAgICAgICBlbmQ6ICdcIicsXG4gICAgICAgIGlsbGVnYWw6ICdcXFxcbicsXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgaGxqcy5CQUNLU0xBU0hfRVNDQVBFLFxuICAgICAgICAgIFNVQlNUXG4gICAgICAgIF1cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3N0cmluZycsXG4gICAgICAgIGJlZ2luOiAnW2Etel0rXCJcIlwiJyxcbiAgICAgICAgZW5kOiAnXCJcIlwiJyxcbiAgICAgICAgY29udGFpbnM6IFsgU1VCU1QgXSxcbiAgICAgICAgcmVsZXZhbmNlOiAxMFxuICAgICAgfVxuICAgIF1cblxuICB9O1xuXG4gIGNvbnN0IFNZTUJPTCA9IHtcbiAgICBjbGFzc05hbWU6ICdzeW1ib2wnLFxuICAgIGJlZ2luOiAnXFwnXFxcXHdbXFxcXHdcXFxcZF9dKig/IVxcJyknXG4gIH07XG5cbiAgY29uc3QgVFlQRSA9IHtcbiAgICBjbGFzc05hbWU6ICd0eXBlJyxcbiAgICBiZWdpbjogJ1xcXFxiW0EtWl1bQS1aYS16MC05X10qJyxcbiAgICByZWxldmFuY2U6IDBcbiAgfTtcblxuICBjb25zdCBOQU1FID0ge1xuICAgIGNsYXNzTmFtZTogJ3RpdGxlJyxcbiAgICBiZWdpbjogL1teMC05XFxuXFx0IFwiJygpLC5ge31cXFtcXF06O11bXlxcblxcdCBcIicoKSwuYHt9XFxbXFxdOjtdK3xbXjAtOVxcblxcdCBcIicoKSwuYHt9XFxbXFxdOjs9XS8sXG4gICAgcmVsZXZhbmNlOiAwXG4gIH07XG5cbiAgY29uc3QgQ0xBU1MgPSB7XG4gICAgY2xhc3NOYW1lOiAnY2xhc3MnLFxuICAgIGJlZ2luS2V5d29yZHM6ICdjbGFzcyBvYmplY3QgdHJhaXQgdHlwZScsXG4gICAgZW5kOiAvWzo9e1xcW1xcbjtdLyxcbiAgICBleGNsdWRlRW5kOiB0cnVlLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBobGpzLkNfTElORV9DT01NRU5UX01PREUsXG4gICAgICBobGpzLkNfQkxPQ0tfQ09NTUVOVF9NT0RFLFxuICAgICAge1xuICAgICAgICBiZWdpbktleXdvcmRzOiAnZXh0ZW5kcyB3aXRoJyxcbiAgICAgICAgcmVsZXZhbmNlOiAxMFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC9cXFsvLFxuICAgICAgICBlbmQ6IC9cXF0vLFxuICAgICAgICBleGNsdWRlQmVnaW46IHRydWUsXG4gICAgICAgIGV4Y2x1ZGVFbmQ6IHRydWUsXG4gICAgICAgIHJlbGV2YW5jZTogMCxcbiAgICAgICAgY29udGFpbnM6IFsgVFlQRSBdXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdwYXJhbXMnLFxuICAgICAgICBiZWdpbjogL1xcKC8sXG4gICAgICAgIGVuZDogL1xcKS8sXG4gICAgICAgIGV4Y2x1ZGVCZWdpbjogdHJ1ZSxcbiAgICAgICAgZXhjbHVkZUVuZDogdHJ1ZSxcbiAgICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgICBjb250YWluczogWyBUWVBFIF1cbiAgICAgIH0sXG4gICAgICBOQU1FXG4gICAgXVxuICB9O1xuXG4gIGNvbnN0IE1FVEhPRCA9IHtcbiAgICBjbGFzc05hbWU6ICdmdW5jdGlvbicsXG4gICAgYmVnaW5LZXl3b3JkczogJ2RlZicsXG4gICAgZW5kOiAvWzo9e1xcWyhcXG47XS8sXG4gICAgZXhjbHVkZUVuZDogdHJ1ZSxcbiAgICBjb250YWluczogWyBOQU1FIF1cbiAgfTtcblxuICByZXR1cm4ge1xuICAgIG5hbWU6ICdTY2FsYScsXG4gICAga2V5d29yZHM6IHtcbiAgICAgIGxpdGVyYWw6ICd0cnVlIGZhbHNlIG51bGwnLFxuICAgICAga2V5d29yZDogJ3R5cGUgeWllbGQgbGF6eSBvdmVycmlkZSBkZWYgd2l0aCB2YWwgdmFyIHNlYWxlZCBhYnN0cmFjdCBwcml2YXRlIHRyYWl0IG9iamVjdCBpZiBmb3JTb21lIGZvciB3aGlsZSB0aHJvdyBmaW5hbGx5IHByb3RlY3RlZCBleHRlbmRzIGltcG9ydCBmaW5hbCByZXR1cm4gZWxzZSBicmVhayBuZXcgY2F0Y2ggc3VwZXIgY2xhc3MgY2FzZSBwYWNrYWdlIGRlZmF1bHQgdHJ5IHRoaXMgbWF0Y2ggY29udGludWUgdGhyb3dzIGltcGxpY2l0J1xuICAgIH0sXG4gICAgY29udGFpbnM6IFtcbiAgICAgIGhsanMuQ19MSU5FX0NPTU1FTlRfTU9ERSxcbiAgICAgIGhsanMuQ19CTE9DS19DT01NRU5UX01PREUsXG4gICAgICBTVFJJTkcsXG4gICAgICBTWU1CT0wsXG4gICAgICBUWVBFLFxuICAgICAgTUVUSE9ELFxuICAgICAgQ0xBU1MsXG4gICAgICBobGpzLkNfTlVNQkVSX01PREUsXG4gICAgICBBTk5PVEFUSU9OXG4gICAgXVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IHNjYWxhO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9