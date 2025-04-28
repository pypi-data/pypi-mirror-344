(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_dockerfile"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/dockerfile.js":
/*!*****************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/dockerfile.js ***!
  \*****************************************************************************************************/
/***/ ((module) => {

/*
Language: Dockerfile
Requires: bash.js
Author: Alexis Hénaut <alexis@henaut.net>
Description: language definition for Dockerfile files
Website: https://docs.docker.com/engine/reference/builder/
Category: config
*/

/** @type LanguageFn */
function dockerfile(hljs) {
  return {
    name: 'Dockerfile',
    aliases: ['docker'],
    case_insensitive: true,
    keywords: 'from maintainer expose env arg user onbuild stopsignal',
    contains: [
      hljs.HASH_COMMENT_MODE,
      hljs.APOS_STRING_MODE,
      hljs.QUOTE_STRING_MODE,
      hljs.NUMBER_MODE,
      {
        beginKeywords: 'run cmd entrypoint volume add copy workdir label healthcheck shell',
        starts: {
          end: /[^\\]$/,
          subLanguage: 'bash'
        }
      }
    ],
    illegal: '</'
  };
}

module.exports = dockerfile;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfZG9ja2VyZmlsZS5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL2RvY2tlcmZpbGUuanMiXSwic291cmNlc0NvbnRlbnQiOlsiLypcbkxhbmd1YWdlOiBEb2NrZXJmaWxlXG5SZXF1aXJlczogYmFzaC5qc1xuQXV0aG9yOiBBbGV4aXMgSMOpbmF1dCA8YWxleGlzQGhlbmF1dC5uZXQ+XG5EZXNjcmlwdGlvbjogbGFuZ3VhZ2UgZGVmaW5pdGlvbiBmb3IgRG9ja2VyZmlsZSBmaWxlc1xuV2Vic2l0ZTogaHR0cHM6Ly9kb2NzLmRvY2tlci5jb20vZW5naW5lL3JlZmVyZW5jZS9idWlsZGVyL1xuQ2F0ZWdvcnk6IGNvbmZpZ1xuKi9cblxuLyoqIEB0eXBlIExhbmd1YWdlRm4gKi9cbmZ1bmN0aW9uIGRvY2tlcmZpbGUoaGxqcykge1xuICByZXR1cm4ge1xuICAgIG5hbWU6ICdEb2NrZXJmaWxlJyxcbiAgICBhbGlhc2VzOiBbJ2RvY2tlciddLFxuICAgIGNhc2VfaW5zZW5zaXRpdmU6IHRydWUsXG4gICAga2V5d29yZHM6ICdmcm9tIG1haW50YWluZXIgZXhwb3NlIGVudiBhcmcgdXNlciBvbmJ1aWxkIHN0b3BzaWduYWwnLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBobGpzLkhBU0hfQ09NTUVOVF9NT0RFLFxuICAgICAgaGxqcy5BUE9TX1NUUklOR19NT0RFLFxuICAgICAgaGxqcy5RVU9URV9TVFJJTkdfTU9ERSxcbiAgICAgIGhsanMuTlVNQkVSX01PREUsXG4gICAgICB7XG4gICAgICAgIGJlZ2luS2V5d29yZHM6ICdydW4gY21kIGVudHJ5cG9pbnQgdm9sdW1lIGFkZCBjb3B5IHdvcmtkaXIgbGFiZWwgaGVhbHRoY2hlY2sgc2hlbGwnLFxuICAgICAgICBzdGFydHM6IHtcbiAgICAgICAgICBlbmQ6IC9bXlxcXFxdJC8sXG4gICAgICAgICAgc3ViTGFuZ3VhZ2U6ICdiYXNoJ1xuICAgICAgICB9XG4gICAgICB9XG4gICAgXSxcbiAgICBpbGxlZ2FsOiAnPC8nXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gZG9ja2VyZmlsZTtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==