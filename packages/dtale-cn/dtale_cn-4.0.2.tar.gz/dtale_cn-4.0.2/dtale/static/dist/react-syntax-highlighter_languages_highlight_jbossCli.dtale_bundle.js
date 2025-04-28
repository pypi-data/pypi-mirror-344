(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_jbossCli"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/jboss-cli.js":
/*!****************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/jboss-cli.js ***!
  \****************************************************************************************************/
/***/ ((module) => {

/*
 Language: JBoss CLI
 Author: Raphaël Parrëe <rparree@edc4it.com>
 Description: language definition jboss cli
 Website: https://docs.jboss.org/author/display/WFLY/Command+Line+Interface
 Category: config
 */

function jbossCli(hljs) {
  const PARAM = {
    begin: /[\w-]+ *=/,
    returnBegin: true,
    relevance: 0,
    contains: [
      {
        className: 'attr',
        begin: /[\w-]+/
      }
    ]
  };
  const PARAMSBLOCK = {
    className: 'params',
    begin: /\(/,
    end: /\)/,
    contains: [PARAM],
    relevance: 0
  };
  const OPERATION = {
    className: 'function',
    begin: /:[\w\-.]+/,
    relevance: 0
  };
  const PATH = {
    className: 'string',
    begin: /\B([\/.])[\w\-.\/=]+/
  };
  const COMMAND_PARAMS = {
    className: 'params',
    begin: /--[\w\-=\/]+/
  };
  return {
    name: 'JBoss CLI',
    aliases: ['wildfly-cli'],
    keywords: {
      $pattern: '[a-z\-]+',
      keyword: 'alias batch cd clear command connect connection-factory connection-info data-source deploy ' +
      'deployment-info deployment-overlay echo echo-dmr help history if jdbc-driver-info jms-queue|20 jms-topic|20 ls ' +
      'patch pwd quit read-attribute read-operation reload rollout-plan run-batch set shutdown try unalias ' +
      'undeploy unset version xa-data-source', // module
      literal: 'true false'
    },
    contains: [
      hljs.HASH_COMMENT_MODE,
      hljs.QUOTE_STRING_MODE,
      COMMAND_PARAMS,
      OPERATION,
      PATH,
      PARAMSBLOCK
    ]
  };
}

module.exports = jbossCli;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfamJvc3NDbGkuZHRhbGVfYnVuZGxlLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9qYm9zcy1jbGkuanMiXSwic291cmNlc0NvbnRlbnQiOlsiLypcbiBMYW5ndWFnZTogSkJvc3MgQ0xJXG4gQXV0aG9yOiBSYXBoYcOrbCBQYXJyw6tlIDxycGFycmVlQGVkYzRpdC5jb20+XG4gRGVzY3JpcHRpb246IGxhbmd1YWdlIGRlZmluaXRpb24gamJvc3MgY2xpXG4gV2Vic2l0ZTogaHR0cHM6Ly9kb2NzLmpib3NzLm9yZy9hdXRob3IvZGlzcGxheS9XRkxZL0NvbW1hbmQrTGluZStJbnRlcmZhY2VcbiBDYXRlZ29yeTogY29uZmlnXG4gKi9cblxuZnVuY3Rpb24gamJvc3NDbGkoaGxqcykge1xuICBjb25zdCBQQVJBTSA9IHtcbiAgICBiZWdpbjogL1tcXHctXSsgKj0vLFxuICAgIHJldHVybkJlZ2luOiB0cnVlLFxuICAgIHJlbGV2YW5jZTogMCxcbiAgICBjb250YWluczogW1xuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdhdHRyJyxcbiAgICAgICAgYmVnaW46IC9bXFx3LV0rL1xuICAgICAgfVxuICAgIF1cbiAgfTtcbiAgY29uc3QgUEFSQU1TQkxPQ0sgPSB7XG4gICAgY2xhc3NOYW1lOiAncGFyYW1zJyxcbiAgICBiZWdpbjogL1xcKC8sXG4gICAgZW5kOiAvXFwpLyxcbiAgICBjb250YWluczogW1BBUkFNXSxcbiAgICByZWxldmFuY2U6IDBcbiAgfTtcbiAgY29uc3QgT1BFUkFUSU9OID0ge1xuICAgIGNsYXNzTmFtZTogJ2Z1bmN0aW9uJyxcbiAgICBiZWdpbjogLzpbXFx3XFwtLl0rLyxcbiAgICByZWxldmFuY2U6IDBcbiAgfTtcbiAgY29uc3QgUEFUSCA9IHtcbiAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgIGJlZ2luOiAvXFxCKFtcXC8uXSlbXFx3XFwtLlxcLz1dKy9cbiAgfTtcbiAgY29uc3QgQ09NTUFORF9QQVJBTVMgPSB7XG4gICAgY2xhc3NOYW1lOiAncGFyYW1zJyxcbiAgICBiZWdpbjogLy0tW1xcd1xcLT1cXC9dKy9cbiAgfTtcbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnSkJvc3MgQ0xJJyxcbiAgICBhbGlhc2VzOiBbJ3dpbGRmbHktY2xpJ10sXG4gICAga2V5d29yZHM6IHtcbiAgICAgICRwYXR0ZXJuOiAnW2EtelxcLV0rJyxcbiAgICAgIGtleXdvcmQ6ICdhbGlhcyBiYXRjaCBjZCBjbGVhciBjb21tYW5kIGNvbm5lY3QgY29ubmVjdGlvbi1mYWN0b3J5IGNvbm5lY3Rpb24taW5mbyBkYXRhLXNvdXJjZSBkZXBsb3kgJyArXG4gICAgICAnZGVwbG95bWVudC1pbmZvIGRlcGxveW1lbnQtb3ZlcmxheSBlY2hvIGVjaG8tZG1yIGhlbHAgaGlzdG9yeSBpZiBqZGJjLWRyaXZlci1pbmZvIGptcy1xdWV1ZXwyMCBqbXMtdG9waWN8MjAgbHMgJyArXG4gICAgICAncGF0Y2ggcHdkIHF1aXQgcmVhZC1hdHRyaWJ1dGUgcmVhZC1vcGVyYXRpb24gcmVsb2FkIHJvbGxvdXQtcGxhbiBydW4tYmF0Y2ggc2V0IHNodXRkb3duIHRyeSB1bmFsaWFzICcgK1xuICAgICAgJ3VuZGVwbG95IHVuc2V0IHZlcnNpb24geGEtZGF0YS1zb3VyY2UnLCAvLyBtb2R1bGVcbiAgICAgIGxpdGVyYWw6ICd0cnVlIGZhbHNlJ1xuICAgIH0sXG4gICAgY29udGFpbnM6IFtcbiAgICAgIGhsanMuSEFTSF9DT01NRU5UX01PREUsXG4gICAgICBobGpzLlFVT1RFX1NUUklOR19NT0RFLFxuICAgICAgQ09NTUFORF9QQVJBTVMsXG4gICAgICBPUEVSQVRJT04sXG4gICAgICBQQVRILFxuICAgICAgUEFSQU1TQkxPQ0tcbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gamJvc3NDbGk7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=