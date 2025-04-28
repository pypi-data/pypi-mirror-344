(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_makefile"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/makefile.js":
/*!***************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/makefile.js ***!
  \***************************************************************************************************/
/***/ ((module) => {

/*
Language: Makefile
Author: Ivan Sagalaev <maniac@softwaremaniacs.org>
Contributors: Joël Porquet <joel@porquet.org>
Website: https://www.gnu.org/software/make/manual/html_node/Introduction.html
Category: common
*/

function makefile(hljs) {
  /* Variables: simple (eg $(var)) and special (eg $@) */
  const VARIABLE = {
    className: 'variable',
    variants: [
      {
        begin: '\\$\\(' + hljs.UNDERSCORE_IDENT_RE + '\\)',
        contains: [ hljs.BACKSLASH_ESCAPE ]
      },
      {
        begin: /\$[@%<?\^\+\*]/
      }
    ]
  };
  /* Quoted string with variables inside */
  const QUOTE_STRING = {
    className: 'string',
    begin: /"/,
    end: /"/,
    contains: [
      hljs.BACKSLASH_ESCAPE,
      VARIABLE
    ]
  };
  /* Function: $(func arg,...) */
  const FUNC = {
    className: 'variable',
    begin: /\$\([\w-]+\s/,
    end: /\)/,
    keywords: {
      built_in:
        'subst patsubst strip findstring filter filter-out sort ' +
        'word wordlist firstword lastword dir notdir suffix basename ' +
        'addsuffix addprefix join wildcard realpath abspath error warning ' +
        'shell origin flavor foreach if or and call eval file value'
    },
    contains: [ VARIABLE ]
  };
  /* Variable assignment */
  const ASSIGNMENT = {
    begin: '^' + hljs.UNDERSCORE_IDENT_RE + '\\s*(?=[:+?]?=)'
  };
  /* Meta targets (.PHONY) */
  const META = {
    className: 'meta',
    begin: /^\.PHONY:/,
    end: /$/,
    keywords: {
      $pattern: /[\.\w]+/,
      'meta-keyword': '.PHONY'
    }
  };
  /* Targets */
  const TARGET = {
    className: 'section',
    begin: /^[^\s]+:/,
    end: /$/,
    contains: [ VARIABLE ]
  };
  return {
    name: 'Makefile',
    aliases: [
      'mk',
      'mak',
      'make',
    ],
    keywords: {
      $pattern: /[\w-]+/,
      keyword: 'define endef undefine ifdef ifndef ifeq ifneq else endif ' +
      'include -include sinclude override export unexport private vpath'
    },
    contains: [
      hljs.HASH_COMMENT_MODE,
      VARIABLE,
      QUOTE_STRING,
      FUNC,
      ASSIGNMENT,
      META,
      TARGET
    ]
  };
}

module.exports = makefile;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfbWFrZWZpbGUuZHRhbGVfYnVuZGxlLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsS0FBSztBQUNMO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL21ha2VmaWxlLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogTWFrZWZpbGVcbkF1dGhvcjogSXZhbiBTYWdhbGFldiA8bWFuaWFjQHNvZnR3YXJlbWFuaWFjcy5vcmc+XG5Db250cmlidXRvcnM6IEpvw6tsIFBvcnF1ZXQgPGpvZWxAcG9ycXVldC5vcmc+XG5XZWJzaXRlOiBodHRwczovL3d3dy5nbnUub3JnL3NvZnR3YXJlL21ha2UvbWFudWFsL2h0bWxfbm9kZS9JbnRyb2R1Y3Rpb24uaHRtbFxuQ2F0ZWdvcnk6IGNvbW1vblxuKi9cblxuZnVuY3Rpb24gbWFrZWZpbGUoaGxqcykge1xuICAvKiBWYXJpYWJsZXM6IHNpbXBsZSAoZWcgJCh2YXIpKSBhbmQgc3BlY2lhbCAoZWcgJEApICovXG4gIGNvbnN0IFZBUklBQkxFID0ge1xuICAgIGNsYXNzTmFtZTogJ3ZhcmlhYmxlJyxcbiAgICB2YXJpYW50czogW1xuICAgICAge1xuICAgICAgICBiZWdpbjogJ1xcXFwkXFxcXCgnICsgaGxqcy5VTkRFUlNDT1JFX0lERU5UX1JFICsgJ1xcXFwpJyxcbiAgICAgICAgY29udGFpbnM6IFsgaGxqcy5CQUNLU0xBU0hfRVNDQVBFIF1cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiAvXFwkW0AlPD9cXF5cXCtcXCpdL1xuICAgICAgfVxuICAgIF1cbiAgfTtcbiAgLyogUXVvdGVkIHN0cmluZyB3aXRoIHZhcmlhYmxlcyBpbnNpZGUgKi9cbiAgY29uc3QgUVVPVEVfU1RSSU5HID0ge1xuICAgIGNsYXNzTmFtZTogJ3N0cmluZycsXG4gICAgYmVnaW46IC9cIi8sXG4gICAgZW5kOiAvXCIvLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBobGpzLkJBQ0tTTEFTSF9FU0NBUEUsXG4gICAgICBWQVJJQUJMRVxuICAgIF1cbiAgfTtcbiAgLyogRnVuY3Rpb246ICQoZnVuYyBhcmcsLi4uKSAqL1xuICBjb25zdCBGVU5DID0ge1xuICAgIGNsYXNzTmFtZTogJ3ZhcmlhYmxlJyxcbiAgICBiZWdpbjogL1xcJFxcKFtcXHctXStcXHMvLFxuICAgIGVuZDogL1xcKS8sXG4gICAga2V5d29yZHM6IHtcbiAgICAgIGJ1aWx0X2luOlxuICAgICAgICAnc3Vic3QgcGF0c3Vic3Qgc3RyaXAgZmluZHN0cmluZyBmaWx0ZXIgZmlsdGVyLW91dCBzb3J0ICcgK1xuICAgICAgICAnd29yZCB3b3JkbGlzdCBmaXJzdHdvcmQgbGFzdHdvcmQgZGlyIG5vdGRpciBzdWZmaXggYmFzZW5hbWUgJyArXG4gICAgICAgICdhZGRzdWZmaXggYWRkcHJlZml4IGpvaW4gd2lsZGNhcmQgcmVhbHBhdGggYWJzcGF0aCBlcnJvciB3YXJuaW5nICcgK1xuICAgICAgICAnc2hlbGwgb3JpZ2luIGZsYXZvciBmb3JlYWNoIGlmIG9yIGFuZCBjYWxsIGV2YWwgZmlsZSB2YWx1ZSdcbiAgICB9LFxuICAgIGNvbnRhaW5zOiBbIFZBUklBQkxFIF1cbiAgfTtcbiAgLyogVmFyaWFibGUgYXNzaWdubWVudCAqL1xuICBjb25zdCBBU1NJR05NRU5UID0ge1xuICAgIGJlZ2luOiAnXicgKyBobGpzLlVOREVSU0NPUkVfSURFTlRfUkUgKyAnXFxcXHMqKD89WzorP10/PSknXG4gIH07XG4gIC8qIE1ldGEgdGFyZ2V0cyAoLlBIT05ZKSAqL1xuICBjb25zdCBNRVRBID0ge1xuICAgIGNsYXNzTmFtZTogJ21ldGEnLFxuICAgIGJlZ2luOiAvXlxcLlBIT05ZOi8sXG4gICAgZW5kOiAvJC8sXG4gICAga2V5d29yZHM6IHtcbiAgICAgICRwYXR0ZXJuOiAvW1xcLlxcd10rLyxcbiAgICAgICdtZXRhLWtleXdvcmQnOiAnLlBIT05ZJ1xuICAgIH1cbiAgfTtcbiAgLyogVGFyZ2V0cyAqL1xuICBjb25zdCBUQVJHRVQgPSB7XG4gICAgY2xhc3NOYW1lOiAnc2VjdGlvbicsXG4gICAgYmVnaW46IC9eW15cXHNdKzovLFxuICAgIGVuZDogLyQvLFxuICAgIGNvbnRhaW5zOiBbIFZBUklBQkxFIF1cbiAgfTtcbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnTWFrZWZpbGUnLFxuICAgIGFsaWFzZXM6IFtcbiAgICAgICdtaycsXG4gICAgICAnbWFrJyxcbiAgICAgICdtYWtlJyxcbiAgICBdLFxuICAgIGtleXdvcmRzOiB7XG4gICAgICAkcGF0dGVybjogL1tcXHctXSsvLFxuICAgICAga2V5d29yZDogJ2RlZmluZSBlbmRlZiB1bmRlZmluZSBpZmRlZiBpZm5kZWYgaWZlcSBpZm5lcSBlbHNlIGVuZGlmICcgK1xuICAgICAgJ2luY2x1ZGUgLWluY2x1ZGUgc2luY2x1ZGUgb3ZlcnJpZGUgZXhwb3J0IHVuZXhwb3J0IHByaXZhdGUgdnBhdGgnXG4gICAgfSxcbiAgICBjb250YWluczogW1xuICAgICAgaGxqcy5IQVNIX0NPTU1FTlRfTU9ERSxcbiAgICAgIFZBUklBQkxFLFxuICAgICAgUVVPVEVfU1RSSU5HLFxuICAgICAgRlVOQyxcbiAgICAgIEFTU0lHTk1FTlQsXG4gICAgICBNRVRBLFxuICAgICAgVEFSR0VUXG4gICAgXVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IG1ha2VmaWxlO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9