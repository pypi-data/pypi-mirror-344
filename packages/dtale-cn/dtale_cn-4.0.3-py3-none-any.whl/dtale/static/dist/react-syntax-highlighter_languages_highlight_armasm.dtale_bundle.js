(self["webpackChunkdtale"] = self["webpackChunkdtale"] || []).push([["react-syntax-highlighter_languages_highlight_armasm"],{

/***/ "./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/armasm.js":
/*!*************************************************************************************************!*\
  !*** ./node_modules/react-syntax-highlighter/node_modules/highlight.js/lib/languages/armasm.js ***!
  \*************************************************************************************************/
/***/ ((module) => {

/*
Language: ARM Assembly
Author: Dan Panzarella <alsoelp@gmail.com>
Description: ARM Assembly including Thumb and Thumb2 instructions
Category: assembler
*/

/** @type LanguageFn */
function armasm(hljs) {
  // local labels: %?[FB]?[AT]?\d{1,2}\w+

  const COMMENT = {
    variants: [
      hljs.COMMENT('^[ \\t]*(?=#)', '$', {
        relevance: 0,
        excludeBegin: true
      }),
      hljs.COMMENT('[;@]', '$', {
        relevance: 0
      }),
      hljs.C_LINE_COMMENT_MODE,
      hljs.C_BLOCK_COMMENT_MODE
    ]
  };

  return {
    name: 'ARM Assembly',
    case_insensitive: true,
    aliases: ['arm'],
    keywords: {
      $pattern: '\\.?' + hljs.IDENT_RE,
      meta:
        // GNU preprocs
        '.2byte .4byte .align .ascii .asciz .balign .byte .code .data .else .end .endif .endm .endr .equ .err .exitm .extern .global .hword .if .ifdef .ifndef .include .irp .long .macro .rept .req .section .set .skip .space .text .word .arm .thumb .code16 .code32 .force_thumb .thumb_func .ltorg ' +
        // ARM directives
        'ALIAS ALIGN ARM AREA ASSERT ATTR CN CODE CODE16 CODE32 COMMON CP DATA DCB DCD DCDU DCDO DCFD DCFDU DCI DCQ DCQU DCW DCWU DN ELIF ELSE END ENDFUNC ENDIF ENDP ENTRY EQU EXPORT EXPORTAS EXTERN FIELD FILL FUNCTION GBLA GBLL GBLS GET GLOBAL IF IMPORT INCBIN INCLUDE INFO KEEP LCLA LCLL LCLS LTORG MACRO MAP MEND MEXIT NOFP OPT PRESERVE8 PROC QN READONLY RELOC REQUIRE REQUIRE8 RLIST FN ROUT SETA SETL SETS SN SPACE SUBT THUMB THUMBX TTL WHILE WEND ',
      built_in:
        'r0 r1 r2 r3 r4 r5 r6 r7 r8 r9 r10 r11 r12 r13 r14 r15 ' + // standard registers
        'pc lr sp ip sl sb fp ' + // typical regs plus backward compatibility
        'a1 a2 a3 a4 v1 v2 v3 v4 v5 v6 v7 v8 f0 f1 f2 f3 f4 f5 f6 f7 ' + // more regs and fp
        'p0 p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 p11 p12 p13 p14 p15 ' + // coprocessor regs
        'c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12 c13 c14 c15 ' + // more coproc
        'q0 q1 q2 q3 q4 q5 q6 q7 q8 q9 q10 q11 q12 q13 q14 q15 ' + // advanced SIMD NEON regs

        // program status registers
        'cpsr_c cpsr_x cpsr_s cpsr_f cpsr_cx cpsr_cxs cpsr_xs cpsr_xsf cpsr_sf cpsr_cxsf ' +
        'spsr_c spsr_x spsr_s spsr_f spsr_cx spsr_cxs spsr_xs spsr_xsf spsr_sf spsr_cxsf ' +

        // NEON and VFP registers
        's0 s1 s2 s3 s4 s5 s6 s7 s8 s9 s10 s11 s12 s13 s14 s15 ' +
        's16 s17 s18 s19 s20 s21 s22 s23 s24 s25 s26 s27 s28 s29 s30 s31 ' +
        'd0 d1 d2 d3 d4 d5 d6 d7 d8 d9 d10 d11 d12 d13 d14 d15 ' +
        'd16 d17 d18 d19 d20 d21 d22 d23 d24 d25 d26 d27 d28 d29 d30 d31 ' +

        '{PC} {VAR} {TRUE} {FALSE} {OPT} {CONFIG} {ENDIAN} {CODESIZE} {CPU} {FPU} {ARCHITECTURE} {PCSTOREOFFSET} {ARMASM_VERSION} {INTER} {ROPI} {RWPI} {SWST} {NOSWST} . @'
    },
    contains: [
      {
        className: 'keyword',
        begin: '\\b(' + // mnemonics
            'adc|' +
            '(qd?|sh?|u[qh]?)?add(8|16)?|usada?8|(q|sh?|u[qh]?)?(as|sa)x|' +
            'and|adrl?|sbc|rs[bc]|asr|b[lx]?|blx|bxj|cbn?z|tb[bh]|bic|' +
            'bfc|bfi|[su]bfx|bkpt|cdp2?|clz|clrex|cmp|cmn|cpsi[ed]|cps|' +
            'setend|dbg|dmb|dsb|eor|isb|it[te]{0,3}|lsl|lsr|ror|rrx|' +
            'ldm(([id][ab])|f[ds])?|ldr((s|ex)?[bhd])?|movt?|mvn|mra|mar|' +
            'mul|[us]mull|smul[bwt][bt]|smu[as]d|smmul|smmla|' +
            'mla|umlaal|smlal?([wbt][bt]|d)|mls|smlsl?[ds]|smc|svc|sev|' +
            'mia([bt]{2}|ph)?|mrr?c2?|mcrr2?|mrs|msr|orr|orn|pkh(tb|bt)|rbit|' +
            'rev(16|sh)?|sel|[su]sat(16)?|nop|pop|push|rfe([id][ab])?|' +
            'stm([id][ab])?|str(ex)?[bhd]?|(qd?)?sub|(sh?|q|u[qh]?)?sub(8|16)|' +
            '[su]xt(a?h|a?b(16)?)|srs([id][ab])?|swpb?|swi|smi|tst|teq|' +
            'wfe|wfi|yield' +
        ')' +
        '(eq|ne|cs|cc|mi|pl|vs|vc|hi|ls|ge|lt|gt|le|al|hs|lo)?' + // condition codes
        '[sptrx]?' + // legal postfixes
        '(?=\\s)' // followed by space
      },
      COMMENT,
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
            begin: '[#$=]?0x[0-9a-f]+'
          },
          { // bin
            begin: '[#$=]?0b[01]+'
          },
          { // literal
            begin: '[#$=]\\d+'
          },
          { // bare number
            begin: '\\b\\d+'
          }
        ],
        relevance: 0
      },
      {
        className: 'symbol',
        variants: [
          { // GNU ARM syntax
            begin: '^[ \\t]*[a-z_\\.\\$][a-z0-9_\\.\\$]+:'
          },
          { // ARM syntax
            begin: '^[a-z_\\.\\$][a-z0-9_\\.\\$]+'
          },
          { // label reference
            begin: '[=#]\\w+'
          }
        ],
        relevance: 0
      }
    ]
  };
}

module.exports = armasm;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyX2xhbmd1YWdlc19oaWdobGlnaHRfYXJtYXNtLmR0YWxlX2J1bmRsZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0Esa0NBQWtDLElBQUk7O0FBRXRDO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1Asc0JBQXNCO0FBQ3RCO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQSxVQUFVLEtBQUssTUFBTSxPQUFPLFFBQVEsTUFBTSxTQUFTLFNBQVMsV0FBVyxNQUFNLE1BQU0sZUFBZSxnQkFBZ0IsaUJBQWlCLFFBQVEsT0FBTyxPQUFPLE9BQU8sUUFBUTtBQUN4SyxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLCtDQUErQyxJQUFJO0FBQ25EO0FBQ0E7QUFDQTtBQUNBLHNCQUFzQixFQUFFO0FBQ3hCO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTztBQUNQO0FBQ0E7QUFDQTtBQUNBLFlBQVk7QUFDWjtBQUNBLFdBQVc7QUFDWCxZQUFZO0FBQ1o7QUFDQSxXQUFXO0FBQ1gsWUFBWTtBQUNaO0FBQ0EsV0FBVztBQUNYLFlBQVk7QUFDWjtBQUNBO0FBQ0E7QUFDQTtBQUNBLE9BQU87QUFDUDtBQUNBO0FBQ0E7QUFDQSxZQUFZO0FBQ1o7QUFDQSxXQUFXO0FBQ1gsWUFBWTtBQUNaO0FBQ0EsV0FBVztBQUNYLFlBQVk7QUFDWjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vZHRhbGUvLi9ub2RlX21vZHVsZXMvcmVhY3Qtc3ludGF4LWhpZ2hsaWdodGVyL25vZGVfbW9kdWxlcy9oaWdobGlnaHQuanMvbGliL2xhbmd1YWdlcy9hcm1hc20uanMiXSwic291cmNlc0NvbnRlbnQiOlsiLypcbkxhbmd1YWdlOiBBUk0gQXNzZW1ibHlcbkF1dGhvcjogRGFuIFBhbnphcmVsbGEgPGFsc29lbHBAZ21haWwuY29tPlxuRGVzY3JpcHRpb246IEFSTSBBc3NlbWJseSBpbmNsdWRpbmcgVGh1bWIgYW5kIFRodW1iMiBpbnN0cnVjdGlvbnNcbkNhdGVnb3J5OiBhc3NlbWJsZXJcbiovXG5cbi8qKiBAdHlwZSBMYW5ndWFnZUZuICovXG5mdW5jdGlvbiBhcm1hc20oaGxqcykge1xuICAvLyBsb2NhbCBsYWJlbHM6ICU/W0ZCXT9bQVRdP1xcZHsxLDJ9XFx3K1xuXG4gIGNvbnN0IENPTU1FTlQgPSB7XG4gICAgdmFyaWFudHM6IFtcbiAgICAgIGhsanMuQ09NTUVOVCgnXlsgXFxcXHRdKig/PSMpJywgJyQnLCB7XG4gICAgICAgIHJlbGV2YW5jZTogMCxcbiAgICAgICAgZXhjbHVkZUJlZ2luOiB0cnVlXG4gICAgICB9KSxcbiAgICAgIGhsanMuQ09NTUVOVCgnWztAXScsICckJywge1xuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH0pLFxuICAgICAgaGxqcy5DX0xJTkVfQ09NTUVOVF9NT0RFLFxuICAgICAgaGxqcy5DX0JMT0NLX0NPTU1FTlRfTU9ERVxuICAgIF1cbiAgfTtcblxuICByZXR1cm4ge1xuICAgIG5hbWU6ICdBUk0gQXNzZW1ibHknLFxuICAgIGNhc2VfaW5zZW5zaXRpdmU6IHRydWUsXG4gICAgYWxpYXNlczogWydhcm0nXSxcbiAgICBrZXl3b3Jkczoge1xuICAgICAgJHBhdHRlcm46ICdcXFxcLj8nICsgaGxqcy5JREVOVF9SRSxcbiAgICAgIG1ldGE6XG4gICAgICAgIC8vIEdOVSBwcmVwcm9jc1xuICAgICAgICAnLjJieXRlIC40Ynl0ZSAuYWxpZ24gLmFzY2lpIC5hc2NpeiAuYmFsaWduIC5ieXRlIC5jb2RlIC5kYXRhIC5lbHNlIC5lbmQgLmVuZGlmIC5lbmRtIC5lbmRyIC5lcXUgLmVyciAuZXhpdG0gLmV4dGVybiAuZ2xvYmFsIC5od29yZCAuaWYgLmlmZGVmIC5pZm5kZWYgLmluY2x1ZGUgLmlycCAubG9uZyAubWFjcm8gLnJlcHQgLnJlcSAuc2VjdGlvbiAuc2V0IC5za2lwIC5zcGFjZSAudGV4dCAud29yZCAuYXJtIC50aHVtYiAuY29kZTE2IC5jb2RlMzIgLmZvcmNlX3RodW1iIC50aHVtYl9mdW5jIC5sdG9yZyAnICtcbiAgICAgICAgLy8gQVJNIGRpcmVjdGl2ZXNcbiAgICAgICAgJ0FMSUFTIEFMSUdOIEFSTSBBUkVBIEFTU0VSVCBBVFRSIENOIENPREUgQ09ERTE2IENPREUzMiBDT01NT04gQ1AgREFUQSBEQ0IgRENEIERDRFUgRENETyBEQ0ZEIERDRkRVIERDSSBEQ1EgRENRVSBEQ1cgRENXVSBETiBFTElGIEVMU0UgRU5EIEVOREZVTkMgRU5ESUYgRU5EUCBFTlRSWSBFUVUgRVhQT1JUIEVYUE9SVEFTIEVYVEVSTiBGSUVMRCBGSUxMIEZVTkNUSU9OIEdCTEEgR0JMTCBHQkxTIEdFVCBHTE9CQUwgSUYgSU1QT1JUIElOQ0JJTiBJTkNMVURFIElORk8gS0VFUCBMQ0xBIExDTEwgTENMUyBMVE9SRyBNQUNSTyBNQVAgTUVORCBNRVhJVCBOT0ZQIE9QVCBQUkVTRVJWRTggUFJPQyBRTiBSRUFET05MWSBSRUxPQyBSRVFVSVJFIFJFUVVJUkU4IFJMSVNUIEZOIFJPVVQgU0VUQSBTRVRMIFNFVFMgU04gU1BBQ0UgU1VCVCBUSFVNQiBUSFVNQlggVFRMIFdISUxFIFdFTkQgJyxcbiAgICAgIGJ1aWx0X2luOlxuICAgICAgICAncjAgcjEgcjIgcjMgcjQgcjUgcjYgcjcgcjggcjkgcjEwIHIxMSByMTIgcjEzIHIxNCByMTUgJyArIC8vIHN0YW5kYXJkIHJlZ2lzdGVyc1xuICAgICAgICAncGMgbHIgc3AgaXAgc2wgc2IgZnAgJyArIC8vIHR5cGljYWwgcmVncyBwbHVzIGJhY2t3YXJkIGNvbXBhdGliaWxpdHlcbiAgICAgICAgJ2ExIGEyIGEzIGE0IHYxIHYyIHYzIHY0IHY1IHY2IHY3IHY4IGYwIGYxIGYyIGYzIGY0IGY1IGY2IGY3ICcgKyAvLyBtb3JlIHJlZ3MgYW5kIGZwXG4gICAgICAgICdwMCBwMSBwMiBwMyBwNCBwNSBwNiBwNyBwOCBwOSBwMTAgcDExIHAxMiBwMTMgcDE0IHAxNSAnICsgLy8gY29wcm9jZXNzb3IgcmVnc1xuICAgICAgICAnYzAgYzEgYzIgYzMgYzQgYzUgYzYgYzcgYzggYzkgYzEwIGMxMSBjMTIgYzEzIGMxNCBjMTUgJyArIC8vIG1vcmUgY29wcm9jXG4gICAgICAgICdxMCBxMSBxMiBxMyBxNCBxNSBxNiBxNyBxOCBxOSBxMTAgcTExIHExMiBxMTMgcTE0IHExNSAnICsgLy8gYWR2YW5jZWQgU0lNRCBORU9OIHJlZ3NcblxuICAgICAgICAvLyBwcm9ncmFtIHN0YXR1cyByZWdpc3RlcnNcbiAgICAgICAgJ2Nwc3JfYyBjcHNyX3ggY3Bzcl9zIGNwc3JfZiBjcHNyX2N4IGNwc3JfY3hzIGNwc3JfeHMgY3Bzcl94c2YgY3Bzcl9zZiBjcHNyX2N4c2YgJyArXG4gICAgICAgICdzcHNyX2Mgc3Bzcl94IHNwc3JfcyBzcHNyX2Ygc3Bzcl9jeCBzcHNyX2N4cyBzcHNyX3hzIHNwc3JfeHNmIHNwc3Jfc2Ygc3Bzcl9jeHNmICcgK1xuXG4gICAgICAgIC8vIE5FT04gYW5kIFZGUCByZWdpc3RlcnNcbiAgICAgICAgJ3MwIHMxIHMyIHMzIHM0IHM1IHM2IHM3IHM4IHM5IHMxMCBzMTEgczEyIHMxMyBzMTQgczE1ICcgK1xuICAgICAgICAnczE2IHMxNyBzMTggczE5IHMyMCBzMjEgczIyIHMyMyBzMjQgczI1IHMyNiBzMjcgczI4IHMyOSBzMzAgczMxICcgK1xuICAgICAgICAnZDAgZDEgZDIgZDMgZDQgZDUgZDYgZDcgZDggZDkgZDEwIGQxMSBkMTIgZDEzIGQxNCBkMTUgJyArXG4gICAgICAgICdkMTYgZDE3IGQxOCBkMTkgZDIwIGQyMSBkMjIgZDIzIGQyNCBkMjUgZDI2IGQyNyBkMjggZDI5IGQzMCBkMzEgJyArXG5cbiAgICAgICAgJ3tQQ30ge1ZBUn0ge1RSVUV9IHtGQUxTRX0ge09QVH0ge0NPTkZJR30ge0VORElBTn0ge0NPREVTSVpFfSB7Q1BVfSB7RlBVfSB7QVJDSElURUNUVVJFfSB7UENTVE9SRU9GRlNFVH0ge0FSTUFTTV9WRVJTSU9OfSB7SU5URVJ9IHtST1BJfSB7UldQSX0ge1NXU1R9IHtOT1NXU1R9IC4gQCdcbiAgICB9LFxuICAgIGNvbnRhaW5zOiBbXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ2tleXdvcmQnLFxuICAgICAgICBiZWdpbjogJ1xcXFxiKCcgKyAvLyBtbmVtb25pY3NcbiAgICAgICAgICAgICdhZGN8JyArXG4gICAgICAgICAgICAnKHFkP3xzaD98dVtxaF0/KT9hZGQoOHwxNik/fHVzYWRhPzh8KHF8c2g/fHVbcWhdPyk/KGFzfHNhKXh8JyArXG4gICAgICAgICAgICAnYW5kfGFkcmw/fHNiY3xyc1tiY118YXNyfGJbbHhdP3xibHh8YnhqfGNibj96fHRiW2JoXXxiaWN8JyArXG4gICAgICAgICAgICAnYmZjfGJmaXxbc3VdYmZ4fGJrcHR8Y2RwMj98Y2x6fGNscmV4fGNtcHxjbW58Y3BzaVtlZF18Y3BzfCcgK1xuICAgICAgICAgICAgJ3NldGVuZHxkYmd8ZG1ifGRzYnxlb3J8aXNifGl0W3RlXXswLDN9fGxzbHxsc3J8cm9yfHJyeHwnICtcbiAgICAgICAgICAgICdsZG0oKFtpZF1bYWJdKXxmW2RzXSk/fGxkcigoc3xleCk/W2JoZF0pP3xtb3Z0P3xtdm58bXJhfG1hcnwnICtcbiAgICAgICAgICAgICdtdWx8W3VzXW11bGx8c211bFtid3RdW2J0XXxzbXVbYXNdZHxzbW11bHxzbW1sYXwnICtcbiAgICAgICAgICAgICdtbGF8dW1sYWFsfHNtbGFsPyhbd2J0XVtidF18ZCl8bWxzfHNtbHNsP1tkc118c21jfHN2Y3xzZXZ8JyArXG4gICAgICAgICAgICAnbWlhKFtidF17Mn18cGgpP3xtcnI/YzI/fG1jcnIyP3xtcnN8bXNyfG9ycnxvcm58cGtoKHRifGJ0KXxyYml0fCcgK1xuICAgICAgICAgICAgJ3JldigxNnxzaCk/fHNlbHxbc3Vdc2F0KDE2KT98bm9wfHBvcHxwdXNofHJmZShbaWRdW2FiXSk/fCcgK1xuICAgICAgICAgICAgJ3N0bShbaWRdW2FiXSk/fHN0cihleCk/W2JoZF0/fChxZD8pP3N1Ynwoc2g/fHF8dVtxaF0/KT9zdWIoOHwxNil8JyArXG4gICAgICAgICAgICAnW3N1XXh0KGE/aHxhP2IoMTYpPyl8c3JzKFtpZF1bYWJdKT98c3dwYj98c3dpfHNtaXx0c3R8dGVxfCcgK1xuICAgICAgICAgICAgJ3dmZXx3Zml8eWllbGQnICtcbiAgICAgICAgJyknICtcbiAgICAgICAgJyhlcXxuZXxjc3xjY3xtaXxwbHx2c3x2Y3xoaXxsc3xnZXxsdHxndHxsZXxhbHxoc3xsbyk/JyArIC8vIGNvbmRpdGlvbiBjb2Rlc1xuICAgICAgICAnW3NwdHJ4XT8nICsgLy8gbGVnYWwgcG9zdGZpeGVzXG4gICAgICAgICcoPz1cXFxccyknIC8vIGZvbGxvd2VkIGJ5IHNwYWNlXG4gICAgICB9LFxuICAgICAgQ09NTUVOVCxcbiAgICAgIGhsanMuUVVPVEVfU1RSSU5HX01PREUsXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3N0cmluZycsXG4gICAgICAgIGJlZ2luOiAnXFwnJyxcbiAgICAgICAgZW5kOiAnW15cXFxcXFxcXF1cXCcnLFxuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3RpdGxlJyxcbiAgICAgICAgYmVnaW46ICdcXFxcfCcsXG4gICAgICAgIGVuZDogJ1xcXFx8JyxcbiAgICAgICAgaWxsZWdhbDogJ1xcXFxuJyxcbiAgICAgICAgcmVsZXZhbmNlOiAwXG4gICAgICB9LFxuICAgICAge1xuICAgICAgICBjbGFzc05hbWU6ICdudW1iZXInLFxuICAgICAgICB2YXJpYW50czogW1xuICAgICAgICAgIHsgLy8gaGV4XG4gICAgICAgICAgICBiZWdpbjogJ1sjJD1dPzB4WzAtOWEtZl0rJ1xuICAgICAgICAgIH0sXG4gICAgICAgICAgeyAvLyBiaW5cbiAgICAgICAgICAgIGJlZ2luOiAnWyMkPV0/MGJbMDFdKydcbiAgICAgICAgICB9LFxuICAgICAgICAgIHsgLy8gbGl0ZXJhbFxuICAgICAgICAgICAgYmVnaW46ICdbIyQ9XVxcXFxkKydcbiAgICAgICAgICB9LFxuICAgICAgICAgIHsgLy8gYmFyZSBudW1iZXJcbiAgICAgICAgICAgIGJlZ2luOiAnXFxcXGJcXFxcZCsnXG4gICAgICAgICAgfVxuICAgICAgICBdLFxuICAgICAgICByZWxldmFuY2U6IDBcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIGNsYXNzTmFtZTogJ3N5bWJvbCcsXG4gICAgICAgIHZhcmlhbnRzOiBbXG4gICAgICAgICAgeyAvLyBHTlUgQVJNIHN5bnRheFxuICAgICAgICAgICAgYmVnaW46ICdeWyBcXFxcdF0qW2Etel9cXFxcLlxcXFwkXVthLXowLTlfXFxcXC5cXFxcJF0rOidcbiAgICAgICAgICB9LFxuICAgICAgICAgIHsgLy8gQVJNIHN5bnRheFxuICAgICAgICAgICAgYmVnaW46ICdeW2Etel9cXFxcLlxcXFwkXVthLXowLTlfXFxcXC5cXFxcJF0rJ1xuICAgICAgICAgIH0sXG4gICAgICAgICAgeyAvLyBsYWJlbCByZWZlcmVuY2VcbiAgICAgICAgICAgIGJlZ2luOiAnWz0jXVxcXFx3KydcbiAgICAgICAgICB9XG4gICAgICAgIF0sXG4gICAgICAgIHJlbGV2YW5jZTogMFxuICAgICAgfVxuICAgIF1cbiAgfTtcbn1cblxubW9kdWxlLmV4cG9ydHMgPSBhcm1hc207XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=