(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_roboconf"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/roboconf.js":
/*!***************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/roboconf.js ***!
  \***************************************************************************************************/
/***/ ((module) => {

/*
Language: Roboconf
Author: Vincent Zurczak <vzurczak@linagora.com>
Description: Syntax highlighting for Roboconf's DSL
Website: http://roboconf.net
Category: config
*/

function roboconf(hljs) {
  const IDENTIFIER = '[a-zA-Z-_][^\\n{]+\\{';

  const PROPERTY = {
    className: 'attribute',
    begin: /[a-zA-Z-_]+/,
    end: /\s*:/,
    excludeEnd: true,
    starts: {
      end: ';',
      relevance: 0,
      contains: [
        {
          className: 'variable',
          begin: /\.[a-zA-Z-_]+/
        },
        {
          className: 'keyword',
          begin: /\(optional\)/
        }
      ]
    }
  };

  return {
    name: 'Roboconf',
    aliases: [
      'graph',
      'instances'
    ],
    case_insensitive: true,
    keywords: 'import',
    contains: [
      // Facet sections
      {
        begin: '^facet ' + IDENTIFIER,
        end: /\}/,
        keywords: 'facet',
        contains: [
          PROPERTY,
          hljs.HASH_COMMENT_MODE
        ]
      },

      // Instance sections
      {
        begin: '^\\s*instance of ' + IDENTIFIER,
        end: /\}/,
        keywords: 'name count channels instance-data instance-state instance of',
        illegal: /\S/,
        contains: [
          'self',
          PROPERTY,
          hljs.HASH_COMMENT_MODE
        ]
      },

      // Component sections
      {
        begin: '^' + IDENTIFIER,
        end: /\}/,
        contains: [
          PROPERTY,
          hljs.HASH_COMMENT_MODE
        ]
      },

      // Comments
      hljs.HASH_COMMENT_MODE
    ]
  };
}

module.exports = roboconf;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfcm9ib2NvbmYuZHRhbGVfYnVuZGxlLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQSxzQ0FBc0MsS0FBSzs7QUFFM0M7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxTQUFTO0FBQ1Q7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsZ0JBQWdCO0FBQ2hCO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPOztBQUVQO0FBQ0E7QUFDQTtBQUNBLGdCQUFnQjtBQUNoQjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87O0FBRVA7QUFDQTtBQUNBO0FBQ0EsZ0JBQWdCO0FBQ2hCO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTzs7QUFFUDtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9yb2JvY29uZi5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKlxuTGFuZ3VhZ2U6IFJvYm9jb25mXG5BdXRob3I6IFZpbmNlbnQgWnVyY3phayA8dnp1cmN6YWtAbGluYWdvcmEuY29tPlxuRGVzY3JpcHRpb246IFN5bnRheCBoaWdobGlnaHRpbmcgZm9yIFJvYm9jb25mJ3MgRFNMXG5XZWJzaXRlOiBodHRwOi8vcm9ib2NvbmYubmV0XG5DYXRlZ29yeTogY29uZmlnXG4qL1xuXG5mdW5jdGlvbiByb2JvY29uZihobGpzKSB7XG4gIGNvbnN0IElERU5USUZJRVIgPSAnW2EtekEtWi1fXVteXFxcXG57XStcXFxceyc7XG5cbiAgY29uc3QgUFJPUEVSVFkgPSB7XG4gICAgY2xhc3NOYW1lOiAnYXR0cmlidXRlJyxcbiAgICBiZWdpbjogL1thLXpBLVotX10rLyxcbiAgICBlbmQ6IC9cXHMqOi8sXG4gICAgZXhjbHVkZUVuZDogdHJ1ZSxcbiAgICBzdGFydHM6IHtcbiAgICAgIGVuZDogJzsnLFxuICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgY29udGFpbnM6IFtcbiAgICAgICAge1xuICAgICAgICAgIGNsYXNzTmFtZTogJ3ZhcmlhYmxlJyxcbiAgICAgICAgICBiZWdpbjogL1xcLlthLXpBLVotX10rL1xuICAgICAgICB9LFxuICAgICAgICB7XG4gICAgICAgICAgY2xhc3NOYW1lOiAna2V5d29yZCcsXG4gICAgICAgICAgYmVnaW46IC9cXChvcHRpb25hbFxcKS9cbiAgICAgICAgfVxuICAgICAgXVxuICAgIH1cbiAgfTtcblxuICByZXR1cm4ge1xuICAgIG5hbWU6ICdSb2JvY29uZicsXG4gICAgYWxpYXNlczogW1xuICAgICAgJ2dyYXBoJyxcbiAgICAgICdpbnN0YW5jZXMnXG4gICAgXSxcbiAgICBjYXNlX2luc2Vuc2l0aXZlOiB0cnVlLFxuICAgIGtleXdvcmRzOiAnaW1wb3J0JyxcbiAgICBjb250YWluczogW1xuICAgICAgLy8gRmFjZXQgc2VjdGlvbnNcbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICdeZmFjZXQgJyArIElERU5USUZJRVIsXG4gICAgICAgIGVuZDogL1xcfS8sXG4gICAgICAgIGtleXdvcmRzOiAnZmFjZXQnLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIFBST1BFUlRZLFxuICAgICAgICAgIGhsanMuSEFTSF9DT01NRU5UX01PREVcbiAgICAgICAgXVxuICAgICAgfSxcblxuICAgICAgLy8gSW5zdGFuY2Ugc2VjdGlvbnNcbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICdeXFxcXHMqaW5zdGFuY2Ugb2YgJyArIElERU5USUZJRVIsXG4gICAgICAgIGVuZDogL1xcfS8sXG4gICAgICAgIGtleXdvcmRzOiAnbmFtZSBjb3VudCBjaGFubmVscyBpbnN0YW5jZS1kYXRhIGluc3RhbmNlLXN0YXRlIGluc3RhbmNlIG9mJyxcbiAgICAgICAgaWxsZWdhbDogL1xcUy8sXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgJ3NlbGYnLFxuICAgICAgICAgIFBST1BFUlRZLFxuICAgICAgICAgIGhsanMuSEFTSF9DT01NRU5UX01PREVcbiAgICAgICAgXVxuICAgICAgfSxcblxuICAgICAgLy8gQ29tcG9uZW50IHNlY3Rpb25zXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAnXicgKyBJREVOVElGSUVSLFxuICAgICAgICBlbmQ6IC9cXH0vLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIFBST1BFUlRZLFxuICAgICAgICAgIGhsanMuSEFTSF9DT01NRU5UX01PREVcbiAgICAgICAgXVxuICAgICAgfSxcblxuICAgICAgLy8gQ29tbWVudHNcbiAgICAgIGhsanMuSEFTSF9DT01NRU5UX01PREVcbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gcm9ib2NvbmY7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=