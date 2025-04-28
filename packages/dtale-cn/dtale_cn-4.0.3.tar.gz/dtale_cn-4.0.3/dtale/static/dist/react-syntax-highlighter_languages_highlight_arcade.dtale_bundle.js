(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_arcade"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/arcade.js":
/*!*************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/arcade.js ***!
  \*************************************************************************************************/
/***/ ((module) => {

/*
 Language: ArcGIS Arcade
 Category: scripting
 Author: John Foster <jfoster@esri.com>
 Website: https://developers.arcgis.com/arcade/
 Description: ArcGIS Arcade is an expression language used in many Esri ArcGIS products such as Pro, Online, Server, Runtime, JavaScript, and Python
*/

/** @type LanguageFn */
function arcade(hljs) {
  const IDENT_RE = '[A-Za-z_][0-9A-Za-z_]*';
  const KEYWORDS = {
    keyword:
      'if for while var new function do return void else break',
    literal:
      'BackSlash DoubleQuote false ForwardSlash Infinity NaN NewLine null PI SingleQuote Tab TextFormatting true undefined',
    built_in:
      'Abs Acos Angle Attachments Area AreaGeodetic Asin Atan Atan2 Average Bearing Boolean Buffer BufferGeodetic ' +
      'Ceil Centroid Clip Console Constrain Contains Cos Count Crosses Cut Date DateAdd ' +
      'DateDiff Day Decode DefaultValue Dictionary Difference Disjoint Distance DistanceGeodetic Distinct ' +
      'DomainCode DomainName Equals Exp Extent Feature FeatureSet FeatureSetByAssociation FeatureSetById FeatureSetByPortalItem ' +
      'FeatureSetByRelationshipName FeatureSetByTitle FeatureSetByUrl Filter First Floor Geometry GroupBy Guid HasKey Hour IIf IndexOf ' +
      'Intersection Intersects IsEmpty IsNan IsSelfIntersecting Length LengthGeodetic Log Max Mean Millisecond Min Minute Month ' +
      'MultiPartToSinglePart Multipoint NextSequenceValue Now Number OrderBy Overlaps Point Polygon ' +
      'Polyline Portal Pow Random Relate Reverse RingIsClockWise Round Second SetGeometry Sin Sort Sqrt Stdev Sum ' +
      'SymmetricDifference Tan Text Timestamp Today ToLocal Top Touches ToUTC TrackCurrentTime ' +
      'TrackGeometryWindow TrackIndex TrackStartTime TrackWindow TypeOf Union UrlEncode Variance ' +
      'Weekday When Within Year '
  };
  const SYMBOL = {
    className: 'symbol',
    begin: '\\$[datastore|feature|layer|map|measure|sourcefeature|sourcelayer|targetfeature|targetlayer|value|view]+'
  };
  const NUMBER = {
    className: 'number',
    variants: [
      {
        begin: '\\b(0[bB][01]+)'
      },
      {
        begin: '\\b(0[oO][0-7]+)'
      },
      {
        begin: hljs.C_NUMBER_RE
      }
    ],
    relevance: 0
  };
  const SUBST = {
    className: 'subst',
    begin: '\\$\\{',
    end: '\\}',
    keywords: KEYWORDS,
    contains: [] // defined later
  };
  const TEMPLATE_STRING = {
    className: 'string',
    begin: '`',
    end: '`',
    contains: [
      hljs.BACKSLASH_ESCAPE,
      SUBST
    ]
  };
  SUBST.contains = [
    hljs.APOS_STRING_MODE,
    hljs.QUOTE_STRING_MODE,
    TEMPLATE_STRING,
    NUMBER,
    hljs.REGEXP_MODE
  ];
  const PARAMS_CONTAINS = SUBST.contains.concat([
    hljs.C_BLOCK_COMMENT_MODE,
    hljs.C_LINE_COMMENT_MODE
  ]);

  return {
    name: 'ArcGIS Arcade',
    keywords: KEYWORDS,
    contains: [
      hljs.APOS_STRING_MODE,
      hljs.QUOTE_STRING_MODE,
      TEMPLATE_STRING,
      hljs.C_LINE_COMMENT_MODE,
      hljs.C_BLOCK_COMMENT_MODE,
      SYMBOL,
      NUMBER,
      { // object attr container
        begin: /[{,]\s*/,
        relevance: 0,
        contains: [{
          begin: IDENT_RE + '\\s*:',
          returnBegin: true,
          relevance: 0,
          contains: [{
            className: 'attr',
            begin: IDENT_RE,
            relevance: 0
          }]
        }]
      },
      { // "value" container
        begin: '(' + hljs.RE_STARTERS_RE + '|\\b(return)\\b)\\s*',
        keywords: 'return',
        contains: [
          hljs.C_LINE_COMMENT_MODE,
          hljs.C_BLOCK_COMMENT_MODE,
          hljs.REGEXP_MODE,
          {
            className: 'function',
            begin: '(\\(.*?\\)|' + IDENT_RE + ')\\s*=>',
            returnBegin: true,
            end: '\\s*=>',
            contains: [{
              className: 'params',
              variants: [
                {
                  begin: IDENT_RE
                },
                {
                  begin: /\(\s*\)/
                },
                {
                  begin: /\(/,
                  end: /\)/,
                  excludeBegin: true,
                  excludeEnd: true,
                  keywords: KEYWORDS,
                  contains: PARAMS_CONTAINS
                }
              ]
            }]
          }
        ],
        relevance: 0
      },
      {
        className: 'function',
        beginKeywords: 'function',
        end: /\{/,
        excludeEnd: true,
        contains: [
          hljs.inherit(hljs.TITLE_MODE, {
            begin: IDENT_RE
          }),
          {
            className: 'params',
            begin: /\(/,
            end: /\)/,
            excludeBegin: true,
            excludeEnd: true,
            contains: PARAMS_CONTAINS
          }
        ],
        illegal: /\[|%/
      },
      {
        begin: /\$[(.]/
      }
    ],
    illegal: /#(?!!)/
  };
}

module.exports = arcade;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfYXJjYWRlLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxrQkFBa0I7QUFDbEIsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFFBQVE7QUFDUixrQkFBa0I7QUFDbEI7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsV0FBVztBQUNYLFNBQVM7QUFDVCxPQUFPO0FBQ1AsUUFBUTtBQUNSO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsaUJBQWlCO0FBQ2pCO0FBQ0E7QUFDQSxpQkFBaUI7QUFDakI7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsYUFBYTtBQUNiO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSxnQkFBZ0I7QUFDaEI7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL2FyY2FkZS5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKlxuIExhbmd1YWdlOiBBcmNHSVMgQXJjYWRlXG4gQ2F0ZWdvcnk6IHNjcmlwdGluZ1xuIEF1dGhvcjogSm9obiBGb3N0ZXIgPGpmb3N0ZXJAZXNyaS5jb20+XG4gV2Vic2l0ZTogaHR0cHM6Ly9kZXZlbG9wZXJzLmFyY2dpcy5jb20vYXJjYWRlL1xuIERlc2NyaXB0aW9uOiBBcmNHSVMgQXJjYWRlIGlzIGFuIGV4cHJlc3Npb24gbGFuZ3VhZ2UgdXNlZCBpbiBtYW55IEVzcmkgQXJjR0lTIHByb2R1Y3RzIHN1Y2ggYXMgUHJvLCBPbmxpbmUsIFNlcnZlciwgUnVudGltZSwgSmF2YVNjcmlwdCwgYW5kIFB5dGhvblxuKi9cblxuLyoqIEB0eXBlIExhbmd1YWdlRm4gKi9cbmZ1bmN0aW9uIGFyY2FkZShobGpzKSB7XG4gIGNvbnN0IElERU5UX1JFID0gJ1tBLVphLXpfXVswLTlBLVphLXpfXSonO1xuICBjb25zdCBLRVlXT1JEUyA9IHtcbiAgICBrZXl3b3JkOlxuICAgICAgJ2lmIGZvciB3aGlsZSB2YXIgbmV3IGZ1bmN0aW9uIGRvIHJldHVybiB2b2lkIGVsc2UgYnJlYWsnLFxuICAgIGxpdGVyYWw6XG4gICAgICAnQmFja1NsYXNoIERvdWJsZVF1b3RlIGZhbHNlIEZvcndhcmRTbGFzaCBJbmZpbml0eSBOYU4gTmV3TGluZSBudWxsIFBJIFNpbmdsZVF1b3RlIFRhYiBUZXh0Rm9ybWF0dGluZyB0cnVlIHVuZGVmaW5lZCcsXG4gICAgYnVpbHRfaW46XG4gICAgICAnQWJzIEFjb3MgQW5nbGUgQXR0YWNobWVudHMgQXJlYSBBcmVhR2VvZGV0aWMgQXNpbiBBdGFuIEF0YW4yIEF2ZXJhZ2UgQmVhcmluZyBCb29sZWFuIEJ1ZmZlciBCdWZmZXJHZW9kZXRpYyAnICtcbiAgICAgICdDZWlsIENlbnRyb2lkIENsaXAgQ29uc29sZSBDb25zdHJhaW4gQ29udGFpbnMgQ29zIENvdW50IENyb3NzZXMgQ3V0IERhdGUgRGF0ZUFkZCAnICtcbiAgICAgICdEYXRlRGlmZiBEYXkgRGVjb2RlIERlZmF1bHRWYWx1ZSBEaWN0aW9uYXJ5IERpZmZlcmVuY2UgRGlzam9pbnQgRGlzdGFuY2UgRGlzdGFuY2VHZW9kZXRpYyBEaXN0aW5jdCAnICtcbiAgICAgICdEb21haW5Db2RlIERvbWFpbk5hbWUgRXF1YWxzIEV4cCBFeHRlbnQgRmVhdHVyZSBGZWF0dXJlU2V0IEZlYXR1cmVTZXRCeUFzc29jaWF0aW9uIEZlYXR1cmVTZXRCeUlkIEZlYXR1cmVTZXRCeVBvcnRhbEl0ZW0gJyArXG4gICAgICAnRmVhdHVyZVNldEJ5UmVsYXRpb25zaGlwTmFtZSBGZWF0dXJlU2V0QnlUaXRsZSBGZWF0dXJlU2V0QnlVcmwgRmlsdGVyIEZpcnN0IEZsb29yIEdlb21ldHJ5IEdyb3VwQnkgR3VpZCBIYXNLZXkgSG91ciBJSWYgSW5kZXhPZiAnICtcbiAgICAgICdJbnRlcnNlY3Rpb24gSW50ZXJzZWN0cyBJc0VtcHR5IElzTmFuIElzU2VsZkludGVyc2VjdGluZyBMZW5ndGggTGVuZ3RoR2VvZGV0aWMgTG9nIE1heCBNZWFuIE1pbGxpc2Vjb25kIE1pbiBNaW51dGUgTW9udGggJyArXG4gICAgICAnTXVsdGlQYXJ0VG9TaW5nbGVQYXJ0IE11bHRpcG9pbnQgTmV4dFNlcXVlbmNlVmFsdWUgTm93IE51bWJlciBPcmRlckJ5IE92ZXJsYXBzIFBvaW50IFBvbHlnb24gJyArXG4gICAgICAnUG9seWxpbmUgUG9ydGFsIFBvdyBSYW5kb20gUmVsYXRlIFJldmVyc2UgUmluZ0lzQ2xvY2tXaXNlIFJvdW5kIFNlY29uZCBTZXRHZW9tZXRyeSBTaW4gU29ydCBTcXJ0IFN0ZGV2IFN1bSAnICtcbiAgICAgICdTeW1tZXRyaWNEaWZmZXJlbmNlIFRhbiBUZXh0IFRpbWVzdGFtcCBUb2RheSBUb0xvY2FsIFRvcCBUb3VjaGVzIFRvVVRDIFRyYWNrQ3VycmVudFRpbWUgJyArXG4gICAgICAnVHJhY2tHZW9tZXRyeVdpbmRvdyBUcmFja0luZGV4IFRyYWNrU3RhcnRUaW1lIFRyYWNrV2luZG93IFR5cGVPZiBVbmlvbiBVcmxFbmNvZGUgVmFyaWFuY2UgJyArXG4gICAgICAnV2Vla2RheSBXaGVuIFdpdGhpbiBZZWFyICdcbiAgfTtcbiAgY29uc3QgU1lNQk9MID0ge1xuICAgIGNsYXNzTmFtZTogJ3N5bWJvbCcsXG4gICAgYmVnaW46ICdcXFxcJFtkYXRhc3RvcmV8ZmVhdHVyZXxsYXllcnxtYXB8bWVhc3VyZXxzb3VyY2VmZWF0dXJlfHNvdXJjZWxheWVyfHRhcmdldGZlYXR1cmV8dGFyZ2V0bGF5ZXJ8dmFsdWV8dmlld10rJ1xuICB9O1xuICBjb25zdCBOVU1CRVIgPSB7XG4gICAgY2xhc3NOYW1lOiAnbnVtYmVyJyxcbiAgICB2YXJpYW50czogW1xuICAgICAge1xuICAgICAgICBiZWdpbjogJ1xcXFxiKDBbYkJdWzAxXSspJ1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46ICdcXFxcYigwW29PXVswLTddKyknXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogaGxqcy5DX05VTUJFUl9SRVxuICAgICAgfVxuICAgIF0sXG4gICAgcmVsZXZhbmNlOiAwXG4gIH07XG4gIGNvbnN0IFNVQlNUID0ge1xuICAgIGNsYXNzTmFtZTogJ3N1YnN0JyxcbiAgICBiZWdpbjogJ1xcXFwkXFxcXHsnLFxuICAgIGVuZDogJ1xcXFx9JyxcbiAgICBrZXl3b3JkczogS0VZV09SRFMsXG4gICAgY29udGFpbnM6IFtdIC8vIGRlZmluZWQgbGF0ZXJcbiAgfTtcbiAgY29uc3QgVEVNUExBVEVfU1RSSU5HID0ge1xuICAgIGNsYXNzTmFtZTogJ3N0cmluZycsXG4gICAgYmVnaW46ICdgJyxcbiAgICBlbmQ6ICdgJyxcbiAgICBjb250YWluczogW1xuICAgICAgaGxqcy5CQUNLU0xBU0hfRVNDQVBFLFxuICAgICAgU1VCU1RcbiAgICBdXG4gIH07XG4gIFNVQlNULmNvbnRhaW5zID0gW1xuICAgIGhsanMuQVBPU19TVFJJTkdfTU9ERSxcbiAgICBobGpzLlFVT1RFX1NUUklOR19NT0RFLFxuICAgIFRFTVBMQVRFX1NUUklORyxcbiAgICBOVU1CRVIsXG4gICAgaGxqcy5SRUdFWFBfTU9ERVxuICBdO1xuICBjb25zdCBQQVJBTVNfQ09OVEFJTlMgPSBTVUJTVC5jb250YWlucy5jb25jYXQoW1xuICAgIGhsanMuQ19CTE9DS19DT01NRU5UX01PREUsXG4gICAgaGxqcy5DX0xJTkVfQ09NTUVOVF9NT0RFXG4gIF0pO1xuXG4gIHJldHVybiB7XG4gICAgbmFtZTogJ0FyY0dJUyBBcmNhZGUnLFxuICAgIGtleXdvcmRzOiBLRVlXT1JEUyxcbiAgICBjb250YWluczogW1xuICAgICAgaGxqcy5BUE9TX1NUUklOR19NT0RFLFxuICAgICAgaGxqcy5RVU9URV9TVFJJTkdfTU9ERSxcbiAgICAgIFRFTVBMQVRFX1NUUklORyxcbiAgICAgIGhsanMuQ19MSU5FX0NPTU1FTlRfTU9ERSxcbiAgICAgIGhsanMuQ19CTE9DS19DT01NRU5UX01PREUsXG4gICAgICBTWU1CT0wsXG4gICAgICBOVU1CRVIsXG4gICAgICB7IC8vIG9iamVjdCBhdHRyIGNvbnRhaW5lclxuICAgICAgICBiZWdpbjogL1t7LF1cXHMqLyxcbiAgICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgICBjb250YWluczogW3tcbiAgICAgICAgICBiZWdpbjogSURFTlRfUkUgKyAnXFxcXHMqOicsXG4gICAgICAgICAgcmV0dXJuQmVnaW46IHRydWUsXG4gICAgICAgICAgcmVsZXZhbmNlOiAwLFxuICAgICAgICAgIGNvbnRhaW5zOiBbe1xuICAgICAgICAgICAgY2xhc3NOYW1lOiAnYXR0cicsXG4gICAgICAgICAgICBiZWdpbjogSURFTlRfUkUsXG4gICAgICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgICAgICB9XVxuICAgICAgICB9XVxuICAgICAgfSxcbiAgICAgIHsgLy8gXCJ2YWx1ZVwiIGNvbnRhaW5lclxuICAgICAgICBiZWdpbjogJygnICsgaGxqcy5SRV9TVEFSVEVSU19SRSArICd8XFxcXGIocmV0dXJuKVxcXFxiKVxcXFxzKicsXG4gICAgICAgIGtleXdvcmRzOiAncmV0dXJuJyxcbiAgICAgICAgY29udGFpbnM6IFtcbiAgICAgICAgICBobGpzLkNfTElORV9DT01NRU5UX01PREUsXG4gICAgICAgICAgaGxqcy5DX0JMT0NLX0NPTU1FTlRfTU9ERSxcbiAgICAgICAgICBobGpzLlJFR0VYUF9NT0RFLFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGNsYXNzTmFtZTogJ2Z1bmN0aW9uJyxcbiAgICAgICAgICAgIGJlZ2luOiAnKFxcXFwoLio/XFxcXCl8JyArIElERU5UX1JFICsgJylcXFxccyo9PicsXG4gICAgICAgICAgICByZXR1cm5CZWdpbjogdHJ1ZSxcbiAgICAgICAgICAgIGVuZDogJ1xcXFxzKj0+JyxcbiAgICAgICAgICAgIGNvbnRhaW5zOiBbe1xuICAgICAgICAgICAgICBjbGFzc05hbWU6ICdwYXJhbXMnLFxuICAgICAgICAgICAgICB2YXJpYW50czogW1xuICAgICAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgICAgIGJlZ2luOiBJREVOVF9SRVxuICAgICAgICAgICAgICAgIH0sXG4gICAgICAgICAgICAgICAge1xuICAgICAgICAgICAgICAgICAgYmVnaW46IC9cXChcXHMqXFwpL1xuICAgICAgICAgICAgICAgIH0sXG4gICAgICAgICAgICAgICAge1xuICAgICAgICAgICAgICAgICAgYmVnaW46IC9cXCgvLFxuICAgICAgICAgICAgICAgICAgZW5kOiAvXFwpLyxcbiAgICAgICAgICAgICAgICAgIGV4Y2x1ZGVCZWdpbjogdHJ1ZSxcbiAgICAgICAgICAgICAgICAgIGV4Y2x1ZGVFbmQ6IHRydWUsXG4gICAgICAgICAgICAgICAgICBrZXl3b3JkczogS0VZV09SRFMsXG4gICAgICAgICAgICAgICAgICBjb250YWluczogUEFSQU1TX0NPTlRBSU5TXG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICBdXG4gICAgICAgICAgICB9XVxuICAgICAgICAgIH1cbiAgICAgICAgXSxcbiAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdmdW5jdGlvbicsXG4gICAgICAgIGJlZ2luS2V5d29yZHM6ICdmdW5jdGlvbicsXG4gICAgICAgIGVuZDogL1xcey8sXG4gICAgICAgIGV4Y2x1ZGVFbmQ6IHRydWUsXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgaGxqcy5pbmhlcml0KGhsanMuVElUTEVfTU9ERSwge1xuICAgICAgICAgICAgYmVnaW46IElERU5UX1JFXG4gICAgICAgICAgfSksXG4gICAgICAgICAge1xuICAgICAgICAgICAgY2xhc3NOYW1lOiAncGFyYW1zJyxcbiAgICAgICAgICAgIGJlZ2luOiAvXFwoLyxcbiAgICAgICAgICAgIGVuZDogL1xcKS8sXG4gICAgICAgICAgICBleGNsdWRlQmVnaW46IHRydWUsXG4gICAgICAgICAgICBleGNsdWRlRW5kOiB0cnVlLFxuICAgICAgICAgICAgY29udGFpbnM6IFBBUkFNU19DT05UQUlOU1xuICAgICAgICAgIH1cbiAgICAgICAgXSxcbiAgICAgICAgaWxsZWdhbDogL1xcW3wlL1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgYmVnaW46IC9cXCRbKC5dL1xuICAgICAgfVxuICAgIF0sXG4gICAgaWxsZWdhbDogLyMoPyEhKS9cbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBhcmNhZGU7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=