(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_lua"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/lua.js":
/*!**********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/lua.js ***!
  \**********************************************************************************************/
/***/ ((module) => {

/*
Language: Lua
Description: Lua is a powerful, efficient, lightweight, embeddable scripting language.
Author: Andrew Fedorov <dmmdrs@mail.ru>
Category: common, scripting
Website: https://www.lua.org
*/

function lua(hljs) {
  const OPENING_LONG_BRACKET = '\\[=*\\[';
  const CLOSING_LONG_BRACKET = '\\]=*\\]';
  const LONG_BRACKETS = {
    begin: OPENING_LONG_BRACKET,
    end: CLOSING_LONG_BRACKET,
    contains: ['self']
  };
  const COMMENTS = [
    hljs.COMMENT('--(?!' + OPENING_LONG_BRACKET + ')', '$'),
    hljs.COMMENT(
      '--' + OPENING_LONG_BRACKET,
      CLOSING_LONG_BRACKET,
      {
        contains: [LONG_BRACKETS],
        relevance: 10
      }
    )
  ];
  return {
    name: 'Lua',
    keywords: {
      $pattern: hljs.UNDERSCORE_IDENT_RE,
      literal: "true false nil",
      keyword: "and break do else elseif end for goto if in local not or repeat return then until while",
      built_in:
        // Metatags and globals:
        '_G _ENV _VERSION __index __newindex __mode __call __metatable __tostring __len ' +
        '__gc __add __sub __mul __div __mod __pow __concat __unm __eq __lt __le assert ' +
        // Standard methods and properties:
        'collectgarbage dofile error getfenv getmetatable ipairs load loadfile loadstring ' +
        'module next pairs pcall print rawequal rawget rawset require select setfenv ' +
        'setmetatable tonumber tostring type unpack xpcall arg self ' +
        // Library methods and properties (one line per library):
        'coroutine resume yield status wrap create running debug getupvalue ' +
        'debug sethook getmetatable gethook setmetatable setlocal traceback setfenv getinfo setupvalue getlocal getregistry getfenv ' +
        'io lines write close flush open output type read stderr stdin input stdout popen tmpfile ' +
        'math log max acos huge ldexp pi cos tanh pow deg tan cosh sinh random randomseed frexp ceil floor rad abs sqrt modf asin min mod fmod log10 atan2 exp sin atan ' +
        'os exit setlocale date getenv difftime remove time clock tmpname rename execute package preload loadlib loaded loaders cpath config path seeall ' +
        'string sub upper len gfind rep find match char dump gmatch reverse byte format gsub lower ' +
        'table setn insert getn foreachi maxn foreach concat sort remove'
    },
    contains: COMMENTS.concat([
      {
        className: 'function',
        beginKeywords: 'function',
        end: '\\)',
        contains: [
          hljs.inherit(hljs.TITLE_MODE, {
            begin: '([_a-zA-Z]\\w*\\.)*([_a-zA-Z]\\w*:)?[_a-zA-Z]\\w*'
          }),
          {
            className: 'params',
            begin: '\\(',
            endsWithParent: true,
            contains: COMMENTS
          }
        ].concat(COMMENTS)
      },
      hljs.C_NUMBER_MODE,
      hljs.APOS_STRING_MODE,
      hljs.QUOTE_STRING_MODE,
      {
        className: 'string',
        begin: OPENING_LONG_BRACKET,
        end: CLOSING_LONG_BRACKET,
        contains: [LONG_BRACKETS],
        relevance: 5
      }
    ])
  };
}

module.exports = lua;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfbHVhLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLFdBQVc7QUFDWDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvbHVhLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogTHVhXG5EZXNjcmlwdGlvbjogTHVhIGlzIGEgcG93ZXJmdWwsIGVmZmljaWVudCwgbGlnaHR3ZWlnaHQsIGVtYmVkZGFibGUgc2NyaXB0aW5nIGxhbmd1YWdlLlxuQXV0aG9yOiBBbmRyZXcgRmVkb3JvdiA8ZG1tZHJzQG1haWwucnU+XG5DYXRlZ29yeTogY29tbW9uLCBzY3JpcHRpbmdcbldlYnNpdGU6IGh0dHBzOi8vd3d3Lmx1YS5vcmdcbiovXG5cbmZ1bmN0aW9uIGx1YShobGpzKSB7XG4gIGNvbnN0IE9QRU5JTkdfTE9OR19CUkFDS0VUID0gJ1xcXFxbPSpcXFxcWyc7XG4gIGNvbnN0IENMT1NJTkdfTE9OR19CUkFDS0VUID0gJ1xcXFxdPSpcXFxcXSc7XG4gIGNvbnN0IExPTkdfQlJBQ0tFVFMgPSB7XG4gICAgYmVnaW46IE9QRU5JTkdfTE9OR19CUkFDS0VULFxuICAgIGVuZDogQ0xPU0lOR19MT05HX0JSQUNLRVQsXG4gICAgY29udGFpbnM6IFsnc2VsZiddXG4gIH07XG4gIGNvbnN0IENPTU1FTlRTID0gW1xuICAgIGhsanMuQ09NTUVOVCgnLS0oPyEnICsgT1BFTklOR19MT05HX0JSQUNLRVQgKyAnKScsICckJyksXG4gICAgaGxqcy5DT01NRU5UKFxuICAgICAgJy0tJyArIE9QRU5JTkdfTE9OR19CUkFDS0VULFxuICAgICAgQ0xPU0lOR19MT05HX0JSQUNLRVQsXG4gICAgICB7XG4gICAgICAgIGNvbnRhaW5zOiBbTE9OR19CUkFDS0VUU10sXG4gICAgICAgIHJlbGV2YW5jZTogMTBcbiAgICAgIH1cbiAgICApXG4gIF07XG4gIHJldHVybiB7XG4gICAgbmFtZTogJ0x1YScsXG4gICAga2V5d29yZHM6IHtcbiAgICAgICRwYXR0ZXJuOiBobGpzLlVOREVSU0NPUkVfSURFTlRfUkUsXG4gICAgICBsaXRlcmFsOiBcInRydWUgZmFsc2UgbmlsXCIsXG4gICAgICBrZXl3b3JkOiBcImFuZCBicmVhayBkbyBlbHNlIGVsc2VpZiBlbmQgZm9yIGdvdG8gaWYgaW4gbG9jYWwgbm90IG9yIHJlcGVhdCByZXR1cm4gdGhlbiB1bnRpbCB3aGlsZVwiLFxuICAgICAgYnVpbHRfaW46XG4gICAgICAgIC8vIE1ldGF0YWdzIGFuZCBnbG9iYWxzOlxuICAgICAgICAnX0cgX0VOViBfVkVSU0lPTiBfX2luZGV4IF9fbmV3aW5kZXggX19tb2RlIF9fY2FsbCBfX21ldGF0YWJsZSBfX3Rvc3RyaW5nIF9fbGVuICcgK1xuICAgICAgICAnX19nYyBfX2FkZCBfX3N1YiBfX211bCBfX2RpdiBfX21vZCBfX3BvdyBfX2NvbmNhdCBfX3VubSBfX2VxIF9fbHQgX19sZSBhc3NlcnQgJyArXG4gICAgICAgIC8vIFN0YW5kYXJkIG1ldGhvZHMgYW5kIHByb3BlcnRpZXM6XG4gICAgICAgICdjb2xsZWN0Z2FyYmFnZSBkb2ZpbGUgZXJyb3IgZ2V0ZmVudiBnZXRtZXRhdGFibGUgaXBhaXJzIGxvYWQgbG9hZGZpbGUgbG9hZHN0cmluZyAnICtcbiAgICAgICAgJ21vZHVsZSBuZXh0IHBhaXJzIHBjYWxsIHByaW50IHJhd2VxdWFsIHJhd2dldCByYXdzZXQgcmVxdWlyZSBzZWxlY3Qgc2V0ZmVudiAnICtcbiAgICAgICAgJ3NldG1ldGF0YWJsZSB0b251bWJlciB0b3N0cmluZyB0eXBlIHVucGFjayB4cGNhbGwgYXJnIHNlbGYgJyArXG4gICAgICAgIC8vIExpYnJhcnkgbWV0aG9kcyBhbmQgcHJvcGVydGllcyAob25lIGxpbmUgcGVyIGxpYnJhcnkpOlxuICAgICAgICAnY29yb3V0aW5lIHJlc3VtZSB5aWVsZCBzdGF0dXMgd3JhcCBjcmVhdGUgcnVubmluZyBkZWJ1ZyBnZXR1cHZhbHVlICcgK1xuICAgICAgICAnZGVidWcgc2V0aG9vayBnZXRtZXRhdGFibGUgZ2V0aG9vayBzZXRtZXRhdGFibGUgc2V0bG9jYWwgdHJhY2ViYWNrIHNldGZlbnYgZ2V0aW5mbyBzZXR1cHZhbHVlIGdldGxvY2FsIGdldHJlZ2lzdHJ5IGdldGZlbnYgJyArXG4gICAgICAgICdpbyBsaW5lcyB3cml0ZSBjbG9zZSBmbHVzaCBvcGVuIG91dHB1dCB0eXBlIHJlYWQgc3RkZXJyIHN0ZGluIGlucHV0IHN0ZG91dCBwb3BlbiB0bXBmaWxlICcgK1xuICAgICAgICAnbWF0aCBsb2cgbWF4IGFjb3MgaHVnZSBsZGV4cCBwaSBjb3MgdGFuaCBwb3cgZGVnIHRhbiBjb3NoIHNpbmggcmFuZG9tIHJhbmRvbXNlZWQgZnJleHAgY2VpbCBmbG9vciByYWQgYWJzIHNxcnQgbW9kZiBhc2luIG1pbiBtb2QgZm1vZCBsb2cxMCBhdGFuMiBleHAgc2luIGF0YW4gJyArXG4gICAgICAgICdvcyBleGl0IHNldGxvY2FsZSBkYXRlIGdldGVudiBkaWZmdGltZSByZW1vdmUgdGltZSBjbG9jayB0bXBuYW1lIHJlbmFtZSBleGVjdXRlIHBhY2thZ2UgcHJlbG9hZCBsb2FkbGliIGxvYWRlZCBsb2FkZXJzIGNwYXRoIGNvbmZpZyBwYXRoIHNlZWFsbCAnICtcbiAgICAgICAgJ3N0cmluZyBzdWIgdXBwZXIgbGVuIGdmaW5kIHJlcCBmaW5kIG1hdGNoIGNoYXIgZHVtcCBnbWF0Y2ggcmV2ZXJzZSBieXRlIGZvcm1hdCBnc3ViIGxvd2VyICcgK1xuICAgICAgICAndGFibGUgc2V0biBpbnNlcnQgZ2V0biBmb3JlYWNoaSBtYXhuIGZvcmVhY2ggY29uY2F0IHNvcnQgcmVtb3ZlJ1xuICAgIH0sXG4gICAgY29udGFpbnM6IENPTU1FTlRTLmNvbmNhdChbXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ2Z1bmN0aW9uJyxcbiAgICAgICAgYmVnaW5LZXl3b3JkczogJ2Z1bmN0aW9uJyxcbiAgICAgICAgZW5kOiAnXFxcXCknLFxuICAgICAgICBjb250YWluczogW1xuICAgICAgICAgIGhsanMuaW5oZXJpdChobGpzLlRJVExFX01PREUsIHtcbiAgICAgICAgICAgIGJlZ2luOiAnKFtfYS16QS1aXVxcXFx3KlxcXFwuKSooW19hLXpBLVpdXFxcXHcqOik/W19hLXpBLVpdXFxcXHcqJ1xuICAgICAgICAgIH0pLFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGNsYXNzTmFtZTogJ3BhcmFtcycsXG4gICAgICAgICAgICBiZWdpbjogJ1xcXFwoJyxcbiAgICAgICAgICAgIGVuZHNXaXRoUGFyZW50OiB0cnVlLFxuICAgICAgICAgICAgY29udGFpbnM6IENPTU1FTlRTXG4gICAgICAgICAgfVxuICAgICAgICBdLmNvbmNhdChDT01NRU5UUylcbiAgICAgIH0sXG4gICAgICBobGpzLkNfTlVNQkVSX01PREUsXG4gICAgICBobGpzLkFQT1NfU1RSSU5HX01PREUsXG4gICAgICBobGpzLlFVT1RFX1NUUklOR19NT0RFLFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgICAgICBiZWdpbjogT1BFTklOR19MT05HX0JSQUNLRVQsXG4gICAgICAgIGVuZDogQ0xPU0lOR19MT05HX0JSQUNLRVQsXG4gICAgICAgIGNvbnRhaW5zOiBbTE9OR19CUkFDS0VUU10sXG4gICAgICAgIHJlbGV2YW5jZTogNVxuICAgICAgfVxuICAgIF0pXG4gIH07XG59XG5cbm1vZHVsZS5leHBvcnRzID0gbHVhO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9