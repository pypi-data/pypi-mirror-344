(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_oxygene"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/oxygene.js":
/*!**************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/oxygene.js ***!
  \**************************************************************************************************/
/***/ ((module) => {

/*
Language: Oxygene
Author: Carlo Kok <ck@remobjects.com>
Description: Oxygene is built on the foundation of Object Pascal, revamped and extended to be a modern language for the twenty-first century.
Website: https://www.elementscompiler.com/elements/default.aspx
*/

function oxygene(hljs) {
  const OXYGENE_KEYWORDS = {
    $pattern: /\.?\w+/,
    keyword:
      'abstract add and array as asc aspect assembly async begin break block by case class concat const copy constructor continue ' +
      'create default delegate desc distinct div do downto dynamic each else empty end ensure enum equals event except exit extension external false ' +
      'final finalize finalizer finally flags for forward from function future global group has if implementation implements implies in index inherited ' +
      'inline interface into invariants is iterator join locked locking loop matching method mod module namespace nested new nil not notify nullable of ' +
      'old on operator or order out override parallel params partial pinned private procedure property protected public queryable raise read readonly ' +
      'record reintroduce remove repeat require result reverse sealed select self sequence set shl shr skip static step soft take then to true try tuple ' +
      'type union unit unsafe until uses using var virtual raises volatile where while with write xor yield await mapped deprecated stdcall cdecl pascal ' +
      'register safecall overload library platform reference packed strict published autoreleasepool selector strong weak unretained'
  };
  const CURLY_COMMENT = hljs.COMMENT(
    /\{/,
    /\}/,
    {
      relevance: 0
    }
  );
  const PAREN_COMMENT = hljs.COMMENT(
    '\\(\\*',
    '\\*\\)',
    {
      relevance: 10
    }
  );
  const STRING = {
    className: 'string',
    begin: '\'',
    end: '\'',
    contains: [
      {
        begin: '\'\''
      }
    ]
  };
  const CHAR_STRING = {
    className: 'string',
    begin: '(#\\d+)+'
  };
  const FUNCTION = {
    className: 'function',
    beginKeywords: 'function constructor destructor procedure method',
    end: '[:;]',
    keywords: 'function constructor|10 destructor|10 procedure|10 method|10',
    contains: [
      hljs.TITLE_MODE,
      {
        className: 'params',
        begin: '\\(',
        end: '\\)',
        keywords: OXYGENE_KEYWORDS,
        contains: [
          STRING,
          CHAR_STRING
        ]
      },
      CURLY_COMMENT,
      PAREN_COMMENT
    ]
  };
  return {
    name: 'Oxygene',
    case_insensitive: true,
    keywords: OXYGENE_KEYWORDS,
    illegal: '("|\\$[G-Zg-z]|\\/\\*|</|=>|->)',
    contains: [
      CURLY_COMMENT,
      PAREN_COMMENT,
      hljs.C_LINE_COMMENT_MODE,
      STRING,
      CHAR_STRING,
      hljs.NUMBER_MODE,
      FUNCTION,
      {
        className: 'class',
        begin: '=\\bclass\\b',
        end: 'end;',
        keywords: OXYGENE_KEYWORDS,
        contains: [
          STRING,
          CHAR_STRING,
          CURLY_COMMENT,
          PAREN_COMMENT,
          hljs.C_LINE_COMMENT_MODE,
          FUNCTION
        ]
      }
    ]
  };
}

module.exports = oxygene;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfb3h5Z2VuZS5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUCxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxhQUFhO0FBQ2I7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxrQkFBa0I7QUFDbEI7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL294eWdlbmUuanMiXSwic291cmNlc0NvbnRlbnQiOlsiLypcbkxhbmd1YWdlOiBPeHlnZW5lXG5BdXRob3I6IENhcmxvIEtvayA8Y2tAcmVtb2JqZWN0cy5jb20+XG5EZXNjcmlwdGlvbjogT3h5Z2VuZSBpcyBidWlsdCBvbiB0aGUgZm91bmRhdGlvbiBvZiBPYmplY3QgUGFzY2FsLCByZXZhbXBlZCBhbmQgZXh0ZW5kZWQgdG8gYmUgYSBtb2Rlcm4gbGFuZ3VhZ2UgZm9yIHRoZSB0d2VudHktZmlyc3QgY2VudHVyeS5cbldlYnNpdGU6IGh0dHBzOi8vd3d3LmVsZW1lbnRzY29tcGlsZXIuY29tL2VsZW1lbnRzL2RlZmF1bHQuYXNweFxuKi9cblxuZnVuY3Rpb24gb3h5Z2VuZShobGpzKSB7XG4gIGNvbnN0IE9YWUdFTkVfS0VZV09SRFMgPSB7XG4gICAgJHBhdHRlcm46IC9cXC4/XFx3Ky8sXG4gICAga2V5d29yZDpcbiAgICAgICdhYnN0cmFjdCBhZGQgYW5kIGFycmF5IGFzIGFzYyBhc3BlY3QgYXNzZW1ibHkgYXN5bmMgYmVnaW4gYnJlYWsgYmxvY2sgYnkgY2FzZSBjbGFzcyBjb25jYXQgY29uc3QgY29weSBjb25zdHJ1Y3RvciBjb250aW51ZSAnICtcbiAgICAgICdjcmVhdGUgZGVmYXVsdCBkZWxlZ2F0ZSBkZXNjIGRpc3RpbmN0IGRpdiBkbyBkb3dudG8gZHluYW1pYyBlYWNoIGVsc2UgZW1wdHkgZW5kIGVuc3VyZSBlbnVtIGVxdWFscyBldmVudCBleGNlcHQgZXhpdCBleHRlbnNpb24gZXh0ZXJuYWwgZmFsc2UgJyArXG4gICAgICAnZmluYWwgZmluYWxpemUgZmluYWxpemVyIGZpbmFsbHkgZmxhZ3MgZm9yIGZvcndhcmQgZnJvbSBmdW5jdGlvbiBmdXR1cmUgZ2xvYmFsIGdyb3VwIGhhcyBpZiBpbXBsZW1lbnRhdGlvbiBpbXBsZW1lbnRzIGltcGxpZXMgaW4gaW5kZXggaW5oZXJpdGVkICcgK1xuICAgICAgJ2lubGluZSBpbnRlcmZhY2UgaW50byBpbnZhcmlhbnRzIGlzIGl0ZXJhdG9yIGpvaW4gbG9ja2VkIGxvY2tpbmcgbG9vcCBtYXRjaGluZyBtZXRob2QgbW9kIG1vZHVsZSBuYW1lc3BhY2UgbmVzdGVkIG5ldyBuaWwgbm90IG5vdGlmeSBudWxsYWJsZSBvZiAnICtcbiAgICAgICdvbGQgb24gb3BlcmF0b3Igb3Igb3JkZXIgb3V0IG92ZXJyaWRlIHBhcmFsbGVsIHBhcmFtcyBwYXJ0aWFsIHBpbm5lZCBwcml2YXRlIHByb2NlZHVyZSBwcm9wZXJ0eSBwcm90ZWN0ZWQgcHVibGljIHF1ZXJ5YWJsZSByYWlzZSByZWFkIHJlYWRvbmx5ICcgK1xuICAgICAgJ3JlY29yZCByZWludHJvZHVjZSByZW1vdmUgcmVwZWF0IHJlcXVpcmUgcmVzdWx0IHJldmVyc2Ugc2VhbGVkIHNlbGVjdCBzZWxmIHNlcXVlbmNlIHNldCBzaGwgc2hyIHNraXAgc3RhdGljIHN0ZXAgc29mdCB0YWtlIHRoZW4gdG8gdHJ1ZSB0cnkgdHVwbGUgJyArXG4gICAgICAndHlwZSB1bmlvbiB1bml0IHVuc2FmZSB1bnRpbCB1c2VzIHVzaW5nIHZhciB2aXJ0dWFsIHJhaXNlcyB2b2xhdGlsZSB3aGVyZSB3aGlsZSB3aXRoIHdyaXRlIHhvciB5aWVsZCBhd2FpdCBtYXBwZWQgZGVwcmVjYXRlZCBzdGRjYWxsIGNkZWNsIHBhc2NhbCAnICtcbiAgICAgICdyZWdpc3RlciBzYWZlY2FsbCBvdmVybG9hZCBsaWJyYXJ5IHBsYXRmb3JtIHJlZmVyZW5jZSBwYWNrZWQgc3RyaWN0IHB1Ymxpc2hlZCBhdXRvcmVsZWFzZXBvb2wgc2VsZWN0b3Igc3Ryb25nIHdlYWsgdW5yZXRhaW5lZCdcbiAgfTtcbiAgY29uc3QgQ1VSTFlfQ09NTUVOVCA9IGhsanMuQ09NTUVOVChcbiAgICAvXFx7LyxcbiAgICAvXFx9LyxcbiAgICB7XG4gICAgICByZWxldmFuY2U6IDBcbiAgICB9XG4gICk7XG4gIGNvbnN0IFBBUkVOX0NPTU1FTlQgPSBobGpzLkNPTU1FTlQoXG4gICAgJ1xcXFwoXFxcXConLFxuICAgICdcXFxcKlxcXFwpJyxcbiAgICB7XG4gICAgICByZWxldmFuY2U6IDEwXG4gICAgfVxuICApO1xuICBjb25zdCBTVFJJTkcgPSB7XG4gICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICBiZWdpbjogJ1xcJycsXG4gICAgZW5kOiAnXFwnJyxcbiAgICBjb250YWluczogW1xuICAgICAge1xuICAgICAgICBiZWdpbjogJ1xcJ1xcJydcbiAgICAgIH1cbiAgICBdXG4gIH07XG4gIGNvbnN0IENIQVJfU1RSSU5HID0ge1xuICAgIGNsYXNzTmFtZTogJ3N0cmluZycsXG4gICAgYmVnaW46ICcoI1xcXFxkKykrJ1xuICB9O1xuICBjb25zdCBGVU5DVElPTiA9IHtcbiAgICBjbGFzc05hbWU6ICdmdW5jdGlvbicsXG4gICAgYmVnaW5LZXl3b3JkczogJ2Z1bmN0aW9uIGNvbnN0cnVjdG9yIGRlc3RydWN0b3IgcHJvY2VkdXJlIG1ldGhvZCcsXG4gICAgZW5kOiAnWzo7XScsXG4gICAga2V5d29yZHM6ICdmdW5jdGlvbiBjb25zdHJ1Y3RvcnwxMCBkZXN0cnVjdG9yfDEwIHByb2NlZHVyZXwxMCBtZXRob2R8MTAnLFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICBobGpzLlRJVExFX01PREUsXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3BhcmFtcycsXG4gICAgICAgIGJlZ2luOiAnXFxcXCgnLFxuICAgICAgICBlbmQ6ICdcXFxcKScsXG4gICAgICAgIGtleXdvcmRzOiBPWFlHRU5FX0tFWVdPUkRTLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIFNUUklORyxcbiAgICAgICAgICBDSEFSX1NUUklOR1xuICAgICAgICBdXG4gICAgICB9LFxuICAgICAgQ1VSTFlfQ09NTUVOVCxcbiAgICAgIFBBUkVOX0NPTU1FTlRcbiAgICBdXG4gIH07XG4gIHJldHVybiB7XG4gICAgbmFtZTogJ094eWdlbmUnLFxuICAgIGNhc2VfaW5zZW5zaXRpdmU6IHRydWUsXG4gICAga2V5d29yZHM6IE9YWUdFTkVfS0VZV09SRFMsXG4gICAgaWxsZWdhbDogJyhcInxcXFxcJFtHLVpnLXpdfFxcXFwvXFxcXCp8PC98PT58LT4pJyxcbiAgICBjb250YWluczogW1xuICAgICAgQ1VSTFlfQ09NTUVOVCxcbiAgICAgIFBBUkVOX0NPTU1FTlQsXG4gICAgICBobGpzLkNfTElORV9DT01NRU5UX01PREUsXG4gICAgICBTVFJJTkcsXG4gICAgICBDSEFSX1NUUklORyxcbiAgICAgIGhsanMuTlVNQkVSX01PREUsXG4gICAgICBGVU5DVElPTixcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnY2xhc3MnLFxuICAgICAgICBiZWdpbjogJz1cXFxcYmNsYXNzXFxcXGInLFxuICAgICAgICBlbmQ6ICdlbmQ7JyxcbiAgICAgICAga2V5d29yZHM6IE9YWUdFTkVfS0VZV09SRFMsXG4gICAgICAgIGNvbnRhaW5zOiBbXG4gICAgICAgICAgU1RSSU5HLFxuICAgICAgICAgIENIQVJfU1RSSU5HLFxuICAgICAgICAgIENVUkxZX0NPTU1FTlQsXG4gICAgICAgICAgUEFSRU5fQ09NTUVOVCxcbiAgICAgICAgICBobGpzLkNfTElORV9DT01NRU5UX01PREUsXG4gICAgICAgICAgRlVOQ1RJT05cbiAgICAgICAgXVxuICAgICAgfVxuICAgIF1cbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBveHlnZW5lO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9