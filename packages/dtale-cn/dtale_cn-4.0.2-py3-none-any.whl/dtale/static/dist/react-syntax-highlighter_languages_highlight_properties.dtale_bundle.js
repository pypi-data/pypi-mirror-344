(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_properties"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/properties.js":
/*!*****************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/properties.js ***!
  \*****************************************************************************************************/
/***/ ((module) => {

/*
Language: .properties
Contributors: Valentin Aitken <valentin@nalisbg.com>, Egor Rogov <e.rogov@postgrespro.ru>
Website: https://en.wikipedia.org/wiki/.properties
Category: common, config
*/

function properties(hljs) {

  // whitespaces: space, tab, formfeed
  var WS0 = '[ \\t\\f]*';
  var WS1 = '[ \\t\\f]+';
  // delimiter
  var EQUAL_DELIM = WS0+'[:=]'+WS0;
  var WS_DELIM = WS1;
  var DELIM = '(' + EQUAL_DELIM + '|' + WS_DELIM + ')';
  var KEY_ALPHANUM = '([^\\\\\\W:= \\t\\f\\n]|\\\\.)+';
  var KEY_OTHER = '([^\\\\:= \\t\\f\\n]|\\\\.)+';

  var DELIM_AND_VALUE = {
          // skip DELIM
          end: DELIM,
          relevance: 0,
          starts: {
            // value: everything until end of line (again, taking into account backslashes)
            className: 'string',
            end: /$/,
            relevance: 0,
            contains: [
              { begin: '\\\\\\\\'},
              { begin: '\\\\\\n' }
            ]
          }
        };

  return {
    name: '.properties',
    case_insensitive: true,
    illegal: /\S/,
    contains: [
      hljs.COMMENT('^\\s*[!#]', '$'),
      // key: everything until whitespace or = or : (taking into account backslashes)
      // case of a "normal" key
      {
        returnBegin: true,
        variants: [
          { begin: KEY_ALPHANUM + EQUAL_DELIM, relevance: 1 },
          { begin: KEY_ALPHANUM + WS_DELIM, relevance: 0 }
        ],
        contains: [
          {
            className: 'attr',
            begin: KEY_ALPHANUM,
            endsParent: true,
            relevance: 0
          }
        ],
        starts: DELIM_AND_VALUE
      },
      // case of key containing non-alphanumeric chars => relevance = 0
      {
        begin: KEY_OTHER + DELIM,
        returnBegin: true,
        relevance: 0,
        contains: [
          {
            className: 'meta',
            begin: KEY_OTHER,
            endsParent: true,
            relevance: 0
          }
        ],
        starts: DELIM_AND_VALUE
      },
      // case of an empty key
      {
        className: 'attr',
        relevance: 0,
        begin: KEY_OTHER + WS0 + '$'
      }
    ]
  };
}

module.exports = properties;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfcHJvcGVydGllcy5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsZ0JBQWdCLGtCQUFrQjtBQUNsQyxnQkFBZ0I7QUFDaEI7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxZQUFZLGlEQUFpRDtBQUM3RCxZQUFZO0FBQ1o7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL3Byb3BlcnRpZXMuanMiXSwic291cmNlc0NvbnRlbnQiOlsiLypcbkxhbmd1YWdlOiAucHJvcGVydGllc1xuQ29udHJpYnV0b3JzOiBWYWxlbnRpbiBBaXRrZW4gPHZhbGVudGluQG5hbGlzYmcuY29tPiwgRWdvciBSb2dvdiA8ZS5yb2dvdkBwb3N0Z3Jlc3Byby5ydT5cbldlYnNpdGU6IGh0dHBzOi8vZW4ud2lraXBlZGlhLm9yZy93aWtpLy5wcm9wZXJ0aWVzXG5DYXRlZ29yeTogY29tbW9uLCBjb25maWdcbiovXG5cbmZ1bmN0aW9uIHByb3BlcnRpZXMoaGxqcykge1xuXG4gIC8vIHdoaXRlc3BhY2VzOiBzcGFjZSwgdGFiLCBmb3JtZmVlZFxuICB2YXIgV1MwID0gJ1sgXFxcXHRcXFxcZl0qJztcbiAgdmFyIFdTMSA9ICdbIFxcXFx0XFxcXGZdKyc7XG4gIC8vIGRlbGltaXRlclxuICB2YXIgRVFVQUxfREVMSU0gPSBXUzArJ1s6PV0nK1dTMDtcbiAgdmFyIFdTX0RFTElNID0gV1MxO1xuICB2YXIgREVMSU0gPSAnKCcgKyBFUVVBTF9ERUxJTSArICd8JyArIFdTX0RFTElNICsgJyknO1xuICB2YXIgS0VZX0FMUEhBTlVNID0gJyhbXlxcXFxcXFxcXFxcXFc6PSBcXFxcdFxcXFxmXFxcXG5dfFxcXFxcXFxcLikrJztcbiAgdmFyIEtFWV9PVEhFUiA9ICcoW15cXFxcXFxcXDo9IFxcXFx0XFxcXGZcXFxcbl18XFxcXFxcXFwuKSsnO1xuXG4gIHZhciBERUxJTV9BTkRfVkFMVUUgPSB7XG4gICAgICAgICAgLy8gc2tpcCBERUxJTVxuICAgICAgICAgIGVuZDogREVMSU0sXG4gICAgICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgICAgIHN0YXJ0czoge1xuICAgICAgICAgICAgLy8gdmFsdWU6IGV2ZXJ5dGhpbmcgdW50aWwgZW5kIG9mIGxpbmUgKGFnYWluLCB0YWtpbmcgaW50byBhY2NvdW50IGJhY2tzbGFzaGVzKVxuICAgICAgICAgICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICAgICAgICAgIGVuZDogLyQvLFxuICAgICAgICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICAgICAgeyBiZWdpbjogJ1xcXFxcXFxcXFxcXFxcXFwnfSxcbiAgICAgICAgICAgICAgeyBiZWdpbjogJ1xcXFxcXFxcXFxcXG4nIH1cbiAgICAgICAgICAgIF1cbiAgICAgICAgICB9XG4gICAgICAgIH07XG5cbiAgcmV0dXJuIHtcbiAgICBuYW1lOiAnLnByb3BlcnRpZXMnLFxuICAgIGNhc2VfaW5zZW5zaXRpdmU6IHRydWUsXG4gICAgaWxsZWdhbDogL1xcUy8sXG4gICAgY29udGFpbnM6IFtcbiAgICAgIGhsanMuQ09NTUVOVCgnXlxcXFxzKlshI10nLCAnJCcpLFxuICAgICAgLy8ga2V5OiBldmVyeXRoaW5nIHVudGlsIHdoaXRlc3BhY2Ugb3IgPSBvciA6ICh0YWtpbmcgaW50byBhY2NvdW50IGJhY2tzbGFzaGVzKVxuICAgICAgLy8gY2FzZSBvZiBhIFwibm9ybWFsXCIga2V5XG4gICAgICB7XG4gICAgICAgIHJldHVybkJlZ2luOiB0cnVlLFxuICAgICAgICB2YXJpYW50czogW1xuICAgICAgICAgIHsgYmVnaW46IEtFWV9BTFBIQU5VTSArIEVRVUFMX0RFTElNLCByZWxldmFuY2U6IDEgfSxcbiAgICAgICAgICB7IGJlZ2luOiBLRVlfQUxQSEFOVU0gKyBXU19ERUxJTSwgcmVsZXZhbmNlOiAwIH1cbiAgICAgICAgXSxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBjbGFzc05hbWU6ICdhdHRyJyxcbiAgICAgICAgICAgIGJlZ2luOiBLRVlfQUxQSEFOVU0sXG4gICAgICAgICAgICBlbmRzUGFyZW50OiB0cnVlLFxuICAgICAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICAgICAgfVxuICAgICAgICBdLFxuICAgICAgICBzdGFydHM6IERFTElNX0FORF9WQUxVRVxuICAgICAgfSxcbiAgICAgIC8vIGNhc2Ugb2Yga2V5IGNvbnRhaW5pbmcgbm9uLWFscGhhbnVtZXJpYyBjaGFycyA9PiByZWxldmFuY2UgPSAwXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiBLRVlfT1RIRVIgKyBERUxJTSxcbiAgICAgICAgcmV0dXJuQmVnaW46IHRydWUsXG4gICAgICAgIHJlbGV2YW5jZTogMCxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBjbGFzc05hbWU6ICdtZXRhJyxcbiAgICAgICAgICAgIGJlZ2luOiBLRVlfT1RIRVIsXG4gICAgICAgICAgICBlbmRzUGFyZW50OiB0cnVlLFxuICAgICAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICAgICAgfVxuICAgICAgICBdLFxuICAgICAgICBzdGFydHM6IERFTElNX0FORF9WQUxVRVxuICAgICAgfSxcbiAgICAgIC8vIGNhc2Ugb2YgYW4gZW1wdHkga2V5XG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ2F0dHInLFxuICAgICAgICByZWxldmFuY2U6IDAsXG4gICAgICAgIGJlZ2luOiBLRVlfT1RIRVIgKyBXUzAgKyAnJCdcbiAgICAgIH1cbiAgICBdXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gcHJvcGVydGllcztcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==