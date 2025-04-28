(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_xl"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/xl.js":
/*!*********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/xl.js ***!
  \*********************************************************************************************/
/***/ ((module) => {

/*
Language: XL
Author: Christophe de Dinechin <christophe@taodyne.com>
Description: An extensible programming language, based on parse tree rewriting
Website: http://xlr.sf.net
*/

function xl(hljs) {
  const BUILTIN_MODULES =
    'ObjectLoader Animate MovieCredits Slides Filters Shading Materials LensFlare Mapping VLCAudioVideo ' +
    'StereoDecoder PointCloud NetworkAccess RemoteControl RegExp ChromaKey Snowfall NodeJS Speech Charts';

  const XL_KEYWORDS = {
    $pattern: /[a-zA-Z][a-zA-Z0-9_?]*/,
    keyword:
      'if then else do while until for loop import with is as where when by data constant ' +
      'integer real text name boolean symbol infix prefix postfix block tree',
    literal:
      'true false nil',
    built_in:
      'in mod rem and or xor not abs sign floor ceil sqrt sin cos tan asin ' +
      'acos atan exp expm1 log log2 log10 log1p pi at text_length text_range ' +
      'text_find text_replace contains page slide basic_slide title_slide ' +
      'title subtitle fade_in fade_out fade_at clear_color color line_color ' +
      'line_width texture_wrap texture_transform texture scale_?x scale_?y ' +
      'scale_?z? translate_?x translate_?y translate_?z? rotate_?x rotate_?y ' +
      'rotate_?z? rectangle circle ellipse sphere path line_to move_to ' +
      'quad_to curve_to theme background contents locally time mouse_?x ' +
      'mouse_?y mouse_buttons ' +
      BUILTIN_MODULES
  };

  const DOUBLE_QUOTE_TEXT = {
    className: 'string',
    begin: '"',
    end: '"',
    illegal: '\\n'
  };
  const SINGLE_QUOTE_TEXT = {
    className: 'string',
    begin: '\'',
    end: '\'',
    illegal: '\\n'
  };
  const LONG_TEXT = {
    className: 'string',
    begin: '<<',
    end: '>>'
  };
  const BASED_NUMBER = {
    className: 'number',
    begin: '[0-9]+#[0-9A-Z_]+(\\.[0-9-A-Z_]+)?#?([Ee][+-]?[0-9]+)?'
  };
  const IMPORT = {
    beginKeywords: 'import',
    end: '$',
    keywords: XL_KEYWORDS,
    contains: [ DOUBLE_QUOTE_TEXT ]
  };
  const FUNCTION_DEFINITION = {
    className: 'function',
    begin: /[a-z][^\n]*->/,
    returnBegin: true,
    end: /->/,
    contains: [
      hljs.inherit(hljs.TITLE_MODE, {
        starts: {
          endsWithParent: true,
          keywords: XL_KEYWORDS
        }
      })
    ]
  };
  return {
    name: 'XL',
    aliases: [ 'tao' ],
    keywords: XL_KEYWORDS,
    contains: [
      hljs.C_LINE_COMMENT_MODE,
      hljs.C_BLOCK_COMMENT_MODE,
      DOUBLE_QUOTE_TEXT,
      SINGLE_QUOTE_TEXT,
      LONG_TEXT,
      FUNCTION_DEFINITION,
      IMPORT,
      BASED_NUMBER,
      hljs.NUMBER_MODE
    ]
  };
}

module.exports = xl;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfeGwuZHRhbGVfYnVuZGxlLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL3hsLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogWExcbkF1dGhvcjogQ2hyaXN0b3BoZSBkZSBEaW5lY2hpbiA8Y2hyaXN0b3BoZUB0YW9keW5lLmNvbT5cbkRlc2NyaXB0aW9uOiBBbiBleHRlbnNpYmxlIHByb2dyYW1taW5nIGxhbmd1YWdlLCBiYXNlZCBvbiBwYXJzZSB0cmVlIHJld3JpdGluZ1xuV2Vic2l0ZTogaHR0cDovL3hsci5zZi5uZXRcbiovXG5cbmZ1bmN0aW9uIHhsKGhsanMpIHtcbiAgY29uc3QgQlVJTFRJTl9NT0RVTEVTID1cbiAgICAnT2JqZWN0TG9hZGVyIEFuaW1hdGUgTW92aWVDcmVkaXRzIFNsaWRlcyBGaWx0ZXJzIFNoYWRpbmcgTWF0ZXJpYWxzIExlbnNGbGFyZSBNYXBwaW5nIFZMQ0F1ZGlvVmlkZW8gJyArXG4gICAgJ1N0ZXJlb0RlY29kZXIgUG9pbnRDbG91ZCBOZXR3b3JrQWNjZXNzIFJlbW90ZUNvbnRyb2wgUmVnRXhwIENocm9tYUtleSBTbm93ZmFsbCBOb2RlSlMgU3BlZWNoIENoYXJ0cyc7XG5cbiAgY29uc3QgWExfS0VZV09SRFMgPSB7XG4gICAgJHBhdHRlcm46IC9bYS16QS1aXVthLXpBLVowLTlfP10qLyxcbiAgICBrZXl3b3JkOlxuICAgICAgJ2lmIHRoZW4gZWxzZSBkbyB3aGlsZSB1bnRpbCBmb3IgbG9vcCBpbXBvcnQgd2l0aCBpcyBhcyB3aGVyZSB3aGVuIGJ5IGRhdGEgY29uc3RhbnQgJyArXG4gICAgICAnaW50ZWdlciByZWFsIHRleHQgbmFtZSBib29sZWFuIHN5bWJvbCBpbmZpeCBwcmVmaXggcG9zdGZpeCBibG9jayB0cmVlJyxcbiAgICBsaXRlcmFsOlxuICAgICAgJ3RydWUgZmFsc2UgbmlsJyxcbiAgICBidWlsdF9pbjpcbiAgICAgICdpbiBtb2QgcmVtIGFuZCBvciB4b3Igbm90IGFicyBzaWduIGZsb29yIGNlaWwgc3FydCBzaW4gY29zIHRhbiBhc2luICcgK1xuICAgICAgJ2Fjb3MgYXRhbiBleHAgZXhwbTEgbG9nIGxvZzIgbG9nMTAgbG9nMXAgcGkgYXQgdGV4dF9sZW5ndGggdGV4dF9yYW5nZSAnICtcbiAgICAgICd0ZXh0X2ZpbmQgdGV4dF9yZXBsYWNlIGNvbnRhaW5zIHBhZ2Ugc2xpZGUgYmFzaWNfc2xpZGUgdGl0bGVfc2xpZGUgJyArXG4gICAgICAndGl0bGUgc3VidGl0bGUgZmFkZV9pbiBmYWRlX291dCBmYWRlX2F0IGNsZWFyX2NvbG9yIGNvbG9yIGxpbmVfY29sb3IgJyArXG4gICAgICAnbGluZV93aWR0aCB0ZXh0dXJlX3dyYXAgdGV4dHVyZV90cmFuc2Zvcm0gdGV4dHVyZSBzY2FsZV8/eCBzY2FsZV8/eSAnICtcbiAgICAgICdzY2FsZV8/ej8gdHJhbnNsYXRlXz94IHRyYW5zbGF0ZV8/eSB0cmFuc2xhdGVfP3o/IHJvdGF0ZV8/eCByb3RhdGVfP3kgJyArXG4gICAgICAncm90YXRlXz96PyByZWN0YW5nbGUgY2lyY2xlIGVsbGlwc2Ugc3BoZXJlIHBhdGggbGluZV90byBtb3ZlX3RvICcgK1xuICAgICAgJ3F1YWRfdG8gY3VydmVfdG8gdGhlbWUgYmFja2dyb3VuZCBjb250ZW50cyBsb2NhbGx5IHRpbWUgbW91c2VfP3ggJyArXG4gICAgICAnbW91c2VfP3kgbW91c2VfYnV0dG9ucyAnICtcbiAgICAgIEJVSUxUSU5fTU9EVUxFU1xuICB9O1xuXG4gIGNvbnN0IERPVUJMRV9RVU9URV9URVhUID0ge1xuICAgIGNsYXNzTmFtZTogJ3N0cmluZycsXG4gICAgYmVnaW46ICdcIicsXG4gICAgZW5kOiAnXCInLFxuICAgIGlsbGVnYWw6ICdcXFxcbidcbiAgfTtcbiAgY29uc3QgU0lOR0xFX1FVT1RFX1RFWFQgPSB7XG4gICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICBiZWdpbjogJ1xcJycsXG4gICAgZW5kOiAnXFwnJyxcbiAgICBpbGxlZ2FsOiAnXFxcXG4nXG4gIH07XG4gIGNvbnN0IExPTkdfVEVYVCA9IHtcbiAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgIGJlZ2luOiAnPDwnLFxuICAgIGVuZDogJz4+J1xuICB9O1xuICBjb25zdCBCQVNFRF9OVU1CRVIgPSB7XG4gICAgY2xhc3NOYW1lOiAnbnVtYmVyJyxcbiAgICBiZWdpbjogJ1swLTldKyNbMC05QS1aX10rKFxcXFwuWzAtOS1BLVpfXSspPyM/KFtFZV1bKy1dP1swLTldKyk/J1xuICB9O1xuICBjb25zdCBJTVBPUlQgPSB7XG4gICAgYmVnaW5LZXl3b3JkczogJ2ltcG9ydCcsXG4gICAgZW5kOiAnJCcsXG4gICAga2V5d29yZHM6IFhMX0tFWVdPUkRTLFxuICAgIGNvbnRhaW5zOiBbIERPVUJMRV9RVU9URV9URVhUIF1cbiAgfTtcbiAgY29uc3QgRlVOQ1RJT05fREVGSU5JVElPTiA9IHtcbiAgICBjbGFzc05hbWU6ICdmdW5jdGlvbicsXG4gICAgYmVnaW46IC9bYS16XVteXFxuXSotPi8sXG4gICAgcmV0dXJuQmVnaW46IHRydWUsXG4gICAgZW5kOiAvLT4vLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBobGpzLmluaGVyaXQoaGxqcy5USVRMRV9NT0RFLCB7XG4gICAgICAgIHN0YXJ0czoge1xuICAgICAgICAgIGVuZHNXaXRoUGFyZW50OiB0cnVlLFxuICAgICAgICAgIGtleXdvcmRzOiBYTF9LRVlXT1JEU1xuICAgICAgICB9XG4gICAgICB9KVxuICAgIF1cbiAgfTtcbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnWEwnLFxuICAgIGFsaWFzZXM6IFsgJ3RhbycgXSxcbiAgICBrZXl3b3JkczogWExfS0VZV09SRFMsXG4gICAgY29udGFpbnM6IFtcbiAgICAgIGhsanMuQ19MSU5FX0NPTU1FTlRfTU9ERSxcbiAgICAgIGhsanMuQ19CTE9DS19DT01NRU5UX01PREUsXG4gICAgICBET1VCTEVfUVVPVEVfVEVYVCxcbiAgICAgIFNJTkdMRV9RVU9URV9URVhULFxuICAgICAgTE9OR19URVhULFxuICAgICAgRlVOQ1RJT05fREVGSU5JVElPTixcbiAgICAgIElNUE9SVCxcbiAgICAgIEJBU0VEX05VTUJFUixcbiAgICAgIGhsanMuTlVNQkVSX01PREVcbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0geGw7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=