(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_vala"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/vala.js":
/*!***********************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/vala.js ***!
  \***********************************************************************************************/
/***/ ((module) => {

/*
Language: Vala
Author: Antono Vasiljev <antono.vasiljev@gmail.com>
Description: Vala is a new programming language that aims to bring modern programming language features to GNOME developers without imposing any additional runtime requirements and without using a different ABI compared to applications and libraries written in C.
Website: https://wiki.gnome.org/Projects/Vala
*/

function vala(hljs) {
  return {
    name: 'Vala',
    keywords: {
      keyword:
        // Value types
        'char uchar unichar int uint long ulong short ushort int8 int16 int32 int64 uint8 ' +
        'uint16 uint32 uint64 float double bool struct enum string void ' +
        // Reference types
        'weak unowned owned ' +
        // Modifiers
        'async signal static abstract interface override virtual delegate ' +
        // Control Structures
        'if while do for foreach else switch case break default return try catch ' +
        // Visibility
        'public private protected internal ' +
        // Other
        'using new this get set const stdout stdin stderr var',
      built_in:
        'DBus GLib CCode Gee Object Gtk Posix',
      literal:
        'false true null'
    },
    contains: [
      {
        className: 'class',
        beginKeywords: 'class interface namespace',
        end: /\{/,
        excludeEnd: true,
        illegal: '[^,:\\n\\s\\.]',
        contains: [ hljs.UNDERSCORE_TITLE_MODE ]
      },
      hljs.C_LINE_COMMENT_MODE,
      hljs.C_BLOCK_COMMENT_MODE,
      {
        className: 'string',
        begin: '"""',
        end: '"""',
        relevance: 5
      },
      hljs.APOS_STRING_MODE,
      hljs.QUOTE_STRING_MODE,
      hljs.C_NUMBER_MODE,
      {
        className: 'meta',
        begin: '^#',
        end: '$',
        relevance: 2
      }
    ]
  };
}

module.exports = vala;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfdmFsYS5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0E7QUFDQSxnQkFBZ0I7QUFDaEI7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQSIsInNvdXJjZXMiOlsid2VicGFjazovL2R0YWxlLy4vbm9kZV9tb2R1bGVzL3JlYWN0LXN5bnRheC1oaWdobGlnaHRlci9ub2RlX21vZHVsZXMvaGlnaGxpZ2h0LmpzL2xpYi9sYW5ndWFnZXMvdmFsYS5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKlxuTGFuZ3VhZ2U6IFZhbGFcbkF1dGhvcjogQW50b25vIFZhc2lsamV2IDxhbnRvbm8udmFzaWxqZXZAZ21haWwuY29tPlxuRGVzY3JpcHRpb246IFZhbGEgaXMgYSBuZXcgcHJvZ3JhbW1pbmcgbGFuZ3VhZ2UgdGhhdCBhaW1zIHRvIGJyaW5nIG1vZGVybiBwcm9ncmFtbWluZyBsYW5ndWFnZSBmZWF0dXJlcyB0byBHTk9NRSBkZXZlbG9wZXJzIHdpdGhvdXQgaW1wb3NpbmcgYW55IGFkZGl0aW9uYWwgcnVudGltZSByZXF1aXJlbWVudHMgYW5kIHdpdGhvdXQgdXNpbmcgYSBkaWZmZXJlbnQgQUJJIGNvbXBhcmVkIHRvIGFwcGxpY2F0aW9ucyBhbmQgbGlicmFyaWVzIHdyaXR0ZW4gaW4gQy5cbldlYnNpdGU6IGh0dHBzOi8vd2lraS5nbm9tZS5vcmcvUHJvamVjdHMvVmFsYVxuKi9cblxuZnVuY3Rpb24gdmFsYShobGpzKSB7XG4gIHJldHVybiB7XG4gICAgbmFtZTogJ1ZhbGEnLFxuICAgIGtleXdvcmRzOiB7XG4gICAgICBrZXl3b3JkOlxuICAgICAgICAvLyBWYWx1ZSB0eXBlc1xuICAgICAgICAnY2hhciB1Y2hhciB1bmljaGFyIGludCB1aW50IGxvbmcgdWxvbmcgc2hvcnQgdXNob3J0IGludDggaW50MTYgaW50MzIgaW50NjQgdWludDggJyArXG4gICAgICAgICd1aW50MTYgdWludDMyIHVpbnQ2NCBmbG9hdCBkb3VibGUgYm9vbCBzdHJ1Y3QgZW51bSBzdHJpbmcgdm9pZCAnICtcbiAgICAgICAgLy8gUmVmZXJlbmNlIHR5cGVzXG4gICAgICAgICd3ZWFrIHVub3duZWQgb3duZWQgJyArXG4gICAgICAgIC8vIE1vZGlmaWVyc1xuICAgICAgICAnYXN5bmMgc2lnbmFsIHN0YXRpYyBhYnN0cmFjdCBpbnRlcmZhY2Ugb3ZlcnJpZGUgdmlydHVhbCBkZWxlZ2F0ZSAnICtcbiAgICAgICAgLy8gQ29udHJvbCBTdHJ1Y3R1cmVzXG4gICAgICAgICdpZiB3aGlsZSBkbyBmb3IgZm9yZWFjaCBlbHNlIHN3aXRjaCBjYXNlIGJyZWFrIGRlZmF1bHQgcmV0dXJuIHRyeSBjYXRjaCAnICtcbiAgICAgICAgLy8gVmlzaWJpbGl0eVxuICAgICAgICAncHVibGljIHByaXZhdGUgcHJvdGVjdGVkIGludGVybmFsICcgK1xuICAgICAgICAvLyBPdGhlclxuICAgICAgICAndXNpbmcgbmV3IHRoaXMgZ2V0IHNldCBjb25zdCBzdGRvdXQgc3RkaW4gc3RkZXJyIHZhcicsXG4gICAgICBidWlsdF9pbjpcbiAgICAgICAgJ0RCdXMgR0xpYiBDQ29kZSBHZWUgT2JqZWN0IEd0ayBQb3NpeCcsXG4gICAgICBsaXRlcmFsOlxuICAgICAgICAnZmFsc2UgdHJ1ZSBudWxsJ1xuICAgIH0sXG4gICAgY29udGFpbnM6IFtcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnY2xhc3MnLFxuICAgICAgICBiZWdpbktleXdvcmRzOiAnY2xhc3MgaW50ZXJmYWNlIG5hbWVzcGFjZScsXG4gICAgICAgIGVuZDogL1xcey8sXG4gICAgICAgIGV4Y2x1ZGVFbmQ6IHRydWUsXG4gICAgICAgIGlsbGVnYWw6ICdbXiw6XFxcXG5cXFxcc1xcXFwuXScsXG4gICAgICAgIGNvbnRhaW5zOiBbIGhsanMuVU5ERVJTQ09SRV9USVRMRV9NT0RFIF1cbiAgICAgIH0sXG4gICAgICBobGpzLkNfTElORV9DT01NRU5UX01PREUsXG4gICAgICBobGpzLkNfQkxPQ0tfQ09NTUVOVF9NT0RFLFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdzdHJpbmcnLFxuICAgICAgICBiZWdpbjogJ1wiXCJcIicsXG4gICAgICAgIGVuZDogJ1wiXCJcIicsXG4gICAgICAgIHJlbGV2YW5jZTogNVxuICAgICAgfSxcbiAgICAgIGhsanMuQVBPU19TVFJJTkdfTU9ERSxcbiAgICAgIGhsanMuUVVPVEVfU1RSSU5HX01PREUsXG4gICAgICBobGpzLkNfTlVNQkVSX01PREUsXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ21ldGEnLFxuICAgICAgICBiZWdpbjogJ14jJyxcbiAgICAgICAgZW5kOiAnJCcsXG4gICAgICAgIHJlbGV2YW5jZTogMlxuICAgICAgfVxuICAgIF1cbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSB2YWxhO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9