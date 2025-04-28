(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_mipsasm"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/mipsasm.js":
/*!**************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/mipsasm.js ***!
  \**************************************************************************************************/
/***/ ((module) => {

/*
Language: MIPS Assembly
Author: Nebuleon Fumika <nebuleon.fumika@gmail.com>
Description: MIPS Assembly (up to MIPS32R2)
Website: https://en.wikipedia.org/wiki/MIPS_architecture
Category: assembler
*/

function mipsasm(hljs) {
  // local labels: %?[FB]?[AT]?\d{1,2}\w+
  return {
    name: 'MIPS Assembly',
    case_insensitive: true,
    aliases: [ 'mips' ],
    keywords: {
      $pattern: '\\.?' + hljs.IDENT_RE,
      meta:
        // GNU preprocs
        '.2byte .4byte .align .ascii .asciz .balign .byte .code .data .else .end .endif .endm .endr .equ .err .exitm .extern .global .hword .if .ifdef .ifndef .include .irp .long .macro .rept .req .section .set .skip .space .text .word .ltorg ',
      built_in:
        '$0 $1 $2 $3 $4 $5 $6 $7 $8 $9 $10 $11 $12 $13 $14 $15 ' + // integer registers
        '$16 $17 $18 $19 $20 $21 $22 $23 $24 $25 $26 $27 $28 $29 $30 $31 ' + // integer registers
        'zero at v0 v1 a0 a1 a2 a3 a4 a5 a6 a7 ' + // integer register aliases
        't0 t1 t2 t3 t4 t5 t6 t7 t8 t9 s0 s1 s2 s3 s4 s5 s6 s7 s8 ' + // integer register aliases
        'k0 k1 gp sp fp ra ' + // integer register aliases
        '$f0 $f1 $f2 $f2 $f4 $f5 $f6 $f7 $f8 $f9 $f10 $f11 $f12 $f13 $f14 $f15 ' + // floating-point registers
        '$f16 $f17 $f18 $f19 $f20 $f21 $f22 $f23 $f24 $f25 $f26 $f27 $f28 $f29 $f30 $f31 ' + // floating-point registers
        'Context Random EntryLo0 EntryLo1 Context PageMask Wired EntryHi ' + // Coprocessor 0 registers
        'HWREna BadVAddr Count Compare SR IntCtl SRSCtl SRSMap Cause EPC PRId ' + // Coprocessor 0 registers
        'EBase Config Config1 Config2 Config3 LLAddr Debug DEPC DESAVE CacheErr ' + // Coprocessor 0 registers
        'ECC ErrorEPC TagLo DataLo TagHi DataHi WatchLo WatchHi PerfCtl PerfCnt ' // Coprocessor 0 registers
    },
    contains: [
      {
        className: 'keyword',
        begin: '\\b(' + // mnemonics
            // 32-bit integer instructions
            'addi?u?|andi?|b(al)?|beql?|bgez(al)?l?|bgtzl?|blezl?|bltz(al)?l?|' +
            'bnel?|cl[oz]|divu?|ext|ins|j(al)?|jalr(\\.hb)?|jr(\\.hb)?|lbu?|lhu?|' +
            'll|lui|lw[lr]?|maddu?|mfhi|mflo|movn|movz|move|msubu?|mthi|mtlo|mul|' +
            'multu?|nop|nor|ori?|rotrv?|sb|sc|se[bh]|sh|sllv?|slti?u?|srav?|' +
            'srlv?|subu?|sw[lr]?|xori?|wsbh|' +
            // floating-point instructions
            'abs\\.[sd]|add\\.[sd]|alnv.ps|bc1[ft]l?|' +
            'c\\.(s?f|un|u?eq|[ou]lt|[ou]le|ngle?|seq|l[et]|ng[et])\\.[sd]|' +
            '(ceil|floor|round|trunc)\\.[lw]\\.[sd]|cfc1|cvt\\.d\\.[lsw]|' +
            'cvt\\.l\\.[dsw]|cvt\\.ps\\.s|cvt\\.s\\.[dlw]|cvt\\.s\\.p[lu]|cvt\\.w\\.[dls]|' +
            'div\\.[ds]|ldx?c1|luxc1|lwx?c1|madd\\.[sd]|mfc1|mov[fntz]?\\.[ds]|' +
            'msub\\.[sd]|mth?c1|mul\\.[ds]|neg\\.[ds]|nmadd\\.[ds]|nmsub\\.[ds]|' +
            'p[lu][lu]\\.ps|recip\\.fmt|r?sqrt\\.[ds]|sdx?c1|sub\\.[ds]|suxc1|' +
            'swx?c1|' +
            // system control instructions
            'break|cache|d?eret|[de]i|ehb|mfc0|mtc0|pause|prefx?|rdhwr|' +
            'rdpgpr|sdbbp|ssnop|synci?|syscall|teqi?|tgei?u?|tlb(p|r|w[ir])|' +
            'tlti?u?|tnei?|wait|wrpgpr' +
        ')',
        end: '\\s'
      },
      // lines ending with ; or # aren't really comments, probably auto-detect fail
      hljs.COMMENT('[;#](?!\\s*$)', '$'),
      hljs.C_BLOCK_COMMENT_MODE,
      hljs.QUOTE_STRING_MODE,
      {
        className: 'string',
        begin: '\'',
        end: '[^\\\\]\'',
        relevance: 0
      },
      {
        className: 'title',
        begin: '\\|',
        end: '\\|',
        illegal: '\\n',
        relevance: 0
      },
      {
        className: 'number',
        variants: [
          { // hex
            begin: '0x[0-9a-f]+'
          },
          { // bare number
            begin: '\\b-?\\d+'
          }
        ],
        relevance: 0
      },
      {
        className: 'symbol',
        variants: [
          { // GNU MIPS syntax
            begin: '^\\s*[a-z_\\.\\$][a-z0-9_\\.\\$]+:'
          },
          { // numbered local labels
            begin: '^\\s*[0-9]+:'
          },
          { // number local label reference (backwards, forwards)
            begin: '[0-9]+[bf]'
          }
        ],
        relevance: 0
      }
    ],
    // forward slashes are not allowed
    illegal: /\//
  };
}

module.exports = mipsasm;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfbWlwc2FzbS5kdGFsZV9idW5kbGUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBLGtDQUFrQyxJQUFJO0FBQ3RDO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUCw2QkFBNkI7QUFDN0Isc0JBQXNCO0FBQ3RCO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSxZQUFZO0FBQ1o7QUFDQSxXQUFXO0FBQ1gsWUFBWTtBQUNaO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLFlBQVk7QUFDWjtBQUNBLFdBQVc7QUFDWCxZQUFZO0FBQ1o7QUFDQSxXQUFXO0FBQ1gsWUFBWTtBQUNaO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9taXBzYXNtLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG5MYW5ndWFnZTogTUlQUyBBc3NlbWJseVxuQXV0aG9yOiBOZWJ1bGVvbiBGdW1pa2EgPG5lYnVsZW9uLmZ1bWlrYUBnbWFpbC5jb20+XG5EZXNjcmlwdGlvbjogTUlQUyBBc3NlbWJseSAodXAgdG8gTUlQUzMyUjIpXG5XZWJzaXRlOiBodHRwczovL2VuLndpa2lwZWRpYS5vcmcvd2lraS9NSVBTX2FyY2hpdGVjdHVyZVxuQ2F0ZWdvcnk6IGFzc2VtYmxlclxuKi9cblxuZnVuY3Rpb24gbWlwc2FzbShobGpzKSB7XG4gIC8vIGxvY2FsIGxhYmVsczogJT9bRkJdP1tBVF0/XFxkezEsMn1cXHcrXG4gIHJldHVybiB7XG4gICAgbmFtZTogJ01JUFMgQXNzZW1ibHknLFxuICAgIGNhc2VfaW5zZW5zaXRpdmU6IHRydWUsXG4gICAgYWxpYXNlczogWyAnbWlwcycgXSxcbiAgICBrZXl3b3Jkczoge1xuICAgICAgJHBhdHRlcm46ICdcXFxcLj8nICsgaGxqcy5JREVOVF9SRSxcbiAgICAgIG1ldGE6XG4gICAgICAgIC8vIEdOVSBwcmVwcm9jc1xuICAgICAgICAnLjJieXRlIC40Ynl0ZSAuYWxpZ24gLmFzY2lpIC5hc2NpeiAuYmFsaWduIC5ieXRlIC5jb2RlIC5kYXRhIC5lbHNlIC5lbmQgLmVuZGlmIC5lbmRtIC5lbmRyIC5lcXUgLmVyciAuZXhpdG0gLmV4dGVybiAuZ2xvYmFsIC5od29yZCAuaWYgLmlmZGVmIC5pZm5kZWYgLmluY2x1ZGUgLmlycCAubG9uZyAubWFjcm8gLnJlcHQgLnJlcSAuc2VjdGlvbiAuc2V0IC5za2lwIC5zcGFjZSAudGV4dCAud29yZCAubHRvcmcgJyxcbiAgICAgIGJ1aWx0X2luOlxuICAgICAgICAnJDAgJDEgJDIgJDMgJDQgJDUgJDYgJDcgJDggJDkgJDEwICQxMSAkMTIgJDEzICQxNCAkMTUgJyArIC8vIGludGVnZXIgcmVnaXN0ZXJzXG4gICAgICAgICckMTYgJDE3ICQxOCAkMTkgJDIwICQyMSAkMjIgJDIzICQyNCAkMjUgJDI2ICQyNyAkMjggJDI5ICQzMCAkMzEgJyArIC8vIGludGVnZXIgcmVnaXN0ZXJzXG4gICAgICAgICd6ZXJvIGF0IHYwIHYxIGEwIGExIGEyIGEzIGE0IGE1IGE2IGE3ICcgKyAvLyBpbnRlZ2VyIHJlZ2lzdGVyIGFsaWFzZXNcbiAgICAgICAgJ3QwIHQxIHQyIHQzIHQ0IHQ1IHQ2IHQ3IHQ4IHQ5IHMwIHMxIHMyIHMzIHM0IHM1IHM2IHM3IHM4ICcgKyAvLyBpbnRlZ2VyIHJlZ2lzdGVyIGFsaWFzZXNcbiAgICAgICAgJ2swIGsxIGdwIHNwIGZwIHJhICcgKyAvLyBpbnRlZ2VyIHJlZ2lzdGVyIGFsaWFzZXNcbiAgICAgICAgJyRmMCAkZjEgJGYyICRmMiAkZjQgJGY1ICRmNiAkZjcgJGY4ICRmOSAkZjEwICRmMTEgJGYxMiAkZjEzICRmMTQgJGYxNSAnICsgLy8gZmxvYXRpbmctcG9pbnQgcmVnaXN0ZXJzXG4gICAgICAgICckZjE2ICRmMTcgJGYxOCAkZjE5ICRmMjAgJGYyMSAkZjIyICRmMjMgJGYyNCAkZjI1ICRmMjYgJGYyNyAkZjI4ICRmMjkgJGYzMCAkZjMxICcgKyAvLyBmbG9hdGluZy1wb2ludCByZWdpc3RlcnNcbiAgICAgICAgJ0NvbnRleHQgUmFuZG9tIEVudHJ5TG8wIEVudHJ5TG8xIENvbnRleHQgUGFnZU1hc2sgV2lyZWQgRW50cnlIaSAnICsgLy8gQ29wcm9jZXNzb3IgMCByZWdpc3RlcnNcbiAgICAgICAgJ0hXUkVuYSBCYWRWQWRkciBDb3VudCBDb21wYXJlIFNSIEludEN0bCBTUlNDdGwgU1JTTWFwIENhdXNlIEVQQyBQUklkICcgKyAvLyBDb3Byb2Nlc3NvciAwIHJlZ2lzdGVyc1xuICAgICAgICAnRUJhc2UgQ29uZmlnIENvbmZpZzEgQ29uZmlnMiBDb25maWczIExMQWRkciBEZWJ1ZyBERVBDIERFU0FWRSBDYWNoZUVyciAnICsgLy8gQ29wcm9jZXNzb3IgMCByZWdpc3RlcnNcbiAgICAgICAgJ0VDQyBFcnJvckVQQyBUYWdMbyBEYXRhTG8gVGFnSGkgRGF0YUhpIFdhdGNoTG8gV2F0Y2hIaSBQZXJmQ3RsIFBlcmZDbnQgJyAvLyBDb3Byb2Nlc3NvciAwIHJlZ2lzdGVyc1xuICAgIH0sXG4gICAgY29udGFpbnM6IFtcbiAgICAgIHtcbiAgICAgICAgY2xhc3NOYW1lOiAna2V5d29yZCcsXG4gICAgICAgIGJlZ2luOiAnXFxcXGIoJyArIC8vIG1uZW1vbmljc1xuICAgICAgICAgICAgLy8gMzItYml0IGludGVnZXIgaW5zdHJ1Y3Rpb25zXG4gICAgICAgICAgICAnYWRkaT91P3xhbmRpP3xiKGFsKT98YmVxbD98YmdleihhbCk/bD98Ymd0emw/fGJsZXpsP3xibHR6KGFsKT9sP3wnICtcbiAgICAgICAgICAgICdibmVsP3xjbFtvel18ZGl2dT98ZXh0fGluc3xqKGFsKT98amFscihcXFxcLmhiKT98anIoXFxcXC5oYik/fGxidT98bGh1P3wnICtcbiAgICAgICAgICAgICdsbHxsdWl8bHdbbHJdP3xtYWRkdT98bWZoaXxtZmxvfG1vdm58bW92enxtb3ZlfG1zdWJ1P3xtdGhpfG10bG98bXVsfCcgK1xuICAgICAgICAgICAgJ211bHR1P3xub3B8bm9yfG9yaT98cm90cnY/fHNifHNjfHNlW2JoXXxzaHxzbGx2P3xzbHRpP3U/fHNyYXY/fCcgK1xuICAgICAgICAgICAgJ3NybHY/fHN1YnU/fHN3W2xyXT98eG9yaT98d3NiaHwnICtcbiAgICAgICAgICAgIC8vIGZsb2F0aW5nLXBvaW50IGluc3RydWN0aW9uc1xuICAgICAgICAgICAgJ2Fic1xcXFwuW3NkXXxhZGRcXFxcLltzZF18YWxudi5wc3xiYzFbZnRdbD98JyArXG4gICAgICAgICAgICAnY1xcXFwuKHM/Znx1bnx1P2VxfFtvdV1sdHxbb3VdbGV8bmdsZT98c2VxfGxbZXRdfG5nW2V0XSlcXFxcLltzZF18JyArXG4gICAgICAgICAgICAnKGNlaWx8Zmxvb3J8cm91bmR8dHJ1bmMpXFxcXC5bbHddXFxcXC5bc2RdfGNmYzF8Y3Z0XFxcXC5kXFxcXC5bbHN3XXwnICtcbiAgICAgICAgICAgICdjdnRcXFxcLmxcXFxcLltkc3ddfGN2dFxcXFwucHNcXFxcLnN8Y3Z0XFxcXC5zXFxcXC5bZGx3XXxjdnRcXFxcLnNcXFxcLnBbbHVdfGN2dFxcXFwud1xcXFwuW2Rsc118JyArXG4gICAgICAgICAgICAnZGl2XFxcXC5bZHNdfGxkeD9jMXxsdXhjMXxsd3g/YzF8bWFkZFxcXFwuW3NkXXxtZmMxfG1vdltmbnR6XT9cXFxcLltkc118JyArXG4gICAgICAgICAgICAnbXN1YlxcXFwuW3NkXXxtdGg/YzF8bXVsXFxcXC5bZHNdfG5lZ1xcXFwuW2RzXXxubWFkZFxcXFwuW2RzXXxubXN1YlxcXFwuW2RzXXwnICtcbiAgICAgICAgICAgICdwW2x1XVtsdV1cXFxcLnBzfHJlY2lwXFxcXC5mbXR8cj9zcXJ0XFxcXC5bZHNdfHNkeD9jMXxzdWJcXFxcLltkc118c3V4YzF8JyArXG4gICAgICAgICAgICAnc3d4P2MxfCcgK1xuICAgICAgICAgICAgLy8gc3lzdGVtIGNvbnRyb2wgaW5zdHJ1Y3Rpb25zXG4gICAgICAgICAgICAnYnJlYWt8Y2FjaGV8ZD9lcmV0fFtkZV1pfGVoYnxtZmMwfG10YzB8cGF1c2V8cHJlZng/fHJkaHdyfCcgK1xuICAgICAgICAgICAgJ3JkcGdwcnxzZGJicHxzc25vcHxzeW5jaT98c3lzY2FsbHx0ZXFpP3x0Z2VpP3U/fHRsYihwfHJ8d1tpcl0pfCcgK1xuICAgICAgICAgICAgJ3RsdGk/dT98dG5laT98d2FpdHx3cnBncHInICtcbiAgICAgICAgJyknLFxuICAgICAgICBlbmQ6ICdcXFxccydcbiAgICAgIH0sXG4gICAgICAvLyBsaW5lcyBlbmRpbmcgd2l0aCA7IG9yICMgYXJlbid0IHJlYWxseSBjb21tZW50cywgcHJvYmFibHkgYXV0by1kZXRlY3QgZmFpbFxuICAgICAgaGxqcy5DT01NRU5UKCdbOyNdKD8hXFxcXHMqJCknLCAnJCcpLFxuICAgICAgaGxqcy5DX0JMT0NLX0NPTU1FTlRfTU9ERSxcbiAgICAgIGhsanMuUVVPVEVfU1RSSU5HX01PREUsXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3N0cmluZycsXG4gICAgICAgIGJlZ2luOiAnXFwnJyxcbiAgICAgICAgZW5kOiAnW15cXFxcXFxcXF1cXCcnLFxuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3RpdGxlJyxcbiAgICAgICAgYmVnaW46ICdcXFxcfCcsXG4gICAgICAgIGVuZDogJ1xcXFx8JyxcbiAgICAgICAgaWxsZWdhbDogJ1xcXFxuJyxcbiAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdudW1iZXInLFxuICAgICAgICB2YXJpYW50czogW1xuICAgICAgICAgIHsgLy8gaGV4XG4gICAgICAgICAgICBiZWdpbjogJzB4WzAtOWEtZl0rJ1xuICAgICAgICAgIH0sXG4gICAgICAgICAgeyAvLyBiYXJlIG51bWJlclxuICAgICAgICAgICAgYmVnaW46ICdcXFxcYi0/XFxcXGQrJ1xuICAgICAgICAgIH1cbiAgICAgICAgXSxcbiAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdzeW1ib2wnLFxuICAgICAgICB2YXJpYW50czogW1xuICAgICAgICAgIHsgLy8gR05VIE1JUFMgc3ludGF4XG4gICAgICAgICAgICBiZWdpbjogJ15cXFxccypbYS16X1xcXFwuXFxcXCRdW2EtejAtOV9cXFxcLlxcXFwkXSs6J1xuICAgICAgICAgIH0sXG4gICAgICAgICAgeyAvLyBudW1iZXJlZCBsb2NhbCBsYWJlbHNcbiAgICAgICAgICAgIGJlZ2luOiAnXlxcXFxzKlswLTldKzonXG4gICAgICAgICAgfSxcbiAgICAgICAgICB7IC8vIG51bWJlciBsb2NhbCBsYWJlbCByZWZlcmVuY2UgKGJhY2t3YXJkcywgZm9yd2FyZHMpXG4gICAgICAgICAgICBiZWdpbjogJ1swLTldK1tiZl0nXG4gICAgICAgICAgfVxuICAgICAgICBdLFxuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH1cbiAgICBdLFxuICAgIC8vIGZvcndhcmQgc2xhc2hlcyBhcmUgbm90IGFsbG93ZWRcbiAgICBpbGxlZ2FsOiAvXFwvL1xuICB9O1xufVxuXG5tb2R1bGUuZXhwb3J0cyA9IG1pcHNhc207XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=