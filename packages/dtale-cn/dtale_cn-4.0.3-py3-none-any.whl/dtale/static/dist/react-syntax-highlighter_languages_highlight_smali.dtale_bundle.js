(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_smali"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/smali.js":
/*!************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/smali.js ***!
  \************************************************************************************************/
/***/ ((module) => {

/*
Language: Smali
Author: Dennis Titze <dennis.titze@gmail.com>
Description: Basic Smali highlighting
Website: https://github.com/JesusFreke/smali
*/

function smali(hljs) {
  const smali_instr_low_prio = [
    'add',
    'and',
    'cmp',
    'cmpg',
    'cmpl',
    'const',
    'div',
    'double',
    'float',
    'goto',
    'if',
    'int',
    'long',
    'move',
    'mul',
    'neg',
    'new',
    'nop',
    'not',
    'or',
    'rem',
    'return',
    'shl',
    'shr',
    'sput',
    'sub',
    'throw',
    'ushr',
    'xor'
  ];
  const smali_instr_high_prio = [
    'aget',
    'aput',
    'array',
    'check',
    'execute',
    'fill',
    'filled',
    'goto/16',
    'goto/32',
    'iget',
    'instance',
    'invoke',
    'iput',
    'monitor',
    'packed',
    'sget',
    'sparse'
  ];
  const smali_keywords = [
    'transient',
    'constructor',
    'abstract',
    'final',
    'synthetic',
    'public',
    'private',
    'protected',
    'static',
    'bridge',
    'system'
  ];
  return {
    name: 'Smali',
    contains: [
      {
        className: 'string',
        begin: '"',
        end: '"',
        relevance: 0
      },
      hljs.COMMENT(
        '#',
        '$',
        {
          relevance: 0
        }
      ),
      {
        className: 'keyword',
        variants: [
          {
            begin: '\\s*\\.end\\s[a-zA-Z0-9]*'
          },
          {
            begin: '^[ ]*\\.[a-zA-Z]*',
            relevance: 0
          },
          {
            begin: '\\s:[a-zA-Z_0-9]*',
            relevance: 0
          },
          {
            begin: '\\s(' + smali_keywords.join('|') + ')'
          }
        ]
      },
      {
        className: 'built_in',
        variants: [
          {
            begin: '\\s(' + smali_instr_low_prio.join('|') + ')\\s'
          },
          {
            begin: '\\s(' + smali_instr_low_prio.join('|') + ')((-|/)[a-zA-Z0-9]+)+\\s',
            relevance: 10
          },
          {
            begin: '\\s(' + smali_instr_high_prio.join('|') + ')((-|/)[a-zA-Z0-9]+)*\\s',
            relevance: 10
          }
        ]
      },
      {
        className: 'class',
        begin: 'L[^\(;:\n]*;',
        relevance: 0
      },
      {
        begin: '[vp][0-9]+'
      }
    ]
  };
}

module.exports = smali;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfc21hbGkuZHRhbGVfYnVuZGxlLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxXQUFXO0FBQ1g7QUFDQTtBQUNBO0FBQ0EsV0FBVztBQUNYO0FBQ0E7QUFDQTtBQUNBLFdBQVc7QUFDWDtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsV0FBVztBQUNYO0FBQ0E7QUFDQTtBQUNBLFdBQVc7QUFDWDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQSxzQkFBc0IsTUFBTTtBQUM1QjtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FBRUEiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9kdGFsZS8uL25vZGVfbW9kdWxlcy9yZWFjdC1zeW50YXgtaGlnaGxpZ2h0ZXIvbm9kZV9tb2R1bGVzL2hpZ2hsaWdodC5qcy9saWIvbGFuZ3VhZ2VzL3NtYWxpLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogU21hbGlcbkF1dGhvcjogRGVubmlzIFRpdHplIDxkZW5uaXMudGl0emVAZ21haWwuY29tPlxuRGVzY3JpcHRpb246IEJhc2ljIFNtYWxpIGhpZ2hsaWdodGluZ1xuV2Vic2l0ZTogaHR0cHM6Ly9naXRodWIuY29tL0plc3VzRnJla2Uvc21hbGlcbiovXG5cbmZ1bmN0aW9uIHNtYWxpKGhsanMpIHtcbiAgY29uc3Qgc21hbGlfaW5zdHJfbG93X3ByaW8gPSBbXG4gICAgJ2FkZCcsXG4gICAgJ2FuZCcsXG4gICAgJ2NtcCcsXG4gICAgJ2NtcGcnLFxuICAgICdjbXBsJyxcbiAgICAnY29uc3QnLFxuICAgICdkaXYnLFxuICAgICdkb3VibGUnLFxuICAgICdmbG9hdCcsXG4gICAgJ2dvdG8nLFxuICAgICdpZicsXG4gICAgJ2ludCcsXG4gICAgJ2xvbmcnLFxuICAgICdtb3ZlJyxcbiAgICAnbXVsJyxcbiAgICAnbmVnJyxcbiAgICAnbmV3JyxcbiAgICAnbm9wJyxcbiAgICAnbm90JyxcbiAgICAnb3InLFxuICAgICdyZW0nLFxuICAgICdyZXR1cm4nLFxuICAgICdzaGwnLFxuICAgICdzaHInLFxuICAgICdzcHV0JyxcbiAgICAnc3ViJyxcbiAgICAndGhyb3cnLFxuICAgICd1c2hyJyxcbiAgICAneG9yJ1xuICBdO1xuICBjb25zdCBzbWFsaV9pbnN0cl9oaWdoX3ByaW8gPSBbXG4gICAgJ2FnZXQnLFxuICAgICdhcHV0JyxcbiAgICAnYXJyYXknLFxuICAgICdjaGVjaycsXG4gICAgJ2V4ZWN1dGUnLFxuICAgICdmaWxsJyxcbiAgICAnZmlsbGVkJyxcbiAgICAnZ290by8xNicsXG4gICAgJ2dvdG8vMzInLFxuICAgICdpZ2V0JyxcbiAgICAnaW5zdGFuY2UnLFxuICAgICdpbnZva2UnLFxuICAgICdpcHV0JyxcbiAgICAnbW9uaXRvcicsXG4gICAgJ3BhY2tlZCcsXG4gICAgJ3NnZXQnLFxuICAgICdzcGFyc2UnXG4gIF07XG4gIGNvbnN0IHNtYWxpX2tleXdvcmRzID0gW1xuICAgICd0cmFuc2llbnQnLFxuICAgICdjb25zdHJ1Y3RvcicsXG4gICAgJ2Fic3RyYWN0JyxcbiAgICAnZmluYWwnLFxuICAgICdzeW50aGV0aWMnLFxuICAgICdwdWJsaWMnLFxuICAgICdwcml2YXRlJyxcbiAgICAncHJvdGVjdGVkJyxcbiAgICAnc3RhdGljJyxcbiAgICAnYnJpZGdlJyxcbiAgICAnc3lzdGVtJ1xuICBdO1xuICByZXR1cm4ge1xuICAgIG5hbWU6ICdTbWFsaScsXG4gICAgY29udGFpbnM6IFtcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnc3RyaW5nJyxcbiAgICAgICAgYmVnaW46ICdcIicsXG4gICAgICAgIGVuZDogJ1wiJyxcbiAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICB9LFxuICAgICAgaGxqcy5DT01NRU5UKFxuICAgICAgICAnIycsXG4gICAgICAgICckJyxcbiAgICAgICAge1xuICAgICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgICB9XG4gICAgICApLFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdrZXl3b3JkJyxcbiAgICAgICAgdmFyaWFudHM6IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbjogJ1xcXFxzKlxcXFwuZW5kXFxcXHNbYS16QS1aMC05XSonXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbjogJ15bIF0qXFxcXC5bYS16QS1aXSonLFxuICAgICAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbjogJ1xcXFxzOlthLXpBLVpfMC05XSonLFxuICAgICAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbjogJ1xcXFxzKCcgKyBzbWFsaV9rZXl3b3Jkcy5qb2luKCd8JykgKyAnKSdcbiAgICAgICAgICB9XG4gICAgICAgIF1cbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ2J1aWx0X2luJyxcbiAgICAgICAgdmFyaWFudHM6IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBiZWdpbjogJ1xcXFxzKCcgKyBzbWFsaV9pbnN0cl9sb3dfcHJpby5qb2luKCd8JykgKyAnKVxcXFxzJ1xuICAgICAgICAgIH0sXG4gICAgICAgICAge1xuICAgICAgICAgICAgYmVnaW46ICdcXFxccygnICsgc21hbGlfaW5zdHJfbG93X3ByaW8uam9pbignfCcpICsgJykoKC18LylbYS16QS1aMC05XSspK1xcXFxzJyxcbiAgICAgICAgICAgIHJlbGV2YW5jZTogMTBcbiAgICAgICAgICB9LFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIGJlZ2luOiAnXFxcXHMoJyArIHNtYWxpX2luc3RyX2hpZ2hfcHJpby5qb2luKCd8JykgKyAnKSgoLXwvKVthLXpBLVowLTldKykqXFxcXHMnLFxuICAgICAgICAgICAgcmVsZXZhbmNlOiAxMFxuICAgICAgICAgIH1cbiAgICAgICAgXVxuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAnY2xhc3MnLFxuICAgICAgICBiZWdpbjogJ0xbXlxcKDs6XFxuXSo7JyxcbiAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBiZWdpbjogJ1t2cF1bMC05XSsnXG4gICAgICB9XG4gICAgXVxuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IHNtYWxpO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9