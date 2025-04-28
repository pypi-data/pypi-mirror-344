(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_nix"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/nix.js":
/*!**********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/nix.js ***!
  \**********************************************************************************************/
/***/ ((module) => {

/*
Language: Nix
Author: Domen Kožar <domen@dev.si>
Description: Nix functional language
Website: http://nixos.org/nix
*/

function nix(hljs) {
  const NIX_KEYWORDS = {
    keyword:
      'rec with let in inherit assert if else then',
    literal:
      'true false or and null',
    built_in:
      'import abort baseNameOf dirOf isNull builtins map removeAttrs throw ' +
      'toString derivation'
  };
  const ANTIQUOTE = {
    className: 'subst',
    begin: /\$\{/,
    end: /\}/,
    keywords: NIX_KEYWORDS
  };
  const ATTRS = {
    begin: /[a-zA-Z0-9-_]+(\s*=)/,
    returnBegin: true,
    relevance: 0,
    contains: [
      {
        className: 'attr',
        begin: /\S+/
      }
    ]
  };
  const STRING = {
    className: 'string',
    contains: [ ANTIQUOTE ],
    variants: [
      {
        begin: "''",
        end: "''"
      },
      {
        begin: '"',
        end: '"'
      }
    ]
  };
  const EXPRESSIONS = [
    hljs.NUMBER_MODE,
    hljs.HASH_COMMENT_MODE,
    hljs.C_BLOCK_COMMENT_MODE,
    STRING,
    ATTRS
  ];
  ANTIQUOTE.contains = EXPRESSIONS;
  return {
    name: 'Nix',
    aliases: [ "nixos" ],
    keywords: NIX_KEYWORDS,
    contains: EXPRESSIONS
  };
}

module.exports = nix;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfbml4LmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxnQkFBZ0I7QUFDaEIsWUFBWTtBQUNaO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9uaXguanMiXSwic291cmNlc0NvbnRlbnQiOlsiLypcbkxhbmd1YWdlOiBOaXhcbkF1dGhvcjogRG9tZW4gS2/FvmFyIDxkb21lbkBkZXYuc2k+XG5EZXNjcmlwdGlvbjogTml4IGZ1bmN0aW9uYWwgbGFuZ3VhZ2VcbldlYnNpdGU6IGh0dHA6Ly9uaXhvcy5vcmcvbml4XG4qL1xuXG5mdW5jdGlvbiBuaXgoaGxqcykge1xuICBjb25zdCBOSVhfS0VZV09SRFMgPSB7XG4gICAga2V5d29yZDpcbiAgICAgICdyZWMgd2l0aCBsZXQgaW4gaW5oZXJpdCBhc3NlcnQgaWYgZWxzZSB0aGVuJyxcbiAgICBsaXRlcmFsOlxuICAgICAgJ3RydWUgZmFsc2Ugb3IgYW5kIG51bGwnLFxuICAgIGJ1aWx0X2luOlxuICAgICAgJ2ltcG9ydCBhYm9ydCBiYXNlTmFtZU9mIGRpck9mIGlzTnVsbCBidWlsdGlucyBtYXAgcmVtb3ZlQXR0cnMgdGhyb3cgJyArXG4gICAgICAndG9TdHJpbmcgZGVyaXZhdGlvbidcbiAgfTtcbiAgY29uc3QgQU5USVFVT1RFID0ge1xuICAgIGNsYXNzTmFtZTogJ3N1YnN0JyxcbiAgICBiZWdpbjogL1xcJFxcey8sXG4gICAgZW5kOiAvXFx9LyxcbiAgICBrZXl3b3JkczogTklYX0tFWVdPUkRTXG4gIH07XG4gIGNvbnN0IEFUVFJTID0ge1xuICAgIGJlZ2luOiAvW2EtekEtWjAtOS1fXSsoXFxzKj0pLyxcbiAgICByZXR1cm5CZWdpbjogdHJ1ZSxcbiAgICByZWxldmFuY2U6IDAsXG4gICAgY29udGFpbnM6IFtcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnYXR0cicsXG4gICAgICAgIGJlZ2luOiAvXFxTKy9cbiAgICAgIH1cbiAgICBdXG4gIH07XG4gIGNvbnN0IFNUUklORyA9IHtcbiAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgIGNvbnRhaW5zOiBbIEFOVElRVU9URSBdLFxuICAgIHZhcmlhbnRzOiBbXG4gICAgICB7XG4gICAgICAgIGJlZ2luOiBcIicnXCIsXG4gICAgICAgIGVuZDogXCInJ1wiXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogJ1wiJyxcbiAgICAgICAgZW5kOiAnXCInXG4gICAgICB9XG4gICAgXVxuICB9O1xuICBjb25zdCBFWFBSRVNTSU9OUyA9IFtcbiAgICBobGpzLk5VTUJFUl9NT0RFLFxuICAgIGhsanMuSEFTSF9DT01NRU5UX01PREUsXG4gICAgaGxqcy5DX0JMT0NLX0NPTU1FTlRfTU9ERSxcbiAgICBTVFJJTkcsXG4gICAgQVRUUlNcbiAgXTtcbiAgQU5USVFVT1RFLmNvbnRhaW5zID0gRVhQUkVTU0lPTlM7XG4gIHJldHVybiB7XG4gICAgbmFtZTogJ05peCcsXG4gICAgYWxpYXNlczogWyBcIm5peG9zXCIgXSxcbiAgICBrZXl3b3JkczogTklYX0tFWVdPUkRTLFxuICAgIGNvbnRhaW5zOiBFWFBSRVNTSU9OU1xuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IG5peDtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==