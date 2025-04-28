(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_nim"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/nim.js":
/*!**********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/nim.js ***!
  \**********************************************************************************************/
/***/ ((module) => {

/*
Language: Nim
Description: Nim is a statically typed compiled systems programming language.
Website: https://nim-lang.org
Category: system
*/

function nim(hljs) {
  return {
    name: 'Nim',
    keywords: {
      keyword:
        'addr and as asm bind block break case cast const continue converter ' +
        'discard distinct div do elif else end enum except export finally ' +
        'for from func generic if import in include interface is isnot iterator ' +
        'let macro method mixin mod nil not notin object of or out proc ptr ' +
        'raise ref return shl shr static template try tuple type using var ' +
        'when while with without xor yield',
      literal:
        'shared guarded stdin stdout stderr result true false',
      built_in:
        'int int8 int16 int32 int64 uint uint8 uint16 uint32 uint64 float ' +
        'float32 float64 bool char string cstring pointer expr stmt void ' +
        'auto any range array openarray varargs seq set clong culong cchar ' +
        'cschar cshort cint csize clonglong cfloat cdouble clongdouble ' +
        'cuchar cushort cuint culonglong cstringarray semistatic'
    },
    contains: [
      {
        className: 'meta', // Actually pragma
        begin: /\{\./,
        end: /\.\}/,
        relevance: 10
      },
      {
        className: 'string',
        begin: /[a-zA-Z]\w*"/,
        end: /"/,
        contains: [
          {
            begin: /""/
          }
        ]
      },
      {
        className: 'string',
        begin: /([a-zA-Z]\w*)?"""/,
        end: /"""/
      },
      hljs.QUOTE_STRING_MODE,
      {
        className: 'type',
        begin: /\b[A-Z]\w+\b/,
        relevance: 0
      },
      {
        className: 'number',
        relevance: 0,
        variants: [
          {
            begin: /\b(0[xX][0-9a-fA-F][_0-9a-fA-F]*)('?[iIuU](8|16|32|64))?/
          },
          {
            begin: /\b(0o[0-7][_0-7]*)('?[iIuUfF](8|16|32|64))?/
          },
          {
            begin: /\b(0(b|B)[01][_01]*)('?[iIuUfF](8|16|32|64))?/
          },
          {
            begin: /\b(\d[_\d]*)('?[iIuUfF](8|16|32|64))?/
          }
        ]
      },
      hljs.HASH_COMMENT_MODE
    ]
  };
}

module.exports = nim;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfbmltLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7QUFDQSxrQkFBa0I7QUFDbEIsa0JBQWtCO0FBQ2xCO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFdBQVc7QUFDWDtBQUNBO0FBQ0EsV0FBVztBQUNYO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL25pbS5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKlxuTGFuZ3VhZ2U6IE5pbVxuRGVzY3JpcHRpb246IE5pbSBpcyBhIHN0YXRpY2FsbHkgdHlwZWQgY29tcGlsZWQgc3lzdGVtcyBwcm9ncmFtbWluZyBsYW5ndWFnZS5cbldlYnNpdGU6IGh0dHBzOi8vbmltLWxhbmcub3JnXG5DYXRlZ29yeTogc3lzdGVtXG4qL1xuXG5mdW5jdGlvbiBuaW0oaGxqcykge1xuICByZXR1cm4ge1xuICAgIG5hbWU6ICdOaW0nLFxuICAgIGtleXdvcmRzOiB7XG4gICAgICBrZXl3b3JkOlxuICAgICAgICAnYWRkciBhbmQgYXMgYXNtIGJpbmQgYmxvY2sgYnJlYWsgY2FzZSBjYXN0IGNvbnN0IGNvbnRpbnVlIGNvbnZlcnRlciAnICtcbiAgICAgICAgJ2Rpc2NhcmQgZGlzdGluY3QgZGl2IGRvIGVsaWYgZWxzZSBlbmQgZW51bSBleGNlcHQgZXhwb3J0IGZpbmFsbHkgJyArXG4gICAgICAgICdmb3IgZnJvbSBmdW5jIGdlbmVyaWMgaWYgaW1wb3J0IGluIGluY2x1ZGUgaW50ZXJmYWNlIGlzIGlzbm90IGl0ZXJhdG9yICcgK1xuICAgICAgICAnbGV0IG1hY3JvIG1ldGhvZCBtaXhpbiBtb2QgbmlsIG5vdCBub3RpbiBvYmplY3Qgb2Ygb3Igb3V0IHByb2MgcHRyICcgK1xuICAgICAgICAncmFpc2UgcmVmIHJldHVybiBzaGwgc2hyIHN0YXRpYyB0ZW1wbGF0ZSB0cnkgdHVwbGUgdHlwZSB1c2luZyB2YXIgJyArXG4gICAgICAgICd3aGVuIHdoaWxlIHdpdGggd2l0aG91dCB4b3IgeWllbGQnLFxuICAgICAgbGl0ZXJhbDpcbiAgICAgICAgJ3NoYXJlZCBndWFyZGVkIHN0ZGluIHN0ZG91dCBzdGRlcnIgcmVzdWx0IHRydWUgZmFsc2UnLFxuICAgICAgYnVpbHRfaW46XG4gICAgICAgICdpbnQgaW50OCBpbnQxNiBpbnQzMiBpbnQ2NCB1aW50IHVpbnQ4IHVpbnQxNiB1aW50MzIgdWludDY0IGZsb2F0ICcgK1xuICAgICAgICAnZmxvYXQzMiBmbG9hdDY0IGJvb2wgY2hhciBzdHJpbmcgY3N0cmluZyBwb2ludGVyIGV4cHIgc3RtdCB2b2lkICcgK1xuICAgICAgICAnYXV0byBhbnkgcmFuZ2UgYXJyYXkgb3BlbmFycmF5IHZhcmFyZ3Mgc2VxIHNldCBjbG9uZyBjdWxvbmcgY2NoYXIgJyArXG4gICAgICAgICdjc2NoYXIgY3Nob3J0IGNpbnQgY3NpemUgY2xvbmdsb25nIGNmbG9hdCBjZG91YmxlIGNsb25nZG91YmxlICcgK1xuICAgICAgICAnY3VjaGFyIGN1c2hvcnQgY3VpbnQgY3Vsb25nbG9uZyBjc3RyaW5nYXJyYXkgc2VtaXN0YXRpYydcbiAgICB9LFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ21ldGEnLCAvLyBBY3R1YWxseSBwcmFnbWFcbiAgICAgICAgYmVnaW46IC9cXHtcXC4vLFxuICAgICAgICBlbmQ6IC9cXC5cXH0vLFxuICAgICAgICByZWxldmFuY2U6IDEwXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgICAgICBiZWdpbjogL1thLXpBLVpdXFx3KlwiLyxcbiAgICAgICAgZW5kOiAvXCIvLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiAvXCJcIi9cbiAgICAgICAgICB9XG4gICAgICAgIF1cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3N0cmluZycsXG4gICAgICAgIGJlZ2luOiAvKFthLXpBLVpdXFx3Kik/XCJcIlwiLyxcbiAgICAgICAgZW5kOiAvXCJcIlwiL1xuICAgICAgfSxcbiAgICAgIGhsanMuUVVPVEVfU1RSSU5HX01PREUsXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3R5cGUnLFxuICAgICAgICBiZWdpbjogL1xcYltBLVpdXFx3K1xcYi8sXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnbnVtYmVyJyxcbiAgICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgICB2YXJpYW50czogW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiAvXFxiKDBbeFhdWzAtOWEtZkEtRl1bXzAtOWEtZkEtRl0qKSgnP1tpSXVVXSg4fDE2fDMyfDY0KSk/L1xuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgYmVnaW46IC9cXGIoMG9bMC03XVtfMC03XSopKCc/W2lJdVVmRl0oOHwxNnwzMnw2NCkpPy9cbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiAvXFxiKDAoYnxCKVswMV1bXzAxXSopKCc/W2lJdVVmRl0oOHwxNnwzMnw2NCkpPy9cbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiAvXFxiKFxcZFtfXFxkXSopKCc/W2lJdVVmRl0oOHwxNnwzMnw2NCkpPy9cbiAgICAgICAgICB9XG4gICAgICAgIF1cbiAgICAgIH0sXG4gICAgICBobGpzLkhBU0hfQ09NTUVOVF9NT0RFXG4gICAgXVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IG5pbTtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==