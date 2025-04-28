(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_go"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/go.js":
/*!*********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/go.js ***!
  \*********************************************************************************************/
/***/ ((module) => {

/*
Language: Go
Author: Stephan Kountso aka StepLg <steplg@gmail.com>
Contributors: Evgeny Stepanischev <imbolk@gmail.com>
Description: Google go language (golang). For info about language
Website: http://golang.org/
Category: common, system
*/

function go(hljs) {
  const GO_KEYWORDS = {
    keyword:
      'break default func interface select case map struct chan else goto package switch ' +
      'const fallthrough if range type continue for import return var go defer ' +
      'bool byte complex64 complex128 float32 float64 int8 int16 int32 int64 string uint8 ' +
      'uint16 uint32 uint64 int uint uintptr rune',
    literal:
       'true false iota nil',
    built_in:
      'append cap close complex copy imag len make new panic print println real recover delete'
  };
  return {
    name: 'Go',
    aliases: ['golang'],
    keywords: GO_KEYWORDS,
    illegal: '</',
    contains: [
      hljs.C_LINE_COMMENT_MODE,
      hljs.C_BLOCK_COMMENT_MODE,
      {
        className: 'string',
        variants: [
          hljs.QUOTE_STRING_MODE,
          hljs.APOS_STRING_MODE,
          {
            begin: '`',
            end: '`'
          }
        ]
      },
      {
        className: 'number',
        variants: [
          {
            begin: hljs.C_NUMBER_RE + '[i]',
            relevance: 1
          },
          hljs.C_NUMBER_MODE
        ]
      },
      {
        begin: /:=/ // relevance booster
      },
      {
        className: 'function',
        beginKeywords: 'func',
        end: '\\s*(\\{|$)',
        excludeEnd: true,
        contains: [
          hljs.TITLE_MODE,
          {
            className: 'params',
            begin: /\(/,
            end: /\)/,
            keywords: GO_KEYWORDS,
            illegal: /["']/
          }
        ]
      }
    ]
  };
}

module.exports = go;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfZ28uZHRhbGVfYnVuZGxlLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsV0FBVztBQUNYO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSxzQkFBc0I7QUFDdEI7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9nby5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKlxuTGFuZ3VhZ2U6IEdvXG5BdXRob3I6IFN0ZXBoYW4gS291bnRzbyBha2EgU3RlcExnIDxzdGVwbGdAZ21haWwuY29tPlxuQ29udHJpYnV0b3JzOiBFdmdlbnkgU3RlcGFuaXNjaGV2IDxpbWJvbGtAZ21haWwuY29tPlxuRGVzY3JpcHRpb246IEdvb2dsZSBnbyBsYW5ndWFnZSAoZ29sYW5nKS4gRm9yIGluZm8gYWJvdXQgbGFuZ3VhZ2VcbldlYnNpdGU6IGh0dHA6Ly9nb2xhbmcub3JnL1xuQ2F0ZWdvcnk6IGNvbW1vbiwgc3lzdGVtXG4qL1xuXG5mdW5jdGlvbiBnbyhobGpzKSB7XG4gIGNvbnN0IEdPX0tFWVdPUkRTID0ge1xuICAgIGtleXdvcmQ6XG4gICAgICAnYnJlYWsgZGVmYXVsdCBmdW5jIGludGVyZmFjZSBzZWxlY3QgY2FzZSBtYXAgc3RydWN0IGNoYW4gZWxzZSBnb3RvIHBhY2thZ2Ugc3dpdGNoICcgK1xuICAgICAgJ2NvbnN0IGZhbGx0aHJvdWdoIGlmIHJhbmdlIHR5cGUgY29udGludWUgZm9yIGltcG9ydCByZXR1cm4gdmFyIGdvIGRlZmVyICcgK1xuICAgICAgJ2Jvb2wgYnl0ZSBjb21wbGV4NjQgY29tcGxleDEyOCBmbG9hdDMyIGZsb2F0NjQgaW50OCBpbnQxNiBpbnQzMiBpbnQ2NCBzdHJpbmcgdWludDggJyArXG4gICAgICAndWludDE2IHVpbnQzMiB1aW50NjQgaW50IHVpbnQgdWludHB0ciBydW5lJyxcbiAgICBsaXRlcmFsOlxuICAgICAgICd0cnVlIGZhbHNlIGlvdGEgbmlsJyxcbiAgICBidWlsdF9pbjpcbiAgICAgICdhcHBlbmQgY2FwIGNsb3NlIGNvbXBsZXggY29weSBpbWFnIGxlbiBtYWtlIG5ldyBwYW5pYyBwcmludCBwcmludGxuIHJlYWwgcmVjb3ZlciBkZWxldGUnXG4gIH07XG4gIHJldHVybiB7XG4gICAgbmFtZTogJ0dvJyxcbiAgICBhbGlhc2VzOiBbJ2dvbGFuZyddLFxuICAgIGtleXdvcmRzOiBHT19LRVlXT1JEUyxcbiAgICBpbGxlZ2FsOiAnPC8nLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBobGpzLkNfTElORV9DT01NRU5UX01PREUsXG4gICAgICBobGpzLkNfQkxPQ0tfQ09NTUVOVF9NT0RFLFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgICAgICB2YXJpYW50czogW1xuICAgICAgICAgIGhsanMuUVVPVEVfU1RSSU5HX01PREUsXG4gICAgICAgICAgaGxqcy5BUE9TX1NUUklOR19NT0RFLFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiAnYCcsXG4gICAgICAgICAgICBlbmQ6ICdgJ1xuICAgICAgICAgIH1cbiAgICAgICAgXVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnbnVtYmVyJyxcbiAgICAgICAgdmFyaWFudHM6IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbjogaGxqcy5DX05VTUJFUl9SRSArICdbaV0nLFxuICAgICAgICAgICAgcmVsZXZhbmNlOiAxXG4gICAgICAgICAgfSxcbiAgICAgICAgICBobGpzLkNfTlVNQkVSX01PREVcbiAgICAgICAgXVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC86PS8gLy8gcmVsZXZhbmNlIGJvb3N0ZXJcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ2Z1bmN0aW9uJyxcbiAgICAgICAgYmVnaW5LZXl3b3JkczogJ2Z1bmMnLFxuICAgICAgICBlbmQ6ICdcXFxccyooXFxcXHt8JCknLFxuICAgICAgICBleGNsdWRlRW5kOiB0cnVlLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIGhsanMuVElUTEVfTU9ERSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICBjbGFzc05hbWU6ICdwYXJhbXMnLFxuICAgICAgICAgICAgYmVnaW46IC9cXCgvLFxuICAgICAgICAgICAgZW5kOiAvXFwpLyxcbiAgICAgICAgICAgIGtleXdvcmRzOiBHT19LRVlXT1JEUyxcbiAgICAgICAgICAgIGlsbGVnYWw6IC9bXCInXS9cbiAgICAgICAgICB9XG4gICAgICAgIF1cbiAgICAgIH1cbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gZ287XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=